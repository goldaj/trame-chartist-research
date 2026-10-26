"""S2b: matched input representation ablation, synthetic or authorised offline.

Quantized vs continuous INPUTS ONLY; targets are identical true returns.
Same architecture, target normalizer, loss, seed and minibatch sequence.
This is not a trading strategy or an independently validated backtest.
"""
from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import time

import numpy as np
import torch

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.models import ContinuousDirectionModel
from research.continuous_direction.runner import (
    _arrays, _origin_digest, _source_code_commit, _ridge_forecasts,
)
from research.continuous_direction.diagnostics import prior_from_train
from research.scaling_study.runner import _validate_chronology
from research.scaling_study.metrics import (
    training_magnitude_thresholds, baseline_forecasts, score_forecasts,
)


REPRESENTATIONS = ("continuous_bps", "legacy_quantized_bps")
MODES = ("regression", "joint")


def features(cases, representation):
    """Always fit transforms from past data; no target is read in this function."""
    if representation not in REPRESENTATIONS:
        raise ValueError("unknown representation")
    if not cases:
        raise ValueError("nonempty causal cases required")
    if any(len(c.encoded_past) != 20 or len(c.continuous_past_bps) != 20
           for c in cases):
        raise ValueError("all cases require exactly 20 historical returns")
    if representation == "continuous_bps":
        result = np.asarray([c.continuous_past_bps for c in cases], dtype=np.float64)
    else:
        # Uses the ACTUAL historical code rather than re-quantizing a potentially
        # rounded continuous feature from a different calculation.
        result = 10.0 * np.asarray([c.encoded_past for c in cases],
                                    dtype=np.float64)
    if result.shape != (len(cases), 20) or not np.isfinite(result).all():
        raise ValueError("invalid causal return feature matrix")
    return result


def quantization_diagnostics(cases):
    actual=features(cases,"continuous_bps")
    quantized=features(cases,"legacy_quantized_bps")
    actual_nonzero=actual != 0.
    lost=actual_nonzero & (np.sign(actual)!=np.sign(quantized))
    return {
        "past_observations":int(actual.size),
        "past_nonzero_observations":int(np.sum(actual_nonzero)),
        "past_quantized_to_zero_count":int(np.sum(actual_nonzero & (quantized==0))),
        "past_sign_lost_or_changed_count":int(np.sum(lost)),
        "past_sign_lost_fraction_nonzero":(
            float(np.sum(lost)/np.sum(actual_nonzero))
            if np.any(actual_nonzero) else None),
        "past_reconstruction_mae_bps":float(np.mean(np.abs(actual-quantized))),
        "diagnostics_only_not_prediction_skill":True,
    }


def _paired_base_scores(train, development):
    _past, anchors, actuals, train_y = _arrays(train)
    thresholds=training_magnitude_thresholds(train)
    _, dev_anchors, dev_actuals, _ = _arrays(development)
    controls={}
    for name,prediction in baseline_forecasts(development).items():
        controls[name]=score_forecasts(
            dev_anchors,dev_actuals,prediction,train_thresholds=thresholds)
    controls["ridge_train_only"]=score_forecasts(
        dev_anchors,dev_actuals,_ridge_forecasts(train,development),
        train_thresholds=thresholds)
    drift=float(np.mean(train_y))
    controls["mean_log_return_train_only"]=score_forecasts(
        dev_anchors,dev_actuals,dev_anchors*np.exp(drift/10000.),
        train_thresholds=thresholds)
    return controls, thresholds, dev_anchors, dev_actuals


