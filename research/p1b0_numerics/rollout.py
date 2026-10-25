"""Causal 20-step P1-B0 generative smoke test and native-price CRPS.

The head_factory receives ONLY (step, previous cumulative integer code).
It must not receive the realized future. Models remain untrained.
"""
from dataclasses import dataclass
import math

import numpy as np

try:
    from .head import Head, decode_lattice_price
except ImportError:
    from head import Head, decode_lattice_price


@dataclass(frozen=True)
class Path:
    codes: tuple
    cumulative_codes: tuple
    prices: tuple


def rollout(anchor, scale, head_factory, rng, *, horizon=20):
    if type(horizon) is not int or not (1 <= horizon <= 20):
        raise ValueError('horizon must be 1..20 per P1-B0 0.2')
    n = 0
    codes, states, prices = [], [], []
    for h in range(1, horizon + 1):
        head = head_factory(h, n)
        if not isinstance(head, Head):
            raise TypeError('head_factory must provide a P1-B0 Head')
        k = head.sample(rng)
        n += k
        codes.append(k)
        states.append(n)
        prices.append(decode_lattice_price(anchor, scale, n))
    return Path(tuple(codes), tuple(states), tuple(prices))


def teacher_forced_log_likelihood(true_codes, head_factory):
    """Score explicitly provided codes, with ONLY true prior codes as inputs."""
    if not (1 <= len(true_codes) <= 20):
        raise ValueError('target sequence must be 1..20 codes')
    n, score = 0, 0.0
    for h, k in enumerate(true_codes, 1):
        if type(k) is not int:
            raise TypeError('target codes must be exact ints')
        head = head_factory(h, n)
        score += head.log_prob(k)
        n += k
    return score


def empirical_crps(forecast_prices, true_price):
    """CRPS of the *empirical* forecast distribution (not unbiased law CRPS).

    CRPS = E|X-y| - 0.5 E|X-X'|. Sorting yields O(n log n) pairs.
    A finite ensemble is itself a discrete forecast; this score is proper
    for that empirical distribution, not an unbiased population estimator.
    """
    x = np.asarray(forecast_prices, dtype=np.float64)
    if x.ndim != 1 or len(x) < 1 or not np.isfinite(x).all() or np.any(x <= 0):
        raise ValueError('nonempty vector of finite positive forecast prices required')
    if not math.isfinite(true_price) or true_price <= 0:
        raise ValueError('observed price must be finite positive')
    n = len(x)
    # Rescale by the observation to avoid overflow in pair sums for
    # large but finite native prices. CRPS is positively homogeneous.
    unit = float(true_price)
    xs = np.sort(x / unit)
    if not np.isfinite(xs).all():
        raise OverflowError('scaled ensemble is not finite')
    mean_error = float(np.mean(abs(xs - 1.0)))
    pair_sum = float(np.dot(2*np.arange(n) - n + 1, xs))
    out = unit * (mean_error - pair_sum / (n*n))
    if not math.isfinite(out):
        raise OverflowError('CRPS not representable')
    return max(out, 0.0) if out > -1e-12 * unit else out
