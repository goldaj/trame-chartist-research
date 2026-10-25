"""Ablation probe: tiny Transformer + P1-B0 BASE/HIER/FLAT heads.

Controlled miniature is NOT the 256-context published architecture. Fixed
backbone width and optimization steps; output parameter counts differ.
All examples are artificial; never read the reserved synthetic test.
"""
import torch
from torch import nn

from research.p1b0_numerics.torch_head import bounds_transform, log_interval_mass
from research.mini_gpt_synthetic.model import MiniTRAME


def corrected_batched_nll(actual, mu, sigma, corrections):
    """Fully normalized P1-B0 likelihood, including out-of-core targets."""
    if actual.shape!=mu.shape or mu.shape!=sigma.shape or corrections.shape!=(*actual.shape,4096):
        raise ValueError('target, parameters and 4096-correction shapes mismatch')
    if actual.dtype!=torch.float64 or corrections.dtype!=torch.float64:
        raise TypeError('scientific ablation requires float64')
    device=actual.device
    grid=torch.arange(-2048,2048,device=device,dtype=torch.float64)
    logq=log_interval_mass(grid,mu[...,None],sigma[...,None])
    bounded=4.*torch.tanh(corrections/4.)
    lp_left=torch.special.log_ndtr((-2048.5-mu)/sigma)
    lp_right=torch.special.log_ndtr(-(2047.5-mu)/sigma)
    logz=torch.logsumexp(torch.cat([logq+bounded,lp_left[...,None],
                                    lp_right[...,None]],dim=-1),dim=-1)
    center=(actual>=-2048)&(actual<=2047)
    # Index is clamped ONLY to keep gather in bounds; actual target likelihood
    # is evaluated unmodified, including true out-of-core labels.
    gather_index=(actual.long()+2048).clamp(0,4095)
    corr_target=torch.gather(bounded,-1,gather_index[...,None]).squeeze(-1)
    raw_target=log_interval_mass(actual,mu,sigma)
    return (logz-raw_target-torch.where(center,corr_target,0.)).mean()


class CorrectedMiniTRAME(MiniTRAME):
    def __init__(self,arm='HIER',*,length=8,width=16):
        if arm not in ('HIER','FLAT'):
            raise ValueError('corrected arm must be HIER or FLAT')
        super().__init__(length=length,width=width)
        self.arm=arm
        self.correction_output=nn.Linear(width, 518 if arm=='HIER' else 4096,
                                         dtype=torch.float64)
        nn.init.zeros_(self.correction_output.weight)
        nn.init.zeros_(self.correction_output.bias)

    def forward_full(self,prior_codes):
        if prior_codes.ndim!=2 or prior_codes.shape[1]>self.length:
            raise ValueError('too many tokens')
        if prior_codes.dtype!=torch.float64:
            raise TypeError('need float64 inputs')
        t=prior_codes.shape[1]
        pos=torch.arange(t,device=prior_codes.device)
        x=self.input_proj(prior_codes[...,None]/8.) + self.position(pos)[None,...]
        mask=torch.triu(torch.ones((t,t),device=prior_codes.device,
                                   dtype=torch.bool),diagonal=1)
        hidden=self.backbone(x,mask=mask)
        raw=self.output(hidden)
        mu,sigma=bounds_transform(raw[...,0],raw[...,1],S=self.S)
        rawcor=self.correction_output(hidden)
        if self.arm=='FLAT':
            corrected=rawcor
        else:
            coarse=rawcor[...,:512]
            bits=rawcor[...,512:].reshape(*rawcor.shape[:-1],3,2)
            code=torch.arange(-2048,2048,device=prior_codes.device)
            qi=torch.div(code,8,rounding_mode='floor')+256
            remainder=torch.remainder(code,8)
            corrected=coarse[...,qi]
            for j,shift in enumerate((2,1,0)):
                corrected=corrected+bits[...,j,((remainder>>shift)&1)]
        return mu,sigma,corrected

    def nll(self,prior_codes,actual_codes):
        mu,sigma,raw=self.forward_full(prior_codes)
        return corrected_batched_nll(actual_codes,mu,sigma,raw)
