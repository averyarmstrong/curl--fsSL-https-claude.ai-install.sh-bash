# 03 — Breaking the spring's symmetry: the Gate from first principles

Written 2026-10-17 after reading the drawings (FIG. 8 markup, the two hand
sketches, the Fusion two-stage collapse animation, "One iteration" render).
This document starts from nothing but Newton and the drawings and derives
what the one-way clutches do to a spring. It is the normative statement of
*why* the Gate produces power and *where that power comes from*. Nothing in
it depends on quarter-car theory; `01_physics.md` §7 is reached at the end
as a consequence, not assumed.

Tags: every number below is `modeled` (reproduced by
`tests/test_symmetry_breaking.py`) or `measured` (Ebsco spring sheet).

---

## 1. What the drawings establish (and do not)

| Feature | Seen in | What it fixes |
|---|---|---|
| Upper frame: three square plates on four posts, bias stage (red) between the plates; the animation shows the stage collapsing in two steps (top plate to middle plate, then the lower red stage) | sketches 1–2, Fusion GIF, "One iteration" | Topology of claim 1: plates 109/110/111, posts 112/113, spring 115. Two bias stages in series in the current Fusion iteration. |
| Generator / flywheel body (sphere) hanging from the lowest frame plate; drive rod passes through it and down the axis of the main coil spring to the base plate | Fusion GIF, "One iteration", FIG. 8 markup | The generator rides on the main-spring seat; the rod is anchored to the chassis. Relative motion between them is the **bias-stage deflection** `x_b`, nothing else. |
| Sprag clutches at both ends of the generator body, flyweight cross-bars outboard of each sprag | sketch 2 inset, FIG. 8 (103/104/105/107) | Full-wave rectification about the generator; flyweights on the generator shaft, not on the rod. |
| Hand labels "bias spring", "coil spring", "CAR Axle" on FIG. 8 | `3 drawings copy.pdf` p. 3 | Confirms the series stack: chassis → bias spring → frame → main spring → axle. |
| Dimensions | none of the files | Nothing. Plate size, post length, rod diameter, sphere diameter, spring counts are all **open** (`09_open_parameters.md`). |

So the mechanism is exactly the one modeled in `elements/gate.py`: a
generator that sees `|ẋ_b|·r` whenever a sprag is engaged, mounted across
the soft stage of a two-spring series stack. The drawings add no new
element and no number. They do settle one thing that was ambiguous in the
text: the rod is driven by the *bias stage*, so the harvested stroke is
`x_b`, not the full suspension deflection.

---

## 2. The symmetry of a spring, stated precisely

A spring is a conservative element: its force depends on position only,
`F = -dU/dx`. Over any closed path in `x` the work is zero,

    ∮ F dx = 0.                                                   (2.1)

Equivalently the force–deflection curve is retraced on compression and
extension: the loop in the `(x, F)` plane has **zero area**. That is the
"symmetry" in question. It is a symmetry under time reversal: run the
film backwards and a spring behaves identically. Whatever energy the body
puts into the spring on the down-stroke (`½ k x²`) the spring hands back
on the up-stroke, with sign reversed and nothing lost.

Two consequences follow immediately and must be carried in the head:

1. A spring **stores** energy, it does not **supply** energy. The static
   partition between the two springs of the stack (89.3 % of the series
   deflection lives in the bias stage for the Ebsco 8.35:1 pair,
   `01_physics.md` §2) is a statement about storage, not about watts.
2. A spring plus any other conservative element (a mass, a flywheel on a
   rigid shaft, a second spring) is still conservative. Zero loop area.
   No arrangement of springs, masses and rigid links can produce net work.

The test `test_pure_spring_zero_loop_area` holds the Gate element to (2.1)
with the clutches forced open: the actuator's net work over five cycles is
below 1e-6 of the stored energy.

---

## 3. What the sprags break

A one-way clutch is a **kinematic inequality constraint**. For sprag A on
the rod,

    ω ≥  r ẋ_b   (A can only drive the rotor up to the race speed),
    ω ≥ -r ẋ_b   (B, mounted opposed).                               (3.1)

When a sprag is engaged the rotor speed is pinned to the race speed,
`ω = ±r ẋ_b`; when the rotor is faster than both races it freewheels.
The rotor speed is therefore

    ω = r |ẋ_b|   whenever the rotor is not coasting.                (3.2)

