"""P1-B0 0.2 numeric probability head, experimental and untrained.

The published 2026-10-16 candidate specifies a rounded Gaussian q(k) on
all integers, optional bounded central correction w(k), and Z normalization.
No market data, network, model weights or optimizer enter this module.
"""
from dataclasses import dataclass
import math
from typing import Optional

import numpy as np
from scipy.special import log_ndtr, logsumexp
from scipy.stats import truncnorm

LEFT, RIGHT = -2048, 2047
GRID = np.arange(LEFT, RIGHT + 1, dtype=np.int64)
CORE_N = 4096
A = 4.0


def _logdiffexp(larger, smaller):
    """Log(exp(larger)-exp(smaller)), avoiding subtraction of near equals."""
    larger, smaller = np.asarray(larger), np.asarray(smaller)
    if np.any(smaller > larger + 1e-12):
        raise ArithmeticError("probability endpoints reversed")
    with np.errstate(divide="ignore", under="ignore", invalid="ignore"):
        return larger + np.log(-np.expm1(np.minimum(0.0, smaller - larger)))


def log_rounded_normal_mass(k, mu, sigma):
    """Stable log Pr[k-.5 <= X < k+.5], for X~N(mu,sigma**2)."""
    k = np.asarray(k, dtype=np.float64)
    zlo = (k - 0.5 - mu) / sigma
    zhi = (k + 0.5 - mu) / sigma
    if np.any(~np.isfinite(zlo)) or np.any(~np.isfinite(zhi)):
        raise ValueError("standardized boundaries must be finite")
    if np.any(zlo >= zhi):
        raise ArithmeticError("float64 cannot resolve this rounding cell")
    positive = zlo >= 0
    # Lower tail: difference of small CDFs. Upper tail: difference of
    # small survival probabilities. Neither ever computes 1 - CDF.
    first = np.where(positive, log_ndtr(-zlo), log_ndtr(zhi))
    second = np.where(positive, log_ndtr(-zhi), log_ndtr(zlo))
    result = _logdiffexp(first, second)
    if np.any(np.isnan(result)):
        raise ArithmeticError("log interval mass became NaN")
    return float(result) if result.ndim == 0 else result


def hierarchical_logits(coarse, bit_logits):
    """Construct raw g_k from 512 coarse values and three (0,1) bit pairs."""
    coarse = np.asarray(coarse, dtype=np.float64)
    bits = np.asarray(bit_logits, dtype=np.float64)
    if coarse.shape != (512,) or bits.shape != (3, 2):
        raise ValueError("HIER needs 512 coarse and 3 x 2 bit logits")
    if not np.isfinite(coarse).all() or not np.isfinite(bits).all():
        raise ValueError("non-finite HIER logits")
    q = GRID // 8 + 256
    rem = GRID % 8  # Euclidean mod handles negative k.
    return coarse[q] + bits[0, (rem >> 2) & 1] + bits[1, (rem >> 1) & 1] + bits[2, rem & 1]


