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
2. The Gate's share of that budget, φ = P_elec / P_road, is what the
   experiments compute. With the stock damper left in place the Gate takes
   under 10% (experiment 001); the remaining experiments map φ against
   damper reduction, generator load, drive ratio, flywheel inertia,
   spring ratio, travel, road class, speed and vehicle. Headline ranges are
   in each `experiments/*/results/RESULTS.md` and summarised below once
   the chain completes.
3. Two architectural facts emerge before any optimisation: the geared
   rotor's reflected inertance J·r² can lock the soft stage (F2), and a
   soft stage with 2–5 in of travel binds at a few percent of corner-load
   variation at the prototype spring ratio (F3).

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

`docs/00_intake.md` → `docs/01_physics.md` → `tests/` → `docs/08_findings…`
→ `experiments/001…/README.md` → `docs/07_claims_audit.md`.

## Rules

Ranges, not points. Units on everything. Sources with page numbers. No
marketing language. Never invent a measurement. Never silently calibrate.
Bad news goes in `docs/08_findings_that_change_the_story.md` first.
