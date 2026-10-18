# 03a — The push-down spinning top, from first principles

Companion to `03_symmetry_breaking_first_principles.md`. Avery asked that
the toy be studied properly, not used as a metaphor. This document records
what the toy's own literature establishes, derives its dynamics from Newton
alone, runs those dynamics (`aks_lab.toy.PumpTop`, experiment 009, tests in
`tests/test_pump_top.py`) and then maps every element onto the Gate.

Tags: literature facts are `literature` (snippet-graded: the primary pages
could not be opened from this container, see §1); toy parameters are
`asserted` (no toy on the bench); every result is `modeled` and reproduced by
`python experiments/009_pump_top_toy/run.py`.

---

## 1. What the record says about how the toy works

Primary hosts (Google Patents, USPTO full-text, Wikipedia, Cambridge
engineering pages) were refused by the container's proxy; the statements
below are from search-engine excerpts of those pages and should be upgraded
to page citations when the PDFs can be opened.

| Source | What it establishes | Grade |
|---|---|---|
| US 2,841,920 (Balleis, 1958, "Spinning top") | A screw-like driving rod reciprocates inside a hollow shaft; "a downward-pumping movement of the rod will be converted into a one-way rotary motion" by a clutch between rod and tube. The helix + one-way clutch architecture of the pump top is at least this old. | excerpt |
| US 3,785,081 (Ohio Art, 1974, "Toy spinning top") | "An axially reciprocal screw means for rotating the body", passing "through a ratchet means and into a tube within the top". Ratchet = pawl one-way element; the body is the flywheel. | excerpt |
| US 4,304,064 ("Toy spinning top") | Helical plunger through the head; a "gripping member slidably mounted on the screw so as to rotate when moved relative to the screw"; a clutch that "engages the mass" on the down-stroke; centrifugally actuated members. Confirms: the nut rides the helix, the clutch acts on the heavy mass, release on the up-stroke. | excerpt |
| US 4,455,781 ("Sorting top") | Body spun "by pumping a plunger"; clutch disks engage on the down push. Same architecture, friction clutch instead of pawl. | excerpt |
| US 6,406,349 / 6,607,420 ("Gyroscopic toy") | Flywheel spun by string or flexible rack; "once the flywheel is spinning it is impossible to impart more spin energy to the flywheel with the basic design"; the patent's fix is a gear reduction. This is the **race-speed ceiling** derived in §3: the driver cannot push the rotor above its own speed × ratio. | excerpt |
| otvinta.com / Thingiverse 3336383 (3D-printed mechanical top) | "The overrunning clutch converts the reciprocal motion of the spiral rod to the one-way rotational motion of the spinning top's body"; pawls with printed torsion springs; 20 cm body. A modern, fully documented build of the same mechanism. | excerpt |
| Yankee / spiral-ratchet screwdriver (North Bros 1899; engineering explainers) | Steep-lead multi-start helix; a pawl holds the nut on the push so the spindle must rotate as it translates; a return spring resets it; a second pawl lets it return without turning the bit. Turns per stroke = stroke / lead. | excerpt |
| Power-screw mechanics (standard texts) | Frictionless torque per unit axial force `T/F = L/2π`; with friction, efficiency `η = tan λ / tan(λ+φ)`, λ the lead angle, φ = atan μ; self-locking when μ > tan λ. A pump top needs a steep lead (λ ≫ φ) so the screw back-drives. | textbook |
| Pump drill (Neolithic to Iroquois; Wikipedia, Britannica, Firgelli explainer) | Cord wound on the spindle, crossbar pushed down → spindle spins; "the flywheel's inertia keeps the spindle turning after the push ends, which winds the cord back on in the opposite direction and lifts the crossbar". The return stroke is paid for by the flywheel. Direction alternates each stroke. | excerpt |
| Hugh Hunt (Cambridge), sleeping-top criterion | A top stands upright only when `C²ω² > 4·A·m·g·l` (C axial, A transverse inertia, l centre-of-mass height); for "a typical pump-up top" about 10 rev/s. | excerpt / standard result |
| Hobby tops with tachometers (Instructables) | Hand-launched and 3D-printed tops reach 2,000–5,000 rpm; measured by slow-motion video or optical tachometer. No pump-top rpm measurement was found. | excerpt |

