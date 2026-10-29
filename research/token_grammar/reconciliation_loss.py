"""TRAME S3.1E: loss aligned to differentiable proxy of served hard reconciliation.

HARD infer: sign(logit>=0)*abs(mu) (S2 existing)
SOFT surrogate: tanh(logit/2)*sqrt(mu²+1e-12)
HARD is scored as served, SOFT only a diagnostic. Train labels <2020;
monitor labels 2020-2021. Never open 2022-2025 external dev nor 2026.
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
from research.token_grammar.learned_embeddings import (
    CausalTokenProvider,_sha_params)

ARMS=("legacy","reconciled_025","reconciled_100")
WEIGHTS={"legacy":0.0,"reconciled_025":0.25,"reconciled_100":1.0}
EPS=1e-6


def soft_reconciled_return(mu,logit):
    """Normalized continuous surrogate, not identical to hard binary forecast."""
    if (mu.ndim!=1 or logit.shape!=mu.shape or mu.dtype!=torch.float64
            or logit.dtype!=torch.float64 or not bool(torch.isfinite(mu).all())
            or not bool(torch.isfinite(logit).all())):
        raise ValueError("same length finite float64 model outputs expected")
    return torch.tanh(logit/2.)*torch.sqrt(mu.square()+EPS**2)


def objective(model,x,y,arm):
    if arm not in ARMS or model.mode!="joint":
        raise ValueError("unknown loss arm or non-joint model")
    if (y.ndim!=1 or y.shape[0]!=len(x) or y.dtype!=torch.float64
            or not bool(torch.isfinite(y).all())):
        raise ValueError("finite float64 normalized targets expected")
    mu,logit=model(x)
    price=F.smooth_l1_loss(mu,y,beta=1.)
    mask=y!=0
    binary=(F.binary_cross_entropy_with_logits(
        logit[mask],(y[mask]>0).to(torch.float64))
        if bool(mask.any()) else price.new_zeros(()))
    reconciliation=F.smooth_l1_loss(
        soft_reconciled_return(mu,logit),y,beta=1.)
    return price+0.5*binary+WEIGHTS[arm]*reconciliation


def fixed_loss(model,x,y,arm):
    if len(y)<1:raise ValueError("empty cohort")
    model.eval()
    total=0.
    with torch.no_grad():
        for i in range(0,len(y),64):
            sl=slice(i,i+64)
            loss=objective(model,x[sl],y[sl],arm)
            if not bool(torch.isfinite(loss)):
                raise ArithmeticError("bad held-out objective")
            total+=float(loss)*len(y[sl])
    return total/len(y)


def evaluate_hard_and_soft(model,x,monitor,*,scale,thresholds,prior):
    anchor=np.asarray([c.anchor_usd for c in monitor],dtype=np.float64)
    actual=np.asarray([c.target_usd for c in monitor],dtype=np.float64)
    hard,probs,mu_bps=[],[],[]
    for i in range(0,len(monitor),64):
        sl=slice(i,i+64)
        pred,up,mu=forecast_prices(
            model,x[sl],anchor[sl],scale_bps=float(scale))
        hard.extend(pred.tolist())
        probs.extend(up.tolist())
        mu_bps.extend(mu.tolist())
    hard=np.asarray(hard)
    probs=np.asarray(probs)
    mu_bps=np.asarray(mu_bps)
    # 2*sigmoid(logit)-1 == tanh(logit/2) in exact math.
    soft_bps=(2*probs-1)*np.sqrt(mu_bps**2+(EPS*scale)**2)
    soft=anchor*np.exp(soft_bps/10000.)
    h=score_forecasts(anchor,actual,hard,train_thresholds=thresholds)
    s=score_forecasts(anchor,actual,soft,train_thresholds=thresholds)
    h.update(probability_report(anchor,actual,probs,train_prior=prior))
    h["predicted_up_percent"]=100.*h["n_predicted_up"]/h["forecast_rows"]
    h["monoclasse_99pct"]=bool(
        max(h["n_predicted_up"],h["n_predicted_down"])
        /h["forecast_rows"]>=.99)
    h["regression_vs_head_sign_disagreement_fraction"]=float(
        np.mean((mu_bps>=0)!=(probs>=.5)))
    h["regression_zero_fraction"]=float(np.mean(mu_bps==0))
    h["hard_soft_price_gap_bps"]=float(np.mean(
        np.abs((hard-soft)/anchor)*10000))
    h["soft_surrogate_mae_bps_anchor"]=s["mae_bps_anchor"]
    h["soft_surrogate_mae_native_usd"]=s["mae_native_usd"]
    h["soft_surrogate_absolute_magnitude_error_bps"]=s["absolute_magnitude_error_bps"]
    return h


def run_cases(train,monitor,*,interval,
              arms=ARMS,seeds=(20261025,20261026,20261027),
              checkpoints=CHECKPOINTS,batch_size=16,
              data_origin="ARTIFICIAL_FIXTURE",engineering_canary=False):
    if interval not in ("D1","H1","M1"):
        raise ValueError("unknown historical horizon")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("unknown source provenance")
    if (not arms or len(set(arms))!=len(arms)
            or any(x not in ARMS for x in arms)
            or not seeds or len(set(seeds))!=len(seeds)
            or any(type(s)!=int for s in seeds)
            or not checkpoints or tuple(sorted(set(checkpoints)))!=tuple(checkpoints)
            or any(type(s)!=int or not 1<=s<=2000 for s in checkpoints)
            or type(batch_size)!=int or not 1<=batch_size<=256):
        raise ValueError("invalid pre-registered comparison grid")
    if (data_origin=="BTC_PUBLIC_REAL"
            and tuple(checkpoints)!=CHECKPOINTS
            and not (engineering_canary and tuple(checkpoints)==(10,20,40))):
        raise ValueError("real BTC requires checkpoints 200/800/2000 or marked smoke")
    a,b=split_internal_pre2022(train+monitor)
    if len(a)!=len(train) or len(b)!=len(monitor):
        raise ValueError("invalid internal cohort boundary")
    train,monitor=a,b
    commit=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    scale=float(np.std(continuous_features(train,"continuous_bps")))
    if not math.isfinite(scale) or scale<=1e-8:
        scale=1.
    center=provider.centers("signed_quantile_g2")
    train_id=provider.ids(train,"signed_quantile_g2")
    monitor_id=provider.ids(monitor,"signed_quantile_g2")
    xt=torch.as_tensor(center[train_id]/scale,dtype=torch.float64)
    xm=torch.as_tensor(center[monitor_id]/scale,dtype=torch.float64)
    _,_,_,ytrain=_arrays(train)
    _,_,_,ymonitor=_arrays(monitor)
    yt=torch.as_tensor(ytrain/scale,dtype=torch.float64)
    ym=torch.as_tensor(ymonitor/scale,dtype=torch.float64)
    threshold=training_magnitude_thresholds(train)
    prior=prior_from_train(train)
    a_mon=np.asarray([c.anchor_usd for c in monitor],dtype=np.float64)
    y_mon=np.asarray([c.target_usd for c in monitor],dtype=np.float64)
    baselines={
        name:score_forecasts(a_mon,y_mon,forecast,train_thresholds=threshold)
        for name,forecast in baseline_forecasts(monitor).items()}
    torch.set_num_threads(1)
    rows=[]
    for seed in seeds:
        rng=np.random.default_rng(seed)
        minibatches=[rng.integers(0,len(train),size=batch_size)
                     for _ in range(checkpoints[-1])]
        for arm in arms:
            torch.manual_seed(seed)
            model=ContinuousDirectionModel(
                width=16,depth=1,context=20,mode="joint")
            init_sha=_sha_params(model)
            optim=torch.optim.AdamW(model.parameters(),lr=.003,
                                   weight_decay=.001)
            grad_history=[]
            last_loss=None
            start=time.perf_counter()
            for step,ids in enumerate(minibatches,1):
                model.train()
                optim.zero_grad(set_to_none=True)
                loss=objective(model,xt[ids],yt[ids],arm)
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite optimization loss")
                loss.backward()
                grad=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
                if not bool(torch.isfinite(grad)):
                    raise ArithmeticError("nonfinite gradient")
                grad_history.append(float(grad))
                optim.step()
                last_loss=float(loss.detach())
                if step not in checkpoints:
                    continue
                scores=evaluate_hard_and_soft(
                    model,xm,monitor,scale=scale,
                    thresholds=threshold,prior=prior)
                recent=grad_history[-min(50,len(grad_history)):]
                rows.append({
                    "interval":interval,"arm":arm,
                    "reconciled_surrogate_weight":WEIGHTS[arm],
                    "seed":seed,"checkpoint_updates":step,
                    "same_optimizer_continued":True,
                    "width":16,"depth":1,"mode":"joint",
                    "backbone_initial_sha256":init_sha,
                    "parameter_count":sum(p.numel() for p in model.parameters()),
                    "train_normalizer_std_bps":scale,
                    "train_common_legacy_loss":fixed_loss(
                        model,xt[:min(128,len(train))],
                        yt[:min(128,len(train))],"legacy"),
                    "monitor_common_legacy_loss":fixed_loss(
                        model,xm,ym,"legacy"),
                    "monitor_arm_loss":fixed_loss(model,xm,ym,arm),
                    "last_minibatch_arm_loss":last_loss,
                    "gradient_norm_last50_before_clip_mean":float(np.mean(recent)),
                    "gradient_clip_fraction_last50":float(
                        np.mean(np.asarray(recent)>5.)),
                    "cpu_seconds_cumulative":time.perf_counter()-start,
                    **scores,
                })
    return {
        "experiment":"TRAME_S3_1E_SOFT_RECONCILIATION_LOSS_V1",
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "train_label_end_exclusive":"2020-01-01",
        "monitor_label_years":"2020-2021",
        "external_2022_2025_used":False,
        "holdout_2026_used":False,
        "independent_test_used":False,
        "token_quantile_normalizer_prior_train_only":True,
        "same_initial_sha_and_batches":True,
        "soft_surrogate_is_not_hard_served_forecast":True,
        "served_hard_sign_reconciliation_unchanged":True,
        "all_arms_same_parameter_count":True,
        "checkpoint_evaluations_not_independent":True,
        "no_portfolio_pnl":True,
        "transaction_costs_ignored":True,
        "engineering_canary_not_scientific_selection":bool(engineering_canary),
        "soft_epsilon_normalized":EPS,
        "weights":WEIGHTS,
        "train_count":len(train),"monitor_count":len(monitor),
        "train_origins_sha256":_origin_digest(train),
        "monitor_origins_sha256":_origin_digest(monitor),
        "model_source_commit":commit,
        "github_workflow_sha":os.environ.get("GITHUB_SHA","none"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "seed_list":list(seeds),"checkpoint_steps":list(checkpoints),
        "arms":list(arms),
        "train_only_prior_up":prior,
        "quantile_boundaries_train_only_bps":
            list(provider.quantile_boundaries_bps),
        "train_normalizer_std_bps":scale,
        "baseline_scores":baselines,"results":rows,
    }


def run_history(*,interval,directory=ROOT,
                seeds=(20261025,20261026,20261027),
                checkpoints=CHECKPOINTS,
                engineering_canary=False,data_origin="BTC_PUBLIC_REAL"):
    train,monitor,inventory=collect_internal(interval,directory)
    result=run_cases(train,monitor,interval=interval,seeds=seeds,
                     checkpoints=checkpoints,engineering_canary=engineering_canary,
                     data_origin=data_origin)
    result["sampling_information"]=inventory
    return result


def main(argv=None):
    p=argparse.ArgumentParser(
        description="S3.1E pre2022 coherent hard price / soft loss scientific test")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--seeds",type=int,nargs="+",
                   default=[20261025,20261026,20261027])
    p.add_argument("--checkpoints",type=int,nargs="+",
                   default=list(CHECKPOINTS))
    p.add_argument("--engineering-canary",action="store_true")
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists():
        p.error("refusing to overwrite existing study")
    r=run_history(interval=args.interval,directory=args.directory,
                  seeds=tuple(args.seeds),
                  checkpoints=tuple(args.checkpoints),
                  engineering_canary=args.engineering_canary)
    args.output.write_text(json.dumps(r,indent=2,
                           allow_nan=False)+"\n",encoding="utf-8")
    print("S3.1E causal pre2022, 2022–26 unopened, hard served forecasts")


if __name__=="__main__":
    main()
