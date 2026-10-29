"""Versioned S1 result panel. Consumes aggregated development JSON ONLY.

No market data, wallet, exchange credentials or trading orders. Never claims
cross-horizon comparability or identifies a statistically significant winner.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean, stdev

PRIMARY = (
    "direction_accuracy_all", "balanced_direction_accuracy",
    "mae_native_usd", "mae_bps_anchor", "absolute_magnitude_error_bps",
    "gross_signal_return_mean_bps_per_sample",
    "observed_cpu_train_seconds",
)


def _validate(source):
    if source.get("experiment") != "TRAME_S1_scaling_depth_direction_development_v1":
        raise ValueError("unknown S1 experiment format")
    if (source.get("labels_2026_opened") is not False
            or source.get("independent_test_used") is not False):
        raise ValueError("holdout or independent result must never be mixed")
    if source.get("interval") not in ("D1", "H1", "M1"):
        raise ValueError("invalid resolution")
    if source.get("data_origin") not in ("BTC_PRIVATE_REAL", "ARTIFICIAL_FIXTURE"):
        raise ValueError("missing origin")
    if (source.get("total_compute_matched") is not False or
            source.get("hyperparameter_tuning_matched") is not False):
        raise ValueError("unsubstantiated compute matching")
    if not isinstance(source.get("results"), list) or not source["results"]:
        raise ValueError("no rows")
    for row in source["results"]:
        if (row.get("architecture") not in (
            "legacy_causal_transformer", "modern_gpt_style_mini",
            "recurrent_gru_control") or
                row.get("depth") not in (1, 2, 4) or
                not isinstance(row.get("target_parameters"), int) or
                not isinstance(row.get("seed"), int) or
                not isinstance(row.get("steps"), int) or
                row.get("steps") <= 0):
            raise ValueError("invalid arm")
        for metric in PRIMARY:
            number = row.get(metric)
            if not isinstance(number, (int, float)) or not math.isfinite(number):
                raise ValueError("missing/nonfinite metric " + metric)
        for metric in ("direction_accuracy_all", "balanced_direction_accuracy"):
            if not 0 <= row[metric] <= 1:
                raise ValueError("direction accuracy out of bounds")
        for metric in ("mae_native_usd", "mae_bps_anchor",
                       "absolute_magnitude_error_bps",
                       "observed_cpu_train_seconds"):
            if row[metric] < 0:
                raise ValueError("negative loss/cost metric")
        if (row.get("n_predicted_up", 0)+row.get("n_predicted_down", 0)
                +row.get("n_predicted_flat", 0) != row.get("forecast_rows")):
            raise ValueError("sign counts do not sum to cases")


def build_panel(sources):
    if not sources:
        raise ValueError("at least one JSON source required")
    data=[]
    for source in sources:
        _validate(source)
        for row in source["results"]:
            data.append({
                "interval": source["interval"],
                "data_origin":source["data_origin"],
                "training_cases":source["training_cases"],
                "development_cases":source["development_cases"],
                **row,
            })
    grouped=defaultdict(list)
    seen=set()
    for row in data:
        key=(
            row["data_origin"],row["interval"],row["architecture"],
            row["target_parameters"],row["depth"],row["steps"],
            row["seed"],
        )
        if key in seen:
            raise ValueError("duplicate arm/seed; refusing to double count")
        seen.add(key)
        g=(key[0],key[1],key[2],key[3],key[4],key[5])
        grouped[g].append(row)
    output=[]
    for key,rows in sorted(grouped.items()):
        n=len(rows)
        if len({x["development_cases"] for x in rows}) != 1:
            raise ValueError("incomparable case counts within arm")
        result={
            "data_origin":key[0], "interval":key[1], "architecture":key[2],
            "target_parameters":key[3], "depth":key[4], "steps":key[5],
            "seeds":sorted(x["seed"] for x in rows), "n_seeds":n,
            "development_cases":rows[0]["development_cases"],
            "actual_parameter_counts":sorted({x["parameter_count"] for x in rows}),
            "magnitude_and_direction_both_required":True,
            "compute_matched":False, "independent_test":False,
        }
        for metric in PRIMARY:
            values=[r[metric] for r in rows]
            result[metric+"_mean"]=mean(values)
            result[metric+"_sd_across_seeds"]=stdev(values) if n>1 else None
        result["predicted_up_fraction_mean"]=mean(
            r["n_predicted_up"]/r["forecast_rows"] for r in rows)
        result["predicted_down_fraction_mean"]=mean(
            r["n_predicted_down"]/r["forecast_rows"] for r in rows)
        result["directional_skill_proven"]=False
        output.append(result)
    return {
        "panel":"TRAME_S1_scaling_multihorizon_development_v1",
        "no_independent_test":True,
        "no_compute_or_hyperparameter_matching":True,
        "not_cumulative_portfolio_return":True,
        "transaction_costs_ignored_by_owner":True,
        "n_rows":len(output),"n_model_fits":len(data),
        "entries":output,
    }


def to_markdown(panel):
    out=[
        "# TRAME scaling / direction / amplitude (development only)",
        "",
        "**NOT independent validation; NOT compute-matched; no trading.**",
        "Every row is one combination of horizon, family, target parameter "
        "budget, depth and training updates. Different horizons or update "
        "budgets must NOT be ranked together.",
        "",
    ]
    for interval in ("D1","H1","M1"):
        rows=[r for r in panel["entries"] if r["interval"]==interval]
        if not rows:
            continue
        out += [
            "## "+interval,
            "",
            "| Family | Target params | Depth | Updates | Seeds | "
            "Dir correct % | Balanced % | Forecast up % | "
            "MAE USD | MAE bps | Magnitude error bps | CPU training s |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for r in rows:
            val=lambda metric:r[metric+"_mean"]
            out.append(
                f"| {r['architecture']} | {r['target_parameters']} | "
                f"{r['depth']} | {r['steps']} | {r['n_seeds']} | "
                f"{100*val('direction_accuracy_all'):.2f} | "
                f"{100*val('balanced_direction_accuracy'):.2f} | "
                f"{100*r['predicted_up_fraction_mean']:.2f} | "
                f"{val('mae_native_usd'):.3f} | {val('mae_bps_anchor'):.3f} | "
                f"{val('absolute_magnitude_error_bps'):.3f} | "
                f"{val('observed_cpu_train_seconds'):.2f} |"
            )
        out += ["", "One-seed means are not evidence of convergence or statistical "
                "significance; true train/dev price series remain private.", ""]
    return "\n".join(out)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser(description="Consolidate aggregate development evidence")
    p.add_argument("--inputs",type=Path,nargs="+",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path)
    ns=p.parse_args(argv)
    paths=[ns.output]+([ns.markdown] if ns.markdown else [])
    if any(path.exists() for path in paths):
        p.error("refusing to overwrite study reports")
    inputs=[json.loads(path.read_text(encoding="utf-8")) for path in ns.inputs]
    panel=build_panel(inputs)
    ns.output.write_text(json.dumps(panel,indent=2,ensure_ascii=False,
                                    allow_nan=False)+"\n",encoding="utf-8")
    if ns.markdown:
        ns.markdown.write_text(to_markdown(panel),encoding="utf-8")


if __name__=="__main__":
    main()
