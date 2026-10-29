"""P1 checkpoint and P2 causal-development diagnostics adversarial tests."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
import tempfile
import unittest

from research.predictive_product.checkpoint_contract import validate_manifest
from research.predictive_product.development_diagnostics import (
    ForecastRecord, development_diagnostics,
)


def fixture_manifest(content=b"opaque artifact"):
    return {
        "source_release": "btcusd-bitstamp-2010-2026-reference-v1",
        "source_resolution": "H1",
        "split_version": "btc-pre2022-dev2022-2025-v1",
        "origin_policy": "close-known-at-decision-time-only",
        "architecture": "research-mini-transformer",
        "representation": "quantized-log-return-P1-B0",
        "objective": "rounded-Gaussian-BASENLL",
        "seed": 20261025,
        "hardware": "research-cpu",
        "environment": "python3.12-cpu",
        "train_budget": 12,
        "search_budget": 0,
        "code_commit": "a" * 40,
        "train_only_transforms": True,
        "artifact_sha256": hashlib.sha256(content).hexdigest(),
        "weight_license": "research-unreviewed",
        "independent_test_opened": False,
    }


def rows(n=20):
    start=datetime(2023,1,1,tzinfo=timezone.utc)
    out=[]
    for i in range(n):
        origin=start+timedelta(hours=i)
        out.append(ForecastRecord(
            origin_utc=origin, target_utc=origin+timedelta(hours=1),
            prediction_available_utc=origin,
            label_available_utc=origin+timedelta(hours=1),
            q10_usd=90., q50_usd=100., q90_usd=110.,
            actual_usd=98.+(i%5),
            context_contiguous_at_origin=True,
            in_training_support_at_origin=True))
    return out


class P1P2ControlsTests(unittest.TestCase):
    def test_manifest_schema_requires_pinned_reference_and_unopened_test(self):
        report=validate_manifest(fixture_manifest())
        self.assertEqual(len(report["manifest_sha256"]),64)
        self.assertFalse(report["ready_for_production"])
        self.assertFalse(report["training_run_independently_verified"])
        self.assertFalse(report["checkpoint_bytes_match_declared_sha256"])
        for field, bad in [
            ("source_release", "latest"),
            ("independent_test_opened", True),
            ("train_only_transforms", False),
            ("code_commit", "not-a-commit"),
            ("artifact_sha256", "invalid"),
            ("train_budget", 0),
            ("seed", True),
        ]:
            m=fixture_manifest()
            m[field]=bad
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_manifest(m)

    def test_checkpoint_bytes_hashed_not_deserialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"dummy.safetensors"
            path.write_bytes(b"opaque artifact")
            verified=validate_manifest(fixture_manifest(), checkpoint_path=path)
            self.assertTrue(verified["checkpoint_bytes_match_declared_sha256"])
            self.assertFalse(verified["model_skill_independently_verified"])
            path.write_bytes(b"altered")
            with self.assertRaisesRegex(ValueError, "sha256"):
                validate_manifest(fixture_manifest(), checkpoint_path=path)
            bad=Path(tmp)/"weights.pkl"
            bad.write_bytes(b"opaque artifact")
            with self.assertRaises(ValueError):
                validate_manifest(fixture_manifest(), checkpoint_path=bad)

    def test_quantile_coverage_and_predeclared_abstention(self):
        records=rows()
        records[2]=replace(records[2], context_contiguous_at_origin=False)
        records[3]=replace(records[3], in_training_support_at_origin=False)
        report=development_diagnostics(records, split="btc_development")
        self.assertEqual(report["forecasts_not_abstained"],18)
        self.assertEqual(report["abstained_due_to_missing_context"],1)
        self.assertEqual(report["abstained_due_to_training_support"],1)
        self.assertEqual(report["empirical_80pct_coverage"],1.0)
        self.assertEqual(report["horizon_seconds"],3600)
        self.assertFalse(report["calibration_independently_verified"])
        self.assertFalse(report["holdout_opened_by_diagnostics"])

    def test_reject_future_prediction_and_heldout_2026(self):
        data=rows()
        invalid=[
            replace(data[0], prediction_available_utc=data[0].origin_utc+timedelta(seconds=1)),
            replace(data[0], target_utc=data[0].origin_utc),
            replace(data[0], q10_usd=105, q50_usd=100),
            replace(data[0], context_contiguous_at_origin=1),
            replace(data[0], origin_utc=data[0].origin_utc.replace(tzinfo=None)),
        ]
        for item in invalid:
            with self.subTest(item=item), self.assertRaises(ValueError):
                development_diagnostics([item]+data[1:])
        bad=replace(data[0], target_utc=datetime(2026,1,2,tzinfo=timezone.utc))
        with self.assertRaises(ValueError):
            development_diagnostics([bad]+data[1:], split="btc_development")
        with self.assertRaises(ValueError):
            development_diagnostics(data, split="independent_test")
        data[1]=replace(data[1], target_utc=data[1].target_utc+timedelta(hours=1))
        with self.assertRaises(ValueError):
            development_diagnostics(data)


if __name__ == "__main__":
    unittest.main()
