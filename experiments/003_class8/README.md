# Experiment 003 — heavy wheel stations: box truck, Class 8 tractor (empty), Class 8 loaded, MRAP

**Question.** Same model, heavy corners: per wheel station, by ISO class
and speed, output / φ / P_net / ride and tire-load change / stop rate /
rotor speed, as ranges. The brief asks for ranges, never points.

**Setup.** `config.yaml`. Per-station parameter sets in `vehicles.yaml`
(box truck 2.6 t sprung per station, k_t 1.6 MN/m duals; Class 8 empty
1.1 t / 1.8 MN/m; Class 8 loaded 3.6 t / 1.8 MN/m; MRAP 3.45 t / 1.1 MN/m
single). Gate scaled to the host: same k_b/k_m = 1/8.35, 4 in travel,
r = 300, J = 1e-4 (J r² = 9 kg), m_f 20 kg, hardware mass 20–25 kg; load
re-swept (c_gen 0.03 / 0.1 / 0.3); damper ×1 and ×0.25. ISO A–D, 30 and
60 mph, 40 s, 2 seeds, 448 cases, 0 errors, closures < 10⁻⁵.

**Answer — 60 mph, per wheel station** (`results/best_load.csv`).

| station | ISO | supply W | stock damper: P_elec (φ) · P_net · ΔDTL | damper ×0.25: P_elec (φ) · P_net · ΔDTL · t_stop |
|---|---|---|---|---|
| box truck (dual) | B | 271 | 33 (0.12) · −26 · −1 % | 89 (0.33) · +14 · +32 % · 0 |
| | C | 1084 | 132 (0.12) · +53 · −1 % | 356 (0.33) · +213 · +32 % · 0 |
| | D | 4337 | 528 (0.12) · +370 · −1 % | 1227 (0.28) · +812 · +35 % · 11 % |
| Class 8 empty (dual) | C | 1220 | 135 (0.11) · +35 · 0 % | 356 (0.29) · +200 · +52 % · 0 |
| | D | 4879 | 539 (0.11) · +336 · 0 % | 1336 (0.27) · +902 · +54 % · 4 % |
| Class 8 loaded (dual) | B | 305 | 38 (0.13) · −35 · −3 % | 93 (0.30) · +8 · +19 % · 0 |
| | C | 1220 | **153 (0.13) · +57 · −3 %** | 370 (0.30) · +231 · +19 % · 0 |
| | D | 4879 | **614 (0.13) · +425 · −3 %** | 1439 (0.29) · +1076 · +20 % · 4 % |
| MRAP (single) | B | 186 | 24 (0.13) · −47 · −7 % | 53 (0.29) · −23 · −1 % · 0 |
| | C | 745 | 95 (0.13) · +11 · −7 % | 214 (0.29) · +105 · −1 % · 0 |
| | D | 2982 | 381 (0.13) · +239 · −7 % | 838 (0.28) · +602 · 0 % · 4 % |

At 30 mph everything halves (ISO C loaded Class 8: 77 W stock, 185 W
reduced; MRAP 48 / 107 W).

1. **φ is again a corner property**: 0.11–0.13 with the stock damper,
   0.28–0.33 at ×0.25, for every class and speed. Heavy stations harvest
   ten times a car's because their tires are ten times stiffer, not because
   they are heavy (F1).
2. **Net benefit is positive from ISO C at highway speed on every heavy
   station with the stock damper** (+35 to +57 W per station, after 20–25
   kg of hardware each), and on ISO B only with the damper reduced. Per
   vehicle: a loaded tractor-trailer (9 dual stations) nets ~0.5 kW on
   ISO C and ~3.8 kW on ISO D at 60 mph with stock damping; 2.1 / 9.7 kW
   with damping reduced and the tire-load penalty accepted.
3. **The MRAP is the exception that proves the grip rule**: its damper is
   heavy enough (ζ 0.32 on 3.45 t) that cutting it to 25 % leaves dynamic
   tire load unchanged (−1 %) while doubling output. Tactical vehicles with
   over-damped off-road tunes are where damper reduction is cheapest.
4. **Stops** appear only on ISO D at reduced damping (4–11 % of the time,
   12–64 contacts/km with 4 in travel). Heavy stations want more travel or
   a progressive bias spring for off-road duty.
5. **Rotor/race speed** at ISO D reaches p95 of 2400–4300 rpm at r = 300:
   far above sprag lift-off. For heavy vehicles the clutches must sit on
   the slow side of a step-up (or use a lift-off-free sprag) and the
   generator is a 1–2 N·m, 1000–4000 rpm machine.

**Against the public claims.** The deck's "loaded Class 8 ~5 kW average,
10–16 kW rough-road peaks": the model gives 1.4 kW per vehicle gross on
ISO C (5.5 kW on ISO D) with stock damping, 3.3 / 13 kW with damping
reduced. The kilowatt scale is real on rough roads and tactical duty; the
"average roads" label is not (F7).

**Caveats.** Per-station parameter sets are literature-typical, not
measured for a specific truck (`09_open_parameters.md`); the load grid is
coarse and tops out at c_gen 0.1 for the two heaviest stations (their
stock-damper numbers are slightly conservative); air-spring tractors and
leaf-spring trailers are modelled as linear springs; no pitch coupling.

**Ledger.** Table above; tag modeled; exp 003, 2026-10-17. Figures
`results/fig_power_by_class.png`, `results/fig_ride_handling_delta.png`.
