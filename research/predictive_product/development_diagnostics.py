"""P2: offline descriptive calibration and predeclared abstention checks.

Input forecast records are supplied by a caller and not authenticated.
Supports *development diagnostics only*. No independent test, no trading,
no inference engine, no financial-validity verdict.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass(frozen=True)
class ForecastRecord:
    origin_utc: datetime
    target_utc: datetime
    prediction_available_utc: datetime
    label_available_utc: datetime
    q10_usd: float
    q50_usd: float
    q90_usd: float
    actual_usd: float
    context_contiguous_at_origin: bool
    in_training_support_at_origin: bool


def _utc(value):
    if (not isinstance(value, datetime) or value.tzinfo is None
            or value.utcoffset() != timedelta(0)):
        raise ValueError("aware UTC datetime required")
    return value


def development_diagnostics(records, *, split="synthetic_development"):
    """Describe coverage and pinball without using any reserved test labels."""
    if split not in ("synthetic_development", "btc_development"):
        raise ValueError("only explicitly exploratory development is permitted")
    if not isinstance(records, (tuple, list)) or not 10 <= len(records) <= 100_000:
        raise ValueError("10..100000 development forecast pairs required")
    previous_origin = None
    horizon = None
    accepted = []
    excluded_quality = excluded_ood = 0
    btc_end = datetime.fromisoformat("2026-01-01T00:00:00+00:00")
    btc_start = datetime.fromisoformat("2022-01-01T00:00:00+00:00")
    for row in records:
        if not isinstance(row, ForecastRecord):
            raise TypeError("ForecastRecord required")
        for field in ("origin_utc", "target_utc", "prediction_available_utc",
                      "label_available_utc"):
            _utc(getattr(row, field))
        if (row.prediction_available_utc > row.origin_utc
                or row.target_utc <= row.origin_utc
                or row.label_available_utc < row.target_utc):
            raise ValueError("future leakage or target chronology violation")
        if previous_origin is not None and row.origin_utc <= previous_origin:
            raise ValueError("origins must strictly increase")
        previous_origin = row.origin_utc
        period = row.target_utc - row.origin_utc
        if horizon is None:
            horizon = period
        elif period != horizon:
            raise ValueError("mixed forecast horizons must be scored separately")
        if split == "btc_development" and not (
                btc_start <= row.target_utc < btc_end):
            raise ValueError("BTC development targets must be in 2022–2025")
        prices = (row.q10_usd, row.q50_usd, row.q90_usd, row.actual_usd)
        if (any(type(p) not in (int, float) or not math.isfinite(p) or p <= 0
                for p in prices)
                or not row.q10_usd <= row.q50_usd <= row.q90_usd):
            raise ValueError("invalid or crossing predicted price quantiles")
        if (type(row.context_contiguous_at_origin) is not bool
                or type(row.in_training_support_at_origin) is not bool):
            raise ValueError("origin-time quality flags must be booleans")
        if not row.context_contiguous_at_origin:
            excluded_quality += 1
        elif not row.in_training_support_at_origin:
            excluded_ood += 1
        else:
            accepted.append(row)
    def pinball(q, truth, level):
        error = truth - q
        return max(level * error, (level-1) * error)
    n = len(accepted)
    coverage = (sum(p.q10_usd <= p.actual_usd <= p.q90_usd
                    for p in accepted)/n) if n else None
    scores = {}
    if n:
        for level, attr in ((.1, "q10_usd"), (.5, "q50_usd"), (.9, "q90_usd")):
            scores[str(level)] = sum(pinball(getattr(p,attr), p.actual_usd, level)
                                     for p in accepted)/n
    return {
        "schema": "TRAME_P2_EXPLORATORY_CALIBRATION_V1",
        "split": split,
        "horizon_seconds": int(horizon.total_seconds()),
        "origins_seen": len(records),
        "forecasts_not_abstained": n,
        "abstained_due_to_missing_context": excluded_quality,
        "abstained_due_to_training_support": excluded_ood,
        "empirical_80pct_coverage": coverage,
        "pinball_native_usd": scores,
        "target_80pct_coverage": .8,
        "calibration_independently_verified": False,
        "holdout_opened_by_diagnostics": False,
        "source_authenticity_verified": False,
        "model_ready_for_financial_prediction": False,
        "no_model_selection_from_reserved_test": True,
    }
