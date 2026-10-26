"""S2 continuous inputs: matched-backbone Huber vs Huber+direction BCE arms.

The BTC future target is NOT an input. No pretrained weights, no action,
no exchange usage, no retrieval of price files from this module.
"""
from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

from research.architecture_comparison.models import CausalGQABlock, RMSNorm


class ContinuousDirectionModel(nn.Module):
    def __init__(self, *, width=16, depth=1, context=20, mode="regression"):
        super().__init__()
        if (type(width) is not int or width < 8 or width % 4 != 0
                or type(depth) is not int or depth not in (1, 2)
                or type(context) is not int or not 1 <= context <= 20
                or mode not in ("regression", "joint")):
            raise ValueError("width multiple of 4, depth 1/2, context 1..20, valid mode")
        self.context = context
        self.mode = mode
        self.input_proj = nn.Linear(1, width, dtype=torch.float64)
        self.blocks = nn.ModuleList(CausalGQABlock(width) for _ in range(depth))
        self.last_norm = RMSNorm(width)
        self.return_head = nn.Linear(width, 1, dtype=torch.float64)
        self.direction_head = nn.Linear(width, 1, dtype=torch.float64)
        with torch.no_grad():
            self.return_head.weight.mul_(0.01)
            self.return_head.bias.zero_()
            self.direction_head.weight.mul_(0.01)
            self.direction_head.bias.zero_()

    def forward(self, past_return_normalized):
        x = past_return_normalized
        if (x.ndim != 2 or not 1 <= x.shape[1] <= self.context
                or x.dtype != torch.float64
                or not bool(torch.isfinite(x).all())):
            raise ValueError("finite float64 context expected")
        hidden = self.input_proj(x.unsqueeze(-1))
        for block in self.blocks:
            hidden = block(hidden)
        final = self.last_norm(hidden[:, -1])
        return (
            self.return_head(final).squeeze(-1),
            self.direction_head(final).squeeze(-1),
        )

    def loss(self, x, y_normalized):
        if (y_normalized.ndim != 1 or y_normalized.shape[0] != x.shape[0]
                or y_normalized.dtype != torch.float64
                or not bool(torch.isfinite(y_normalized).all())):
            raise ValueError("finite normalized scalar returns required")
        pred, logit = self(x)
        huber = F.smooth_l1_loss(pred, y_normalized, beta=1.0)
        if self.mode == "regression":
            return huber
        mask = y_normalized != 0.0
        if not bool(mask.any()):
            # No directional label exists on an all-flat minibatch.
            return huber
        bce = F.binary_cross_entropy_with_logits(
            logit[mask], (y_normalized[mask] > 0).to(dtype=torch.float64))
        return huber + 0.5 * bce


def forecast_prices(model, normalized_histories, anchors, *, scale_bps):
    """S2 preregistered direction-and-magnitude reconciliation."""
    import numpy as np

    if (not isinstance(scale_bps, float) or not 0 < scale_bps < float("inf")):
        raise ValueError("finite positive train-only scale required")
    a=np.asarray(anchors,dtype=float)
    if a.ndim!=1 or np.any(~np.isfinite(a)) or np.any(a<=0):
        raise ValueError("positive anchor prices required")
    model.eval()
    with torch.no_grad():
        predicted_norm, logits = model(normalized_histories)
    mu_bps = predicted_norm.cpu().numpy() * scale_bps
    p_up = torch.sigmoid(logits).cpu().numpy()
    if model.mode == "regression":
        reconciled_bps = mu_bps
    else:
        classification_sign = np.where(p_up >= 0.5, 1.0, -1.0)
        reconciled_bps = classification_sign * np.abs(mu_bps)
    if not np.all(np.isfinite(reconciled_bps)):
        raise ArithmeticError("nonfinite predictions")
    if len(reconciled_bps) != len(a):
        raise ValueError("context/anchor count mismatch")
    # Reject extreme outputs instead of silently clipping them. Clipping
    # would fabricate a different forecast and bias MAE/directional scores.
    if np.any(np.abs(reconciled_bps) > 100000):
        raise ArithmeticError("implausible predicted log-return: do not clip forecasts")
    forecast = a * np.exp(reconciled_bps / 10000.0)
    if not np.isfinite(forecast).all() or np.any(forecast <= 0):
        raise ArithmeticError("forecast overflow/underflow")
    return forecast, p_up, mu_bps
