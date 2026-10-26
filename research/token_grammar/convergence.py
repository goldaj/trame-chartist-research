"""S3.1C pre-2022 optimization diagnostics with a disjoint 2020-21 monitor.

Only the earlier pre-2020 cohort contributes gradients, train-only vocabulary
quantiles, scales, priors, and baseline fits. Later 2020-21 is a monitor and
never updates parameters. The external 2022-25 dev is NOT accessed by this
experiment, and the 2026 test is closed.

27 trajectories x checkpoints [200,800,2000] = 81 observations, NOT 81 fits.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
from statistics import mean
import time

import numpy as np
import torch

from research.btc_h1_m1.stream import ROOT,iter_cases
from research.continuous_direction.models import ContinuousDirectionModel,forecast_prices
from research.continuous_direction.diagnostics import prior_from_train,probability_report
from research.continuous_direction.runner import _arrays,_origin_digest,_source_code_commit
from research.representation_ablation.runner import features as continuous_features
from research.scaling_study.metrics import (
    training_magnitude_thresholds,baseline_forecasts,score_forecasts,
)
from research.token_grammar.learned_embeddings import (
    CausalTokenProvider,TokenScalarModel,_sha_params,
)

ARMS=("decoded","embedding_ordered","embedding_random")
CHECKPOINTS=(200,800,2000)
TRAIN_CUTOFF=datetime(2020,1,1,tzinfo=timezone.utc)
MONITOR_END=datetime(2022,1,1,tzinfo=timezone.utc)


def split_internal_pre2022(cases):
    """Fail closed if an external-dev or 2026 label appears even once."""
    if not cases:
        raise ValueError("pre2022 source cohort required")
    train=[]
    monitor=[]
    for c in cases:
        if (c.decision_time>=c.label_available_time or
            c.target_open>=c.label_available_time or
            c.label_available_time.tzinfo is None or
            c.label_available_time>=MONITOR_END):
            raise ValueError("2022+ label or noncausal timestamp in internal split")
        if c.label_available_time<TRAIN_CUTOFF:
            train.append(c)
        else:
            monitor.append(c)
    train.sort(key=lambda c:c.target_open)
    monitor.sort(key=lambda c:c.target_open)
    if len(train)<32 or len(monitor)<32:
        raise ValueError("pre2020 train and 2020-21 monitor each require >=32 examples")
    if not (max(x.label_available_time for x in train)<TRAIN_CUTOFF
            and min(x.label_available_time for x in monitor)>=TRAIN_CUTOFF):
        raise AssertionError("internal temporal boundary violated")
    return train,monitor


def collect_internal(interval, directory=ROOT, *, max_cases=4096, sampling_seed=20261025):
    if interval not in ("D1","H1","M1"):
        raise ValueError("resolution D1/H1/M1 required")
    if type(max_cases)!=int or not 100<=max_cases<=50000:
        raise ValueError("invalid train-only reservoir size")
    rng=np.random.default_rng(sampling_seed)
    stride=60 if interval=="M1" else 1
    pool=[]
    scanned=0
    # train_only=True yields NO external 2022-25 cases, even though the source
    # reader streams through older files for chronological integrity.
    for group,c in iter_cases(interval,Path(directory),
                              step=stride,train_only=True):
        if group!="train":
            raise AssertionError("train_only reader leaked external cohort")
        if c.label_available_time>=MONITOR_END:
            raise ValueError("reader unexpectedly yielded 2022+ label")
        scanned+=1
        if len(pool)<max_cases:
            pool.append(c)
        else:
            k=int(rng.integers(0,scanned))
            if k<max_cases:
                pool[k]=c
    early,monitor=split_internal_pre2022(pool)
    return early,monitor,{"scanned_pre2022":scanned,
                         "reservoir_cases":len(pool),"sampling_stride":stride,
                         "external_2022_2025_cases_accessed":False}


def _monitor_loss(model,x,y):
    model.eval()
    total=0.
    count=0
    with torch.no_grad():
        for k in range(0,len(y),128):
            v=float(model.loss(x[k:k+128],y[k:k+128]))
            if not math.isfinite(v):
                raise ArithmeticError("nonfinite diagnostic loss")
            n=len(y[k:k+128])
            total+=n*v
            count+=n
    model.train()
    return total/count


def _evaluate(model,x,monitor,*,scale,thresholds,prior):
    anchors=np.asarray([c.anchor_usd for c in monitor],dtype=float)
    actual=np.asarray([c.target_usd for c in monitor],dtype=float)
    predicted=[]
    probs=[]
    for offset in range(0,len(monitor),64):
        sl=slice(offset,offset+64)
        p,up,_mu=forecast_prices(model,x[sl],anchors[sl],
                                  scale_bps=float(scale))
        predicted.extend(p.tolist())
        probs.extend(up.tolist())
    scores=score_forecasts(anchors,actual,np.asarray(predicted),
                           train_thresholds=thresholds)
    scores.update(probability_report(anchors,actual,probs,train_prior=prior))
    scores["predicted_up_percent"]=100.*scores["n_predicted_up"]/scores["forecast_rows"]
    scores["monoclasse_99pct"]=(max(scores["n_predicted_up"],
                                    scores["n_predicted_down"])/scores["forecast_rows"]>=.99)
    return scores


def run_cases(train,monitor,*,interval,arms=ARMS,
              seeds=(20261025,20261026,20261027),
              checkpoints=CHECKPOINTS,batch_size=16,
              data_origin="ARTIFICIAL_FIXTURE"):
    if interval not in ("D1","H1","M1"):
        raise ValueError("invalid interval")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("unknown data provenance")
    if (not arms or any(a not in ARMS for a in arms)
            or len(set(arms))!=len(arms)
            or not seeds or len(set(seeds))!=len(seeds)
            or any(type(s)!=int for s in seeds)
            or not checkpoints or any(type(x)!=int or x<=0 for x in checkpoints)
            or tuple(sorted(set(checkpoints)))!=tuple(checkpoints)
            or checkpoints[-1]>2000
            or type(batch_size)!=int or not 1<=batch_size<=256):
        raise ValueError("invalid pre-registered grid")
    if data_origin=="BTC_PUBLIC_REAL" and tuple(checkpoints)!=CHECKPOINTS:
        raise ValueError("real BTC checkpoints must be [200,800,2000]")
    selected_train,selected_monitor=split_internal_pre2022(train+monitor)
    if len(selected_train)!=len(train) or len(selected_monitor)!=len(monitor):
        raise ValueError("mislabelled chronological cohorts")
    train=selected_train
    monitor=selected_monitor
    source_sha=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    scale=float(np.std(continuous_features(train,"continuous_bps")))
    if not math.isfinite(scale) or scale<=1e-8:
        scale=1.
    train_id=provider.ids(train,"signed_quantile_g2")
    mon_id=provider.ids(monitor,"signed_quantile_g2")
    centers=provider.centers("signed_quantile_g2")
    xtrain={
        "decoded":torch.as_tensor(centers[train_id]/scale,dtype=torch.float64),
        "learned":torch.as_tensor(train_id,dtype=torch.int64),
    }
    xmonitor={
        "decoded":torch.as_tensor(centers[mon_id]/scale,dtype=torch.float64),
        "learned":torch.as_tensor(mon_id,dtype=torch.int64),
    }
    _train_x,_train_a,_train_y,ytrain=_arrays(train)
    _mon_x,_mon_a,_mon_y,ymonitor=_arrays(monitor)
    ytorch=torch.as_tensor(ytrain/scale,dtype=torch.float64)
    ymon=torch.as_tensor(ymonitor/scale,dtype=torch.float64)
    thresholds=training_magnitude_thresholds(train)
    prior=prior_from_train(train)
    monitor_anchor=np.asarray([c.anchor_usd for c in monitor],dtype=float)
    monitor_true=np.asarray([c.target_usd for c in monitor],dtype=float)
    baselines={
        k:score_forecasts(monitor_anchor,monitor_true,p,
                          train_thresholds=thresholds)
        for k,p in baseline_forecasts(monitor).items()
    }
    rows=[]
    torch.set_num_threads(1)
    for seed in seeds:
        rng=np.random.default_rng(seed)
        batch_indices=[rng.integers(0,len(train),size=batch_size)
                       for _ in range(checkpoints[-1])]
        for arm in arms:
            torch.manual_seed(seed)
            if arm=="decoded":
                model=ContinuousDirectionModel(
                    width=16,depth=1,context=20,mode="joint")
                core_sha=_sha_params(model)
                trainable_extra=0
            else:
                model=TokenScalarModel(
                    width=16,depth=1,mode="joint",
                    init_style="ordered" if arm=="embedding_ordered" else "random",
                    centers_bps=centers,scale_bps=scale)
                core_sha=model.backbone_initial_sha256
                trainable_extra=11
            xtr=xtrain["decoded" if arm=="decoded" else "learned"]
            xmo=xmonitor["decoded" if arm=="decoded" else "learned"]
            optim=torch.optim.AdamW(model.parameters(),lr=.003,
                                     weight_decay=.001)
            grad_history=[]
            last_loss=float("nan")
            started=time.perf_counter()
            checkpoint_lookup=set(checkpoints)
            for step,batch in enumerate(batch_indices,start=1):
                model.train()
                optim.zero_grad(set_to_none=True)
                loss=model.loss(xtr[batch],ytorch[batch])
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite loss")
                loss.backward()
                before_clip=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
                if not bool(torch.isfinite(before_clip)):
                    raise ArithmeticError("nonfinite gradient")
                grad_history.append(float(before_clip))
                optim.step()
                last_loss=float(loss.detach())
                if step in checkpoint_lookup:
                    train_sample=min(len(train),128)
                    train_monitor_loss=_monitor_loss(
                        model,xtr[:train_sample],ytorch[:train_sample])
                    independent_monitor_loss=_monitor_loss(model,xmo,ymon)
                    scores=_evaluate(
                        model,xmo,monitor,scale=scale,
                        thresholds=thresholds,prior=prior)
                    recent=grad_history[-min(50,len(grad_history)):]
                    rows.append({
                        "interval":interval,
                        "arm":arm,"seed":seed,"checkpoint_updates":step,
                        "mode":"joint","width":16,"depth":1,
                        "backbone_initial_sha256":core_sha,
                        "parameter_count":sum(p.numel() for p in model.parameters()),
                        "learned_embedding_parameters":trainable_extra,
                        "train_monitor_loss":train_monitor_loss,
                        "internal_validation_monitor_loss":independent_monitor_loss,
                        "gradient_norm_last50_mean_before_clip":float(mean(recent)),
                        "gradient_clipping_fraction_last50":float(
                            sum(x>5. for x in recent)/len(recent)),
                        "last_minibatch_loss":last_loss,
                        "cumulative_cpu_train_seconds":time.perf_counter()-started,
                        **scores,
                    })
    return {
        "experiment":"TRAME_S3_1C_PRE2022_CONVERGENCE_V1",
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "training_labels_before":"2020-01-01",
        "internal_monitor_labels":"2020-2021",
        "external_development_2022_2025_accessed":False,
        "labels_2026_opened":False,
        "independent_test_used":False,
        "convergence_not_confirmatory":True,
        "only_train_fits_vocabulary_normalizer_and_prior":True,
        "quantile_g2_boundaries_train_only_bps":list(provider.quantile_boundaries_bps),
        "normalizer_std_bps_train_only":scale,
        "train_count":len(train),"monitor_count":len(monitor),
        "train_origins_sha256":_origin_digest(train),
        "monitor_origins_sha256":_origin_digest(monitor),
        "model_source_commit":source_sha,
        "github_workflow_commit":os.environ.get("GITHUB_SHA","not running under Actions"),
        "checkpoint_steps":list(checkpoints),
        "seeds":list(seeds),"arms":list(arms),
        "width":16,"depth":1,"mode":"joint",
        "base_parameters":rows[0]["parameter_count"]-(11 if rows[0]["learned_embedding_parameters"] else 0),
        "train_only_up_prior":prior,
        "monitor_baselines":baselines,
        "not_cumulative_portfolio_return":True,
        "transaction_costs_ignored":True,
        "results":rows,
    }


def run_history(*,interval,directory=ROOT,
                seeds=(20261025,20261026,20261027),
                checkpoints=CHECKPOINTS,
                data_origin="BTC_PUBLIC_REAL"):
    train,monitor,inventory=collect_internal(interval,directory)
    d=run_cases(train,monitor,interval=interval,seeds=tuple(seeds),
                checkpoints=tuple(checkpoints),data_origin=data_origin)
    d["sampling_information"]=inventory
    return d


def main(argv=None):
    p=argparse.ArgumentParser(description="S3.1C pre2022 loss/gradient/bias convergence diagnosis")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--seeds",nargs="+",type=int,default=[20261025,20261026,20261027])
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("refusing to overwrite results")
    rep=run_history(interval=a.interval,directory=a.directory,
                    seeds=tuple(a.seeds))
    a.output.write_text(json.dumps(rep,indent=2,allow_nan=False)+"\n",
                        encoding="utf-8")
    print("Completed TRAIN<2020 internal MONITOR2020-21, no 2022+/trades")


if __name__=="__main__":
    main()