@dataclass
class Head:
    """Numerically evaluable single-state P1-B0 head, not a neural network.

    Raw central logits are transformed as a=A*tanh(g/A), preserving the
    candidate's bounded corrections. No trainable mu/sigma gradients yet.
    """
    mu: float = 0.0
    sigma: float = 8.0
    logits: Optional[np.ndarray] = None
    max_sigma: float = 256.0

    def __post_init__(self):
        if not math.isfinite(self.mu) or abs(self.mu) > 256:
            raise ValueError("mu outside the declared P1-B0 bound")
        if not math.isfinite(self.sigma) or not (0.25 <= self.sigma <= self.max_sigma):
            raise ValueError("sigma outside the declared P1-B0 bound")
        if self.max_sigma not in (64.0, 256.0):
            raise ValueError("only preregistered S=64 or S=256")
        self.raw = (np.zeros(CORE_N, dtype=np.float64) if self.logits is None
                    else np.asarray(self.logits, dtype=np.float64).copy())
        if self.raw.shape != (CORE_N,) or not np.isfinite(self.raw).all():
            raise ValueError("central logits must be 4096 finite numbers")
        self.correction = A * np.tanh(self.raw / A)
        self.log_core_q = log_rounded_normal_mass(GRID, self.mu, self.sigma)
        self.log_left_q = float(log_ndtr((LEFT - .5 - self.mu) / self.sigma))
        self.log_right_q = float(log_ndtr(-(RIGHT + .5 - self.mu) / self.sigma))
        self.log_z = float(logsumexp(np.r_[self.log_left_q, self.log_right_q,
                                            self.log_core_q + self.correction]))
        if not math.isfinite(self.log_z):
            raise ArithmeticError("normalizer not finite")

    def log_prob(self, k):
        if type(k) not in (int, np.int64, np.int32):
            raise TypeError("k must be an integer")
        base = log_rounded_normal_mass(k, self.mu, self.sigma)
        if LEFT <= k <= RIGHT:
            base += float(self.correction[k - LEFT])
        return base - self.log_z

    def negative_log_likelihood(self, k):
        return -self.log_prob(k)

    def grad_logits(self, target):
        """Exact analytic gradient of -log p(target) w.r.t. raw central g.

        This validates only correction logits; mu/sigma and model gradients
        are not supplied. The normalizer includes both unbounded tails.
        """
        probs = np.exp(self.log_core_q + self.correction - self.log_z)
        if LEFT <= target <= RIGHT:
            probs[target - LEFT] -= 1.0
        return probs * (1.0 - np.tanh(self.raw / A)**2)

    def mass_audit(self):
        left = math.exp(self.log_left_q - self.log_z)
        right = math.exp(self.log_right_q - self.log_z)
        core = float(np.exp(self.log_core_q + self.correction - self.log_z).sum())
        return {"core": core, "left": left, "right": right,
                "sum": core + left + right, "log_z": self.log_z,
                "left_tail_underflow": left == 0.0,
                "right_tail_underflow": right == 0.0}

    def sample(self, rng):
        """Sample core/tails when their masses are representable in float64.

        The mathematical distribution has infinite support but a tiny tail
        can underflow to zero in this sampler. log_prob stays finite in
        the tails. Do not use this sampler as a tail-calibration proof.
        """
        probs = np.exp(np.r_[self.log_core_q + self.correction,
                             self.log_left_q, self.log_right_q] - self.log_z)
        probs /= probs.sum()  # remove last few float64 ULPs for choice
        ix = int(rng.choice(CORE_N + 2, p=probs))
        if ix < CORE_N:
            return LEFT + ix
        cutoff = LEFT - .5 if ix == CORE_N else RIGHT + .5
        a, b = ((-np.inf, (cutoff - self.mu)/self.sigma) if ix == CORE_N
                else ((cutoff - self.mu)/self.sigma, np.inf))
        draw = float(truncnorm.rvs(a, b, loc=self.mu,
                                  scale=self.sigma, random_state=rng))
        result = math.floor(draw + .5)
        if ix == CORE_N and result >= LEFT or ix == CORE_N + 1 and result <= RIGHT:
            raise ArithmeticError("truncated tail sampled into the core")
        return result


def decode_lattice_price(anchor, scale, cumulative_k):
    """Convert a simulated integer sum to price, with overflow detection."""
    if not math.isfinite(anchor) or anchor <= 0 or not math.isfinite(scale) or scale <= 0:
        raise ValueError("anchor and scale must be positive finite")
    if type(cumulative_k) is not int:
        raise TypeError("cumulative state must be exact integer")
    log_price = math.log(anchor) + (scale / 8.0) * cumulative_k
    if not (-744.0 < log_price < math.log(np.finfo(float).max)):
        raise OverflowError("lattice price outside safe float64 exp range")
    return math.exp(log_price)
