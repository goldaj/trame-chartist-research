"""S2b paired (continuous - legacy quantized) synthetic/aggregate report.

No private BTC rows, portfolio return, wallet, or exchange calls.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

from research.representation_ablation.runner import REPRESENTATIONS, MODES


PAIRED = (
    "direction_accuracy_all", "balanced_direction_accuracy",
    "mae_native_usd", "mae_bps_anchor",
    "absolute_magnitude_error_bps", "observed_cpu_train_seconds",
)


def _stat(values):
    return {"mean":float(mean(values)),
            "sd_across_seeds":float(stdev(values)) if len(values)>1 else None}


def validate(report):
    if report.get("experiment")!="TRAME_S2B_REPRESENTATION_ABLATION_V1":
        raise ValueError("not an S2b ablation report")
    if (report.get("interval") not in ("D1","H1","M1")
            or report.get("labels_2026_opened") is not False
            or report.get("independent_test_used") is not False
            or report.get("same_target_normalization_all_representations") is not True
            or report.get("same_input_normalization_all_representations") is not True
            or report.get("compute_matched") is not False
            or report.get("common_batch_indices_per_seed") is not True
            or report.get("data_origin") not in ("BTC_PRIVATE_REAL","ARTIFICIAL_FIXTURE")):
        raise ValueError("invalid chronology or comparison contract")
    if report.get("data_origin")=="BTC_PRIVATE_REAL":
        code=report.get("model_source_commit","")
        if len(code)!=40 or any(c not in "0123456789abcdef" for c in code):
            raise ValueError("model source SHA missing")
    for control in ("persistence_flat","always_up_1bp","always_down_1bp",
                    "mean_log_return_train_only","ridge_train_only"):
        if not isinstance(report.get("baseline_scores",{}).get(control),dict):
            raise ValueError("missing no-skill baseline")
    if not report.get("results") or not isinstance(report["results"],list):
        raise ValueError("no model results")
    for row in report["results"]:
        if (row.get("representation") not in REPRESENTATIONS
                or row.get("mode") not in MODES
                or row.get("depth") not in (1,2)
                or type(row.get("width")) is not int
                or type(row.get("seed")) is not int
                or type(row.get("steps")) is not int
                or type(row.get("parameter_count")) is not int
                or type(row.get("forecast_rows")) is not int
                or row["forecast_rows"]!=report.get("dev_count")):
            raise ValueError("invalid fitted-arm metadata")
        if (type(row.get("initial_state_sha256")) is not str
                or len(row["initial_state_sha256"])!=64):
            raise ValueError("initial model weights fingerprint missing")
        if sum(row.get(k, -9999999) for k in (
                "n_predicted_up","n_predicted_down","n_predicted_flat")) != row["forecast_rows"]:
            raise ValueError("bad direction counts")
        for key in PAIRED:
            x=row.get(key)
            if type(x) not in (int,float) or not math.isfinite(x):
                raise ValueError("non-finite "+key)
        for key in ("direction_accuracy_all","balanced_direction_accuracy"):
            if not 0<=row[key]<=1:
                raise ValueError("direction score out of bounds")


def build_panel(reports):
    if not reports:
        raise ValueError("input report required")
    seen_horizon=set()
    group=defaultdict(list)
    baselines=[]
    n_fits=0
    for source in reports:
        validate(source)
        ident=(source["data_origin"],source["interval"])
        if ident in seen_horizon:
            raise ValueError("duplicate horizon report")
        seen_horizon.add(ident)
        baselines.append({
            "data_origin":ident[0],"interval":ident[1],
            "always_up_direction_accuracy":source["baseline_scores"]["always_up_1bp"]["direction_accuracy_all"],
            "always_down_direction_accuracy":source["baseline_scores"]["always_down_1bp"]["direction_accuracy_all"],
            "persistence_mae_bps":source["baseline_scores"]["persistence_flat"]["mae_bps_anchor"],
            "mean_drift_mae_bps":source["baseline_scores"]["mean_log_return_train_only"]["mae_bps_anchor"],
            "dev_origins_sha256":source["development_origins_sha256"],
            "train_origins_sha256":source["train_origins_sha256"],
        })
        current=set()
        for row in source["results"]:
            key=(row["width"],row["depth"],row["mode"],row["seed"],
                 row["steps"],row["representation"])
            if key in current:
                raise ValueError("duplicate arm/seed")
            current.add(key)
            group[(ident[0],ident[1],row["width"],row["depth"],
                   row["mode"],row["steps"],row["seed"])].append(row)
            n_fits+=1

    grouped=defaultdict(list)
    for key,rows in group.items():
        if len(rows)!=2 or {r["representation"] for r in rows}!=set(REPRESENTATIONS):
            raise ValueError("comparison requires BOTH paired representations for every seed")
        continuous=next(r for r in rows if r["representation"]=="continuous_bps")
        quantized=next(r for r in rows if r["representation"]=="legacy_quantized_bps")
        if (continuous["initial_state_sha256"]!=quantized["initial_state_sha256"]
                or continuous["parameter_count"]!=quantized["parameter_count"]
                or continuous["input_normalizer_std_bps"]!=quantized["input_normalizer_std_bps"]
                or continuous["target_normalizer_std_bps_common"]!=quantized["target_normalizer_std_bps_common"]):
            raise ValueError("not matched initialization/model/target")
        delta={metric:continuous[metric]-quantized[metric] for metric in PAIRED}
        grouped[key[:6]].append({
            "seed":key[6],
            "quantized":quantized,"continuous":continuous,
            "delta":delta,
        })

    rows=[]
    for key,pairs in sorted(grouped.items()):
        d={"data_origin":key[0],"interval":key[1],
           "width":key[2],"depth":key[3],
           "mode":key[4],"steps":key[5],
           "n_seeds":len(pairs),"seeds":sorted(r["seed"] for r in pairs)}
        for metric in PAIRED:
            d[metric+"_quantized"]=_stat([r["quantized"][metric] for r in pairs])
            d[metric+"_continuous"]=_stat([r["continuous"][metric] for r in pairs])
            d[metric+"_delta_continuous_minus_quantized"]=_stat(
                [r["delta"][metric] for r in pairs])
        d["predicted_up_fraction_quantized"]=_stat([
            r["quantized"]["n_predicted_up"]/r["quantized"]["forecast_rows"] for r in pairs])
        d["predicted_up_fraction_continuous"]=_stat([
            r["continuous"]["n_predicted_up"]/r["continuous"]["forecast_rows"] for r in pairs])
        if key[4]=="joint":
            for rep in ("quantized","continuous"):
                d["brier_skill_"+rep]=_stat([
                    r[rep]["brier_skill_vs_train_prior"] for r in pairs])
        rows.append(d)

    return {"report":"TRAME_S2B_PAIRED_COMPARISON_V1",
            "independent_test":False,"cross_horizon_rank_valid":False,
            "compute_matched":False,"costs_ignored":True,
            "not_cumulative_portfolio_return":True,
            "n_fits":n_fits,"baselines":baselines,"groups":rows}


def to_markdown(panel):
    lines=["# TRAME S2b : impact du seul encodage (exploratoire)","",
           "**Aucune preuve de trading ; labels 2026 non utilisés.**",
           "Valeur positive du delta accuracy : meilleur en continu ; "
           "valeur négative du delta erreur : meilleur en continu.",""]
    for horizon in ("D1","H1","M1"):
        subset=[x for x in panel["groups"] if x["interval"]==horizon]
        if not subset:
            continue
        lines.extend([
            "## "+horizon,"",
            "| Width | Depth | Loss | Steps | Seeds | Δ balanced (pp) | "
            "Δ MAE (bps) | Δ amplitude (bps) | P(up) quant. % | P(up) continu % |",
            "|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|"])
        for row in subset:
            v=lambda k:row[k+"_delta_continuous_minus_quantized"]["mean"]
            lines.append(
                f"| {row['width']} | {row['depth']} | {row['mode']} | "
                f"{row['steps']} | {row['n_seeds']} | "
                f"{100*v('balanced_direction_accuracy'):.2f} | "
                f"{v('mae_bps_anchor'):.3f} | "
                f"{v('absolute_magnitude_error_bps'):.3f} | "
                f"{100*row['predicted_up_fraction_quantized']['mean']:.2f} | "
                f"{100*row['predicted_up_fraction_continuous']['mean']:.2f} |")
        lines+=["","Les groupes partagent uniquement le calendrier de "
                "développement d'un même horizon ; aucune preuve "
                "indépendante ni FLOP-matching.",""]
    return "\n".join(lines)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser(description="S2b paired aggregate JSON panel")
    p.add_argument("--inputs",type=Path,nargs="+",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    x=p.parse_args(argv)
    if x.output.exists() or x.markdown.exists():
        p.error("refusing to overwrite report")
    report=build_panel([json.loads(pth.read_text(encoding="utf-8"))
                        for pth in x.inputs])
    x.output.write_text(json.dumps(report,indent=2,
                                   allow_nan=False)+"\n",encoding="utf-8")
    x.markdown.write_text(to_markdown(report),encoding="utf-8")


if __name__=="__main__":
    main()
