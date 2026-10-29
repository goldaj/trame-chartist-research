"""Offline evidence digest for TRAME CPU synthetic architecture experiments.

No internet, wallets, model downloads or private Bitcoin archives.
The report does not merge NLL across protocols, certify source integrity
or declare an experimental architecture winner.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from html import escape
import hashlib
import json
import math
from pathlib import Path
import statistics


SPECS = {
    "trame_a3c_proxy_budget_synthetic_pilot_v0.1": {
        "origin": "ARTIFICIAL_TRAIN_AND_DEVELOPMENT",
        "arms": ("legacy_causal_transformer", "modern_gpt_style_mini",
                 "recurrent_gru_control"),
        "params": "parameter_count",
        "warning": ("Measured-operator budget proxy only. FLOPs, "
                    "memory and tuning are NOT fully equalized."),
    },
    "a5_attention_gru_control_paired_synthetic_v0.1": {
        "origin": "ARTIFICIAL_ONLY",
        "arms": ("legacy_causal_transformer", "modern_gpt_style_mini",
                 "recurrent_gru_control", "attention_gru_hybrid_control"),
        "params": "parameters",
        "warning": ("Same step count but parameters, FLOPs and "
                    "hyperparameter tuning NOT matched. Hybrid is GRU, not Mamba."),
    },
}


def _reject_constant(value):
    raise ValueError(f"not a finite JSON number: {value}")


def read_report(path):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        raise ValueError("input must be a regular JSON file")
    if path.stat().st_size > 5_000_000:
        raise ValueError("refusing oversized JSON evidence input")
    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file, parse_constant=_reject_constant)
    if not isinstance(raw, dict):
        raise ValueError("JSON experiment object required")
    kind = raw.get("experiment")
    if not isinstance(kind, str) or kind not in SPECS:
        raise ValueError("unknown or unapproved experiment type")
    spec = SPECS[kind]
    if raw.get("data_origin") != spec["origin"]:
        raise ValueError("experiment provenance mismatch")
    if (raw.get("reserved_synthetic_test_opened") is not False
            or raw.get("financial_holdout_opened") is not False):
        raise ValueError("test or financial holdout must remain unopened")
    if kind.startswith("trame_a3c"):
        if (raw.get("true_compute_matched") is not False
                or raw.get("flops_coverage_complete") is not False):
            raise ValueError("false compute fairness claim")
    elif (raw.get("compute_matched") is not False
          or raw.get("hybrid_is_selective_ssm") is not False):
        raise ValueError("false hybrid/compute equivalence claim")
    rows = raw.get("results")
    if not isinstance(rows, list) or len(rows) < len(spec["arms"]) * 3:
        raise ValueError("at least three seeds per architecture required")
    seen = set()
    by_arm = defaultdict(list)
    seeds = defaultdict(set)
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("result object required")
        name, seed = row.get("architecture"), row.get("seed")
        if not isinstance(name, str) or name not in spec["arms"] or type(seed) is not int:
            raise ValueError("unknown arm or invalid seed")
        pair = (name, seed)
        if pair in seen:
            raise ValueError("duplicate seed/architecture result")
        seen.add(pair)
        loss = row.get("development_nll")
        if kind.startswith("trame_a3c"):
            loss = row.get("development_nll")
        nparam = row.get(spec["params"])
        if (type(loss) not in (float, int) or not math.isfinite(loss)
                or loss < 0 or type(nparam) is not int or nparam < 1):
            raise ValueError("invalid development NLL or parameter count")
        by_arm[name].append(float(loss))
        seeds[name].add(seed)
    seed_sets = [seeds[name] for name in spec["arms"]]
    if any(len(seed_set) < 3 or seed_set != seed_sets[0] for seed_set in seed_sets):
        raise ValueError("all arms must have at least three identical paired seeds")
    return {
        "experiment": kind,
        "data_origin": spec["origin"],
        "origin_file": path.name,
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "independent_financial_evidence": False,
        "full_compute_fairness_proven": False,
        "source_integrity_verified": False,
        "warnings": spec["warning"],
        "seeds": sorted(seed_sets[0]),
        "rows": [{
            "architecture": name, "n": len(by_arm[name]),
            "mean_development_nll": statistics.mean(by_arm[name]),
            "sd_development_nll": statistics.stdev(by_arm[name]),
        } for name in spec["arms"]],
    }


def render(inputs):
    if not isinstance(inputs, (list, tuple)) or not inputs:
        raise ValueError("at least one report input required")
    panels = [read_report(p) for p in inputs]
    if len({p["experiment"] for p in panels}) != len(panels):
        raise ValueError("duplicate experiment type")
    digest = {
        "title": "TRAME research evidence, synthetic exploratory only",
        "no_financial_validation": True, "not_a_trading_signal": True,
        "no_cross_protocol_ranking": True,
        "source_files_not_cryptographically_verified": True,
        "panels": panels,
    }
    sections = []
    for panel in panels:
        title = escape(panel["experiment"])
        body_rows = "".join(
            "<tr><th scope='row'>" + escape(row["architecture"]) + "</th>"
            f"<td>{row['n']}</td>"
            f"<td>{row['mean_development_nll']:.6f}</td>"
            f"<td>{row['sd_development_nll']:.6f}</td></tr>"
            for row in panel["rows"])
        sections.append(
            "<section><h2>" + title + "</h2><p>"
            + escape(panel["warnings"]) + "</p><p>Source input: "
            + escape(panel["origin_file"]) + " (SHA-256 fingerprint recorded, origin unverified). "
            + "Artificial training/development data only.</p>"
            + "<table><caption>Within-protocol exploratory development NLL; "
            + "lower is not proof of generalization</caption>"
            + "<thead><tr><th scope='col'>Architecture</th><th scope='col'>Seeds</th>"
            + "<th scope='col'>Mean NLL</th><th scope='col'>SD</th></tr></thead>"
            + "<tbody>" + body_rows + "</tbody></table></section>")
    html = ("<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>TRAME exploratory synthetic evidence</title>"
            "<style>body{font:1rem system-ui;max-width:78rem;margin:auto;padding:2rem;"
            "line-height:1.5}table{border-collapse:collapse;width:100%;margin:1rem 0}"
            "td,th{padding:.65rem;border:1px solid #777;text-align:left}"
            "caption{font-weight:bold;margin:.5rem}section{margin:2rem 0}</style>"
            "</head><body><main><h1>TRAME: données ARTIFICIELLES uniquement</h1>"
            "<p>Expériences exploratoires, <strong>pas de preuve financière, "
            "pas de test indépendant, pas de recommandations de trading</strong>. "
            "Ces tableaux utilisent des protocoles différents et ne doivent "
            "pas être classés ensemble. La provenance cryptographique des "
            "fichiers d'entrée n'est pas contrôlée.</p>"
            + "".join(sections) + "</main></body></html>\n")
    return digest, html


def write_output(*, input_files, output):
    output = Path(output)
    if output.suffix.lower() != ".html":
        raise ValueError("output filename must end in .html")
    companion = output.with_suffix(".json")
    if output.exists() or companion.exists():
        raise FileExistsError("refuse to overwrite existing report or JSON companion")
    digest, html = render(input_files)
    # Two-file replacement is NOT atomic. Roll back an initial output
    # if creating the companion fails. Never overwrite existing files.
    try:
        with output.open("x", encoding="utf-8") as file:
            file.write(html)
        with companion.open("x", encoding="utf-8") as file:
            json.dump(digest, file, indent=2, ensure_ascii=False, allow_nan=False)
            file.write("\n")
    except Exception:
        if output.exists() and not companion.exists():
            output.unlink()
        raise
    return output, companion


def main(argv=None):
    parser = argparse.ArgumentParser(description="TRAME offline exploratory report")
    parser.add_argument("--input", action="append", dest="inputs", required=True,
                        type=Path, help="JSON artifacts, repeat option")
    parser.add_argument("--output", type=Path, required=True)
    ns = parser.parse_args(argv)
    html, companion = write_output(input_files=ns.inputs, output=ns.output)
    print(f"Synthetic-only HTML: {html}; JSON: {companion}")


if __name__ == "__main__":
    main()
