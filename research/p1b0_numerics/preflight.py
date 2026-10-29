"""Deterministic numerical stress protocol for the P1-B0 candidate.

Only constructed parameters. It does not download, fit or test market data,
and its success cannot be interpreted as a predictive or trading result.
"""
import json
import math
import platform

import numpy as np
import scipy

try:
    from .head import Head, hierarchical_logits
except ImportError:
    from head import Head, hierarchical_logits


def run():
    configurations = [(0.0, 8.0, 64.0), (256.0, 64.0, 64.0),
                      (-256.0, 64.0, 64.0), (256.0, 256.0, 256.0),
                      (0.0, 0.25, 64.0)]
    flat = np.zeros(4096)
    flat[2048] = 20.0
    flat[2049] = -20.0
    hierarchical = hierarchical_logits(
        np.sin(np.arange(512, dtype=np.float64) / 29),
        np.array([[0.2, -0.2], [-0.1, 0.1], [0.3, -0.3]]))
    arms = {'BASE': None, 'FLAT': flat, 'HIER': hierarchical}
    results = []
    for mu, sigma, limit in configurations:
        for arm, logits in arms.items():
            head = Head(mu, sigma, logits=logits, max_sigma=limit)
            audit = head.mass_audit()
            assert abs(audit['sum'] - 1) <= 1e-12
            tails = {
                'left_log_probability': head.log_left_q - head.log_z,
                'right_log_probability': head.log_right_q - head.log_z,
                'outside_probability': audit['left'] + audit['right'],
            }
            assert math.isfinite(head.log_prob(-4000))
            assert math.isfinite(head.log_prob(4000))
            assert math.isfinite(head.log_prob(0))
            results.append({
                'arm': arm, 'mu': mu, 'sigma': sigma, 'S_limit': limit,
                'normalizer_log': audit['log_z'],
                'mass_total': audit['sum'],
                'core_mass': audit['core'],
                'tails': tails,
                'rare_log_prob_minus4000': head.log_prob(-4000),
                'rare_log_prob_plus4000': head.log_prob(4000),
            })
    return {
        'experiment': 'p1b0_numerical_preflight_v0.1',
        'status': 'constructed_parameters_only',
        'market_data_read': False,
        'model_trained': False,
        'forecast_quality_tested': False,
        'rng_used': False,
        'runtime': {'python': platform.python_version(),
                    'numpy': np.__version__, 'scipy': scipy.__version__},
        'tolerances': {'mass_error': 1e-12},
        'cases': results,
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, allow_nan=False))
