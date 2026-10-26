# TRAME S2 — continuous-return causal direction laboratory
Read [preregistered protocol](PROTOCOL_20261026.md) before using outputs.

## Motivation
The original A7/S1 models operate on integer-coded
`round(1000*log_return)` returns and train a rounded-Gaussian NLL.
Even after 200 updates and 1/2/4 layers many models predict only one
direction. S2 tests an **independent hypothesis**, not a retrofit of
old scores: direct continuous bps past returns plus a head explicitly
trained to classify up/down and another to regress magnitude.

## New components
- `research/btc_h1_m1/stream.py` augments the existing immutable
  `Case` with `continuous_past_bps`, strictly past 20 realized returns.
  The integer codec and original `Case` fields stay unchanged.
  The daily indicative 2010–2011 prices are still only descriptive.
- `models.py`: GQA/RoPE causal backbone 1/2 layers, common return
  and direction heads, two **predeclared** objectives:
  `regression` Huber, `joint` Huber + 0.5 BCE,
  flats excluded from BCE.
- `runner.py`: train-only return normalization, same sampling splits,
  same batches/seeds, score USD/bps/direction/balanced/magnitude
  and always-up/down controls.
- `test_continuous.py`: adversarial fake-return fixtures, future-token
  invariance, finite gradients, direction/amplitude price consistency,
  no use of 2026. CI `trame-s2-continuous.yml`.

## Fabricated fixture-only checks
~~~bash
python -m unittest research.continuous_direction.test_continuous -v
~~~

## Commands for an authorised PRIVATE, CPU runner
The three resolution archives must be present in the pinned private
release cache, with no GitHub token passed to Python training:

~~~bash
python -m research.continuous_direction.runner --interval D1 --steps 200 --output /tmp/s2_d1_real.json
python -m research.continuous_direction.runner --interval H1 --steps 200 --output /tmp/s2_h1_real.json
python -m research.continuous_direction.runner --interval M1 --steps 200 --output /tmp/s2_m1_real.json
~~~

Each horizon evaluates 2 modes × 2 widths(16/32) × 2 depths(1/2)
× 3 seeds = **24 fits**, total **72**. **Same task, not
compute/parameter matched** to the older 1/2/4 scaling grid;
results are development-only and cannot justify a production choice.

## Interpretation
A good up/down accuracy with a biased one-sided sign mix is no
discriminative improvement. Require balanced accuracy, predicted
up/down counts, score vs 1bp constant-up/down controls, Brier,
magnitude error bps, native price MAE and per-seed dispersion.
Never compare regression Huber/BCE to the old Gaussian BASE
NLL as though they were the same likelihood.
No fees by owner instruction, no portfolio PnL, no trading orders.
2026 is still the quarantined test set, forbidden for tuning.

## Codex
This is [PR #19](https://github.com/goldaj/trame-chartist-research/pull/19)
based on PR #18 (D1 recovery) and its parents #17/#14/#10/#9/#8.
No merges by default. Read `AGENTS.md`,
`docs/CODEX_D1_HANDOFF_20261026.md`,
`research/scaling_study/S1_REAL_200UPDATES_20261026.md`,
and this protocol. Keep experimental lineage explicit and
private prices entirely out of public commits.
