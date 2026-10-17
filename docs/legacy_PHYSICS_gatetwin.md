# gate-twin PHYSICS

Digital twin of the **Armstrong Gate** (U.S. Patent 12,409,695 B2, granted
2025-09-09): a mechanical full-wave rectifier harvesting energy from the
suspension **spring** stroke. This document is the authoritative derivation;
`src/gatetwin/` implements exactly this and nothing more.

**IP guardrail:** only the granted-patent mechanism is modelled. No unfiled
concepts appear anywhere in this repo.

---

## 1. The machine (per granted claims)

- A vertically collapsible **3-plate frame** between chassis and suspension.
- A **frame biasing spring** with rate `k_b` strictly **lower** than the main
  suspension spring `k_s` (Claims 2/11 — the core novelty). Being the soft
  element of a series stack, it takes the *first* 2–5 in of every stroke and
  routes that motion into the generator path before the main spring
  appreciably deflects (**soft-first series architecture**).
- A **drive shaft** fixed to the top plate plunges through **two opposed
  sprag (one-way) clutches** with opposite-hand screw engagement: compression
  drives one clutch, rebound the other, and **both spin the hollow generator
  shaft in the same direction** — mechanical **full-wave rectification**.
- **Fly weights (flywheel)** carry rotation through stroke reversals — the
  smoothing capacitor of the rectifier analogy.
- A **generator/alternator** converts the smoothed one-way rotation to
  electricity. Screw lead ≈ 1 in/rev, internal step-up ≈ 5–8:1 (design
  variables).

## 2. Topology, coordinates, sign conventions

All coordinates are perturbations about static equilibrium, positive up;
gravity therefore cancels against spring preloads and does not appear.
(Consequence to remember: frame travel limits are placed symmetrically about
the *loaded* equilibrium; asymmetric preload can be added later by offsetting
`x_b_max`.)

```
   m_s  (z_s)        sprung mass
    |
    |  FRAME STAGE: k_b, c_b, hard stops, screw+sprags+generator
    |                stroke r_b = z_s − z_f
   m_f  (z_f)        frame middle-plate / drive-shaft mass
    |
    |  MAIN STAGE:  k_s, c_s          r_m = z_f − z_u
   m_u  (z_u)        unsprung mass
    |
    |  TIRE:        k_t               r_t = z_u − z_r
   z_r(t)            road elevation
```

Newton (freewheel mode):

```
m_s z̈_s = −F_b
m_f z̈_f =  F_b − F_m
m_u z̈_u =  F_m − F_t
```

with `F_b = k_b r_b + c_b ṙ_b + F_stop(r_b, ṙ_b) + F_screw`,
`F_m = k_s r_m + c_s ṙ_m`, `F_t = k_t r_t`.

Because `k_b < k_s`, low-amplitude motion deflects the frame stage first —
the patent's soft-first behavior emerges from the series stack; it is not
imposed.

**Hard stops** at `|r_b| = x_b_max`: one-sided Kelvin–Voigt,
`F_stop = clip(k_stop·pen + c_stop·ṙ_b)` (push-only). Stored part
`½k_stop·pen²`; the remainder of `F_stop·ṙ_b` is booked as stop loss, keeping
the ledger exact even under force clipping.

## 3. Rectifier kinematics and the sprag pair

Screw: `ω_screw = (2π/lead)·ṙ_b`. Step-up `N` puts the equivalent race speed
at the generator shaft:

```
ω_A = +Gt·ṙ_b ,   ω_B = −Gt·ṙ_b ,   Gt = 2π·n_step/lead   [rad/s per m/s]
```

Baseline `Gt = 2π·6/0.0254 ≈ 1484`.

Each sprag is an ideal one-way clutch, handled **event-driven** with exact
kinematic constraints (chosen over penalty coupling — see LAB_NOTEBOOK entry
2026-07-02 — because it keeps the energy ledger exact and avoids ~kHz
penalty modes):

- **Engage** (solver event, counted for durability): `ω_i − ω` crosses zero
  upward, with hysteresis `eps_engage = 1e-6 rad/s`. At that instant race and
  rotor speeds are equal, so engagement is impact-free.
- **Engaged**: constraint `ω = ±Gt·ṙ_b`. The rotor inertia reflects onto the
  stroke DOF as an **inertance** `Jr = J·Gt²` (baseline ≈ 660 kg — large and
  *physical*; the same effect dominates published MMR devices, cf. Li & Zuo
  2013). Lagrange with `KE = … + ½Jr(v_s−v_f)²` gives the coupled mass matrix

  ```
  [ m_s+Jr   −Jr  ] [a_s]   [ −F_b'  − s·Gt·T_r ]
  [ −Jr    m_f+Jr ] [a_f] = [  F_b' − F_m + s·Gt·T_r ]
  ```

  where `F_b'` is the passive frame force (no screw), `T_r = T_gen + c_w·ω`,
  `s = +1` (clutch A) or `−1` (clutch B). Then `ω̇ = s·Gt·(a_s − a_f)` and the
  transmitted torque is `T_c = J·ω̇ + T_r`.
- **Disengage** (solver event): `T_c` crosses zero downward — a sprag cannot
  pull. Grazing engagements (`T_c < 0` immediately) are rejected with a
  micro-step guard; a Zeno counter aborts pathological chattering.
