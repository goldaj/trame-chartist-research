"""A3c.4: controlled synthetic budget pilot; partial FLOP accounting != true FLOPs.

Both the calibration and training use CPU float64. Train/dev datasets are
synthetic and the reserved split is never opened. Steps per arm use one
calibrated *partial counted-op* proxy, not a scientifically complete compute
budget. This cannot rank financial architectures.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import time

import numpy as np
import torch

from research.architecture_comparison.compute_audit import compute_audit
from research.architecture_comparison.experiment import ARMS, choose_widths
from research.mini_gpt_synthetic.data import get_split, previous_codes


def allocate_steps(costs, *, reference_steps=12, step_cap=120):
    """Pure planner: use same measured counted-ops target for all arms."""
    if type(reference_steps) is not int or not 2 <= reference_steps <= 100:
        raise ValueError("reference_steps must be 2..100")
    if type(step_cap) is not int or not 2 <= step_cap <= 200:
        raise ValueError("step_cap must be 2..200")
    if (not isinstance(costs, dict) or set(costs) != set(ARMS)
            or any(type(x) is not int or x <= 0 for x in costs.values())):
        raise ValueError("one strictly positive integer cost per known architecture")
    target = statistics.median(costs.values()) * reference_steps
    result = {}
    for name in ARMS:
        unit_cost = costs[name]
        steps = max(2, min(step_cap, int(round(target / unit_cost))))
        counted_ops = steps * unit_cost
        result[name] = {
            "counted_ops_per_step": unit_cost,
            "steps": steps, "planned_partial_counted_ops": counted_ops,
            "relative_proxy_budget_gap": abs(counted_ops - target) / target,
            "hit_step_cap": steps == step_cap,
        }
    return {"target_partial_counted_ops": target, "arms": result,
            "proxy_budget_within_10pct": all(
                v["relative_proxy_budget_gap"] <= .10 for v in result.values()),
            "true_compute_matched": False, "flops_coverage_complete": False}


def run_pilot(*, seeds=(20261025, 20261026, 20261027),
              reference_steps=12, max_steps=120):
    if (not isinstance(seeds, (tuple, list)) or len(seeds) < 3
            or len(set(seeds)) != len(seeds)
            or any(type(s) is not int for s in seeds)):
        raise ValueError("at least 3 distinct integer seeds required")
    torch.set_num_threads(1)
    chosen = choose_widths()
    widths = {name: v["width"] for name, v in chosen["selected"].items()}
    audit = compute_audit(widths=tuple(sorted(set(widths.values()))),
                          contexts=(20,), repeats=3, batch_size=16)
    costs = {}
    for row in audit["results"]:
        if row["width"] == widths[row["architecture"]]:
            name = row["architecture"]
            costs[name] = row["train_profiler"]["accounted_flops_lower_bound"]
    plan = allocate_steps(costs, reference_steps=reference_steps,
                          step_cap=max_steps)
    train = get_split("train")
    dev = get_split("development")
    xtrain = torch.as_tensor(previous_codes(train), dtype=torch.float64)
    ytrain = torch.as_tensor(train, dtype=torch.float64)
    xdev = torch.as_tensor(previous_codes(dev), dtype=torch.float64)
    ydev = torch.as_tensor(dev, dtype=torch.float64)
    max_batches = max(row["steps"] for row in plan["arms"].values())
    records = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        common_batches = [rng.integers(0, len(train), size=16)
                          for _ in range(max_batches)]
        for name, factory in ARMS.items():
            torch.manual_seed(seed)
            model = factory(width=widths[name], length=20)
            optimizer = torch.optim.AdamW(model.parameters(), lr=.003,
                                          weight_decay=.001)
            model.train()
            steps = plan["arms"][name]["steps"]
            start = time.perf_counter()
            for ids in common_batches[:steps]:
                optimizer.zero_grad(set_to_none=True)
                loss = model.nll(xtrain[ids], ytrain[ids])
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite synthetic train loss")
                loss.backward()
                gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
                if not bool(torch.isfinite(gn)):
                    raise ArithmeticError("nonfinite gradient")
                optimizer.step()
            elapsed = time.perf_counter() - start
            model.eval()
            with torch.no_grad():
                dev_nll = float(model.nll(xdev, ydev))
                train_nll = float(model.nll(xtrain, ytrain))
            if not np.isfinite(dev_nll) or not np.isfinite(train_nll):
                raise ArithmeticError("nonfinite synthetic evaluation")
            records.append({
                "seed": seed, "architecture": name,
                "width": widths[name], "steps": steps,
                "parameter_count": sum(p.numel() for p in model.parameters()),
                "train_cpu_seconds": elapsed,
                "train_nll": train_nll,
                "development_nll": dev_nll,
                "planned_partial_counted_ops": plan["arms"][name][
                    "planned_partial_counted_ops"]})
    return {
        "experiment": "trame_a3c_proxy_budget_synthetic_pilot_v0.1",
        "data_origin": "ARTIFICIAL_TRAIN_AND_DEVELOPMENT",
        "reserved_synthetic_test_opened": False,
        "financial_holdout_opened": False,
        "same_common_batch_prefix_per_seed": True,
        "unequal_steps_across_arms": True,
        "tuning_compute_equalized": False,
        "true_compute_matched": False,
        "flops_coverage_complete": False,
        "not_independent_financial_validation": True,
        "cost_calibration": {
            "method": "torch.profiler partial counted ops in one forward+backward",
            "batch_size": 16, "context_tokens": 20,
            "dtype": "torch.float64", "cpu_threads": 1,
            "widths": widths, "hardware_specific": True,
        },
        "budget_plan": plan, "seed_count": len(seeds),
        "results": records,
        "torch_version": torch.__version__,
        "python_version": platform.python_version(),
        "git_sha": os.environ.get("GITHUB_SHA", "not recorded outside CI"),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Synthetic A3c.4 pilot, no markets")
    ap.add_argument("--reference-steps", type=int, default=12)
    ap.add_argument("--max-steps", type=int, default=120)
    ap.add_argument("--seeds", type=int, nargs="+",
                    default=[20261025, 20261026, 20261027])
    args = ap.parse_args(argv)
    print(json.dumps(run_pilot(reference_steps=args.reference_steps,
                               max_steps=args.max_steps,
                               seeds=args.seeds), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
