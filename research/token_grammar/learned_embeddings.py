"""S3.1B trainable scalar categorical token embeddings; causal BTC SPOT research.

Each past return maps to one of 11 categorical IDs. Numeric baseline uses
fixed bin centers / common TRAIN scale; learned arms use a trainable table
nn.Embedding(11,1) before the identical S2b transformer backbone.

Learned arms add EXACTLY 11 trainable scalars vs numeric, a disclosed
capacity confound. Ordered-vs-random learned arms are exactly capacity matched.
No learned vector embedding or live trading.
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
from torch import nn
from torch.nn import functional as F

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT
from research.continuous_direction.models import ContinuousDirectionModel,forecast_prices
from research.continuous_direction.diagnostics import prior_from_train,probability_report
from research.continuous_direction.runner import _arrays,_origin_digest,_source_code_commit
from research.representation_ablation.runner import _paired_base_scores,features as s2b_features
from research.scaling_study.runner import _validate_chronology
from research.scaling_study.metrics import score_forecasts
from research.token_grammar.predictive import TrainOnlyGrammarFeatures

GRAMMARS=("signed_uniform_g1","signed_quantile_g2")
ARMS=("decoded","embedding_ordered","embedding_random")
MODES=("regression","joint")
VOCAB_SIZE=11


def token_id(token):
    if token=="FLAT":
        return 0
    for prefix,base in (("DOWN",1),("UP",6)):
        if token.startswith(prefix):
            suffix=token[len(prefix):]
            if suffix in ("0","1","2","3","4"):
                return base+int(suffix)
    raise ValueError("unexpected signed token or out of range bin")


class CausalTokenProvider:
    def __init__(self,train):
        self.train_grammar=TrainOnlyGrammarFeatures(train,quantile_bins=5)
        self.quantile_boundaries_bps=self.train_grammar.quantile_boundaries_bps

    def centers(self,grammar):
        if grammar not in GRAMMARS:
            raise ValueError("only G1 and G2")
        codec=self.train_grammar.codecs[grammar]
        centers=tuple(float(x) for x in codec.centers_bps)
        if len(centers)!=5:
            raise ValueError("expected five bins")
        return np.asarray((0.,)+tuple(-x for x in centers)+centers,
                          dtype=np.float64)

    def ids(self,cases,grammar):
        if grammar not in GRAMMARS or not cases:
            raise ValueError("unknown grammar or empty cases")
        codec=self.train_grammar.codecs[grammar]
        if any(len(c.continuous_past_bps)!=20 for c in cases):
            raise ValueError("must use 20 completed past returns")
        values=np.asarray([
            tuple(token_id(x) for x in codec.encode(c.continuous_past_bps))
            for c in cases],dtype=np.int64)
        if values.shape!=(len(cases),20) or np.any(values>=VOCAB_SIZE):
            raise ValueError("invalid token matrix")
        return values

    def decoded(self,cases,grammar):
        return self.centers(grammar)[self.ids(cases,grammar)]


class TokenScalarModel(nn.Module):
    """Same S2b network, with 11-value learnable scalar lookup before it."""

    def __init__(self,*,width,depth,mode,init_style,centers_bps,scale_bps):
        super().__init__()
        if init_style not in ("ordered","random"):
            raise ValueError("invalid embedding initialization")
        if (type(scale_bps) not in (float,int)
                or not math.isfinite(scale_bps) or scale_bps<=0):
            raise ValueError("positive common train-only normalizer required")
        vals=np.asarray(centers_bps,dtype=np.float64)
        if vals.shape!=(VOCAB_SIZE,) or not np.all(np.isfinite(vals)):
            raise ValueError("exactly 11 finite center values required")
        self.core=ContinuousDirectionModel(
            width=width,depth=depth,context=20,mode=mode)
        self.mode=mode
        self.backbone_initial_sha256=hashlib.sha256(b"".join(
            p.detach().cpu().contiguous().numpy().tobytes()
            for p in self.core.parameters())).hexdigest()
        self.token_embedding=nn.Embedding(
            VOCAB_SIZE,1,dtype=torch.float64)
        with torch.no_grad():
            if init_style=="ordered":
                self.token_embedding.weight[:,0].copy_(
                    torch.as_tensor(vals/scale_bps,dtype=torch.float64))
            else:
                self.token_embedding.weight.normal_(0.0,.25)
        self.initial_embedding_sha256=hashlib.sha256(
            self.token_embedding.weight.detach().numpy().tobytes()).hexdigest()

    def forward(self,x):
        if (x.ndim!=2 or x.shape[1]!=20 or x.dtype!=torch.int64
                or not bool(((x>=0)&(x<VOCAB_SIZE)).all())):
            raise ValueError("int64 causal token IDs in [0,11) expected")
        decoded=self.token_embedding(x).squeeze(-1)
        return self.core(decoded)

    def loss(self,x,y):
        if (y.ndim!=1 or y.shape[0]!=x.shape[0]
            or y.dtype!=torch.float64 or not bool(torch.isfinite(y).all())):
            raise ValueError("target must be finite continuous float64")
        mu,logit=self(x)
        loss=F.smooth_l1_loss(mu,y,beta=1.)
        if self.mode=="regression":
            return loss
        keep=y!=0
        if not bool(keep.any()):
            return loss
        return loss+0.5*F.binary_cross_entropy_with_logits(
            logit[keep],(y[keep]>0).to(dtype=torch.float64))


def _sha_params(model):
    return hashlib.sha256(b"".join(
        p.detach().cpu().contiguous().numpy().tobytes()
        for p in model.parameters())).hexdigest()


def _validate_dimensions(widths,depths,seeds,steps,batch_size,
                         grammars,arms,modes):
    for names,allowed,label in (
        (grammars,GRAMMARS,"grammars"),
        (arms,ARMS,"arms"),
        (modes,MODES,"modes"),
        (depths,(1,2),"depths")):
        if not names or len(set(names))!=len(names) or any(x not in allowed for x in names):
            raise ValueError("invalid "+label)
    if (not widths or len(set(widths))!=len(widths)
        or any(type(w)!=int or w<8 or w%4 for w in widths)
        or not seeds or len(set(seeds))!=len(seeds)
        or any(type(s)!=int for s in seeds)
        or type(steps)!=int or not 1<=steps<=2000
        or type(batch_size)!=int or not 1<=batch_size<=256):
        raise ValueError("invalid training grid")


def run_cases(train,dev,*,interval,grammars=GRAMMARS,
              arms=ARMS,modes=MODES,widths=(16,32),
              depths=(1,2),seeds=(20261025,20261026,20261027),
              steps=200,batch_size=16,data_origin="ARTIFICIAL_FIXTURE"):
    if interval not in ("D1","H1","M1"):
        raise ValueError("invalid interval")
    if data_origin not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL"):
        raise ValueError("invalid data provenance")
    _validate_dimensions(widths,depths,seeds,steps,batch_size,
                         grammars,arms,modes)
    _validate_chronology(train,dev)
    if len(train)<32 or len(dev)<32:
        raise ValueError(">=32 cases per split required")
    source_sha=_source_code_commit(data_origin)
    provider=CausalTokenProvider(train)
    train_continuous=s2b_features(train,"continuous_bps")
    scale=float(np.std(train_continuous))
    scale_fallback=not math.isfinite(scale) or scale<=1e-8
    if scale_fallback:
        scale=1.
    _xs,_an,_ac,y=_arrays(train)
    ys=torch.as_tensor(y/scale,dtype=torch.float64)
    controls,thresholds,dev_anchors,dev_actuals=_paired_base_scores(train,dev)
    prior=prior_from_train(train)
    prepared={}
    for grammar in grammars:
        train_ids=provider.ids(train,grammar)
        dev_ids=provider.ids(dev,grammar)
        centers=provider.centers(grammar)
        prepared[grammar]={
            "centers":centers,
            "train_ids":torch.as_tensor(train_ids,dtype=torch.int64),
            "dev_ids":torch.as_tensor(dev_ids,dtype=torch.int64),
            "train_decoded":torch.as_tensor(centers[train_ids]/scale,
                                            dtype=torch.float64),
            "dev_decoded":torch.as_tensor(centers[dev_ids]/scale,
                                          dtype=torch.float64),
            "vocabulary_train_used":int(len(set(train_ids.reshape(-1).tolist()))),
            "vocabulary_dev_used":int(len(set(dev_ids.reshape(-1).tolist()))),
        }
    torch.set_num_threads(1)
    results=[]
    for seed in seeds:
        batch_rng=np.random.default_rng(seed)
        batches=[batch_rng.integers(0,len(train),size=batch_size)
                 for _ in range(steps)]
        for width in widths:
            for depth in depths:
                for mode in modes:
                    for grammar in grammars:
                        entry=prepared[grammar]
                        for arm in arms:
                            torch.manual_seed(seed)
                            if arm=="decoded":
                                model=ContinuousDirectionModel(
                                    width=width,depth=depth,context=20,mode=mode)
                                backbone_sha=_sha_params(model)
                                embedding_sha=None
                            else:
                                init_style=("ordered" if arm=="embedding_ordered"
                                            else "random")
                                model=TokenScalarModel(
                                    width=width,depth=depth,mode=mode,
                                    init_style=init_style,
                                    centers_bps=entry["centers"],
                                    scale_bps=scale)
                                backbone_sha=model.backbone_initial_sha256
                                embedding_sha=model.initial_embedding_sha256
                            xtrain=(entry["train_decoded"] if arm=="decoded"
                                    else entry["train_ids"])
                            xdev=(entry["dev_decoded"] if arm=="decoded"
                                  else entry["dev_ids"])
                            optimizer=torch.optim.AdamW(
                                model.parameters(),lr=.003,weight_decay=.001)
                            started=time.perf_counter()
                            model.train()
                            for idx in batches:
                                optimizer.zero_grad(set_to_none=True)
                                loss=model.loss(xtrain[idx],ys[idx])
                                if not bool(torch.isfinite(loss)):
                                    raise ArithmeticError("nonfinite research loss")
                                loss.backward()
                                grad=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
                                if not bool(torch.isfinite(grad)):
                                    raise ArithmeticError("nonfinite gradients")
                                optimizer.step()
                            elapsed=time.perf_counter()-started
                            prices=[]
                            probs=[]
                            returns=[]
                            for start in range(0,len(dev),64):
                                ids=slice(start,start+64)
                                p,up,mu=forecast_prices(
                                    model,xdev[ids],
                                    dev_anchors[ids],scale_bps=float(scale))
                                prices.extend(p.tolist())
                                probs.extend(up.tolist())
                                returns.extend(mu.tolist())
                            scores=score_forecasts(
                                dev_anchors,dev_actuals,np.asarray(prices),
                                train_thresholds=thresholds)
                            if mode=="joint":
                                classifications=probability_report(
                                    dev_anchors,dev_actuals,probs,train_prior=prior)
                                classifications["head_regression_sign_disagreement"]=float(
                                    np.mean((np.asarray(probs)>=.5)!=
                                            (np.asarray(returns)>=0)))
                            else:
                                classifications={
                                    "binary_probabilities_from_trained_head":False,
                                    "brier_nonflat":None,
                                    "brier_skill_vs_train_prior":None,
                                    "head_regression_sign_disagreement":None,
                                }
                            total=sum(x.numel() for x in model.parameters())
                            results.append({
                                "grammar":grammar,"arm":arm,"mode":mode,
                                "width":width,"depth":depth,"seed":seed,
                                "steps":steps,"batch_size":batch_size,
                                "parameter_count":total,
                                "embedding_trainable_parameters":(0 if arm=="decoded" else VOCAB_SIZE),
                                "backbone_parameter_count":(
                                    total if arm=="decoded" else total-VOCAB_SIZE),
                                "backbone_initial_sha256":backbone_sha,
                                "embedding_initial_sha256":embedding_sha,
                                "train_normalizer_std_bps_common":scale,
                                "vocabulary_size":VOCAB_SIZE,
                                "vocabulary_train_used":entry["vocabulary_train_used"],
                                "vocabulary_dev_used":entry["vocabulary_dev_used"],
                                "cpu_train_seconds":elapsed,
                                "last_minibatch_loss":float(loss.detach()),
                                **scores,**classifications,
                            })
    return {
        "experiment":"TRAME_S3_1B_SCALAR_LEARNED_TOKEN_EMBEDDINGS_V1",
        "created_at_utc":datetime.now(timezone.utc).isoformat(),
        "data_origin":data_origin,"interval":interval,
        "train_count":len(train),"dev_count":len(dev),
        "train_before":"2022-01-01","dev_years":"2022-2025",
        "labels_2026_opened":False,"independent_test_used":False,
        "quantile_fit_on":"TRAIN_PAST_CONTEXTS_ONLY",
        "quantile_boundaries_bps":list(provider.quantile_boundaries_bps),
        "same_backbone_initialisation":True,
        "same_target_and_input_scale_train_only":True,
        "common_batch_indices_per_seed":True,
        "learned_vs_decoded_trainable_params_matched":False,
        "ordered_vs_random_trainable_params_matched":True,
        "transaction_costs_ignored":True,
        "not_cumulative_portfolio_return":True,
        "train_origins_sha256":_origin_digest(train),
        "development_origins_sha256":_origin_digest(dev),
        "model_source_commit":source_sha,
        "github_workflow_commit":os.environ.get("GITHUB_SHA","not recorded outside CI"),
        "python_version":platform.python_version(),
        "torch_version":torch.__version__,
        "train_only_direction_prior":prior,
        "baseline_scores":controls,
        "seeds":list(seeds),"steps":steps,
        "grammars":list(grammars),"arms":list(arms),"modes":list(modes),
        "results":results,
    }


def run_history(*,interval,directory=ROOT,grammars=GRAMMARS,
                arms=ARMS,modes=MODES,widths=(16,32),
                depths=(1,2),seeds=(20261025,20261026,20261027),
                steps=200,data_origin="BTC_PUBLIC_REAL",
                max_train=4096,max_dev=1024):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 expected")
    stride=60 if interval=="M1" else 1
    cohorts,scanned=collect(interval,Path(directory),
                            max_train=max_train,max_dev=max_dev,stride=stride)
    result=run_cases(cohorts["train"],cohorts["development"],
                     interval=interval,grammars=grammars,arms=arms,modes=modes,
                     widths=widths,depths=depths,seeds=seeds,steps=steps,
                     data_origin=data_origin)
    result["sampling_stride"]=stride
    result["scanned_candidates"]=scanned
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description="S3.1B learned 11-token scalar embedding offline experiment")
    p.add_argument("--interval",choices=("D1","H1","M1"),required=True)
    p.add_argument("--directory",type=Path,default=ROOT)
    p.add_argument("--grammars",nargs="+",choices=GRAMMARS,default=list(GRAMMARS))
    p.add_argument("--arms",nargs="+",choices=ARMS,default=list(ARMS))
    p.add_argument("--modes",nargs="+",choices=MODES,default=list(MODES))
    p.add_argument("--widths",nargs="+",type=int,default=[16,32])
    p.add_argument("--depths",nargs="+",type=int,default=[1,2])
    p.add_argument("--steps",type=int,default=200)
    p.add_argument("--seeds",nargs="+",type=int,
                   default=[20261025,20261026,20261027])
    p.add_argument("--data-origin",choices=("BTC_PUBLIC_REAL",),
                   default="BTC_PUBLIC_REAL")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists():
        p.error("refusing to overwrite existing research output")
    result=run_history(interval=a.interval,directory=a.directory,
                       grammars=tuple(a.grammars),arms=tuple(a.arms),
                       modes=tuple(a.modes),widths=tuple(a.widths),
                       depths=tuple(a.depths),seeds=tuple(a.seeds),
                       steps=a.steps,data_origin=a.data_origin)
    a.output.write_text(json.dumps(result,indent=2,
                        allow_nan=False)+"\n",encoding="utf-8")
    print("S3.1B saved: development-only, no 2026 holdout or trading")


if __name__=="__main__":
    main()
