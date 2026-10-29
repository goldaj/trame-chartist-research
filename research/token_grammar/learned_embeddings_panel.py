"""S3.1B strict three-arm paired comparison from aggregate research JSON only."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev

from research.token_grammar.learned_embeddings import GRAMMARS,ARMS,MODES

METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps")
CONTRASTS=(("embedding_ordered","decoded"),
           ("embedding_random","decoded"),
           ("embedding_ordered","embedding_random"))


def mean_sd(values):
    if not values:
        raise ValueError("empty metric")
    return {"mean":float(mean(values)),
            "sd_across_fits":float(stdev(values)) if len(values)>1 else None,
            "n":len(values)}


def validate(source):
    if (source.get("experiment")!="TRAME_S3_1B_SCALAR_LEARNED_TOKEN_EMBEDDINGS_V1"
            or source.get("data_origin") not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL")
            or source.get("interval") not in ("D1","H1","M1")
            or source.get("labels_2026_opened") is not False
            or source.get("independent_test_used") is not False
            or source.get("quantile_fit_on")!="TRAIN_PAST_CONTEXTS_ONLY"
            or source.get("same_backbone_initialisation") is not True
            or source.get("same_target_and_input_scale_train_only") is not True
            or source.get("common_batch_indices_per_seed") is not True
            or source.get("learned_vs_decoded_trainable_params_matched") is not False
            or source.get("ordered_vs_random_trainable_params_matched") is not True):
        raise ValueError("invalid chronology, training provenance, or capacity disclosure")
    if source["data_origin"]=="BTC_PUBLIC_REAL":
        sha=source.get("model_source_commit","")
        if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError("unverifiable code source")
    if not source.get("results") or not source.get("baseline_scores",{}).get("persistence_flat"):
        raise ValueError("missing fits or baseline")
    for row in source["results"]:
        if (row.get("grammar") not in GRAMMARS
                or row.get("arm") not in ARMS
                or row.get("mode") not in MODES
                or row.get("forecast_rows")!=source.get("dev_count")
                or row.get("vocabulary_size")!=11
                or type(row.get("seed"))!=int
                or type(row.get("width"))!=int
                or type(row.get("depth"))!=int
                or type(row.get("steps"))!=int
                or len(row.get("backbone_initial_sha256",""))!=64):
            raise ValueError("malformed trained arm")
        for metric in METRICS:
            if type(row.get(metric)) not in (float,int) or not math.isfinite(row[metric]):
                raise ValueError("nonfinite metric "+metric)
        if not 0<=row["balanced_direction_accuracy"]<=1:
            raise ValueError("invalid balanced direction accuracy")
        if row["mode"]=="joint":
            if (row.get("binary_probabilities_from_trained_head") is not True
                    or not math.isfinite(row.get("brier_skill_vs_train_prior",float("nan")))):
                raise ValueError("joint mode lacks calibrated-prior comparison")
        else:
            if row.get("brier_nonflat") is not None:
                raise ValueError("untrained direction head falsely evaluated")


def panel(sources):
    seen=set()
    groups=defaultdict(dict)
    grouped=defaultdict(list)
    cohort=[]
    for source in sources:
        validate(source)
        k=(source["data_origin"],source["interval"])
        if k in seen:
            raise ValueError("duplicate horizon")
        seen.add(k)
        cohort.append({"source":k[0],"interval":k[1],
                       "train":source["train_count"],"dev":source["dev_count"],
                       "train_origins_sha256":source["train_origins_sha256"],
                       "dev_origins_sha256":source["development_origins_sha256"],
                       "model_source_commit":source["model_source_commit"]})
        for row in source["results"]:
            pair=(k[0],k[1],row["grammar"],row["mode"],
                  row["seed"],row["width"],row["depth"],row["steps"])
            if row["arm"] in groups[pair]:
                raise ValueError("duplicate pairing row")
            groups[pair][row["arm"]]=row
            grouped[(k[0],k[1],row["grammar"],row["mode"],row["arm"])].append(row)
    deltas=defaultdict(list)
    for pair,rows in groups.items():
        if set(rows)!=set(ARMS):
            raise ValueError("incomplete three-way comparison")
        backs={r["backbone_initial_sha256"] for r in rows.values()}
        scales={r["train_normalizer_std_bps_common"] for r in rows.values()}
        if len(backs)!=1 or len(scales)!=1:
            raise ValueError("unmatched backbone or input/target normalization")
        numeric=rows["decoded"]
        a,b=rows["embedding_ordered"],rows["embedding_random"]
        if not (a["parameter_count"]==b["parameter_count"]==
                numeric["parameter_count"]+11
                and a["embedding_trainable_parameters"]==11
                and b["embedding_trainable_parameters"]==11
                and numeric["embedding_trainable_parameters"]==0):
            raise ValueError("incorrect capacity contrast")
        for arm,base in CONTRASTS:
            deltas[(pair[0],pair[1],pair[2],pair[3],arm,base)].append({
                key:rows[arm][key]-rows[base][key] for key in METRICS})
    summary=[]
    for k,rows in sorted(grouped.items()):
        data={
            "source":k[0],"interval":k[1],
            "grammar":k[2],"mode":k[3],"arm":k[4],
            "n_fits":len(rows),
            "unique_seeds":len({r["seed"] for r in rows}),
            "parameters":sorted({r["parameter_count"] for r in rows}),
            "embedding_parameters":rows[0]["embedding_trainable_parameters"],
            "predicted_up_percent":mean_sd(
                [100*r["n_predicted_up"]/r["forecast_rows"] for r in rows]),
            "monoclasse_99pct_fits":sum(
                max(r["n_predicted_up"],r["n_predicted_down"])
                /r["forecast_rows"]>=.99 for r in rows),
            "train_seconds":mean_sd([r["cpu_train_seconds"] for r in rows]),
        }
        for metric in METRICS:
            data[metric]=mean_sd([r[metric] for r in rows])
        data["brier_skill_vs_train_prior"]=(
            mean_sd([r["brier_skill_vs_train_prior"] for r in rows])
            if k[3]=="joint" else None)
        summary.append(data)
    comparisons=[]
    for k,values in sorted(deltas.items()):
        out={"source":k[0],"interval":k[1],
             "grammar":k[2],"mode":k[3],
             "arm":k[4],"reference_arm":k[5],
             "n_paired_fits":len(values),
             "exact_parameter_match":k[4]!= "decoded" and k[5]!="decoded"}
        for metric in METRICS:
            out[metric+"_delta"]=mean_sd([v[metric] for v in values])
        comparisons.append(out)
    return {"report":"TRAME_S3_1B_PAIRED_EMBEDDING_V1",
            "n_fits":sum(len(v) for v in groups.values()),
            "n_three_arm_groups":len(groups),
            "independent_test":False,"labels_2026_opened":False,
            "no_cumulative_trading_return":True,
            "learned_vs_numeric_parameter_confounded":True,
            "ordered_vs_random_parameter_matched":True,
            "cohorts":cohort,"summary":summary,"paired_deltas":comparisons}


def markdown(report):
    out=["# TRAME S3.1B — vrais embeddings de tokens signés","",
        "**Développement uniquement, 2026 non ouvert, aucun profit de trading démontré.**",
        "Embeddings learned +11 paramètres entraînables vs decoded.",
        "Ordered vs random : exactement mêmes paramètres.",""]
    for interval in ("D1","H1","M1"):
        rows=[r for r in report["summary"] if r["interval"]==interval]
        if not rows:continue
        out+=["## "+interval,"",
              "| Grammaire | Loss | Bras | Fits | BA % | MAE USD | MAE bps | Erreur amplitude bps | UP % | Monoclasse | Brier skill |",
              "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in rows:
            m=lambda k:r[k]["mean"]
            brier="n/a" if r["brier_skill_vs_train_prior"] is None else f"{m('brier_skill_vs_train_prior'):.5f}"
            out.append(
                f"| {r['grammar']} | {r['mode']} | {r['arm']} | {r['n_fits']} | "
                f"{100*m('balanced_direction_accuracy'):.2f} | "
                f"{m('mae_native_usd'):.2f} | {m('mae_bps_anchor'):.3f} | "
                f"{m('absolute_magnitude_error_bps'):.3f} | "
                f"{m('predicted_up_percent'):.1f} | "
                f"{r['monoclasse_99pct_fits']}/{r['n_fits']} | {brier} |")
        out+=["","Deltas appariés, dispersion et empreintes de cohorte dans le JSON.",""]
    return "\n".join(out)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",nargs="+",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists() or a.markdown.exists():
        p.error("will not overwrite results")
    rep=panel([json.loads(x.read_text(encoding="utf-8")) for x in a.inputs])
    a.output.write_text(json.dumps(rep,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    a.markdown.write_text(markdown(rep),encoding="utf-8")


if __name__=="__main__":
    main()
