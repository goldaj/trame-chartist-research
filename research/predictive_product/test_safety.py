"""Offline product readiness and synthetic transaction accounting guards."""
import json
import unittest
from dataclasses import replace
from datetime import timedelta

from research.predictive_product.release_preflight import GATES, assess
from research.predictive_product.transaction_sandbox import (
    Step, fabricated_fixture, simulate,
)


class ResearchToProductSafetyTests(unittest.TestCase):
    def test_product_stays_no_go_without_external_review(self):
        blocked = assess()
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertFalse(blocked["ready_for_launch"])
        self.assertFalse(blocked["trading_enabled"])
        spoofed = assess({name: True for name in GATES})
        self.assertEqual(spoofed["status"], "EXTERNAL_REVIEW_REQUIRED")
        self.assertFalse(spoofed["ready_for_launch"])
        self.assertFalse(spoofed["independent_review_verified_by_this_tool"])
        json.dumps(spoofed, allow_nan=False)

    def test_reject_unexpected_declarations(self):
        with self.assertRaises(ValueError):
            assess({"unsafe_launch": True})
        with self.assertRaises(ValueError):
            assess({GATES[0]: 1})
        with self.assertRaises(ValueError):
            assess([GATES[0]])

    def test_synthetic_costs_reduce_returns(self):
        sample = fabricated_fixture()
        clean = simulate(sample, fee_bps=0, spread_bps=0, slippage_bps=0)
        costly = simulate(sample, fee_bps=10, spread_bps=10, slippage_bps=5)
        self.assertEqual(clean["input_provenance"], "ARTIFICIAL_ONLY")
        self.assertFalse(clean["real_execution_validated"])
        self.assertFalse(clean["approved_for_live_trading"])
        self.assertLess(costly["net_simple_return"], clean["net_simple_return"])
        self.assertGreater(costly["total_turnover_units"], 0)
        self.assertGreaterEqual(costly["max_drawdown_fraction"], 0)
        json.dumps(costly, allow_nan=False)

    def test_future_signal_and_unrealistic_position_are_forbidden(self):
        data = fabricated_fixture()
        bad = replace(data[0],
                      signal_available_utc=data[0].origin_utc+timedelta(seconds=1))
        with self.assertRaisesRegex(ValueError, "signal"):
            simulate([bad]+data[1:])
        bad = replace(data[0], position=3)
        with self.assertRaises(ValueError):
            simulate([bad]+data[1:])
        bad = replace(data[0], observed_price=-1)
        with self.assertRaises(ValueError):
            simulate([bad]+data[1:])

    def test_cost_and_calendar_checks(self):
        data = fabricated_fixture()
        with self.assertRaises(ValueError):
            simulate(data, fee_bps=-1)
        with self.assertRaises(ValueError):
            simulate(data, spread_bps=float("nan"))
        with self.assertRaises(ValueError):
            simulate(data[:1])
        with self.assertRaises(ValueError):
            simulate([data[0],data[0],*data[2:]])

    def test_market_paths_not_loaded_automatically(self):
        report = simulate(fabricated_fixture())
        self.assertFalse(report["hyperliquid_funding_history_used"])
        self.assertFalse(report["price_is_executable_quote"])
        self.assertTrue(report["funding_is_assumption"])


if __name__ == "__main__":
    unittest.main()
