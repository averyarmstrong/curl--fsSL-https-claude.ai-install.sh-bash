# aks-lab — session memory

**Mission:** the computational home of Armstrong Kinetic Solutions.
Measurable, reproducible models of the Gate (U.S. 12,409,695 B2 only).
Foundation principle: "Our ambition can be unlimited. Our claims must be
measurable." Repo stays PRIVATE.

Read `docs/01_physics.md` (normative derivations), `docs/08_findings…`
(what already contradicts public AKS statements) and `docs/LAB_NOTEBOOK.md`
before touching physics code. `docs/00_intake.md` says what every prior AKS
document establishes and leaves open.

## Non-negotiables

- Tags on every number: `measured` / `modeled` / `target` / `asserted` /
  `unsupported`. Zero AKS numbers are `measured` as of 2026-10-17.
- Provenance on every parameter (`params/gate_baseline.yaml`,
  `vehicles.yaml`); enforced by `tests/test_params.py`. Open parameters go
  in `docs/09_open_parameters.md` with ranges and get swept.
- Energy ledger closes < 1% on every run (`SimResult.energy_audit()`), or
  the row carries an `error`.
- Model ONLY the granted mechanism. No other concept is named anywhere.
- Report the ugly runs in `LAB_NOTEBOOK.md`; findings that contradict public
  claims go in `docs/08_findings_that_change_the_story.md` first.
- House tone = Website Blueprint "Say / Do not say" table.

## The one physics fact to carry in your head

Mean road input power per corner = ¼·k_t·W_v = π²·G_d(n₀)·n₀²·V·k_t, exact
for any causal corner on an undamped point-contact tire, nonlinear or not
(01_physics §7, tested). Nothing above the tire changes the supply; the
Gate changes the split (φ) and the ride. Mid-size car, 60 mph: 122 W per
corner on ISO C. Vehicle weight enters only through tire stiffness.

## Project state (update every session)

- [x] Intake, prototype params, physics, definitions (commit 9cd5803)
- [x] aks_lab package; validation (a)(b)(c); 41 tests passing (9576396)
- [x] Prior art, claims audit (29 claims), findings F1–F4, bench protocol
      + data reduction, numbers ledger (128926d)
- [x] Experiment 001 first pass: stock damper → φ < 0.1, P_net < 0
- [ ] Experiment chain running (`experiments/run_all.sh`; progress in
      `experiments/chain.log`): 001 resume (damper axis) → 002 → 004 → 005
      → 006 → 003. Then: each `README.md`, F5+, ledger rows, sizing report
      (`python reports/component_sizing.py`), README headline ranges.
- [ ] Half-car (pitch) model; measured-profile ingest from FHWA LTPP
- [ ] Performance: compiled RHS (numba) — sweeps cost ~0.5 s per simulated
      second per core

## Architecture map

- `elements/gate.py` — Gate element: passive force, stops, opposed sprags
  as exact constraints with backlash impact (eq. 4.5) and torque-capacity
  slip; `engaged_accels` solves the coupled 2×2 with reflected inertance
  J·r²; events `engage_gap`.
- `solvers/hybrid.py` — generic mode/event integrator (LSODA + terminal
  events + state resets, Zeno guard).
- `vehicles/quarter_car.py` — `PassiveQuarterCar` (2-DOF linear) and
  `QuarterCarGate` (3-DOF + rotor, modes FREE/ENG/SLIP, damper span
  `full`|`main`); 18 states incl. 9 energy integrals.
- `validate/analytic.py` — transmissibility; exact mean road power via
  Lyapunov; Zuo baseline.
- `sweeps/` — case dict → row; multiprocessing; resumable parquet.
- `bench/` — prescribed-stroke rig (hand-derivation anchor), CSV reduction.

## Gotchas

- YAML floats: `16.0e-6` not `16e-6`. `.inf` for infinity.
- The fixed-body 1-DOF limit of the road-power formula is singular (Brownian
  road + body fixed in space) — don't re-derive it; see LAB_NOTEBOOK 3.
- ISO 2631 W_k upward-step stage has NO (ω₆/ω₅)² factor.
- On the prescribed-stroke bench, lock-up impulses do work on the actuator:
  booked at the event (LAB_NOTEBOOK 5).
- Slip exits to FREE, never "relock" (LAB_NOTEBOOK 6).
- `c_eq_fit` on the bench ≠ c_gen·r² when J > 0; run the model with the
  measured J.
- Case worker: `c_s_scale` scales the OEM damper on the Gate corner only.
- Mid-size-car parameters are literature-typical, NOT Zuo & Zhang's table
  (not retrievable here).

## Process

Conventional commits, one per numbered step, message states the question
answered. Push to `claude/modest-hamilton-c7f0g9`. `make test && make lint`
before every commit.
