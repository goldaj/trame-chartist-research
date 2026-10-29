"""Hardware-specific CPU forward/backward timings on artificial training inputs.

This is a diagnostic, NOT FLOPs parity or performance on financial data.
"""
import argparse
import json
import platform
import statistics
import time

import torch

from research.architecture_comparison.experiment import ARMS
from research.mini_gpt_synthetic.data import get_split, previous_codes


def cost_audit(*, widths=(8, 16, 32), repeats=10, seed=20261025):
    if (not isinstance(widths,(tuple,list)) or not widths
            or any(type(x) is not int or x not in (8,12,16,20,24,28,32) for x in widths)
            or len(set(widths))!=len(widths)):
        raise ValueError('unique supported widths required')
    if type(repeats) is not int or not 3<=repeats<=100:
        raise ValueError('repeats between 3 and 100')
    if type(seed) is not int:
        raise ValueError('integer seed required')
    torch.set_num_threads(1)
    toy=get_split('train')[:8,:8]
    x=torch.as_tensor(previous_codes(toy),dtype=torch.float64)
    y=torch.as_tensor(toy,dtype=torch.float64)
    output=[]
    for name,factory in ARMS.items():
        for width in widths:
            torch.manual_seed(seed)
            model=factory(width=width)
            model.eval()
            with torch.no_grad():
                for _ in range(3): model.nll(x,y)
            elapsed_fwd=[]
            with torch.no_grad():
                for _ in range(repeats):
                    start=time.perf_counter()
                    model.nll(x,y)
                    elapsed_fwd.append(1000*(time.perf_counter()-start))
            model.train()
            for _ in range(3):
                model.zero_grad(set_to_none=True)
                model.nll(x,y).backward()
            elapsed_back=[]
            for _ in range(repeats):
                model.zero_grad(set_to_none=True)
                start=time.perf_counter()
                model.nll(x,y).backward()
                elapsed_back.append(1000*(time.perf_counter()-start))
            output.append({
                'architecture':name,'width':width,
                'parameters':sum(p.numel() for p in model.parameters()),
                'median_forward_ms':statistics.median(elapsed_fwd),
                'median_forward_backward_ms':statistics.median(elapsed_back),
                'repeats':repeats, 'workload':'8 synthetic paths x 8 tokens, float64 CPU',
            })
    return {'experiment':'hardware_dependent_architecture_cost_diagnostic',
            'data_origin':'ARTIFICIAL_ONLY',
            'reserved_synthetic_test_opened':False,
            'device':'cpu', 'threads':1, 'seed':seed,
            'torch_version':torch.__version__,'python_version':platform.python_version(),
            'not_fair_flops_comparison':True,
            'no_inference_throughput_claim':True,
            'results':output}


def main(argv=None):
    ap=argparse.ArgumentParser(description='Synthetic-only architecture CPU profiling')
    ap.add_argument('--repeats',type=int,default=10)
    ap.add_argument('--widths',type=int,nargs='+',default=[8,16,32])
    ns=ap.parse_args(argv)
    print(json.dumps(cost_audit(widths=ns.widths,repeats=ns.repeats),indent=2,allow_nan=False))


if __name__=='__main__':
    main()