What no source gives: energy per push, mechanical efficiency of the
helix–pawl path, or a measured pump-top speed. Those are exactly what §4
computes, and what a one-afternoon bench test with a cheap pump top, a
force gauge and a phone's slow-motion camera would turn into `measured`.

---

## 2. The machine, element by element

```
hand ──► plunger (m_p) ──► helix (lead L) ──► nut + pawl ──► top body (J) ──► bearing, air
            │                                     │
       return spring k_r                    overruns when ω > 2π v / L
       stops at x = 0 and x = S
```

- **Helix.** One revolution per `L` metres of plunger travel. The race
  ratio is `r = 2π / L` rad/m — the same quantity as the Gate's `r`.
- **Pawl.** A one-way element between nut and body: it can push the body
  up to the nut's speed, never pull it. Inequality `ω ≥ r·v` (down-stroke
  positive). When engaged, `ω = r·v` exactly.
- **Return spring.** Zero force at the top stop, `k_r·S` at the bottom.
  It stores `½ k_r S²` on the way down and gives it back on the way up — to
  the hand, or to a second pawl if there is one.
- **Stops.** The plunger hits the bottom when the hand keeps pushing after
  the body has outrun the nut (audible clack), and the top stop on return.
- **Body.** A disk of inertia `J` on a bearing (`c_w ω`) in air (`c_a ω²`),
  optionally loaded by a generator (`c_load ω`).

---

## 3. Dynamics from Newton

Plunger (down positive), hand force `F_h`, pawl force `F_c` (the force the
plunger transmits through the nut):

    m_p ẍ = F_h − k_r x + F_stop − F_c.                                 (3.1)

Body, with screw efficiency `η_s` on the transmitted power:

    J ω̇ = η_s F_c / r − c_w ω − c_a ω|ω| − c_load ω.                   (3.2)

**Free (pawl overrunning):** `F_c = 0`; (3.1) and (3.2) decouple.

**Engaged:** `ω = r v`, so `ω̇ = r ẍ`. Eliminating `F_c`,

    (m_p + J r² / η_s) ẍ = F_h − k_r x + F_stop − r (c_w ω + c_a ω² + c_load ω) / η_s.   (3.3)

The hand pushes the plunger plus a **reflected mass** `J r² / η_s`. For
the baseline toy (`J` = 1.25e-4 kg m², `L` = 25 mm/rev) that is 7.9 kg: a
20 g plunger that feels like eight kilograms while the pawl is driving.
This is the single most important sensation of the toy and the Gate's F2
in miniature — a fine helix (large `r`) multiplies both the speed ceiling
and the inertia the driver must push.

**Engagement** is an event at `r v − ω = 0⁺`. The plunger and body exchange
momentum through the pawl, `(m_p + J r²) v⁺ = m_p v⁻ + J r ω⁻`, with the
kinetic-energy deficit booked as pawl loss (zero when they meet at equal
speed, as they always do in the toy; the Gate's backlash impact is the
same bookkeeping, 01_physics §4.4).

**Disengagement** is the event `F_c = 0⁻`: the body no longer needs
pushing because the plunger is decelerating faster than the body is. From
then on `ω` only decays, while the plunger continues to the bottom stop.

**Ledger** (integrated as states, closes to 1e-8 on every run):

    E_hand = ΔKE_plunger + ΔKE_body + ΔU_spring + ΔU_stop
           + E_screw + E_bearing + E_air + E_load + E_pawl + E_stoploss.    (3.4)

