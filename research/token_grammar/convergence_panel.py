"""S3.1C pre2022 training-dynamics aggregation; no external-dev re-use."""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import mean,stdev

ARMS=("decoded","embedding_ordered","embedding_random")
STEPS=(200,800,2000)
METRICS=("balanced_direction_accuracy","direction_accuracy_all",
         "mae_native_usd","mae_bps_anchor",
         "absolute_magnitude_error_bps",
         "train_monitor_loss","internal_validation_monitor_loss",
         "gradient_norm_last50_mean_before_clip",
         "gradient_clipping_fraction_last50",
         "brier_skill_vs_train_prior")


def stats(v):
    return {"mean":float(mean(v)),"sd_seeds":float(stdev(v)) if len(v)>1 else None,
            "n":len(v)}


def validate(d):
    if (d.get("experiment")!="TRAME_S3_1C_PRE2022_CONVERGENCE_V1"
            or d.get("interval") not in ("D1","H1","M1")
            or d.get("data_origin") not in ("BTC_PUBLIC_REAL","ARTIFICIAL_FIXTURE")
            or d.get("external_development_2022_2025_accessed") is not False
            or d.get("labels_2026_opened") is not False
            or d.get("training_labels_before")!="2020-01-01"
            or d.get("internal_monitor_labels")!="2020-2021"
            or d.get("only_train_fits_vocabulary_normalizer_and_prior") is not True):
        raise ValueError("wrong study or leaked monitoring cohort")
    if d["data_origin"]=="BTC_PUBLIC_REAL":
        sha=d.get("model_source_commit","")
        if len(sha)!=40 or any(x not in "0123456789abcdef" for x in sha):
            raise ValueError("unverifiable source commit")
        if tuple(d.get("checkpoint_steps",()))!=STEPS:
            raise ValueError("real BTC must report all pre-registered checkpoints")
    if not d.get("results"):
        raise ValueError("no optimizer history rows")
    for r in d["results"]:
        if (r.get("arm") not in ARMS or r.get("mode")!="joint"
                or r.get("depth")!=1 or r.get("width")!=16
                or r.get("interval")!=d["interval"]
                or r.get("checkpoint_updates") not in d["checkpoint_steps"]
                or type(r.get("seed"))!=int
                or len(r.get("backbone_initial_sha256",""))!=64):
            raise ValueError("unmatched architecture/trajectory metadata")
        for k in METRICS:
            if type(r.get(k)) not in (float,int) or not math.isfinite(r[k]):
                raise ValueError("nonfinite "+k)


