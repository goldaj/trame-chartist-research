"""A5.4 paired synthetic comparison: original arms vs causal attention+GRU.

No Mamba, no financial data. Parameters/FLOPs/tuning NOT matched.
"""
from __future__ import annotations

import argparse
import json
import platform
import time

import numpy as np
import torch

from research.architecture_comparison.experiment import ARMS, choose_widths
from research.hybrid_controls.models import AttentionGRUHybrid
from research.mini_gpt_synthetic.data import get_split, previous_codes


HYBRID_ARMS = {**ARMS, "attention_gru_hybrid_control": AttentionGRUHybrid}


def compare_hybrid(*, steps=12, seeds=(20261025, 20261026, 20261027)):
    if type(steps) is not int or not 1 <= steps <= 200:
        raise ValueError("steps 1..200 required")
    if (not isinstance(seeds, (tuple, list)) or len(seeds) < 3
            or len(set(seeds)) != len(seeds)
            or any(type(s) is not int for s in seeds)):
        raise ValueError("at least three distinct integer seeds required")
    torch.set_num_threads(1)
    train = get_split("train")
    dev = get_split("development")
    xt = torch.as_tensor(previous_codes(train), dtype=torch.float64)
    yt = torch.as_tensor(train, dtype=torch.float64)
    xd = torch.as_tensor(previous_codes(dev), dtype=torch.float64)
    yd = torch.as_tensor(dev, dtype=torch.float64)
    original = choose_widths()["selected"]
    widths = {name: row["width"] for name, row in original.items()}
    widths["attention_gru_hybrid_control"] = 16
    results = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        indices = [rng.integers(0, len(train), size=16) for _ in range(steps)]
        for name, factory in HYBRID_ARMS.items():
            torch.manual_seed(seed)
            model = factory(width=widths[name], length=20)
            optimizer = torch.optim.AdamW(model.parameters(), lr=.003,
                                          weight_decay=.001)
            model.train()
            start = time.perf_counter()
            for batch in indices:
                optimizer.zero_grad(set_to_none=True)
                loss = model.nll(xt[batch], yt[batch])
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite loss")
                loss.backward()
                gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
                if not bool(torch.isfinite(gn)):
                    raise ArithmeticError("nonfinite gradient")
                optimizer.step()
            elapsed = time.perf_counter() - start
            model.eval()
            with torch.no_grad():
                val = float(model.nll(xd, yd))
            if not np.isfinite(val):
                raise ArithmeticError("nonfinite development NLL")
            results.append({
                "seed": seed, "architecture": name, "width": widths[name],
                "parameters": sum(p.numel() for p in model.parameters()),
                "train_cpu_seconds": elapsed, "development_nll": val,
                "train_steps": steps, "same_minibatches_per_seed": True})
    return {
        "experiment": "a5_attention_gru_control_paired_synthetic_v0.1",
        "data_origin": "ARTIFICIAL_ONLY",
        "split_used": ["train", "development"],
        "reserved_synthetic_test_opened": False,
        "financial_holdout_opened": False,
        "mamba_ssm_implemented_in_this_branch": False,
        "hybrid_is_selective_ssm": False,
        "compute_matched": False, "parameter_matched": False,
        "tuning_budget_matched": False,
        "same_batch_prefix": True,
        "torch_version": torch.__version__, "python_version": platform.python_version(),
        "results": results,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="CPU synthetic attention+GRU baseline")
    ap.add_argument("--steps", type=int, default=12)
    ap.add_argument("--seeds", nargs="+", type=int,
                    default=[20261025, 20261026, 20261027])
    args = ap.parse_args(argv)
    print(json.dumps(compare_hybrid(steps=args.steps, seeds=args.seeds),
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
