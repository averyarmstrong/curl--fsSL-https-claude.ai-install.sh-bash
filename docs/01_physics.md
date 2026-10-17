# 01 — Physics: every equation, derived before it appears in code

Scope: the '695 mechanism only. Sign conventions, coordinates and the
energy ledger here are normative; `src/aks_lab/` implements exactly this.
Where a result is known from the literature it is cited and re-derived.

Notation: SI throughout. Positive displacement is **up**. All displacement
coordinates are perturbations about the static equilibrium under gravity, so
gravity and spring preloads cancel identically and never appear in the
equations (they reappear only when converting to physical spring lengths,
§3.4).

---

## 1. Topology

Load path chassis → axle, in series (patent FIG. 7/8):

```
            m_s   sprung mass (chassis share + top plate 109)         z_s
             │
   ╔═════════╧═════════╗   FRAME STAGE (the Gate)
   ║ k_b bias spring    ║   stroke  r_b = z_s − z_f   (+ = frame collapsing)
   ║ c_b guide friction ║   stops   −x_e ≤ r_b ≤ +x_c   (coil bind / full extension)
   ║ drive rod → ratio r → opposed sprags → rotor J → generator
   ╚═════════╤═════════╝
            m_f   moving plate(s) + anything that translates with 111        z_f
             │
   ─────────┴────────── MAIN STAGE  k_m shortened main spring, c_s damper
             │                       r_m = z_f − z_u
            m_u   unsprung mass                                            z_u
             │
   ─────────┴────────── TIRE  k_t (c_t optional, default 0)   r_t = z_u − z_r
             │
            z_r(t)  road elevation
```

The damper c_s is the OEM shock absorber. It spans chassis to axle in the
real car, i.e. across the *whole* stack (z_s − z_u). Two options are
provided and the choice is reported with every result:

- `damper_span = "main"` : c_s acts on ṙ_m (shock mounted between plate 111
  and the axle — the "replacement spring + shock" reading of the patent).
- `damper_span = "full"` : c_s acts on ż_s − ż_u (OEM shock untouched,
  bridging the Gate). This is the drop-in retrofit case and the default.

Newton's second law (free-wheeling clutches):

```
m_s z̈_s = −F_b − F_d·[full]
m_f z̈_f =  F_b − F_m − F_d·[main]
m_u z̈_u =  F_m + F_d − F_t
```

with
```
F_b = k_b r_b + c_b ṙ_b + F_stop(r_b, ṙ_b) + F_drive          (frame stage)
F_m = k_m r_m                                                 (main spring)
F_d = c_s ṙ_d ,   ṙ_d = ṙ_m  or  (ż_s − ż_u)                   (damper)
F_t = k_t r_t + c_t ṙ_t                                        (tire)
```
`[full]`/`[main]` are 1 for the selected damper span, else 0. `F_drive` is
the reaction of the rectifier/generator path on the stroke (§4).

**Passive baseline** (no Gate, Q3 comparator): remove the frame stage,
z_f ≡ z_s, add the Gate hardware mass to m_s (equal total mass), use the
*original* un-shortened spring k_m with the same static height (claim 3 says
the heights add up, so the comparison is at equal ride height by
construction).

---

## 2. The series stack and the static partition (what the AKS documents call "capture fraction")

Two ideal springs in series carry the same force F. Deflections
x_b = F/k_b, x_m = F/k_m; stored energies E_i = F²/(2k_i). Hence

```
E_b / (E_b + E_m) = k_m / (k_m + k_b)                              (2.1)
```

With the bench articles, 15.902/17.807 = 0.893. **This is the fraction of
stored elastic energy that sits in the bias spring at any instant. It is not
an energy flow, not a harvest fraction, and not a ceiling.** A conservative
spring returns everything it stores; the only energy that leaves the stack is
what the generator path and the losses remove. The harvested fraction φ_s
(§8) is a dynamic quantity and is computed, never read off (2.1).

Effective stiffness of the series pair while the frame is between its stops:
```
k_eff = k_b k_m / (k_b + k_m)                                        (2.2)
```
With k_b = k_m/8.35, k_eff = 0.893·k_b = 0.107·k_m: the corner is ~9× softer
than stock until the frame binds. That is a first-order ride change and is
why the hard stops are not a detail.