def build_panel(reports):
    if not reports:raise ValueError("missing horizons")
    seen=set()
    keyed=defaultdict(dict)
    summaries=defaultdict(list)
    cohorts=[]
    for d in reports:
        validate(d)
        key=(d["data_origin"],d["interval"])
        if key in seen:
            raise ValueError("duplicate horizon")
        seen.add(key)
        cohorts.append({
            "interval":d["interval"],"origin":d["data_origin"],
            "train":d["train_count"],"monitor":d["monitor_count"],
            "train_origins_sha256":d["train_origins_sha256"],
            "monitor_origins_sha256":d["monitor_origins_sha256"],
            "model_source_commit":d["model_source_commit"]
        })
        for r in d["results"]:
            key2=(d["interval"],r["seed"],r["checkpoint_updates"])
            if r["arm"] in keyed[key2]:
                raise ValueError("duplicate checkpoint/arm")
            keyed[key2][r["arm"]]=r
            summaries[(d["interval"],r["arm"],r["checkpoint_updates"])].append(r)
    deltas=defaultdict(list)
    for key,arms in keyed.items():
        if set(arms)!=set(ARMS):
            raise ValueError("incomplete 3-way checkpoint")
        if len({x["backbone_initial_sha256"] for x in arms.values()})!=1:
            raise ValueError("mismatched backbone")
        if not (arms["embedding_ordered"]["parameter_count"]==
                arms["embedding_random"]["parameter_count"]==
                arms["decoded"]["parameter_count"]+11):
            raise ValueError("undeclared embedding capacity")
        for arm,other in (("embedding_ordered","decoded"),
                          ("embedding_random","embedding_ordered")):
            delta={metric:arms[arm][metric]-arms[other][metric] for metric in METRICS}
            deltas[(key[0],key[2],arm,other)].append(delta)
    table=[]
    for (h,arm,step),rows in sorted(summaries.items()):
        x={"interval":h,"arm":arm,"step":step,
           "seeds":sorted({r["seed"] for r in rows}),"n_fits":len(rows),
           "monoclasse_99pct_fits":sum(r["monoclasse_99pct"] for r in rows),
           "predicted_up_percent":stats([r["predicted_up_percent"] for r in rows]),
           "embedding_extra_params":rows[0]["learned_embedding_parameters"]}
        for k in METRICS:x[k]=stats([r[k] for r in rows])
        table.append(x)
    contrasts=[]
    for (h,step,arm,ref),rows in sorted(deltas.items()):
        x={"interval":h,"checkpoint":step,"arm":arm,
           "reference":ref,"n_paired_seeds":len(rows),
           "equal_trainable_params":ref!="decoded"}
        for k in METRICS:x[k+"_delta"]=stats([r[k] for r in rows])
        contrasts.append(x)
    n_traj=len({(h,seed,arm) for (h,seed,step),arms in keyed.items() for arm in arms})
    return {"report":"TRAME_S3_1C_PRE2022_OPTIMIZER_DIAGNOSTICS_V1",
            "n_trajectories":n_traj,"n_checkpoint_rows":sum(len(x) for x in keyed.values()),
            "external_2022_2025_used":False,"holdout_2026_used":False,
            "not_independent_test":True,"no_cumulative_trading_return":True,
            "cohorts":cohorts,"summary":table,"paired_deltas":contrasts}


def markdown(d):
    out=["# TRAME S3.1C — convergence interne 200/800/2000 updates","",
        "**Only pre2020 TRAIN / 2020-21 MONITOR. External dev 2022-25 AND 2026 unused.**",
        "Checkpoints d'un même entraînement, pas des runs indépendants.",""]
    for h in ("D1","H1","M1"):
        xs=[r for r in d["summary"] if r["interval"]==h]
        if not xs:continue
        out+=["## "+h,"",
          "| Bras | Updates | Seeds | BA % | MAE $ | MAE bps | Erreur amplitude bps | UP % | Monoclasse | Loss TRAIN | Loss monitor | Grad norm | Brier skill |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for r in xs:
            m=lambda key:r[key]["mean"]
            out.append(
                f"| {r['arm']} | {r['step']} | {r['n_fits']} | "
                f"{100*m('balanced_direction_accuracy'):.2f} | "
                f"{m('mae_native_usd'):.2f} | {m('mae_bps_anchor'):.3f} | "
                f"{m('absolute_magnitude_error_bps'):.3f} | "
                f"{m('predicted_up_percent'):.1f} | "
                f"{r['monoclasse_99pct_fits']}/{r['n_fits']} | "
                f"{m('train_monitor_loss'):.5f} | "
                f"{m('internal_validation_monitor_loss'):.5f} | "
                f"{m('gradient_norm_last50_mean_before_clip'):.3f} | "
                f"{m('brier_skill_vs_train_prior'):.5f} |")
        out+=["","Les deltas appariés détaillés se trouvent dans le JSON.",""]
    return "\n".join(out)+"\n"


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--inputs",nargs="+",type=Path,required=True)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--markdown",required=True,type=Path)
    a=p.parse_args(argv)
    if a.output.exists() or a.markdown.exists():
        p.error("will not overwrite scientific artifact")
    result=build_panel([json.loads(x.read_text()) for x in a.inputs])
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    a.markdown.write_text(markdown(result))


if __name__=="__main__":
    main()
