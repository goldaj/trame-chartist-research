"""A6 model licensing and temporal safety tests, no checkpoints loaded."""
import unittest
from datetime import datetime, timedelta, timezone

from research.foundation_models.registry import MODELS, decision
from research.foundation_models.forecast_contract import (
    Forecast, Observation, validate_forecast_contract,
)


T0 = datetime(2021, 1, 3, tzinfo=timezone.utc)
HISTORY = [
    Observation(T0 - timedelta(days=2), T0 - timedelta(days=1), 29000.0),
    Observation(T0 - timedelta(days=1), T0, 30000.0),
]
OUTPUT = [
    Forecast(T0 + timedelta(days=1), {0.1: 28000., 0.5: 30000., 0.9: 32000.})
]


class FoundationSafetyTests(unittest.TestCase):
    def test_license_blocks_research_only_checkpoints_in_product(self):
        self.assertEqual(len(MODELS), 3)
        for model in ("timesfm3", "moirai2"):
            with self.subTest(model=model):
                r = decision(model, commercial=True, revision="pinned-commit")
                self.assertFalse(r["admissible_under_known_constraints"])
                self.assertIn("checkpoint_weight_license_noncommercial", r["blockers"])
                self.assertFalse(r["loaded_weights"])

    def test_chronos_is_not_confirmatory_without_contamination_audit(self):
        self.assertTrue(decision("chronos2", commercial=True,
                                 revision="pin")["admissible_under_known_constraints"])
        r = decision("chronos2", commercial=True, confirmatory=True,
                     revision="pin")
        self.assertFalse(r["admissible_under_known_constraints"])
        self.assertIn("pretraining_contamination_unknown", r["blockers"])

    def test_temporal_contract_accepts_known_history(self):
        out = validate_forecast_contract(origin=T0, history=HISTORY, output=OUTPUT,
                 known_future=((T0 + timedelta(days=1),
                                T0 - timedelta(days=2), 1.0),))
        self.assertTrue(out["valid_temporal_contract"])
        self.assertFalse(out["pretraining_contamination_ruled_out"])

    def test_reject_future_or_revised_history(self):
        future = HISTORY + [Observation(T0 + timedelta(days=1), T0, 31000.)]
        with self.assertRaises(ValueError):
            validate_forecast_contract(origin=T0, history=future, output=OUTPUT)
        late = [HISTORY[0], Observation(T0 - timedelta(days=1),
                                        T0 + timedelta(seconds=1), 30000.)]
        with self.assertRaises(ValueError):
            validate_forecast_contract(origin=T0, history=late, output=OUTPUT)

    def test_reject_quantile_crossing_and_future_covariate(self):
        crossing = [Forecast(T0+timedelta(days=1), {0.1: 32000., 0.9: 30000.})]
        with self.assertRaises(ValueError):
            validate_forecast_contract(origin=T0, history=HISTORY, output=crossing)
        with self.assertRaises(ValueError):
            validate_forecast_contract(origin=T0, history=HISTORY, output=OUTPUT,
                known_future=((T0+timedelta(days=1),
                               T0+timedelta(seconds=1), 1.),))


if __name__ == "__main__":
    unittest.main()
