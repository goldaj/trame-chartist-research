"""Two CPU miniature causal challengers; NOT a pretrained modern LLM or Mamba.

Exact same rounded-Gaussian BASE output family as MiniTRAME. The GPT-style
arm tests RMSNorm, RoPE, grouped-query attention, SwiGLU and decoder-only
causal masking; GRU is a classical recurrent control, NOT an SSM.
"""
import torch
from torch import nn
from torch.nn import functional as F

from research.p1b0_numerics.torch_head import bounds_transform, log_interval_mass, logit_for_sigma


class RMSNorm(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(width, dtype=torch.float64))

    def forward(self, x):
        return x * torch.rsqrt(x.square().mean(dim=-1, keepdim=True) + 1e-8) * self.weight


def rotate_pairs(x, positions):
    """Apply deterministic RoPE to [B, heads, time, head_dim]."""
    dim = x.shape[-1]
    if dim % 2:
        raise ValueError('RoPE head dimension must be even')
    freqs = 1.0 / (10000.0 ** (torch.arange(0, dim, 2, dtype=x.dtype, device=x.device) / dim))
    theta = positions.to(dtype=x.dtype)[:, None] * freqs[None, :]
    sine = theta.sin()[None, None, :, :]
    cosine = theta.cos()[None, None, :, :]
    a, b = x[..., 0::2], x[..., 1::2]
    return torch.stack((a * cosine - b * sine, a * sine + b * cosine), dim=-1).flatten(-2)


class CausalGQABlock(nn.Module):
    """Small GPT-style pre-norm block; 2 query heads, one KV head."""
    def __init__(self, width):
        super().__init__()
        if width % 4:
            raise ValueError('width must be divisible by 4')
        self.width = width
        self.head_dim = width // 2
        self.att_norm = RMSNorm(width)
        self.q_proj = nn.Linear(width, width, bias=False, dtype=torch.float64)
        self.k_proj = nn.Linear(width, self.head_dim, bias=False, dtype=torch.float64)
        self.v_proj = nn.Linear(width, self.head_dim, bias=False, dtype=torch.float64)
        self.att_out = nn.Linear(width, width, bias=False, dtype=torch.float64)
        self.ff_norm = RMSNorm(width)
        self.ff_in = nn.Linear(width, width * 4, bias=False, dtype=torch.float64)
        self.ff_out = nn.Linear(width * 2, width, bias=False, dtype=torch.float64)

    def forward(self, x):
        batch, length, width = x.shape
        h = self.att_norm(x)
        q = self.q_proj(h).reshape(batch, length, 2, self.head_dim).transpose(1, 2)
        k = self.k_proj(h).reshape(batch, length, 1, self.head_dim).transpose(1, 2)
        v = self.v_proj(h).reshape(batch, length, 1, self.head_dim).transpose(1, 2)
        pos = torch.arange(length, device=x.device)
        q = rotate_pairs(q, pos)
        k = rotate_pairs(k, pos)
        k = k.expand(-1, 2, -1, -1)
        v = v.expand(-1, 2, -1, -1)
        attention = F.scaled_dot_product_attention(q, k, v, is_causal=True, dropout_p=0.0)
        x = x + self.att_out(attention.transpose(1, 2).reshape(batch, length, width))
        a, b = self.ff_in(self.ff_norm(x)).chunk(2, dim=-1)
        return x + self.ff_out(F.silu(a) * b)


class CausalGaussianModel(nn.Module):
    """Common likelihood and input check for competing causal backbones."""
    def __init__(self, width=16, length=20):
        super().__init__()
        if type(width) is not int or width < 4 or width % 4 or type(length) is not int or not 1 <= length <= 128:
            raise ValueError('width multiple of 4 >=4 and length 1..128 required')
        self.length = length
        self.input_proj = nn.Linear(1, width, dtype=torch.float64)
        self.output = nn.Linear(width, 2, dtype=torch.float64)
        with torch.no_grad():
            self.output.weight.mul_(.01)
            self.output.bias[0] = 0.0
            self.output.bias[1] = logit_for_sigma(3.0)

    def _validate(self, prior_codes):
        if prior_codes.ndim != 2 or not 1 <= prior_codes.shape[1] <= self.length:
            raise ValueError('context outside configured model limit')
        if prior_codes.dtype != torch.float64 or not bool(torch.isfinite(prior_codes).all()):
            raise ValueError('finite float64 contexts required')

    def forward(self, prior_codes):
        self._validate(prior_codes)
        x = self.input_proj((prior_codes / 8.0).unsqueeze(-1))
        hidden = self.encode(x)
        raw = self.output(hidden)
        return bounds_transform(raw[..., 0], raw[..., 1], S=64.0)

    def nll(self, prior_codes, actual_codes):
        if prior_codes.shape != actual_codes.shape or actual_codes.dtype != torch.float64:
            raise ValueError('matching float64 targets required')
        mu, sigma = self(prior_codes)
        return -log_interval_mass(actual_codes, mu, sigma).mean()


class ModernGPTMini(CausalGaussianModel):
    """Tiny modernized decoder-only Transformer; randomly initialized."""
    def __init__(self, width=16, length=20):
        super().__init__(width, length)
        self.block = CausalGQABlock(width)
        self.last_norm = RMSNorm(width)

    def encode(self, x):
        return self.last_norm(self.block(x))


class GRUMini(CausalGaussianModel):
    """Classical recurrent control: not Mamba, xLSTM or a modern LLM."""
    def __init__(self, width=16, length=20):
        super().__init__(width, length)
        self.gru = nn.GRU(input_size=width, hidden_size=width, batch_first=True, dtype=torch.float64)

    def encode(self, x):
        return self.gru(x)[0]
