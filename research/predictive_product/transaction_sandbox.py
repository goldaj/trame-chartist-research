"""P3 synthetic-only economic sandbox with explicit fees, spread and slippage.

No trading API, no orders, wallets or actual exchange execution simulation.
This is a numerical test instrument, NOT a deployable backtest or edge.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
import math
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    origin_utc: datetime
    signal_available_utc: datetime
    observed_price: float
    next_observed_price: float
    position: int
    target_utc: datetime


def _valid_utc(value):
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError("timezone-aware UTC required")


def simulate(steps, *, fee_bps=5.0, spread_bps=3.0, slippage_bps=2.0,
             funding_bps_per_step=0.0):
    """Simplified unlevered per-period price changes, with explicit cost debits.

    A signal for period (t,t+1) must be available no later than t.
    Observed prices represent marking prices, not executable quotes.
    Cost on turnover includes entering, flipping and final liquidation.
    """
    if not isinstance(steps, (tuple, list)) or len(steps) < 2:
        raise ValueError("at least two synthetic periods required")
    costs=(fee_bps,spread_bps,slippage_bps,funding_bps_per_step)
    if any(type(x) not in (int,float) or not math.isfinite(x) or x < 0 or x > 10000
           for x in costs):
        raise ValueError("finite nonnegative bps up to 10000 required")
    oneway=(fee_bps+spread_bps/2+slippage_bps)/10000.0
    funding=funding_bps_per_step/10000.0
    equity=1.0
    high=1.0
    max_drawdown=0.0
    total_turnover=0
    cumulative_cost=0.0
    previous_position=0
    previous_origin=None
    previous_target=None
    previous_next_price=None
    ledger=[]
    defaulted=False
    for step in steps:
        if not isinstance(step, Step):
            raise TypeError("Step required")
        _valid_utc(step.origin_utc)
        _valid_utc(step.signal_available_utc)
        _valid_utc(step.target_utc)
        if step.signal_available_utc > step.origin_utc:
            raise ValueError("signal published after decision origin")
        if step.target_utc <= step.origin_utc:
            raise ValueError("target must occur after decision origin")
        if previous_origin is not None and step.origin_utc <= previous_origin:
            raise ValueError("origins must be strictly increasing")
        if previous_target is not None and step.origin_utc != previous_target:
            raise ValueError("unrepresented calendar gap or overlapping target")
        if (previous_next_price is not None
                and not math.isclose(step.observed_price, previous_next_price,
                                     rel_tol=1e-12, abs_tol=0.0)):
            raise ValueError("next mark and subsequent entry price inconsistent")
        if type(step.position) is not int or step.position not in (-1,0,1):
            raise ValueError("positions limited to unlevered -1, 0, 1")
        if (any(type(x) not in (float,int) or not math.isfinite(x) or x <= 0
                for x in (step.observed_price,step.next_observed_price))):
            raise ValueError("finite positive marking prices required")
        turnover=abs(step.position-previous_position)
        entry_cost=turnover*oneway
        funding_cost=abs(step.position)*funding
        gross=step.position*(step.next_observed_price/step.observed_price-1.0)
        factor=1+gross-entry_cost-funding_cost
        cumulative_cost+=entry_cost+funding_cost
        total_turnover+=turnover
        equity*=max(0.0, factor)
        if factor <= 0:
            defaulted=True
        high=max(high,equity)
        max_drawdown=max(max_drawdown,1.0-equity/high)
        ledger.append({
            "origin_utc":step.origin_utc.isoformat(),
            "target_utc":step.target_utc.isoformat(),
            "position":step.position,
            "turnover_units":turnover,
            "gross_simple_return":gross,
            "debit_in_fraction_of_equity":entry_cost+funding_cost,
            "end_equity_starting_at_one":equity,
        })
        previous_position=step.position
        previous_origin=step.origin_utc
        previous_target=step.target_utc
        previous_next_price=step.next_observed_price
        if defaulted:
            break
    if not defaulted:
        exit_cost=abs(previous_position)*oneway
        cumulative_cost+=exit_cost
        total_turnover+=abs(previous_position)
        equity*=max(0.0,1-exit_cost)
        max_drawdown=max(max_drawdown,1.0-equity/high)
    return {
        "experiment":"p3_offline_synthetic_transaction_cost_sandbox_v0.1",
        "input_provenance":"ARTIFICIAL_ONLY",
        "provenance_independently_verified":False,
        "calendar_and_mark_continuity_checked":True,
        "real_execution_validated":False,
        "hyperliquid_funding_history_used":False,
        "approved_for_live_trading":False,
        "funding_is_assumption":True,
        "price_is_executable_quote":False,
        "fee_bps":float(fee_bps),"spread_bps":float(spread_bps),
        "slippage_bps":float(slippage_bps),
        "funding_bps_per_step":float(funding_bps_per_step),
        "net_simple_return":equity-1.,
        "max_drawdown_fraction":max_drawdown,
        "number_of_evaluated_periods":len(ledger),
        "total_turnover_units":total_turnover,
        "cumulative_cost_as_approx_fraction_of_start_equity":cumulative_cost,
        "ruin_or_liquidation_proxy":defaulted,
        "ledger":ledger,
    }


def fabricated_fixture():
    """Deterministic made-up hourly prices, not a synthetic financial market proof."""
    start=datetime.fromisoformat("2024-01-01T00:00:00+00:00")
    prices=(100.0,101.0,99.0,100.0,102.0,101.0)
    positions=(1,1,0,-1,-1)
    return [
        Step(start+timedelta(hours=i),start+timedelta(hours=i),
             prices[i],prices[i+1],positions[i],
             start+timedelta(hours=i+1))
        for i in range(len(positions))
    ]


def sensitivity_report(steps):
    """Compare unchanged toy signals with cash and toy buy-and-hold controls.

    This is NOT a real-world execution simulation or proof of edge.
    """
    if not isinstance(steps, (list, tuple)) or len(steps) < 2:
        raise ValueError("at least two synthetic periods required")
    cases=(
        ("frictionless",0.,0.,0.,0.),
        ("base",5.,3.,2.,0.),
        ("stress",15.,10.,10.,3.),
    )
    result=[]
    for name,fee,spread,slippage,funding in cases:
        common=dict(fee_bps=fee,spread_bps=spread,
                    slippage_bps=slippage,funding_bps_per_step=funding)
        strategy=simulate(steps,**common)
        cash=simulate([replace(step,position=0) for step in steps],**common)
        passive=simulate([replace(step,position=1) for step in steps],**common)
        result.append({
            "scenario":name,
            "cost_assumptions_bps":common,
            "strategy_net_return":strategy["net_simple_return"],
            "cash_net_return":cash["net_simple_return"],
            "synthetic_buy_hold_net_return":passive["net_simple_return"],
            "strategy_max_drawdown":strategy["max_drawdown_fraction"],
            "strategy_turnover_units":strategy["total_turnover_units"],
        })
    return {
        "experiment":"P3_SYNTHETIC_COST_SENSITIVITY_V1",
        "source_is_artificial_only_caller_declaration":True,
        "origin_and_market_data_independently_verified":False,
        "replicates_real_exchange_fills":False,
        "model_has_financial_edge":False,
        "allowed_for_live_trading":False,
        "scenarios":result,
    }


def main(argv=None):
    parser=argparse.ArgumentParser(description="Synthetic only offline risk arithmetic")
    parser.add_argument("--fee-bps",type=float,default=5.0)
    parser.add_argument("--spread-bps",type=float,default=3.0)
    parser.add_argument("--slippage-bps",type=float,default=2.0)
    parser.add_argument("--sensitivity",action="store_true",
                        help="compare cost assumptions with synthetic cash/buy-hold")
    args=parser.parse_args(argv)
    if args.sensitivity:
        print(json.dumps(sensitivity_report(fabricated_fixture()),
                         indent=2,allow_nan=False))
        return
    out=simulate(fabricated_fixture(),fee_bps=args.fee_bps,
                 spread_bps=args.spread_bps,slippage_bps=args.slippage_bps)
    print(json.dumps(out,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
