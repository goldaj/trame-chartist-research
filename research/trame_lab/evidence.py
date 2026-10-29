"""TRAME A8: strictly labelled, offline read-only exploratory evidence report.

Consumes *locally supplied* JSON reports. Does not fetch, train, trade,
unlock a holdout, or certify authenticity of supplied report fields.
Only whitelisted research artefact shapes can be displayed.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path
from tempfile import NamedTemporaryFile


KINDS = {
    "TRAME_A3c_partial_compute_accounting_v0.1": "synthetic_cost_partial",
    "trame_a3c_proxy_budget_synthetic_pilot_v0.1": "synthetic_proxy_budget",
    "a5_attention_gru_control_paired_synthetic_v0.1": "synthetic_hybrid_control",
    "btc_training_only_statistical_baselines_v0.1": "btc_exploratory_baselines",
}
ORIGINS = {
    "synthetic_cost_partial": "ARTIFICIAL_COST_ONLY",
    "synthetic_proxy_budget": "ARTIFICIAL_TRAIN_AND_DEVELOPMENT",
    "synthetic_hybrid_control": "ARTIFICIAL_ONLY",
}


def _finite(value, label, *, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    if positive and value <= 0:
        raise ValueError(f"{label} must be positive")
    return value


def _rows_from_payload(data):
    if not isinstance(data, dict) or data.get("experiment") not in KINDS:
        raise ValueError("unrecognized research report schema")
    kind = KINDS[data["experiment"]]
    if kind != "btc_exploratory_baselines":
        if data.get("data_origin") != ORIGINS[kind]:
            raise ValueError("synthetic origin mismatch")
        if data.get("reserved_synthetic_test_opened") is not False:
            raise ValueError("reserved synthetic holdout is not permitted")
        if data.get("financial_holdout_opened", False) is not False:
            raise ValueError("financial holdout must not be opened")
        if data.get("compute_matched", False) is not False:
            raise ValueError("cannot import claimed compute-matched result")
        if data.get("flops_coverage_complete", False) is not False:
            raise ValueError("partial cost instrument may not claim complete FLOPs")
        if data.get("true_compute_matched", False) is not False:
            raise ValueError("true compute parity was not demonstrated")
        if data.get("tuning_compute_equalized", False) is not False:
            raise ValueError("tuning compute was not equalized")
        if (kind == "synthetic_hybrid_control" and
                data.get("hybrid_is_selective_ssm") is not False):
            raise ValueError("GRU control may not be reported as selective SSM")
        results = data.get("results")
        if not isinstance(results, list) or not results or len(results) > 500:
            raise ValueError("research results must contain 1..500 records")
        output = []
        seen = set()
        for item in results:
            if not isinstance(item, dict) or not isinstance(item.get("architecture"), str):
                raise ValueError("architecture id required")
            arm = item["architecture"]
            if not arm or len(arm) > 96:
                raise ValueError("invalid architecture id")
            if kind == "synthetic_cost_partial":
                context = item.get("context_tokens")
                width = item.get("width")
                if type(context) is not int or context < 1 or type(width) is not int or width < 1:
                    raise ValueError("positive context/width required")
                metric = "CPU forward+backward median (ms)"
                value = item.get("train_step_median_ms_unprofiled")
                key = (arm, context, width)
                descriptor = f"{arm} / width {width} / context {context}"
            else:
                seed = item.get("seed")
                if type(seed) is not int:
                    raise ValueError("integer seed required")
                metric = "Synthetic development NLL"
                value = item.get("development_nll")
                key = (arm, seed)
                descriptor = f"{arm} / seed {seed}"
            if key in seen:
                raise ValueError("duplicate arm/context or arm/seed row")
            seen.add(key)
            _finite(value, metric, positive=True)
            output.append({"label": descriptor, "metric": metric, "value": value})
        return kind, output
    # BTC output is only ever labelled exploratory. We cannot prove its original
    # bytes, causal splits or data rights solely by validating a JSON file.
    if (data.get("not_confirmatory") is not True
            or data.get("2026_test_quarantined") is not True
            or data.get("not_hyperliquid_execution") is not True
            or data.get("model_selection_using_development") is not False
            or not isinstance(data.get("fit"), dict)
            or data["fit"].get("fitted_using_development") is not False
            or data.get("interval") not in ("H1", "M1")):
        raise ValueError("BTC report must retain all exploration/holdout limitations")
    baselines = data.get("baselines")
    if not isinstance(baselines, dict) or set(baselines) != {
        "persistence", "ridge_three_past_only_features"}:
        raise ValueError("BTC report must contain persistence and Ridge")
    output = []
    for name in sorted(baselines):
        record = baselines[name]
        if not isinstance(record, dict):
            raise ValueError("invalid baseline data")
        for metric in ("mae_native_usd", "rmse_native_usd", "coverage_80pct"):
            value = _finite(record.get(metric), metric)
            if metric == "coverage_80pct" and not 0 <= value <= 1:
                raise ValueError("coverage outside [0,1]")
            if metric != "coverage_80pct" and value < 0:
                raise ValueError("negative error")
            output.append({"label": f"{data['interval']} / {name}",
                           "metric": metric, "value": value})
    return kind, output


def collect_evidence(paths):
    """Read at most 12 small local reports with stable content hashes."""
    if not isinstance(paths, (list, tuple)) or not 1 <= len(paths) <= 12:
        raise ValueError("provide 1..12 local JSON report paths")
    sources, rows, seen = [], [], set()
    for input_path in paths:
        path = Path(input_path)
        if path.is_symlink() or not path.is_file():
            raise ValueError("source must be an existing regular non-symlink file")
        if path.stat().st_size > 8_000_000:
            raise ValueError("source report too large")
        raw = path.read_bytes()
        fingerprint = hashlib.sha256(raw).hexdigest()
        if fingerprint in seen:
            raise ValueError("duplicate source bytes")
        seen.add(fingerprint)
        data = json.loads(raw.decode("utf-8"), parse_constant=lambda s:
                          (_ for _ in ()).throw(ValueError("invalid JSON number")))
        kind, metrics = _rows_from_payload(data)
        sources.append({"sha256": fingerprint, "kind": kind,
                        "source_authenticity_independently_verified": False,
                        "reported_metrics_count": len(metrics)})
        for metric in metrics:
            rows.append({"source_sha256": fingerprint, "kind": kind, **metric})
    return {
        "schema": "TRAME_EXPLORATORY_EVIDENCE_V1",
        "reports_are_untrusted_locally_supplied_inputs": True,
        "true_compute_parity_established": False,
        "financial_skill_established": False,
        "independent_holdout_validated": False,
        "trading_enabled": False,
        "sources": sources,
        "metrics": rows,
    }


def render_evidence(evidence):
    """Accessible static report. Escape every external label; no JS or CDN."""
    if evidence.get("schema") != "TRAME_EXPLORATORY_EVIDENCE_V1":
        raise ValueError("wrong evidence schema")
    if (evidence.get("true_compute_parity_established") is not False
            or evidence.get("financial_skill_established") is not False
            or evidence.get("independent_holdout_validated") is not False):
        raise ValueError("unsafe evidence claim")
    rows = []
    for record in evidence["metrics"]:
        val = _finite(record["value"], "metric")
        rows.append("<tr><td>{}</td><td>{}</td><td>{}</td><td>{:.6g}</td></tr>".format(
            html.escape(record["kind"]), html.escape(record["label"]),
            html.escape(record["metric"]), val))
    sources = "\n".join(
        f"<li>{html.escape(x['kind'])}: <code>{html.escape(x['sha256'])}</code></li>"
        for x in evidence["sources"])
    return """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>TRAME | preuves exploratoires</title>
