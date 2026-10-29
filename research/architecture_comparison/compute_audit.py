"""A3c diagnostic: partial operator FLOPs and CPU timings on artificial train only.

Not FLOPs parity. torch.profiler with_flops counts a subset of operators
(matrix multiplications/convolutions); unaccounted ops are UNKNOWN, not free.
No historical market data, reserved test or development labels are loaded.
Artificial random-walk-like paths are created exclusively for cost timing.
"""
from __future__ import annotations

import argparse
import json
import platform
import statistics
import time

import numpy as np
import torch
from torch.profiler import ProfilerActivity, profile

from research.architecture_comparison.experiment import ARMS


SUPPORTED_WIDTHS = (8, 12, 16, 20, 24, 28, 32)
SUPPORTED_CONTEXTS = (8, 16, 20, 32, 64, 128)


def _unique_choices(values, allowed, field):
    if (not isinstance(values, (tuple, list)) or not values
            or any(type(v) is not int or v not in allowed for v in values)
            or len(values) != len(set(values))):
        raise ValueError(f"{field}: distinct values from {allowed} required")


def _profiler_summary(model, x, y, *, backward):
    model.zero_grad(set_to_none=True)
    with profile(activities=[ProfilerActivity.CPU],
                 with_flops=True, profile_memory=True) as recording:
        loss = model.nll(x, y)
        if backward:
            loss.backward()
    if not bool(torch.isfinite(loss)):
        raise ArithmeticError("nonfinite synthetic loss")
    events = recording.key_averages()
    rows = []
    for event in events:
        flops = int(event.flops or 0)
        if flops:
            rows.append({"operator": event.key, "count": int(event.count),
                         "accounted_flops": flops})
    # This number is NOT full-model FLOPs: many torch kernels have no counters.
    return {"accounted_flops_lower_bound": sum(row["accounted_flops"] for row in rows),
            "flop_accounted_operators": sorted(rows, key=lambda r: r["operator"]),
            "profiler_event_types": len(events),
            "event_max_reported_cpu_allocation_bytes": max(
                (max(0, int(e.cpu_memory_usage)) for e in events), default=0),
            "memory_is_process_peak": False,
            "flops_coverage_complete": False}


def compute_audit(*, widths=(8, 16), contexts=(8, 16, 20, 32, 64),
                  repeats=3, seed=20261025, batch_size=8):
    """Measure a compact, explicitly non-confirmatory synthetic CPU workload."""
    _unique_choices(widths, SUPPORTED_WIDTHS, "widths")
    _unique_choices(contexts, SUPPORTED_CONTEXTS, "contexts")
    if type(repeats) is not int or not 3 <= repeats <= 40:
        raise ValueError("repeats must be 3..40")
    if type(seed) is not int:
        raise ValueError("integer seed required")
    if type(batch_size) is not int or not 2 <= batch_size <= 16:
        raise ValueError("batch_size must be 2..16")
    torch.set_num_threads(1)
    # New, explicitly artificial cost-only workload. Never open any held-out
    # stream or use financial data. The prefix is identical for each context.
    rng = np.random.default_rng(seed)
    length = max(contexts)
    target = np.zeros((batch_size, length), dtype=np.int64)
    state = np.zeros(batch_size, dtype=np.int64)
    for t in range(length):
        state = np.floor(.75 * state + rng.normal(size=batch_size) * 3 + .5).astype(np.int64)
        target[:, t] = state
    prior = np.zeros_like(target)
    prior[:, 1:] = target[:, :-1]
    results = []
    for width in widths:
        for context in contexts:
            x = torch.as_tensor(prior[:, :context].copy(), dtype=torch.float64)
            y = torch.as_tensor(target[:, :context].copy(), dtype=torch.float64)
            for name, factory in ARMS.items():
                torch.manual_seed(seed)
                model = factory(width=width, length=context)
                model.eval()
                with torch.no_grad():
                    for _ in range(2):
                        model.nll(x, y)
                forward_ms = []
                with torch.no_grad():
                    for _ in range(repeats):
                        start = time.perf_counter()
                        loss = model.nll(x, y)
                        forward_ms.append((time.perf_counter() - start) * 1000)
                        if not bool(torch.isfinite(loss)):
                            raise ArithmeticError("nonfinite forward loss")
                model.train()
                for _ in range(2):
                    model.zero_grad(set_to_none=True)
                    model.nll(x, y).backward()
                train_step_ms = []
                for _ in range(repeats):
                    model.zero_grad(set_to_none=True)
                    start = time.perf_counter()
                    loss = model.nll(x, y)
                    loss.backward()
                    train_step_ms.append((time.perf_counter() - start) * 1000)
                    if not bool(torch.isfinite(loss)):
                        raise ArithmeticError("nonfinite training loss")
                model.eval()
                with torch.no_grad():
                    prof_fwd = _profiler_summary(model, x, y, backward=False)
                model.train()
                prof_train = _profiler_summary(model, x, y, backward=True)
                parameters = sum(p.numel() for p in model.parameters())
                results.append({
                    "architecture": name, "width": width, "context_tokens": context,
                    "batch_size": batch_size, "parameter_count": parameters,
                    "trainable_parameter_count": sum(p.numel() for p in model.parameters()
                                                      if p.requires_grad),
                    "forward_median_ms_unprofiled": statistics.median(forward_ms),
                    "train_step_median_ms_unprofiled": statistics.median(train_step_ms),
                    "forward_profiler": prof_fwd, "train_profiler": prof_train,
                    "same_inputs_across_architectures": True})
    return {
        "experiment": "TRAME_A3c_partial_compute_accounting_v0.1",
        "data_origin": "ARTIFICIAL_COST_ONLY",
        "train_only": False, "reserved_synthetic_test_opened": False,
        "cost_only_inputs_generated_from_seed": True,
        "financial_holdout_opened": False, "source_is_real_finance": False,
        "compute_matched": False, "flops_matched": False,
        "flops_coverage_complete": False,
        "flops_method": "torch.profiler with_flops=True, partial ops only; backward incomplete",
        "memory_method": "max positive profiler event, NOT process peak memory",
        "timing_method": "median CPU perf_counter, outside profiler, 2 warmups",
        "device": "cpu", "dtype": "float64", "threads": 1,
        "seed": seed, "repeats": repeats,
        "torch_version": torch.__version__, "python_version": platform.python_version(),
        "results": results}


def main(argv=None):
    parser = argparse.ArgumentParser(description="A3c synthetic cost audit, no markets")
    parser.add_argument("--widths", type=int, nargs="+", default=[8, 16])
    parser.add_argument("--contexts", type=int, nargs="+", default=[8, 16, 20])
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args(argv)
    print(json.dumps(compute_audit(widths=args.widths,
                                   contexts=args.contexts, repeats=args.repeats),
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
