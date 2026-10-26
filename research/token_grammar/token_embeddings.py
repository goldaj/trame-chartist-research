"""S3.1B genuinely learned categorical tokens with a matched hybrid backbone.

Five arms always instantiate the SAME embedding+scalar network. No data
download, train/test split selection, future label or market execution here.
"""
from __future__ import annotations

import numpy as np
import torch
from torch import nn

from research.continuous_direction.models import ContinuousDirectionModel
from research.representation_ablation.runner import features as s2b_features
from research.token_grammar.predictive import TrainOnlyGrammarFeatures


ARMS=("continuous_scalar","g1_decoded_scalar","g1_learned_token",
      "g2_decoded_scalar","g2_learned_token")
VOCAB_SIZE=11
TOKEN_TO_ID={"FLAT":0, **{f"UP{i}":1+i for i in range(5)},
             **{f"DOWN{i}":6+i for i in range(5)}}


class TokenHybridDirectionModel(ContinuousDirectionModel):
    """Both channels and ALL 11 token embeddings exist in every arm."""

    def __init__(self, *, width=16, depth=1, context=20, mode="regression"):
        super().__init__(width=width,depth=depth,context=context,mode=mode)
        self.token_embedding=nn.Embedding(VOCAB_SIZE,width,dtype=torch.float64)

    def forward(self, token_and_return):
        x=token_and_return
        if (x.ndim!=3 or x.shape[-1]!=2 or
                not 1<=x.shape[1]<=self.context or
                x.dtype!=torch.float64 or
                not bool(torch.isfinite(x).all())):
            raise ValueError("finite float64 [batch,context,2] expected")
        scalars=x[:,:,0]
        ids=x[:,:,1]
        if (bool(torch.any(ids<0)) or
                bool(torch.any(ids>=VOCAB_SIZE)) or
                not bool(torch.all(ids==torch.floor(ids)))):
            raise ValueError("token ids must be exact integers in vocabulary 0..10")
        hidden=self.input_proj(scalars.unsqueeze(-1))
        hidden=hidden+self.token_embedding(ids.to(torch.int64))
        for block in self.blocks:
            hidden=block(hidden)
        final=self.last_norm(hidden[:,-1])
        return (self.return_head(final).squeeze(-1),
                self.direction_head(final).squeeze(-1))


class EmbeddingGrammarFeatures:
    """Immutable TRAIN-only codec fit; never inspect future dev targets."""

    def __init__(self,train, *,quantile_bins=5):
        self.base=TrainOnlyGrammarFeatures(train,quantile_bins=quantile_bins)
        continuous=s2b_features(train,"continuous_bps")
        std=float(np.std(continuous))
        if not np.isfinite(std) or std<1e-8:
            std=1.0
            self.scale_fallback=True
        else:
            self.scale_fallback=False
        self.train_scalar_scale_bps=std
        self.quantile_boundaries_bps=self.base.quantile_boundaries_bps
        self.quantile_centers_bps=self.base.quantile_centers_bps

    def __call__(self,cases,arm):
        if arm not in ARMS:
            raise ValueError("unknown embedding grammar")
        if not cases or any(len(c.continuous_past_bps)!=20 for c in cases):
            raise ValueError("need 20 completed historical log-returns")
        n=len(cases)
        x=np.zeros((n,20,2),dtype=np.float64)
        if arm=="continuous_scalar":
            x[:,:,0]=s2b_features(cases,"continuous_bps")/self.train_scalar_scale_bps
        elif arm in ("g1_decoded_scalar","g2_decoded_scalar"):
            family=("signed_uniform_g1" if arm.startswith("g1") else "signed_quantile_g2")
            x[:,:,0]=self.base(cases,family)/self.train_scalar_scale_bps
        else:
            family=("signed_uniform_g1" if arm.startswith("g1") else "signed_quantile_g2")
            codec=self.base.codecs[family]
            for i,c in enumerate(cases):
                x[i,:,1]=[TOKEN_TO_ID[t] for t in codec.encode(c.continuous_past_bps)]
        if not np.isfinite(x).all():
            raise ValueError("nonfinite encoded features")
        return x
