"""P4 readiness preflight. Declarations never authorize an actual launch.

This check intentionally cannot certify authenticity of experiments or
independent review from self-reported JSON. A positive preflight is
ONLY a request for an external scientific, legal and security review.
"""
from __future__ import annotations

import argparse
import json


GATES = (
    "real_market_baselines_run",
    "paired_compute_review_completed",
    "trained_model_checkpoint_verified",
    "independent_holdout_evaluated_once",
    "calibration_and_stress_review_passed",
    "weight_licenses_permit_product",
    "realistic_transaction_cost_review_passed",
    "offline_install_and_security_review_passed",
    "human_scientific_signoff",
)


def assess(declarations=None):
    if declarations is None:
        declarations = {}
    if not isinstance(declarations, dict) or any(
            key not in GATES or type(value) is not bool
            for key,value in declarations.items()):
        raise ValueError("gate declarations must be known boolean keys only")
    missing = [name for name in GATES if declarations.get(name) is not True]
    return {
        "product": "TRAME Predictive v1",
        "status": "BLOCKED" if missing else "EXTERNAL_REVIEW_REQUIRED",
        "declared_gates": {name: declarations.get(name, False) for name in GATES},
        "missing_declarations": missing,
        "declarations_cryptographically_verified": False,
        "independent_review_verified_by_this_tool": False,
        "ready_for_launch": False,
        "trading_enabled": False,
        "may_access_wallet_or_exchange": False,
        "warning": "This CLI cannot certify experiments or authorize production.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="TRAME product release gates, safe preflight")
    parser.add_argument("--declarations", help="optional untrusted local JSON boolean declarations")
    args = parser.parse_args(argv)
    if args.declarations:
        with open(args.declarations, "r", encoding="utf-8") as inp:
            data = json.load(inp)
    else:
        data = None
    print(json.dumps(assess(data), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
