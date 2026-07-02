# gate-twin — session memory

**Mission:** validated, investor-grade digital twin of the Armstrong Gate — a
mechanical full-wave rectifier harvesting energy from the suspension SPRING
stroke (U.S. Patent 12,409,695 B2, granted 2025-09-09). Multi-day,
publication-quality. Repo must stay PRIVATE.

Read `docs/PHYSICS.md` (authoritative derivation) and
`docs/LAB_NOTEBOOK.md` (decisions/failures log) before touching physics code.

## Honesty norms (non-negotiable)

- **No parameter tuning to flatter AKS numbers.** Priors come from published
  sources only; every parameter in `params/params.yaml` carries a mandatory
  provenance tag ([PATENT]/[MEASURED]/[LITERATURE]/[ASSUMPTION]) — enforced
  by `tests/test_params.py`.
- **Report the ugly runs.** Failures and deviations go in
  `docs/LAB_NOTEBOOK.md` and in reports, not down the memory hole.
- Passenger-car absolute numbers are **modest (hundreds of watts)**. Never
  imply a self-charging sedan. The kW story lives on heavy vehicles and
  rough duty.
- Every table distinguishes **measured anchors / derived predictions /
  assumptions**.
- The binding constraint is **road energy input**, not the generator
  (10 kW ≈ 16 N·m @ 6000 rpm — trivial shaft conditions).
- **IP guardrail:** model ONLY the granted-patent mechanism. Never introduce
  or speculate about unfiled concepts anywhere in this repo.
- When a physical parameter is uncertain: search literature, cite it, record
  it in params.yaml — never guess silently.

## Validation gates — do NOT skip ahead

V1 (analytic limits) → V2 (Zuo MMR: ~40 W @ 0.047 m/s RMS, >60% mech eff,
±25%) → V3 (Audi eROT parallel damper: 3 / 100–150 / ~613 W, ±30%) →
V4 (κ shorthand: ≈0.10 parallel, ≈0.18–0.20 rectifier). Only then
predictions. Tag `v0.1-validated` when V1–V4 pass; `v0.2-predictions` after
prediction outputs. Energy audit must close <1% on EVERY run (it's a state
of the ODE system, check `result.energy_audit()['closure']`).

## Project state (update every session)

- [x] Scaffold, params+provenance, ISO 8608 roads, PM + claw-pole generator
      models, event-driven hybrid quarter-car+Gate model, shaker bench rig
- [x] V1 gates implemented in `tests/test_v1_gates.py` — ALL PASSING
- [ ] V2 Zuo MMR anchor (needs: single-corner rectifier config at RMS
      velocity 0.047 m/s; source: Li, Zuo et al. 2013 retrofit MMR shock)
- [ ] V3 Audi eROT anchor (reconfigure as parallel electromagnetic damper,
      1800 kg sedan)
- [ ] V4 κ consistency sweep
- [ ] Predictions: per-vehicle tables (F-150 2500 kg, HD pickup 4500, box
      truck 12000, semi empty 9070, semi loaded 36300, MRAP 15000) ×
      road class × 20–90 mph; Monte Carlo uncertainty bands
- [ ] Tornado sensitivity (k_b/k_s, lead, n_step, J, generator type, R_load,
      road class)
- [ ] Durability: engagement cycles/mile vs 1e7 fatigue; lift-off margin
- [ ] Generator time-at-RPM heatmap vs alternator curve (claw-pole vs PM)
- [ ] reports/bench_preregistration.md (Duke bench, 3–5 amplitude/frequency
      points, pass/fail bands, damper-floor falsification statement)
- [ ] reports/gate_twin_report.pdf

## Architecture map

- `src/gatetwin/model.py` — QuarterCarGate: event-driven hybrid ODE
  (modes free/engA/engB; sprags = exact kinematic constraints; engaged mode
  couples the (z_s,z_f) mass matrix via reflected inertance Jr=J·Gt²).
  Energy integrals are ODE states; `SimResult.energy_audit()`.
- `src/gatetwin/bench.py` — BenchRig: prescribed stroke x_b(t) (Duke shaker
  config + V1 gates).
- `src/gatetwin/roads.py` — ISO 8608 synthesis (class A–E), PSD-verified.
- `src/gatetwin/generator.py` — PMGenerator, ClawPoleAlternator (measured
  14 V curve), all satisfy T·ω = P_elec + P_loss exactly.
- `src/gatetwin/params.py` — provenance-enforcing loader.

## Gotchas

- YAML floats: write `16.0e-6` (with the dot) — PyYAML parses `16e-6` as a
  string.
- `Params` is frozen; use `dataclasses.replace` for overrides.
- Engaged-mode ω is integrated (not substituted); drift vs Gt·ṙ_b is a V1a
  check, keep it that way.
- Reflected inertance Jr ≈ 660 kg at baseline (J=3e-4, Gt≈1484) — dominant,
  physical for MMR class; sensitivity study must expose it.
- Run `pytest -q` (V1 + units, ~1 min); validation anchors will be
  `pytest -m validation`.

## Process

Conventional commits. Update LAB_NOTEBOOK.md every session with what was
tried, what failed, why. Verify each validation gate before starting the
next.
