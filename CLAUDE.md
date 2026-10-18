# aks-lab — session memory

**Mission:** the computational home of Armstrong Kinetic Solutions.
Measurable, reproducible models of the Gate (U.S. 12,409,695 B2 only).
Foundation principle: "Our ambition can be unlimited. Our claims must be
measurable." Repo stays PRIVATE.

Read `docs/01_physics.md` (normative derivations), `docs/03_symmetry_breaking…`
(why the sprags make a spring yield net work, and where it comes from), `docs/08_findings…`
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
- [x] Experiments 001–006 run (1,794 cases, 0 errors), READMEs written,
      findings F1–F7, ledger, sizing report, linear frontier, README table
- [x] Experiment 007 Monte Carlo (1,152 live cases; Class 8 load range
      corrected and re-run), README, bands in F5 and ledger
- [x] Session 3: body-force channel (E_body), one-sided tire, gravity test, exp 008, F8
- [x] Session 4: drawings viewed; `docs/03_symmetry_breaking_first_principles.md` + test (loop area = energy; spring is storage)
- [x] Session 4b: pump-top toy researched and modeled (`aks_lab.toy.PumpTop`, exp 009, `docs/03a`): race ceiling ω ≤ r·v_hand, reflected mass J r², full-wave = capture not source
- [ ] Clutch endurance leg T6 and bench data when hardware runs
- [ ] Half-car (pitch) model; measured-profile ingest from FHWA LTPP
- [x] numba RHS (3.5×); sweeps default to it

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
- `toy/pump_top.py` — the push-down top with a Hill hand, helix, pawl(s), flywheel, stops; own event loop; ledger as states.

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
- Case worker: `c_s_scale` scales the OEM damper on the Gate corner only;
  `body_force` / `tire_oneside` force the reference (non-numba) model.
- NSTATE is 19 (E_body added session 3); the numba model zero-fills it.
- Mid-size-car parameters are literature-typical, NOT Zuo & Zhang's table
  (not retrievable here).

## Process

- **Surrogate first.** Before any sweep, run `validate.analytic.linear_gate_power` /
  `optimise_linear_gate` (milliseconds) to set the c_gen, c_s_scale and r/J grids;
  then confirm with the hybrid model. Today's first 001 pass burned 10 min of
  4 cores at r = 1484 that the surrogate would have ruled out.
- Heavy stations need their own load grid (optimum c_gen ≈ 0.1–0.3 at r = 300).
- `experiments/run_all.sh` chains everything; `make report` regenerates.

Conventional commits, one per numbered step, message states the question
answered. Push to `claude/modest-hamilton-c7f0g9`. `make test && make lint`
before every commit.