- **Overrunning**: small viscous drag `T_od = c_od·(ω_i − ω)` on each
  freewheeling sprag, with its axial reaction `F_screw = Gt·(T_A − T_B)`
  applied to the stroke so action–reaction (and the ledger) stay exact.
- **Centrifugal lift-off** (design check, not dynamics): sprag catalogs put
  lift-off at 800–1500 rpm on the race. `SimResult.screw_rpm` reports the
  race speed; predictions must flag margins against `sprag_liftoff_rpm`.

Only one clutch can be engaged at a time (ω ≥ 0 in operation and
ω_A = −ω_B). Both half-strokes torque the rotor in the **same** direction —
full-wave rectification is verified, not assumed (test V1d).

## 4. Flywheel + generator

Rotor: `J·ω̇ = T_clutch − T_gen − c_w·ω` (freewheel: clutch drag replaces
`T_clutch`).

Two machine models (`generator.py`), both satisfying
`T_gen·ω = P_elec + P_loss` **exactly** so the audit can close:

1. **PM generator**: EMF `e = k_e ω`, `i = e/(R_int+R_load)`,
   `T = k_e i`, `P_elec = i²R_load`, `P_loss = i²R_int`. Peak conversion
   efficiency `R_load/(R_load+R_int)` ≈ 85–90% at design point; `R_load` is
   the impedance-matching knob.
2. **Claw-pole alternator** (measured curve at 14 V): cut-in 1600 rpm,
   current {1600:77, 2000:100, 2500:117, 3500:138, 6000:152} A,
   η ≈ 0.52. `T = P_elec/(η·ω)`. Cut-in smoothed over ~30 rpm for the
   solver.

## 5. Road inputs

ISO 8608:2016 one-sided displacement PSD `Gd(n) = Gd0·(n/n0)⁻²`,
`n0 = 0.1 cycles/m`, class centers A=16, B=64, C=256, D=1024, E=4096
(×10⁻⁶ m³). Synthesis: 1024 cosines, random phases, band 0.011–2.83
cycles/m, traversed at vehicle speed `v`; raised-cosine startup ramp so the
audit starts quiescent; `z` and `ż` from one cubic spline for a
self-consistent road-power integral. Verified against the target PSD in
`tests/test_roads.py`. (Planned: FHWA LTPP measured-profile ingest.)

Road power into the system: `P_in = −F_t·ż_r = k_t(z_r − z_u)·ż_r`.

## 6. Energy ledger (hard gate on every run)

Carried as ODE states, so closure is limited only by solver tolerance:

```
E_road_in = E_elec + E_genloss + E_damper + E_stop + E_clutch + Δ(storage)
storage   = ½m_s v_s² + ½m_f v_f² + ½m_u v_u² + ½Jω²
          + ½k_b r_b² + ½k_s r_m² + ½k_t r_t² + ½k_stop pen²
```

`SimResult.energy_audit()` returns all terms and `closure` (relative
residual). **Every** simulation must close < 1% (V1e); typical closure is
solver-tolerance level (≪0.1%). A twin that doesn't conserve energy is
worthless.

## 7. Validation gates

| Gate | Statement | Test |
|------|-----------|------|
| V1a | Locked clutch reproduces exact kinematic ratio `ω = Gt·ṙ_b` | `TestV1aKinematicRatio` |
| V1b | No-input spin-down = `ω₀·exp(−c_w t/J)` to 1e-6 | `TestV1bSpinDown` |
| V1c | Pure spring (rectifier disconnected): F–x loop area = 0 | `TestV1cZeroArea` |
| V1d | Rectified: loop area > 0 = harvested energy; ω never negative; both clutches engage | `TestV1dRectifiedArea` |
| V1e | Full system on ISO C road: audit closes < 1% | `TestV1eFullSystemAudit` |
| V2 | Zuo MMR anchor: ≈40 W @ 0.047 m/s RMS, >60% mech. eff. (±25%) | planned |
| V3 | Audi eROT anchor (parallel damper): 3 / 100–150 / ~613 W (±30%) | planned |
| V4 | κ backs out ≈0.10 (parallel) vs ≈0.18–0.20 (rectifier) | planned |

Predictions (per-vehicle power tables, sensitivities, durability, generator
operating maps, bench pre-registration) are **gated behind V1–V4**.

## 8. Known limitations (candid list, kept current)

- Quarter-car only so far; half-car with pitch coupling is planned for the
  per-vehicle tables.
- Sprag compliance and backlash neglected (ideal constraint); engagement is
  impact-free by construction, so engagement-shock durability loads are
  underpredicted — cycle *counts* are still exact.
- Overrun drag is a viscous equivalent of a roughly constant catalog torque.
- Alternator model is quasi-static (measured curve), no field-lag dynamics.
- Frame guides modelled as viscous `c_b`; real friction is partly Coulomb.
- Tire modelled as point-contact spring, no damping, no enveloping.
- Reflected inertance `Jr = J·Gt²` with baseline parameters is ~660 kg;
  whether real Gate hardware targets this regime is a design question the
  sensitivity study must expose, not hide.

## 9. Parameter provenance

Every value in `params/params.yaml` carries `{value, units, provenance}` with
tags [PATENT]/[MEASURED]/[LITERATURE]/[ASSUMPTION]; enforced by
`tests/test_params.py`. Assumption-tagged parameters must appear in the
sensitivity study and never carry a validation gate.
