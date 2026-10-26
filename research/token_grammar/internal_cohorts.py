"""S3.1C strictly pre-2022 internally time-split reservoir sampler.

The streamer stops before 2022 candles/labels. Old S1/S2/S3 cases remain
unchanged if this optional cutoff is not supplied. This module never calls
the A7 collect() function, which would read external development.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path

import numpy as np

from research.btc_h1_m1.stream import ROOT,iter_cases
from research.continuous_direction.runner import _origin_digest

UTC=timezone.utc
TRAIN_END=datetime(2020,1,1,tzinfo=UTC)
MONITOR_END=datetime(2022,1,1,tzinfo=UTC)


def validate_internal(train,monitor):
    if not train or not monitor:
        raise ValueError("train and monitor must each be nonempty")
    train_keys=set()
    monitor_keys=set()
    for name,cases,lo,hi in (
            ("train",train,None,TRAIN_END),
            ("monitor",monitor,TRAIN_END,MONITOR_END)):
        for c in cases:
            when=c.label_available_time
            if (when.tzinfo is None or when.utcoffset().total_seconds()!=0
                    or when>=hi or (lo is not None and when<lo)
                    or c.decision_time>=when or c.target_open>=when
                    or len(c.continuous_past_bps)!=20):
                raise ValueError(f"{name} label time/causality violation")
            key=when.isoformat()
            keys=train_keys if name=="train" else monitor_keys
            if key in keys:
                raise ValueError("duplicate label time in same internal split")
            keys.add(key)
    if train_keys & monitor_keys:
        raise ValueError("leaked repeated target between splits")
    if max(c.label_available_time for c in train)>=min(
            c.label_available_time for c in monitor):
        raise ValueError("nonchronological train-monitor split")
    return {"train_count":len(train),"monitor_count":len(monitor),
            "train_origins_sha256":_origin_digest(train),
            "monitor_origins_sha256":_origin_digest(monitor),
            "last_train_label":max(c.label_available_time for c in train).isoformat(),
            "first_monitor_label":min(c.label_available_time for c in monitor).isoformat(),
            "all_labels_before_2022":True,"external_development_read":False}


def split_case_sequence(cases, *, max_train=4096,max_monitor=1024,
                        sampling_seed=20261025):
    if (type(max_train)!=int or max_train<32 or
            type(max_monitor)!=int or max_monitor<32
            or type(sampling_seed)!=int):
        raise ValueError("invalid deterministic sample caps")
    pools={"train":[],"monitor":[]}
    seen={"train":0,"monitor":0}
    rng={"train":np.random.default_rng(sampling_seed),
         "monitor":np.random.default_rng(sampling_seed+1)}
    for c in cases:
        time=c.label_available_time
        if time>=MONITOR_END:
            raise ValueError("post-2021 case reached the internal sampling boundary")
        part="train" if time<TRAIN_END else "monitor"
        n=seen[part]+1
        seen[part]=n
        cap=max_train if part=="train" else max_monitor
        if len(pools[part])<cap:
            pools[part].append(c)
        else:
            index=int(rng[part].integers(0,n))
            if index<cap:
                pools[part][index]=c
    if min(len(pools["train"]),len(pools["monitor"]))<32:
        raise ValueError("insufficient 2012–2019 train or 2020–2021 monitor data")
    for cases in pools.values():
        cases.sort(key=lambda c:c.label_available_time)
    provenance=validate_internal(pools["train"],pools["monitor"])
    return pools,{**provenance,"scanned_case_counts":seen,
                  "reservoir_seed":sampling_seed,
                  "reservoir_selected_after_time_split":True}


def collect_pre2022(interval,folder=ROOT, *, max_train=4096,
                    max_monitor=1024,sampling_seed=20261025):
    if interval not in ("D1","H1","M1"):
        raise ValueError("D1/H1/M1 only")
    stride=60 if interval=="M1" else 1
    def _pre2022():
        for split,case in iter_cases(interval,Path(folder),
                  step=stride,train_only=True,
                  stop_labels_before=MONITOR_END):
            if split!="train":
                raise ValueError("unexpected external development case")
            yield case
    pools,provenance=split_case_sequence(
        _pre2022(),max_train=max_train,
        max_monitor=max_monitor,sampling_seed=sampling_seed)
    provenance["interval"]=interval
    provenance["sampling_stride"]=stride
    return pools,provenance
