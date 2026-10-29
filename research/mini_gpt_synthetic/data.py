"""P2 synthetic autoregressive code paths with point-in-time known oracle.

Generated from disjoint RNG streams. No actual prices or any protected
financial holdout. Never use the reserved synthetic test to tune the model.
"""
import numpy as np

PATH_LENGTH = 20
RHO = .75
NOISE_SIGMA = 3.
SPLIT_SEEDS = {'train': 202610251, 'development': 202610252,
               'reserved_synthetic_test': 202610253}
SPLIT_COUNTS = {'train': 192, 'development': 96,
                'reserved_synthetic_test': 96}


def generated_codes(n, *, seed, length=PATH_LENGTH):
    if type(n) is not int or n < 1 or type(seed) is not int:
        raise ValueError('positive path count and exact integer seed required')
    if type(length) is not int or not (1 <= length <= PATH_LENGTH):
        raise ValueError('path length 1..20 required')
    rng=np.random.default_rng(seed)
    data=np.empty((n,length),dtype=np.int64)
    state=np.zeros(n,dtype=np.int64)
    for t in range(length):
        innovation=rng.normal(size=n)*NOISE_SIGMA
        state=np.floor(RHO*state+innovation+0.5).astype(np.int64)
        data[:,t]=state
    return data


def get_split(name, *, allow_reserved_test=False):
    if name not in SPLIT_SEEDS:
        raise ValueError('unknown split')
    if name=='reserved_synthetic_test' and not allow_reserved_test:
        raise PermissionError('reserved test requires explicit authorization; do not tune')
    if len(set(SPLIT_SEEDS.values()))!=len(SPLIT_SEEDS):
        raise AssertionError('split streams must differ')
    return generated_codes(SPLIT_COUNTS[name],seed=SPLIT_SEEDS[name])


def previous_codes(target_codes):
    """Input at t contains k[t-1], NEVER k[t] or beyond."""
    arr=np.asarray(target_codes)
    if arr.ndim!=2 or arr.shape[1]>PATH_LENGTH or arr.shape[1]<1:
        raise ValueError('expected batch of 1..20 integer codes')
    if not np.issubdtype(arr.dtype,np.integer):
        raise TypeError('target codes must be integer')
    prev=np.zeros_like(arr)
    prev[:,1:]=arr[:,:-1]
    return prev


def oracle_mu(previous):
    """True conditional mean of the unrounded Gaussian generator."""
    return RHO*np.asarray(previous,dtype=np.float64)
