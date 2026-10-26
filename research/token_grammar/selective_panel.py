"""S3.1G robust summary of train-fitted magnitude gates.

Strictly separate 9 trained models from 108 dependent threshold/rule scores.
Never hide empty subgroups or missing balanced accuracy; compare baseline
persistence on exactly the same selected monitor candles.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev
from research.token_grammar.inference_ablation import RULES
from research.token_grammar.selective_forecast import QUANTILES

METRICS=("mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps",
         "persistence_mae_native_usd",
         "persistence_mae_bps_anchor",
         "direction_accuracy_all",
         "mean_abs_predicted_move_bps",
         "mean_abs_actual_move_bps")

def summarize_numeric(xs):
    arr=[x for x in xs if x is not None]
    if any(type(x) not in (float,int) or not math.isfinite(x) for x in arr):
        raise ValueError("unbounded or nonfinite score")
    return {"mean":float(mean(arr)) if arr else None,
            "sd_seeds":float(stdev(arr)) if len(arr)>1 else None,
            "n_available":len(arr),"n_missing":len(xs)-len(arr)}

def validate(x,*,seeds=(20261025,20261026,20261027),
             steps=2000,allow_canary=False):
    if (x.get("experiment")!="TRAME_S3_1G_TRAIN_ONLY_SELECTIVE_MAGNITUDE_V1"
        or x.get("interval") not in ("D1","H1","M1")
        or x.get("data_origin") not in ("ARTIFICIAL_FIXTURE","BTC_PUBLIC_REAL")
        or x.get("train_labels_before")!="2020-01-01"
        or x.get("monitor_labels_years")!="2020-2021"
        or x.get("external_2022_2025_used") is not False
        or x.get("holdout_2026_used") is not False
        or x.get("only_train_predictions_define_cutoffs") is not True
        or x.get("all_rules_same_monitored_subset") is not True
        or x.get("only_hard_pred_magnitude_gates") is not True
        or x.get("no_monitor_optimized_thresholds") is not True
        or x.get("shared_backbone_and_loss_s3f") is not True
        or x.get("not_independent_test") is not True
        or x.get("engineering_canary_not_scientific_selection") is not allow_canary
        or x.get("rules")!=list(RULES)
        or x.get("thresholds")!=[q for q,_ in QUANTILES]
        or x.get("min_informative_cases")!=30
        or x.get("seeds")!=list(seeds)
        or x.get("training_steps")!=steps):
        raise ValueError("unregistered selective study, non-causal threshold or unlocked holdout")
    if x["data_origin"]=="BTC_PUBLIC_REAL":
        h=x.get("model_source_commit","")
        if len(h)!=40 or any(a not in "0123456789abcdef" for a in h):
            raise ValueError("missing source model SHA")
    if len(x.get("trajectories",[]))!=len(seeds):
        raise ValueError("missing actual model training paths")
    if len(x.get("results",[]))!=len(seeds)*len(QUANTILES)*len(RULES):
        raise ValueError("not 12 pricing/coverage scores per trained model")
    groups=defaultdict(dict)
    thresholds_by_seed={}
    for t in x["trajectories"]:
        seed=t.get("seed")
        if seed not in seeds or seed in thresholds_by_seed or t.get("trained_models")!=1 or t.get("steps")!=steps:
            raise ValueError("model counts or training trajectories invalid")
        th=t["train_prediction_thresholds_bps"]
        if list(th)!=[q for q,_ in QUANTILES]:
            raise ValueError("threshold order changed")
        if not (th["all"]==0<=th["q50"]<=th["q75"]<=th["q90"]):
            raise ValueError("threshold monotonicity or TRAIN leak")
        thresholds_by_seed[seed]=th
    for r in x["results"]:
        seed=r.get("seed")
        q=r.get("threshold")
        rule=r.get("rule")
        if (seed not in seeds or q not in thresholds_by_seed.get(seed,{})
            or rule not in RULES
            or r.get("quantile_fit_only_on_training_predictions") is not True
            or r.get("same_weights_three_rules") is not True
            or r.get("model_steps")!=steps
            or r.get("n_monitor")!=x.get("monitor_count")
            or r.get("head_probabilities_diagnostic_only_for_direct")
                        is not (rule=="signed_direct_mu")
            or r.get("threshold_train_bps")!=thresholds_by_seed[seed][q]
            or len(r.get("selection_sha256",""))!=64):
            raise ValueError("wrong shared cohort or source of selection")
        n=r.get("n_selected")
        if type(n)!=int or not 0<=n<=x["monitor_count"]:
            raise ValueError("selection size invalid")
        if not math.isclose(r.get("coverage",-1),n/x["monitor_count"],abs_tol=1e-12):
            raise ValueError("coverage denominator invalid")
        if q=="all" and n!=x["monitor_count"]:
            raise ValueError("all group missing cases")
        if n==0:
            if r["status"]!="NO_COVERAGE" or r["mae_bps_anchor"] is not None:
                raise ValueError("empty group generated a fake statistic")
        elif (r["status"]=="INFORMATIVE") != (n>=30 and r["n_actual_up"]>0 and r["n_actual_down"]>0):
            raise ValueError("wrong coverage/class imbalance diagnostics")
        if r["status"]!="INFORMATIVE" and r["balanced_direction_accuracy"] is not None:
            raise ValueError("BA fabricated for insufficient class coverage")
        for m in METRICS:
            v=r.get(m)
            if n>0 and (type(v) not in (float,int) or not math.isfinite(v)):
                raise ValueError("nonfinite conditional "+m)
        key=(seed,q)
        if rule in groups[key]:
            raise ValueError("duplicate rule on same selected group")
        groups[key][rule]=r
    for (seed,q),values in groups.items():
        if set(values)!=set(RULES):
            raise ValueError("different models falsely presented as 3 rules")
        if len({r["selection_sha256"] for r in values.values()})!=1:
            raise ValueError("different selected cases across pricing rules")
        if len({r["n_selected"] for r in values.values()})!=1:
            raise ValueError("different observed coverage")
        if len({r["initial_weights_sha256"] for r in values.values()})!=1:
            raise ValueError("weights do not match")
        if len({r["model_parameters"] for r in values.values()})!=1:
            raise ValueError("architecture drift")
        if len({r["persistence_mae_bps_anchor"] for r in values.values()})!=1:
            raise ValueError("unfair persistence sample")
    if len(groups)!=len(seeds)*len(QUANTILES):
        raise ValueError("missing selected cells")
    for seed in seeds:
        counts=[groups[(seed,q)]["joint_hard"]["n_selected"]
                for q,_ in QUANTILES]
        if not (counts[0]>=counts[1]>=counts[2]>=counts[3]):
            raise ValueError("non-nested selection")
        if any(groups[(seed,q)]["joint_hard"]["initial_weights_sha256"]!=
               x["trajectories"][list(seeds).index(seed)]["same_weights_sha256"]
               for q,_ in QUANTILES):
            raise ValueError("wrong model in postselection")
    return groups


def panel(reports,*,seeds=(20261025,20261026,20261027),
          steps=2000,allow_canary=False):
    done=set()
    grouped=defaultdict(list)
    diffs=defaultdict(list)
    cohorts=[]
    for x in reports:
        iv=x["interval"]
        if iv in done:raise ValueError("duplicate interval")
        done.add(iv)
        groups=validate(x,seeds=seeds,steps=steps,allow_canary=allow_canary)
        cohorts.append({"interval":iv,"train_count":x["train_count"],
                        "monitor_count":x["monitor_count"],
                        "train_sha":x["train_origins_sha256"],
                        "monitor_sha":x["monitor_origins_sha256"],
                        "code_sha":x["model_source_commit"]})
        for (seed,q),variants in groups.items():
            ref=variants["joint_hard"]
            for rule,r in variants.items():
                grouped[(iv,q,rule)].append(r)
                if rule!="joint_hard" and r["n_selected"]>0:
                    diffs[(iv,q,rule)].append({
                        m:r[m]-ref[m] for m in METRICS
                    })
    rows=[]
    for (iv,q,rule),items in sorted(grouped.items()):
        rec={"interval":iv,"threshold":q,"rule":rule,
             "n_models":len(items),
             "n_informative_seeds":sum(x["status"]=="INFORMATIVE" for x in items),
             "n_below_min_or_one_class":sum(x["status"]=="INSUFFICIENT_COVERAGE_OR_CLASS" for x in items),
             "n_empty":sum(x["status"]=="NO_COVERAGE" for x in items),
             "n_selected":summarize_numeric([x["n_selected"] for x in items]),
             "coverage":summarize_numeric([x["coverage"] for x in items]),
             "balanced_direction_accuracy":summarize_numeric([
                 x["balanced_direction_accuracy"] for x in items]),
             "status":"DESCRIPTIVE_NOT_INDEPENDENT",
             "threshold_bps":summarize_numeric([x["threshold_train_bps"] for x in items]),
             "brier_is_head_diagnostic_only_for_direct":rule=="signed_direct_mu"}
        for m in METRICS:
            rec[m]=summarize_numeric([x[m] for x in items])
        rows.append(rec)
    delta_rows=[]
    for (iv,q,rule),values in sorted(diffs.items()):
        out={"interval":iv,"threshold":q,"rule":rule,"vs":"joint_hard",
             "n_paired_nonempty_seeds":len(values)}
        for m in METRICS:out[m+"_delta"]=summarize_numeric([x[m] for x in values])
        delta_rows.append(out)
    return {
        "report":"TRAME_S3_1G_PRETRAINED_MAGNITUDE_GATES_V1",
        "n_models_trained":len(done)*len(seeds),
        "n_threshold_price_rule_scores":len(done)*len(seeds)*len(QUANTILES)*len(RULES),
        "trained_models_not_independent_time_series":True,
        "thresholds_train_predictions_only":True,
        "same_selected_cases_all_rules":True,
        "no_holdout_test":True,
        "external_dev_2022_2025_opened":False,
        "holdout_2026_opened":False,
        "no_cumulative_pnl":True,
        "cohorts":cohorts,"summary":rows,"paired_deltas":delta_rows,
    }


def markdown(panel):
    rows=["# S3.1G : performance conditionnelle aux mouvements prédits",
          "","Seuils q50/q75/q90 fittés sur |prédiction HARD| TRAIN uniquement.",
          "**Données monitor 2020–2021 exploratoires, aucun test indépendant**.",
          "BA = n/a si moins de 30 cas ou classe réelle absente.",""]
    for iv in ("D1","H1","M1"):
        a=[r for r in panel["summary"] if r["interval"]==iv]
        if not a:continue
        rows+=["## "+iv,"",
              "| Seuil | Règle | Couverture % | N cas | N graines BA valides | BA % | MAE $ | MAE bps | AMP bps | Persistance bps même cas |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in a:
            v=lambda k:r[k]["mean"]
            fmt=lambda k,p=3: f"{v(k):.{p}f}" if v(k) is not None else "n/a"
            rows.append(f"| {r['threshold']} | {r['rule']} | "
                        f"{100*v('coverage'):.1f} | "
                        f"{v('n_selected'):.0f} | "
                        f"{r['n_informative_seeds']}/3 | "
                        f"{100*v('balanced_direction_accuracy'):.2f}" if False else "")
            # format explicitly to avoid mixing nullable BA and non-null metrics
            rows.pop()
            ba=r["balanced_direction_accuracy"]["mean"]
            ba_str=f"{100*ba:.2f}" if ba is not None else "n/a"
            rows.append(f"| {r['threshold']} | {r['rule']} | "
                        f"{100*v('coverage'):.1f} | {v('n_selected'):.0f} | "
                        f"{r['n_informative_seeds']}/3 | {ba_str} | "
                        f"{fmt('mae_native_usd',2)} | "
                        f"{fmt('mae_bps_anchor')} | "
                        f"{fmt('absolute_magnitude_error_bps')} | "
                        f"{fmt('persistence_mae_bps_anchor')} |")
        rows+=["","Les groupes insuffisants ou vides sont explicites en JSON.",""]
    return "\n".join(rows)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",type=Path,nargs="+",required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--markdown",type=Path,required=True)
    a=p.parse_args(argv)
    if a.output.exists() or a.markdown.exists():p.error("refuse overwrite")
    r=panel([json.loads(x.read_text(encoding="utf-8")) for x in a.inputs])
    a.output.write_text(json.dumps(r,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    a.markdown.write_text(markdown(r),encoding="utf-8")

if __name__=="__main__":
    main()
