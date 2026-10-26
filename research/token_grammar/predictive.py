"""S3.1A predictive decoder-grammar ablation, BTC SPOT research only.

Uses the identical S2b network/loss, model init, minibatch indices, target,
scale, year cutoff and labels. Codec quantiles fitted on TRAIN past only.
All 4 decoded inputs remain scalar returns in basis points. This is NOT
a learned categorical embedding experiment (that is S3.1B).
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path

import numpy as np

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT
from research.representation_ablation.runner import (
    run_cases as s2b_run_cases, features as s2b_features,
)
from research.token_grammar.diagnostics import (
    signed_uniform_grammar, fit_signed_quantile_grammar,
    reconstruction_diagnostics,
)
from research.scaling_study.runner import _validate_chronology

GRAMMARS=("continuous_bps","legacy_quantized_bps",
          "signed_uniform_g1","signed_quantile_g2")
LOSSES=("regression","joint")


def _flatten_train(cases):
    if not cases:
        raise ValueError("train cases required")
    if any(len(c.continuous_past_bps)!=20 for c in cases):
        raise ValueError("only complete 20-bar histories")
    return tuple(float(x) for c in cases for x in c.continuous_past_bps)


class TrainOnlyGrammarFeatures:
    """Immutable vocabulary fitted once to the caller's TRAIN cohort.

    To make the model architecture fully matched, the tokens are decoded
    back to a single scalar bps per candle *before* the common input_proj.
    """

    def __init__(self, train, *, quantile_bins=5):
        self.reference_train_past=_flatten_train(train)
        self.codecs={
            "signed_uniform_g1":signed_uniform_grammar(),
            "signed_quantile_g2":fit_signed_quantile_grammar(
                self.reference_train_past,bins=quantile_bins),
        }
        self.quantile_boundaries_bps=tuple(
            self.codecs["signed_quantile_g2"].boundaries_bps)
        self.quantile_centers_bps=tuple(
            self.codecs["signed_quantile_g2"].centers_bps)
        self.quantile_bins=quantile_bins

    def __call__(self,cases,grammar):
        if grammar in ("continuous_bps","legacy_quantized_bps"):
            return s2b_features(cases,grammar)
        if grammar not in self.codecs:
            raise ValueError("not a declared S3.1 grammar")
        codec=self.codecs[grammar]
        # Each context is complete and chronological. Never use target.
        if not cases or any(len(c.continuous_past_bps)!=20 for c in cases):
            raise ValueError("20 historical returns required")
        result=np.asarray([
            codec.decode(codec.encode(c.continuous_past_bps))
            for c in cases],dtype=np.float64)
        if result.shape!=(len(cases),20) or not np.isfinite(result).all():
            raise ValueError("invalid causal grammar features")
        return result


def run_cases(train,development,*,interval,grammars=GRAMMARS,
              modes=LOSSES,widths=(16,32),depths=(1,2),
              seeds=(20261025,20261026,20261027),
              steps=200,batch_size=16,
              data_origin="ARTIFICIAL_FIXTURE",quantile_bins=5):
    _validate_chronology(train,development)
    if not grammars or any(g not in GRAMMARS for g in grammars) or len(set(grammars))!=len(grammars):
        raise ValueError("invalid S3 grammar selection")
    codec=TrainOnlyGrammarFeatures(train,quantile_bins=quantile_bins)
    result=s2b_run_cases(
        train,development,interval=interval,
        representations=tuple(grammars),modes=tuple(modes),
        widths=tuple(widths),depths=tuple(depths),
        seeds=tuple(seeds),steps=steps,batch_size=batch_size,
        data_origin=data_origin,feature_provider=codec)
    result["experiment"]="TRAME_S3_1A_PREDICTIVE_GRAMMAR_V1"
    result["grammar_stage"]="decoded_scalar_ablation_NO_LEARNED_TOKEN_EMBEDDINGS"
    result["grammars"]=list(grammars)
    result["quantile_fit_on"]="TRAIN_PAST_CONTEXTS_ONLY"
    result["quantile_bins"]=quantile_bins
    result["quantile_boundaries_bps"]=list(codec.quantile_boundaries_bps)
    result["quantile_centers_bps"]=list(codec.quantile_centers_bps)
    result["sampling_contexts_overlapping"]=True
    result["prediction_dev_selected_not_independent"]=True
    result["no_future_price_as_grammar_input"]=True
    result["grammar_reconstruction_dev"]={
        name:reconstruction_diagnostics(
            codec.codecs[name],
            tuple(float(x) for case in development for x in case.continuous_past_bps))
        for name in ("signed_uniform_g1","signed_quantile_g2")
    }
    return result


def run_history(*,interval,directory=ROOT,grammars=GRAMMARS,
                modes=LOSSES,widths=(16,32),depths=(1,2),
                seeds=(20261025,20261026,20261027),
                steps=200,batch_size=16,quantile_bins=5,
                data_origin="BTC_PUBLIC_REAL",
                max_train=4096,max_dev=1024):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 expected")
    stride=60 if interval=="M1" else 1
    cohorts,scanned=collect(interval,Path(directory),
                            max_train=max_train,max_dev=max_dev,stride=stride)
    result=run_cases(cohorts["train"],cohorts["development"],
                     interval=interval,grammars=grammars,modes=modes,
                     widths=widths,depths=depths,seeds=seeds,
                     steps=steps,batch_size=batch_size,
                     quantile_bins=quantile_bins,data_origin=data_origin)
    result["sampling_stride"]=stride
    result["scanned_candidates"]=scanned
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="S3.1A real decoded grammar forecast comparison (offline)")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--grammars",nargs="+",choices=GRAMMARS,default=list(GRAMMARS))
    p.add_argument("--modes",nargs="+",choices=LOSSES,default=list(LOSSES))
    p.add_argument("--widths",nargs="+",type=int,default=[16,32])
    p.add_argument("--depths",nargs="+",type=int,default=[1,2])
    p.add_argument("--steps",type=int,default=200)
    p.add_argument("--seeds",nargs="+",type=int,default=[20261025,20261026,20261027])
    p.add_argument("--quantile-bins",type=int,default=5)
    p.add_argument("--data-origin",choices=("BTC_PUBLIC_REAL","BTC_PRIVATE_REAL"),
                   default="BTC_PUBLIC_REAL")
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("refusing to overwrite scientific artifact")
    result=run_history(interval=a.interval,directory=a.directory,
                       grammars=tuple(a.grammars),modes=tuple(a.modes),
                       widths=tuple(a.widths),depths=tuple(a.depths),
                       steps=a.steps,seeds=tuple(a.seeds),
                       quantile_bins=a.quantile_bins,data_origin=a.data_origin)
    a.output.write_text(json.dumps(result,ensure_ascii=False,
                    allow_nan=False,indent=2)+"\n",encoding="utf-8")
    print("S3.1A development-only results recorded, 2026 unopened, no trades")


if __name__=="__main__":
    main()