---

## 3. The frame stage

### 3.1 Bias spring and parasitic friction
`k_b r_b + c_b ṙ_b`. Guide-bar/sleeve friction is modelled viscous
(`c_b`); Coulomb friction is an acknowledged simplification
(`09_open_parameters.md`).

### 3.2 Hard stops (coil bind and full extension)
Compression stop at r_b = +x_c (bias spring solid, plates 109/110 meet),
extension stop at r_b = −x_e (guide-bar retainers). One-sided Kelvin–Voigt
contact, force clipped so a stop can only push:

```
pen = max(0, r_b − x_c) + min(0, r_b + x_e)
F_stop = clip( k_stop·pen + c_stop·ṙ_b ,  sign such that it opposes penetration )
```

Energy: the conservative part ½k_stop·pen² is storage; the remainder
(F_stop − k_stop·pen)·ṙ_b is booked as stop loss `E_stop`. This keeps the
ledger exact even when the clip is active.

### 3.3 Travel budget: how x_c and x_e follow from the spring sheet
Physical bias-spring compression at static load: δ_0 = δ_preload + (W_corner
− F_preload)/k_b where the frame may be assembled with preload F_preload
(spring compressed δ_preload between plates and retained by the guide-bar
shoulders). With total frame travel T (patent intent 2–5 in):

```
x_c = (travel_to_solid − δ_0)      compression margin to coil bind
x_e = δ_0 − δ_preload              extension margin to the retainer
x_c + x_e = travel_to_solid − δ_preload = T
```

