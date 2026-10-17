# 05 — Bench protocol (Duke rig) and data reduction

Purpose: make the first physical test of the Gate produce the **same
metrics the model reports**, under conditions where the model has a hand-
checkable prediction, so that agreement or disagreement is unambiguous.
Pre-registered: the predictions below are fixed before the test; the data
are reported either way (`LAB_NOTEBOOK.md`).

## 1. Article

The v1 bench article: Ebsco EB-7234 bias spring (1.905 lbf/in, 5.50 in
free, 3.256 in to solid) and EB-7233 main spring (15.902 lbf/in) in the
machined housing (`data/prototype/prototype_v1.yaml`). Drive ratio r and
rotor inertia J are **unknown** (open parameters) and are the first things
the bench measures (§4, tests T1–T2).

## 2. Instrumentation (minimum)

| Channel | Sensor | Rate | Why |
|---|---|---|---|
| frame stroke x(t) | LVDT or string pot on plate 109 vs 111 | ≥ 1 kHz | loop area, stroke amplitude |
| actuator force F(t) | load cell in series with the shaker | ≥ 1 kHz | loop area = energy per cycle |
| rotor speed ω(t) | optical tach or Hall on the rotor | ≥ 1 kHz | one-way check, ripple, J fit |
| DC output v, i | shunt + divider after the rectifier into a resistive load | ≥ 1 kHz | P_elec, η_chain |
| housing temperature | thermocouple on the generator | 1 Hz | drift check |

Load: a switchable resistor bank (at least 5 values spanning a decade) so
c_gen can be swept; record R_load per run.

## 3. Test matrix

Prescribed sinusoidal stroke about a preload (the Diligence Response
proposed 2.0 in preload; keep it, and record the actual standing force).

| Test | Amplitude a | Frequency f | Load | Purpose |
|---|---|---|---|---|
| T0 | 0 | 0 | open | spin rotor by hand to ω₀, record decay → c_w = J·(decay rate) once J known |
| T1 | 3 mm | 0.5 Hz | open | quasi-static: F–x line slope = k_b; residual loop = guide friction |
| T2 | 3, 6 mm | 0.5–4 Hz sweep | open | engaged-mode inertance: F–x loop gains a mass-like term J r² ẍ; fit J r² |
| T3 | 6, 12.7 mm | 1, 2, 3 Hz | 5 loads | **power curve**: P_in, P_elec vs load; confirms full-wave (both clutches engage; ω never negative) |
| T4 | 12.7 mm | 2.5 Hz | best load | 30-min run: temperature drift, engagement count, any clutch chatter |
| T5 | stroke to the stop | 1 Hz | best load | stop contact: force spike, loss per contact |

Amplitudes stay ≥ 20% below the coil-bind margin (3.256 − 2.0 = 1.256 in
after preload) except in T5.

## 4. Pre-registered predictions

From `01_physics.md` §11 with J → 0 (no losses): mean mechanical power into
the generator path

    P̄ = ½ c_gen r² (2π f a)²

The Diligence Response's "1.7–5.2 W mechanical at ±0.5–1.0 in, 2–3 Hz"
corresponds to a reflected damping c_gen r² between

    c_gen r² = 2 P̄ / (2π f a)²  →  1.7 W at 2 Hz, 12.7 mm: 133 N·s/m
                                   5.2 W at 3 Hz, 25.4 mm: 45 N·s/m

i.e. the prediction is only a prediction once r and c_gen are fixed. **The
bench therefore measures c_eq = c_gen r² directly** (slope of the
non-conservative force F − k_b x against ẋ; `bench/reduce.py::reduce_run`)
and the model's prediction for each load is `aks_lab.BenchRig` run with the
measured J, r, c_eq. Pass band: measured P_in within ±25% of the BenchRig
prediction at every T3 point; measured η_chain = P_elec/P_in within ±0.10
of the generator's own efficiency at that load.

Falsification statements (fixed now):

1. If the F–x loop area with the generator **open-circuit** exceeds 30% of
   the loop area at the best load, the device is friction-dominated and the
   "soft stage routes energy to the generator" mechanism is not demonstrated
   at this scale.
2. If ω goes negative or only one clutch set is seen to engage over a
   cycle, full-wave rectification (claim 4) is not demonstrated.
3. If the engaged-mode inertance J r² fitted in T2 exceeds ~0.1 × (the mass
   the article is meant to serve), the drive ratio must be reduced before a
   vehicle-scale design (F2).

## 5. Data reduction

`src/aks_lab/bench/reduce.py`: `load_raw` → `clean` (uniform resample,
zero-phase 50 Hz low-pass, remove static offsets) → `cycles` (zero-
upcrossings of x, first 3 cycles dropped) → `reduce_run` (loop area per
cycle and its scatter, P_in, P_elec, η, ω statistics, one-way flag, c_eq
fit). `compare` tabulates bench vs `BenchRig` for the same (a, f, load).

## 6. What the bench cannot tell us

A prescribed-stroke bench measures the Gate's own efficiency and
impedance. It cannot measure φ: the share of *road* power the Gate takes
on a vehicle depends on the corner dynamics (F1). The second test article
should therefore be a quarter-car rig (sprung mass on the Gate + spring +
tire on a shaker) or an instrumented vehicle corner. The brief's "~14 W"
early datum, when supplied, will be interpreted against §4 with its
amplitude, frequency and load.
