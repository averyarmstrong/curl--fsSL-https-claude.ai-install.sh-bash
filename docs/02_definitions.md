# 02 — Definitions

Every quantity reported anywhere in `aks-lab` is one of the symbols below,
computed by the named function, over the stationary window of a run (start
ramp excluded), with its conditions attached (road class, speed, vehicle,
generator load, damper span, seed). Where a quantity is a ratio, numerator
and denominator are both reported.

| Symbol | Name | Definition | Code |
|---|---|---|---|
| `P_road` | road input power | mean of F_t · ż_r (eq. 5.2) | `power.ledger.rates()` |
| `P_frame` | frame-stage input power | mean of (F_b) · ṙ_b — power entering the Gate stage from the chassis side | `ledger` |
| `P_gate` | generator-path mechanical power | mean of T_c · ω while a clutch is engaged (equivalently the loop area × frequency on a bench) | `ledger` |
| `P_elec` | electrical output | mean of generator electrical power, before any DC-DC stage | `ledger` |
| `P_damper` | damper dissipation | mean c_s ṙ_d² | `ledger` |
| `P_friction` | Gate parasitics | guide friction + overrun drag + clutch impact/slip + windage + generator internal loss, each also reported alone | `ledger` |
| `P_stop` | hard-stop loss | dissipative part of the stop force | `ledger` |
| `P_spring,cycle` | reactive spring power | mean of \|k_m r_m ṙ_m\| (diagnostic: how much elastic energy cycles through the main spring per unit time; it is **not** available energy) | `metrics.energy` |
| **`φ`** | extraction fraction | `P_elec / P_road` | `metrics.energy.phi()` |
| **`φ_s`** | spring-cycle extraction | `P_elec / P_spring,cycle` | `metrics.energy.phi_s()` |
| `η_mech` | Gate mechanical efficiency | `P_gate / P_frame` | `metrics.energy` |
| `η_chain` | electrical chain efficiency | `P_elec / P_gate` | `metrics.energy` |
| `κ` | legacy shorthand | `P_elec / (W_corner · v_rms,susp)` — reported only so prior AKS documents can be compared; never used to predict | `metrics.energy.kappa()` |
| `ΔP_mass` | propulsion penalty of added mass | Δm g (C_rr + sin θ) V (+ Δm a V on a drive cycle) | `metrics.net.mass_penalty()` |
| `ΔP_ride` | ride penalty in watts | **placeholder**, reported as `None` with the ride metrics beside it; `TODO(bench)` | `metrics.net` |
| **`P_net`** | net benefit per corner | `P_elec − P_friction − ΔP_mass − ΔP_ride` (with ΔP_ride = 0 and flagged) | `metrics.net.p_net()` |
| `a_s,rms` | sprung-mass acceleration RMS | unweighted | `metrics.ride` |
| `a_w,rms` | ISO 2631-1 W_k-weighted sprung acceleration RMS | frequency-domain W_k | `metrics.ride.iso2631_wk_rms()` |
| `SWS` | suspension working space | RMS of (z_s − z_u) | `metrics.ride` |
| `x_b,rms`, `t_stop` | frame stroke RMS; fraction of time with a stop force active | | `metrics.ride` |
| `DTL` | dynamic tire load | RMS(F_t)/F_static; fraction of time F_t < 0 | `metrics.handling` |
| `N_eng/km` | sprag engagements per km (A and B separately) | event counts / distance | `metrics.sizing` |
| `T_c,max`, `T_c,99` | sprag torque envelope | max and 99th percentile of transmitted torque; impact impulse Λ max | `metrics.sizing` |
| `N_stop/km` | hard-stop contacts per km (compression / extension) | | `metrics.sizing` |
| `ω` envelope | rotor speed percentiles; fraction of time above alternator cut-in; race-speed max vs lift-off | | `metrics.sizing` |
| `closure` | ledger closure | eq. §6; must be < 0.01 | `power.ledger.audit()` |

Deltas (Q3) are always `Gate − passive baseline`, same road realisation,
equal total corner mass, equal static height; sign convention: negative
Δa_w is a ride improvement.

Tags: `measured` · `modeled` · `target` · `asserted` (prior AKS statement
without calculation) · `unsupported` (contradicted or non-physical).
