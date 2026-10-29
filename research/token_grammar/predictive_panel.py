"""S3.1A matched grammar comparison from aggregate reports only."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean, stdev

from research.token_grammar.predictive import GRAMMARS

METRICS=("direction_accuracy_all","balanced_direction_accuracy",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps")
REFERENCE="continuous_bps"


def _stat(v):
    return {"mean":float(mean(v)),
            "sd_across_fits":float(stdev(v)) if len(v)>1 else None,
            "n":len(v)}


def validate(source):
    if (source.get("experiment")!="TRAME_S3_1A_PREDICTIVE_GRAMMAR_V1"
        or source.get("interval") not in ("D1","H1","M1")
        or source.get("data_origin") not in ("BTC_PUBLIC_REAL","ARTIFICIAL_FIXTURE")
        or source.get("labels_2026_opened") is not False
        or source.get("independent_test_used") is not False
        or source.get("same_input_normalization_all_representations") is not True
        or source.get("same_target_normalization_all_representations") is not True
        or source.get("common_batch_indices_per_seed") is not True
        or source.get("grammar_stage")!="decoded_scalar_ablation_NO_LEARNED_TOKEN_EMBEDDINGS"
        or source.get("quantile_fit_on")!="TRAIN_PAST_CONTEXTS_ONLY"):
        raise ValueError("S3 experiment provenance, causality, or matching invalid")
    if source["data_origin"]=="BTC_PUBLIC_REAL":
        sha=source.get("model_source_commit","")
        if len(sha)!=40 or any(x not in "0123456789abcdef" for x in sha):
            raise ValueError("unverifiable model SHA")
    if not source.get("results"):
        raise ValueError("empty S3 results")
    if not source.get("baseline_scores",{}).get("persistence_flat"):
        raise ValueError("missing persistence reference")
    for r in source["results"]:
        if (r.get("representation") not in GRAMMARS
                or r.get("mode") not in ("regression","joint")
                or type(r.get("seed")) is not int
                or type(r.get("width")) is not int
                or type(r.get("depth")) is not int
                or type(r.get("steps")) is not int
                or type(r.get("forecast_rows")) is not int
                or r["forecast_rows"]!=source.get("dev_count")
                or len(r.get("initial_state_sha256",""))!=64):
            raise ValueError("malformed trained grammar arm")
        for key in METRICS:
            if type(r.get(key)) not in (int,float) or not math.isfinite(r[key]):
                raise ValueError(f"nonfinite {key}")
        if not (0<=r["balanced_direction_accuracy"]<=1
                and 0<=r["direction_accuracy_all"]<=1):
            raise ValueError("impossible direction score")
        if r["mode"]=="joint" and (
            r.get("binary_probabilities_from_trained_head") is not True
            or not isinstance(r.get("brier_skill_vs_train_prior"),float)
            or not math.isfinite(r["brier_skill_vs_train_prior"])):
            raise ValueError("joint head lacks probability evaluation")
        if r["mode"]=="regression" and (
            r.get("binary_probabilities_from_trained_head") is not False
            or r.get("brier_nonflat") is not None):
            raise ValueError("untrained head claimed as classifier")


def build_panel(sources):
    seen_horizons=set()
    pairs=defaultdict(dict)
    strata=defaultdict(list)
    cohorts=[]
    for source in sources:
        validate(source)
        key=(source["data_origin"],source["interval"])
        if key in seen_horizons:
            raise ValueError("duplicate resolution")
        seen_horizons.add(key)
        cohorts.append({
            "origin":key[0],"interval":key[1],
            "train_count":source["train_count"],
            "dev_count":source["dev_count"],
            "train_dates_sha256":source["train_origins_sha256"],
            "dev_dates_sha256":source["development_origins_sha256"],
            "source_commit":source["model_source_commit"],
            "quantile_boundaries_train_bps":source["quantile_boundaries_bps"],
            "persistence_mae_bps":source["baseline_scores"]["persistence_flat"]["mae_bps_anchor"]
        })
        for r in source["results"]:
            arm=(key[0],key[1],r["seed"],r["mode"],r["width"],
                 r["depth"],r["steps"])
            name=r["representation"]
            if name in pairs[arm]:
                raise ValueError("duplicate arm")
            pairs[arm][name]=r
            strata[(key[0],key[1],r["mode"],name)].append(r)
    deltas=defaultdict(list)
    for key,arms in pairs.items():
        if set(arms)!=set(GRAMMARS):
            raise ValueError("missing matched grammar within one seed/config")
        conditions={(r["initial_state_sha256"],r["parameter_count"],
                     r["input_normalizer_std_bps"],
                     r["target_normalizer_std_bps_common"],
                     r["forecast_rows"]) for r in arms.values()}
        if len(conditions)!=1:
            raise ValueError("mismatched initialisation/architecture/normalization")
        base=arms[REFERENCE]
        for name,r in arms.items():
            if name==REFERENCE:
                continue
            diff={metric:r[metric]-base[metric] for metric in METRICS}
            deltas[(key[0],key[1],key[3],name)].append(diff)
    groups=[]
    for key,rows in sorted(strata.items()):
        record={
            "origin":key[0],"interval":key[1],
            "mode":key[2],"grammar":key[3],
            "n_fits":len(rows),
            "n_unique_seeds":len({r["seed"] for r in rows}),
            "predicted_up_percent":_stat([
                100*r["n_predicted_up"]/r["forecast_rows"] for r in rows]),
            "monoclasse_99pct_fits":sum(
                max(r["n_predicted_up"],r["n_predicted_down"])
                /r["forecast_rows"]>=.99 for r in rows),
            "parameter_count_values":sorted({r["parameter_count"] for r in rows}),
        }
        for m in METRICS:
            record[m]=_stat([r[m] for r in rows])
        if key[2]=="joint":
            record["brier_skill_vs_train_prior"]=_stat([
                r["brier_skill_vs_train_prior"] for r in rows])
        else:
            record["brier_skill_vs_train_prior"]=None
        groups.append(record)
    comparative=[]
    for key,values in sorted(deltas.items()):
        entry={"origin":key[0],"interval":key[1],
               "mode":key[2],"grammar":key[3],
               "baseline":REFERENCE,"paired_fits":len(values)}
        for m in METRICS:
            entry[m+"_delta_grammar_minus_continuous"]=_stat([
                row[m] for row in values])
        comparative.append(entry)
    return {
        "report":"TRAME_S3_1A_DECODED_GRAMMAR_COMPARISON_V1",
        "n_fits":sum(len(v) for v in pairs.values()),
        "paired_groups":len(pairs),
        "independent_test":False,"labels_2026_opened":False,
        "no_portfolio_return":True,
        "not_a_categorical_embedding_study":True,
        "cohorts":cohorts,"summary":groups,
        "paired_deltas":comparative,
        "note":"3 seeds share the same temporal development data. Seed SD is not a sampling CI. No significance or real-trading claim.",
    }


def to_markdown(panel):
    out=["# TRAME S3.1A : représentations historiques décodées",
         "", "**Résultats de développement, 2026 réservé. Aucune valeur de trading démontrée.**",
         "G1/G2 tokens sont décodés en scalaire : ceci n'évalue pas d'embeddings appris.",""]
    for horizon in ("D1","H1","M1"):
        data=[x for x in panel["summary"] if x["interval"]==horizon]
        if not data:continue
        out+=["## "+horizon,"",
             "| Objectif | Grammaire | Fits | BA % | Acc. % | MAE $ | MAE bps | Erreur amplitude bps | Hausses % | Monoclasse / fits | Brier skill |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for x in data:
            met=lambda k:x[k]["mean"]
            brier="n/a" if x["brier_skill_vs_train_prior"] is None else f"{met('brier_skill_vs_train_prior'):.5f}"
            out.append(f"| {x['mode']} | {x['grammar']} | {x['n_fits']} | "
                       f"{100*met('balanced_direction_accuracy'):.2f} | "
                       f"{100*met('direction_accuracy_all'):.2f} | "
                       f"{met('mae_native_usd'):.2f} | {met('mae_bps_anchor'):.3f} | "
                       f"{met('absolute_magnitude_error_bps'):.3f} | "
                       f"{met('predicted_up_percent'):.1f} | "
                       f"{x['monoclasse_99pct_fits']}/{x['n_fits']} | {brier} |")
        out+=["", "Les deltas appariés complets, par graine/architecture/objectif, sont dans le JSON.",""]
    return "\n".join(out)+"\n"


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--inputs",type=Path,nargs="+",required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--markdown",type=Path,required=True)
    a=parser.parse_args(argv)
    if a.output.exists() or a.markdown.exists():
        parser.error("refusing to overwrite evidence")
    panel=build_panel([json.loads(p.read_text(encoding="utf-8")) for p in a.inputs])
    a.output.write_text(json.dumps(panel,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    a.markdown.write_text(to_markdown(panel),encoding="utf-8")


if __name__=="__main__":
    main()
