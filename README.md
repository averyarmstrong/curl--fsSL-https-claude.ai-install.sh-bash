# aks-lab

**PRIVATE — Armstrong Kinetic Solutions.** The computational home of AKS.
Everything here is built to be read line by line by a hostile expert.
Foundation principle: *our ambition can be unlimited; our claims must be
measurable.* Every number this repo produces is reproducible from a
command, carries its assumptions, and is tagged `measured`, `modeled` or
`target`.

The repo models **only** the mechanism of U.S. Patent 12,409,695 B2
("Vehicle suspension energy reclamation generator", L. D. Armstrong,
granted 2025-09-09): a vertically collapsible frame between chassis and
suspension; a frame biasing spring softer than the (shortened) main spring,
in series with it; a drive rod through a hollow generator shaft; two
opposed sprag clutches that turn both collapse and expansion into one-way
rotation; fly weights; a generator. We call that assembly the Gate.

## Ten-minute version

**What we claim.** Nothing yet beyond the physics in `docs/01_physics.md`
and the granted claims. No AKS performance figure is `measured` as of
2026-10-17 (`docs/08_findings_that_change_the_story.md`, F4). The first
bench run is pre-registered in `docs/05_bench_protocol.md`.

**What we have modeled (and validated how).**

1. The road sets the budget. For any corner on a point-contact tire of
   rate k_t driven by an ISO 8608 road, the mean power the road delivers is
   exactly ¼·k_t·W_v = π²·G_d(n₀)·n₀²·V·k_t — independent of masses,
   springs, damper, and of the Gate (`docs/01_physics.md` §7; exact to
   10⁻⁶ in `tests/test_analytic_limits.py`, reproduced by the nonlinear
   Gate simulation). Mid-size car, 60 mph: 30 / 122 / 488 / 1952 W per
   vehicle on ISO A / B / C / D. This reproduces the published 100–400 W
   (Zuo & Zhang 2013) and replaces every "the spring is a bigger
   reservoir" statement in prior AKS material (F1, `docs/07_claims_audit.md`).
2. The Gate's share of that budget, φ = P_elec / P_road, is a property of
   the corner, not of the road: 0.08 (mid-size car), 0.09 (F-150), 0.11
   (HMMWV), 0.11–0.13 (heavy stations) with the OEM damper in place; about
   0.3 when the damper is cut to a quarter, paid for with +20–50 % dynamic
   tire load. Per corner at 60 mph, stock damper (experiments 002–003,
   1,000 runs, ±3 % seed scatter):

   | corner | ISO C: supply → P_elec → net of hardware mass | ISO D |
   |---|---|---|
   | mid-size car | 122 → 9.7 → −21 W | 488 → 39 → −3 W |
   | F-150 | 169 → 15 → −23 W | 678 → 59 → +3 W |
   | HMMWV | 271 → 29 → −18 W | 1084 → 117 → +48 W |
   | MRAP (15 t) | 745 → 95 → +11 W | 2982 → 381 → +239 W |
   | Class 8 loaded, dual station | 1220 → 153 → +57 W | 4879 → 614 → +425 W |

   Passenger cars: tens of watts, roughly break-even. Heavy and tactical
   vehicles on rough roads: hundreds of watts per station, kilowatts per
   vehicle. Every claim in prior AKS material is re-tagged against this in
   `docs/07_claims_audit.md` (12 of 29 unsupported, all for one reason: F1).
3. Design rules that fell out of the sweeps: the reflected inertance J·r²
   must stay below ~10 kg for a car corner or the soft stage locks (exp
   004, 006); the optimum generator load is c_gen·r² ≈ 300–900 N·s/m and
   is insensitive to the bias ratio (exp 001, 005); where the OEM damper
   acts is the largest single lever and trades harvest against grip along
   one curve (exp 006); stops are a class-D / reduced-damper issue, not a
   paved-road one (exp 005, 002); peak race speed exceeds catalog sprag
   lift-off above r ≈ 200 rad/m (sizing report); clutch service life has no
   literature basis at ~170 engagements per km per set (F6).

An exact linear surrogate of the Gate corner (`validate/analytic.py`)
reproduces the nonlinear sweeps within ~10 % wherever the clutches are
engaged most of the time and gives the ride/grip-constrained ceiling in
milliseconds (`reports/linear_frontier.md`); a numba RHS runs the hybrid
model 3.5× faster (`vehicles/quarter_car_fast.py`, equivalence-tested).

**Validation gates (all passing, `make test`).** (a) linear quarter car
vs analytic transmissibility < 1%; (b) Zuo baseline band; (c) single-stroke
hand derivation vs the Gate element to 0.5%; energy ledger closure to solver
tolerance on every path (free, engaged, backlash impact, torque-capacity
slip, hard stop); ISO 2631-1 W_k vs the standard's table.

**What we have measured.** Nothing. Prototype hardware numbers that exist
are the Ebsco spring pair (1.905 / 15.902 lbf/in, ratio 8.35) in
`data/prototype/prototype_v1.yaml`.

## Layout

```
src/aks_lab/
  elements/   gate.py (bias spring, stops, ratio r, opposed sprags with backlash & torque
              capacity, flywheel, generator interface), generator.py
  vehicles/   quarter_car.py (passive baseline + corner-with-Gate), vehicles.yaml (per-corner
              parameter sets with provenance)
  roads/      iso8608.py (synthesis, PSD-verified), deterministic.py (sine/step/bump/measured)
  solvers/    hybrid.py (event-driven, stiff-aware; clutches and stops are events/exact resets)
  power/      (ledger lives in SimResult.energy_audit; every term is an ODE state)
  metrics/    ride (ISO 2631 W_k), handling, energy (φ, φ_s, η), net (P_net), sizing
  validate/   analytic.py (transmissibility, exact H2 mean road power, Zuo baseline)
  sweeps/     cases.py (one case → one row), runner.py (multiprocessing, incremental parquet)
  bench/      harness.py (prescribed-stroke rig), reduce.py (raw CSV → same metrics as model)
  viz/        plots.py (figures with parameter set embedded), report.py (`make report`)
experiments/  001 load sweep · 002 roads×speeds×light vehicles · 003 heavy corners ·
              004 drive ratio · 005 bias ratio×travel · 006 flywheel + tornado
docs/         00 intake · 01 physics · 02 definitions · 04 prior art · 05 bench protocol ·
              06 numbers ledger · 07 claims audit · 08 findings that change the story ·
              09 open parameters · LAB_NOTEBOOK
data/         prototype/, literature/ (prior-art dossier), roads/
params/       gate_baseline.yaml (every value with provenance; enforced by tests)
reports/      component_sizing.py → component_sizing.md
```

## Commands

```bash
make install            # pip install -e ".[dev]"
make test               # pytest (≈2 min)
make lint               # ruff
make exp001 … exp006    # run one experiment (resumable; results/ parquet + figures + RESULTS.md)
experiments/run_all.sh  # the whole chain, sequential, 4 workers
make report             # regenerate every figure/table from parquet, no simulation
```

## Reading order for a reviewer

`docs/00_intake.md` → `docs/01_physics.md` → `docs/03_symmetry_breaking_first_principles.md` → `tests/` → `docs/08_findings…`
→ `experiments/001…/README.md` → `docs/07_claims_audit.md`.

## Rules

Ranges, not points. Units on everything. Sources with page numbers. No
marketing language. Never invent a measurement. Never silently calibrate.
Bad news goes in `docs/08_findings_that_change_the_story.md` first.
