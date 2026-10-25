"""Attention + GRU CPU hybrid control, NOT Mamba or selective SSM.

This exploratory arm shares TRAME's causal input and Gaussian BASE head.
It is a baseline for determining whether combining attention and a classical
recurrent unit warrants a proper attention+SSM experiment on real GPU.
"""
from __future__ import annotations

import torch
from torch import nn

from research.architecture_comparison.models import (
    CausalGaussianModel, CausalGQABlock, RMSNorm,
)


class AttentionGRUHybrid(CausalGaussianModel):
    """One causal GQA attention block followed by a gated GRU residual."""

    def __init__(self, *, width=16, length=20):
        super().__init__(width=width, length=length)
        self.attention = CausalGQABlock(width)
        self.gru = nn.GRU(input_size=width, hidden_size=width,
                          batch_first=True, dtype=torch.float64)
        self.recurrent_gate_logit = nn.Parameter(torch.tensor(
            0.0, dtype=torch.float64))
        self.final_norm = RMSNorm(width)

    def encode(self, x):
        attended = self.attention(x)
        recurrent, _ = self.gru(attended)
        gate = torch.sigmoid(self.recurrent_gate_logit)
        return self.final_norm(attended + gate * recurrent)
