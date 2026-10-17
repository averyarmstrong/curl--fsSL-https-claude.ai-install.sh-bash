# gate-twin lab notebook

Running record of what was tried, what failed, and why. Newest entries at
the bottom. Candor is the point — ugly runs get written down.

---

## 2026-07-02 — Session 1: scaffold, physics core, V1 gates

**Goal:** repo scaffold, PHYSICS.md, hybrid model, V1 analytic gates.

### Decisions

1. **Sprag model: exact kinematic constraint + event-driven mode switching**
   (modes free/engA/engB), not high-stiffness penalty coupling. Rationale:
   (a) the <1% energy-closure gate wants a ledger exact to solver tolerance —
   penalty contact adds a stiff spring whose stored energy sloshes into the
   audit; (b) the penalty stiffness reflected through Gt ≈ 1484 (rad/s)/(m/s)
   creates ~kHz modes that would force tiny steps. Engagement events occur at
   zero relative speed, so they are impact-free; disengagement is the
   physical T_c = 0 (a sprag cannot pull). Grazing engagements (T_c < 0 at
   contact) are rejected with a 1e-8 s micro-step; a Zeno counter guards
   chatter.

2. **Reflected inertance.** With patent-brief kinematics (lead 1 in/rev,
   step-up 6) a generator-shaft inertia J = 3e-4 kg·m² reflects onto the
   frame stroke as Jr = J·Gt² ≈ 660 kg. This is not a bug: MMR-class devices
   are known to behave as large inerters (Li & Zuo 2013). It WILL shape V2
   calibration and must be a headline axis of the sensitivity study. Flagged
   in PHYSICS.md §8.

3. **Energy integrals as ODE states** (damper, stop, clutch, electrical,
   generator loss, road work) so the audit is limited only by rtol. Stop
   force clipping is booked exactly by splitting conservative (½k·pen²) from
   the residual.

4. **Coordinates:** perturbations about static equilibrium → gravity cancels;
   frame travel ±x_b_max symmetric about loaded equilibrium (asymmetric
   preload deferred, noted in PHYSICS.md).

### Failures / gotchas hit

- PyYAML parses `16e-6` as a *string*; wrote `16.0e-6`. Added a params test
  that yaml and dataclass defaults agree so drift is caught.
- Loader bug: `_leaf` was indexing the dict with the dotted path label.
- **Ugly run, reported per honesty norms:** first V1d bench run passed the
  closure gate but the ledger showed **57% of input energy going to sprag
  overrun drag** (1100 J of 1914 J; electrical fraction only 29%). Cause:
  first-guess c_od = 5e-3 N·m·s/rad gives ~3.5 N·m drag at ~700 rad/s slip —
  10–70× sprag-catalog drag (0.05–0.5 N·m), and reflected through Gt² it is
  a ~22,000 N·s/m parasitic damper on the stroke. Corrected to c_od = 2e-4
  (≈0.1 N·m at 500 rad/s slip, catalog-anchored). This is a prior correction
  to published hardware data, not tuning to a power target — but it shows
  how sensitive the architecture is to overrun drag × Gt²; c_od goes on the
  tornado-sensitivity list.

### V1 status

See `tests/test_v1_gates.py` — results recorded in session summary and CI.

### Next session

V2: configure single-corner rectifier at 0.047 m/s RMS suspension velocity,
reproduce Zuo MMR ≈40 W/unit and >60% mechanical efficiency within ±25%.
Pull the actual Li/Zuo 2013 numbers via web search and cite precisely
(power level, device kinematics, test conditions) before running anything.

---

## 2026-10-17 — Session 2: gate-twin → aks-lab, the road-power theorem, first sweeps

**Goal.** Execute the AKS Lab kickoff brief: intake every prior AKS
document, derive the physics by hand, rebuild the package as `aks_lab`,
validate against closed forms and the Zuo baseline, run experiments
001–006, write prior art / claims audit / bench protocol / findings.

### What was tried, what failed, why

1. **Website fetch failed** (DNS not resolvable through the proxy). Used the
   114-page Website Blueprint from Drive as the tone of record instead.
