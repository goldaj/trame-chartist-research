"""Tiny causal Transformer forecasting P1-B0 BASE on artificial integer paths.

Small-footprint wiring experiment, NOT the full P1-B0 architecture.
No asset embeddings, ECB context 256, HIER/FLAT corrections, or
calibrated real-market forecasts. Those are future controlled experiments.
"""
import torch
from torch import nn

try:
    from ..p1b0_numerics.torch_head import bounds_transform, log_interval_mass, logit_for_sigma
except ImportError:
    from torch_head import bounds_transform, log_interval_mass, logit_for_sigma


class MiniTRAME(nn.Module):
    def __init__(self, *, length=20, width=16):
        super().__init__()
        if not (1<=length<=20 and width%2==0):
            raise ValueError('length 1..20, width multiple of 2')
        self.length=length
        self.input_proj=nn.Linear(1,width,dtype=torch.float64)
        self.position=nn.Embedding(length,width,dtype=torch.float64)
        layer=nn.TransformerEncoderLayer(d_model=width,nhead=2,
                  dim_feedforward=width*2,dropout=0.0,batch_first=True,
                  activation='gelu',norm_first=True,dtype=torch.float64)
        self.backbone=nn.TransformerEncoder(layer,num_layers=1,enable_nested_tensor=False)
        self.output=nn.Linear(width,2,dtype=torch.float64)
        with torch.no_grad():
            self.output.weight.mul_(.01)
            self.output.bias[0]=0.
            self.output.bias[1]=logit_for_sigma(NOISE_SIGMA_INIT)
        self.S=64.

    def forward(self, prior_codes):
        if prior_codes.ndim!=2 or prior_codes.shape[1]>self.length or prior_codes.shape[1]<1:
            raise ValueError('batch x context length 1..20 required')
        if prior_codes.dtype!=torch.float64:
            raise TypeError('double precision required during research qualification')
        if not torch.isfinite(prior_codes).all():
            raise ValueError('nonfinite context')
        T=prior_codes.shape[1]
        positions=torch.arange(T,device=prior_codes.device)
        x=self.input_proj((prior_codes/8.)[:,:,None])+self.position(positions)[None,:,:]
        causal=torch.triu(torch.ones((T,T),device=prior_codes.device,dtype=torch.bool),diagonal=1)
        hidden=self.backbone(x,mask=causal)
        raw=self.output(hidden)
        mu,sigma=bounds_transform(raw[...,0],raw[...,1],S=self.S)
        return mu,sigma

    def nll(self, prior_codes, actual_codes):
        if prior_codes.shape!=actual_codes.shape:
            raise ValueError('input and target shapes must match')
        mu,sigma=self.forward(prior_codes)
        # In BASE all core corrections vanish: exact Z=1 mathematically.
        # Therefore no need to sum 4096 cells at every training step.
        # This is NOT the HIER/FLAT loss where Z must be computed.
        target=actual_codes.to(dtype=torch.float64)
        return -log_interval_mass(target,mu,sigma).mean()


NOISE_SIGMA_INIT = 3.
