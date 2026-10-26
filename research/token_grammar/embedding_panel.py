"""S3.1B aggregate paired learned-token vs decoded-scalar report."""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev
from research.token_grammar.token_embeddings import ARMS

METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps")
COMPARISONS=(("g1_learned_token","g1_decoded_scalar"),
             ("g2_learned_token","g2_decoded_scalar"),
             ("g1_learned_token","continuous_scalar"),
             ("g2_learned_token","continuous_scalar"))


def _stat(xs):
    return {"mean":float(mean(xs)),
            "sd_between_fits":float(stdev(xs)) if len(xs)>1 else None,
            "n_fits":len(xs)}


def validate(d):
    if (d.get("experiment")!="TRAME_S3_1B_TRUE_TOKEN_EMBEDDING_V1"
            or d.get("interval") not in ("D1","H1","M1")
            or d.get("data_origin") not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL")
            or d.get("labels_2026_opened") is not False
            or d.get("independent_test_used") is not False
            or d.get("same_architecture_all_arms") is not True
            or d.get("same_target_scale_all_arms") is not True
            or d.get("quantile_fit_on_train_only") is not True
            or d.get("common_minibatches_per_seed") is not True
            or d.get("vocab_size_all_arms")!=11
            or not d.get("results")):
        raise ValueError("invalid model/data/holdout contract")
    if d["data_origin"]=="BTC_PUBLIC_REAL":
        sha=d.get("model_source_commit","")
        if len(sha)!=40 or not all(x in "0123456789abcdef" for x in sha):
            raise ValueError("real model code SHA unavailable")
    if "persistence_flat" not in d.get("baselines",{}):
        raise ValueError("persistence baseline missing")
    for r in d["results"]:
        if (r.get("arm") not in ARMS or r.get("mode") not in ("regression","joint")
                or type(r.get("seed")) is not int or type(r.get("width")) is not int
                or r.get("depth") not in (1,2) or type(r.get("steps")) is not int
                or len(r.get("initial_state_sha256",""))!=64
                or r.get("trainable_embedding") is not True
                or r.get("token_vocab_size")!=11
                or r.get("forecast_rows")!=d.get("dev_count")):
            raise ValueError("invalid arm configuration or provenance")
        for m in METRICS:
            v=r.get(m)
            if type(v) not in (int,float) or not math.isfinite(v):
                raise ValueError("nonfinite metric "+m)
        if not (0<=r["balanced_direction_accuracy"]<=1 and
                0<=r["direction_accuracy_all"]<=1):
            raise ValueError("direction accuracy outside interval")
        if r["mode"]=="joint":
            if (r.get("binary_probabilities_from_trained_head") is not True
                    or type(r.get("brier_skill_vs_train_prior")) not in (int,float)
                    or not math.isfinite(r["brier_skill_vs_train_prior"])):
                raise ValueError("no trained probability-head score")
        else:
            if (r.get("binary_probabilities_from_trained_head") is not False
                    or r.get("brier_nonflat") is not None):
                raise ValueError("untrained classification logits were scored")