2. **Several brief-named inputs do not exist** in Drive or the uploads:
   `aks_quarter_car_v0.py`, `AKS_ClaudeCode_Prompt_DigitalTwin.md`,
   `AKS_Armstrong_Gate_Simulation.html`, `Housing plate 1/2.pdf`, Larry's
   drawing JPEGs, and the "14 W measured" record. Logged in 00_intake and F4.
3. **The fixed-body road-power derivation was wrong.** I first wrote
   P̄ = W_v k_t²/(4(k_t+k_eff)); the exact Lyapunov evaluation returned
   W_v k_t/4 for *every* parameter set including m_s → ∞. Cause: a body
   fixed in absolute space under a Brownian road is non-stationary (the
   main spring stretches without bound), so the 1-DOF limit is singular.
   The correct statement is the stronger one — P̄ = ¼ k_t W_v, independent
   of everything above the tire, nonlinear corners included — and it is now
   proved in 01_physics §7 and tested both ways. The failed test is kept as
   `test_fixed_body_formula_is_not_the_limit` so the pitfall is documented.
4. **ISO 2631 W_k came out exactly 2× high.** The upward-step stage was
   written with an (ω₆/ω₅)² normalisation that the standard's tabulated
   weights contradict (W_k → 1 above ~4 Hz, ≈ 0.48 at 1 Hz). Removed; all
   seven tabulated points now match within 5%.
5. **Bench-rig ledger failed to close with backlash.** The lock-up impulse
   J·Δω is reacted by the kinematic actuator at race speed and does work
   J·Δω·ω_race that the integrated F·ẋ cannot see. Booked at the event;
   closure returned to 1e-9.
6. **Slip mode went negative in the clutch ledger.** The "relock" exit from
   slip let the rotor overtake the race while still transmitting T_cap. A
   one-way clutch cannot do that: slip now exits to FREE when the race falls
   behind, and re-engagement goes through the normal engage event. Closure
   exact.
7. **Vehicle provenance correction.** I had labelled the mid-size-car
   parameter set as "Zuo & Zhang 2013 Table 1" from memory; the prior-art
   dossier confirms the paper's table was not retrievable here. Relabelled
   as literature-typical values with the derivation shown. The validation
   (b) band (122–488 W per car, B–C) is therefore our own reproduction of
   the scaling, not a check against their exact parameters.
8. **gate-twin's V2 anchor was mis-cited.** "40 W @ 0.047 m/s RMS" mixed the
   1.5 Hz × 5 mm efficiency condition (peak 0.047 m/s) with the 3 Hz × 5 mm
   power condition (40.4 W). Withdrawn; 04_prior_art item 1.

### Decisions

- Gate element keeps the exact-constraint hybrid formulation; engagement
  impact (backlash), torque-capacity slip, asymmetric stops added. The
  element exposes forces/coupling/events; the host assembles the mass
  matrix. Documented interface in `elements/gate.py`.
- Transmission is one parameter r [rad/m]; the screw+step-up reading is a
  derived convenience.
- Damper span `full` (OEM shock bridging the Gate) is the default retrofit
  topology; `main` is kept and swept.
- ΔP_ride stays `None` with the ride metric beside it; no exchange rate is
  invented.

### Results so far (details in experiment READMEs)

- Validation (a): transmissibility < 1% at 0.7/1.1/3/11 Hz. (b): 30 /
  122 / 488 / 1952 W per car for A/B/C/D at 60 mph. (c): hand derivation to
  0.5%. Ledger closure 1e-6–1e-9 on every path.
- F1–F4 written before any sweep completed (08_findings).
- Smoke run: at r = 1484, J = 3e-4 the frame strokes 3.7 mm RMS and yields
  3 W; at r = 300, J = 3e-5, 10 mm and 11 W at c_gen 0.01 (ISO C, 60 mph,
  mid-size car). Reflected inertance is the first-order design variable.

### Ugly things to keep in view

- Per-sim cost ~0.5 s per simulated second on one core; sweeps are hours,
  not minutes. Numba or a compiled RHS is the next performance step.
