"""S3.1D strict five-way paired loss ablation with direction+amount measures."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev

from research.token_grammar.loss_ablation import OBJECTIVES,ARMS

METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps",
         "brier_skill_vs_train_prior",
         "monitor_reference_joint_loss",
         "train_reference_joint_loss",
         "gradient_norm_last50_mean_before_clip")


def avg(xs):
    if not xs or any(type(x) not in (int,float) or not math.isfinite(x) for x in xs):
        raise ValueError("invalid ablation metric")
    return {"mean":float(mean(xs)),
            "sd_across_seeds":float(stdev(xs)) if len(xs)>1 else None,
            "n":len(xs)}


def validate(report,*,checkpoints=(200,800,2000),
             seeds=(20261025,20261026,20261027)):
    if (report.get("experiment")!="TRAME_S3_1D_DIRECTION_MAGNITUDE_LOSS_ABLATION_V1"
            or report.get("interval") not in ("D1","H1","M1")
            or report.get("data_origin") not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL")
            or report.get("external_2022_2025_used") is not False
            or report.get("holdout_2026_used") is not False
            or report.get("independent_test_used") is not False
            or report.get("token_quantile_input_scale_prior_train_only") is not True
            or report.get("all_arms_same_model_initial_weights") is not True
            or report.get("all_arms_same_batch_order") is not True
            or report.get("all_arms_same_forecast_reconciliation") is not True
            or report.get("checkpoints_not_independent_models") is not True
            or report.get("nonzero_BCE_weight_for_all_arms") is not True
            or report.get("train_label_cutoff_exclusive")!="2020-01-01"
            or report.get("monitor_label_years")!="2020-2021"
            or report.get("arms")!=list(ARMS)
            or report.get("seeds")!=list(seeds)
            or report.get("checkpoint_steps")!=list(checkpoints)):
        raise ValueError("wrong preregistered loss comparison or external development leakage")
    rows=report.get("results",[])
    if len(rows)!=len(ARMS)*len(seeds)*len(checkpoints):
        raise ValueError("incomplete loss/checkpoint matrix")
    cohorts=defaultdict(dict)
    for r in rows:
        if (r.get("loss_arm") not in ARMS
                or r.get("seed") not in seeds
                or r.get("checkpoint_updates") not in checkpoints
                or r.get("mode")!="joint"
                or r.get("width")!=16 or r.get("depth")!=1
                or r.get("model_checkpoint_continuing_same_optimizer") is not True
                or len(r.get("backbone_initial_sha256",""))!=64):
            raise ValueError("mismatched objective arm")
        a=r["loss_arm"]
        if (r.get("direction_weight")!=OBJECTIVES[a][0]
                or r.get("magnitude_weight")!=OBJECTIVES[a][1]):
            raise ValueError("unexpected loss coefficients")
        for k in METRICS:
            if type(r.get(k)) not in (float,int) or not math.isfinite(r[k]):
                raise ValueError("missing finite score "+k)
        key=(r["seed"],r["checkpoint_updates"])
        if a in cohorts[key]:
            raise ValueError("duplicated loss arm")
        cohorts[key][a]=r
    for key,arms in cohorts.items():
        if set(arms)!=set(ARMS):
            raise ValueError("partial seed/checkpoint group")
        if len({x["backbone_initial_sha256"] for x in arms.values()})!=1:
            raise ValueError("different initial weights")
        if len({x["parameter_count"] for x in arms.values()})!=1:
            raise ValueError("objective altered model capacity")
        if len({x["normalizer_train_bps"] for x in arms.values()})!=1:
            raise ValueError("objective altered train-only normalizer")
    return cohorts


def panel(reports,*,checkpoints=(200,800,2000),
          seeds=(20261025,20261026,20261027)):
    seen=set()
    buckets=defaultdict(list)
    paired=defaultdict(list)
    cohorts=[]
    for report in reports:
        key=report["interval"]
        if key in seen:raise ValueError("duplicate horizon")
        seen.add(key)
        groups=validate(report,checkpoints=checkpoints,seeds=seeds)
        cohorts.append({
            "interval":key,"train_count":report["train_count"],
            "monitor_count":report["monitor_count"],
            "train_origins_sha256":report["train_origins_sha256"],
            "monitor_origins_sha256":report["monitor_origins_sha256"],
            "model_source_commit":report["model_source_commit"],
            "persistence_mae_bps":report["monitor_baselines"]["persistence_flat"]["mae_bps_anchor"],
        })
        for (seed,step),arms in groups.items():
            baseline=arms["reference"]
            for arm,row in arms.items():
                buckets[(key,arm,step)].append(row)
                if arm!="reference":
                    paired[(key,arm,step)].append({
                        k:row[k]-baseline[k] for k in METRICS})
    summary=[]
    for (h,arm,step),rows in sorted(buckets.items()):
        data={"interval":h,"loss_arm":arm,"checkpoint":step,
              "n_seeds":len(rows),
              "direction_weight":OBJECTIVES[arm][0],
              "magnitude_weight":OBJECTIVES[arm][1],
              "predicted_up_percent":avg([r["predicted_up_percent"] for r in rows]),
              "monoclasse_99pct_count":sum(r["monoclasse_99pct"] for r in rows)}
        for k in METRICS:data[k]=avg([r[k] for r in rows])
        summary.append(data)
    contrasts=[]
    for (h,arm,step),rows in sorted(paired.items()):
        data={"interval":h,"loss_arm":arm,"vs":"reference",
              "checkpoint":step,"paired_seeds":len(rows),
              "same_parameter_count":True}
        for k in METRICS:data[k+"_delta"]=avg([r[k] for r in rows])
        contrasts.append(data)
    return {
        "report":"TRAME_S3_1D_LOSS_ABLATION_PANEL_V1",
        "n_distinct_trajectories":len(seen)*len(ARMS)*len(seeds),
        "n_checkpoint_observations":len(seen)*len(ARMS)*len(seeds)*len(checkpoints),
        "external_dev_2022_2025_used":False,
        "holdout_2026_used":False,
        "not_independent_test":True,
        "same_capacity_all_loss_arms":True,
        "no_real_trading_or_cumulative_pnl":True,
        "cohorts":cohorts,"summary":summary,"contrasts":contrasts,
    }


def markdown(result):
    lines=["# S3.1D — ablation objective prix / direction / amplitude",
           "","**Contrôle interne 2020–2021, pas de validation indépendante.**",
           "Même backbone, seule la loss change. 2022–2025 et 2026 non utilisés.",""]
    for iv in ("D1","H1","M1"):
        rows=[r for r in result["summary"] if r["interval"]==iv]
        if not rows:continue
        lines+=["## "+iv,"",
                "| Loss | Updates | BA % | MAE USD | MAE bps | Amp. bps | UP % | Mono/3 | Brier skill | Monitor loss commune |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in rows:
            v=lambda k:r[k]["mean"]
            lines.append(
                f"| {r['loss_arm']} | {r['checkpoint']} | "
                f"{100*v('balanced_direction_accuracy'):.2f} | "
                f"{v('mae_native_usd'):.2f} | {v('mae_bps_anchor'):.3f} | "
                f"{v('absolute_magnitude_error_bps'):.3f} | "
                f"{v('predicted_up_percent'):.1f} | "
                f"{r['monoclasse_99pct_count']}/{r['n_seeds']} | "
                f"{v('brier_skill_vs_train_prior'):.5f} | "
                f"{v('monitor_reference_joint_loss'):.4f} |")
        lines+=["","Contrastes appariés complets, SHA et écarts-types dans le JSON.",""]
    return "\n".join(lines)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",nargs="+",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists() or args.markdown.exists():
        p.error("refuse overwriting scientific evidence")
    rep=panel([json.loads(p.read_text()) for p in args.inputs])
    args.output.write_text(json.dumps(rep,indent=2,
                           allow_nan=False)+"\n",encoding="utf-8")
    args.markdown.write_text(markdown(rep),encoding="utf-8")


if __name__=="__main__":
    main()
