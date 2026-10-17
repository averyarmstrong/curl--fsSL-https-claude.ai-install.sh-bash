# Experiment 006 — flywheel inertia sweep and one-at-a-time tornado

**Question.** (a) How much flywheel is needed to hold rotor speed through
clutch hand-over, and what does it cost? (b) Which open parameters
(`docs/09_open_parameters.md`) move the headline numbers, and by how much?

**Setup.** `config.yaml`. Mid-size car, ISO C, 60 mph, 40 s, 3 seeds,
stock damper, baseline r = 300, J = 3e-5, c_gen 0.01, k_b/k_m 0.12, 4 in.
J sweep 1e-5 – 3e-3; tornado over 13 parameters at the low and high end
of their ranges. 102 cases, 0 errors.

**Answer — flywheel** (`results/RESULTS.md`).

| J [kg m²] | J r² [kg] | P_elec [W] | rotor rpm mean / p95 | ΔW_k |
|---|---|---|---|---|
| 1e-5 | 0.9 | 9.7 | 254 / 623 | −5.8 % |
| 3e-5 | 2.7 | 9.7 | 256 / 622 | −5.6 % |
| 1e-4 | 9 | 9.6 | 261 / 614 | −4.9 % |
| 3e-4 | 27 | 9.3 | 273 / 570 | −3.8 % |
| 1e-3 | 90 | 8.9 | 287 / 498 | −3.3 % |
| 3e-3 | 270 | 8.5 | 293 / 432 | −3.4 % |

Speed ripple (std/mean) is ~0.7 at every J: at these rotor speeds the
flywheel never carries the rotor across a full stroke reversal because the
clutches are engaged 90–95 % of the time anyway (the two races hand over
almost continuously on a random road). More J smooths the speed slightly
(p95 falls) and costs output through J r². **For a PM generator that makes
power at any speed, the fly weights are a ride/NVH and clutch-shock choice,
not a power choice; the claim-8 function (keep rotating through transition)
is already provided by the rotor's own inertia.** A claw-pole alternator
would need a speed the flywheel cannot provide (frac > 1600 rpm = 0.01).

**Answer — tornado** (`results/fig_tornado.png`, `results/tornado.csv`),
span of P_elec [W] across each parameter's range, baseline 9.7 W:

| parameter | low end → P_elec | high end → P_elec | span |
|---|---|---|---|
| damper span (main vs full) | **46.8** (main) | 9.7 (full) | 37.1 |
| r (150 – 800) | 10.0 | 5.0 | 5.0 |
| guide friction c_b (20 – 500) | 10.7 | 6.4 | 4.3 |
| overrun drag c_od (5e-5 – 1e-3) | 10.4 | 7.1 | 3.2 |
| k_b/k_m (0.05 – 0.5) | 10.0 | 8.2 | 1.8 |
| c_gen (0.003 – 0.03) | 8.6 | 7.9 | 0.8 |
| c_w, J, m_f, θ_bl | < 0.5 each | | |
| travel, eq_fraction, k_stop | 0 (stops not reached) | | |

1. **Where the OEM damper acts is the largest lever in the design.** With
   the shock between the frame's bottom plate and the axle ("main" span —
   the integrated layout, where the damper does not bridge the Gate) the
   corner yields 46.8 W (φ 0.38) and P_net turns positive (+1.4 W). It is
   not free: tire-load RMS rises 40 % and W_k falls 39 %, the same
   trade as cutting the damper to 10 % in the retrofit layout (experiment
   001: 33 W at +105 % DTL). The integrated layout sits higher on the same
   harvest-vs-grip curve; it does not leave it.
2. **Parasitics matter at the 30–40 % level.** Guide friction and overrun
   drag at the high end of their ranges together remove a third of the
   output; both are measurable on the bench (T1, T0) before any vehicle
   work.
3. **Backlash, plate mass, windage and the stop parameters do not matter**
   on this road at this damping.

**Caveats.** One-at-a-time at a single operating point; interactions
(e.g. damper span × load) are in the Monte Carlo (experiment 007) and the
linear frontier.

**Ledger.** 46.8 W (φ 0.38, DTL +40 %) with the damper on the main stage;
9.7 W with the damper bridging the Gate; mid-size car, ISO C, 60 mph. Tag
modeled, exp 006, 2026-10-17.
