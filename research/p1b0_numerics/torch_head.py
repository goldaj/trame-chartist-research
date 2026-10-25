"""Differentiable P1-B0 conditional distribution (research, no trained model).

PyTorch tensor implementation independently cross-checked against the
existing SciPy Head. All arithmetic MUST use float64 in this preflight.
The 4096-core normalizer is deliberate; no tail clipping or market data.
"""
import math

import torch

LEFT, RIGHT = -2048, 2047
CORRECTION_BOUND = 4.0


def log_interval_mass(k, mu, sigma):
    """Log probability of rounded Gaussian cell k in both extreme tails."""
    low = (k - .5 - mu) / sigma
    high = (k + .5 - mu) / sigma
    if bool(torch.any(low >= high)):
        raise ArithmeticError("floating precision cannot resolve cell")
    positive = low >= 0
    big = torch.where(positive, torch.special.log_ndtr(-low),
                      torch.special.log_ndtr(high))
    small = torch.where(positive, torch.special.log_ndtr(-high),
                        torch.special.log_ndtr(low))
    with torch.no_grad():
        if bool(torch.any(small > big)):
            raise ArithmeticError("probability endpoints reversed")
    return big + torch.log(-torch.expm1(small - big))


def bounds_transform(g_mu, g_sigma, *, S=64.0):
    """Candidate 0.2: mu=M*tanh(raw/M), sigma=.25+(S-.25)*sigmoid(raw).

    Saturation is possible by design: measure it rather than claim that
    gradients remain healthy everywhere.
    """
    if S not in (64.0, 256.0):
        raise ValueError("S must be 64 or 256")
    mu = 256.0 * torch.tanh(g_mu / 256.0)
    sigma = .25 + (S - .25) * torch.sigmoid(g_sigma)
    return mu, sigma


def nll(target, mu, sigma, raw_corrections=None, *, S=64.0):
    """Return (-log p(target), log Z) preserving mu/sigma autograd."""
    if mu.dtype != torch.float64 or sigma.dtype != torch.float64:
        raise TypeError("numerical qualification requires torch.float64")
    if not (torch.isfinite(mu).all() and torch.isfinite(sigma).all()):
        raise ValueError("parameters must be finite")
    if not (-256 <= float(mu.detach()) <= 256 and .25 <= float(sigma.detach()) <= S):
        raise ValueError("physical parameters outside declared bounds")
    if type(target) is not int:
        raise TypeError("target must be an exact integer")
    if raw_corrections is None:
        raw = torch.zeros(4096, dtype=torch.float64, device=mu.device)
    else:
        raw = raw_corrections
        if raw.shape != (4096,) or raw.dtype != torch.float64 or not bool(torch.isfinite(raw).all()):
            raise ValueError("4096 finite float64 correction logits required")
    grid = torch.arange(LEFT, RIGHT + 1, dtype=torch.float64, device=mu.device)
    central = log_interval_mass(grid, mu, sigma)
    corr = CORRECTION_BOUND * torch.tanh(raw / CORRECTION_BOUND)
    left = torch.special.log_ndtr((LEFT - .5 - mu) / sigma)
    right = torch.special.log_ndtr(-(RIGHT + .5 - mu) / sigma)
    logz = torch.logsumexp(torch.cat((central + corr, left.reshape(1), right.reshape(1))), dim=0)
    target_logq = log_interval_mass(torch.tensor(float(target), dtype=torch.float64,device=mu.device), mu, sigma)
    if LEFT <= target <= RIGHT:
        target_logq = target_logq + corr[target - LEFT]
    return logz - target_logq, logz


def logit_for_sigma(sigma, S=64.0):
    """Inverse sigmoid at interior physical sigma (for reproducible init)."""
    if not (.25 < sigma < S):
        raise ValueError("saturated boundary has no finite inverse")
    odds = (sigma-.25)/(S-sigma)
    return math.log(odds)
