"""S1.3: depth/width scalable versions of the three existing causal controls.

Not a production forecasting model. Float64, common rounded Gaussian BASE head.
The 1-layer legacy architecture intentionally follows MiniTRAME's forward path.
"""
from __future__ import annotations

import torch
from torch import nn

from research.architecture_comparison.models import (
    CausalGaussianModel, CausalGQABlock, RMSNorm,
)
from research.p1b0_numerics.torch_head import (
    bounds_transform, log_interval_mass, logit_for_sigma,
)


class ScaledLegacyTransformer(nn.Module):
    """Causal masked TransformerEncoder 1/2/4 layers, GELU/LayerNorm."""
    def __init__(self, *, width=16, depth=1, length=20):
        super().__init__()
        validate_dimensions(width, depth, length)
        self.length = length
        self.input_proj = nn.Linear(1, width, dtype=torch.float64)
        self.position = nn.Embedding(length, width, dtype=torch.float64)
        layer = nn.TransformerEncoderLayer(
            d_model=width, nhead=2, dim_feedforward=width * 2,
            dropout=0.0, batch_first=True, activation="gelu",
            norm_first=True, dtype=torch.float64,
        )
        self.backbone = nn.TransformerEncoder(
            layer, num_layers=depth, enable_nested_tensor=False,
        )
        self.output = nn.Linear(width, 2, dtype=torch.float64)
        with torch.no_grad():
            self.output.weight.mul_(0.01)
            self.output.bias[0] = 0.0
            self.output.bias[1] = logit_for_sigma(3.0)

    def forward(self, previous_codes):
        if (previous_codes.ndim != 2 or
                not 1 <= previous_codes.shape[1] <= self.length):
            raise ValueError("context length outside configured limits")
        if previous_codes.dtype != torch.float64:
            raise TypeError("float64 input required")
        if not bool(torch.isfinite(previous_codes).all()):
            raise ValueError("nonfinite input")
        t = previous_codes.shape[1]
        positions = torch.arange(t, device=previous_codes.device)
        x = (self.input_proj((previous_codes / 8.0).unsqueeze(-1))
             + self.position(positions)[None, :, :])
        causal_mask = torch.triu(
            torch.ones((t, t), device=previous_codes.device, dtype=torch.bool),
            diagonal=1,
        )
        hidden = self.backbone(x, mask=causal_mask)
        out = self.output(hidden)
        return bounds_transform(out[..., 0], out[..., 1], S=64.0)

    def nll(self, previous_codes, target_codes):
        mu, sigma = self(previous_codes)
        if target_codes.shape != mu.shape or target_codes.dtype != torch.float64:
            raise ValueError("float64 targets must match context shape")
        return -log_interval_mass(target_codes, mu, sigma).mean()


class ScaledModernGPT(CausalGaussianModel):
    """Decoder-only pre-norm RMSNorm/GQA/RoPE/SwiGLU with 1/2/4 blocks."""
    def __init__(self, *, width=16, depth=1, length=20):
        validate_dimensions(width, depth, length)
        super().__init__(width=width, length=length)
        self.blocks = nn.ModuleList(CausalGQABlock(width) for _ in range(depth))
        self.last_norm = RMSNorm(width)

    def encode(self, x):
        for block in self.blocks:
            x = block(x)
        return self.last_norm(x)


class ScaledGRU(CausalGaussianModel):
    """Recurrent multi-layer classical control, not Mamba."""
    def __init__(self, *, width=16, depth=1, length=20):
        validate_dimensions(width, depth, length)
        super().__init__(width=width, length=length)
        self.gru = nn.GRU(
            input_size=width, hidden_size=width, num_layers=depth,
            batch_first=True, dtype=torch.float64,
        )

    def encode(self, x):
        return self.gru(x)[0]


FAMILIES = {
    "legacy_causal_transformer": ScaledLegacyTransformer,
    "modern_gpt_style_mini": ScaledModernGPT,
    "recurrent_gru_control": ScaledGRU,
}
TARGET_PARAMETERS = (2400, 37000, 148000, 592000, 2360000)
DEPTHS = (1, 2, 4)


def validate_dimensions(width, depth, length):
    if (type(width) is not int or width < 8 or width % 4 != 0
            or type(depth) is not int or depth not in DEPTHS
            or type(length) is not int or not 1 <= length <= 128):
        raise ValueError("width divisible by 4 >=8, depth 1/2/4, length 1..128")


def expected_parameters(family, *, width, depth, length=20):
    """Formula for actual current PyTorch modules; checked against numel in tests."""
    validate_dimensions(width, depth, length)
    if family == "legacy_causal_transformer":
        return depth * (8 * width * width + 11 * width) + (length + 4) * width + 2
    if family == "modern_gpt_style_mini":
        return depth * (9 * width * width + 2 * width) + 5 * width + 2
    if family == "recurrent_gru_control":
        return depth * (6 * width * width + 6 * width) + 4 * width + 2
    raise ValueError("unknown family")


def capacity_grid(*, targets=TARGET_PARAMETERS, depths=DEPTHS,
                  families=tuple(FAMILIES), length=20, width_max=704):
    """Select width nearest each target, no promise of equality or compute matching."""
    if (not targets or not depths or not families
            or any(type(v) is not int or v < 100 for v in targets)
            or any(d not in DEPTHS for d in depths)
            or any(f not in FAMILIES for f in families)
            or type(width_max) is not int or width_max < 8
            or width_max % 4):
        raise ValueError("invalid grid options")
    rows = []
    for family in families:
        for target in targets:
            for depth in depths:
                candidates = (
                    (w, expected_parameters(family, width=w, depth=depth,
                                             length=length))
                    for w in range(8, width_max + 1, 4)
                )
                width, count = min(
                    candidates, key=lambda row: (abs(row[1] - target), row[0])
                )
                rows.append({
                    "architecture": family, "target_parameters": target,
                    "depth": depth, "width": width, "parameter_count": count,
                    "relative_parameter_gap": abs(count - target) / target,
                    "within_10pct_target": abs(count - target) <= target * 0.10,
                    "compute_matched": False,
                })
    return rows