- Bench `c_eq_fit` (99 N·s/m) differs from c_gen r² (45 N·s/m) when J > 0
  because the fit absorbs inertance and partial engagement — the bench
  comparison must run the model with the measured J, not read c_gen off the
  fit.

### Later in session 2 (03:00–03:10)

- **Exp 001 first pass**: φ 0.03–0.08 with the stock damper; best c_gen 0.01
  at r = 300 (c_eq = 900 N·s/m). P_net negative. Added `c_s_scale` axis and
  re-ran; chain 001→002→004→005→006→003 launched 02:57.
- **Linear surrogate** (`validate.analytic.linear_gate_power`): exact H₂ of
  the corner with the frame stage as k_b ∥ c_eq ∥ inerter. Matches the
  nonlinear point (10.6 vs 9.7 W). Gave the frontier in minutes: optimum
  c_eq ≈ 300–500 N·s/m, nearly independent of k_b/k_m; tire-load variation
  is the binding constraint; passenger-car P_net < 0 below ISO D (F5).
  Lesson: build the linear surrogate *first* next time; it would have set
  the sweep grids correctly before burning CPU on r = 1484.
- **numba RHS** (`vehicles/quarter_car_fast.py`): 3.5× faster with the
  cores loaded; equivalence to the reference 1e-4 (3 configurations incl.
  backlash and torque-capacity slip). Sweeps default to it.
- **Exp 007 (Monte Carlo)** script written; 1152 cases; to run after the
  chain.

### Session 2 close-out (03:55)

- Chain finished 03:52: 1,794 cases, 0 errors, max closure 7.6e-6.
- φ is a corner property (stock damper 0.08–0.13 across all classes,
  speeds, vehicles); heavy stations are 10× a car because of tire
  stiffness; P_net > 0 from ISO C at highway speed for heavy stations only.
- Damper placement is the biggest lever (46.8 W vs 9.7 W, mid-size car) and
  trades grip exactly like damper reduction. Harvest-vs-tire-load is one
  curve.
- Stops never reached on ISO C at stock damping (F3 regime corrected);
  class D with reduced damping: 4–12 % of time on a stop.
- Race speed exceeds catalog lift-off above r ≈ 200 rad/m at the peaks;
  clutch must sit on the slow side of a step-up or be lift-off-free.
- Launched exp 007 Monte Carlo (48 LHS samples × 4 vehicles × 3 classes).
- Ugly: the c_gen grids in 002/003 top out for the heaviest stations
  (stock-damper optimum at the grid edge) → those numbers are slightly
  conservative; widen the grid next run. The linear surrogate's optimum
  (c_eq 300–500 for a car) scales with corner impedance for trucks; use it
  to set grids first.
- **Tire-damping check (04:05).** c_t 0/300/1000 N·s/m, midsize ISO C 60 mph:
  P_road 121/179/303 W (the tire dashpot eats band-limited white velocity
  up to the 76 Hz synthesis edge), P_elec 9.5/8.8/7.8 W. The extra is tire
  heat, not suspension budget. Ledger note: the passive model books tire
  loss under E_genloss (no machine present) — rename to E_tire if c_t is
  ever used in a sweep; all experiments ran c_t = 0.

## 2026-10-17 — Session 3: gravity / wind / lift-off objection

Avery's objection: the theorem ignores gravity, weight, torque, heave,
tire deformation, tires jumping, wind. Turned each into a test or a run
(exp 008, F8). Two bugs of mine on the way, both caught by the tests: the
full-gravity comparison model omitted the spring preload (body sank 25 cm —
the check worked), and I first asserted the random-road invariance on a
deterministic bump where it does not hold (reworded to "not ∝ weight",
which it is not: 153 → 108 J for 4× mass). The 19th state `E_body` changed
NSTATE; the numba model and the 1e-4 equivalence test still pass. Reference
model only for body-force / one-sided cases (~5 s per simulated 40 s).
Outcome: wind ≤ 2 W per corner at 400 N RMS per vehicle; powertrain 0;
lift-off −1 % (D) / −12 % (E) of supply; gravity identical to 1e-6.
