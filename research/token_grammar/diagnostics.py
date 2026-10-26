"""S3.0 purely diagnostic market-grammar codecs, without private BTC data.

Each input is a *completed* candle's scalar log-return in basis points.
No price level, future close, order, or per-asset secret is consumed.
A codec's train-only fit is immutable and has no evaluation-time fitting.
This module deliberately does NOT train a forecasting model.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import floor, isfinite, log2
from statistics import mean
from typing import Sequence


def _finite(values):
    if not isinstance(values, (tuple, list)) or not values:
        raise ValueError("non-empty list/tuple of return bps required")
    if any(type(x) not in (int, float) or not isfinite(x) for x in values):
        raise ValueError("only finite numeric returns accepted")
    return tuple(float(x) for x in values)


def _quantile(sorted_values, probability):
    """Simple linear interpolation, deterministic across Python environments."""
    if not sorted_values:
        raise ValueError("empty quantile input")
    pos=(len(sorted_values)-1)*probability
    low=floor(pos)
    high=min(low+1,len(sorted_values)-1)
    return sorted_values[low]+(pos-low)*(sorted_values[high]-sorted_values[low])


@dataclass(frozen=True)
class Grammar:
    family: str
    boundaries_bps: tuple[float, ...] = ()
    centers_bps: tuple[float, ...] = ()
    fit_on_train_only: bool = True
    exact_zero_preserved: bool = True

    def encode(self, returns_bps):
        inputs=_finite(returns_bps)
        if self.family=="legacy_g0a":
            # Legacy code_return round(1000*log_return) = floor(bps/10 + 0.5).
            return tuple(f"R{floor(v/10+0.5)}" for v in inputs)
        if self.family=="continuous_g0b":
            return inputs
        if self.family not in ("signed_uniform_g1","signed_quantile_g2"):
            raise ValueError("unknown grammar")
        result=[]
        for v in inputs:
            if v==0.0:
                result.append("FLAT")
            else:
                magnitude=abs(v)
                index=sum(magnitude > edge for edge in self.boundaries_bps)
                result.append(("UP" if v>0 else "DOWN")+str(index))
        return tuple(result)

    def decode(self, tokens):
        if not isinstance(tokens, (list, tuple)) or not tokens:
            raise ValueError("nonempty tokens needed")
        if self.family=="continuous_g0b":
            return _finite(tokens)
        result=[]
        for token in tokens:
            if not isinstance(token,str):
                raise ValueError("string tokens required")
            if self.family=="legacy_g0a":
                if not token.startswith("R"):
                    raise ValueError("invalid legacy token")
                try:
                    index=int(token[1:])
                except ValueError as exc:
                    raise ValueError("invalid integer token") from exc
                if token!=f"R{index}":
                    raise ValueError("noncanonical legacy token")
                result.append(float(index*10))
                continue
            if token=="FLAT":
                result.append(0.0)
                continue
            if self.family not in ("signed_uniform_g1","signed_quantile_g2"):
                raise ValueError("unknown grammar")
            prefix=("UP" if token.startswith("UP")
                    else "DOWN" if token.startswith("DOWN") else None)
            if prefix is None:
                raise ValueError("unknown signed token")
            suffix=token[len(prefix):]
            if not suffix.isdecimal():
                raise ValueError("invalid bucket index")
            index=int(suffix)
            if suffix!=str(index) or not 0<=index<len(self.centers_bps):
                raise ValueError("bucket outside fitted vocabulary")
            result.append((1.0 if prefix=="UP" else -1.0)*self.centers_bps[index])
        return tuple(result)


def legacy_grammar():
    return Grammar("legacy_g0a",exact_zero_preserved=False)


def continuous_grammar():
    return Grammar("continuous_g0b")


def signed_uniform_grammar():
    # Fixed, explicit bps magnitude bands; 150bps saturates at the extreme bin.
    boundaries=(1.,5.,20.,100.)
    centers=(0.5,3.,12.5,60.,150.)
    return Grammar("signed_uniform_g1",boundaries,centers)


def fit_signed_quantile_grammar(train_returns_bps,*,bins=5):
    """Quantile vocabulary fit ONLY on past TRAIN returns, NEVER on dev."""
    inputs=_finite(train_returns_bps)
    if type(bins) is not int or not 2<=bins<=16:
        raise ValueError("quantile bins 2..16 required")
    magnitudes=sorted(abs(x) for x in inputs if x!=0)
    if len(magnitudes)<bins or len(set(magnitudes))<bins:
        raise ValueError("too few distinct non-flat TRAIN magnitudes")
    # Quantiles chosen without consulting any eval labels. Repeated quantile
    # edges can be caused by uneven data; fail rather than hide empty buckets.
    boundaries=tuple(_quantile(magnitudes,i/bins) for i in range(1,bins))
    if len(set(boundaries))!=len(boundaries):
        raise ValueError("nonidentifiable train quantile bins")
    centers=[]
    lower=0.
    for upper in boundaries:
        centers.append((lower+upper)/2)
        lower=upper
    last=_quantile(magnitudes,1.0)
    centers.append((lower+last)/2)
    return Grammar("signed_quantile_g2",boundaries,tuple(centers))


def reconstruction_diagnostics(grammar,returns_bps):
    """Descriptive information preservation, NEVER forecast skill."""
    original=_finite(returns_bps)
    token_sequence=grammar.encode(original)
    reconstructed=grammar.decode(token_sequence)
    size=len(original)
    c=Counter(token_sequence) if grammar.family!="continuous_g0b" else Counter()
    original_nonflat=sum(x!=0 for x in original)
    lost_direction=sum(
        x!=0 and (y==0 or (x>0)!=(y>0))
        for x,y in zip(original,reconstructed))
    abs_err=mean(abs(abs(x)-abs(y)) for x,y in zip(original,reconstructed))
    thresholds=grammar.boundaries_bps
    out_of_range=sum(abs(x)>thresholds[-1] for x in original) if (
        grammar.family=="signed_quantile_g2" and thresholds) else None
    return {
        "grammar":grammar.family,
        "samples":size,
        "forecast_skill_measured":False,
        "uses_future_labels_for_fit":False,
        "original_nonflat_count":original_nonflat,
        "direction_lost_count":lost_direction,
        "direction_lost_fraction_of_nonflat":(
            lost_direction/original_nonflat if original_nonflat else None),
        "absolute_magnitude_reconstruction_mae_bps":abs_err,
        "vocabulary_used":len(c) if c else None,
        "empirical_token_entropy_bits":(
            -sum((v/size)*log2(v/size) for v in c.values()) if c else None),
        "above_largest_train_boundary_count":out_of_range,
        "note":"Reconstruction metric only; not accuracy or PnL",
    }
