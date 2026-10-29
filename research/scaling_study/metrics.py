"""S1.4: causal direction + price-amplitude scores on aligned one-candle forecasts.

No transaction fees, position sizing, backtested account curve or trade execution.
Magnitude buckets use thresholds fitted on TRAIN realised moves only; dev
labels never choose which signal is large.
"""
from __future__ import annotations

import math
import numpy as np


def training_magnitude_thresholds(train_cases):
    if len(train_cases) < 16:
        raise ValueError("at least 16 train cases required")
    anchors = np.asarray([c.anchor_usd for c in train_cases], dtype=float)
    true = np.asarray([c.target_usd for c in train_cases], dtype=float)
    if (not np.isfinite(anchors).all() or not np.isfinite(true).all()
            or np.any(anchors <= 0) or np.any(true <= 0)):
        raise ValueError("positive finite train prices required")
    absolute_bps = 10000.0 * np.abs(true / anchors - 1.0)
    q50, q75 = np.quantile(absolute_bps, (0.5, 0.75))
    return {"q50_bps": float(q50), "q75_bps": float(q75),
            "thresholds_trained_only": True, "train_count": len(train_cases)}


def _safe_fraction(numerator, denominator):
    return float(numerator / denominator) if denominator else None


def _direction_summary(true_sign, pred_sign):
    active = pred_sign != 0
    truth_nonflat = true_sign != 0
    both = active & truth_nonflat
    correct = true_sign == pred_sign
    positive = true_sign == 1
    negative = true_sign == -1
    up_recall = _safe_fraction(int(np.sum(correct & positive)), int(np.sum(positive)))
    down_recall = _safe_fraction(int(np.sum(correct & negative)), int(np.sum(negative)))
    return {
        "direction_accuracy_all": float(np.mean(correct)),
        "direction_accuracy_nonflat_truth": _safe_fraction(
            int(np.sum(correct & truth_nonflat)), int(np.sum(truth_nonflat))),
        "direction_accuracy_when_signaled": _safe_fraction(
            int(np.sum(correct & active)), int(np.sum(active))),
        "signal_coverage": float(np.mean(active)),
        "direction_accuracy_active_nonflat": _safe_fraction(
            int(np.sum(correct & both)), int(np.sum(both))),
        "balanced_direction_accuracy": (
            (up_recall + down_recall) / 2
            if up_recall is not None and down_recall is not None else None),
        "n_up_actual": int(np.sum(positive)),
        "n_down_actual": int(np.sum(negative)),
        "n_flat_actual": int(np.sum(true_sign == 0)),
        "n_predicted_up": int(np.sum(pred_sign == 1)),
        "n_predicted_down": int(np.sum(pred_sign == -1)),
        "n_predicted_flat": int(np.sum(pred_sign == 0)),
    }


def score_forecasts(anchors, actuals, forecasts, *, train_thresholds):
    a = np.asarray(anchors, dtype=float)
    y = np.asarray(actuals, dtype=float)
    p = np.asarray(forecasts, dtype=float)
    if (a.ndim != 1 or len(a) == 0 or y.shape != a.shape or p.shape != a.shape
            or not np.isfinite(a).all() or not np.isfinite(y).all()
            or not np.isfinite(p).all()
            or np.any(a <= 0) or np.any(y <= 0) or np.any(p <= 0)):
        raise ValueError("aligned finite positive one-dimensional prices required")
    if (not isinstance(train_thresholds, dict)
            or train_thresholds.get("thresholds_trained_only") is not True
            or not all(k in train_thresholds for k in ("q50_bps", "q75_bps"))
            or any(not isinstance(train_thresholds[k], (float, int)) or
                   not math.isfinite(train_thresholds[k])
                   for k in ("q50_bps", "q75_bps"))
            or not 0 <= train_thresholds["q50_bps"] <= train_thresholds["q75_bps"]):
        raise ValueError("finite nonnegative train-only magnitude thresholds needed")

    target_move = (y / a - 1) * 10000.0
    forecast_move = (p / a - 1) * 10000.0
    magnitude_error = np.abs(np.abs(forecast_move) - np.abs(target_move))
    price_error = p - y
    true_sign = np.sign(y - a).astype(int)
    pred_sign = np.sign(p - a).astype(int)
    direction = _direction_summary(true_sign, pred_sign)
    threshold50 = train_thresholds["q50_bps"]
    threshold75 = train_thresholds["q75_bps"]
    forecast_abs = np.abs(forecast_move)
    groups = (
        ("small_predicted_move", forecast_abs <= threshold50),
        ("medium_predicted_move",
         (forecast_abs > threshold50) & (forecast_abs <= threshold75)),
        ("large_predicted_move", forecast_abs > threshold75),
    )
    buckets = {}
    for name, mask in groups:
        n = int(np.sum(mask))
        if n == 0:
            buckets[name] = {"count": 0, "direction_accuracy": None,
                             "mae_bps_anchor": None,
                             "mean_abs_forecast_move_bps": None,
                             "mean_abs_realised_move_bps": None}
            continue
        buckets[name] = {
            "count": n,
            "direction_accuracy": float(np.mean(true_sign[mask] == pred_sign[mask])),
            "signal_coverage": float(np.mean(pred_sign[mask] != 0)),
            "mae_bps_anchor": float(np.mean(np.abs(price_error[mask] / a[mask]) * 10000)),
            "mean_abs_forecast_move_bps": float(np.mean(forecast_abs[mask])),
            "mean_abs_realised_move_bps": float(np.mean(np.abs(target_move[mask]))),
        }
    result = {
        "forecast_rows": len(a),
        "mae_native_usd": float(np.mean(np.abs(price_error))),
        "rmse_native_usd": float(np.sqrt(np.mean(price_error ** 2))),
        "mae_bps_anchor": float(np.mean(np.abs(price_error / a) * 10000)),
        "absolute_magnitude_error_bps": float(np.mean(magnitude_error)),
        "signed_forecast_bias_bps": float(np.mean(forecast_move - target_move)),
        "mean_abs_predicted_move_bps": float(np.mean(forecast_abs)),
        "mean_abs_actual_move_bps": float(np.mean(np.abs(target_move))),
        "gross_signal_return_mean_bps_per_sample": float(
            np.mean(pred_sign * target_move)),
        "buy_hold_same_sample_mean_bps": float(np.mean(target_move)),
        "gross_signal_dollars_per_1000_per_sample": float(
            np.mean(pred_sign * target_move) / 10.0),
        "direction_by_predicted_magnitude": buckets,
        "magnitude_thresholds_bps_train_only": {
            "q50": threshold50, "q75": threshold75},
        "not_cumulative_portfolio_return": True,
        "no_trading_costs": True,
        "no_trade_execution": True,
    }
    result.update(direction)
    return result


def baseline_forecasts(dev_cases):
    """Persistence and last past *quantized-code* sign, with no future labels."""
    if not dev_cases:
        raise ValueError("no development cases")
    anchor = np.asarray([c.anchor_usd for c in dev_cases], dtype=float)
    # Deliberately predict a tiny, fixed 1bp move. This baseline only tests
    # direction, NOT price magnitude or strategy optimisation.
    last_code = np.asarray([c.encoded_past[-1] for c in dev_cases], dtype=float)
    direction = np.sign(last_code)
    return {
        "persistence_flat": anchor.copy(),
        "always_up_1bp": anchor * (1.0 + 1.0 / 10000.0),
        "always_down_1bp": anchor * (1.0 - 1.0 / 10000.0),
        "last_quantized_momentum_1bp": anchor * (1.0 + direction / 10000.0),
    }
