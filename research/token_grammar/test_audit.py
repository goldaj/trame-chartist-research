"""S3.0c: fabricated contextual returns, never a BTC result."""
from dataclasses import replace
from math import floor
import unittest

from research.continuous_direction.test_continuous import fabricated_case
from research.token_grammar.audit import run_cases


def cases(year):
    items=[]
    for index in range(40):
        c=fabricated_case(year,index)
        past=tuple(
            ((-1)**(index+j)) * (0.01 + ((index*20+j)%97)*0.173)
            for j in range(20))
        items.append(replace(
            c,continuous_past_bps=past,
            encoded_past=tuple(floor(v/10+0.5) for v in past)))
    return items


class TokenAuditFixtures(unittest.TestCase):
    def test_train_only_vocabulary_and_four_grammar_diagnostics(self):
        report=run_cases(cases(2018),cases(2023),interval="D1",
                         data_origin="ARTIFICIAL_FIXTURE")
        self.assertEqual(report["experiment"],"TRAME_S3_TOKEN_INFORMATION_AUDIT_V1")
        self.assertFalse(report["model_trained"])
        self.assertFalse(report["price_prediction_performed"])
        self.assertFalse(report["labels_2026_opened"])
        self.assertEqual(report["sampled_train_origins"],40)
        self.assertEqual(report["sampled_development_origins"],40)
        self.assertTrue(report["context_token_observations_overlapping"])
        self.assertEqual(len(report["quantile_magnitude_boundaries_bps"]),4)
        self.assertEqual(set(report["development_context_reconstruction"]),{
            "legacy_g0a","continuous_g0b",
            "signed_uniform_g1","signed_quantile_g2"})
        c=report["development_context_reconstruction"]
        self.assertGreater(c["legacy_g0a"]["direction_lost_fraction_of_nonflat"],0)
        self.assertEqual(c["continuous_g0b"]["direction_lost_count"],0)
        self.assertEqual(c["signed_uniform_g1"]["direction_lost_count"],0)
        self.assertEqual(c["signed_quantile_g2"]["direction_lost_count"],0)
        self.assertTrue(all(x["forecast_skill_measured"] is False
                            for x in c.values()))

    def test_vocabulary_independent_of_extreme_development_values(self):
        train=cases(2018)
        dev=cases(2023)
        first=run_cases(train,dev,interval="H1")
        extreme=[replace(x,continuous_past_bps=tuple(
            100000.0*((-1)**i) for i in range(20))) for x in dev]
        changed=run_cases(train,extreme,interval="H1")
        self.assertEqual(first["quantile_magnitude_boundaries_bps"],
                         changed["quantile_magnitude_boundaries_bps"])
        self.assertEqual(first["train_context_reconstruction"],
                         changed["train_context_reconstruction"])
        self.assertNotEqual(first["development_context_reconstruction"],
                            changed["development_context_reconstruction"])

    def test_rejects_2026_holdout_and_wrong_resolution(self):
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2026),interval="M1")
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2023),interval="W1")


if __name__=="__main__":
    unittest.main()
