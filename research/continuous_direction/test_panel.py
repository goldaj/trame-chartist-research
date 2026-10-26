"""S2 results panel never sees private prices: artificial Case records only."""
import copy
import math
import unittest

from research.continuous_direction.runner import run_cases
from research.continuous_direction.test_continuous import fabricated_case
from research.continuous_direction.panel import build_panel,to_markdown


def fabricated_report(interval="D1"):
    training=[fabricated_case(2018,i) for i in range(40)]
    development=[fabricated_case(2023,i) for i in range(40)]
    return run_cases(training,development,interval=interval,
                     widths=(16,),depths=(1,),
                     modes=("regression","joint"),steps=1,
                     seeds=(17,18),data_origin="ARTIFICIAL_FIXTURE")


class S2PanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=fabricated_report()

    def test_panel_shows_metrics_and_same_seed_paired_deltas(self):
        panel=build_panel([self.report])
        self.assertEqual(panel["n_model_fits"],4)
        self.assertEqual(panel["n_groups"],2)
        self.assertEqual(len(panel["paired_joint_minus_regression"]),1)
        self.assertEqual(panel["paired_joint_minus_regression"][0]
                         ["paired_seed_count"],2)
        markdown=to_markdown(panel)
        self.assertIn("Témoin toujours hausse",markdown)
        self.assertIn("Magnitude err. bps",markdown)
        self.assertIn("Brier skill",markdown)
        groups={x["mode"]:x for x in panel["model_summary"]}
        self.assertIsNone(groups["regression"]["brier_skill_vs_train_prior"])
        self.assertTrue(math.isfinite(groups["joint"]
                                      ["brier_skill_vs_train_prior"]["mean"]))

    def test_duplicate_horizons_or_runs_are_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate horizon"):
            build_panel([self.report,self.report])
        broken=copy.deepcopy(self.report)
        broken["results"].append(copy.deepcopy(broken["results"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate seed"):
            build_panel([broken])

    def test_no_holdout_fake_compute_or_untrained_probabilities(self):
        for name,value in (
            ("labels_2026_opened",True),
            ("independent_test_used",True),
            ("total_compute_matched",True),
        ):
            damaged=copy.deepcopy(self.report)
            damaged[name]=value
            with self.subTest(field=name),self.assertRaises(ValueError):
                build_panel([damaged])
        damaged=copy.deepcopy(self.report)
        regression=next(r for r in damaged["results"] if r["mode"]=="regression")
        regression["binary_probabilities_from_trained_head"]=True
        regression["brier_nonflat"]=.2
        with self.assertRaisesRegex(ValueError,"must not be scored"):
            build_panel([damaged])


if __name__=="__main__":
    unittest.main()
