"""A6 causal input-output contract for external pre-trained forecast models.

No model imports/downloads. This checks chronology/units and quantile order;
it cannot prove the internal checkpoint never saw a held-out series before.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass(frozen=True)
class Observation:
    observed_at: datetime
    available_at: datetime
    price_native: float


@dataclass(frozen=True)
class Forecast:
    target_at: datetime
    quantiles_native: dict[float, float]


def _utc(t):
    if (not isinstance(t, datetime) or t.tzinfo is None
            or t.utcoffset() != timedelta(0)):
        raise ValueError("timezone-aware UTC datetime required")
    return t


def validate_forecast_contract(*, origin, history, output, known_future=()):
    """Enforce no known temporal leakage in reported inputs/outputs."""
    _utc(origin)
    if (not isinstance(history, (tuple, list)) or len(history) < 2
            or not isinstance(output, (tuple, list)) or not output):
        raise ValueError("at least two historical inputs and one future target required")
    previous = None
    for bar in history:
        if not isinstance(bar, Observation):
            raise TypeError("Observation records required")
        t = _utc(bar.observed_at)
        _utc(bar.available_at)
        if (t > origin or bar.available_at > origin
                or (previous is not None and t <= previous)):
            raise ValueError("unavailable, nonmonotonic or future historical observation")
        if not (math.isfinite(bar.price_native) and bar.price_native > 0):
            raise ValueError("positive finite prices required")
        previous = t
    last_target = origin
    for forecast in output:
        if not isinstance(forecast, Forecast):
            raise TypeError("Forecast records required")
        at = _utc(forecast.target_at)
        if at <= last_target:
            raise ValueError("forecast targets must strictly follow the origin")
        last_target = at
        q = forecast.quantiles_native
        if not isinstance(q, dict) or not q:
            raise ValueError("positive price quantile dict required")
        keys = sorted(q)
        if any(type(level) not in (int, float) or not 0 < level < 1 for level in keys):
            raise ValueError("quantile levels must be in (0,1)")
        values = [q[level] for level in keys]
        if (any(type(value) not in (float, int) or not math.isfinite(value)
                or value <= 0 for value in values)
                or any(v > nxt for v, nxt in zip(values, values[1:]))):
            raise ValueError("nonfinite, nonpositive or crossing quantiles")
    for known_time, published_at, value in known_future:
        _utc(known_time)
        _utc(published_at)
        if published_at > origin:
            raise ValueError("future covariate not known at the forecast origin")
        if not math.isfinite(float(value)):
            raise ValueError("nonfinite covariate")
    return {
        "valid_temporal_contract": True,
        "origin_utc": origin.isoformat(), "context_points": len(history),
        "forecast_horizons": len(output),
        "all_covariates_known_at_origin": True,
        "zero_shot_weight_executed": False,
        "pretraining_contamination_ruled_out": False,
        "independent_financial_test_completed": False,
    }