The equilibrium sits mid-travel only if the preload is chosen for it. The
force excursion the frame can take before hitting a stop is k_b·x_c in
compression and k_b·x_e in rebound. **Worked example (vehicle scale, from
the Diligence Response's own numbers):** main 200 lbf/in (35 kN/m), bias
24 lbf/in (4.2 kN/m), T = 4 in = 0.102 m centred → ±0.051 m → ±214 N, i.e.
±5% of a 4,300 N corner load. Dynamic spring-force variation on an ISO C
road at 60 mph is of order 10–15% RMS of static load, so **such a frame
would be against a stop most of the time.** This is the central design
tension of the architecture (Q4) and the model must expose it, not hide it.

### 3.4 Static length bookkeeping (claim 3)
L_bias,normal + L_main,shortened = L_OEM. With perturbation coordinates none
of this enters the dynamics; it enters the bench protocol and the component
sizing as the constraint that the shortened main spring must still carry
W_corner within its own travel to solid.

---

## 4. The rectifier: kinematics, sprags, flywheel, generator

### 4.1 Transmission ratio
The patent does not fix the linear-to-rotary mechanism ("spiral gears"). We
use one parameter:
```
ω_race = r · ṙ_b        r [rad/m]                                    (4.1)
```
For a screw of lead L with a step-up N, r = 2πN/L (the gate-twin baseline
1 in lead × 6 gives r = 1484 rad/m). r is swept (experiment 004).

### 4.2 Sprag pair as an exact one-way constraint
Two races: A turns +r·ṙ_b (collapse stroke), B turns −r·ṙ_b (expansion
stroke). Each sprag locks when its race tries to overrun the rotor in the
driving sense and freewheels otherwise. Modelled **event-driven as an exact
kinematic constraint** (not a stiff penalty — see `LAB_NOTEBOOK.md`
2026-07-02 for why), with modes FREE / ENG_A / ENG_B (/ SLIP_A / SLIP_B).

- **Engage event** (counted, Q5): s·r·ṙ_b − ω crosses zero upward, where
  s = +1 (A) or −1 (B). With zero backlash the race and rotor speeds are
  equal at that instant and engagement is impact-free.
- **Backlash θ_bl**: after a disengagement the relative angle between race
  and rotor must advance θ_bl before the sprag can lock. By the time it
  locks the race is generally faster than the rotor by Δω. Engagement is
  then an inelastic impact between the rotor J and the stroke DOF through
  the ratio r (§4.4). The lost energy is booked as `E_clutch` and the impact
  torque impulse Λ is recorded — it is the engagement-shock load Formsprag
  needs.
- **Engaged**: constraint ω = s·r·ṙ_b. Lagrange with kinetic energy
  ½J ω² = ½ J r² (ż_s − ż_f)² gives a reflected inertance
  ```
  J_r = J r²                                                       (4.2)
  ```
  on the stroke DOF and the coupled mass matrix
  ```
  [ m_s + J_r     −J_r   ] [z̈_s]   [ −F_b′ − F_d[full] − s r T_r              ]
  [  −J_r      m_f + J_r ] [z̈_f] = [  F_b′ − F_m − F_d[main] + s r T_r      ]    (4.3)
  ```
  where F_b′ is the passive frame force (spring, friction, stops) and
  T_r = T_gen(ω) + c_w ω is the torque resisting the rotor. Then
  ω̇ = s r (z̈_s − z̈_f) and the torque transmitted by the engaged sprag is
  ```
  T_c = J ω̇ + T_r                                                   (4.4)
  ```
  J_r is large for realistic parameters (J = 3×10⁻⁴ kg m², r = 1484 → J_r =
  660 kg). The Gate is therefore an **inerter** in the sense of Smith (2002)
  whenever a clutch is engaged, which is exactly the behaviour measured for
  MMR devices (Li et al. 2013). This is physics, not an artefact, and the
  flywheel sweep (experiment 006) exposes it.
- **Disengage event**: T_c crosses zero downward (a sprag cannot pull).
  Grazing engagements (T_c < 0 immediately) are rejected with a micro-step;
  a Zeno counter guards against chatter.
- **Torque capacity T_cap** (optional): if T_c exceeds T_cap the clutch
  slips at Coulomb torque T_cap·sign(ω_race − ω) until the relative speed
  returns to zero (SLIP modes). Slip work is booked as `E_clutch`. Default
  T_cap = ∞; the number of exceedances per km is a sizing output.
- **Overrunning drag**: T_od,i = c_od (ω_i − ω) on each freewheeling race,
  with its axial reaction on the stroke, F = r (T_A − T_B), applied to the
  stroke DOF so action–reaction is exact. Catalog drag is roughly constant
  (0.05–0.5 N·m); the viscous form is a solver-friendly equivalent sized at
  the operating slip (`09_open_parameters.md`).
- **Centrifugal lift-off**: a design check only. Race speed r·|ṙ_b| is
  reported in rpm against `sprag_liftoff_rpm`.

Full-wave rectification is therefore not assumed: both clutches must be
observed engaging and the rotor must never be driven negative (test
`test_gate_single_dof.py::test_full_wave`).

### 4.3 Rotor and generator
```
J ω̇ = T_c − T_gen(ω) − c_w ω        (engaged)
J ω̇ = T_A + T_B − T_gen(ω) − c_w ω  (free, T_i = overrun drag)
```
Generator models (all satisfy T_gen·ω = P_elec + P_loss exactly):

1. **Linear load** (brief's starting point): T_gen = c_gen ω, P_elec =
   η c_gen ω², P_loss = (1−η) c_gen ω².
2. **PM machine on a resistive load**: e = k_e ω, i = e/(R_i + R_L),
   T = k_e i. This *is* model 1 with c_gen = k_e²/(R_i+R_L) and
   η = R_L/(R_i+R_L); kept because R_L is the physical knob (Q4).
3. **Claw-pole alternator** (measured 14 V curve, cut-in 1600 rpm,
   η≈0.52): kept to quantify why a Lundell machine is a poor fit.

Mechanical power into the generator path, P_gate = T_c ω while engaged, is
the quantity a bench torque transducer sees.

### 4.4 Impact at engagement with backlash
At the lock instant the race leads the rotor by Δω = s r ṙ_b − ω > 0. The
clutch applies a torque impulse Λ to the rotor and a force impulse s r Λ to
the stroke:
```
J (ω⁺ − ω⁻) = Λ ,  m_s (ż_s⁺ − ż_s⁻) = −s r Λ ,  m_f (ż_f⁺ − ż_f⁻) = +s r Λ
with ω⁺ = s r (ż_s⁺ − ż_f⁺)
⇒ Λ = Δω / ( 1/J + r² (1/m_s + 1/m_f) )                                (4.5)
```
Energy lost = ½Δω²/(1/J + r²(1/m_s + 1/m_f)) ≥ 0, booked in `E_clutch`.
Zero backlash ⇒ Δω = 0 ⇒ Λ = 0 (impact-free), recovering the gate-twin
behaviour.

---

## 5. Road input

ISO 8608:2016 one-sided displacement PSD in spatial frequency n [cycles/m]:
```
G_d(n) = G_d(n_0) (n/n_0)^−2 ,   n_0 = 0.1 cycles/m
G_d(n_0) class centres: A 16, B 64, C 256, D 1024, E 4096  (×10⁻⁶ m³)
```
Traversed at speed V, temporal frequency f = nV and
```
S_d(f) = G_d(f/V)/V = G_d(n_0) n_0² V / f²
S_v(f) = (2πf)² S_d(f) = 4π² G_d(n_0) n_0² V  ≡ W_v   (white, one-sided)  (5.1)
```
Ground **velocity** is white. Synthesis: sum of N cosines with random phases
on a linear n-grid, amplitude √(2 G_d(n_i) Δn), band 0.011–2.83 cycles/m
(ISO 8608 reporting band), raised-cosine start ramp so the ledger starts
quiescent, z and ż from one cubic spline. Verified against (5.1) in
`tests/test_roads.py`. Deterministic inputs (sine, step, half-sine bump,
raised-cosine) are provided for hand checks.

Power delivered by the road to the corner:
```
P_road = F_t ż_r = k_t (z_r − z_u) ż_r   (+ c_t ṙ_t ż_r if tire damping)   (5.2)
```

---

## 6. Energy ledger (hard gate on every run)

All work and loss integrals are ODE states, so closure is limited only by
solver tolerance:
```
E_road = E_elec + E_genloss + E_damper + E_friction + E_stop + E_clutch + ΔE_storage
E_storage = ½m_s ż_s² + ½m_f ż_f² + ½m_u ż_u² + ½J ω²
          + ½k_b r_b² + ½k_m r_m² + ½k_t r_t² + ½k_stop pen²
```
`closure = |residual| / max(|E_road|, Σ dissipations + |ΔE_storage|)` must be
< 1% (typical 10⁻⁵). A run that fails raises; it is never silently reported.
When mass is added to the vehicle, the propulsion penalty ΔP_mass (§9) is a
*separate* term computed from the drive cycle, not a term of this ledger
(the ledger is the vertical dynamics only).

---

## 7. The road-power theorem: what any corner device can and cannot do

This section is the physics behind `08_findings_that_change_the_story.md`
entry 1. Zuo & Zhang (2013) obtained the linear case via the H₂ norm and
reported "insensitivity" to suspension parameters; the statement below is
exact, holds for nonlinear corners, and its consequence for the AKS
narrative has not previously been drawn.

**Theorem.** Let the tire be a point-contact spring of rate k_t with no
damping, and let everything above it (springs, dampers, the Gate, stops,
clutches — linear or not) be a causal system with finite masses, so that
nothing above the contact patch responds *instantaneously* to ground
velocity. Drive the corner with ground velocity ż_r that is white, of
one-sided level W_v (eq. 5.1), over the band in which the corner responds.
Then the mean power the road delivers is

```
P̄_road = E[F_t ż_r] = ¼ k_t W_v = π² G_d(n_0) n_0² V k_t                 (7.1)
```

independent of every parameter above the tire.

**Proof.** F_t = k_t (z_r − z_u), so P̄_road = k_t E[z_r ż_r] − k_t E[z_u ż_r].
For a Wiener-type z_r (white velocity), ½ d/dt E[z_r²] = W_v/4, so the first
term is k_t W_v/4. In the second term z_u(t) is a non-anticipating functional
of the velocity history up to t with no instantaneous component (its response
to a velocity impulse starts from zero because m_u is finite), so it is
uncorrelated with the white increment at t: E[z_u ż_r] = 0. ∎
(For the band-limited stationary synthesis used in the code the two terms
are redistributed — E[z_r ż_r] = 0 for any stationary process — but their
sum is unchanged to the extent the band covers the corner's response; the
Lyapunov/H₂ evaluation in `validate/analytic.py` returns ¼ k_t W_v to
machine precision for arbitrary m_s, m_u, k_m, c_s, and the time-domain
simulations, passive and with the Gate, reproduce it to within the
realisation scatter — `tests/test_analytic_limits.py`.)

**Numbers.** Mid-size car (k_t = 180 kN/m), 60 mph: class A 7.6 W, B 30 W,
C 122 W, D 488 W per corner; ×4 gives 30 / 122 / 488 / 1952 W per car. Zuo &
Zhang's 100–400 W for "good to average" roads is the B–C band of this table.
Everything else — vehicle weight, spring rates, damping, the Gate — changes
*what happens to* these watts, not how many there are.

Consequences:

1. **The dissipator does not set the pie.** Damper, generator, or any
   mix: the mean power supplied is fixed; what changes is how large the
   motion must be to dissipate it. A generator that takes over the damper's
   dissipation harvests the damper's watts. It does not uncover a reservoir
   the damper had been missing.
2. **Vehicle weight enters only through the tire.** Heavier vehicles run
   stiffer tires (and more of them), so a loaded Class 8 wheel station on
   duals (k_t ≈ 1.8 MN/m) sees 10× the power of a car corner on the same
   road at the same speed — not because of its weight but because of its
   tire stiffness. "P ∝ W" is not a law of this system; "P ∝ G_d V k_t" is.
3. **Road class and speed are the levers.** One ISO class is a factor of
   four; doubling speed doubles the power.
4. **Tire damping and enveloping** (not in the theorem) are the only places
   where the device upstream could change the mean input, and they act to
   *reduce* it at high frequency. The model exposes c_t as a parameter.

**Reactive power is not harvestable.** The instantaneous spring power
k_m r_m ṙ_m has a large amplitude (of order the dissipated power divided by
2ζ, a few times larger at ζ ≈ 0.3) and a mean of exactly zero. The AKS
pitch-deck comparison "the spring handles several times the damper's flow"
is a true statement about reactive power and an irrelevant one about
harvest. `metrics.energy` reports `P_spring_cycle` beside `P_road` so the
distinction is visible in every table.

**What the Gate *can* do** (and what the experiments test): (a) convert the
dissipated share from heat to electricity with efficiency η_chain; (b) move
dissipation from the damper to the generator by changing the impedance the
road sees, which changes ride and tire-load metrics (Q3); (c) lose some of
it to clutch, friction, stop and generator losses; (d) add mass (Q2). The
ceiling on P_elec per corner is therefore η_chain · ¼ k_t W_v minus the
damper's residual share, and the design problem is impedance matching
against that fixed supply.

## 8. Definitions (normative; also in `02_definitions.md`)

```
φ   = P_elec / P_road                 extraction fraction of road input power
φ_s = P_elec / P_spring,cycle          electrical output per unit of elastic energy
                                       cycled through the main spring:
                                       P_spring,cycle = mean(|k_m r_m ṙ_m|)
                                       (mean absolute reactive power; a
                                       diagnostic, not a ceiling)
η_mech = P_gate / P_frame              mechanical efficiency of the Gate:
                                       power into the generator path over
                                       power into the frame stage
η_chain = P_elec / P_gate              generator + electrical efficiency
P_net = P_elec − P_friction − ΔP_mass − ΔP_ride   per corner (§9)
```
All are time averages over the stationary part of a run (start ramp
excluded), reported with the road class, speed, vehicle, generator load and
seed, and with a bootstrap 90% interval over seeds.

---

## 9. Net-benefit terms

- **P_friction**: Gate-internal losses that would not exist on the passive
  corner: `E_friction/T` (guide friction c_b), overrun drag and clutch
  impact/slip (`E_clutch/T`), windage c_w ω², and generator loss. Reported
  individually.
- **ΔP_mass**: added mass Δm per corner costs propulsion power through
  rolling resistance and grade only (aerodynamics is mass-independent):
  ΔP_mass = Δm g (C_rr + sin θ) V  (+ Δm a V on an acceleration cycle). At
  C_rr = 0.01, V = 26.8 m/s, Δm = 12 kg: 31 W. Δm is OPEN (housing and
  generator mass unknown) and is swept.
- **ΔP_ride**: the ride change is reported as a metric (Q3), not converted
  to watts; the brief's `ΔP_ride_penalty` is left as an explicit placeholder
  with sign, `TODO(bench)`, because no defensible exchange rate exists.

---

## 10. Ride and handling metrics (Q3)

- Sprung-mass acceleration RMS, raw and ISO 2631-1 W_k-weighted (W_k
  realised per the standard's transfer functions: band-limit f₁ = 0.4 Hz,
  f₂ = 100 Hz; a-v transition f₃ = f₄ = 12.5 Hz, Q₄ = 0.63; upward step
  f₅ = 2.37 Hz, Q₅ = 0.91, f₆ = 3.35 Hz, Q₆ = 0.91; implemented in the
  frequency domain and checked against the tabulated weights at 1, 4, 8,
  16 Hz).
- Suspension working space: RMS of (z_s − z_u), plus frame stroke RMS and
  the fraction of time on a stop.
- Dynamic tire load variation: RMS of F_t divided by static load; fraction
  of time with F_t < 0 (lift-off).
- All deltas are Gate minus passive baseline at equal total mass and equal
  static height, same road realisation (same seed).

---

## 11. Single-stroke hand derivation (test anchor for the Gate element)

Prescribed frame stroke r_b(t) = a sin(2πf t), ratio r, linear generator
c_gen, J → 0 (so the rotor follows the race), no losses. While clutch A is
engaged (ṙ_b > 0): ω = r ṙ_b, P_gate = c_gen ω² = c_gen r² ṙ_b². While B is
engaged (ṙ_b < 0): identical. Hence the rotor is driven on both half-strokes
and the mean mechanical power is
```
P̄ = c_gen r² ⟨ṙ_b²⟩ = ½ c_gen r² (2πf a)²                                 (11.1)
```
and the loop area per cycle is P̄/f. With J > 0 the rotor coasts above the
race near each reversal and the clutches freewheel; P̄ falls below (11.1)
and the fraction of the cycle engaged is a reported quantity. The test
`test_gate_single_dof.py::test_hand_derivation` checks (11.1) to 0.5% with
J = 10⁻⁹ and checks that P̄(J) ≤ P̄(0) monotonically.

Worked number (bench articles, Diligence Response conditions): a = 0.0127 m
(±0.5 in), f = 2.5 Hz, so ⟨ṙ_b²⟩ = ½(2π·2.5·0.0127)² = 0.0199 m²/s². With
r = 1484 rad/m and c_gen = 2.5×10⁻⁶ N·m·s/rad (the gate-twin PM baseline,
k_e = 0.05, R_i + R_L = 1.4 Ω → c_gen = 1.79×10⁻³ … *see note*), P̄ =
c_gen r² ⟨ṙ_b²⟩. The Diligence Response's 1.7–5.2 W is reproduced only for
a specific c_gen; the bench protocol (§05) states the c_gen that would give
it and treats the load as the thing to be measured.

---

## 12. Known limitations (kept current)

- Quarter car only; pitch/roll coupling and four-corner totals are 4× a
  corner ± nothing. Half-car is on the list.
- Ideal sprag constraint with lumped backlash; sprag compliance neglected.
- Viscous guide friction and overrun drag.
- Tire as point-contact spring; no enveloping.
- Quasi-static alternator map; PM model linear.
- Static-load-dependent bias-spring preload handled by choosing x_c, x_e; no
  spring nonlinearity near solid height.

## 13. References

- Zuo, L., Zhang, P.-S. (2013). Energy harvesting, ride comfort, and road
  handling of regenerative vehicle suspensions. *J. Vib. Acoust.* 135(1)
  011002.
- Li, Z., Zuo, L., Kuang, J., Luhrs, G. (2013). Energy-harvesting shock
  absorber with a mechanical motion rectifier. *Smart Mater. Struct.* 22
  025008.
- Smith, M. C. (2002). Synthesis of mechanical networks: the inerter. *IEEE
  Trans. Autom. Control* 47(10).
- ISO 8608:2016; ISO 2631-1:1997.
- Karnopp, D. (1989). Permanent magnet linear motors used as variable
  mechanical dampers for vehicle suspensions. *Veh. Syst. Dyn.* 18.
- US 12,409,695 B2.
