"""Numerical tail diagnostics and *conditional* stress sampling, not trading.

Floating-point RNGs cannot unconditionally draw probabilities below their
resolution. A conditional draw is a stress tool and must NEVER be passed off
as a sample of the unconditional law.
"""
import math

import numpy as np
from scipy.special import ndtri_exp

try:
    from .head import Head, LEFT, RIGHT
except ImportError:
    from head import Head, LEFT, RIGHT


def log_tail_probability(head, side):
    if not isinstance(head, Head) or side not in ('left','right'):
        raise ValueError('Head and left/right required')
    return (head.log_left_q if side=='left' else head.log_right_q) - head.log_z


def conditional_tail_sample(head, side, rng):
    """Draw from k | k < LEFT or k > RIGHT, even for underflowed masses.

    Via inverse logarithmic standard normal CDF. Distribution beyond the
    core has correction=0, so conditioning cancels the log normalizer.
    Both sides are genuine unbounded half-lines, not clipped categories.
    """
    if not isinstance(head, Head) or side not in ('left','right'):
        raise ValueError('Head and left/right required')
    u=max(float(rng.random()),np.finfo(float).tiny)
    log_u=math.log(u)
    if side=='left':
        zcut=(LEFT-0.5-head.mu)/head.sigma
        z=float(ndtri_exp(head.log_left_q+log_u))
        value=head.mu+head.sigma*z
        code=math.floor(value+.5)
        if code>=LEFT:
            raise ArithmeticError('tail rounding lost strict boundary')
    else:
        zcut=(RIGHT+0.5-head.mu)/head.sigma
        z=-float(ndtri_exp(head.log_right_q+log_u))
        value=head.mu+head.sigma*z
        code=math.floor(value+.5)
        if code<=RIGHT:
            raise ArithmeticError('tail rounding lost strict boundary')
    if not math.isfinite(value):
        raise ArithmeticError('conditional tail sample nonfinite')
    return code


def sampling_support_audit(head):
    """Explain which nonzero tails are lost in current unconditioned sampler."""
    return {
        'left_logp':log_tail_probability(head,'left'),
        'right_logp':log_tail_probability(head,'right'),
        'left_float64_mass':math.exp(log_tail_probability(head,'left')),
        'right_float64_mass':math.exp(log_tail_probability(head,'right')),
        'left_underflow':math.exp(log_tail_probability(head,'left'))==0.,
        'right_underflow':math.exp(log_tail_probability(head,'right'))==0.,
        'conditional_stress_sampler_is_not_unconditional':True,
        'unconditional_extreme_sampling_certified':False,
    }
