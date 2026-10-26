"""S3.1C pre-2022, same-trajectory checkpoint diagnostics on joint loss.

Internal TRAIN targets <2020, MONITOR 2020–2021. Neither external dev
2022–25 nor the 2026 holdout are loaded. NO trades, no return backtest.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import time
from datetime import datetime,timezone

import numpy as np
import torch

from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.models import ContinuousDirectionModel,forecast_prices
from research.continuous_direction.runner import _arrays,_source_code_commit
from research.continuous_direction.diagnostics import prior_from_train,probability_report
from research.representation_ablation.runner import _paired_base_scores
from research.scaling_study.metrics import score_forecasts
from research.token_grammar.internal_cohorts import collect_pre2022,validate_internal
from research.token_grammar.learned_embeddings import (
    CausalTokenProvider,TokenScalarModel,_sha_params,
)

ARMS=("decoded","embedding_ordered","embedding_random")
CHECKPOINTS=(200,800,2000)
GRAMMAR="signed_quantile_g2"


def _sample_loss(model,x,y,*,batch_size=64):
    model.eval()
    weighted=0.
    with torch.no_grad():
        for start in range(0,len(y),batch_size):
            yb=y[start:start+batch_size]
            l=model.loss(x[start:start+batch_size],yb)
            if not bool(torch.isfinite(l)):
                raise ArithmeticError("nonfinite fixed internal monitor loss")
            weighted+=float(l)*len(yb)
    return weighted/len(y)


def _forecast(model,x,anchors,*,scale):
    price=[]
    logits=[]
    reg=[]
    for start in range(0,len(anchors),64):
        p,prob,mu=forecast_prices(model,x[start:start+64],
                        anchors[start:start+64],scale_bps=float(scale))
        price.extend(p.tolist())
        logits.extend(prob.tolist())
        reg.extend(mu.tolist())
    return np.asarray(price),np.asarray(logits),np.asarray(reg)


def run_cases(train,monitor,*,interval,
              arms=ARMS,seeds=(20261025,20261026,20261027),
              checkpoints=CHECKPOINTS,batch_size=16,
              width=16,depth=1,data_origin="ARTIFICIAL_FIXTURE"):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 only")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("invalid data origin")
    if (not arms or len(arms)!=len(set(arms)) or any(a not in ARMS for a in arms)
            or not seeds or len(seeds)>5 or len(set(seeds))!=len(seeds)
            or any(type(seed)!=int for seed in seeds)
            or not checkpoints or tuple(sorted(set(checkpoints)))!=tuple(checkpoints)
            or any(type(k)!=int or not 1<=k<=2000 for k in checkpoints)
            or type(width)!=int or width<8 or width%4
            or type(depth)!=int or depth not in (1,2)
            or type(batch_size)!=int or not 1<=batch_size<=256):
        raise ValueError("invalid preregistered convergence grid")
    if len(train)<32 or len(monitor)<32:
        raise ValueError("internal sample cohorts must each contain >=32")
    split=validate_internal(train,monitor)
    source_commit=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    centers=provider.centers(GRAMMAR)
    train_ids=provider.ids(train,GRAMMAR)
    monitor_ids=provider.ids(monitor,GRAMMAR)
    inputs_train=torch.as_tensor(train_ids,dtype=torch.int64)
    inputs_monitor=torch.as_tensor(monitor_ids,dtype=torch.int64)
    scale=float(np.std(np.asarray([c.continuous_past_bps for c in train],
                                     dtype=np.float64)))
    if not math.isfinite(scale) or scale<=1e-8:
        scale=1.
    numeric_train=torch.as_tensor(centers[train_ids]/scale,dtype=torch.float64)
    numeric_monitor=torch.as_tensor(centers[monitor_ids]/scale,dtype=torch.float64)
    _past,_,_,ytrain=_arrays(train)
    _past,mon_anchor,mon_actual,ymonitor=_arrays(monitor)
    y=torch.as_tensor(ytrain/scale,dtype=torch.float64)
    ym=torch.as_tensor(ymonitor/scale,dtype=torch.float64)
    train_indices=np.linspace(0,len(train)-1,min(256,len(train)),
                              dtype=np.int64)
    train_fixed=torch.as_tensor(train_indices,dtype=torch.int64)
    baselines,thresholds,_,_=_paired_base_scores(train,monitor)
    prior=prior_from_train(train)
    torch.set_num_threads(1)
    evaluations=[]
    trajectories=[]
    for seed in seeds:
        batch_rng=np.random.default_rng(seed)
        batches=[batch_rng.integers(0,len(train),size=batch_size)
                 for _ in range(checkpoints[-1])]
        for arm in arms:
            torch.manual_seed(seed)
            if arm=="decoded":
                model=ContinuousDirectionModel(
                    width=width,depth=depth,context=20,mode="joint")
                backbone_sha=_sha_params(model)
                embedded_params=0
                xtrain=numeric_train
                xmonitor=numeric_monitor
            else:
                model=TokenScalarModel(
                    width=width,depth=depth,mode="joint",
                    init_style="ordered" if arm=="embedding_ordered"
                               else "random",
                    centers_bps=centers,scale_bps=scale)
                backbone_sha=model.backbone_initial_sha256
                embedded_params=11
                xtrain=inputs_train
                xmonitor=inputs_monitor
            optim=torch.optim.AdamW(model.parameters(),lr=.003,
                                    weight_decay=.001)
            start_time=time.perf_counter()
            prev=0
            all_grads=[]
            clipped=0
            latest_loss=None
            for step,batch in enumerate(batches,start=1):
                model.train()
                optim.zero_grad(set_to_none=True)
                loss=model.loss(xtrain[batch],y[batch])
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite minibatch loss")
                loss.backward()
                pre_clip=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
                if not bool(torch.isfinite(pre_clip)):
                    raise ArithmeticError("nonfinite gradient norm")
                g=float(pre_clip)
                all_grads.append(g)
                clipped+=int(g>5.)
                optim.step()
                latest_loss=float(loss.detach())
                if step not in checkpoints:
                    continue
                trainloss=_sample_loss(
                    model,xtrain[train_fixed],y[train_fixed])
                monitorloss=_sample_loss(model,xmonitor,ym)
                forecast,prob,raw_mu=_forecast(
                    model,xmonitor,mon_anchor,scale=scale)
                scores=score_forecasts(
                    mon_anchor,mon_actual,forecast,
                    train_thresholds=thresholds)
                classification=probability_report(
                    mon_anchor,mon_actual,prob,train_prior=prior)
                classification["head_regression_sign_disagreement"]=float(
                    np.mean((prob>=.5)!=(raw_mu>=0)))
                recent=all_grads[prev:step]
                row={
                    "arm":arm,"seed":seed,"checkpoint_steps":step,
                    "total_training_updates_so_far":step,
                    "same_optimizer_continued":True,
                    "width":width,"depth":depth,"mode":"joint",
                    "grammar":GRAMMAR,
                    "parameter_count":sum(p.numel() for p in model.parameters()),
                    "embedding_trainable_parameters":embedded_params,
                    "backbone_initial_sha256":backbone_sha,
                    "train_normalizer_std_bps":scale,
                    "train_sample_fixed_count":len(train_fixed),
                    "train_fixed_joint_loss":trainloss,
                    "monitor_joint_loss":monitorloss,
                    "last_minibatch_loss":latest_loss,
                    "gradient_norm_before_clip_mean":float(np.mean(recent)),
                    "gradient_norm_before_clip_max":float(np.max(recent)),
                    "gradient_clip_fraction_cumulative":clipped/step,
                    "cpu_training_seconds_cumulative":time.perf_counter()-start_time,
                    "forecast_rows":len(monitor),
                    **scores,**classification,
                }
                evaluations.append(row)
                prev=step
            trajectories.append({
                "seed":seed,"arm":arm,"training_updates":len(batches),
                "checkpoint_count":len(checkpoints),
                "parameter_count":sum(p.numel() for p in model.parameters()),
                "backbone_initial_sha256":backbone_sha,
            })
    return {
        "experiment":"TRAME_S3_1C_PRE2022_CONVERGENCE_V1",
        "interval":interval,"data_origin":data_origin,
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "train_label_cutoff_exclusive":"2020-01-01",
        "internal_monitor_label_years":"2020-2021",
        "external_dev_2022_2025_opened":False,
        "labels_2026_opened":False,
        "independent_test_used":False,
        "internal_monitor_never_backpropagated":True,
        "token_quantiles_fit_train_only":True,
        "scale_and_prior_fit_train_only":True,
        "sampled_context_windows_overlap":True,
        "checkpoint_evaluations_not_independent_runs":True,
        "learned_has_11_extra_parameters":True,
        "ordered_random_exact_parameter_match":True,
        "no_trading_or_portfolio_pnl":True,
        "transaction_costs_ignored":True,
        "model_source_commit":source_commit,
        "github_workflow_sha":os.environ.get("GITHUB_SHA","none"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "train_cases":len(train),"monitor_cases":len(monitor),
        **split,
        "grammar":GRAMMAR,"quantile_boundaries_train_bps":
            list(provider.quantile_boundaries_bps),
        "input_and_target_train_scale_bps":scale,
        "direction_prior_train_only":prior,
        "baseline_scores_train_fit_monitor_evaluated":baselines,
        "arms":list(arms),"seeds":list(seeds),
        "checkpoints":list(checkpoints),
        "trajectories":trajectories,
        "evaluations":evaluations,
    }


def run_history(*,interval,directory=ROOT,
                seeds=(20261025,20261026,20261027),
                checkpoints=CHECKPOINTS,arms=ARMS,
                max_train=4096,max_monitor=1024,
                data_origin="BTC_PUBLIC_REAL"):
    cohort,provenance=collect_pre2022(
        interval,directory,max_train=max_train,
        max_monitor=max_monitor)
    result=run_cases(cohort["train"],cohort["monitor"],
                     interval=interval,arms=arms,
                     seeds=seeds,checkpoints=checkpoints,
                     data_origin=data_origin)
    result["sampling_provenance"]=provenance
    return result


def main(argv=None):
    p=argparse.ArgumentParser(
        description="TRAME S3.1C internal pre2022 convergence diagnostic")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--arms",nargs="+",choices=ARMS,default=list(ARMS))
    p.add_argument("--seeds",nargs="+",type=int,
                   default=[20261025,20261026,20261027])
    p.add_argument("--checkpoints",nargs="+",type=int,
                   default=list(CHECKPOINTS))
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("refuse to overwrite existing evidence")
    report=run_history(interval=a.interval,directory=a.directory,
              arms=tuple(a.arms),seeds=tuple(a.seeds),
              checkpoints=tuple(a.checkpoints))
    a.output.write_text(json.dumps(report,indent=2,
                        allow_nan=False)+"\n",encoding="utf-8")
    print("S3.1C PRE2022 ONLY, no external development, 2026 unopened")


if __name__=="__main__":
    main()
