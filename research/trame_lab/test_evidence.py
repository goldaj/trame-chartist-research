"""Offline evidence import tests: labels, provenance hashes, safe HTML, no live claims."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from research.trame_lab.evidence import (
    collect_evidence, render_evidence, write_evidence,
)


def cost():
    return {
        "experiment": "TRAME_A3c_partial_compute_accounting_v0.1",
        "data_origin": "ARTIFICIAL_COST_ONLY",
        "reserved_synthetic_test_opened": False,
        "financial_holdout_opened": False,
        "compute_matched": False,
        "flops_coverage_complete": False,
        "results": [{
            "architecture": 'hybrid<script>alert("test")</script>',
            "width": 16, "context_tokens": 20,
            "train_step_median_ms_unprofiled": 2.25
        }]
    }


def budget():
    return {
        "experiment": "trame_a3c_proxy_budget_synthetic_pilot_v0.1",
        "data_origin": "ARTIFICIAL_TRAIN_AND_DEVELOPMENT",
        "reserved_synthetic_test_opened": False,
        "financial_holdout_opened": False,
        "flops_coverage_complete": False,
        "true_compute_matched": False,
        "results": [{"architecture": "gru", "seed": 2026,
                     "development_nll": 2.9}]
    }


def btc():
    return {
        "experiment": "btc_training_only_statistical_baselines_v0.1",
        "2026_test_quarantined": True,
        "not_confirmatory": True,
        "not_hyperliquid_execution": True,
        "model_selection_using_development": False,
        "fit": {"fitted_using_development": False},
        "interval": "H1",
        "baselines": {
            name: {"mae_native_usd": 40.1, "rmse_native_usd": 52.2,
                   "coverage_80pct": .6}
            for name in ("persistence", "ridge_three_past_only_features")
        },
    }


class EvidenceTests(unittest.TestCase):
    def put(self, folder, name, data):
        path = Path(folder) / name
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_all_three_sources_remain_exploratory(self):
        with tempfile.TemporaryDirectory() as tmp:
            sources = [
                self.put(tmp, "cost.json", cost()),
                self.put(tmp, "budget.json", budget()),
                self.put(tmp, "btc.json", btc()),
            ]
            report = collect_evidence(sources)
            self.assertEqual(report["schema"], "TRAME_EXPLORATORY_EVIDENCE_V1")
            self.assertEqual(len(report["sources"]), 3)
            self.assertEqual(len(report["metrics"]), 8)
            self.assertFalse(report["financial_skill_established"])
            self.assertFalse(report["independent_holdout_validated"])
            for item, source in zip(report["sources"], sources):
                self.assertEqual(item["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
                self.assertFalse(item["source_authenticity_independently_verified"])
            rendered = render_evidence(report)
            self.assertIn("AUCUNE PREUVE DE RENTABILITÉ", rendered)
            self.assertIn("&lt;script&gt;", rendered)
            self.assertNotIn("<script>", rendered)
            self.assertIn("<caption>Mesures importées", rendered)

    def test_reject_false_holdout_or_compute_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            invalid = [
                ("data_origin", "REAL"),
                ("reserved_synthetic_test_opened", True),
                ("financial_holdout_opened", True),
                ("compute_matched", True),
                ("flops_coverage_complete", True),
            ]
            for key, val in invalid:
                with self.subTest(key=key):
                    bad = cost()
                    bad[key] = val
                    path = self.put(tmp, "bad.json", bad)
                    with self.assertRaises(ValueError):
                        collect_evidence([path])
            self.put(tmp, "bad.json", {**cost(), "results": [
                {**cost()["results"][0], "train_step_median_ms_unprofiled": float("nan")}]})
            with self.assertRaises(ValueError):
                collect_evidence([Path(tmp)/"bad.json"])

    def test_reject_development_fit_and_independent_2026_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            for field, value in [
                ("2026_test_quarantined", False),
                ("not_confirmatory", False),
                ("not_hyperliquid_execution", False),
                ("model_selection_using_development", True),
            ]:
                bad = btc()
                bad[field] = value
                with self.subTest(field=field), self.assertRaises(ValueError):
                    collect_evidence([self.put(tmp, "badbtc.json", bad)])
            bad = btc()
            bad["fit"]["fitted_using_development"] = True
            with self.assertRaises(ValueError):
                collect_evidence([self.put(tmp, "badbtc.json", bad)])

    def test_write_html_json_and_guard_against_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = collect_evidence([self.put(tmp, "input.json", budget())])
            destination = Path(tmp)/"out.html"
            htmlpath, jsonpath = write_evidence(data, destination)
            self.assertTrue(Path(htmlpath).is_file())
            self.assertEqual(json.loads(Path(jsonpath).read_text())["schema"],
                             "TRAME_EXPLORATORY_EVIDENCE_V1")
            previous = destination.read_bytes()
            with self.assertRaises(FileExistsError):
                write_evidence(data, destination)
            self.assertEqual(previous, destination.read_bytes())
            write_evidence(data, destination, overwrite=True)
            self.assertEqual(previous, destination.read_bytes())
            self.assertFalse(list(Path(tmp).glob("*.tmp")))

    def test_duplicate_sources_rejected_and_claims_cannot_be_rendered(self):
        with tempfile.TemporaryDirectory() as tmp:
            item = self.put(tmp, "x.json", cost())
            with self.assertRaises(ValueError):
                collect_evidence([item, item])
        bad_report = {
            "schema": "TRAME_EXPLORATORY_EVIDENCE_V1",
            "financial_skill_established": True,
            "true_compute_parity_established": False,
            "independent_holdout_validated": False,
        }
        with self.assertRaises(ValueError):
            render_evidence(bad_report)


if __name__ == "__main__":
    unittest.main()
