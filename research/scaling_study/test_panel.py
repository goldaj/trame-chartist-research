"""Scientific-panel aggregation tests: fabricated in-memory results only."""
import copy
import unittest
from research.scaling_study.panel import build_panel,to_markdown

def fake_source():
    return {
      "experiment":"TRAME_S1_scaling_depth_direction_development_v1",
      "labels_2026_opened":False,"independent_test_used":False,
      "total_compute_matched":False,"hyperparameter_tuning_matched":False,
      "interval":"D1","data_origin":"ARTIFICIAL_FIXTURE",
      "training_cases":64,"development_cases":32,
      "results":[{
        "architecture":"modern_gpt_style_mini","depth":2,
        "target_parameters":37000,"parameter_count":36500,
        "seed":42,"steps":40,"forecast_rows":32,
        "n_predicted_up":10,"n_predicted_down":22,"n_predicted_flat":0,
        "direction_accuracy_all":0.5,
        "balanced_direction_accuracy":0.49,
        "mae_native_usd":7.0,"mae_bps_anchor":15.0,
        "absolute_magnitude_error_bps":12.0,
        "gross_signal_return_mean_bps_per_sample":-1.3,
        "observed_cpu_train_seconds":0.12,
      }]
    }

class PanelTests(unittest.TestCase):
    def test_single_fixture_and_report_warning(self):
        panel=build_panel([fake_source()])
        self.assertEqual(panel["n_model_fits"],1)
        self.assertEqual(panel["entries"][0]["n_seeds"],1)
        self.assertAlmostEqual(panel["entries"][0]["predicted_up_fraction_mean"],10/32)
        self.assertIsNone(panel["entries"][0]["direction_accuracy_all_sd_across_seeds"])
        text=to_markdown(panel)
        self.assertIn("development only",text)
        self.assertIn("Magnit",text)

    def test_mismatched_source_rejected(self):
        source=fake_source()
        source["labels_2026_opened"]=True
        with self.assertRaises(ValueError):
            build_panel([source])
        source=fake_source()
        source["results"][0]["n_predicted_up"]=11
        with self.assertRaises(ValueError):
            build_panel([source])
        source=fake_source()
        source["results"][0]["direction_accuracy_all"]=float("nan")
        with self.assertRaises(ValueError):
            build_panel([source])

    def test_duplicate_seeds_fail_and_distinct_seeds_aggregate(self):
        source=fake_source()
        with self.assertRaisesRegex(ValueError,"duplicate"):
            build_panel([source,source])
        different=copy.deepcopy(source)
        different["results"][0]["seed"]=43
        different["results"][0]["direction_accuracy_all"]=0.75
        panel=build_panel([source,different])
        self.assertEqual(panel["entries"][0]["n_seeds"],2)
        self.assertAlmostEqual(panel["entries"][0]["direction_accuracy_all_mean"],0.625)
        self.assertIsNotNone(panel["entries"][0]["direction_accuracy_all_sd_across_seeds"])

if __name__=="__main__":
    unittest.main()
