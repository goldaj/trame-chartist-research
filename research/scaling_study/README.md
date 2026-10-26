# TRAME S1 — size × depth × direction and magnitude
Start here: [full scientific protocol](PROTOCOL_20261026.md).

**Scientific status:** exploratory development; not an independent proof of
forecasting or a usable trading system. Never merges itself with the bot.

## What this branch adds
- `models.py`: old masked Transformer, GPT-style GQA/RoPE and GRU, depths **1/2/4**, capacity targets **2.4k / 37k / 148k / 592k / 2.36M**. Width chosen separately, actual parameter count checked at runtime; do not call these compute-matched.
- `metrics.py`: direction accuracy including flat labels, directional coverage, balanced up/down recall, MAE USD, relative and absolute-move bps, train-only magnitude buckets and a **gross one-candle sampled signal score**. Fees intentionally excluded on owner instruction. **A mean over sampled candles is not a cumulative portfolio return.**
- `runner.py`: same train/dev BTC cases and common mini-batches per seed; independent test **2026 untouched**; CPU float64, seed repeatability and provenance.
- `test_scaling.py`: fabricated cases only, anti-leakage, causality, parameter accounting, magnitude and gradients; workflow `trame-s1-scaling.yml`.

## Dry run without touching the data
```bash
python -m unittest research.scaling_study.test_scaling -v
python -m research.scaling_study.runner --interval H1 --plan-only > s1_grid.json
```

## First real-data *exploratory* pilots (on private authorised runner)
Before running, read [private release integration](../btc_h1_m1/README.md).
The caller must have the approved release in the local pinned cache; do not
include a dataset or token in a public workflow.

```bash
# Minimal canary, one family, 1 layer, 2400-parameter target, one seed:
python -m research.scaling_study.runner --interval H1 \
  --targets 2400 --depths 1 \
  --architectures modern_gpt_style_mini \
  --steps 2 --seeds 20261026 --output /tmp/s1_h1_canary.json

# First 5x3x3 pilot: up to 45 arms x 3 seeds per interval.
# Cost can be material for 2.36M on CPU; start with --steps 40
# and measured CPU latency, then budget explicitly before longer runs.
python -m research.scaling_study.runner --interval H1 \
  --steps 40 --output /tmp/s1_h1_exploration.json
python -m research.scaling_study.runner --interval M1 \
  --steps 40 --output /tmp/s1_m1_exploration.json
```

With all 5 size targets, all 3 depths, 3 families and 3 seeds there
are **135 fits per horizon, 270 total**. Runs intentionally process **one
model at a time**, with no GPU availability claim.

## Interpretation and caveats
- The previous A7 experiment trained only **40 optimizer updates**. A larger
  model might score worse simply because it has not converged. Study learning
  curves and compute budgets before ranking the size axis.
- The existing `FIXED_SCALE=1000` integer log-return codec throws away
  small movements, especially at M1. Inspect the fraction of zero-coded
  targets separately; propose a continuous-return representation as a new
  controlled arm, not a silent change.
- This early comparison is not matched on FLOPs, wall clock, hyperparameter
  search, memory or latency. Directional class imbalance also matters.
- The momentum 1bp control is **only a direction diagnostic**, not a
  recommended trading rule; persistence makes *no* directional call.
- USD MAE rises with nominal BTC price; always report bps and regime-year
  stratification as next steps.
- Synthetic test fixtures in CI **do not** download or open private BTC rows.
  Real output should stay in private Actions artifacts or local paths. Only
  aggregate statistics and exact provenance may enter this public branch.
- Never open the reserved 2026 target labels for architecture/size selection;
  no order, API execution, Hyperliquid integration or trading automation.

## Codex handoff
Review `AGENTS.md`, `docs/CODEX_EXECUTION_BOARD_20261025.md`,
`research/btc_h1_m1/A7_STATUS_20261025.md`, then this protocol.
This branch is stacked on **PR #14**, which is stacked on PR #10/#9/#8.
PR #11–#16 are sibling experiments not automatically included.
No merge without comparing the current PR graph and green CI.

## Remaining stages
S1.6 CI qualification; S1.7 private-runner H1/M1 launch with reproducible
SHA/artefacts; S1.8 270-run aggregate table including direction and magnitude;
S1.9 uncertainty, chronological regimes and new model representations.
