"""Causality/shape contract for CPU hybrids and future official SSM blocks.

This checker does NOT claim a black-box proof of causality; it is one
adversarial perturbation test. It MUST be complemented by operator review
and real device-specific gradients for production-quality SSM kernels.
"""
from __future__ import annotations

import torch


def verify_sequence_backbone(backbone, x, *, atol=1e-10, rtol=1e-10):
    if x.ndim != 3 or x.shape[1] < 4 or not bool(torch.isfinite(x).all()):
        raise ValueError("finite batch x time x width tensor with >=4 tokens required")
    if type(atol) not in (int, float) or type(rtol) not in (int, float):
        raise ValueError("numeric tolerances required")
    if atol < 0 or rtol < 0:
        raise ValueError("nonnegative tolerances required")
    midpoint = x.shape[1] // 2
    moved = x.clone()
    moved[:, midpoint:] += 100.0
    was_training = backbone.training
    backbone.eval()
    try:
        with torch.no_grad():
            original = backbone(x)
            changed = backbone(moved)
    finally:
        backbone.train(was_training)
    if not (isinstance(original, torch.Tensor)
            and isinstance(changed, torch.Tensor)
            and original.shape == x.shape and changed.shape == x.shape
            and original.dtype == x.dtype and changed.dtype == x.dtype):
        raise ValueError("backbone violates same-shape/same-dtype sequence contract")
    if not (bool(torch.isfinite(original).all()) and bool(torch.isfinite(changed).all())):
        raise ValueError("nonfinite sequence backbone output")
    if not torch.allclose(original[:, :midpoint], changed[:, :midpoint],
                          atol=atol, rtol=rtol):
        raise ValueError("backbone may leak information from future tokens")
    return {"causal_prefix_perturbation_passed": True,
            "shape_preserved": True, "dtype_preserved": True,
            "tested_prefix_tokens": midpoint,
            "is_formal_causality_proof": False,
            "real_ssm_kernel_validated": False}
