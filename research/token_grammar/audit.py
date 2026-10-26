"""S3.0c offline grammar-information audit, no forecasting or trading.

Operates on causal completed PAST returns per case. Report is a
reconstruction / information-loss diagnostic only. Never ranks models
or estimates PnL. 2026 labels excluded by existing split validator.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.runner import _source_code_commit, _origin_digest
from research.scaling_study.runner import _validate_chronology
from research.token_grammar.diagnostics import (
    continuous_grammar, legacy_grammar, signed_uniform_grammar,
    fit_signed_quantile_grammar, reconstruction_diagnostics,
)


def _past(cases):
    if not cases:
        raise ValueError("empty case cohort")
    if any(len(c.continuous_past_bps)!=20 for c in cases):
        raise ValueError("completed 20-return contexts required")
    return tuple(float(x) for c in cases for x in c.continuous_past_bps)


def run_cases(train, development, *, interval, data_origin="ARTIFICIAL_FIXTURE",
              quantile_bins=5):
    if interval not in ("D1","H1","M1"):
        raise ValueError("expected D1/H1/M1 resolution")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PRIVATE_REAL"):
        raise ValueError("unrecognised provenance")
    if type(quantile_bins) is not int or not 2<=quantile_bins<=16:
        raise ValueError("2..16 quantile magnitude buckets required")
    _validate_chronology(train,development)
    model_commit=_source_code_commit(data_origin)
    past_train=_past(train)
    past_dev=_past(development)
    gram={
        "legacy_g0a":legacy_grammar(),
        "continuous_g0b":continuous_grammar(),
        "signed_uniform_g1":signed_uniform_grammar(),
        "signed_quantile_g2":fit_signed_quantile_grammar(
            past_train,bins=quantile_bins),
    }
    train_scores={}
    dev_scores={}
    for name,grammar in gram.items():
        train_scores[name]=reconstruction_diagnostics(grammar,past_train)
        dev_scores[name]=reconstruction_diagnostics(grammar,past_dev)
        if train_scores[name]["forecast_skill_measured"] or dev_scores[name]["forecast_skill_measured"]:
            raise AssertionError("tokenizer information must not be called forecast skill")
    return {
        "experiment":"TRAME_S3_TOKEN_INFORMATION_AUDIT_V1",
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "model_trained":False,"price_prediction_performed":False,
        "transaction_simulation_performed":False,"fees_ignored":True,
        "independent_test_used":False,"labels_2026_opened":False,
        "quantile_vocab_fit_train_only":True,
        "quantile_bins":quantile_bins,
        "quantile_magnitude_boundaries_bps":list(
            gram["signed_quantile_g2"].boundaries_bps),
        "sampled_train_origins":len(train),
        "sampled_development_origins":len(development),
        "past_tokens_per_origin":20,
        "context_token_observations_overlapping":True,
        "estimated_unique_candle_count":None,
        "train_origins_sha256":_origin_digest(train),
        "development_origins_sha256":_origin_digest(development),
        "model_source_commit":model_commit,
        "train_context_reconstruction":train_scores,
        "development_context_reconstruction":dev_scores,
        "caveat":"OVERLAPPING 20-step contexts re-use candles. Token counts are not independent observations and no signal forecast has been measured.",
    }


def run_history(*,interval,directory=ROOT,max_train=4096,max_dev=1024,
                quantile_bins=5):
    if interval not in ("D1","H1","M1"):
        raise ValueError("expected D1/H1/M1")
    stride=60 if interval=="M1" else 1
    pools,scanned=collect(
        interval,Path(directory),max_train=max_train,max_dev=max_dev,
        stride=stride)
    result=run_cases(
        pools["train"],pools["development"],interval=interval,
        data_origin="BTC_PRIVATE_REAL",quantile_bins=quantile_bins)
    result["scanned_candidate_origins"]=scanned
    result["sampling_stride"]=stride
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="S3 token grammar information-loss audit, not forecasting")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--quantile-bins",type=int,default=5)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists():
        p.error("refusing to overwrite research result")
    result=run_history(
        interval=args.interval,directory=args.directory,
        quantile_bins=args.quantile_bins)
    args.output.write_text(json.dumps(
        result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
        encoding="utf-8")
    print("Diagnostic of codec information only; not a BTC forecasting result.")


if __name__=="__main__":
    main()