Equation (3.2) is the whole invention in one line. The map
`ẋ_b → |ẋ_b|` is **not invariant under time reversal**: reverse the film
and the rod runs the other way but the rotor still spins the same way.
The sprag pair takes a motion that is symmetric (up and down) and feeds
the generator a motion that is one-signed. That is what "breaking the
spring's symmetry" means mechanically. The spring itself is untouched; it
is the *path* of the motion through the clutch that loses its symmetry.

A generator on that rotor exerts a torque `T = c_gen ω` opposing `ω`. Pull
it back to the rod through the engaged sprag and the rod feels

    F_gen = r T = c_gen r² |ẋ_b| · sign(ẋ_b) = c_eq ẋ_b,   c_eq ≡ c_gen r².   (3.3)

The force always opposes the rod's velocity, on **both** strokes. The
`(x_b, F)` loop is no longer retraced; it encloses an area. For a
sinusoidal stroke `x_b = A sin ωt` the area is

    W_cycle = ∮ F_gen dx_b = π c_eq ω A²,                           (3.4)

and the power is `P = f · W_cycle = ½ c_eq ω² A²`. That is the hand
derivation already anchored in `01_physics.md` §11; here it is derived
from the symmetry argument rather than assumed.

Adding the flywheel (`J > 0`) does not change the sign structure. With
inertia the rod force while engaged is

    F = r (J ω̇ + c_gen ω) = J r² ẍ_b + c_eq ẋ_b,                       (3.5)

so the rotor adds a reflected mass `J r²` on the rod and, near the stroke
reversals where `|ẋ_b|` drops below `ω/r`, the sprag releases and the rotor
coasts. During coasting the generator keeps drawing from the flywheel; the
flywheel gives it back only what the rod put in while engaged. The
flywheel smooths the *delivery*, it does not add to the *supply*.

---

## 4. Where the energy comes from

Write Newton for the stack with a massless frame plate (frame mass
`m_f` is carried in the full model; it only adds a `m_f ẍ` term). Force
continuity across the frame plate gives

    k_m x_m  =  k_b x_b + F_gen(ẋ_b, ...).                          (4.1)

Multiply by `ẋ_b` and integrate over a cycle. The left side is the work
done *on the bias stage by the main spring*; the `k_b x_b ẋ_b` term
integrates to zero by (2.1). What remains:

    ∮ k_m x_m dx_b  =  ∮ F_gen dx_b  =  W_cycle  > 0.                (4.2)

So every joule the generator takes out per cycle is a joule of work done
*through* the main spring on the bias stage, which in turn is work done
on the main spring by the relative motion of axle and chassis. Trace it
one step further and the chassis–axle relative motion is driven by the
road through the tire (plus any body force on the chassis). There is no
other term in (4.1). The springs appear only inside closed integrals.

This is the honest content of "we break the spring's symmetry":

- **Without the Gate** the body pushes energy into the stack on the
  down-stroke and the stack pushes all of it back on the up-stroke.
- **With the Gate** the stack pushes back *less* than it received; the
  difference is `W_cycle` and it went into the generator. The body therefore
  comes up with less energy than it went down with. Energetically that is a
  damper's signature, whatever the hardware is called, and it is why the
  Gate is a ride element as well as a generator (exp 001–007).

The source is the rod being pushed. Rectification decides how much of what
is pushed is kept; it does not add to what is pushed. That statement is
tested: in every run of this repo the ledger closes with
`E_road + E_body = E_elec + losses + ΔE_stored` to better than 1 % (3,290
cases, 0 errors), and the bench harness closes it to 1e-10.

---

## 5. The toy, derived

The push-down spinning top is the same machine with a human hand for a
road:

| Toy | Gate |
|---|---|
| hand pushing the knob | main spring pushing the frame plate (ultimately the axle through the tire) |
| return spring under the knob | bias spring |
| helical shaft + one-way pawl | sprag A (one direction) |
| the top's mass | flywheel `J` and generator |
| the top slowing down | `c_gen` (electrical load) + `c_w` (bearing drag) |

In the toy only the down-stroke drives; the return spring re-extends the
knob and does work on the *hand*, not on the top. The Gate's second,
opposed sprag harvests that return stroke too. But the return stroke can
only return what the down-stroke stored in the bias spring, and that
stored energy came from the hand. Full-wave rectification is worth at most
a factor of two in **capture**, never a new source. Any child who has
played with the toy knows the top stops when they stop pushing.

