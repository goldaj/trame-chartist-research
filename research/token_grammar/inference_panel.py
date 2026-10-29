"""S3.1F strict same-weights inference-rule panel: 9 models, 27 checkpoints,
81 dependent price reconstructions. Never count three rules as three fits.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev

from research.token_grammar.inference_ablation import RULES

METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps",
         "signed_forecast_bias_bps")


def moments(a):
    if not a or any(type(x) not in (int,float) or not math.isfinite(x) for x in a):
        raise ValueError("missing or nonfinite metric")
    return {"mean":float(mean(a)),
            "sd_across_seeds":float(stdev(a)) if len(a)>1 else None,
            "n":len(a)}


def validate(run,*,seeds=(20261025,20261026,20261027),
             checkpoints=(200,800,2000),allow_canary=False):
    if (run.get("experiment")!="TRAME_S3_1F_INFERENCE_ONLY_RULE_ABLATION_V1"
        or run.get("data_origin") not in ("BTC_PUBLIC_REAL","ARTIFICIAL_FIXTURE")
        or run.get("interval") not in ("D1","H1","M1")
        or run.get("train_labels_before")!="2020-01-01"
        or run.get("monitor_labels_years")!="2020-2021"
        or run.get("external_dev_2022_2025_accessed") is not False
        or run.get("holdout_2026_accessed") is not False
        or run.get("train_only_codec_normalizer_prior") is not True
        or run.get("one_model_shared_by_three_pricing_rules") is not True
        or run.get("hard_reproduces_existing_forecast_prices_exactly") is not True
        or run.get("same_checkpoint_for_all_rules") is not True
        or run.get("head_probabilities_do_not_calibrate_direct_mu_sign") is not True
        or run.get("checkpoints_not_independent_models") is not True
        or run.get("independent_test") is not False
        or run.get("engineering_canary_not_scientific_selection") is not allow_canary
        or run.get("rules")!=list(RULES)
        or run.get("seeds")!=list(seeds)
        or run.get("checkpoints")!=list(checkpoints)):
        raise ValueError("wrong causal inference study or evaluation grid")
    if run["data_origin"]=="BTC_PUBLIC_REAL":
        sha=run.get("model_source_commit","")
        if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha):
            raise ValueError("model commit SHA missing")
    if len(run.get("trajectories",[]))!=len(seeds):
        raise ValueError("unexpected number of actual trained models")
    if len(run.get("results",[]))!=len(seeds)*len(checkpoints)*len(RULES):
        raise ValueError("missing price rule evaluations")
    grouped=defaultdict(dict)
    for row in run["results"]:
        rule=row.get("rule")
        if (rule not in RULES or row.get("seed") not in seeds
                or row.get("step") not in checkpoints
                or row.get("same_model_weights") is not True
                or row.get("trained_once_no_reinitialisation") is not True
                or row.get("legacy_loss_unchanged") is not True
                or row.get("forecast_rows")!=run["monitor_count"]
                or len(row.get("backbone_initial_sha256",""))!=64):
            raise ValueError("nonpaired inference rule or wrong training")
        for k in METRICS+("head_sign_disagreement_fraction",):
            if type(row.get(k)) not in (float,int) or not math.isfinite(row[k]):
                raise ValueError("invalid score "+k)
        pair=(row["seed"],row["step"])
        if rule in grouped[pair]:
            raise ValueError("duplicate pricing rule")
        grouped[pair][rule]=row
    for key,arms in grouped.items():
        if set(arms)!=set(RULES):
            raise ValueError("incomplete inference-rule checkpoint")
        if len({r["backbone_initial_sha256"] for r in arms.values()})!=1:
            raise ValueError("initial seed mismatch")
        if len({r["parameter_count"] for r in arms.values()})!=1:
            raise ValueError("parameter mismatch")
        if len({r["normalizer_std_bps_train_only"] for r in arms.values()})!=1:
            raise ValueError("normalizer mismatch")
        if len({r["head_sign_disagreement_fraction"] for r in arms.values()})!=1:
            raise ValueError("different heads/weights at same checkpoint")
        if len({r["head_brier_score"] for r in arms.values()})!=1:
            raise ValueError("head probabilities changed across rules")
    return grouped


def panel(reports,*,seeds=(20261025,20261026,20261027),
          checkpoints=(200,800,2000),allow_canary=False):
    seen=set()
    summary_rows=defaultdict(list)
    differences=defaultdict(list)
    cohorts=[]
    for report in reports:
        iv=report["interval"]
        if iv in seen:
            raise ValueError("duplicate horizon")
        seen.add(iv)
        groups=validate(report,seeds=seeds,checkpoints=checkpoints,
                        allow_canary=allow_canary)
        cohorts.append({"interval":iv,"train":report["train_count"],
                        "monitor":report["monitor_count"],
                        "train_sha":report["train_origins_sha256"],
                        "monitor_sha":report["monitor_origins_sha256"],
                        "model_sha":report["model_source_commit"],
                        "persistence_mae_bps":
                        report["baseline_scores"]["persistence_flat"]["mae_bps_anchor"]})
        for (seed,step),models in groups.items():
            baseline=models["joint_hard"]
            for rule,row in models.items():
                summary_rows[(iv,rule,step)].append(row)
                if rule!="joint_hard":
                    differences[(iv,rule,step)].append({
                        k:row[k]-baseline[k] for k in METRICS})
    summary=[]
    for (iv,rule,step),rows in sorted(summary_rows.items()):
        x={"interval":iv,"rule":rule,"checkpoint":step,
           "n_seeds":len(rows),
           "predicted_up_percent":moments([
               r["predicted_up_percent"] for r in rows]),
           "monoclasse_99pct_fits":sum(r["monoclasse_99pct"] for r in rows),
           "head_sign_disagreement_percent":moments([
               100*r["head_sign_disagreement_fraction"] for r in rows]),
           "head_brier_diagnostic":moments([
               r["head_brier_skill_vs_train_prior"] for r in rows])}
        for k in METRICS:x[k]=moments([r[k] for r in rows])
        summary.append(x)
    paired=[]
    for (iv,rule,step),rows in sorted(differences.items()):
        item={"interval":iv,"rule":rule,"reference":"joint_hard",
              "checkpoint":step,"n_paired_seeds":len(rows),
              "same_exact_trained_weights":True}
        for k in METRICS:item[k+"_delta"]=moments([r[k] for r in rows])
        paired.append(item)
    return {
        "report":"TRAME_S3_1F_SAME_MODEL_THREE_INFERENCE_RULES_V1",
        "n_models_trained":len(seen)*len(seeds),
        "n_distinct_checkpoints":len(seen)*len(seeds)*len(checkpoints),
        "n_rule_evaluations":len(seen)*len(seeds)*len(checkpoints)*len(RULES),
        "rules_are_not_independent_models":True,
        "hard_rule_exactly_previous_served_model":True,
        "external_2022_2025_used":False,
        "holdout_2026_used":False,
        "not_independent_test":True,
        "no_cumulative_portfolio_pnl":True,
        "cohorts":cohorts,"summary":summary,"paired_deltas":paired,
    }


def markdown(r):
    rows=["# TRAME S3.1F : prix dur, retour mu direct et soft sur les MÊMES modèles",
          "","**Un modèle entraîné par graine et horizon ; 3 évaluations au même checkpoint, pas 3 modèles.**",
          "Uniquement monitor interne 2020–21, aucune validation indépendante.",""]
    for iv in ("D1","H1","M1"):
        a=[x for x in r["summary"] if x["interval"]==iv]
        if not a:continue
        rows+=["## "+iv,"",
           "| Règle | Updates | BA % | MAE prix $ | MAE bps | AMP bps | UP % | MONO/3 | Désaccord têtes % |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for x in a:
            v=lambda k:x[k]["mean"]
            rows.append(f"| {x['rule']} | {x['checkpoint']} | "
                        f"{100*v('balanced_direction_accuracy'):.2f} | "
                        f"{v('mae_native_usd'):.2f} | "
                        f"{v('mae_bps_anchor'):.3f} | "
                        f"{v('absolute_magnitude_error_bps'):.3f} | "
                        f"{v('predicted_up_percent'):.1f} | "
                        f"{x['monoclasse_99pct_fits']}/3 | "
                        f"{v('head_sign_disagreement_percent'):.1f} |")
        rows+=["","Les deltas appariés et dispersions figurent dans le JSON.",""]
    return "\n".join(rows)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",nargs="+",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists() or a.markdown.exists():
        p.error("refusing to overwrite results")
    r=panel([json.loads(f.read_text()) for f in a.inputs])
    a.output.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    a.markdown.write_text(markdown(r),encoding="utf-8")


if __name__=="__main__":
    main()