<style>body{background:#101825;color:#e5eef7;font:16px/1.6 system-ui;
max-width:1100px;margin:auto;padding:24px}a{color:#9fd4ff}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{text-align:left;border-bottom:1px solid #5b6a7e;padding:8px}
th{color:#b5dfff}code{overflow-wrap:anywhere}caption{text-align:left;
font-weight:bold;margin:12px 0}.warning{border:1px solid #ad8e5e;
padding:16px;margin:16px 0}main{overflow-wrap:anywhere}</style></head>
<body><main><h1>TRAME : résultats de recherche exploratoire</h1>
<div class="warning"><strong>AUCUNE PREUVE DE RENTABILITÉ OU DE MODÈLE GAGNANT.</strong>
Données synthétiques ou rapports BTC exploratoires fournis localement.
Les compteurs FLOPs partiels ne démontrent pas une comparaison équitable.
Les données BTC ne démontrent pas une validation indépendante.
Ce rapport ne permet aucun ordre de trading.</div>
<table><caption>Mesures importées, par source et horizon</caption>
<thead><tr><th>Type</th><th>Architecture ou témoin</th>
<th>Métrique</th><th>Valeur</th></tr></thead><tbody>""" + "\n".join(rows) + """</tbody></table>
<h2>Empreintes SHA-256 des fichiers JSON reçus</h2><ul>""" + sources + """</ul>
<p>Les empreintes identifient les fichiers importés mais ne certifient
ni la véracité de leurs contenus ni les droits, ni l'indépendance des tests.</p>
</main></body></html>"""


def write_evidence(evidence, destination, *, overwrite=False):
    """Stage both outputs first; two replacements are NOT one atomic transaction."""
    path = Path(destination)
    if path.suffix.lower() != ".html" or not path.parent.is_dir():
        raise ValueError("output must be .html in an existing directory")
    companion = path.with_suffix(".json")
    if (path.exists() or companion.exists()) and not overwrite:
        raise FileExistsError("report exists; opt into overwrite")
    # Fully validate/render BEFORE staging or changing existing output.
    html_body = render_evidence(evidence)
    json_body = json.dumps(evidence, indent=2, allow_nan=False, ensure_ascii=False) + "\n"
    staged = []
    try:
        for target, body in ((companion, json_body), (path, html_body)):
            with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                   prefix="." + target.name + ".",
                                   suffix=".tmp", delete=False) as f:
                staged.append(Path(f.name))
                f.write(body)
        staged[0].replace(companion)
        staged[1].replace(path)
    finally:
        for tmp in staged:
            tmp.unlink(missing_ok=True)
    return str(path), str(companion)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline TRAME research evidence viewer")
    parser.add_argument("--input", nargs="+", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    report = collect_evidence(args.input)
    one, other = write_evidence(report, args.output, overwrite=args.overwrite)
    print(f"Exploratory research only. HTML: {one}; JSON: {other}")


if __name__ == "__main__":
    main()
