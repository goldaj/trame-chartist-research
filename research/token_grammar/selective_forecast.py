"""S3.1G train-only predicted movement magnitude conditional reliability.

9 legacy-trained BTC models, 2000 updates. Four TRAIN-fitted absolute HARD
forecast thresholds, then the SAME MONITOR rows scored using HARD/DIRECT/SOFT
pricing on the SAME model. No 2022-25 dev, 2026 holdout, trades or PnL.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
import math
import os
from pathlib import Path
import platform
import time
import hashlib

import numpy as np
import torch

from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.models import ContinuousDirectionModel,forecast_prices
from research.continuous_direction.runner import _arrays,_origin_digest,_source_code_commit
from research.continuous_direction.diagnostics import prior_from_train,probability_report
from research.representation_ablation.runner import features as continuous_features
from research.scaling_study.metrics import (
    score_forecasts,training_magnitude_thresholds)
from research.token_grammar.convergence import collect_internal,split_internal_pre2022
from research.token_grammar.learned_embeddings import CausalTokenProvider,_sha_params
from research.token_grammar.inference_ablation import (
    RULES,inference_rule_prices)

QUANTILES=(("all",0.),("q50",.50),("q75",.75),("q90",.90))
MAX_STEPS=2000
MIN_INFORMATIVE_CASES=30


def eligible_masks(train_abs_hard_bps,monitor_abs_hard_bps):
    train=np.asarray(train_abs_hard_bps,dtype=np.float64)
    mon=np.asarray(monitor_abs_hard_bps,dtype=np.float64)
    if (train.ndim!=1 or len(train)<32 or mon.ndim!=1 or len(mon)<1
        or not np.isfinite(train).all() or not np.isfinite(mon).all()
        or np.any(train<0) or np.any(mon<0)):
        raise ValueError("only finite nonnegative TRAIN and MONITOR predicted amplitude arrays")
    thresholds={}
    masks={}
    for name,q in QUANTILES:
        threshold=0. if name=="all" else float(np.quantile(train,q))
        thresholds[name]=threshold
        masks[name]=(mon>=threshold)
    if not np.all(masks["all"]):
        raise AssertionError("all-case rule must keep the entire monitor")
    if not (np.all(masks["q90"]<=masks["q75"])
            and np.all(masks["q75"]<=masks["q50"])):
        raise AssertionError("selection not nested")
    return thresholds,masks


def _predictions(model,x,anchors,scale):
    anchor=np.asarray(anchors,dtype=np.float64)
    if len(x)!=len(anchor) or len(x)<1:
        raise ValueError("aligned nonempty model inputs required")
    up=[];mu=[];hard=[]
    for i in range(0,len(x),64):
        pr,p,r=forecast_prices(
            model,x[i:i+64],anchor[i:i+64],scale_bps=float(scale))
        hard.extend(pr.tolist());up.extend(p.tolist());mu.extend(r.tolist())
    rules=inference_rule_prices(np.asarray(mu),np.asarray(up),anchor,
                                 scale_bps=scale)
    np.testing.assert_array_equal(rules["joint_hard"],np.asarray(hard))
    return np.asarray(mu),np.asarray(up),rules


def selected_metrics(anchors,actuals,price,mask,*,train_thresholds,
                     train_prior,head_probabilities):
    n=int(np.sum(mask))
    total=len(mask)
    if n==0:
        return {"n_selected":0,"n_monitor":total,"coverage":0.,
                "status":"NO_COVERAGE","balanced_direction_accuracy":None,
                "n_actual_up":0,"n_actual_down":0,"n_actual_flat":0,
                "n_predicted_up":0,"n_predicted_down":0,"n_predicted_flat":0,
                "direction_accuracy_all":None,
                "direction_accuracy_nonflat_truth":None,
                "mae_native_usd":None,"mae_bps_anchor":None,
                "absolute_magnitude_error_bps":None,
                "signed_forecast_bias_bps":None,
                "mean_abs_predicted_move_bps":None,
                "mean_abs_actual_move_bps":None,
                "magnitude_ratio_predicted_over_realized":None,
                "persistence_mae_native_usd":None,
                "persistence_mae_bps_anchor":None,
                "brier_skill_vs_train_prior_head_diagnostic":None,
                "n_nonflat_probability_cases":0}
    a=np.asarray(anchors,dtype=float)[mask]
    y=np.asarray(actuals,dtype=float)[mask]
    p=np.asarray(price,dtype=float)[mask]
    score=score_forecasts(a,y,p,train_thresholds=train_thresholds)
    baseline=score_forecasts(a,y,a,train_thresholds=train_thresholds)
    calibration=probability_report(
        a,y,np.asarray(head_probabilities,dtype=float)[mask],
        train_prior=train_prior)
    truthful_both=score["n_up_actual"]>0 and score["n_down_actual"]>0
    informative=bool(n>=MIN_INFORMATIVE_CASES and truthful_both)
    return {
        "status":"INFORMATIVE" if informative else "INSUFFICIENT_COVERAGE_OR_CLASS",
        "n_selected":n,"n_monitor":total,"coverage":n/total,
        "n_actual_up":score["n_up_actual"],
        "n_actual_down":score["n_down_actual"],
        "n_actual_flat":score["n_flat_actual"],
        "n_predicted_up":score["n_predicted_up"],
        "n_predicted_down":score["n_predicted_down"],
        "n_predicted_flat":score["n_predicted_flat"],
        "balanced_direction_accuracy":score["balanced_direction_accuracy"]
              if informative else None,
        "direction_accuracy_all":score["direction_accuracy_all"],
        "direction_accuracy_nonflat_truth":score["direction_accuracy_nonflat_truth"],
        "mae_native_usd":score["mae_native_usd"],
        "mae_bps_anchor":score["mae_bps_anchor"],
        "absolute_magnitude_error_bps":score["absolute_magnitude_error_bps"],
        "signed_forecast_bias_bps":score["signed_forecast_bias_bps"],
        "mean_abs_predicted_move_bps":score["mean_abs_predicted_move_bps"],
        "mean_abs_actual_move_bps":score["mean_abs_actual_move_bps"],
        "magnitude_ratio_predicted_over_realized":(
            score["mean_abs_predicted_move_bps"]/score["mean_abs_actual_move_bps"]
            if score["mean_abs_actual_move_bps"]>0 else None),
        "persistence_mae_native_usd":baseline["mae_native_usd"],
        "persistence_mae_bps_anchor":baseline["mae_bps_anchor"],
        "brier_skill_vs_train_prior_head_diagnostic":
             calibration["brier_skill_vs_train_prior"],
        "n_nonflat_probability_cases":calibration["nonflat_probability_cases"],
    }


def run_cases(train,monitor,*,interval,
              seeds=(20261025,20261026,20261027),
              training_steps=MAX_STEPS,
              data_origin="ARTIFICIAL_FIXTURE",
              engineering_canary=False):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1 H1 M1 only")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("invalid real source provenance")
    if (not seeds or len(set(seeds))!=len(seeds)
        or any(type(s)!=int for s in seeds)
        or type(training_steps)!=int or training_steps<1
        or training_steps>MAX_STEPS):
        raise ValueError("invalid model seed/step")
    if (data_origin=="BTC_PUBLIC_REAL"
        and training_steps!=MAX_STEPS
        and not (engineering_canary and training_steps==40)):
        raise ValueError("real data only 2000 preregistered or 40-step engineering smoke")
    a,b=split_internal_pre2022(train+monitor)
    if len(a)!=len(train) or len(b)!=len(monitor):
        raise ValueError("training/monitor label time leak")
    train,monitor=a,b
    source_sha=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    scale=float(np.std(continuous_features(train,"continuous_bps")))
    if not math.isfinite(scale) or scale<=1e-8:scale=1.
    center=provider.centers("signed_quantile_g2")
    ti=provider.ids(train,"signed_quantile_g2")
    mi=provider.ids(monitor,"signed_quantile_g2")
    xt=torch.as_tensor(center[ti]/scale,dtype=torch.float64)
    xm=torch.as_tensor(center[mi]/scale,dtype=torch.float64)
    _,_,_,ytrain=_arrays(train)
    yt=torch.as_tensor(ytrain/scale,dtype=torch.float64)
    train_anchor=np.asarray([c.anchor_usd for c in train],dtype=float)
    mon_anchor=np.asarray([c.anchor_usd for c in monitor],dtype=float)
    mon_actual=np.asarray([c.target_usd for c in monitor],dtype=float)
    thresholds_train_true=training_magnitude_thresholds(train)
    prior=prior_from_train(train)
    torch.set_num_threads(1)
    output=[]
    trajectories=[]
    for seed in seeds:
        torch.manual_seed(seed)
        model=ContinuousDirectionModel(
            width=16,depth=1,context=20,mode="joint")
        init_sha=_sha_params(model)
        rng=np.random.default_rng(seed)
        batches=[rng.integers(0,len(train),size=16)
                 for _ in range(training_steps)]
        optimizer=torch.optim.AdamW(
            model.parameters(),lr=.003,weight_decay=.001)
        started=time.perf_counter()
        for ids in batches:
            model.train()
            optimizer.zero_grad(set_to_none=True)
            loss=model.loss(xt[ids],yt[ids])
            if not bool(torch.isfinite(loss)):
                raise ArithmeticError("nonfinite legacy loss")
            loss.backward()
            grad=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
            if not bool(torch.isfinite(grad)):
                raise ArithmeticError("nonfinite model gradients")
            optimizer.step()
        _,_,train_prices=_predictions(model,xt,train_anchor,scale)
        monitor_mu,monitor_prob,monitor_prices=_predictions(
            model,xm,mon_anchor,scale)
        # HARD model magnitude = abs(mu), same train & monitor model.
        abs_train=np.abs(np.log(train_prices["joint_hard"]/train_anchor)*10000)
        abs_monitor=np.abs(monitor_mu)
        cutoffs,masks=eligible_masks(abs_train,abs_monitor)
        for name,_ in QUANTILES:
            mask=masks[name]
            # Each threshold computed only on TRAIN predicted movement.
            # All three rules must be scored on identical selected rows.
            selection_sha=hashlib.sha256(
                np.flatnonzero(mask).astype("<i8").tobytes()).hexdigest()
            for rule in RULES:
                metrics=selected_metrics(
                    mon_anchor,mon_actual,monitor_prices[rule],mask,
                    train_thresholds=thresholds_train_true,
                    train_prior=prior,head_probabilities=monitor_prob)
                output.append({
                    "interval":interval,"seed":seed,
                    "rule":rule,"threshold":name,
                    "quantile_fit_only_on_training_predictions":True,
                    "threshold_train_bps":cutoffs[name],
                    "selection_sha256":selection_sha,
                    "same_weights_three_rules":True,
                    "initial_weights_sha256":init_sha,
                    "model_parameters":sum(p.numel() for p in model.parameters()),
                    "model_steps":training_steps,
                    "head_probabilities_diagnostic_only_for_direct":
                      rule=="signed_direct_mu",
                    **metrics,
                })
        trajectories.append({
            "seed":seed,"trained_models":1,"steps":training_steps,
            "same_weights_sha256":init_sha,
            "train_prediction_thresholds_bps":cutoffs,
            "elapsed_train_seconds":time.perf_counter()-started,
        })
    return {
        "experiment":"TRAME_S3_1G_TRAIN_ONLY_SELECTIVE_MAGNITUDE_V1",
        "data_origin":data_origin,"interval":interval,
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "train_labels_before":"2020-01-01",
        "monitor_labels_years":"2020-2021",
        "external_2022_2025_used":False,
        "holdout_2026_used":False,
        "only_train_predictions_define_cutoffs":True,
        "all_rules_same_monitored_subset":True,
        "only_hard_pred_magnitude_gates":True,
        "no_monitor_optimized_thresholds":True,
        "shared_backbone_and_loss_s3f":True,
        "not_independent_test":True,
        "no_cumulative_portfolio_pnl":True,
        "transaction_costs_ignored":True,
        "engineering_canary_not_scientific_selection":bool(engineering_canary),
        "thresholds":[x[0] for x in QUANTILES],
        "rules":list(RULES),
        "seeds":list(seeds),"training_steps":training_steps,
        "min_informative_cases":MIN_INFORMATIVE_CASES,
        "train_count":len(train),"monitor_count":len(monitor),
        "train_origins_sha256":_origin_digest(train),
        "monitor_origins_sha256":_origin_digest(monitor),
        "model_source_commit":source_sha,
        "github_workflow_sha":os.environ.get("GITHUB_SHA","not in CI"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "train_only_prior":prior,
        "g2_quantiles_train_only_bps":list(provider.quantile_boundaries_bps),
        "train_normalizer_std_bps":scale,
        "trajectories":trajectories,"results":output,
    }


def run_history(*,interval,directory=ROOT,
                seeds=(20261025,20261026,20261027),
                training_steps=MAX_STEPS,engineering_canary=False):
    train,monitor,inventory=collect_internal(interval,Path(directory))
    result=run_cases(train,monitor,interval=interval,
                     seeds=seeds,training_steps=training_steps,
                     engineering_canary=engineering_canary,
                     data_origin="BTC_PUBLIC_REAL")
    result["sampling_information"]=inventory
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="S3.1G true train-only selective price reliability")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--seeds",nargs="+",type=int,
                   default=[20261025,20261026,20261027])
    p.add_argument("--steps",type=int,default=MAX_STEPS)
    p.add_argument("--engineering-canary",action="store_true")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("refusing overwrite")
    r=run_history(interval=a.interval,directory=a.directory,seeds=tuple(a.seeds),
                  training_steps=a.steps,engineering_canary=a.engineering_canary)
    a.output.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("TRAME S3.1G, thresholds TRAIN-only, 2022-26 sealed, no trading")
if __name__=="__main__":
    main()
