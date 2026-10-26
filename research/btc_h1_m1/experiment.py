"""Paired GPT-style/Transformer/GRU exploratory study on historical BTC H1/M1.

Only when users copy their historical .csv.gz files into local raw/.
Never loads Hyperliquid perp series, funds, or keys. Dev is for research,
not an independent untouched confirmatory test.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import platform
import time

import numpy as np
import torch

from research.architecture_comparison.experiment import ARMS, choose_widths
from research.btc_h1_m1.stream import ROOT, iter_cases
from research.p1b0_numerics.torch_head import log_interval_mass


def collect(interval, folder, *, max_train=4096, max_dev=1024,
            sampling_seed=20261025, stride=1):
    if (type(max_train) is not int or not 32<=max_train<=50000
            or type(max_dev) is not int or not 32<=max_dev<=10000
            or type(stride) is not int or stride<1):
        raise ValueError("invalid sample cap or stride")
    rng=np.random.default_rng(sampling_seed)
    pool={"train":[], "development":[]}
    seen={"train":0,"development":0}
    for split,case in iter_cases(interval,folder,step=stride):
        n=seen[split]+1
        seen[split]=n
        cap=max_train if split=="train" else max_dev
        if len(pool[split])<cap:
            pool[split].append(case)
        else:
            idx=int(rng.integers(0,n))
            if idx<cap:
                pool[split][idx]=case
    if min(len(pool["train"]),len(pool["development"]))<32:
        raise ValueError("not enough usable train/development candles")
    # Chronological presentation of the selected origins avoids mistaking
    # shuffled data for time-ordered market events.
    for values in pool.values():
        values.sort(key=lambda x:x.target_open)
    return pool,seen


def evaluate(model, cases, *, chunk_size=96):
    nll_sum=mae_sum=persistence_sum=0.0
    model.eval()
    with torch.no_grad():
        for i in range(0,len(cases),chunk_size):
            batch=cases[i:i+chunk_size]
            x=torch.as_tensor([c.encoded_past for c in batch],dtype=torch.float64)
            y=torch.as_tensor([c.encoded_target for c in batch],dtype=torch.float64)
            mu,sigma=model(x)
            mu_last=mu[:,-1]
            ll=log_interval_mass(y,mu_last,sigma[:,-1])
            if not bool(torch.isfinite(ll).all()):
                raise ArithmeticError("nonfinite validation likelihood")
            anchored=np.array([c.anchor_usd for c in batch],dtype=float)
            actual=np.array([c.target_usd for c in batch],dtype=float)
            forecast=anchored*np.exp(mu_last.cpu().numpy()/1000)
            nll_sum+=float((-ll).sum())
            mae_sum+=float(np.abs(forecast-actual).sum())
            persistence_sum+=float(np.abs(anchored-actual).sum())
    return {"dev_nll":nll_sum/len(cases),
            "dev_mae_native_usd":mae_sum/len(cases),
            "dev_persistence_mae_native_usd":persistence_sum/len(cases)}


def compare_history(*, interval, folder=ROOT, steps=40,
                    seeds=(20261025,20261026,20261027),
                    max_train=4096,max_dev=1024,stride=None):
    if interval not in ("D1","H1","M1"):
        raise ValueError("supported horizons: D1/H1/M1")
    if type(steps) is not int or not 1<=steps<=200:
        raise ValueError("steps 1..200")
    if (not isinstance(seeds,(tuple,list)) or not seeds or
            any(type(s) is not int for s in seeds) or len(set(seeds))!=len(seeds)):
        raise ValueError("distinct integer seeds required")
    step=60 if interval=="M1" else 1
    if stride is not None: step=stride
    torch.set_num_threads(1)
    pools,available=collect(interval,Path(folder),max_train=max_train,
                            max_dev=max_dev,stride=step)
    train,dev=pools["train"],pools["development"]
    xtrain=torch.as_tensor([c.encoded_past for c in train],dtype=torch.float64)
    ytrain=torch.as_tensor([c.encoded_target for c in train],dtype=torch.float64)
    capacity=choose_widths()
    outputs=[]
    for seed in seeds:
        rng=np.random.default_rng(seed)
        batches=[rng.integers(0,len(train),size=16) for _ in range(steps)]
        for name,factory in ARMS.items():
            torch.manual_seed(seed)
            width=capacity["selected"][name]["width"]
            model=factory(width=width)
            opt=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.001)
            t0=time.monotonic()
            model.train()
            for indices in batches:
                opt.zero_grad(set_to_none=True)
                mu,sigma=model(xtrain[indices])
                loss=-log_interval_mass(ytrain[indices],mu[:,-1],sigma[:,-1]).mean()
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite BTC training likelihood")
                loss.backward()
                grad_norm=torch.nn.utils.clip_grad_norm_(model.parameters(),5.0)
                if not bool(torch.isfinite(grad_norm)):
                    raise ArithmeticError("nonfinite gradient")
                opt.step()
            elapsed=time.monotonic()-t0
            outputs.append({"architecture":name,"seed":seed,
                "width":width,"parameters":sum(p.numel() for p in model.parameters()),
                "steps":steps,"cpu_train_seconds":elapsed,**evaluate(model,dev)})
    # Only fixed-past baselines; no indicators nor volatility fit on dev.
    last_true=np.array([c.target_usd for c in dev],dtype=float)
    last_anchor=np.array([c.anchor_usd for c in dev],dtype=float)
    baseline={"persistence_mae_usd":float(np.mean(np.abs(last_anchor-last_true)))}
    return {"experiment":"btc_bitstamp_d1_h1_m1_exploratory_three_architectures",
        "interval":interval,"source":"user-approved unchanged Bitstamp compressed archives",
        "not_hyperliquid_history":True,
        "train_target_before":"2022-01-01T00:00:00Z",
        "development_target_before":"2026-01-01T00:00:00Z",
        "2026_observations_quarantined":True,
        "independent_test_used":False,
        "not_executable_backtest":True,
        "zero_volume_and_time_gaps_excluded":True,
        "training_cases":len(train),"development_cases":len(dev),
        "candidate_origins_scanned":available,
        "sampling_stride":step,
        "shared_samples_and_minibatches":True,
        "compute_matched":False,
        "parameter_near_matched":capacity["all_within_10_percent"],
        "output_head":"BASE Gaussian rounded log-return code",
        "baseline":baseline,"results":outputs,
        "torch_version":torch.__version__,
        "python_version":platform.python_version()}


def main(argv=None):
    p=argparse.ArgumentParser(description="TRAME offline Bitstamp H1/M1 development comparison")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--steps",type=int,default=40)
    p.add_argument("--seeds",type=int,nargs="+",default=[20261025,20261026,20261027])
    p.add_argument("--output",type=Path,required=True)
    ns=p.parse_args(argv)
    if ns.output.exists():
        p.error("refusing to overwrite an existing report")
    result=compare_history(interval=ns.interval,folder=ns.directory,
                           steps=ns.steps,seeds=ns.seeds)
    ns.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
                         encoding="utf-8")
    print(f"TRAME BTC {ns.interval} exploratory report: {ns.output}")


if __name__=="__main__":
    main()
