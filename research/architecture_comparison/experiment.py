"""Paired, development-only architecture comparison on manufactured AR(1).

Same splits, same minibatches, same optimizer/precision and scoring family.
NOT param- or compute-matched; neither test nor actual financial data opened.
"""
import argparse
import json
import platform
import time

import numpy as np
import torch

from research.mini_gpt_synthetic.data import get_split, previous_codes
from research.mini_gpt_synthetic.model import MiniTRAME
from research.architecture_comparison.models import ModernGPTMini, GRUMini

ARMS = {'legacy_causal_transformer': MiniTRAME,
        'modern_gpt_style_mini': ModernGPTMini,
        'recurrent_gru_control': GRUMini}


def compare(*, steps=20, seeds=(20261025,)):
    if type(steps) is not int or not 1 <= steps <= 200:
        raise ValueError('steps must be an integer between 1 and 200')
    if not isinstance(seeds, (tuple, list)) or not seeds or any(type(s) is not int for s in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError('unique integer seeds required')
    torch.set_num_threads(1)
    train, development = get_split('train'), get_split('development')
    xtrain = torch.as_tensor(previous_codes(train), dtype=torch.float64)
    ytrain = torch.as_tensor(train, dtype=torch.float64)
    xdev = torch.as_tensor(previous_codes(development), dtype=torch.float64)
    ydev = torch.as_tensor(development, dtype=torch.float64)
    output = []
    for seed in seeds:
        # Draw minibatches ONCE for all architecture families under this seed.
        rng = np.random.default_rng(seed)
        batches = [rng.integers(0, len(train), size=16) for _ in range(steps)]
        for name, factory in ARMS.items():
            torch.manual_seed(seed)
            model = factory(width=16).train()
            optimizer = torch.optim.AdamW(model.parameters(), lr=.003, weight_decay=.001)
            model.eval()
            with torch.no_grad():
                initial = float(model.nll(xdev, ydev))
            model.train()
            clock = time.monotonic()
            for idx in batches:
                optimizer.zero_grad(set_to_none=True)
                loss = model.nll(xtrain[idx], ytrain[idx])
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError('nonfinite training loss')
                loss.backward()
                grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
                if not bool(torch.isfinite(grad_norm)):
                    raise ArithmeticError('nonfinite gradient')
                optimizer.step()
            elapsed = time.monotonic() - clock
            model.eval()
            with torch.no_grad():
                final = float(model.nll(xdev, ydev))
                training = float(model.nll(xtrain, ytrain))
            output.append({'architecture': name, 'seed': seed,
                           'parameter_count': sum(p.numel() for p in model.parameters()),
                           'start_development_nll': initial,
                           'end_development_nll': final,
                           'end_train_nll': training,
                           'wall_seconds_cpu': elapsed,
                           'steps': steps, 'batch_size_paths': 16})
    return {'experiment': 'trame_architecture_comparison_synthetic_exploratory_v0.1',
            'data': 'artificial rounded-Gaussian AR(1), not financial markets',
            'data_origin': 'ARTIFICIAL_ONLY',
            'architectures': list(ARMS),
            'split_used': ['train', 'development'],
            'reserved_synthetic_test_opened': False,
            'financial_holdout_opened': False,
            'common_loss': 'BASE rounded Gaussian cell NLL',
            'common_optimizer': 'AdamW lr=.003 weight_decay=.001 grad_clip=5',
            'precision': 'torch.float64 CPU',
            'same_batches_per_seed': True,
            'parameter_matched': False, 'compute_matched': False,
            'times_are_hardware_specific': True,
            'not_modern_llm_or_mamba_benchmark': True,
            'torch_version': torch.__version__, 'python_version': platform.python_version(),
            'results': output}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Synthetic research only, no markets')
    ap.add_argument('--steps', type=int, default=20)
    ap.add_argument('--seeds', type=int, nargs='+', default=[20261025])
    ns = ap.parse_args(argv)
    print(json.dumps(compare(steps=ns.steps, seeds=ns.seeds), indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
