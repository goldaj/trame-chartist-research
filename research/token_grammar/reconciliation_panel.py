"""TRAME S3.1E three-way, paired, honest hard-price plus soft diagnostic panel."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev

from research.token_grammar.reconciliation_loss import ARMS,WEIGHTS

METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps",
         "brier_skill_vs_train_prior",
         "regression_vs_head_sign_disagreement_fraction",
         "hard_soft_price_gap_bps",
         "soft_surrogate_mae_bps_anchor",
         "soft_surrogate_absolute_magnitude_error_bps",
         "train_common_legacy_loss",
         "monitor_common_legacy_loss",
         "gradient_norm_last50_before_clip_mean")


def stats(values):
    if not values or any(type(x) not in (float,int) or not math.isfinite(x)
                         for x in values):
        raise ValueError("invalid numeric result")
    return {"mean":float(mean(values)),
            "sd_seeds":float(stdev(values)) if len(values)>1 else None,
            "n":len(values)}


def validate(run,*,seeds=(20261025,20261026,20261027),
             checkpoints=(200,800,2000),allow_canary=False):
    if (run.get("experiment")!="TRAME_S3_1E_SOFT_RECONCILIATION_LOSS_V1"
        or run.get("interval") not in ("D1","H1","M1")
        or run.get("data_origin") not in ("BTC_PUBLIC_REAL","ARTIFICIAL_FIXTURE")
        or run.get("external_2022_2025_used") is not False
        or run.get("holdout_2026_used") is not False
        or run.get("independent_test_used") is not False
        or run.get("token_quantile_normalizer_prior_train_only") is not True
        or run.get("same_initial_sha_and_batches") is not True
        or run.get("soft_surrogate_is_not_hard_served_forecast") is not True
        or run.get("served_hard_sign_reconciliation_unchanged") is not True
        or run.get("all_arms_same_parameter_count") is not True
        or run.get("checkpoint_evaluations_not_independent") is not True
        or run.get("train_label_end_exclusive")!="2020-01-01"
        or run.get("monitor_label_years")!="2020-2021"
        or run.get("arms")!=list(ARMS)
        or run.get("weights")!=WEIGHTS
        or run.get("seed_list")!=list(seeds)
        or run.get("checkpoint_steps")!=list(checkpoints)
        or run.get("engineering_canary_not_scientific_selection") is not allow_canary):
        raise ValueError("wrong study or temporal embargo violation")
    if run["data_origin"]=="BTC_PUBLIC_REAL":
        source=run.get("model_source_commit","")
        if len(source)!=40 or any(c not in "0123456789abcdef" for c in source):
            raise ValueError("source SHA missing")
    rows=run.get("results",[])
    if len(rows)!=len(seeds)*len(ARMS)*len(checkpoints):
        raise ValueError("missing trajectories or checkpoints")
    groups=defaultdict(dict)
    for row in rows:
        arm=row.get("arm")
        if (arm not in ARMS
            or row.get("seed") not in seeds
            or row.get("checkpoint_updates") not in checkpoints
            or row.get("reconciled_surrogate_weight")!=WEIGHTS.get(arm)
            or row.get("mode")!="joint"
            or row.get("width")!=16 or row.get("depth")!=1
            or row.get("same_optimizer_continued") is not True
            or row.get("forecast_rows")!=run.get("monitor_count")
            or len(row.get("backbone_initial_sha256",""))!=64):
            raise ValueError("non-paired arm or wrong loss")
        if row.get("regression_vs_head_sign_disagreement_fraction",-1)<0:
            raise ValueError("missing regression/head disagreement")
        for name in METRICS:
            if type(row.get(name)) not in (int,float) or not math.isfinite(row[name]):
                raise ValueError("missing "+name)
        key=(row["seed"],row["checkpoint_updates"])
        if arm in groups[key]:
            raise ValueError("duplicate loss arm")
        groups[key][arm]=row
    for rows in groups.values():
        if set(rows)!=set(ARMS):
            raise ValueError("unmatched 3-way loss group")
        if len({r["backbone_initial_sha256"] for r in rows.values()})!=1:
            raise ValueError("different model initialisation")
        if len({r["parameter_count"] for r in rows.values()})!=1:
            raise ValueError("parameter mismatch")
        if len({r["train_normalizer_std_bps"] for r in rows.values()})!=1:
            raise ValueError("different training scale")
    return groups


def panel(reports,*,seeds=(20261025,20261026,20261027),
          checkpoints=(200,800,2000),allow_canary=False):
    seen=set()
    buckets=defaultdict(list)
    differences=defaultdict(list)
    cohorts=[]
    for report in reports:
        horizon=report["interval"]
        if horizon in seen:
            raise ValueError("duplicate horizon")
        seen.add(horizon)
        groups=validate(report,seeds=seeds,checkpoints=checkpoints,
                        allow_canary=allow_canary)
        cohorts.append({
            "horizon":horizon,"train":report["train_count"],
            "monitor":report["monitor_count"],
            "train_sha":report["train_origins_sha256"],
            "monitor_sha":report["monitor_origins_sha256"],
            "source_sha":report["model_source_commit"],
            "persistence_mae_bps":report["baseline_scores"]["persistence_flat"]["mae_bps_anchor"],
        })
        for (seed,step),arms in groups.items():
            ref=arms["legacy"]
            for arm,row in arms.items():
                buckets[(horizon,arm,step)].append(row)
                if arm!="legacy":
                    differences[(horizon,arm,step)].append({
                        name:row[name]-ref[name] for name in METRICS})
    summary=[]
    for (h,arm,step),rows in sorted(buckets.items()):
        r={"horizon":h,"arm":arm,"checkpoint":step,
           "n_seeds":len(rows),
           "surrogate_weight":WEIGHTS[arm],
           "up_prediction_pct":stats([x["predicted_up_percent"] for x in rows]),
           "n_monoclasse":sum(x["monoclasse_99pct"] for x in rows)}
        for k in METRICS:
            r[k]=stats([x[k] for x in rows])
        summary.append(r)
    deltas=[]
    for (h,arm,step),rows in sorted(differences.items()):
        d={"horizon":h,"arm":arm,"versus":"legacy","checkpoint":step,
           "n_paired_seeds":len(rows),"same_parameter_count":True}
        for metric in METRICS:d[metric+"_delta"]=stats([x[metric] for x in rows])
        deltas.append(d)
    return {
        "report":"TRAME_S3_1E_HARD_PRICE_SOFT_LOSS_PANEL_V1",
        "n_distinct_trajectories":len(seen)*len(ARMS)*len(seeds),
        "n_checkpoint_observations":len(seen)*len(ARMS)*len(seeds)*len(checkpoints),
        "external_dev_2022_2025_used":False,
        "holdout_2026_used":False,
        "not_independent_test":True,
        "hard_forecast_is_served":True,
        "soft_forecast_diagnostics_only":True,
        "same_capacity_all_arms":True,
        "no_portfolio_pnl":True,
        "cohorts":cohorts,"summary":summary,"paired_deltas":deltas,
    }


def markdown(report):
    out=["# TRAME S3.1E : perte de réconciliation du prix",
         "","**Données pré2022 uniquement. Hard-price réellement servi, soft diagnostic seulement.**",
         "Trois graines et checkpoints corrélés, pas de test indépendant ni PnL.",""]
    for h in ("D1","H1","M1"):
        rows=[x for x in report["summary"] if x["horizon"]==h]
        if not rows:continue
        out+=["## "+h,"",
              "| Loss | Updates | BA % hard | MAE $ hard | MAE bps hard | AMP bps hard | MAE bps SOFT | Désaccord des têtes % | UP % | Mono/3 | Brier skill |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in rows:
            v=lambda key:r[key]["mean"]
            out.append(f"| {r['arm']} | {r['checkpoint']} | "
                       f"{v('balanced_direction_accuracy')*100:.2f} | "
                       f"{v('mae_native_usd'):.2f} | "
                       f"{v('mae_bps_anchor'):.3f} | "
                       f"{v('absolute_magnitude_error_bps'):.3f} | "
                       f"{v('soft_surrogate_mae_bps_anchor'):.3f} | "
                       f"{v('regression_vs_head_sign_disagreement_fraction')*100:.1f} | "
                       f"{v('up_prediction_pct'):.1f} | "
                       f"{r['n_monoclasse']}/{r['n_seeds']} | "
                       f"{v('brier_skill_vs_train_prior'):.5f} |")
        out+=["","Tous les deltas appariés et dispersions en JSON.",""]
    return "\n".join(out)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",nargs="+",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    args=p.parse_args(argv)
    if args.output.exists() or args.markdown.exists():
        p.error("refusing to overwrite result")
    r=panel([json.loads(x.read_text()) for x in args.inputs])
    args.output.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    args.markdown.write_text(markdown(r),encoding="utf-8")

if __name__=="__main__":
    main()
