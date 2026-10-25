"""Run an explicit REAL-GPU smoke for official Mamba-2 and/or Mamba-3.

Not run in ordinary CPU CI. The process raises on unavailable CUDA/package;
never creates simulated GPU-success JSON. No BTC data is needed.
"""
from __future__ import annotations

import argparse
import json
import math
import time

import torch

from research.mamba_candidates.official_adapter import (
    CANDIDATES, gpu_environment, new_candidate, require_gpu,
)


def gpu_smoke(*, variant, width=64, context=64, batch=2, seed=20261025):
    if variant not in CANDIDATES:
        raise ValueError("unknown official Mamba variant")
    if type(batch) is not int or not 1 <= batch <= 8:
        raise ValueError("batch 1..8 required")
    if type(seed) is not int:
        raise ValueError("seed integer required")
    require_gpu()
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    model = new_candidate(variant, width=width, length=context)
    x = torch.randn((batch, context), dtype=torch.float64, device="cuda:0") * 3
    targets = torch.zeros_like(x)
    mid = context // 2
    other = x.clone()
    other[:, mid:] += 30.0
    model.eval()
    with torch.no_grad():
        before = model(x)
        after = model(other)
    for a, b in zip(before, after):
        torch.testing.assert_close(a[:, :mid], b[:, :mid], atol=5e-3, rtol=5e-3)
    model.train()
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    loss = model.nll(x, targets)
    if not bool(torch.isfinite(loss)):
        raise ArithmeticError("nonfinite GPU Mamba NLL")
    loss.backward()
    if not all(p.grad is not None and bool(torch.isfinite(p.grad).all())
               for p in model.parameters() if p.requires_grad):
        raise ArithmeticError("nonfinite or missing GPU gradients")
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - t0
    output = {
        "candidate": variant, "official_mamba_backend_actually_executed": True,
        "cuda_verified": True, "seed": seed, "width": width,
        "context_tokens": context, "batch": batch,
        "parameter_count": sum(p.numel() for p in model.parameters()),
        "max_cuda_allocated_bytes": torch.cuda.max_memory_allocated(),
        "one_train_step_seconds": elapsed,
        "loss": float(loss.detach().cpu()),
        "causal_prefix_test_passed": True,
        "finite_backward_passed": True,
        "train_and_development_used": False,
        "source_is_real_market": False,
        "reserved_synthetic_test_opened": False,
        "compute_matched": False,
        "environment": gpu_environment(),
    }
    if not math.isfinite(output["loss"]):
        raise ArithmeticError("nonfinite detached loss")
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description="Real GPU only, official mamba smoke")
    parser.add_argument("--model", choices=(*CANDIDATES, "all"), default="all")
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--context", type=int, default=64)
    parser.add_argument("--batch", type=int, default=2)
    args = parser.parse_args(argv)
    candidates = CANDIDATES if args.model == "all" else (args.model,)
    result = [gpu_smoke(variant=variant, width=args.width,
                        context=args.context, batch=args.batch)
              for variant in candidates]
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
