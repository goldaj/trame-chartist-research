"""Stage-2 miniature autoregressive language-model experiment, artificial data.

Never reads reserved synthetic test; train/development are disjoint streams.
The toy AR(1) oracle and a TRAIN-ONLY fitted linear Gaussian forecaster are
strong controls. One run is exploratory, NOT a market predictive result.
"""
import argparse
import json
import math
import platform
import time

import numpy as np
import torch

from research.p1b0_numerics.torch_head import log_interval_mass
from research.mini_gpt_synthetic.data import (get_split, previous_codes,
                                               NOISE_SIGMA,RHO,SPLIT_SEEDS)
from research.mini_gpt_synthetic.model import MiniTRAME


def to_inputs(codes):
    return (torch.tensor(previous_codes(codes),dtype=torch.float64),
            torch.tensor(codes,dtype=torch.float64))


def log_loss_gaussian(target,mu,sigma):
    t=torch.tensor(target,dtype=torch.float64)
    m=torch.as_tensor(mu,dtype=torch.float64)
    s=torch.as_tensor(sigma,dtype=torch.float64)
    with torch.no_grad():
        return float(-log_interval_mass(t,m,s).mean())


def fit_linear_train_only(train_codes):
    x=previous_codes(train_codes).reshape(-1).astype(np.float64)
    y=train_codes.reshape(-1).astype(np.float64)
    matrix=np.stack((np.ones_like(x),x),axis=1)
    offset,coeff=np.linalg.lstsq(matrix,y,rcond=None)[0]
    sigma=math.sqrt(float(np.mean((y-offset-coeff*x)**2)))
    return {'intercept':float(offset),'coefficient':float(coeff),
            'sigma':max(.25,sigma),'fit_examples':int(len(x)),
            'fitted_on':'train_only'}


def baselines(train,development):
    previous=previous_codes(development)
    oracle=log_loss_gaussian(development,RHO*previous,NOISE_SIGMA)
    fit=fit_linear_train_only(train)
    linear=log_loss_gaussian(development,
               fit['intercept']+fit['coefficient']*previous,fit['sigma'])
    const_scale=max(.25,float(np.std(train.reshape(-1))))
    constant=log_loss_gaussian(development,0.,const_scale)
    return {'oracle_known_generator_nll':oracle,
            'linear_train_only_nll':linear,
            'constant_mu0_train_scale_nll':constant,
            'linear_parameters':fit,
            'constant_sigma_fit_train_only':const_scale}


def run(*,steps=40,seed=20261025):
    if type(steps) is not int or not (1<=steps<=200):
        raise ValueError('1..200 predeclared toy optimization steps')
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    np_rng=np.random.default_rng(seed)
    train=get_split('train')
    dev=get_split('development')
    xtrain,ytrain=to_inputs(train)
    xdev,ydev=to_inputs(dev)
    model=MiniTRAME(width=16).train()
    optim=torch.optim.AdamW(model.parameters(),lr=.003,weight_decay=.001)
    model.eval()
    with torch.no_grad():
        initial=float(model.nll(xdev,ydev))
    model.train()
    start=time.monotonic()
    losses=[]
    for t in range(steps):
        indices=np_rng.integers(0,len(train),size=16)
        optim.zero_grad(set_to_none=True)
        loss=model.nll(xtrain[indices],ytrain[indices])
        if not bool(torch.isfinite(loss)):
            raise ArithmeticError('nonfinite training loss')
        loss.backward()
        grad_norm=torch.nn.utils.clip_grad_norm_(model.parameters(),max_norm=5.)
        if not bool(torch.isfinite(grad_norm)):
            raise ArithmeticError('nonfinite gradient norm')
        optim.step()
        losses.append(float(loss.detach()))
    seconds=time.monotonic()-start
    model.eval()
    with torch.no_grad():
        devloss=float(model.nll(xdev,ydev))
        trainloss=float(model.nll(xtrain,ytrain))
    return {
        'experiment':'mini_transformer_p1b0_base_stage2_dev_v0.1',
        'data':'synthetic rounded-Gaussian AR1 integer increments, no market data',
        'rho':RHO,'innovation_sigma':NOISE_SIGMA,
        'split_seeds':{k:v for k,v in SPLIT_SEEDS.items()
                        if k!='reserved_synthetic_test'},
        'reserved_test_not_opened':True,
        'model':'one causal TransformerEncoder layer, width16, 2 heads; BASE Gaussian head',
        'not_full_p1b0':True,'not_trading_model':True,
        'train_paths':int(len(train)), 'development_paths':int(len(dev)),
        'sequence_length':int(train.shape[1]),
        'model_parameters':sum(p.numel() for p in model.parameters()),
        'torch_seed':seed,'optimizer':'AdamW lr=.003, clip=5',
        'optimization_steps':steps, 'train_batch_paths':16,
        'start_development_nll':initial,
        'end_development_nll':devloss,'end_train_nll':trainloss,
        'last_train_batch_nll':losses[-1],
        'controls_development':baselines(train,dev),
        'wall_seconds_cpu':seconds,'torch_version':torch.__version__,
        'python_version':platform.python_version(),
        'interpretation':'exploratory synthetic development, not held-out market validation',
    }


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps',type=int,default=40)
    ns=parser.parse_args()
    print(json.dumps(run(steps=ns.steps),indent=2,allow_nan=False))
