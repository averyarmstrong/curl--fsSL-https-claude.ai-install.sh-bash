# 09 — Open parameters

Parameters the supplied materials do not fix. Each carries the labeled
engineering estimate used by default in `params/`, the range swept, and
what would close it. Nothing here is load-bearing for a validation gate.

| Parameter | Default (estimate) | Range swept | Why open | Closes when |
|---|---|---|---|---|
| Transmission ratio `r` [rad/m] | 1484 (1 in lead screw × 6:1) | 200 – 4000 | patent says "spiral gears", no lead or ratio | drive-rod drawing / part numbers |
| Rotor + flyweight inertia `J` [kg·m²] | 3×10⁻⁴ | 3×10⁻⁵ – 1×10⁻² | flyweight geometry unknown; tech brief example 0.01 | flyweight drawing |
| Vehicle-scale bias-spring rate `k_b` | k_m/8.35 (prototype ratio) | k_m/20 – k_m/1.5 | only bench-scale articles exist | vehicle-scale spring order |
| Frame travel `T` and preload split (`x_c`, `x_e`) | T = 0.10 m, centred | 0.05 – 0.13 m; split 0.3–0.7 | patent 2–5 in; preload not specified | housing drawings |
| Moving plate mass `m_f` [kg] | 8 | 3 – 15 | plate drawings missing | housing drawings |
| Gate hardware mass per corner `Δm` [kg] | 12 | 6 – 25 | housing, generator, flyweights unknown | weighed prototype |
| Guide friction `c_b` [N·s/m] | 100 (viscous equiv.) | 20 – 500 | real friction is partly Coulomb | bench force–velocity loop with generator open-circuit |
| Overrun drag `c_od` [N·m·s/rad] | 2×10⁻⁴ (≈0.1 N·m at 500 rad/s slip) | 5×10⁻⁵ – 1×10⁻³ | catalog 0.05–0.5 N·m, part not chosen | clutch part number + catalog |
| Backlash `θ_bl` [rad] | 0 | 0 – 0.01 (≈0.5°) | catalog < 0.5° | clutch part number |
| Sprag torque capacity `T_cap` [N·m] | ∞ | 2 – 50 | part not chosen; catalog practice: nominal torque × indexing service factor 2–4 (Stieber: roller 3.0 / sprag 4.0 above 150 strokes/min; Formsprag 2–3 below, 3–4 above 150 spm, +50 % with vibration) | clutch part number |
| Clutch life basis [cycles] | none | — | **no manufacturer publishes a cycles-to-failure basis** for sprag/roller freewheel ratings; one patent background says "a few hundred thousand to a few million high-torque cycles"; GMN rates indexing frequency 10 Hz (Z) – 60 Hz (M) types; no MMR endurance test exists in the literature (research_round2 §1) | bench endurance leg T6 |
| Centrifugal lift-off [rpm] | 1200 | 800 – 1500 | catalog range | clutch part number |
| Windage/bearing `c_w` [N·m·s/rad] | 5×10⁻⁵ | 1×10⁻⁵ – 5×10⁻⁴ | — | spin-down test (V1b protocol) |
| Generator `c_gen` [N·m·s/rad], `η` | swept; η = 0.85 | c_gen 10⁻⁴ – 10⁻¹; η 0.5 – 0.92 | PHINIA map not received | generator dyno map |
| Hard-stop `k_stop`, `c_stop` | 2×10⁶ N/m, 8×10³ N·s/m | ±10× | bump-rubber choice | hardware |
| Tire damping `c_t` | 0 | 0 – 500 N·s/m | literature 1–2% ζ | — |
| Rolling resistance `C_rr` (for ΔP_mass) | 0.010 | 0.007 – 0.012 | tire class | — |
| Damper span (`main` vs `full`) | `full` | both | retrofit vs integrated | design decision |
| Vehicle parameter sets | see `src/aks_lab/vehicles/*.yaml` | — | literature-typical values, cited in file; truck tire 764–1025 kN/m per tire (Wong/UMTRI), 800 kN/m duals (HVTT17); Class 8 drive-axle unsprung 640–1150 kg per axle group (model tables); HMMWV secondary set added | full texts: UMTRI-86-12, SAE 931693 |

Each entry that changes any headline number by more than the reported
range appears on the tornado chart in `experiments/006_*/`.
