"""Honest single-machine timing report; NO claims of equivalent FLOPs or scaling.

Run with no other heavy task for indicative timings. Includes the complete
4096-cell normalizer; warm-up + repeated CPU runs. Output is diagnostics,
not a frozen performance benchmark across different machines or versions.
"""
import json
import platform
import statistics
import time

import numpy as np
import scipy
import torch

try:
    from .head import Head, hierarchical_logits
    from .torch_head import nll
except ImportError:
    from head import Head, hierarchical_logits
    from torch_head import nll


def median_milliseconds(fn, *, repeats=12, warmup=3):
    for _ in range(warmup):
        fn()
    data=[]
    for _ in range(repeats):
        start=time.perf_counter_ns()
        fn()
        data.append((time.perf_counter_ns()-start)/1e6)
    return {'median_ms':statistics.median(data),
            'minimum_ms':min(data),'maximum_ms':max(data),
            'samples':repeats}


def run():
    torch.set_num_threads(1)
    rng=np.random.default_rng(20261025)
    coarse=rng.normal(0,.2,512)
    bits=rng.normal(0,.2,(3,2))
    arms={'BASE':None,'FLAT':rng.normal(0,.2,4096),
          'HIER':hierarchical_logits(coarse,bits)}
    results={}
    for name,values in arms.items():
        results[name]={
            'scipy_create_head_including_4096_cell_normalizer':
                median_milliseconds(lambda:Head(mu=0.,sigma=8.,logits=values,max_sigma=64.))
        }
        tvals=(None if values is None else torch.tensor(values,dtype=torch.float64))
        mu=torch.tensor(0.,dtype=torch.float64,requires_grad=True)
        sigma=torch.tensor(8.,dtype=torch.float64,requires_grad=True)
        def forward_backward():
            if mu.grad is not None:
                mu.grad.zero_()
            if sigma.grad is not None:
                sigma.grad.zero_()
            loss,_=nll(1,mu,sigma,tvals)
            loss.backward()
        results[name]['torch_f64_forward_backward_including_normalizer'] = median_milliseconds(forward_backward)
    return {'experiment':'p1b0_stage1_single_cpu_timing_v0.1',
            'market_data':False,'cuda_used':False,
            'environment':{
                'python':platform.python_version(),
                'numpy':np.__version__,'scipy':scipy.__version__,
                'torch':torch.__version__,
                'torch_threads':torch.get_num_threads(),
                'machine':platform.machine(),
                'processor':platform.processor(),
                'platform':platform.platform(),
            },'timings':results,
            'reliability':'exploratory single-machine timings; CI runners noisy; not a GPU or comparable-model benchmark',
            'float64_required':True,'float32_unsupported_for_scientific_head':True}


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
