"""Price-native ensemble diagnostics, finite Monte-Carlo uncertainty only.

Every metric uses the same native units within ONE instrument and horizon.
No pooled PnL, no claim of independent overlapping origin windows.
"""
import math
import statistics

import numpy as np

try:
    from .rollout import empirical_crps
except ImportError:
    from rollout import empirical_crps


def score_ensemble(draws, observed, anchor):
    x=np.asarray(draws,dtype=np.float64)
    if x.ndim != 1 or x.size < 2 or not np.isfinite(x).all() or (x <= 0).any():
        raise ValueError("at least two positive finite native-price draws required")
    if not math.isfinite(observed) or observed <= 0 or not math.isfinite(anchor) or anchor <= 0:
        raise ValueError("observed and persistence anchor must be finite positive")
    q=np.quantile(x,[.05,.10,.25,.50,.75,.90,.95])
    return {
        'n_draws':len(x),
        'q05':float(q[0]),'q10':float(q[1]),'q25':float(q[2]),
        'median':float(q[3]),'q75':float(q[4]),'q90':float(q[5]),'q95':float(q[6]),
        'median_absolute_error':abs(float(q[3])-observed),
        'persistence_absolute_error':abs(anchor-observed),
        'crps_price_units':empirical_crps(x,observed),
        'coverage50':bool(q[2] <= observed <= q[4]),
        'coverage80':bool(q[1] <= observed <= q[5]),
        'coverage90':bool(q[0] <= observed <= q[6]),
        'width50':float(q[4]-q[2]),
        'width80':float(q[5]-q[1]),
        'width90':float(q[6]-q[0]),
    }


def mc_replicate_crps(draw_group, observed):
    """Repeated independent simulation ensembles measure *MC* uncertainty.

    Not an uncertainty interval across historical market regimes. Group
    count >= 3, no bootstrap of overlapping origin windows.
    """
    if len(draw_group) < 3:
        raise ValueError("at least three independent ensemble replicates")
    scores=[empirical_crps(x,observed) for x in draw_group]
    avg=statistics.mean(scores)
    se=statistics.stdev(scores)/math.sqrt(len(scores))
    return {'replicates':len(scores),'mean_empirical_crps':avg,
            'mc_standard_error_across_independent_ensembles':se,
            'min_crps':min(scores),'max_crps':max(scores),
            'warning':'This is uncertainty from Monte-Carlo only, not from market forecast errors'}
