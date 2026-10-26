"""S2 paired exploratory results report, from aggregate JSON ONLY.

No trading execution; cannot rank a cross-horizon winner or claim statistical
significance. Reports must preserve direction AND magnitude, always-up/down
controls, calibration versus training-only class prior, and seed dispersion.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean, stdev


COMMON_METRICS = (
    "direction_accuracy_all", "balanced_direction_accuracy", "signal_coverage",
    "mae_native_usd", "mae_bps_anchor", "absolute_magnitude_error_bps",
    "mean_abs_predicted_move_bps", "mean_abs_actual_move_bps",
    "observed_cpu_train_seconds",
)
PAIRED_METRICS = (
    "balanced_direction_accuracy", "mae_bps_anchor", "absolute_magnitude_error_bps",
)
ALLOWED_HORIZONS = ("D1", "H1", "M1")


def validate(source):
    if source.get("experiment") != "TRAME_S2_CONTINUOUS_DIRECTION_EXPLORATORY_V1":
        raise ValueError("incorrect experiment schema")
    if source.get("interval") not in ALLOWED_HORIZONS:
        raise ValueError("unknown interval")
    if source.get("data_origin") not in ("BTC_PRIVATE_REAL", "ARTIFICIAL_FIXTURE"):
        raise ValueError("unidentified data origin")
    if (source.get("labels_2026_opened") is not False
            or source.get("independent_test_used") is not False
            or source.get("historical_base_gaussian_nll_not_comparable") is not True
            or source.get("train_only_normalization") is not True
            or source.get("total_compute_matched") is not False):
        raise ValueError("holdout / provenance / comparison contract violated")
    prior = source.get("direction_class_prior_train_only")
    if (not isinstance(prior, dict)
            or prior.get("prior_fit_on_training_only") is not True
            or not isinstance(prior.get("p_up"), float)
            or not 0 < prior["p_up"] < 1):
        raise ValueError("missing train-only direction prior")
    if not isinstance(source.get("results"), list) or not source["results"]:
        raise ValueError("no model results")
    for control in ("always_up_1bp", "always_down_1bp", "persistence_flat"):
        if not isinstance(source.get("baselines", {}).get(control), dict):
            raise ValueError("missing no-skill control " + control)
    for r in source["results"]:
        if (r.get("mode") not in ("joint", "regression")
                or r.get("depth") not in (1, 2)
                or type(r.get("width")) is not int
                or type(r.get("steps")) is not int
                or type(r.get("seed")) is not int
                or type(r.get("parameter_count")) is not int
                or type(r.get("forecast_rows")) is not int
                or r["forecast_rows"] != source.get("dev_count")
                or r["forecast_rows"] < 1):
            raise ValueError("invalid model result metadata")
        for key in COMMON_METRICS:
            val=r.get(key)
            if type(val) not in (int, float) or not math.isfinite(val):
                raise ValueError("invalid numeric metric " + key)
        if (sum(r.get(k, -100000) for k in
                ("n_predicted_up","n_predicted_down","n_predicted_flat"))
                != r["forecast_rows"]):
            raise ValueError("invalid predicted class counts")
        if (r["mode"] == "joint"
                and (r.get("binary_probabilities_from_trained_head") is not True
                     or type(r.get("brier_nonflat")) not in (int,float)
                     or type(r.get("brier_skill_vs_train_prior")) not in (int,float)
                     or not math.isfinite(r["brier_nonflat"])
                     or not math.isfinite(r["brier_skill_vs_train_prior"]))):
            raise ValueError("joint model missing calibrated direction evidence")
        if (r["mode"] == "regression"
                and (r.get("binary_probabilities_from_trained_head") is not False
                     or r.get("brier_nonflat") is not None)):
            raise ValueError("regression-only logit must not be scored as trained")


def _stat(values):
    return {"mean":float(mean(values)), "sd_across_seeds":(
        float(stdev(values)) if len(values)>1 else None)}


def build_panel(sources):
    if not sources:
        raise ValueError("no sources")
    all_rows=[]
    baselines={}
    source_info=[]
    for src in sources:
        validate(src)
        ident=(src["data_origin"],src["interval"])
        if ident in baselines:
            raise ValueError("duplicate horizon/origin source; do not double count")
        baselines[ident]=src["baselines"]
        source_info.append({
            "interval":src["interval"], "origin":src["data_origin"],
            "development_cases":src["dev_count"],
            "model_source_commit":src.get("model_source_commit"),
            "train_only_direction_prior":src["direction_class_prior_train_only"]["p_up"],
        })
        all_rows.extend([{**r,"interval":src["interval"],
                          "data_origin":src["data_origin"]} for r in src["results"]])

    index=defaultdict(list)
    seen=set()
    paired=defaultdict(dict)
    for r in all_rows:
        key=(r["data_origin"],r["interval"],r["width"],
             r["depth"],r["steps"],r["seed"],r["mode"])
        if key in seen:
            raise ValueError("duplicate seed/arm")
        seen.add(key)
        grouped=(r["data_origin"],r["interval"],r["width"],
                 r["depth"],r["steps"],r["mode"])
        index[grouped].append(r)
        pkey=(r["data_origin"],r["interval"],r["width"],
              r["depth"],r["steps"],r["seed"])
        paired[pkey][r["mode"]]=r

    summary=[]
    for key,records in sorted(index.items()):
        d={
            "data_origin":key[0], "interval":key[1],
            "width":key[2], "depth":key[3], "steps":key[4],
            "mode":key[5], "n_seeds":len(records),
            "seeds":sorted(x["seed"] for x in records),
            "parameter_counts":sorted({x["parameter_count"] for x in records}),
            "predicted_up_fraction":_stat([
                x["n_predicted_up"]/x["forecast_rows"] for x in records]),
            "predicted_down_fraction":_stat([
                x["n_predicted_down"]/x["forecast_rows"] for x in records]),
        }
        for metric in COMMON_METRICS:
            d[metric]=_stat([x[metric] for x in records])
        if key[-1]=="joint":
            d["brier_skill_vs_train_prior"]=_stat([
                x["brier_skill_vs_train_prior"] for x in records])
            d["brier_nonflat"]=_stat([x["brier_nonflat"] for x in records])
        else:
            d["brier_skill_vs_train_prior"]=None
            d["brier_nonflat"]=None
        summary.append(d)

    differences=defaultdict(list)
    for key,modes in paired.items():
        if set(modes)=={"joint","regression"}:
            j,r=modes["joint"],modes["regression"]
            family_key=key[:5]
            differences[family_key].append({
                "seed":key[5], **{
                    metric+"_delta_joint_minus_regression":j[metric]-r[metric]
                    for metric in PAIRED_METRICS}})
    paired_summary=[]
    for key,records in sorted(differences.items()):
        row={
            "data_origin":key[0], "interval":key[1],
            "width":key[2], "depth":key[3], "steps":key[4],
            "paired_seeds":sorted(r["seed"] for r in records),
            "paired_seed_count":len(records),
        }
        for metric in PAIRED_METRICS:
            label=metric+"_delta_joint_minus_regression"
            row[label]=_stat([x[label] for x in records])
        paired_summary.append(row)
    return {
        "report":"TRAME_S2_PAIRED_EXPLORATORY_V1",
        "independent_holdout_evaluated":False,
        "cross_horizon_ranking_valid":False,
        "compute_matched":False,
        "no_transaction_costs":True,
        "not_cumulative_portfolio_return":True,
        "sources":source_info,"baseline_by_horizon":[
            {
                "data_origin":ident[0],"interval":ident[1],
                "always_up_accuracy":bs["always_up_1bp"]["direction_accuracy_all"],
                "always_down_accuracy":bs["always_down_1bp"]["direction_accuracy_all"],
                "persistence_mae_usd":bs["persistence_flat"]["mae_native_usd"],
            }
            for ident,bs in sorted(baselines.items())],
        "n_model_fits":len(all_rows),"n_groups":len(summary),
        "model_summary":summary,"paired_joint_minus_regression":paired_summary,
    }


def to_markdown(panel):
    lines=[
        "# TRAME S2 - direction et amplitude, développement seulement",
        "",
        "**Aucune validation indépendante, ni avantage financier démontré.** "
        "Ne jamais classer directement des pertes D1/H1/M1 entre elles.",
        "",
    ]
    for horizon in ALLOWED_HORIZONS:
        arms=[r for r in panel["model_summary"] if r["interval"]==horizon]
        if not arms:
            continue
        base=next(r for r in panel["baseline_by_horizon"]
                  if r["interval"]==horizon and
                  r["data_origin"]==arms[0]["data_origin"])
        lines.extend([
            "## "+horizon,
            "",
            f"Témoin toujours hausse : {base['always_up_accuracy']*100:.2f} % ; "
            f"toujours baisse : {base['always_down_accuracy']*100:.2f} %.",
            "",
            "| Mode | Width | Layers | Steps | Seeds | Direction % | Balanced % | "
            "Up predictions % | MAE USD | MAE bps | Magnitude err. bps | "
            "Brier skill vs train prior |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for r in arms:
            val=lambda metric: r[metric]["mean"]
            brier=(f"{r['brier_skill_vs_train_prior']['mean']:.3f}"
                   if r["brier_skill_vs_train_prior"] is not None else "N/A")
            lines.append(
                f"| {r['mode']} | {r['width']} | {r['depth']} | {r['steps']} | "
                f"{r['n_seeds']} | {val('direction_accuracy_all')*100:.2f} | "
                f"{val('balanced_direction_accuracy')*100:.2f} | "
                f"{r['predicted_up_fraction']['mean']*100:.2f} | "
                f"{val('mae_native_usd'):.2f} | {val('mae_bps_anchor'):.2f} | "
                f"{val('absolute_magnitude_error_bps'):.2f} | {brier} |"
            )
        lines.extend(["", "Paired joint-versus-regression delta: negative error "
                      "is good; positive balanced accuracy is good. "
                      "No significance claim without per-origin paired evidence.", ""])
    return "\n".join(lines)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser(description="Summarize aggregated S2 research JSON only")
    p.add_argument("--inputs",nargs="+",type=Path,required=True)
    p.add_argument("--json",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    opts=p.parse_args(argv)
    if opts.json.exists() or opts.markdown.exists():
        p.error("will not overwrite evidence")
    src=[json.loads(path.read_text(encoding="utf-8")) for path in opts.inputs]
    panel=build_panel(src)
    opts.json.write_text(json.dumps(panel,indent=2,allow_nan=False)+"\n",
                         encoding="utf-8")
    opts.markdown.write_text(to_markdown(panel),encoding="utf-8")


if __name__=="__main__":
    main()
