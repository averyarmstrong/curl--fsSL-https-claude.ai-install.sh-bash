# Experiment 004 — transmission ratio r [rad/m]

**Question.** The patent fixes no linear-to-rotary mechanism. As r varies
(100–3000 rad/m) at two rotor inertias, with the generator load rescaled so
the reflected damping c_gen·r² stays comparable: output, φ, mechanical
efficiency, engagement rate, race speed vs sprag lift-off, ride delta.

**Setup.** `config.yaml`. Mid-size car, ISO C, 60 mph, 40 s, 3 seeds,
stock damper, 129 cases, 0 errors. c_gen = scale × 0.01 × (300/r)² with
scale 0.3 / 1 / 3; best scale reported.

**Answer** (`results/RESULTS.md`).

| J [kg m²] | r | J r² [kg] | P_elec [W] | φ | η_mech | rotor rpm p95 | T_c p99 [N·m] |
|---|---|---|---|---|---|---|---|
| 3e-5 | 100 | 0.3 | 10.7 | 0.087 | 0.73 | 408 | 1.53 |
| 3e-5 | 300 | 2.7 | 9.7 | 0.079 | 0.87 | 622 | 0.89 |
| 3e-5 | 800 | 19 | 6.4 | 0.052 | 0.89 | 760 | 0.51 |
| 3e-5 | 1484 | 66 | 3.8 | 0.031 | 0.79 | 1078 | 0.29 |
| 3e-5 | 3000 | 270 | 1.0 | 0.008 | 0.65 | 1132 | 0.14 |
| 3e-4 | 100 | 3.0 | 10.5 | 0.086 | 0.90 | 217 | 2.67 |
| 3e-4 | 300 | 27 | 9.3 | 0.075 | 0.88 | 570 | 1.05 |
| 3e-4 | 1484 | 661 | 3.4 | 0.027 | 0.80 | 881 | 0.36 |

1. **J r² is the variable, not r or J.** J = 3e-4 at r = 100 (3 kg) gives
   the same output as J = 3e-5 at r = 300 (2.7 kg). Output is flat below
   J r² ≈ 5 kg, down a third at 20 kg, down two-thirds at 66 kg (the
   gate-twin baseline), and gone at 270 kg. Design rule for a passenger-
   car corner: **J r² ≲ 10 kg**; for heavy stations it scales with the
   corner mass (experiment 003 uses J r² = 9 kg at 1–3.6 t sprung).
2. **Torque and speed trade through r.** At r = 100 the rotor sees 1.5–2.7
   N·m at ~200–400 rpm; at r = 1484, 0.3 N·m at ~1000 rpm. The generator
   must be specified at the chosen r; none of these points reach a claw-
   pole cut-in.
3. **Mechanical efficiency** of the Gate (P_gate/P_frame) is 0.85–0.90 in
   the useful band; it falls at r = 100 because overrun drag (viscous,
   c_od) is a larger share at low rotor speed, and at r = 3000 because the
   inertance makes the frame store and return energy through the clutches.
4. **Race speed vs lift-off.** With the sprags on the race at r, race rpm =
   r·|ṙ_b|·60/2π; 95th percentiles stay under 1200 rpm here (ISO C) but
   the maxima do not (`reports/component_sizing.md` §5), and class D
   exceeds it everywhere (experiment 002). Place the clutches before any
   step-up, or specify a lift-off-free sprag.
5. **Ride.** W_k acceleration −10 % (r = 100) to −1 % (r = 3000); tire
   load within ±2 %. Low J r² also gives the better ride.

**Caveats.** c_gen rescaling keeps c_gen·r² at 300–2700 N·s/m, which
brackets the optimum found in experiments 001 and the linear frontier; the
viscous overrun-drag model penalises low r more than a constant catalog
drag would.

**Ledger.** J r² ≲ 10 kg rule; 9.7 ± 0.2 W at r = 300; 3.8 W at r = 1484
(mid-size car, ISO C, 60 mph, stock damper). Tag modeled, exp 004,
2026-10-17. Figure `results/fig_ratio_sweep.png`.
