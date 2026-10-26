"""S2 controlled continuous-return / joint-direction offline experiment.

Uses the exact existing A7 train/development Cases but additional causal,
not-rounded past returns. No 2026 labels. Never trades.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import torch

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT
from research.scaling_study.metrics import (
    score_forecasts, training_magnitude_thresholds, baseline_forecasts,
)
from research.scaling_study.runner import _ridge_forecasts, _validate_chronology
from research.continuous_direction.models import (
    ContinuousDirectionModel, forecast_prices,
)
from research.continuous_direction.diagnostics import prior_from_train, probability_report


def _arrays(cases):
    if not cases:
        raise ValueError("nonempty cases needed")
    lengths={len(c.continuous_past_bps) for c in cases}
    if lengths != {20}:
        raise ValueError("causal continuous past must have 20 completed returns")
    past=np.asarray([c.continuous_past_bps for c in cases],dtype=np.float64)
    anchors=np.asarray([c.anchor_usd for c in cases],dtype=np.float64)
    actual=np.asarray([c.target_usd for c in cases],dtype=np.float64)
    if (not np.isfinite(past).all() or not np.isfinite(anchors).all()
            or not np.isfinite(actual).all() or np.any(actual<=0)
            or np.any(anchors<=0)):
        raise ValueError("finite positive target/anchor and past expected")
    target=10000*np.log(actual/anchors)
    return past,anchors,actual,target


def _evaluate(model,cases,*,scale_bps,train_prior):
    history,anchors,actual,target=_arrays(cases)
    history_tensor=torch.as_tensor(history/scale_bps,dtype=torch.float64)
    forecasts=[]
    probabilities=[]
    regressions=[]
    for start in range(0,len(cases),64):
        a,p,mu=forecast_prices(
            model,history_tensor[start:start+64],anchors[start:start+64],
            scale_bps=float(scale_bps))
        forecasts.extend(a.tolist())
        probabilities.extend(p.tolist())
        regressions.extend(mu.tolist())
    forecasts=np.asarray(forecasts,dtype=float)
    probabilities=np.asarray(probabilities,dtype=float)
    regression=np.asarray(regressions,dtype=float)
    valid=actual!=anchors
    classification={}
    if model.mode=="joint":
        classification=probability_report(
            anchors,actual,probabilities,train_prior=train_prior)
        classification["head_regression_sign_disagreement"]=float(np.mean(
            (probabilities>=.5) != (regression>=0)))
    else:
        # Regression-only direction logits receive NO training gradients.
        # Scoring them as calibrated binary probabilities would be fraudulent.
        classification={
            "binary_probabilities_from_trained_head":False,
            "brier_nonflat":None,"binary_ce_nonflat":None,
            "brier_train_prior_nonflat":None,"binary_ce_train_prior_nonflat":None,
            "brier_skill_vs_train_prior":None,"binary_ce_delta_vs_train_prior":None,
            "predicted_up_probability_mean":None, "reliability_bins":[],
            "head_regression_sign_disagreement":None,
        }
    return forecasts,classification


def _source_code_commit(data_origin):
    """Git SHA of model checkout, NOT the surrounding private workflow SHA."""
    root=Path(__file__).resolve().parents[2]
    try:
        proc=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],
                            check=False,text=True,capture_output=True,timeout=5)
        sha=proc.stdout.strip()
    except (OSError,subprocess.TimeoutExpired):
        sha=""
    if not sha or len(sha)!=40 or any(ch not in "0123456789abcdef" for ch in sha):
        if data_origin=="BTC_PRIVATE_REAL":
            raise RuntimeError("real research requires a traceable Git model checkout")
        return "unavailable_fixture_only"
    return sha


def run_cases(train,development,*,interval,widths=(16,32),depths=(1,2),
              modes=("regression","joint"),steps=200,
              seeds=(20261025,20261026,20261027),
              batch_size=16,data_origin="ARTIFICIAL_FIXTURE"):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 required")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PRIVATE_REAL"):
        raise ValueError("explicit data origin required")
    if (not widths or not depths or not modes
            or any(type(x) is not int or x<8 or x%4 for x in widths)
            or any(x not in (1,2) for x in depths)
            or any(x not in ("regression","joint") for x in modes)
            or len(set(widths))!=len(widths)
            or len(set(depths))!=len(depths)
            or len(set(modes))!=len(modes)):
        raise ValueError("invalid pilot architecture matrix")
    if (type(steps) is not int or not 1<=steps<=2000
            or type(batch_size) is not int or not 1<=batch_size<=256
            or not seeds or len(seeds)>10 or
            any(type(s) is not int for s in seeds)
            or len(set(seeds))!=len(seeds)):
        raise ValueError("invalid training budget")
    _validate_chronology(train,development)
    if len(train)<32 or len(development)<32:
        raise ValueError("train and dev need >=32 cases")
    torch.set_num_threads(1)
    xtrain,_,_,ytrain=_arrays(train)
    xdev,anchor,actual,ydev=_arrays(development)
    scale=float(np.std(xtrain,ddof=0))
    if not math.isfinite(scale) or scale<=1e-8:
        # Degenerate fabricated train only: fixed scale 1 bps.
        scale=1.0
    normalized_train=torch.as_tensor(xtrain/scale,dtype=torch.float64)
    targets_train=torch.as_tensor(ytrain/scale,dtype=torch.float64)
    thresholds=training_magnitude_thresholds(train)
    train_prior=prior_from_train(train)
    baselines={}
    for name,forecast in baseline_forecasts(development).items():
        baselines[name]=score_forecasts(
            anchor,actual,forecast,train_thresholds=thresholds)
    baselines["ridge_train_only"]=score_forecasts(
        anchor,actual,_ridge_forecasts(train,development),
        train_thresholds=thresholds)
    rows=[]
    for seed in seeds:
        rng=np.random.default_rng(seed)
        batches=[rng.integers(0,len(train),size=batch_size) for _ in range(steps)]
        for width in widths:
            for depth in depths:
                for mode in modes:
                    torch.manual_seed(seed)
                    model=ContinuousDirectionModel(
                        width=width,depth=depth,context=20,mode=mode)
                    optimizer=torch.optim.AdamW(
                        model.parameters(),lr=.003,weight_decay=.001)
                    t0=time.perf_counter()
                    model.train()
                    for ids in batches:
                        optimizer.zero_grad(set_to_none=True)
                        loss=model.loss(normalized_train[ids],targets_train[ids])
                        if not bool(torch.isfinite(loss)):
                            raise ArithmeticError("nonfinite S2 training loss")
                        loss.backward()
                        grad_norm=torch.nn.utils.clip_grad_norm_(
                            model.parameters(),5.0)
                        if not bool(torch.isfinite(grad_norm)):
                            raise ArithmeticError("nonfinite gradients")
                        optimizer.step()
                    elapsed=time.perf_counter()-t0
                    forecast,cls=_evaluate(model,development,scale_bps=scale,
                                           train_prior=train_prior)
                    scored=score_forecasts(
                        anchor,actual,forecast,train_thresholds=thresholds)
                    rows.append({
                        "architecture":"gpt_style_continuous",
                        "width":width,"depth":depth,"mode":mode,
                        "parameter_count":sum(p.numel() for p in model.parameters()),
                        "seed":seed,"steps":steps,"batch_size":batch_size,
                        "observed_cpu_train_seconds":elapsed,
                        "final_minibatch_loss":float(loss.detach()),
                        **scored,**cls,
                    })
    return {
        "experiment":"TRAME_S2_CONTINUOUS_DIRECTION_EXPLORATORY_V1",
        "data_origin":data_origin,"interval":interval,
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "train_before":"2022-01-01","dev":"2022-2025",
        "labels_2026_opened":False,"independent_test_used":False,
        "not_hyperliquid_execution":True,"no_transaction_costs":True,
        "not_cumulative_portfolio_return":True,
        "train_only_normalization":True,"train_normalizer_std_bps":scale,
        "continuous_past_input_len":20,
        "direction_class_prior_train_only":train_prior,
        "quantized_target_zero_fraction_train":float(np.mean(
            np.asarray([c.encoded_target for c in train])==0)),
        "true_target_flat_fraction_train":float(np.mean(ytrain==0)),
        "quantized_target_zero_fraction_dev":float(np.mean(
            np.asarray([c.encoded_target for c in development])==0)),
        "true_target_flat_fraction_dev":float(np.mean(ydev==0)),
        "train_count":len(train),"dev_count":len(development),
        "steps":steps,"seed_count":len(seeds),
        "same_batches_per_seed":True,
        "total_compute_matched":False,
        "historical_base_gaussian_nll_not_comparable":True,
        "optimizer":"AdamW lr=.003 weight_decay=.001 grad_clip=5",
        "regression_loss":"Huber beta=1 on train-std normalized return",
        "joint_weight_bce":0.5,
        "flat_classification_training_policy":"skip",
        "baselines":baselines,"results":rows,
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "github_workflow_commit":os.environ.get("GITHUB_SHA","not recorded outside CI"),
        "model_source_commit":_source_code_commit(data_origin),
    }


def run_history(*,interval,directory=ROOT,widths=(16,32),depths=(1,2),
                modes=("regression","joint"),steps=200,
                seeds=(20261025,20261026,20261027),
                max_train=4096,max_dev=1024):
    stride=60 if interval=="M1" else 1
    pools,scanned=collect(
        interval,Path(directory),max_train=max_train,max_dev=max_dev,
        stride=stride)
    output=run_cases(
        pools["train"],pools["development"],interval=interval,
        widths=widths,depths=depths,modes=modes,steps=steps,
        seeds=seeds,data_origin="BTC_PRIVATE_REAL")
    output["scanned_candidates"]=scanned
    output["sampling_stride"]=stride
    return output


def main(argv=None):
    p=argparse.ArgumentParser(description="S2 offline continuous-vs-dual-head research")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--widths",type=int,nargs="+",default=[16,32])
    p.add_argument("--depths",type=int,nargs="+",default=[1,2])
    p.add_argument("--modes",choices=("regression","joint"),
                   nargs="+",default=["regression","joint"])
    p.add_argument("--steps",type=int,default=200)
    p.add_argument("--seeds",type=int,nargs="+",
                   default=[20261025,20261026,20261027])
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists():
        p.error("refusing to overwrite an existing research report")
    report=run_history(
        interval=args.interval,directory=args.directory,
        widths=tuple(args.widths),depths=tuple(args.depths),
        modes=tuple(args.modes),steps=args.steps,seeds=tuple(args.seeds))
    args.output.write_text(
        json.dumps(report,indent=2,allow_nan=False,ensure_ascii=False)+"\n",
        encoding="utf-8")
    print("Exploratory S2 report saved; 2026 unopened; no trading")


if __name__=="__main__":
    main()
