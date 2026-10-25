"""Causal point-forecast scorecard, research sandbox v0.1 (Python stdlib).

This is NOT a predictor. It only scores already-produced out-of-sample
forecasts. Do not pass fitted or in-sample forecasts as independent evidence.
"""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path


REQUIRED = {"asset", "origin_index", "target_index", "horizon",
            "anchor", "actual", "forecast"}


def _positive_number(value, name):
    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and strictly positive")
    return float(value)


def validate_and_score(rows):
    """Aggregate only within asset/horizon; do not pool correlated horizons."""
    groups = defaultdict(list)
    seen = set()
    for i, row in enumerate(rows, 1):
        if type(row) is not dict or set(row) != REQUIRED:
            raise ValueError(f"row {i}: required keys are {sorted(REQUIRED)}")
        asset = row["asset"]
        if type(asset) is not str or not asset.strip() or len(asset) > 64:
            raise ValueError(f"row {i}: invalid asset")
        origin, target, horizon = (row[k] for k in
                                   ("origin_index", "target_index", "horizon"))
        if any(type(x) is not int for x in (origin, target, horizon)):
            raise ValueError(f"row {i}: indices/horizon must be integers")
        if origin < 0 or horizon < 1 or target != origin + horizon:
            raise ValueError(f"row {i}: future target must be origin + horizon")
        key = (asset, origin, horizon)
        if key in seen:
            raise ValueError(f"row {i}: duplicate forecast key")
        seen.add(key)
        anchor = _positive_number(row["anchor"], "anchor")
        actual = _positive_number(row["actual"], "actual")
        forecast = _positive_number(row["forecast"], "forecast")
        groups[(asset, horizon)].append((
            target,
            abs(forecast - actual),
            abs(anchor - actual),
            abs(math.log(forecast / actual)),
            abs(math.log(anchor / actual)),
            (forecast - actual) ** 2,
            (anchor - actual) ** 2,
        ))

    if not groups:
        raise ValueError("empty forecast set")
    outputs = []
    for (asset, horizon), values in sorted(groups.items()):
        n = len(values)
        mean = lambda col: sum(row[col] for row in values) / n
        actual_mae, naive_mae = mean(1), mean(2)
        actual_log_mae, naive_log_mae = mean(3), mean(4)
        outputs.append({
            "asset": asset, "horizon": horizon, "origins": n,
            "distinct_target_observations": len({r[0] for r in values}),
            "forecast_mae_price_units": actual_mae,
            "persistence_mae_price_units": naive_mae,
            "forecast_rmse_price_units": math.sqrt(mean(5)),
            "persistence_rmse_price_units": math.sqrt(mean(6)),
            "forecast_mae_log_price": actual_log_mae,
            "persistence_mae_log_price": naive_log_mae,
            "paired_mae_gain_price_units": naive_mae - actual_mae,
            "paired_mae_gain_log_price": naive_log_mae - actual_log_mae,
        })
    return {
        "status": "descriptive_scorecard_only",
        "not_independent_test_proof": True,
        "not_trading_performance": True,
        "methods": ["forecast", "persistence"],
        "groups": outputs,
        "warnings": [
            "Rows must come from a separately documented chronological out-of-sample pipeline.",
            "Target indices validate horizon geometry, NOT absence of fitting leakage.",
            "Overlapping origins/targets are dependent; no iid p-values or naive intervals.",
            "No pooling of price levels across different assets/currencies.",
            "Point scores are not density likelihoods, calibration, or generative-path evaluation.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("predictions_jsonl", type=Path,
                        help="Explicit user-supplied JSONL, not fetched automatically")
    args = parser.parse_args()
    with args.predictions_jsonl.open("r", encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    print(json.dumps(validate_and_score(rows), indent=2, ensure_ascii=False,
                     allow_nan=False))


if __name__ == "__main__":
    main()
