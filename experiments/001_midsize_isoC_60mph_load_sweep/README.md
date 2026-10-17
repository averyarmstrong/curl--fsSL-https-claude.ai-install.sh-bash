# Experiment 001 — mid-size car, ISO C, 60 mph: generator-load sweep

**Question.** As the generator load varies, what fraction φ of the road's
power does the Gate take, what is P_net after its own losses and its mass,
how do ride (ISO 2631 W_k) and dynamic tire load change against the stock
passive corner, and how often does the frame hit its stops?

**Setup.** `config.yaml`. Mid-size car corner (400/40 kg, k_m 20 kN/m,
c_s 1500 N·s/m, k_t 180 kN/m), ISO C at 26.82 m/s, 40 s runs, 3 road
seeds, stationary window from 5 s. Gate: k_b/k_m = 1/8.35 (prototype
ratio), 4 in travel centred, linear generator (η 0.85), guide friction
100 N·s/m, overrun drag 2×10⁻⁴ N·m·s/rad, no backlash. Axes: c_gen 2×10⁻⁴
– 0.1 N·m·s/rad; (r, J) ∈ {1484, 300} × {3×10⁻⁴, 3×10⁻⁵}; and, after the
first pass, OEM damper scale 1 / 0.5 / 0.25 / 0.1 on the Gate corner at
r = 300. Passive comparator: same road seed, stock damper, +10 kg sprung.
273 cases, 0 errors, every ledger closure < 10⁻⁵.

**Answer (medians over seeds; full tables in `results/RESULTS.md`).**

| configuration | best c_gen | P_elec [W] | φ | P_net [W] | ΔW_k accel | ΔDTL | frame RMS |
|---|---|---|---|---|---|---|---|
| r 1484, J 3e-4 (J r² = 661 kg), damper ×1 | 0.002 | 3.4 | 0.03 | −25 | −1 % | +1 % | 3.8 mm |
| r 300, J 3e-5 (J r² = 3 kg), damper ×1 | 0.01 | 9.7 | 0.08 | −21 | −6 % | −2 % | 9.1 mm |
| r 300, J 3e-5, damper ×0.5 | 0.005 | 13.8 | 0.11 | −21 | −34 % | +16 % | 13 mm |
| r 300, J 3e-5, damper ×0.25 | 0.005 | 20.1 | 0.16 | −19 | −51 % | +49 % | 16 mm |
| r 300, J 3e-5, damper ×0.1 | 0.005 | 32.9 | 0.26 | −14 | −57 % | +105 % | 19 mm |

Road supply (exact): 122.0 W per corner; the passive damper dissipates
123.4 W in the same simulations (the theorem, `docs/01_physics.md` §7).

1. **Load optimum.** The best reflected damping c_gen·r² is 450–900 N·s/m
   at every damper setting; it is a broad optimum (factor 2 in c_gen costs
   < 15 %). At r = 1484 the same reflected damping needs c_gen ≈ 2×10⁻⁴ and
   the best output is a third of the r = 300 value: the reflected inertance
   J·r² (661 kg) holds the frame stroke to 3.8 mm RMS (F2).
2. **The stock damper keeps ~90 % of the budget.** With the OEM shock in
   place the Gate reaches φ = 0.08. Every additional watt comes from
   removing damping, and the series frame stage cannot replace it: at
   damper ×0.1 the W_k acceleration falls 57 % (a softer, floatier body)
   while dynamic tire-load RMS doubles — a corner that does not hold the
   road. There is no load setting at which the Gate corner matches the
   stock corner's tire load and harvests more than ~10 W (F5).
3. **P_net is negative at every point** for this vehicle on this road:
   P_elec ≤ 33 W against 26 W of mass penalty (10 kg at 60 mph, C_rr 0.01)
   plus 1–3 W of Gate parasitics. Break-even needs ISO D or a lighter unit.
4. **Hard stops are never reached** (t_stop = 0 except 0.03 % at damper
   ×0.1): on ISO C the 4 in frame never travels more than ±25 mm RMS at
   these loads. The stop question is a class-D and heavy-vehicle question
   (experiments 005, 003).
5. **Rotor speed** 250–700 rpm at the useful points: below any claw-pole
   alternator's cut-in. A PM machine wound for this band is required.
6. **Engagements** ≈ 170 per km per clutch set (both A and B, symmetric):
   the clutch indexes ≈ 1.7×10⁵ times per 1000 km.
7. **Linear surrogate check** (`fig_surrogate_vs_sim.png`): the exact H₂
   model of the linearised corner predicts the nonlinear median within
   ~10 % wherever the clutches are engaged > 85 % of the time; it
   overpredicts by up to 2× at J r² = 66 kg (engaged fraction 0.8–0.9,
   inertance only acts when locked). Use the surrogate for grid design, the
   hybrid model for numbers.

**Caveats.** Quarter car, white-velocity ISO road, point-contact tire with
no damping, linear generator, viscous friction and overrun drag, open
hardware mass (10 kg estimate; the mass penalty is the largest single term
in P_net). The Gate's own ride benefit (W_k down) is real but comes with
the tire-load cost; neither is converted to watts.

**Numbers for the ledger.** 9.7 W (9.5–9.9) per corner, φ 0.079, stock
damper, best load; 32.9 W (31.9–33.3) at damper ×0.1 with DTL +105 %.
Tag: modeled. Exp 001, 2026-10-17.

Figures: `results/fig_load_sweep.png`, `results/fig_frame_rotor.png`,
`results/fig_surrogate_vs_sim.png`.
