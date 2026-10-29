"""S2 direction probability diagnostics with TRAIN-ONLY reference class prior.

All metrics are observational, never a trading rule. Flat actual prices are
excluded from the binary probability evaluation and their count is retained.
"""
from __future__ import annotations

import math

import numpy as np


def prior_from_train(train_cases):
    """Jeffreys-smoothed P(up | nonflat), using training LABELS only."""
    anchors = np.asarray([x.anchor_usd for x in train_cases], dtype=float)
    actuals = np.asarray([x.target_usd for x in train_cases], dtype=float)
    if not len(anchors) or not np.all(np.isfinite(anchors)) or not np.all(np.isfinite(actuals)):
        raise ValueError("nonempty finite training anchors and closes required")
    if np.any(anchors <= 0) or np.any(actuals <= 0):
        raise ValueError("positive training prices required")
    active = actuals != anchors
    count = int(np.sum(active))
    if count < 1:
        raise ValueError("cannot estimate a binary direction prior from all-flat training")
    up = int(np.sum(actuals[active] > anchors[active]))
    return {"p_up": float((up + 0.5) / (count + 1.0)),
            "nonflat_train_count": count, "up_train_count": up,
            "prior_fit_on_training_only": True,
            "smoothing": "Jeffreys Beta(0.5, 0.5)"}


def probability_report(anchors, actuals, probabilities, *, train_prior):
    """Brier/CE relative to train prior; no post-hoc threshold tuning."""
    a, y, p = [np.asarray(v, dtype=float) for v in (anchors, actuals, probabilities)]
    if (a.ndim != 1 or a.size == 0 or y.shape != a.shape or p.shape != a.shape
            or not np.isfinite(a).all() or not np.isfinite(y).all()
            or not np.isfinite(p).all() or np.any(a <= 0) or np.any(y <= 0)
            or np.any((p < 0) | (p > 1))):
        raise ValueError("finite aligned prices and probabilities in [0, 1] needed")
    if (not isinstance(train_prior, dict)
            or train_prior.get("prior_fit_on_training_only") is not True
            or not isinstance(train_prior.get("p_up"), float)
            or not 0.0 < train_prior["p_up"] < 1.0):
        raise ValueError("valid train-only probability prior required")

    active = y != a
    count = int(np.sum(active))
    result = {
        "nonflat_probability_cases": count,
        "flat_probability_cases_excluded": int(np.sum(~active)),
        "binary_probabilities_from_trained_head": True,
        "train_only_prior_up": train_prior["p_up"],
    }
    if count == 0:
        return {**result, "brier_nonflat": None, "binary_ce_nonflat": None,
                "brier_train_prior_nonflat": None, "binary_ce_train_prior_nonflat": None,
                "brier_skill_vs_train_prior": None,
                "binary_ce_delta_vs_train_prior": None,
                "predicted_up_probability_mean": None, "reliability_bins": []}

    true_up = (y[active] > a[active]).astype(float)
    pred = p[active]
    prior = train_prior["p_up"]
    eps = 1e-12
    brier = float(np.mean((pred - true_up) ** 2))
    base_brier = float(np.mean((prior - true_up) ** 2))
    clipped = np.clip(pred, eps, 1 - eps)
    ce = float(np.mean(-true_up * np.log(clipped) - (1 - true_up) * np.log(1 - clipped)))
    base_ce = float(np.mean(-true_up * math.log(prior) - (1 - true_up) * math.log(1 - prior)))

    bins = []
    # Fixed edges preregistered ex ante; bin information never drives trades.
    for i, (lo, hi) in enumerate(zip(np.linspace(0, 1, 6)[:-1],
                                      np.linspace(0, 1, 6)[1:])):
        mask = (pred >= lo) & (pred <= hi if i == 4 else pred < hi)
        n = int(np.sum(mask))
        bins.append({"lower_inclusive": float(lo), "upper_inclusive_if_last": float(hi),
                     "count": n, "mean_predicted_p_up": float(np.mean(pred[mask])) if n else None,
                     "empirical_up_frequency": float(np.mean(true_up[mask])) if n else None})
    return {**result,
            "brier_nonflat": brier,
            "binary_ce_nonflat": ce,
            "brier_train_prior_nonflat": base_brier,
            "binary_ce_train_prior_nonflat": base_ce,
            "brier_skill_vs_train_prior": 1.0 - brier / base_brier if base_brier > 0 else None,
            "binary_ce_delta_vs_train_prior": ce - base_ce,
            "predicted_up_probability_mean": float(np.mean(pred)),
            "reliability_bins": bins}