def run_cases(train, development, *, interval,
              representations=REPRESENTATIONS, modes=MODES,
              widths=(16,32), depths=(1,2),
              seeds=(20261025,20261026,20261027),
              steps=200, batch_size=16, data_origin="ARTIFICIAL_FIXTURE"):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 only")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PRIVATE_REAL"):
        raise ValueError("invalid origin")
    for name,values,allowed in (
        ("representations",representations,REPRESENTATIONS),
        ("modes",modes,MODES),("depths",depths,(1,2))):
        if not values or any(v not in allowed for v in values) or len(set(values))!=len(values):
            raise ValueError("invalid or duplicate "+name)
    if (not widths or any(type(w) is not int or w<8 or w%4 for w in widths)
            or len(set(widths))!=len(widths)
            or not seeds or len(seeds)>10 or
            any(type(s) is not int for s in seeds) or len(set(seeds))!=len(seeds)
            or type(steps) is not int or not 1<=steps<=2000
            or type(batch_size) is not int or not 1<=batch_size<=256):
        raise ValueError("invalid widths, seeds, steps, or minibatches")
    _validate_chronology(train,development)
    if len(train)<32 or len(development)<32:
        raise ValueError("at least 32 training and 32 dev cases required")
    model_sha=_source_code_commit(data_origin)
    _,_,_,true_train_returns=_arrays(train)
    scale_target=float(np.std(features(train,"continuous_bps")))
    if not math.isfinite(scale_target) or scale_target<=1.e-8:
        scale_target=1.0
        target_scale_fallback=True
    else:
        target_scale_fallback=False
    ytrain=torch.as_tensor(true_train_returns/scale_target,dtype=torch.float64)
    controls,thresholds,dev_anchors,dev_actuals=_paired_base_scores(
        train,development)
    prior=prior_from_train(train)

    prepared={}
    for representation in representations:
        input_train=features(train,representation)
        observed_std=float(np.std(input_train))
        information_degenerate=(not math.isfinite(observed_std) or
                                observed_std<=1.e-8)
        # CRITICAL: both arms use the SAME input denominator learned from
        # continuous TRAIN features. Different denominators would confound
        # the measured effect of rounding with an implicit rescaling.
        prepared[representation]={
            "train_tensor":torch.as_tensor(
                input_train/scale_target,dtype=torch.float64),
            "train_std_bps":scale_target,
            "observed_input_train_std_bps":observed_std,
            "information_degenerate":information_degenerate,
            "train_diagnostics":quantization_diagnostics(train)
            if representation=="legacy_quantized_bps" else None,
        }
    torch.set_num_threads(1)
    results=[]
    for seed in seeds:
        rng=np.random.default_rng(seed)
        common_batches=[rng.integers(0,len(train),size=batch_size)
                        for _ in range(steps)]
        for width in widths:
            for depth in depths:
                for mode in modes:
                    for representation in representations:
                        torch.manual_seed(seed)
                        model=ContinuousDirectionModel(
                            width=width,depth=depth,context=20,mode=mode)
                        initial_state_sha256=hashlib.sha256(b''.join(
                            p.detach().cpu().contiguous().numpy().tobytes()
                            for p in model.parameters())).hexdigest()
                        optimizer=torch.optim.AdamW(
                            model.parameters(),lr=.003,weight_decay=.001)
                        xt=prepared[representation]["train_tensor"]
                        model.train()
                        started=time.perf_counter()
                        for indices in common_batches:
                            optimizer.zero_grad(set_to_none=True)
                            loss=model.loss(xt[indices],ytrain[indices])
                            if not bool(torch.isfinite(loss)):
                                raise ArithmeticError("nonfinite training loss")
                            loss.backward()
                            norm=torch.nn.utils.clip_grad_norm_(
                                model.parameters(),5.0)
                            if not bool(torch.isfinite(norm)):
                                raise ArithmeticError("nonfinite gradients")
                            optimizer.step()
                        elapsed=time.perf_counter()-started
                        # Evaluate the matched representation with the SAME
                        # target de-normalizer on precisely the same dev labels.
                        from research.continuous_direction.models import forecast_prices
                        input_dev=features(development,representation)
                        forecast=[]
                        probabilities=[]
                        regression=[]
                        model.eval()
                        for start in range(0,len(development),64):
                            ids=slice(start,start+64)
                            x=torch.as_tensor(
                                input_dev[ids] / prepared[representation]["train_std_bps"],
                                dtype=torch.float64)
                            p,up,mu=forecast_prices(
                                model,x,dev_anchors[ids],
                                scale_bps=float(scale_target))
                            forecast.extend(p.tolist())
                            probabilities.extend(up.tolist())
                            regression.extend(mu.tolist())
                        stats=score_forecasts(
                            dev_anchors,dev_actuals,np.asarray(forecast),
                            train_thresholds=thresholds)
                        classification={}
                        if mode=="joint":
                            from research.continuous_direction.diagnostics import probability_report
                            classification=probability_report(
                                dev_anchors,dev_actuals,probabilities,
                                train_prior=prior)
                            classification["head_regression_sign_disagreement"]=float(
                                np.mean((np.asarray(probabilities)>=.5)
                                        != (np.asarray(regression)>=0)))
                        else:
                            classification={
                                "binary_probabilities_from_trained_head":False,
                                "brier_nonflat":None,
                                "brier_skill_vs_train_prior":None,
                                "head_regression_sign_disagreement":None,
                            }
                        results.append({
                            "representation":representation,
                            "architecture":"gpt_style_continuous_backbone",
                            "mode":mode,"width":width,"depth":depth,"seed":seed,
                            "steps":steps,"batch_size":batch_size,
                            "parameter_count":sum(p.numel() for p in model.parameters()),
                            "initial_state_sha256":initial_state_sha256,
                            "input_normalizer_std_bps":prepared[representation]["train_std_bps"],
                            "observed_input_train_std_bps":prepared[representation]["observed_input_train_std_bps"],
                            "input_information_degenerate":prepared[representation]["information_degenerate"],
                            "input_scale_fallback":target_scale_fallback,
                            "target_normalizer_std_bps_common":scale_target,
                            "observed_cpu_train_seconds":elapsed,
                            "last_minibatch_loss":float(loss.detach()),
                            **stats, **classification,
                        })
    return {
        "experiment":"TRAME_S2B_REPRESENTATION_ABLATION_V1",
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "train_count":len(train),"dev_count":len(development),
        "train_before":"2022-01-01","development":"2022-2025",
        "labels_2026_opened":False,"independent_test_used":False,
        "transaction_costs_ignored":True,
        "not_cumulative_portfolio_return":True,
        "compute_matched":False,
        "same_target_normalization_all_representations":True,
        "same_input_normalization_all_representations":True,
        "shared_input_normalizer_train_continuous_std_bps":scale_target,
        "target_train_std_bps":scale_target,
        "target_scale_degenerate_fallback":target_scale_fallback,
        "quantization_input_train":quantization_diagnostics(train),
        "quantization_input_development":quantization_diagnostics(development),
        "representations":list(representations),"modes":list(modes),
        "common_batch_indices_per_seed":True,
        "train_only_direction_prior":prior,
        "baseline_scores":controls,
        "seeds":list(seeds),"steps":steps,
        "train_origins_sha256":_origin_digest(train),
        "development_origins_sha256":_origin_digest(development),
        "model_source_commit":model_sha,
        "github_workflow_commit":os.environ.get("GITHUB_SHA","not recorded outside CI"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "results":results,
    }


def run_history(*,interval,directory=ROOT,steps=200,
                representations=REPRESENTATIONS,modes=MODES,
                widths=(16,32),depths=(1,2),
                seeds=(20261025,20261026,20261027),
                max_train=4096,max_dev=1024):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 only")
    stride=60 if interval=="M1" else 1
    pools,scanned=collect(
        interval,Path(directory),max_train=max_train,max_dev=max_dev,stride=stride)
    report=run_cases(
        pools["train"],pools["development"],
        interval=interval,representations=representations,modes=modes,
        widths=widths,depths=depths,seeds=seeds,steps=steps,
        data_origin="BTC_PRIVATE_REAL")
    report["scanned_candidates"]=scanned
    report["sampling_stride"]=stride
    return report


def main(argv=None):
    p=argparse.ArgumentParser(description="TRAME S2b input-only ablation, offline")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--representations",choices=REPRESENTATIONS,nargs="+",
                   default=list(REPRESENTATIONS))
    p.add_argument("--modes",choices=MODES,nargs="+",default=list(MODES))
    p.add_argument("--widths",type=int,nargs="+",default=[16,32])
    p.add_argument("--depths",type=int,nargs="+",default=[1,2])
    p.add_argument("--steps",type=int,default=200)
    p.add_argument("--seeds",type=int,nargs="+",
                   default=[20261025,20261026,20261027])
    p.add_argument("--output",type=Path,required=True)
    ns=p.parse_args(argv)
    if ns.output.exists():
        p.error("refusing to overwrite existing results")
    result=run_history(
        interval=ns.interval,directory=ns.directory,steps=ns.steps,
        representations=tuple(ns.representations),modes=tuple(ns.modes),
        widths=tuple(ns.widths),depths=tuple(ns.depths),seeds=tuple(ns.seeds))
    ns.output.write_text(json.dumps(
        result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",encoding="utf-8")
    print("Exploratory S2b analysis saved; 2026 unopened; no trades")


if __name__=="__main__":
    main()
