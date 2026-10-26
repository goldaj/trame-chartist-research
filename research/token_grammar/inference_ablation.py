"""TRAME S3.1F - compare 3 pricing rules on exactly the SAME trained weights.

ONE legacy training trajectory per interval/seed, 3 rule evaluations at EACH
checkpoint. No post-2021 labels or candles loaded. No trades or PnL.
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

import numpy as np
import torch

from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.models import (
    ContinuousDirectionModel,forecast_prices)
from research.continuous_direction.runner import (
    _arrays,_origin_digest,_source_code_commit)
from research.continuous_direction.diagnostics import (
    prior_from_train,probability_report)
from research.representation_ablation.runner import features as continuous_features
from research.scaling_study.metrics import (
    training_magnitude_thresholds,baseline_forecasts,score_forecasts)
from research.token_grammar.convergence import (
    collect_internal,split_internal_pre2022,CHECKPOINTS)
from research.token_grammar.learned_embeddings import CausalTokenProvider,_sha_params

RULES=("joint_hard","signed_direct_mu","joint_soft_tanh")


def inference_rule_prices(mu_bps,probabilities,anchors,*,scale_bps):
    mu=np.asarray(mu_bps,dtype=np.float64)
    prob=np.asarray(probabilities,dtype=np.float64)
    a=np.asarray(anchors,dtype=np.float64)
    if (mu.ndim!=1 or a.shape!=mu.shape or prob.shape!=mu.shape
        or not np.isfinite(mu).all() or not np.isfinite(prob).all()
        or not np.isfinite(a).all() or np.any(a<=0)
        or np.any((prob<0)|(prob>1))
        or type(scale_bps) not in (float,int)
        or not math.isfinite(scale_bps) or scale_bps<=0):
        raise ValueError("bad aligned model outputs and anchor prices")
    returns={
        "joint_hard":np.where(prob>=.5,1.,-1.)*np.abs(mu),
        "signed_direct_mu":mu,
        "joint_soft_tanh":(2*prob-1.)*np.abs(mu),
    }
    results={}
    for rule,bps in returns.items():
        if np.any(np.abs(bps)>100000):
            raise ArithmeticError("implausible return, refuse clipping")
        price=a*np.exp(bps/10000.)
        if not np.isfinite(price).all() or np.any(price<=0):
            raise ArithmeticError("invalid price from rule")
        results[rule]=price
    return results


def evaluate_same_weights(model,x,monitor,*,scale,thresholds,prior):
    a=np.asarray([c.anchor_usd for c in monitor],dtype=float)
    actual=np.asarray([c.target_usd for c in monitor],dtype=float)
    preds=[]
    ups=[]
    raw_mu=[]
    for start in range(0,len(monitor),64):
        sl=slice(start,start+64)
        pr,up,mu=forecast_prices(
            model,x[sl],a[sl],scale_bps=float(scale))
        preds.extend(pr.tolist())
        ups.extend(up.tolist())
        raw_mu.extend(mu.tolist())
    prob=np.asarray(ups)
    mu_bps=np.asarray(raw_mu)
    forecasts=inference_rule_prices(mu_bps,prob,a,scale_bps=scale)
    np.testing.assert_allclose(
        forecasts["joint_hard"],np.asarray(preds),rtol=0,atol=0,
        err_msg="S3.1F HARD rule must reproduce original product exactly")
    brier=probability_report(a,actual,prob,train_prior=prior)
    mismatch=float(np.mean((mu_bps>=0)!=(prob>=.5)))
    rows={}
    for rule,price in forecasts.items():
        values=score_forecasts(a,actual,price,train_thresholds=thresholds)
        values["predicted_up_percent"]=float(
            100*values["n_predicted_up"]/values["forecast_rows"])
        values["monoclasse_99pct"]=bool(
            max(values["n_predicted_up"],values["n_predicted_down"])
                /values["forecast_rows"]>=.99)
        values["head_sign_disagreement_fraction"]=mismatch
        values["head_brier_diagnostic_only"]=bool(rule!="joint_hard")
        values["head_brier_score"]=brier["brier_nonflat"]
        values["head_brier_skill_vs_train_prior"]=brier["brier_skill_vs_train_prior"]
        values["head_probabilities_not_rule_calibrated_for_direct"]=(
            rule=="signed_direct_mu")
        rows[rule]=values
    return rows


def run_cases(train,monitor,*,interval,
              seeds=(20261025,20261026,20261027),
              checkpoints=CHECKPOINTS,batch_size=16,
              data_origin="ARTIFICIAL_FIXTURE",engineering_canary=False):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1 H1 or M1 expected")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("unexpected BTC provenance")
    if (not seeds or len(set(seeds))!=len(seeds)
        or any(type(s)!=int for s in seeds)
        or not checkpoints or tuple(sorted(set(checkpoints)))!=tuple(checkpoints)
        or any(type(k)!=int or not 1<=k<=2000 for k in checkpoints)
        or type(batch_size)!=int or not 1<=batch_size<=256):
        raise ValueError("invalid train budget")
    if (data_origin=="BTC_PUBLIC_REAL"
        and tuple(checkpoints)!=CHECKPOINTS
        and not (engineering_canary and tuple(checkpoints)==(10,20,40))):
        raise ValueError("BTC study preregistered at 200/800/2000")
    a,b=split_internal_pre2022(train+monitor)
    if len(a)!=len(train) or len(b)!=len(monitor):
        raise ValueError("wrong internal chronological cohorts")
    train,monitor=a,b
    source_sha=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    scale=float(np.std(continuous_features(train,"continuous_bps")))
    if not math.isfinite(scale) or scale<=1e-8:scale=1.
    center=provider.centers("signed_quantile_g2")
    train_id=provider.ids(train,"signed_quantile_g2")
    monitor_id=provider.ids(monitor,"signed_quantile_g2")
    xt=torch.as_tensor(center[train_id]/scale,dtype=torch.float64)
    xm=torch.as_tensor(center[monitor_id]/scale,dtype=torch.float64)
    _,_,_,ytrain=_arrays(train)
    yt=torch.as_tensor(ytrain/scale,dtype=torch.float64)
    threshold=training_magnitude_thresholds(train)
    prior=prior_from_train(train)
    ma=np.asarray([c.anchor_usd for c in monitor],dtype=float)
    my=np.asarray([c.target_usd for c in monitor],dtype=float)
    baselines={
        n:score_forecasts(ma,my,forecast,train_thresholds=threshold)
        for n,forecast in baseline_forecasts(monitor).items()}
    torch.set_num_threads(1)
    trajectories=[]
    checkpoints_rows=[]
    for seed in seeds:
        torch.manual_seed(seed)
        model=ContinuousDirectionModel(width=16,depth=1,context=20,mode="joint")
        initial_sha=_sha_params(model)
        parameters=sum(p.numel() for p in model.parameters())
        rng=np.random.default_rng(seed)
        batches=[rng.integers(0,len(train),size=batch_size)
                 for _ in range(checkpoints[-1])]
        optimizer=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.001)
        started=time.perf_counter()
        grad_hist=[]
        for step,batch in enumerate(batches,1):
            model.train()
            optimizer.zero_grad(set_to_none=True)
            # This is exactly legacy S3.1E's loss, not a new training arm.
            loss=model.loss(xt[batch],yt[batch])
            if not bool(torch.isfinite(loss)):
                raise ArithmeticError("nonfinite legacy regression/BCE loss")
            loss.backward()
            g=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
            if not bool(torch.isfinite(g)):
                raise ArithmeticError("nonfinite gradient")
            grad_hist.append(float(g))
            optimizer.step()
            if step not in checkpoints:
                continue
            variants=evaluate_same_weights(
                model,xm,monitor,scale=scale,
                thresholds=threshold,prior=prior)
            recent=grad_hist[-min(50,len(grad_hist)):]
            for rule,score in variants.items():
                checkpoints_rows.append({
                    "interval":interval,"seed":seed,"step":step,
                    "rule":rule,"same_model_weights":True,
                    "trained_once_no_reinitialisation":True,
                    "legacy_loss_unchanged":True,
                    "backbone_initial_sha256":initial_sha,
                    "parameter_count":parameters,
                    "normalizer_std_bps_train_only":scale,
                    "last_train_minibatch_loss":float(loss.detach()),
                    "gradient_norm_last50_mean":float(np.mean(recent)),
                    "cpu_training_seconds_since_start":time.perf_counter()-started,
                    **score,
                })
        trajectories.append({"seed":seed,
                             "trained_steps":checkpoints[-1],
                             "model_init_sha256":initial_sha,
                             "parameters":parameters,
                             "checkpoint_count":len(checkpoints)})
    return {
        "experiment":"TRAME_S3_1F_INFERENCE_ONLY_RULE_ABLATION_V1",
        "interval":interval,"data_origin":data_origin,
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "train_labels_before":"2020-01-01",
        "monitor_labels_years":"2020-2021",
        "external_dev_2022_2025_accessed":False,
        "holdout_2026_accessed":False,
        "train_only_codec_normalizer_prior":True,
        "one_model_shared_by_three_pricing_rules":True,
        "hard_reproduces_existing_forecast_prices_exactly":True,
        "same_checkpoint_for_all_rules":True,
        "head_probabilities_do_not_calibrate_direct_mu_sign":True,
        "checkpoints_not_independent_models":True,
        "independent_test":False,
        "no_portfolio_pnl":True,
        "transaction_costs_ignored":True,
        "engineering_canary_not_scientific_selection":bool(engineering_canary),
        "rules":list(RULES),"seeds":list(seeds),
        "checkpoints":list(checkpoints),
        "train_count":len(train),"monitor_count":len(monitor),
        "train_origins_sha256":_origin_digest(train),
        "monitor_origins_sha256":_origin_digest(monitor),
        "train_only_prior":prior,
        "g2_train_quantile_boundaries_bps":
            list(provider.quantile_boundaries_bps),
        "train_normalizer_std_bps":scale,
        "baseline_scores":baselines,
        "model_source_commit":source_sha,
        "github_workflow_sha":os.environ.get("GITHUB_SHA","not in Actions"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "trajectories":trajectories,"results":checkpoints_rows,
    }


def run_history(*,interval,directory=ROOT,
                seeds=(20261025,20261026,20261027),
                checkpoints=CHECKPOINTS,
                engineering_canary=False):
    train,monitor,inventory=collect_internal(interval,directory)
    result=run_cases(train,monitor,interval=interval,
                     seeds=seeds,checkpoints=checkpoints,
                     engineering_canary=engineering_canary,
                     data_origin="BTC_PUBLIC_REAL")
    result["sampling_information"]=inventory
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="S3.1F same-weight 3-rule BTC price ablation")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--seeds",nargs="+",type=int,
                   default=[20261025,20261026,20261027])
    p.add_argument("--checkpoints",nargs="+",type=int,default=list(CHECKPOINTS))
    p.add_argument("--engineering-canary",action="store_true")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("refuse existing file overwrite")
    res=run_history(interval=a.interval,directory=a.directory,
                    seeds=tuple(a.seeds),checkpoints=tuple(a.checkpoints),
                    engineering_canary=a.engineering_canary)
    a.output.write_text(json.dumps(res,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print("S3.1F same 9 legacy model weights, no external 2022-25/2026 accessed")


if __name__=="__main__":
    main()
