"""A7.5: descriptive BTC D1/H1/M1 baseline stability by calendar year and ex-ante volatility.

Volatility groups use cutoffs fitted ONLY on train candles, not future outcomes.
This is development-only research. Groups are descriptive, not independent
tests or evidence of profitable trading. No exchange or network usage.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.statistical_baselines import (
    _matrix, _score, fit_baselines,
)
from research.btc_h1_m1.stream import ROOT


def _volatility(cases):
    arr=np.asarray([c.encoded_past for c in cases],dtype=float)
    if arr.ndim != 2 or arr.shape[1] < 5:
        raise ValueError("at least five past codes required")
    return np.std(arr, axis=1, ddof=0)/1000.


def _scores(cases, config):
    x, anchor, actual, _ = _matrix(cases)
    norm=(x-np.asarray(config["feature_mean"]))/np.asarray(
        config["feature_scale_train_only"])
    mu=np.column_stack((np.ones(len(x)),norm)) @ np.asarray(config["ridge_weights"])
    models={
        "persistence": (np.zeros(len(x)),config["persistence_train_sigma_log"]),
        "ridge_three_past_only_features": (mu, config["ridge_train_residual_sigma_log"]),
    }
    result={}
    for name,(point,sigma) in models.items():
        report=_score(anchor,actual,point,sigma)
        pred=anchor*np.exp(point)
        report["mean_abs_relative_error_bps"]=float(np.mean(
            np.abs(pred-actual)/actual)*10_000)
        result[name]=report
    return result


def group_report(train, development, *, min_group=32):
    if type(min_group) is not int or not 32 <= min_group <= 1000:
        raise ValueError("minimum group 32..1000")
    config=fit_baselines(train)
    if any(not 2022 <= c.target_open.year < 2026 for c in development):
        raise ValueError("2026 and outside-development labels forbidden")
    train_vol=_volatility(train)
    lo,hi=np.quantile(train_vol,(1/3,2/3))
    dev_vol=_volatility(development)
    classified=defaultdict(list)
    for case,v in zip(development,dev_vol):
        band="low" if v < lo else "middle" if v < hi else "high"
        classified[("year",str(case.target_open.year))].append(case)
        classified[("trailing_volatility",band)].append(case)
    result=[]
    for (dimension,label),cases in sorted(classified.items()):
        row={"dimension":dimension,"group":label,
             "observations":len(cases),
             "enough_observations_for_descriptive_score":len(cases)>=min_group,
             "scores":_scores(cases,config) if len(cases)>=min_group else None}
        result.append(row)
    return {
        "experiment":"BTC_DEVELOPMENT_REGIME_BASELINES_V1",
        "data_origin":"USER_APPROVED_PRIVATE_BITSTAMP_HISTORICAL",
        "data_origin_independently_verified":False,
        "baseline_fit_train_only":True,
        "regime_thresholds_derived_train_only":True,
        "thresholds_train_only_log_return_sigma":{
            "tercile_one":float(lo),"tercile_two":float(hi)},
        "available_context_used_for_regimes_only":True,
        "development_years":"2022-2025",
        "2026_test_opened":False,
        "is_confirmatory":False,
        "not_hyperliquid_fills":True,
        "groups":result,
    }


def main(argv=None):
    p=argparse.ArgumentParser(description="Train-only BTC regime baselines, exploratory")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists():
        p.error("refusing to overwrite an existing report")
    step=60 if args.interval=="M1" else 1
    pools,counts=collect(args.interval,args.directory,stride=step)
    report=group_report(pools["train"],pools["development"])
    report["resolution"]=args.interval
    report["scanned_origin_counts"]=counts
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
                           encoding="utf-8")
    print(f"Exploratory BTC {args.interval} regime baselines: {args.output}")


if __name__=="__main__":
    main()
