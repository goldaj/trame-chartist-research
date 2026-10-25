"""A8 synthetic evidence dashboard adversarial tests, standard library only."""
import json
from pathlib import Path
import tempfile
import unittest

from research.trame_lab.evidence_report import read_report, render, write_output


def fixture_a5():
    return {
        "experiment": "a5_attention_gru_control_paired_synthetic_v0.1",
        "data_origin": "ARTIFICIAL_ONLY",
        "reserved_synthetic_test_opened": False,
        "financial_holdout_opened": False,
        "compute_matched": False,
        "hybrid_is_selective_ssm": False,
        "results": [
            {"architecture": name, "seed": seed, "parameters": 4000,
             "development_nll": 2.8 + i/100 + seed/100000}
            for i, name in enumerate((
                "legacy_causal_transformer", "modern_gpt_style_mini",
                "recurrent_gru_control", "attention_gru_hybrid_control"))
            for seed in (10, 11, 12)
        ],
    }


def fixture_a3c():
    data = fixture_a5()
    data["experiment"] = "trame_a3c_proxy_budget_synthetic_pilot_v0.1"
    data["data_origin"] = "ARTIFICIAL_TRAIN_AND_DEVELOPMENT"
    data["true_compute_matched"] = False
    data["flops_coverage_complete"] = False
    data["results"] = [
        {**row, "parameter_count": row["parameters"]}
        for row in data["results"] if row["architecture"] != "attention_gru_hybrid_control"
    ]
    return data


class EvidenceDashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def _write(self, name, data):
        path = self.home / name
        path.write_text(json.dumps(data, allow_nan=False), encoding="utf-8")
        return path

    def test_separate_protocols_never_cross_ranked(self):
        a = self._write("a.json", fixture_a3c())
        b = self._write("b.json", fixture_a5())
        report, html = render([a, b])
        self.assertEqual(len(report["panels"]), 2)
        self.assertTrue(report["no_cross_protocol_ranking"])
        self.assertTrue(report["source_files_not_cryptographically_verified"])
        self.assertFalse(report["panels"][1]["full_compute_fairness_proven"])
        self.assertIn("ARTIFICIELLES", html)
        self.assertIn("protocoles différents", html)

    def test_html_escapes_untrusted_filename(self):
        bad = self._write("evil-<script>alert(1)</script>.json".replace("/", "_"), fixture_a5())
        _, html = render([bad])
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_output_and_companion_never_overwritten(self):
        a = self._write("a.json", fixture_a3c())
        report = self.home / "demo.html"
        one, two = write_output(input_files=[a], output=report)
        self.assertTrue(one.exists())
        self.assertTrue(two.exists())
        with self.assertRaises(FileExistsError):
            write_output(input_files=[a], output=report)
        self.assertTrue(json.loads(two.read_text(encoding="utf-8"))["not_a_trading_signal"])

    def test_reject_invalid_status_and_duplicate_seed(self):
        data = fixture_a5()
        data["compute_matched"] = True
        with self.assertRaises(ValueError):
            read_report(self._write("false.json", data))
        data = fixture_a5()
        data["results"].append(data["results"][0])
        with self.assertRaises(ValueError):
            read_report(self._write("dup.json", data))
        data = fixture_a5()
        data["reserved_synthetic_test_opened"] = True
        with self.assertRaises(ValueError):
            read_report(self._write("holdout.json", data))
        data = fixture_a3c()
        data["flops_coverage_complete"] = True
        with self.assertRaises(ValueError):
            read_report(self._write("false_flops.json", data))

    def test_reject_wrong_schema_nan_and_unbalanced_arms(self):
        data = fixture_a3c()
        data["data_origin"] = "REAL_BTC"
        with self.assertRaises(ValueError):
            read_report(self._write("fake_real.json", data))
        data = fixture_a3c()
        data["results"][0]["development_nll"] = -4.0
        with self.assertRaises(ValueError):
            read_report(self._write("nll.json", data))
        data = fixture_a3c()
        data["results"].pop()
        with self.assertRaises(ValueError):
            read_report(self._write("missing.json", data))
        evil = self.home / "nan.json"
        evil.write_text(json.dumps(fixture_a3c()).replace("2.8", "NaN", 1),
                        encoding="utf-8")
        with self.assertRaises(ValueError):
            read_report(evil)


if __name__ == "__main__":
    unittest.main()
