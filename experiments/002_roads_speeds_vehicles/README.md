# Experiment 002 — ISO A–D × 30/60 mph × {mid-size car, F-150, HMMWV}

**Question.** Per corner, by road class and speed: electrical output,
extraction fraction φ, net benefit after Gate losses and hardware mass,
ride (W_k) and dynamic-tire-load change against the stock corner, stop
rate, rotor speed — as ranges over road realisations.

**Setup.** `config.yaml`. 40 s runs, 3 seeds, 504 cases, 0 errors, all
closures < 10⁻⁵. Gate at the low-inertance drive point (r = 300 rad/m,
J = 3×10⁻⁵ kg m², J r² = 2.7 kg), k_b/k_m = 1/8.35, 4 in travel, η 0.85;
load re-swept per case (c_gen 0.003 / 0.01 / 0.03); OEM damper at ×1 and
×0.25 on the Gate corner; passive comparator with stock damper and the
vehicle's `gate_mass` estimate added (10 / 12 / 15 kg). Best load per
cell reported; lo/hi = seed range.

**Answer — 60 mph (full tables in `results/RESULTS.md`, `best_load.csv`).**

| corner | ISO | supply W | **stock damper**: P_elec W (φ) · P_net · ΔW_k · ΔDTL | **damper ×0.25**: P_elec W (φ) · P_net · ΔW_k · ΔDTL · t_stop |
|---|---|---|---|---|
| mid-size car | B | 30 | 2.4 (0.08) · −25 · −6 % · −2 % | 4.9 (0.16) · −23 · −46 % · +53 % · 0 |
| mid-size car | C | 122 | 9.7 (0.08) · −21 · −6 % · −2 % | 19.5 (0.16) · −15 · −46 % · +53 % · 0 |
| mid-size car | D | 488 | 38.7 (0.08) · −3 · −6 % · −2 % | 75 (0.15) · +17 · −46 % · +54 % · 5 % |
| F-150 | B | 42 | 3.7 (0.09) · −29 · −1 % · 0 % | 8.7 (0.20) · −31 · −50 % · +26 % · 0 |
| F-150 | C | 169 | 14.8 (0.09) · −23 · −1 % · 0 % | 34.8 (0.20) · −30 · −50 % · +26 % · 0 |
| F-150 | D | 678 | 59 (0.09) · +3 · −1 % · 0 % | 127 (0.19) · +42 · −43 % · +37 % · 6 % |
| HMMWV | B | 68 | 7.3 (0.11) · −34 · +1 % · 0 % | 19.9 (0.29) · −28 · −39 % · +34 % · 0 |
| HMMWV | C | 271 | 29.3 (0.11) · −18 · +1 % · 0 % | 79.5 (0.29) · +8 · −39 % · +34 % · 0 |
| HMMWV | D | 1084 | 117 (0.11) · +48 · +1 % · 0 % | 276 (0.25) · +114 · −38 % · +37 % · 12 % |

At 30 mph every supply and output halves (the theorem is linear in speed);
P_net at 30 mph is positive only on ISO D (F-150 +25 W, HMMWV +68 W at
damper ×0.25; mid-size car +9 W).

1. **φ is a property of the corner, not the road.** With the stock damper
   φ = 0.08 (car), 0.09 (F-150), 0.11 (HMMWV) on every class and speed; at
   damper ×0.25, 0.16 / 0.20 / 0.29 until stops intervene on class D. The
   HMMWV's higher share comes from its stiffer tire and heavier unsprung
   mass relative to its damping, not from its weight.
2. **Break-even is a rough-road event.** Against the hardware-mass penalty
   (26 / 32 / 39 W at 60 mph), P_net > 0 requires ISO D at highway speed
   for the car and the pickup, and ISO C at damper ×0.25 for the HMMWV.
   The pitch-deck "average roads" case (ISO C, 60 mph) is net negative for
   every passenger vehicle in this table (F5).
3. **Reducing the damper buys watts with grip.** Every ×0.25 column has
   dynamic tire load +26 to +54 % and a much softer body (W_k −40 to −50 %).
   The brief's Q3 answer has a sign: harvesting-by-softening improves the
   seat and worsens the contact patch; the stock-damper configuration
   changes neither by more than a few percent.
4. **Stops appear on class D.** 5–12 % of the time on a stop, 22–58
   contacts per km, at damper ×0.25; essentially none at stock damping or
   on A–C. Travel is 4 in centred — experiment 005 maps this.
5. **Rotor/race speed.** 95th-percentile rotor speed 600–1800 rpm at the
   useful points and 3400 rpm on the HMMWV at ISO D; with the sprags on the
   race at r = 300 the race speed equals the rotor speed and exceeds the
   catalog lift-off range (800–1500 rpm) on class D for every vehicle.
   Either the clutches move to the slow side of a step-up or a lift-off-
   free sprag type is required (`reports/component_sizing.md` §5).

**Caveats.** As experiment 001, plus: the load grid is coarse (3 points);
the HMMWV optimum at stock damping sits at the top of the grid (c_gen
0.03), so its stock-damper numbers are slightly conservative. The
`gate_mass` estimates drive P_net and are open.

**Numbers for the ledger.** Above table; tag modeled; exp 002, 2026-10-17.
Figures: `results/fig_power_by_class.png`, `results/fig_ride_handling_delta.png`.
