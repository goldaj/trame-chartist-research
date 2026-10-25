"""A7.3 classical next-candle BTC baselines with strictly train-only fits.

Research only. Does not download data, open 2026 labels, trade, or claim an
independent test. Historic BTC/Bitstamp candles are spot proxies, not
Hyperliquid perpetual executions.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT


LEVELS = (0.1, 0.5, 0.9)
ZS = tuple(NormalDist().inv_cdf(q) for q in LEVELS)


def _matrix(cases):
    if len(cases) < 32:
        raise ValueError("at least 32 causal examples required")
    past = np.asarray([c.encoded_past for c in cases], dtype=float)
    if past.ndim != 2 or past.shape[1] < 5 or not np.isfinite(past).all():
        raise ValueError("at least 5 finite historical returns per example")
    anchor = np.asarray([c.anchor_usd for c in cases], dtype=float)
    actual = np.asarray([c.target_usd for c in cases], dtype=float)
    if (not np.isfinite(anchor).all() or not np.isfinite(actual).all()
            or np.any(anchor <= 0) or np.any(actual <= 0)):
        raise ValueError("positive finite prices required")
    features = np.column_stack((
        past[:, -1] / 1000.,
        np.mean(past[:, -5:], axis=1) / 1000.,
        np.mean(past, axis=1) / 1000.,
    ))
    target_log_return = np.log(actual / anchor)
    return features, anchor, actual, target_log_return


def fit_baselines(train, *, ridge_alpha=1.0):
    if type(ridge_alpha) not in (float, int) or not 0 < ridge_alpha <= 100:
        raise ValueError("positive ridge_alpha 0..100 required")
    if any(c.target_open.year >= 2022 for c in train):
        raise ValueError("only train targets before 2022 are permitted")
    x, _, _, y = _matrix(train)
    mean = x.mean(axis=0)
    scale = x.std(axis=0)
    scale = np.where(scale < 1e-10, 1., scale)
    normalized = np.column_stack((np.ones(len(x)), (x-mean)/scale))
    penalty = np.diag([0., ridge_alpha, ridge_alpha, ridge_alpha])
    weights = np.linalg.solve(normalized.T @ normalized + penalty,
                              normalized.T @ y)
    resid = y - normalized @ weights
    return {
        "feature_mean": mean.tolist(),
        "feature_scale_train_only": scale.tolist(),
        "ridge_weights": weights.tolist(),
        "ridge_alpha_fixed_pre_dev": float(ridge_alpha),
        "ridge_train_residual_sigma_log": max(1e-5, float(np.std(resid, ddof=1))),
        "persistence_train_sigma_log": max(1e-5, float(np.std(y, ddof=1))),
        "train_targets_seen": len(train),
        "fitted_using_development": False,
    }


def _score(anchor, true, mu, sigma):
    median = anchor * np.exp(mu)
    q = np.asarray([anchor * np.exp(mu + z * sigma) for z in ZS])
    errors = median - true
    pinball = {}
    for index, level in enumerate(LEVELS):
        delta = true - q[index]
        pinball[str(level)] = float(np.mean(np.maximum(level*delta,
                                                       (level-1)*delta)))
    return {
        "mae_native_usd": float(np.mean(np.abs(errors))),
        "rmse_native_usd": float(np.sqrt(np.mean(np.square(errors)))),
        "median_absolute_percentage_error": float(
            np.median(np.abs(errors)/true)),
        "quantile_pinball_native_usd": pinball,
        "coverage_80pct": float(np.mean((true >= q[0]) & (true <= q[2]))),
        "forecast_rows": len(true),
    }


def score_baselines(train, development, *, ridge_alpha=1.0):
    if any(c.target_open.year >= 2022 for c in train):
        raise ValueError("train sample leaks into development")
    if any(not 2022 <= c.target_open.year < 2026 for c in development):
        raise ValueError("only 2022–2025 development targets allowed")
    config = fit_baselines(train, ridge_alpha=ridge_alpha)
    x, anchor, actual, _ = _matrix(development)
    norm = (x - np.asarray(config["feature_mean"])) / np.asarray(
        config["feature_scale_train_only"])
    weights = np.asarray(config["ridge_weights"])
    mu = np.column_stack((np.ones(len(x)), norm)) @ weights
    persistence = _score(anchor, actual, np.zeros(len(x)),
                         config["persistence_train_sigma_log"])
    ridge = _score(anchor, actual, mu,
                   config["ridge_train_residual_sigma_log"])
    return {
        "experiment": "btc_training_only_statistical_baselines_v0.1",
        "source": "fixed user-approved private BTC/Bitstamp release",
        "train_target_before": "2022-01-01T00:00:00Z",
        "development_target_before": "2026-01-01T00:00:00Z",
        "2026_test_quarantined": True,
        "not_confirmatory": True,
        "not_hyperliquid_execution": True,
        "model_selection_using_development": False,
        "fit": config,
        "baselines": {
            "persistence": persistence,
            "ridge_three_past_only_features": ridge,
        },
    }


def run(*, interval, folder=ROOT, max_train=4096, max_dev=1024,
        stride=None):
    if interval not in ("H1", "M1"):
        raise ValueError("H1 or M1 required")
    step = 60 if interval == "M1" else 1
    if stride is not None:
        step = stride
    pools, candidates = collect(interval, Path(folder),
                                max_train=max_train, max_dev=max_dev,
                                stride=step)
    output = score_baselines(pools["train"], pools["development"])
    output["interval"] = interval
    output["scanned_candidates"] = candidates
    output["sampling_stride"] = step
    return output


def main(argv=None):
    ap = argparse.ArgumentParser(description="BTC train-only statistical controls, no trades")
    ap.add_argument("--interval", choices=("H1", "M1"), required=True)
    ap.add_argument("--directory", type=Path, default=ROOT)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    if args.output.exists():
        ap.error("refusing to overwrite existing research output")
    output = run(interval=args.interval, folder=args.directory)
    args.output.write_text(
        json.dumps(output, indent=2, allow_nan=False, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"Wrote {args.output}, exploration only (no 2026 labels)")


if __name__ == "__main__":
    main()
