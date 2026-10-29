"""Exploratory paired block bootstrap by ASSET and horizon, toy data only.

Accepts the score-points schema in PR #1; no retrospective market data read.
Blocks describe serial dependence heuristically. This is NOT an automatic
confirmatory significance test and cannot correct selection on test data.
"""
from collections import defaultdict
import math

import numpy as np

COLUMNS={'asset','origin_index','target_index','horizon',
         'anchor','actual','forecast'}


def validate_records(records):
    if not isinstance(records,list) or not records:
        raise ValueError('nonempty prepared list required')
    cleaned=[]
    keys=set()
    for r in records:
        if not isinstance(r,dict) or set(r)!=COLUMNS:
            raise ValueError('records must match score_points schema exactly')
        if not isinstance(r['asset'],str) or not r['asset']:
            raise ValueError('asset id required')
        origin,target,h=r['origin_index'],r['target_index'],r['horizon']
        if any(type(i) is not int for i in (origin,target,h)) or origin<0 or h<1 or target-origin!=h:
            raise ValueError('invalid observed-index horizon contract')
        for field in ('anchor','actual','forecast'):
            p=r[field]
            if type(p) not in (int,float) or not math.isfinite(p) or p<=0:
                raise ValueError('all prices must be finite positive native prices')
        key=(r['asset'],h,origin)
        if key in keys:
            raise ValueError('duplicate score origin; overlapping labels not new observations')
        keys.add(key)
        cleaned.append(r)
    return cleaned


def paired_group_report(records):
    groups=defaultdict(list)
    for r in validate_records(records):
        groups[(r['asset'],r['horizon'])].append(r)
    report={}
    for (asset,h),items in sorted(groups.items()):
        chronological=sorted(items,key=lambda p:p['origin_index'])
        n=len(chronological)
        differences=np.array([
            abs(p['anchor']-p['actual'])-abs(p['forecast']-p['actual'])
            for p in chronological],dtype=float)
        model=np.mean([abs(p['forecast']-p['actual']) for p in chronological])
        persistence=np.mean([abs(p['anchor']-p['actual']) for p in chronological])
        key=f'{asset}::h={h}'
        report[key]={
            'asset':asset,'horizon':h,'n_origin_presentations':n,
            'n_unique_targets':len(set(p['target_index'] for p in chronological)),
            'mae_native_model':float(model),
            'mae_native_persistence':float(persistence),
            'mean_paired_gain_native':float(np.mean(differences)),
            'gain_percent_if_defined': (
                100*(float(persistence)-float(model))/float(persistence)
                if persistence>0 else None),
            'origin_indices':[p['origin_index'] for p in chronological],
            'paired_gains':differences.tolist(),
            'labels_overlap':h>1 and any(
                chronological[j+1]['origin_index']-chronological[j]['origin_index']<h
                for j in range(n-1)),
        }
    return report


def moving_block_interval(gains,*,block=20,seed=20261025,resamples=1000):
    """Percentile CI conditional on fixed available origins.

    Overlap, nonstationarity, selection, and multi-model comparisons remain
    external statistical concerns; never treat this as a p-value.
    """
    x=np.asarray(gains,dtype=float)
    if x.ndim!=1 or not np.isfinite(x).all():
        raise ValueError('finite 1D paired gains required')
    if type(block) is not int or block<1 or len(x)<2*block:
        raise ValueError('at least two non-overlapping block lengths required')
    if type(resamples) is not int or not (100<=resamples<=10000):
        raise ValueError('100..10000 resamples required')
    rng=np.random.default_rng(seed)
    length=len(x)
    starts=np.arange(length-block+1)
    num=(length+block-1)//block
    samples=np.empty(resamples)
    for i in range(resamples):
        offsets=rng.choice(starts,size=num,replace=True)
        sample=np.concatenate([x[j:j+block] for j in offsets])[:length]
        samples[i]=sample.mean()
    low,high=np.quantile(samples,[.025,.975])
    return {
        'observed_mean_gain':float(np.mean(x)),
        'percentile_ci95':[float(low),float(high)],
        'bootstrap_mean':float(samples.mean()),
        'block_length_origins':block,'resamples':resamples,'seed':seed,
        'uncertainty_scope':'exploratory dependence-aware, not a confirmatory p-value',
        'cannot_fix_selection_leakage':True,
    }