def build_panel(sources):
    if not sources:
        raise ValueError("no reports")
    by_key=defaultdict(dict)
    allrows=defaultdict(list)
    cohorts=[]
    seen=set()
    for d in sources:
        validate(d)
        origin=d["data_origin"];iv=d["interval"]
        if (origin,iv) in seen:
            raise ValueError("duplicate horizon")
        seen.add((origin,iv))
        cohorts.append({
            "data_origin":origin,"interval":iv,
            "train_count":d["train_count"],"dev_count":d["dev_count"],
            "source_commit":d["model_source_commit"],
            "train_origins_sha256":d["train_origins_sha256"],
            "dev_origins_sha256":d["development_origins_sha256"],
            "g2_quantile_train_boundaries":d["token_grammar_quantile_boundaries_train_bps"],
            "persistence_mae_bps":d["baselines"]["persistence_flat"]["mae_bps_anchor"],
        })
        for r in d["results"]:
            key=(origin,iv,r["mode"],r["width"],r["depth"],r["seed"],r["steps"])
            arm=r["arm"]
            if arm in by_key[key]:
                raise ValueError("duplicate arm/seed")
            by_key[key][arm]=r
            allrows[(origin,iv,r["mode"],arm)].append(r)
    comparisons=defaultdict(list)
    for key,arms in by_key.items():
        if set(arms)!=set(ARMS):
            raise ValueError("each config must have all five matched token arms")
        common={(r["initial_state_sha256"],r["parameter_count"],
                 r["train_only_continuous_scale_bps"],
                 r["forecast_rows"],r["steps"]) for r in arms.values()}
        if len(common)!=1:
            raise ValueError("mismatched weights/params/target scale")
        for left,right in COMPARISONS:
            diff={m:arms[left][m]-arms[right][m] for m in METRICS}
            comparisons[(key[0],key[1],key[2],left,right)].append(diff)
    summaries=[]
    for k,rows in sorted(allrows.items()):
        record={
            "data_origin":k[0],"interval":k[1],
            "mode":k[2],"arm":k[3],
            "n_fits":len(rows),
            "unique_seeds":len({r["seed"] for r in rows}),
            "parameter_counts":sorted({r["parameter_count"] for r in rows}),
            "up_predictions_percent":_stat([
                100*r["n_predicted_up"]/r["forecast_rows"] for r in rows]),
            "monoclasse_99pct":sum(
                max(r["n_predicted_up"],r["n_predicted_down"])/
                r["forecast_rows"]>=.99 for r in rows),
        }
        for m in METRICS:
            record[m]=_stat([r[m] for r in rows])
        record["brier_skill_vs_train_prior"]=(
            _stat([r["brier_skill_vs_train_prior"] for r in rows])
            if k[2]=="joint" else None)
        summaries.append(record)
    deltas=[]
    for k,rs in sorted(comparisons.items()):
        row={"data_origin":k[0],"interval":k[1],
             "mode":k[2],"left":k[3],"right":k[4],
             "n_paired_fits":len(rs)}
        for m in METRICS:
            row[m+"_left_minus_right"]=_stat([x[m] for x in rs])
        deltas.append(row)
    return {
        "report":"TRAME_S3_1B_TRUE_EMBEDDING_PAIRED_PANEL_V1",
        "n_fits":sum(len(rows) for rows in by_key.values()),
        "n_paired_groups":len(by_key),
        "no_2026_test":True,"independent_test":False,
        "not_a_trading_profit_result":True,
        "cohorts":cohorts,"summary":summaries,"paired_deltas":deltas,
        "note":"Comparisons are descriptive on overlapping dev samples; no independent statistical or portfolio validation.",
    }


def to_markdown(report):
    out=["# TRAME S3.1B — Embeddings de tokens réellement appris",
         "", "**Dev seulement, 2026 gelé ; aucune performance financière démontrée.**",""]
    for interval in ("D1","H1","M1"):
        current=[x for x in report["summary"] if x["interval"]==interval]
        if not current:
            continue
        out+=["## "+interval,"",
              "| Loss | Entrée | Fits | BA % | MAE USD | MAE bps | Erreur amplitude bps | Hausses % | Monoclasse | Brier skill |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in current:
            v=lambda m:r[m]["mean"]
            skill=("n/a" if r["brier_skill_vs_train_prior"] is None
                   else f"{v('brier_skill_vs_train_prior'):.5f}")
            out.append(
                f"| {r['mode']} | {r['arm']} | {r['n_fits']} | "
                f"{100*v('balanced_direction_accuracy'):.2f} | "
                f"{v('mae_native_usd'):.2f} | {v('mae_bps_anchor'):.3f} | "
                f"{v('absolute_magnitude_error_bps'):.3f} | "
                f"{v('up_predictions_percent'):.1f} | "
                f"{r['monoclasse_99pct']}/{r['n_fits']} | {skill} |")
        out+=["","Les deltas appariés catégoriel moins scalaire sont dans le rapport JSON.",""]
    return "\n".join(out)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser(description="S3.1B 5-arm matched embedding benchmark panel")
    p.add_argument("--inputs",type=Path,nargs="+",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists() or a.markdown.exists():
        p.error("refusing to overwrite report")
    report=build_panel([json.loads(f.read_text(encoding="utf-8")) for f in a.inputs])
    a.output.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    a.markdown.write_text(to_markdown(report),encoding="utf-8")


if __name__=="__main__":
    main()