---

## 6. Worked single cycle with the bench springs (`measured` rates)

Ebsco EB-7234 (bias) 1.905 lbf/in = 333.6 N/m; EB-7233 (main)
15.902 lbf/in = 2,785 N/m. Stroke 1 in (25.4 mm) amplitude at 3 Hz,
reflected damping `c_eq = c_gen r²`, rotor inertia negligible unless stated.

| Quantity | c_eq = 0 (spring alone) | c_eq = 100 N·s/m | c_eq = 500 N·s/m |
|---|---|---|---|
| Energy stored in the bias spring at full stroke, ½ k_b A² | 0.108 J | 0.108 J | 0.108 J |
| Net actuator work per cycle (loop area) | 0 J (< 1e-7 J numerically) | 3.82 J | 19.1 J |
| Mean power into the generator | 0 W | 11.5 W | 57.3 W |
| Peak rod force from the generator, c_eq ω A | 0 N | 48 N | 239 N |
| Ledger closure (bench harness) | — | 6e-10 | 7e-11 |

Add a flywheel giving `J r² = 10 kg` to the 500 N·s/m case: 57.5 W
(the rotor coasts at 15–140 rad/s, never stops), unchanged to 0.4 %. The
flywheel smooths the shaft speed; the watts are the loop area.

Read the table the way the mission asks. The spring's energy per cycle
(0.108 J) is **two orders of magnitude below** the harvested energy per
cycle (19.1 J) and the spring never delivers it anyway. The 19.1 J is
supplied, every cycle, by whatever pushes the rod with a 239 N peak force
through 2 inches peak-to-peak at 3 Hz. On a bench that is the actuator. On
a vehicle it is the main spring's force fluctuation, which is the road's.

---

## 7. What a 1 kW generator needs the rod to do (apparatus-first)

From (3.4): `P = ½ c_eq (2πf)² A²`. Solve for the peak rod force
`F = c_eq (2πf) A` that must be present:

    F_peak = 2 P / (2π f A).                                        (7.1)

| Stroke amplitude A | 1 kW at 1 Hz | 1 kW at 3 Hz | 1 kW at 10 Hz |
|---|---|---|---|
| 0.5 in (12.7 mm) | 25,100 N | 8,400 N | 2,500 N |
| 1 in (25.4 mm) | 12,500 N | 4,200 N | 1,250 N |
| 2 in (50.8 mm) | 6,300 N | 2,100 N | 630 N |
| 5 in (127 mm) | 2,500 N | 840 N | 250 N |

A mid-size-car corner carries 4,300 N static. The dynamic spring force on
ISO C at 60 mph has an RMS of roughly a tenth of that. The force in (7.1)
is what must be *continuously* available across the bias stage, in phase
with its velocity. The springs do not supply it; the road does, at the
rates in `06_numbers_ledger.md` (122 W per corner on ISO C, 488 W on
ISO D, mid-size car). A 1 kW shaft figure on a passenger car is therefore a
`target` that the per-corner supply does not meet on paved roads; on a
loaded Class 8 station (1,220 W per dual station on ISO C) or any vehicle on
ISO D–E it is within the supply and the constraint moves to tire-load
variation and ride (F5, F7).

---

## 8. What is genuinely new, and what is not

**New, and modeled nowhere else we have found:** a generator placed across
the *soft stage of a two-spring series stack*, loaded through a full-wave
sprag rectifier with flywheel, with the stage bounded by coil bind and a
retainer. Its dynamics are a hybrid system (modes FREE / ENG / SLIP, impact
at engagement, stop contacts) whose averaged behaviour is a nonlinear,
inertial, velocity-dependent force across the bias stage. The soft stage is
what routes the deflection to the generator (89 % statically), and the
generator load is what re-stiffens it dynamically when `c_eq ω ≳ k_b` (F2).
That trade is the design problem, and it is the Gate's and nobody else's.

**Not new, and not negotiable:** equations (2.1), (4.2) and the ledger. The
shaft never delivers more than the rod is pushed. Every public AKS number
has to be a loop area times a frequency, and the loop is driven by the
road.

---

## 9. Pointers

- `01_physics.md` §4 (sprag constraint, impact, slip), §7 (the road sets the
  supply), §11 (hand derivation).
- `tests/test_symmetry_breaking.py` reproduces §6 and the 1 kW table.
- `08_findings_that_change_the_story.md` F1, F2, F5, F7.
