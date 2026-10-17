# Experiment 005 — bias-spring ratio k_b/k_m × frame travel

**Question.** The central design tension of `01_physics.md` §3.3: a soft
stage with 2–5 in of travel can only absorb a few percent of corner-load
variation before it binds. Map output, φ, time on a stop, stop contacts per
km and ride delta over the ratio (0.05–0.8) and travel (2 / 4 / 5 in).

**Setup.** `config.yaml`. Mid-size car, ISO C, 60 mph, 40 s, 3 seeds,
stock damper, r = 300, J = 3e-5, load re-swept, 138 cases, 0 errors.

**Answer** (`results/RESULTS.md`): **on ISO C with the stock damper the
frame never reaches a stop at any ratio or travel**, and travel has no
effect on any metric; the ratio moves output by 25 %:

| k_b/k_m | frame stroke RMS | P_elec [W] | φ | ΔW_k | ΔDTL |
|---|---|---|---|---|---|
| 0.05 | 9.2 mm | 10.0 | 0.081 | −5.4 % | −1.5 % |
| 0.12 (prototype) | 9.1 mm | 9.7 | 0.079 | −5.6 % | −1.6 % |
| 0.25 | 8.8 mm | 9.2 | 0.074 | −5.9 % | −1.6 % |
| 0.5 | 7.9 mm | 8.2 | 0.067 | −6.1 % | −1.5 % |
| 0.8 | 6.9 mm | 7.3 | 0.059 | −6.2 % | −1.3 % |

1. **The static argument in F3 was right about the arithmetic and wrong
   about the regime.** With the OEM damper in place the frame stage is
   dominated by the reflected generator damping (c_eq ≈ 900 N·s/m at the
   optimum), not by k_b, and strokes 7–9 mm RMS — a 2 in travel is enough
   with margin on ISO C. Stops become real only when the damper is reduced
   or on class D (experiment 002: 5–12 % of time on a stop, 22–58
   contacts/km at damper ×0.25 on ISO D with 4 in travel).
2. **Soft is slightly better, and the ratio is a weak lever.** The patent's
   k_b < k_m is satisfied by every row; going from the prototype ratio to
   0.05 adds 3 %; going to 0.8 costs 25 %. The static "89.3 % partition"
   does not appear anywhere in the harvest numbers (F1).
3. **The preload split (equilibrium position within the travel) is
   irrelevant** until the stops are reached (tornado, experiment 006).

**Caveats.** Travel limits are symmetric Kelvin–Voigt stops; the bias
spring is linear to the stop (no progressive solid-height behaviour).
Class D and reduced-damper maps are in experiments 002/003.

**Ledger.** 7.3–10.0 W across k_b/k_m 0.8–0.05; t_stop = 0; mid-size car,
ISO C, 60 mph, stock damper. Tag modeled, exp 005, 2026-10-17. Figure
`results/fig_ratio_travel.png`.
