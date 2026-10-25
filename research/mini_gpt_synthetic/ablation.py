"""Small fixed-budget BASE/HIER/FLAT learning comparison on artificial dev.

DO NOT infer model superiority: output parameter counts and compute differ.
The 16 development samples are exploratory, not a protected test cohort.
"""
import json
import math
import time

import numpy as np
import torch

from research.mini_gpt_synthetic.data import get_split,previous_codes
from research.mini_gpt_synthetic.model import MiniTRAME
from research.mini_gpt_synthetic.corrected_model import CorrectedMiniTRAME
from research.mini_gpt_synthetic.experiment import baselines


def run(steps=6):
    if type(steps) is not int or not (1<=steps<=15):
        raise ValueError('small fixed-budget probe only')
    torch.set_num_threads(1)
    train=get_split('train')[:,:8]
    dev=get_split('development')[:16,:8]
    train_prior=torch.tensor(previous_codes(train),dtype=torch.float64)
    train_target=torch.tensor(train,dtype=torch.float64)
    dev_prior=torch.tensor(previous_codes(dev),dtype=torch.float64)
    dev_target=torch.tensor(dev,dtype=torch.float64)
    rng=np.random.default_rng(20261025)
    selections=[rng.integers(0,len(train),size=4) for _ in range(steps)]
    report={}
    for arm in ['BASE','HIER','FLAT']:
        torch.manual_seed(20261025)
        model=MiniTRAME(length=8) if arm=='BASE' else CorrectedMiniTRAME(arm,length=8)
        optim=torch.optim.AdamW(model.parameters(),lr=.001)
        model.eval()
        with torch.no_grad():
            before=float(model.nll(dev_prior,dev_target))
        model.train()
        started=time.monotonic()
        for ix in selections:
            optim.zero_grad(set_to_none=True)
            loss=model.nll(train_prior[ix],train_target[ix])
            if not torch.isfinite(loss):
                raise ArithmeticError('nonfinite ablation loss')
            loss.backward()
            norm=torch.nn.utils.clip_grad_norm_(model.parameters(),5.)
            if not torch.isfinite(norm):
                raise ArithmeticError('nonfinite correction gradients')
            optim.step()
        duration=time.monotonic()-started
        model.eval()
        with torch.no_grad():
            after=float(model.nll(dev_prior,dev_target))
        report[arm]={'before_dev_nll':before,'after_dev_nll':after,
                     'parameter_count':sum(p.numel() for p in model.parameters()),
                     'optimization_steps':steps,
                     'wall_seconds_cpu':duration}
    return {'experiment':'tiny_corrected_heads_development_ablation_v0.1',
            'market_data':False,'reserved_test_opened':False,'sequence_length':8,
            'development_paths':16,'train_paths':len(train),
            'same_random_initialization_seed':20261025,
            'same_minibatch_indices':True,'same_optimizer_steps':steps,
            'arm_results':report,
            'controls':baselines(train,dev),
            'capacity_equalized':False,'flops_equalized':False,
            'conclusion':'exploratory numerical ablation only, not efficacy ranking or market validation'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,allow_nan=False))
