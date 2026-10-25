"""Smoke-test real-market runner on entirely synthetic CSV fixtures only."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.btc_real_data.test_loader import write_fake_history
from research.btc_real_data.experiment import run


class ExperimentalModelTests(unittest.TestCase):
    def test_three_arms_and_baseline_without_touching_2026(self):
        with TemporaryDirectory() as d:
            folder=Path(d)
            write_fake_history(folder)
            result=run(directory=folder,steps=1,seeds=(33,))
        self.assertEqual(result["data_origin"],"REAL_HISTORICAL_SPOT_AND_INDICATIVE_OWNER_TRUSTED")
        self.assertEqual(result["price_history"]["observations"],5827)
        self.assertTrue(result["2026_labels_not_scored_or_quantized"])
        self.assertFalse(result["not_independent_financial_test"] is False)
        self.assertEqual(len(result["results"]),3)
        self.assertEqual({r["architecture"] for r in result["results"]},
                         {"legacy_causal_transformer","modern_gpt_style_mini",
                          "recurrent_gru_control"})
        self.assertGreater(result["baseline"]["development_nll"],0)
        for row in result["results"]:
            self.assertGreater(row["development_nll"],0)
            self.assertGreaterEqual(row["development_mae_price_median_usd"],0)

    def test_reject_nonunique_seeds_and_steps(self):
        for opts in ({"steps":0},{"steps":201},{"steps":True},
                     {"seeds":(1,1)},{"seeds":()},{"seeds":(True,)}):
            with self.subTest(opts=opts),self.assertRaises(ValueError):
                run(**opts)


if __name__=="__main__":
    unittest.main()
