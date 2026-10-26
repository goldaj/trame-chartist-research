"""S1.5 BTC scaling × depth experimental runner (research only).

Same fixed train/development BTC examples for every arm. Never reads 2026
targets, never sends orders, never downloads a dataset unless the caller
explicitly invokes the existing private-release cache handler via collect().
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import time

import numpy as np
import torch

from research.btc_h1_m1.experiment import collect
from research.btc_h1_m1.stream import ROOT
from research.btc_h1_m1.statistical_baselines import fit_baselines, _matrix
from research.p1b0_numerics.torch_head import log_interval_mass
from research.scaling_study.metrics import (
    score_forecasts, training_magnitude_thresholds, baseline_forecasts,
)
from research.scaling_study.models import (
    FAMILIES, TARGET_PARAMETERS, DEPTHS, capacity_grid,
)


def _validate_chronology(train, development):
    if not train or not development:
        raise ValueError("both train and development must be present")
    for case in train:
        if (case.target_open.year >= 2022 or
                case.decision_time >= case.label_available_time or
                case.target_open >= case.label_available_time):
            raise ValueError("training label leaks outside permitted chronology")
    for case in development:
        if (not 2022 <= case.target_open.year <= 2025 or
                case.decision_time >= case.label_available_time or
                case.target_open >= case.label_available_time):
            raise ValueError("development label outside 2022..2025")


def _device_price_arrays(cases):
    anchors = np.asarray([case.anchor_usd for case in cases], dtype=float)
    actuals = np.asarray([case.target_usd for case in cases], dtype=float)
    return anchors, actuals


def _evaluate_model(model, cases, *, batch_size=64):
    model.eval()
    prices = []
    nll_sum = 0.0
    with torch.no_grad():
        for start in range(0, len(cases), batch_size):
            batch = cases[start:start + batch_size]
            past = torch.tensor([case.encoded_past for case in batch],
                                dtype=torch.float64)
            codes = torch.tensor([case.encoded_target for case in batch],
                                 dtype=torch.float64)
            mu, sigma = model(past)
            ll = log_interval_mass(codes, mu[:, -1], sigma[:, -1])
            if not bool(torch.isfinite(ll).all()):
                raise ArithmeticError("nonfinite likelihood")
            last_mu = mu[:, -1].detach().cpu().numpy()
            anchor, _ = _device_price_arrays(batch)
            prices.extend((anchor * np.exp(last_mu / 1000.0)).tolist())
            nll_sum += float((-ll).sum())
    return np.asarray(prices, dtype=float), nll_sum / len(cases)


def _ridge_forecasts(train, dev):
    params = fit_baselines(train)
    x, anchors, _actuals, _target = _matrix(dev)
    mu = np.column_stack((
        np.ones(len(x)),
        (x - np.asarray(params["feature_mean"])) /
        np.asarray(params["feature_scale_train_only"]),
    )) @ np.asarray(params["ridge_weights"])
    return anchors * np.exp(mu)


def run_cases(train, development, *, interval, targets=TARGET_PARAMETERS,
              depths=DEPTHS, architectures=tuple(FAMILIES), steps=40,
              seeds=(20261025, 20261026, 20261027),
              max_width=704, batch_size=16, data_origin="ARTIFICIAL_FIXTURE"):
    """Execute a paired *development-only* matrix from already-collected cases."""
    if interval not in ("H1", "M1"):
        raise ValueError("H1/M1 only")
    if data_origin not in ("ARTIFICIAL_FIXTURE", "BTC_PRIVATE_REAL"):
        raise ValueError("unsupported data origin")
    if (type(steps) is not int or not 1 <= steps <= 2000
            or type(batch_size) is not int or not 1 <= batch_size <= 256
            or not isinstance(seeds, (tuple, list)) or not 1 <= len(seeds) <= 10
            or any(type(x) is not int for x in seeds) or len(set(seeds)) != len(seeds)):
        raise ValueError("invalid steps, batch or seed list")
    _validate_chronology(train, development)
    if len(train) < 32 or len(development) < 16:
        raise ValueError("minimum train/dev cases: 32/16")
    # No GPU claims: float64 CPU is the explicit initial backend.
    torch.set_num_threads(1)
    plan = capacity_grid(targets=tuple(targets), depths=tuple(depths),
                         families=tuple(architectures), width_max=max_width)
    a, y = _device_price_arrays(development)
    thresholds = training_magnitude_thresholds(train)
    baseline = {}
    for name, values in baseline_forecasts(development).items():
        baseline[name] = score_forecasts(a, y, values, train_thresholds=thresholds)
    baseline["ridge_train_only"] = score_forecasts(
        a, y, _ridge_forecasts(train, development), train_thresholds=thresholds)

    xtrain = torch.as_tensor(
        np.asarray([c.encoded_past for c in train], dtype=np.float64))
    ytrain = torch.as_tensor(
        np.asarray([c.encoded_target for c in train], dtype=np.float64))
    rows = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        shared_batches = [rng.integers(0, len(train), size=batch_size)
                          for _ in range(steps)]
        for arm in plan:
            torch.manual_seed(seed)
            model = FAMILIES[arm["architecture"]](
                width=arm["width"], depth=arm["depth"], length=20)
            actual_parameters = sum(p.numel() for p in model.parameters())
            if actual_parameters != arm["parameter_count"]:
                raise AssertionError("parameter count formula mismatch")
            optimizer = torch.optim.AdamW(
                model.parameters(), lr=0.003, weight_decay=0.001)
            model.train()
            started = time.perf_counter()
            last_loss = None
            for indices in shared_batches:
                optimizer.zero_grad(set_to_none=True)
                mu, sigma = model(xtrain[indices])
                loss = -log_interval_mass(
                    ytrain[indices], mu[:, -1], sigma[:, -1]).mean()
                if not bool(torch.isfinite(loss)):
                    raise ArithmeticError("nonfinite train loss")
                loss.backward()
                norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
                if not bool(torch.isfinite(norm)):
                    raise ArithmeticError("nonfinite gradient")
                optimizer.step()
                last_loss = float(loss.detach())
            train_elapsed = time.perf_counter() - started
            evaluated, dev_nll = _evaluate_model(model, development)
            _, train_early_nll = _evaluate_model(model, train[:min(64, len(train))])
            stats = score_forecasts(a, y, evaluated, train_thresholds=thresholds)
            rows.append({
                **arm, "seed": seed, "steps": steps, "batch_size": batch_size,
                "observed_cpu_train_seconds": train_elapsed,
                "last_minibatch_nll": last_loss,
                "development_nll": float(dev_nll),
                "train_first64_nll": float(train_early_nll),
                **stats,
            })
    return {
        "experiment": "TRAME_S1_scaling_depth_direction_development_v1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "interval": interval,
        "source": ("private approved BTC Bitstamp release" if data_origin == "BTC_PRIVATE_REAL"
                   else "artificial test fixtures only"),
        "data_origin": data_origin,
        "split_train_targets_before": "2022-01-01",
        "split_development_targets": "2022-2025",
        "independent_test_used": False, "labels_2026_opened": False,
        "not_hyperliquid_execution": True,
        "financial_production_validated": False,
        "synthesized_or_mocked_data": data_origin != "BTC_PRIVATE_REAL",
        "not_cumulative_portfolio_return": True,
        "transaction_costs_ignored_on_user_instruction": True,
        "fixed_scale_integer_log_return_encoder": 1000,
        "representation_can_erase_tiny_directional_moves": True,
        "training_cases": len(train), "development_cases": len(development),
        "architecture_grid": plan, "seed_count": len(seeds),
        "shared_batches_within_seed": True,
        "total_compute_matched": False, "hyperparameter_tuning_matched": False,
        "training_steps": steps, "batch_size": batch_size,
        "train_only_signal_thresholds": thresholds,
        "baselines": baseline, "results": rows,
        "python_version": platform.python_version(),
        "torch_version": torch.__version__,
        "git_sha": os.environ.get("GITHUB_SHA", "not recorded outside CI"),
    }


def run_history(*, interval, directory=ROOT, targets=TARGET_PARAMETERS,
                depths=DEPTHS, architectures=tuple(FAMILIES), steps=40,
                seeds=(20261025, 20261026, 20261027),
                max_train=4096, max_dev=1024, stride=None):
    if interval not in ("H1", "M1"):
        raise ValueError("H1/M1 only")
    step = (60 if interval == "M1" else 1) if stride is None else stride
    pools, scanned = collect(
        interval, Path(directory), max_train=max_train, max_dev=max_dev,
        stride=step)
    result = run_cases(
        pools["train"], pools["development"], interval=interval,
        targets=targets, depths=depths, architectures=architectures,
        steps=steps, seeds=seeds, data_origin="BTC_PRIVATE_REAL")
    result["sampling_stride"] = step
    result["scanned_candidate_origins"] = scanned
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="TRAME S1 offline BTC development, no orders, no 2026 labels")
    parser.add_argument("--interval", choices=("H1", "M1"), required=True)
    parser.add_argument("--directory", type=Path, default=ROOT)
    parser.add_argument("--targets", type=int, nargs="+", default=list(TARGET_PARAMETERS))
    parser.add_argument("--depths", type=int, nargs="+", default=list(DEPTHS))
    parser.add_argument("--architectures", choices=tuple(FAMILIES), nargs="+",
                        default=list(FAMILIES))
    parser.add_argument("--seeds", type=int, nargs="+",
                        default=[20261025, 20261026, 20261027])
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--max-train", type=int, default=4096)
    parser.add_argument("--max-dev", type=int, default=1024)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args(argv)
    if args.plan_only:
        print(json.dumps({
            "grid": capacity_grid(
                targets=tuple(args.targets), depths=tuple(args.depths),
                families=tuple(args.architectures)),
            "never_downloads_data": True, "not_a_prediction_result": True,
        }, indent=2))
        return
    if args.output is None:
        parser.error("--output is required for running training")
    if args.output.exists():
        parser.error("refusing to overwrite an existing research output")
    output = run_history(
        interval=args.interval, directory=args.directory,
        targets=tuple(args.targets), depths=tuple(args.depths),
        architectures=tuple(args.architectures), seeds=tuple(args.seeds),
        steps=args.steps, max_train=args.max_train, max_dev=args.max_dev)
    args.output.write_text(
        json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8")
    print("Research JSON written. Exploratory: not trading nor independent test.")


if __name__ == "__main__":
    main()
