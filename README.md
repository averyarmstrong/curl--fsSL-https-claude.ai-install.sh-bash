# gate-twin

**PRIVATE — Armstrong Kinetic Solutions (AKS) internal.**

Validated digital twin of the **Armstrong Gate** — a mechanical full-wave rectifier that
harvests energy from a vehicle's suspension **spring** motion
(U.S. Patent 12,409,695 B2, granted 2025-09-09).

The twin models *only* the granted-patent mechanism: a soft-first series biasing stage
(frame spring with lower rate than the main suspension spring) driving a screw through two
opposed sprag clutches (mechanical full-wave rectification) into a flywheel-smoothed
generator.

## Layout

```
src/gatetwin/    physics models (quarter-car + gate, roads, clutch logic, generators)
params/          all physical parameters, every value with a provenance citation
tests/           V1 analytic gates (pytest), V2-V4 literature anchors (marked `validation`)
notebooks/       validation & prediction studies
reports/         investor-grade outputs, bench pre-registration
docs/PHYSICS.md  full derivation, sign conventions, energy ledger
docs/LAB_NOTEBOOK.md  running record of decisions, failures, fixes
CLAUDE.md        session memory: project state, honesty norms, how to resume
```

## Quick start

```bash
pip install -e ".[dev]"
pytest -q                      # V1 gates + unit tests
pytest -q -m validation       # V2-V4 literature anchors
```

## Validation gates (must pass in order)

1. **V1** analytic limits — kinematic ratio, spin-down, zero/positive hysteresis area,
   <1% energy-audit closure on every run.
2. **V2** Zuo MMR anchor — ~40 W @ 0.047 m/s RMS, >60% mech. efficiency (±25%).
3. **V3** Audi eROT anchor — parallel-damper config, 3 / 100–150 / 613 W (±30%).
4. **V4** κ-shorthand consistency — κ≈0.10 (parallel) vs ≈0.18–0.20 (rectifier).

Tag `v0.1-validated` only when V1–V4 pass. Predictions come after, never before.
