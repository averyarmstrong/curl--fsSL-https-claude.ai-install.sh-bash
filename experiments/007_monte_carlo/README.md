# Experiment 007 — Monte Carlo bands over the open parameters

**Question.** With every open parameter (`docs/09_open_parameters.md`)
drawn from its range at once, and the road realisation drawn too, what are
the 5–95 % bands of P_elec and P_net at the ride/grip-respecting design
point (stock-ish damper, low inertance), and which parameters drive the
spread?

**Setup.** `config.yaml`. 48 Latin-hypercube samples per (vehicle, class):
J, c_eq = c_gen·r², guide friction, overrun drag, windage, backlash, bias
ratio, travel, preload split, generator efficiency, plate mass, hardware
mass (×0.6–1.8 of the vehicle estimate); each sample its own road seed;
passive comparator with the same seed and hardware mass. Damper ×0.75,
r = 300. Vehicles: mid-size car, F-150, HMMWV, Class 8 loaded; ISO B/C/D;
60 mph; 40 s. 1,152 cases, 0 errors, closures < 10⁻⁵.

**Ugly run, reported first.** The first pass applied the passenger-car
load range (c_eq 250–800 N·s/m) to the Class 8 station, whose optimum is
~9,000 N·s/m (experiment 003). Its φ came out 0.026 instead of 0.13 and the
Spearman table shows P_elec pinned to c_gen (+0.80) — a grid-edge artefact,
not physics. The config now carries a per-vehicle load range and the Class
8 rows were re-run (`results/RESULTS.md` is the regenerated table, superseded rows filtered
by case id); the first-pass table is in git history (commit 45c7db5).

**Answer — bands (5 % / median / 95 %), 60 mph** (`results/bands.csv`).

| corner | ISO | P_elec [W] | φ (median) | P_net [W] | ΔW_k (median) | ΔDTL (median) | t_stop p95 |
|---|---|---|---|---|---|---|---|
| mid-size car | B | 1.4 / 2.3 / 3.1 | 0.076 | −44 / −31 / −16 | −18 % | +4 % | 0 |
| | C | 5.6 / 9.2 / 12.3 | 0.075 | −45 / −31 / −13 | −18 % | +4 % | 0 |
| | D | 22 / 35 / 46 | 0.072 | −54 / −27 / +1 | −18 % | +5 % | 0.13 |
| F-150 | B | 2.3 / 3.5 / 5.0 | 0.083 | −53 / −37 / −19 | −14 % | +3 % | 0 |
| | C | 9.4 / 14.0 / 20.0 | 0.083 | −55 / −37 / −14 | −14 % | +3 % | 0 |
| | D | 37 / 53 / 73 | 0.077 | −73 / −28 / +9 | −14 % | +3 % | 0.10 |
| HMMWV | B | 4.2 / 6.4 / 8.4 | 0.094 | −66 / −46 / −23 | −12 % | +6 % | 0 |
| | C | 17 / 25 / 34 | 0.094 | −72 / −45 / −13 | −12 % | +6 % | 0.01 |
| | D | 62 / 96 / 125 | 0.089 | −112 / −32 / +30 | −12 % | +6 % | 0.14 |
| Class 8 loaded (dual) | B | 31 / 40 / 44 | 0.130 | −83 / −48 / −13 | −12 % | −2 % | 0 |
| | C | 125 / 159 / 176 | 0.130 | −16 / +36 / +85 | −12 % | −1 % | 0 |
| | D | 475 / 624 / 703 | 0.129 | +204 / +368 / +503 | −12 % | −1 % | 0.09 |

1. **The bands are a factor of ~2 wide in P_elec** and are set by the
   Gate's own parasitics, not by the road: Spearman rank correlation of
   P_elec with guide friction −0.6, overrun drag −0.45, generator
   efficiency +0.33, travel −0.3 (shorter travel with the ×0.75 damper
   occasionally clips), rotor inertia −0.2; backlash, preload split, plate
   mass and windage do not matter. The first bench tests (T0, T1 in
   `05_bench_protocol.md`) measure exactly the two dominant terms.
2. **P_net is negative across the band for all three light vehicles on
   B and C**, and straddles zero on D; its spread is dominated by the
   hardware-mass range (6–18 kg per corner for the car). A 6 kg unit on
   ISO D is where the car first nets watts.
3. **Ride improves and tire load worsens in every sample** (median W_k
   −12 to −18 %, DTL +3 to +6 %) at damper ×0.75 — a milder point on the
   same harvest/grip curve as experiments 001/006.
4. **Stops** are a tail event on class D only (p95 of 10–14 % time on a
   stop; median 2 %).

**Caveats.** Latin hypercube over independent ranges (no correlations
between parameters); one design point per vehicle; the surrogate-derived
load range is right for the light vehicles and was wrong for the Class 8
station in the first pass (now corrected).

**Ledger.** Mid-size car ISO C: 5.6–12.3 W (median 9.2); F-150 9.4–20 W
(14); HMMWV 17–34 W (25); Class 8 loaded station 125–176 W (159), P_net
−16…+85 W; ISO D 475–703 W, P_net +204…+503 W. Tag
modeled, exp 007, 2026-10-17. Figure `results/fig_bands.png`.
