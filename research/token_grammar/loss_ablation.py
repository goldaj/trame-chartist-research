"""S3.1D controlled joint-loss ablation: direction weight vs magnitude term.

SAME model/grammar/20 past candles/weights/seed/batch order/forecast
reconciliation; only coefficients on BCE and |return| change. TRAIN labels
before 2020, internal MONITOR 2020-21, no external 2022-25 or 2026.
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
from torch.nn import functional as F

from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.models import ContinuousDirectionModel
from research.continuous_direction.runner import _arrays,_origin_digest,_source_code_commit
from research.continuous_direction.diagnostics import prior_from_train
from research.representation_ablation.runner import features as continuous_features
from research.scaling_study.metrics import (
    training_magnitude_thresholds,baseline_forecasts,score_forecasts)
from research.token_grammar.convergence import (
    collect_internal,split_internal_pre2022,_evaluate,CHECKPOINTS)
from research.token_grammar.learned_embeddings import CausalTokenProvider,_sha_params

OBJECTIVES={
    "reference":(0.50,0.00),
    "direction_025":(0.25,0.00),
    "direction_100":(1.00,0.00),
    "magnitude_025":(0.50,0.25),
    "magnitude_100":(0.50,1.00),
}
ARMS=tuple(OBJECTIVES)


def components(mu,logits,y):
    if (y.dtype!=torch.float64 or y.ndim!=1 or mu.shape!=y.shape
            or logits.shape!=y.shape or not bool(torch.isfinite(y).all())):
        raise ValueError("aligned finite normalized return targets needed")
    price=F.smooth_l1_loss(mu,y,beta=1.)
    magnitude=F.smooth_l1_loss(mu.abs(),y.abs(),beta=1.)
    nonflat=y!=0
    if bool(nonflat.any()):
        bce=F.binary_cross_entropy_with_logits(
            logits[nonflat],(y[nonflat]>0).to(torch.float64))
    else:
        bce=price.new_zeros(())
    return price,bce,magnitude


def objective(model,x,y,arm):
    if arm not in OBJECTIVES or model.mode!="joint":
        raise ValueError("wrong preregistered loss arm or output convention")
    mu,logits=model(x)
    price,bce,amp=components(mu,logits,y)
    direction_w,magnitude_w=OBJECTIVES[arm]
    return price+direction_w*bce+magnitude_w*amp


def _fixed_loss(model,x,y,arm):
    model.eval()
    n=len(y)
    if n==0:raise ValueError("empty fixed cohort")
    total=0.
    with torch.no_grad():
        for i in range(0,n,64):
            sl=slice(i,i+64)
            l=objective(model,x[sl],y[sl],arm)
            if not bool(torch.isfinite(l)):
                raise ArithmeticError("nonfinite fixed loss")
            total+=float(l)*len(y[sl])
    return total/n


def run_cases(train,monitor,*,interval,
              arms=ARMS,seeds=(20261025,20261026,20261027),
              checkpoints=CHECKPOINTS,batch_size=16,
              data_origin="ARTIFICIAL_FIXTURE",engineering_canary=False):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 only")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("unsupported source provenance")
    if (not arms or any(a not in ARMS for a in arms)
            or len(set(arms))!=len(arms)
            or not seeds or len(set(seeds))!=len(seeds)
            or any(type(s)!=int for s in seeds)
            or not checkpoints or tuple(sorted(set(checkpoints)))!=tuple(checkpoints)
            or any(type(c)!=int or not 1<=c<=2000 for c in checkpoints)
            or not 1<=batch_size<=256 or type(batch_size)!=int):
        raise ValueError("invalid objective ablation matrix")
    if (data_origin=="BTC_PUBLIC_REAL"
            and tuple(checkpoints)!=CHECKPOINTS
            and not (engineering_canary and tuple(checkpoints)==(10,20,40))):
        raise ValueError("real BTC study requires 200/800/2000 (engineering smoke 10/20/40 only)")
    a,b=split_internal_pre2022(train+monitor)
    if len(a)!=len(train) or len(b)!=len(monitor):
        raise ValueError("internal train and monitor must be in correct partitions")
    train,monitor=a,b
    source_sha=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    scale=float(np.std(continuous_features(train,"continuous_bps")))
    if not math.isfinite(scale) or scale<=1e-8:scale=1.
    centers=provider.centers("signed_quantile_g2")
    ids_train=provider.ids(train,"signed_quantile_g2")
    ids_monitor=provider.ids(monitor,"signed_quantile_g2")
    xt=torch.as_tensor(centers[ids_train]/scale,dtype=torch.float64)
    xm=torch.as_tensor(centers[ids_monitor]/scale,dtype=torch.float64)
    _past,_anchors,_actuals,labels_train=_arrays(train)
    _past,_anchors_m,_actuals_m,labels_monitor=_arrays(monitor)
    yt=torch.as_tensor(labels_train/scale,dtype=torch.float64)
    ym=torch.as_tensor(labels_monitor/scale,dtype=torch.float64)
    thresholds=training_magnitude_thresholds(train)
    prior=prior_from_train(train)
    anchor=np.asarray([c.anchor_usd for c in monitor],dtype=float)
    actual=np.asarray([c.target_usd for c in monitor],dtype=float)
    baselines={name:score_forecasts(
        anchor,actual,values,train_thresholds=thresholds)
        for name,values in baseline_forecasts(monitor).items()}
    rows=[]
    torch.set_num_threads(1)
    for seed in seeds:
        rng=np.random.default_rng(seed)
        common_batches=[rng.integers(0,len(train),size=batch_size)
                        for _ in range(checkpoints[-1])]
        for arm in arms:
            torch.manual_seed(seed)
            model=ContinuousDirectionModel(
                width=16,depth=1,context=20,mode="joint")
            initial_sha=_sha_params(model)
            opt=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.001)
            grads=[]
            started=time.perf_counter()
            last_loss=None
            for step,indices in enumerate(common_batches,1):
                model.train()
                opt.zero_grad(set_to_none=True)
                loss=objective(model,xt[indices],yt[indices],arm)
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite research objective")
                loss.backward()
                preclip=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
                if not bool(torch.isfinite(preclip)):
                    raise ArithmeticError("nonfinite objective gradients")
                grads.append(float(preclip))
                opt.step()
                last_loss=float(loss.detach())
                if step not in checkpoints:
                    continue
                monitor_objective=_fixed_loss(model,xm,ym,arm)
                monitor_common_reference=_fixed_loss(model,xm,ym,"reference")
                train_n=min(128,len(train))
                train_common_reference=_fixed_loss(
                    model,xt[:train_n],yt[:train_n],"reference")
                scores=_evaluate(
                    model,xm,monitor,scale=scale,
                    thresholds=thresholds,prior=prior)
                recent=grads[-min(50,len(grads)):]
                rows.append({
                    "interval":interval,"loss_arm":arm,
                    "direction_weight":OBJECTIVES[arm][0],
                    "magnitude_weight":OBJECTIVES[arm][1],
                    "seed":seed,"checkpoint_updates":step,
                    "model_checkpoint_continuing_same_optimizer":True,
                    "mode":"joint","width":16,"depth":1,
                    "backbone_initial_sha256":initial_sha,
                    "parameter_count":sum(p.numel() for p in model.parameters()),
                    "normalizer_train_bps":scale,
                    "train_reference_joint_loss":train_common_reference,
                    "monitor_reference_joint_loss":monitor_common_reference,
                    "monitor_arm_objective_loss":monitor_objective,
                    "last_minibatch_arm_loss":last_loss,
                    "gradient_norm_last50_mean_before_clip":float(np.mean(recent)),
                    "gradient_clipping_fraction_last50":float(
                        np.mean(np.asarray(recent)>5.)),
                    "cumulative_cpu_train_seconds":time.perf_counter()-started,
                    **scores,
                })
    return {
        "experiment":"TRAME_S3_1D_DIRECTION_MAGNITUDE_LOSS_ABLATION_V1",
        "engineering_canary_not_scientific_selection":bool(engineering_canary),
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "train_label_cutoff_exclusive":"2020-01-01",
        "monitor_label_years":"2020-2021",
        "external_2022_2025_used":False,
        "holdout_2026_used":False,
        "independent_test_used":False,
        "token_quantile_input_scale_prior_train_only":True,
        "all_arms_same_model_initial_weights":True,
        "all_arms_same_batch_order":True,
        "all_arms_same_forecast_reconciliation":True,
        "checkpoints_not_independent_models":True,
        "nonzero_BCE_weight_for_all_arms":True,
        "training_uses_spot_btc_no_live_trading":True,
        "transaction_costs_ignored":True,
        "not_cumulative_portfolio_return":True,
        "loss_definition":"SmoothL1(mu,y)+direction_w*BCE(logit,y_up)+magnitude_w*SmoothL1(abs(mu),abs(y))",
        "loss_weights":{arm:{"direction":v[0],"magnitude":v[1]}
                        for arm,v in OBJECTIVES.items()},
        "quantile_g2_boundaries_train_only_bps":list(provider.quantile_boundaries_bps),
        "normalizer_std_bps_train_only":scale,
        "train_only_direction_prior":prior,
        "train_origins_sha256":_origin_digest(train),
        "monitor_origins_sha256":_origin_digest(monitor),
        "model_source_commit":source_sha,
        "github_workflow_sha":os.environ.get("GITHUB_SHA","none"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "train_count":len(train),"monitor_count":len(monitor),
        "checkpoint_steps":list(checkpoints),
        "seeds":list(seeds),"arms":list(arms),
        "monitor_baselines":baselines,"results":rows,
    }


def run_history(*,interval,directory=ROOT,
                seeds=(20261025,20261026,20261027),
                checkpoints=CHECKPOINTS,
                data_origin="BTC_PUBLIC_REAL",engineering_canary=False):
    train,monitor,inventory=collect_internal(interval,directory)
    result=run_cases(train,monitor,interval=interval,
                     seeds=seeds,checkpoints=checkpoints,
                     data_origin=data_origin,
                     engineering_canary=engineering_canary)
    result["sampling_information"]=inventory
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="TRAME S3.1D public BTC loss ablation without external dev")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--seeds",nargs="+",type=int,
                   default=[20261025,20261026,20261027])
    p.add_argument("--checkpoints",nargs="+",type=int,
                   default=list(CHECKPOINTS))
    p.add_argument("--engineering-canary",action="store_true",
                   help="10/20/40 step smoke; not a scientific model comparison")
    p.add_argument("--checkpoints",nargs="+",type=int,default=list(CHECKPOINTS))
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():p.error("refuse overwriting research evidence")
    report=run_history(interval=a.interval,directory=a.directory,
                       seeds=tuple(a.seeds),
                       checkpoints=tuple(a.checkpoints),
                       engineering_canary=a.engineering_canary)
    a.output.write_text(json.dumps(report,indent=2,
                        allow_nan=False)+"\n",encoding="utf-8")
    print("S3.1D: internal pre2022 only; no trading or holdout validation")


if __name__=="__main__":
    main()
