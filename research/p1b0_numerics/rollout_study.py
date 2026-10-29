"""Reproducible demonstration of price-native CRPS on fabricated trajectories."""
import json
import numpy as np

try:
    from .head import Head
    from .rollout import rollout, empirical_crps
except ImportError:
    from head import Head
    from rollout import rollout, empirical_crps


def run():
    rng=np.random.default_rng(20261025)
    law=lambda step,prev: Head(mu=0., sigma=8., max_sigma=64.)
    anchor=100.
    scale=0.02
    horizon=20
    paths=[rollout(anchor,scale,law,rng,horizon=horizon)
           for _ in range(512)]
    prices=[p.prices[-1] for p in paths]
    observed=rollout(anchor,scale,law,rng,horizon=horizon).prices[-1]
    return {
        'experiment':'p1b0_native_price_smoke_v0.1',
        'market_data_read':False, 'model_trained':False,
        'origin_anchor_fictional':anchor,'past_scale_fictional':scale,
        'horizon':horizon,'ensemble':len(prices),'seed':20261025,
        'independent_fictional_truth':observed,
        'price_median':float(np.median(prices)),
        'price_q10':float(np.percentile(prices,10)),
        'price_q90':float(np.percentile(prices,90)),
        'empirical_CRPS_price_units':empirical_crps(prices,observed),
        'persistence_absolute_error_price_units':abs(anchor-observed),
        'limitation':'one random toy realization cannot establish forecast superiority',
    }


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
