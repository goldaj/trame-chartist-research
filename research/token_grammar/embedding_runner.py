"""S3.1B matched scalar-decoding vs truly trained categorical embeddings.

Offline BTC research, 2026 holdout frozen; NOT market order execution.
Deliberately uses S2b metric/normalization helpers, independent model family.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
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
from research.continuous_direction.models import forecast_prices
from research.continuous_direction.runner import _arrays,_source_code_commit,_origin_digest
from research.continuous_direction.diagnostics import prior_from_train,probability_report
from research.representation_ablation.runner import _paired_base_scores
from research.scaling_study.runner import _validate_chronology
from research.scaling_study.metrics import score_forecasts
from research.token_grammar.token_embeddings import (
    TokenHybridDirectionModel,EmbeddingGrammarFeatures,ARMS,
)

MODES=("regression","joint")


def run_cases(train,dev,*,interval,arms=ARMS,modes=MODES,
              widths=(16,32),depths=(1,2),
              seeds=(20261025,20261026,20261027),
              steps=200,batch_size=16,
              data_origin="ARTIFICIAL_FIXTURE"):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1 H1 M1 only")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("fixture or pinned public BTC data only")
    if (not arms or any(x not in ARMS for x in arms)
            or len(set(arms))!=len(arms)
            or not modes or any(x not in MODES for x in modes)
            or len(set(modes))!=len(modes)):
        raise ValueError("unknown or duplicate arm/objective")
    if (not widths or len(set(widths))!=len(widths)
            or any(type(w)is not int or w<8 or w%4 for w in widths)
            or not depths or len(set(depths))!=len(depths)
            or any(d not in (1,2) for d in depths)
            or not seeds or len(set(seeds))!=len(seeds)
            or any(type(seed)is not int for seed in seeds)
            or type(steps)is not int or not 1<=steps<=2000
            or type(batch_size)is not int or not 1<=batch_size<=256):
        raise ValueError("bad factorial dimensions")
    _validate_chronology(train,dev)
    if len(train)<32 or len(dev)<32:
        raise ValueError("need >=32 chronological train and dev origins")
    source_sha=_source_code_commit(data_origin)
    codecs=EmbeddingGrammarFeatures(train)
    scale=float(codecs.train_scalar_scale_bps)
    assert math.isfinite(scale) and scale>0
    y=_arrays(train)[3]
    ytrain=torch.as_tensor(y/scale,dtype=torch.float64)
    controls,thresholds,anchors,actual=_paired_base_scores(train,dev)
    prior=prior_from_train(train)
    train_x={arm:torch.as_tensor(codecs(train,arm),dtype=torch.float64)
             for arm in arms}
    dev_x={arm:codecs(dev,arm) for arm in arms}
    torch.set_num_threads(1)
    rows=[]
    for seed in seeds:
        rng=np.random.default_rng(seed)
        minibatches=[rng.integers(0,len(train),size=batch_size)
                     for _ in range(steps)]
        for width in widths:
            for depth in depths:
                for mode in modes:
                    for arm in arms:
                        torch.manual_seed(seed)
                        model=TokenHybridDirectionModel(
                            width=width,depth=depth,context=20,mode=mode)
                        initial_sha=hashlib.sha256(b"".join(
                            p.detach().cpu().contiguous().numpy().tobytes()
                            for p in model.parameters())).hexdigest()
                        optimizer=torch.optim.AdamW(
                            model.parameters(),lr=.003,weight_decay=.001)
                        start=time.perf_counter()
                        model.train()
                        for idx in minibatches:
                            optimizer.zero_grad(set_to_none=True)
                            loss=model.loss(train_x[arm][idx],ytrain[idx])
                            if not bool(torch.isfinite(loss)):
                                raise ArithmeticError("nonfinite model loss")
                            loss.backward()
                            grad_norm=torch.nn.utils.clip_grad_norm_(
                                model.parameters(),5.0)
                            if not bool(torch.isfinite(grad_norm)):
                                raise ArithmeticError("nonfinite gradient")
                            optimizer.step()
                        elapsed=time.perf_counter()-start
                        forecasts=[]
                        probabilities=[]
                        regressions=[]
                        model.eval()
                        for a in range(0,len(dev),64):
                            sl=slice(a,a+64)
                            x=torch.as_tensor(dev_x[arm][sl],dtype=torch.float64)
                            pred,p_up,mu=forecast_prices(
                                model,x,anchors[sl],scale_bps=float(scale))
                            forecasts.extend(pred.tolist())
                            probabilities.extend(p_up.tolist())
                            regressions.extend(mu.tolist())
                        metrics=score_forecasts(
                            anchors,actual,np.asarray(forecasts),
                            train_thresholds=thresholds)
                        if mode=="joint":
                            probs=probability_report(
                                anchors,actual,probabilities,train_prior=prior)
                            probs["head_regression_sign_disagreement"]=float(
                                np.mean((np.asarray(probabilities)>=.5)
                                        !=(np.asarray(regressions)>=0)))
                        else:
                            probs={
                                "binary_probabilities_from_trained_head":False,
                                "brier_nonflat":None,
                                "brier_skill_vs_train_prior":None,
                                "head_regression_sign_disagreement":None,
                            }
                        rows.append({
                            "arm":arm,"mode":mode,"width":width,"depth":depth,
                            "seed":seed,"steps":steps,"batch_size":batch_size,
                            "initial_state_sha256":initial_sha,
                            "parameter_count":sum(p.numel() for p in model.parameters()),
                            "train_only_continuous_scale_bps":scale,
                            "token_vocab_size":11,
                            "trainable_embedding":True,
                            "observed_cpu_train_seconds":elapsed,
                            "final_training_loss":float(loss.detach()),
                            **metrics,**probs,
                        })
    return {
        "experiment":"TRAME_S3_1B_TRUE_TOKEN_EMBEDDING_V1",
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "train_count":len(train),"dev_count":len(dev),
        "train_before":"2022-01-01","dev_span":"2022-2025",
        "labels_2026_opened":False,"independent_test_used":False,
        "no_portfolio_pnl":True,"fees_ignored":True,
        "same_architecture_all_arms":True,
        "same_target_scale_all_arms":True,
        "quantile_fit_on_train_only":True,
        "common_minibatches_per_seed":True,
        "network_feature_channels":["normalized_scalar_return","integer_token_id"],
        "vocab_size_all_arms":11,
        "token_grammar_quantile_boundaries_train_bps":list(
            codecs.quantile_boundaries_bps),
        "normalization_scale_train_only_bps":scale,
        "input_scale_fallback":codecs.scale_fallback,
        "train_origins_sha256":_origin_digest(train),
        "development_origins_sha256":_origin_digest(dev),
        "model_source_commit":source_sha,
        "github_workflow_commit":os.environ.get("GITHUB_SHA","not recorded outside CI"),
        "torch_version":torch.__version__,
        "python_version":platform.python_version(),
        "arms":list(arms),"modes":list(modes),
        "seeds":list(seeds),"steps":steps,
        "baselines":controls,
        "results":rows,
    }


def run_history(*,interval,directory=ROOT,arms=ARMS,modes=MODES,
                widths=(16,32),depths=(1,2),
                seeds=(20261025,20261026,20261027),
                steps=200,data_origin="BTC_PUBLIC_REAL",
                max_train=4096,max_dev=1024):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 only")
    stride=60 if interval=="M1" else 1
    pools,scanned=collect(interval,Path(directory),max_train=max_train,
                          max_dev=max_dev,stride=stride)
    result=run_cases(pools["train"],pools["development"],interval=interval,
                     arms=arms,modes=modes,widths=widths,depths=depths,
                     seeds=seeds,steps=steps,data_origin=data_origin)
    result["sampling_stride"]=stride
    result["scanned_candidates"]=scanned
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="TRAME S3.1B truly trainable token embedding ablation")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--arms",nargs="+",choices=ARMS,default=list(ARMS))
    p.add_argument("--modes",nargs="+",choices=MODES,default=list(MODES))
    p.add_argument("--widths",nargs="+",type=int,default=[16,32])
    p.add_argument("--depths",nargs="+",type=int,default=[1,2])
    p.add_argument("--seeds",nargs="+",type=int,default=[20261025,20261026,20261027])
    p.add_argument("--steps",type=int,default=200)
    p.add_argument("--data-origin",choices=("BTC_PUBLIC_REAL",),
                   default="BTC_PUBLIC_REAL")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("will not overwrite evidence")
    result=run_history(interval=a.interval,directory=a.directory,
                       arms=tuple(a.arms),modes=tuple(a.modes),
                       widths=tuple(a.widths),depths=tuple(a.depths),
                       seeds=tuple(a.seeds),steps=a.steps,
                       data_origin=a.data_origin)
    a.output.write_text(json.dumps(result,ensure_ascii=False,
                    allow_nan=False,indent=2)+"\n",encoding="utf-8")
    print("S3.1B 2022-2025 DEV only, 2026 unopened; no trading.")


if __name__=="__main__":
    main()
