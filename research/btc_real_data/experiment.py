"""Exploratory BTC/USD D1 three-architecture experiment; local user CSV only.

This is neither independent holdout testing nor historical trading PnL.
The mini-models/optimizer were developed using synthetic data. The 2026
interval is present in owner-provided files but is not scored/fitted here.
"""
import argparse
import json
import math
import platform
from pathlib import Path
import time

import numpy as np
import torch

from research.architecture_comparison.experiment import ARMS, choose_widths
from research.btc_real_data.loader import ROOT, load_history, create_cases, summarize
from research.p1b0_numerics.torch_head import log_interval_mass


def _matrix(cases):
    x=np.asarray([row.prior_codes for row in cases],dtype=np.float64)
    y=np.asarray([row.target_code for row in cases],dtype=np.float64)
    anchors=np.asarray([row.anchor_usd for row in cases],dtype=np.float64)
    actual=np.asarray([row.target_usd for row in cases],dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != 20 or not np.isfinite(x).all():
        raise ValueError("need 20 historical return codes per case")
    return x,y,anchors,actual


def _estimate(train, dev):
    x,y,anchors,actual=_matrix(dev)
    train_targets=np.asarray([row.target_code for row in train],dtype=float)
    # Fit a constant location/scale on TRAIN ONLY; no development refit.
    mu=float(np.mean(train_targets))
    sigma=float(max(0.25,np.std(train_targets,ddof=0)))
    with torch.no_grad():
        nll=float(-log_interval_mass(torch.as_tensor(y,dtype=torch.float64),
                    torch.tensor(mu,dtype=torch.float64),
                    torch.tensor(sigma,dtype=torch.float64)).mean())
    # This is the median under a Gaussian log-return (not expected price).
    forecast=anchors*np.exp(mu/1000.0)
    return {"mean_code":mu,"sigma_code":sigma,"development_nll":nll,
            "development_mae_price_median_usd":float(np.mean(np.abs(forecast-actual))),
            "persistence_development_mae_usd":float(np.mean(np.abs(anchors-actual))),
            "fit":"train_only_constant_gaussian"}


def _score(model, x, y, anchors, actual, *, batch=96):
    masses=[]
    medians=[]
    model.eval()
    with torch.no_grad():
        for start in range(0,len(x),batch):
            xx=torch.as_tensor(x[start:start+batch],dtype=torch.float64)
            yy=torch.as_tensor(y[start:start+batch],dtype=torch.float64)
            mu,sigma=model(xx)
            current=mu[:,-1]
            logp=log_interval_mass(yy,current,sigma[:,-1])
            if not bool(torch.isfinite(logp).all()):
                raise ArithmeticError("nonfinite held development likelihood")
            masses.append(logp.cpu().numpy())
            medians.append(current.cpu().numpy())
    ll=np.concatenate(masses)
    med=np.concatenate(medians)
    estimate=anchors*np.exp(med/1000.0)
    return {"development_nll":float(-ll.mean()),
            "development_mae_price_median_usd":float(np.mean(np.abs(estimate-actual))),
            "development_persistence_mae_usd":float(np.mean(np.abs(anchors-actual)))}


def run(*, directory=ROOT, steps=20, seeds=(20261025,20261026,20261027)):
    if type(steps) is not int or not 1<=steps<=200:
        raise ValueError("steps must be 1..200")
    if not isinstance(seeds,(tuple,list)) or not seeds or any(type(s) is not int for s in seeds) or len(set(seeds))!=len(seeds):
        raise ValueError("seeds must be distinct integers")
    torch.set_num_threads(1)
    history=load_history(Path(directory))
    samples=create_cases(history,context=20)
    train, dev=samples["train"],samples["development"]
    xtrain,ytrain,_,_=_matrix(train)
    xdev,ydev,adeu,vdeu=_matrix(dev)
    xt=torch.as_tensor(xtrain,dtype=torch.float64)
    yt=torch.as_tensor(ytrain,dtype=torch.float64)
    capacity=choose_widths()
    baseline=_estimate(train,dev)
    results=[]
    for seed in seeds:
        rng=np.random.default_rng(seed)
        batches=[rng.integers(0,len(train),size=16) for _ in range(steps)]
        for name,factory in ARMS.items():
            torch.manual_seed(seed)
            width=capacity["selected"][name]["width"]
            model=factory(width=width)
            optimizer=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.001)
            clock=time.monotonic()
            model.train()
            for idx in batches:
                optimizer.zero_grad(set_to_none=True)
                mu,sigma=model(xt[idx])
                loss=-log_interval_mass(yt[idx],mu[:,-1],sigma[:,-1]).mean()
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite BTC train NLL")
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(),5.0)
                optimizer.step()
            seconds=time.monotonic()-clock
            scores=_score(model,xdev,ydev,adeu,vdeu)
            results.append({"architecture":name,"seed":seed,"width":width,
                            "parameter_count":sum(p.numel() for p in model.parameters()),
                            "steps":steps,"fit_seconds_cpu":seconds,**scores})
    return {"experiment":"trame_real_btc_development_exploratory_v0.1",
            "source":"owner-supplied BTC/USD D1 three CSV snapshots, NOT Hyperliquid",
            "data_origin":"REAL_HISTORICAL_SPOT_AND_INDICATIVE_OWNER_TRUSTED",
            "price_history":summarize(history,samples),
            "train_targets_through":"2021-12-31",
            "development_targets":"2022-01-01 through 2025-12-31",
            "2026_labels_not_scored_or_quantized":True,
            "not_independent_financial_test":True,
            "not_backtest_or_executable_trade_pnl":True,
            "pretrained_models_included":False,
            "compute_matched":False,
            "architecture_selection_locked":False,
            "model_head":"BASE rounded-Gaussian cells on 0.001 log-return units",
            "same_batches_per_seed":True,"widths":capacity,
            "baseline":baseline,"results":results,
            "torch_version":torch.__version__,
            "python_version":platform.python_version()}


def main(argv=None):
    p=argparse.ArgumentParser(description="Offline BTC historical exploratory only")
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--steps",type=int,default=20)
    p.add_argument("--seeds",type=int,nargs="+",default=[20261025,20261026,20261027])
    p.add_argument("--output",type=Path,default=None)
    args=p.parse_args(argv)
    report=run(directory=args.directory,steps=args.steps,seeds=args.seeds)
    body=json.dumps(report,indent=2,allow_nan=False,ensure_ascii=False)+"\n"
    if args.output:
        if args.output.exists():
            p.error("output exists; choose new path to prevent overwrite")
        args.output.write_text(body,encoding="utf-8")
        print(str(args.output))
    else:
        print(body)


if __name__=="__main__":
    main()
