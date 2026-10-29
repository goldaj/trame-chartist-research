# TRAME Codex handoff — D1 parity + S1 scaling, 26 October 2026

**Read in order**
1. `AGENTS.md` (latest topmost instruction supersedes former A7 pause).
2. `research/btc_h1_m1/D1_RECOVERY_PLAN_20261026.md`.
3. `research/btc_h1_m1/D1_H1_M1_REAL_RESULTS_20261026.md`.
4. `research/scaling_study/PROTOCOL_20261026.md` and
   `research/scaling_study/S1_REAL_GRID_CANARY_20261026.md`.
5. `research/scaling_study/panel.py` and `test_panel.py`.
6. `docs/CHATGPT_PROJECT_HISTORY.md` (partial annotated history).

## What the owner said
The owner instructed a **full re-inclusion of D1 since canonical BTC
data became available**, to be done before resuming the scaling work.
No transaction fees; directional accuracy AND forecast monetary
amplitude are crucial for later human trader decisions. The owner
requires substep completion notices followed by automatic continuation.

## Repository graph and data boundaries
- **PR #18** branch `chatgpt/trame-d1-parity-20261026`, based on
  **PR #17**, based on **PR #14**; earlier stack #10/#9/#8 untouched.
  PR #11–#16 are siblings and must not be merged into this branch
  implicitly. None of the PRs should be auto-merged.
- Private price release `goldaj/btc-historical-data` tag
  `btcusd-bitstamp-2010-2026-reference-v1`, unchanged.
  DO NOT publish prices/tokens/public datasets or use bot
  `goldaj/hyperliquid-btc-pilot`.
- D1: `daily.py` is the EXISTING canonical 3-CSV reader. The newest
  `stream.py` dispatch uses it and **skips** the 2010–2011
  indicative close-only segment when building OHLCV Case samples.
  Training uses real Bitstamp OHLCV 2011H2–2021 with nonzero-volume,
  contiguous 20-return histories; validation 2022–2025;
  2026 labels unopened. The descriptive long-run close-only reader
  still retains all 2010–2011 indicative points.
- H1/M1 remain independent, with their former source formats and
  2026 quarantine; do not compare their NLL to D1.

## Actual delivered milestones (verifiable)
- D1.1 audit of three archives/schemas/grades.
- D1.2 unified daily source hooked into causal stream (no fake OHLCV).
- D1.3 A7 statistical persistence/Ridge, neuron 3 arms, regime by year
  and trailing-volatility supports D1; on REAL data
  [private run #40280347574](https://github.com/goldaj/btc-historical-data/actions/runs/40280347574),
  succeeded. Train origins 3622, dev candidates 1461, dev sample 1024.
- D1.4 S1 runner accepts D1, same 5 parameter targets and 3 depths.
- D1.5 fabricated schema/holdout tests, CI `trame-d1-parity.yml` succeeded.
- D1.6 actual D1 stats: persistence MAE **974.7802 USD**;
  Transformer **973.7139**, mini GPT **974.6576**, GRU **974.3426**,
  average 3 seeds, 40 steps. Direction GRU **50.6836 %**
  is **exactly an always-up predictor (1024/1024 positive)**.
- D1.7 H1/M1 baselines/regimes/direction rerun with harmonised metrics,
  [private run #40280464439](https://github.com/goldaj/btc-historical-data/actions/runs/40280464439),
  succeeded both jobs. All three horizon reports documented.
- S1 scaling 5 sizes × depths 1/2/4 × 3 families × 3 resolutions,
  [private run #40281223578](https://github.com/goldaj/btc-historical-data/actions/runs/40281223578),
  **all six jobs succeeded**, 135 training canaries one seed, 40
  updates on three smaller capacity targets, 8 on two biggest.
  CPU executes to ~2.39 M params; NO evidence of convergence,
  compute equality or directional advantage.
- Ongoing/next: [private 3-seed, 200-update run #40281657954](https://github.com/goldaj/btc-historical-data/actions/runs/40281657954),
  covering 3 target sizes × 3 depths × 3 architectures × 3 seeds ×
  D1/H1/M1 = 243 additional fits. Inspect its final status and
  private artefact hashes; never label completed without run success.
- `research/scaling_study/metrics.py` now includes no-skill
  `always_up_1bp` and `always_down_1bp` controls.
  `panel.py` / `test_panel.py` reject holdout leakage,
  duplicate arm+seed and fake compute equality, and emit a table
  with paired direction + amplitude metrics.
- All GitHub Actions report only aggregated JSON into the **PRIVATE**
  data repo with 30-day retention. Retain SHA fingerprints in docs.

## SCIENTIFIC NO-GO
- Forty optimizer updates dramatically undertrain models; scaling
  canaries with 8 updates are **hardware/shape smoke only**. Neither
  one seed nor class-majority direction proves usable forecasting.
- `FIXED_SCALE=1000` rounding erases subtle returns, esp. M1.
  A new *continuous-return* or dual-head signed-return model would
  be a **separate preregistered arm**, not a silent fix of the
  historical experiments.
- Group by interval and report n, direction overall+balanced,
  up/down prediction mix, signal coverage, magnitude error,
  MAE USD/bps, seed uncertainty, time, actual param count,
  trained updates. Always-up and down baselines required.
- Sampled gross return per candle with fees omitted is not cumulative
  portfolio performance nor a viable trade execution simulator.
  No backtest with 2026 or exchange order permitted.
- To infer a size effect, compare depths with similar parameters
  and then capacities at fixed depth, matching *credible* training
  FLOPs/tuning and approaching convergence. Current proxy profiler
  undercounts work; `compute_matched=False` must remain.

## Next steps in priority order
1. Check PR #18 CI HEAD and verify the current 200-update private run,
   document failures and hashes/seed-by-seed comparisons.
2. Generate `panel.py` table from three private 200-update JSONs;
   report explicitly no-skill baseline and moving amplitude errors.
3. Repeat 592k/2.36M at 3 seeds with adjusted budgets if
   scientifically worthwhile and private runner capacity measured.
4. Prototype continuous log-return and direction/amplitude outputs
   to address monoclasse and low-magnitude predictions, with causal
   and quantization tests, train/dev freeze.
5. Only then consider statistical interval estimates by regime,
   economic interpretation (still no fees), new horizons, GPU
   Mamba branches and true held-out protocol. **Never** unlock 2026
   simply because the 2022–2025 development scores look good.