**The hand.** A hand is not a prescribed stroke. It is modeled as a
Hill-type force–velocity law, `F_h = F₀ · max(0, 1 − v / v_max)` during the
push phase and zero while the hand lifts: full force when stalled, nothing
once the plunger runs away at `v_max`. This is what makes the ceiling
below kinematic rather than an artefact.

### 3.1 The race ceiling (first principle of the toy)

From the inequality `ω ≥ r v` with the pawl only ever *pushing*:

    ω(t) ≤ max over the current push of r·v(τ)   while engaged,
    ω̇ ≤ 0                                        while free.             (3.5)

So `ω_max ≤ r · v_hand,max`. **The hand's speed limit, not its force, sets
how fast the top can ever go.** This is what the gyroscopic-toy patent
means by "impossible to impart more spin energy with the basic design",
and why its remedy is a gear ratio (a larger `r`).

### 3.2 Energy per push

Per push the hand's work splits as

    W_hand = ΔKE_body + (screw + bearing + air + load over the cycle) + E_stop.

Spin-up continues while `W_hand − losses > 0`; the top saturates when the
losses per period equal the hand's work per period. With no load the
saturation speed is still below `r v_max` because drag grows with `ω²`.

### 3.3 The return stroke

The spring returns `½ k_r S²` (0.36 J in the baseline) on every up-stroke.
With one pawl that energy goes back into the hand and the top stop. A
second, opposed pawl (the Gate's full-wave arrangement) lets the body take
it instead. The body can gain at most what the spring stored, and the
spring stored only what the hand put in on the way down. Full-wave
rectification raises **capture**, bounded by a factor two; it adds no
source. The pump drill is the same lesson from the other side: there the
*flywheel* pays for the return stroke, rewinding the cord and lifting the
crossbar, which is why a pump drill with too little flywheel "stops after
two pumps" (a builder's complaint found in the search).

---

## 4. Results (experiment 009, baseline toy; all `modeled`)

Baseline: lead 25 mm/rev (r = 251 rad/m), 60 mm stroke, 20 g plunger,
200 N/m return spring, 0.1 kg × 50 mm disk, 80 % screw efficiency, hand
15 N / 1 m/s, push 0.3 s in a 0.6 s period.

**Spin-up.** 20 pushes take the top from 0 to 191 rad/s (1,820 rpm). The
first push delivers 0.60 J, of which 0.35 J lands in the body; by the
twentieth, 0.39 J is delivered and 0.03 J lands, the rest going to drag
and to the bottom stop. On every push `ω_end` sits just below
`r · v_peak` of that push (74.8 vs 75.3; 190.6 vs 192.3 rad/s): the race
ceiling in action.

**Lead sweep.** Halving the lead doubles `r`, lifts the 20-push speed from
191 to 241 rad/s and the reflected mass from 7.9 to 31.6 kg. Coarsening it
to 100 mm/rev drops the ceiling to 63 rad/s and the top never passes
116 rad/s; it also wastes 80 % of the hand's work in the bottom stop
because the light reflected mass lets the plunger run away.

**One pawl vs two.** Same hand, 12 s: half-wave puts 2.27 J in the body
and 4.70 J into the stops; full-wave puts 4.21 J in the body and 0.15 J
into the stops, from *less* total hand work (8.13 vs 8.96 J). The second
pawl recovers the return spring's energy. Body energy stays below hand
work in both.

**A generator on the top.** Loading the body with `c_load` from 2e-5 to
5e-4 N·m·s: steady electrical power 0.31 → 0.63 → 0.58 W against hand
power 0.84 → 1.15 → 0.92 W; conversion 37–63 %; steady speed falls from
121 to 16 rad/s. The toy as a generator delivers a fraction of the hand's
power and slows as the load rises. There is a best load (here ~2e-4), as
there is a best `c_gen` for the Gate.

**Hand stops.** ω 168 → 158 → 146 → 127 rad/s over 10 s; nothing enters.
The top is a store with a leak.

**Stronger vs faster hand.** 30 N at 1 m/s: 213 rad/s. 15 N at 2 m/s:
236 rad/s. The speed limit matters more than the force, as (3.5) says.

Sleeping-top check: for this disk `C ≈ 1.25e-4`, `A ≈ 0.5 C`, mass 0.1 kg,
l ≈ 0.03 m → stable above ω ≈ 2·√(A m g l)/C ≈ 69 rad/s, i.e. the first push
already stands it up — consistent with Hunt's "about 10 rev/s".

---

## 5. Mapping onto the Gate (US 12,409,695 B2)

| Toy | Gate | Same equation |
|---|---|---|
| hand pushing the knob | main spring 122/714 pushing the frame plate 111 (driven, through the tire, by the road) | the source term in (3.1) / 01_physics §5 |
| plunger + helix nut | drive rod 101 anchored to the chassis 602 | kinematic input `x_b` |
| lead `L`, `r = 2π/L` | transmission ratio `r` (open parameter; the patent fixes none) | `ω = r·ẋ` |
| one pawl (down-stroke) | sprag 106 | inequality `ω ≥ r ẋ` |
| the second pawl (§3.3) | opposed sprag 107 | `ω ≥ −r ẋ` |
| top body `J` | fly weights 103 + generator rotor 108 | `J ω̇` and reflected mass `J r²` |
| return spring `k_r` | frame biasing spring 115 | conservative, zero loop area |
| stops at 0 and S | coil bind and full-extension retainer | 01_physics §3.2 |
| bearing + air | `c_w`, overrun drag `c_od` | `E_bearing`, `E_clutch` |
| generator load | `c_gen` → battery | `E_load` = `E_elec` |
| race ceiling `ω ≤ r v_hand,max` | `ω ≤ r·max|ẋ_b|`; rotor speed ripple std/mean 0.7 (exp 006) | (3.5) |
| reflected mass 7.9 kg felt by the hand | `J r² ≲ 10 kg` rule (exp 004, F2) | (3.3) |
| saturation when losses = hand work per push | φ set by `c_gen r²` against the corner's dynamics | §3.2 |

Everything the toy does, the Gate does; the only difference is who pushes.
In the toy it is a hand with 15 N and 1 m/s. In the Gate it is the main
spring, whose force fluctuation and velocity are set by the road through
the tire (01_physics §7: 122 W per corner, mid-size car, ISO C, 60 mph).
The toy makes the three structural facts visible without any road theory:

1. the clutch sets a **speed ceiling**, not a source;
2. the flywheel and the spring are **stores**;
3. a second one-way element raises **capture** of what the pusher already
   supplied, by at most a factor two, and the ledger closes either way.

---

## 6. What to measure (cheap, decisive)

A pump top, a 0–20 N force gauge taped under the knob, a ruler and a phone
at 240 fps give in one afternoon: force–stroke loop per push (`W_hand`),
rpm per push (`ΔKE_body` with the disk weighed and measured), spin-down
(`c_w`, `c_a`). Those three numbers test (3.3)–(3.5) directly and would be
the first `measured` entries in this repository. Protocol in
`05_bench_protocol.md` can be reused verbatim at toy scale.

---

## 7. Sources

Web excerpts retrieved 2026-10-18 (full pages blocked from this container):
Google Patents US2841920A, US3785081A, US4304064A, US4455781A, US6406349B1,
US6607420B2; Thingiverse thing:3336383 and otvinta.com/download15.html;
Wikipedia "Yankee screwdriver", "Pump drill"; Britannica "pump drill";
firgelliauto.com mechanism explainers (double-acting screwdriver, pump
drill stock, power-screw calculator); Hugh Hunt, "Why does a spinning top
stay up?", Cambridge University Engineering Department; UCF lecture notes
"top_17.pdf" and arXiv 1201.4918 for the sleeping-top criterion;
Instructables "Designing a FAST 3D printed spinning top (4742 rpm)".
