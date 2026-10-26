"""S3.1C strictly pre2022 convergence summary: same trajectories over time."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev

from research.token_grammar.training_dynamics import ARMS,CHECKPOINTS

METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps",
         "brier_skill_vs_train_prior",
         "train_fixed_joint_loss","monitor_joint_loss",
         "gradient_norm_before_clip_mean",
         "cpu_training_seconds_cumulative")


def avg(xs):
    if not xs or any(type(x) not in (float,int) or not math.isfinite(x)
                     for x in xs):
        raise ValueError("nonfinite convergence series")
    return {"mean":float(mean(xs)),
            "sd_seeds":float(stdev(xs)) if len(xs)>1 else None,
            "n":len(xs)}


def validate(run,*,required_seeds=None,checkpoints=CHECKPOINTS):
    if (run.get("experiment")!="TRAME_S3_1C_PRE2022_CONVERGENCE_V1"
            or run.get("interval") not in ("D1","H1","M1")
            or run.get("data_origin") not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL")
            or run.get("external_dev_2022_2025_opened") is not False
            or run.get("labels_2026_opened") is not False
            or run.get("internal_monitor_never_backpropagated") is not True
            or run.get("token_quantiles_fit_train_only") is not True
            or run.get("scale_and_prior_fit_train_only") is not True
            or run.get("checkpoint_evaluations_not_independent_runs") is not True
            or run.get("train_label_cutoff_exclusive")!="2020-01-01"
            or run.get("internal_monitor_label_years")!="2020-2021"
            or run.get("last_train_label","") >= "2020-01-01"
            or run.get("first_monitor_label","") < "2020-01-01"
            or run.get("arms")!=list(ARMS)
            or run.get("checkpoints")!=list(checkpoints)
            or run.get("learned_has_11_extra_parameters") is not True
            or run.get("ordered_random_exact_parameter_match") is not True):
        raise ValueError("invalid S3.1C split, embargo or training contract")
    if required_seeds is not None and run.get("seeds")!=list(required_seeds):
        raise ValueError("wrong preregistered seeds")
    rows=run.get("evaluations",[])
    seen=set()
    paired=defaultdict(dict)
    for row in rows:
        if (row.get("arm") not in ARMS
                or row.get("checkpoint_steps") not in checkpoints
                or row.get("seed") not in run.get("seeds",[])
                or row.get("mode")!="joint"
                or row.get("grammar")!="signed_quantile_g2"
                or row.get("same_optimizer_continued") is not True
                or row.get("forecast_rows")!=run.get("monitor_count")
                or len(row.get("backbone_initial_sha256",""))!=64):
            raise ValueError("nonpaired checkpoint result")
        for key in METRICS:
            if type(row.get(key)) not in (int,float) or not math.isfinite(row[key]):
                raise ValueError("missing or invalid "+key)
        if not 0<=row["balanced_direction_accuracy"]<=1:
            raise ValueError("invalid accuracy")
        key=(row["seed"],row["checkpoint_steps"],row["arm"])
        if key in seen:
            raise ValueError("duplicate checkpoint")
        seen.add(key)
        paired[(row["seed"],row["checkpoint_steps"])][row["arm"]]=row
    if len(rows)!=len(run["seeds"])*len(checkpoints)*len(ARMS):
        raise ValueError("missing checkpoints or trajectories")
    if len(run.get("trajectories",[]))!=len(run["seeds"])*len(ARMS):
        raise ValueError("checkpoint rows are not distinct full trajectories")
    for (seed,step),values in paired.items():
        if set(values)!=set(ARMS):
            raise ValueError("incomplete arm pairing")
        sha={x["backbone_initial_sha256"] for x in values.values()}
        scale={x["train_normalizer_std_bps"] for x in values.values()}
        if len(sha)!=1 or len(scale)!=1:
            raise ValueError("backbone/scaling mismatch")
        decoded,ordered,random=[values[x] for x in ARMS]
        if (decoded["embedding_trainable_parameters"]!=0
                or ordered["embedding_trainable_parameters"]!=11
                or random["embedding_trainable_parameters"]!=11
                or ordered["parameter_count"]!=random["parameter_count"]
                or ordered["parameter_count"]-decoded["parameter_count"]!=11):
            raise ValueError("11-param capacity disclosure mismatch")


def summarise(reports,*,checkpoints=CHECKPOINTS,
              seeds=(20261025,20261026,20261027)):
    seen=set()
    strata=defaultdict(list)
    cohorts=[]
    for report in reports:
        validate(report,required_seeds=seeds,checkpoints=checkpoints)
        horizon=report["interval"]
        if horizon in seen:
            raise ValueError("duplicate resolution")
        seen.add(horizon)
        cohorts.append({
            "interval":horizon,
            "train_count":report["train_count"],
            "monitor_count":report["monitor_count"],
            "train_origins_sha256":report["train_origins_sha256"],
            "monitor_origins_sha256":report["monitor_origins_sha256"],
            "model_commit":report["model_source_commit"],
            "baseline_persistence_mae_bps":
                report["baseline_scores_train_fit_monitor_evaluated"]
                     ["persistence_flat"]["mae_bps_anchor"],
        })
        for row in report["evaluations"]:
            strata[(horizon,row["arm"],row["checkpoint_steps"])].append(row)
    summary=[]
    for (iv,arm,step),rows in sorted(strata.items()):
        out={"interval":iv,"arm":arm,"checkpoint_steps":step,
             "n_seeds":len(rows),
             "predicted_up_percent":avg([
                 100*x["n_predicted_up"]/x["forecast_rows"] for x in rows]),
             "monoclasse_99pct_fits":sum(
                 max(x["n_predicted_up"],x["n_predicted_down"])
                 /x["forecast_rows"]>=.99 for x in rows)}
        for k in METRICS:
            out[k]=avg([x[k] for x in rows])
        summary.append(out)
    return {
        "report":"TRAME_S3_1C_INTERNAL_CONVERGENCE_PANEL_V1",
        "n_distinct_trajectories":len(seen)*len(ARMS)*len(seeds),
        "n_checkpoint_evaluations":sum(len(rows) for rows in strata.values()),
        "independent_test":False,
        "external_dev_2022_2025_opened":False,
        "labels_2026_opened":False,
        "monitor_2020_2021_only":True,
        "no_portfolio_pnl":True,
        "ordered_random_parameter_matched":True,
        "learned_numeric_parameter_confounded":True,
        "checkpoint_evaluations_not_independent":True,
        "cohorts":cohorts,"summary":summary,
    }


def markdown(result):
    rows=["# TRAME S3.1C — optimisation pré-2022",
          "","**Contrôle interne 2020–2021 seulement. 2022–2025 et 2026 non ouverts.**",
          "27 trajectoires / 81 checkpoints, même optimiseur continué.",
          "Les embeddings appris ajoutent 11 paramètres au témoin numérique.",""]
    for horizon in ("D1","H1","M1"):
        values=[x for x in result["summary"] if x["interval"]==horizon]
        if not values:continue
        rows+=["## "+horizon,"",
           "| Bras | Updates | BA % | Acc. % | MAE $ | MAE bps | Amp. bps | UP % | Mono/3 | Brier skill | Train loss | Monitor loss |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in values:
            get=lambda x:r[x]["mean"]
            rows.append(
                f"| {r['arm']} | {r['checkpoint_steps']} | "
                f"{100*get('balanced_direction_accuracy'):.2f} | "
                f"{100*get('direction_accuracy_all'):.2f} | "
                f"{get('mae_native_usd'):.2f} | "
                f"{get('mae_bps_anchor'):.3f} | "
                f"{get('absolute_magnitude_error_bps'):.3f} | "
                f"{get('predicted_up_percent'):.1f} | "
                f"{r['monoclasse_99pct_fits']}/3 | "
                f"{get('brier_skill_vs_train_prior'):.5f} | "
                f"{get('train_fixed_joint_loss'):.4f} | "
                f"{get('monitor_joint_loss'):.4f} |")
        rows+=["","Écarts-types entre graines dans le JSON. Les checkpoints ne sont pas des expériences indépendantes.",""]
    return "\n".join(rows)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",type=Path,nargs="+",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists() or args.markdown.exists():
        p.error("refusing to overwrite research evidence")
    result=summarise([json.loads(f.read_text(encoding="utf-8"))
                      for f in args.inputs])
    args.output.write_text(json.dumps(result,indent=2,
                           allow_nan=False)+"\n",encoding="utf-8")
    args.markdown.write_text(markdown(result),encoding="utf-8")


if __name__=="__main__":
    main()
