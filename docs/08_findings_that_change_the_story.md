# 08 — Findings that change the story

Written first, plainly, before anything else, whenever a result contradicts
something AKS currently says publicly. Each entry: what AKS says, what the
repo finds, how sure we are, what to say instead.

---

## F1. The road sets the watts; nothing above the tire — damper, spring, or Gate — changes the supply

**What AKS says.** Pitch deck (July 2026) slides 4 and 11: "the spring in
front of that damper handles a several-times-larger flow of energy every
single stroke … nobody instrumented the give-back"; "whoever sits first in
the load path touches it first — and keeps it"; the damper is "5% of the
kinetic pool" (Sept 2026 deck); targets of ~350 W per full-size pickup and
~5 kW per loaded Class 8 on average roads via P = κ·W·v. Diligence Response
(Aug 2026): "the premise that engaging first means engaging at lower energy
is the reverse of how series springs behave … 89.3% of the elastic energy
exchange" is in the bias stage.

**What the repo finds.** For any corner on a point-contact undamped tire of
rate k_t, driven by an ISO 8608 road (white ground velocity of level
W_v = 4π² G_d(n₀) n₀² V), the mean power the road delivers is exactly

    P̄_road = ¼ k_t W_v = π² G_d(n₀) n₀² V k_t

independent of every parameter above the tire — masses, spring rates,
damper, series soft stage, clutches, flywheel, generator load. Proof in
`01_physics.md` §7; exact to 10⁻⁶ for the linear corner by the Lyapunov/H₂
evaluation (`tests/test_analytic_limits.py::test_road_power_theorem_exact_for_linear_corner`)
and reproduced by the full nonlinear Gate simulation within realisation
scatter (`…::test_road_power_theorem_holds_with_the_gate`). Numbers for the
mid-size car (k_t = 180 kN/m) at 60 mph: A 7.6 W, B 30 W, **C 122 W**,
D 488 W per corner. A loaded Class 8 dual-tire station (k_t ≈ 1.8 MN/m)
gets 10× that — because of its tires, not its weight.

The "several-times-larger flow" through the spring is *reactive* power
(stored and returned within each cycle, mean exactly zero). The repo reports
it beside the real power in every table (`P_spring_cycle` vs `P_road`) so
the two cannot be confused again. The static 89.3% partition is a statement
about where elastic energy *sits*, not about what can be *removed*; the
removable fraction is φ, a dynamic quantity that the experiments compute.

**How sure.** Certain for the stated model (it is an identity). The only
physical escape hatches are tire damping and enveloping, both of which
*reduce* the high-frequency supply, and a road spectrum that is not ∝ n⁻²
(ISO 8608 allows w ≠ 2; real roads deviate). Neither opens a reservoir
"several times" larger.

**What to say instead.** "The road delivers a fixed budget of order
100 W per passenger-car corner on an average road at highway speed, and
several hundred to a thousand watts per heavy-truck wheel station. Today
that budget is burned as heat in the damper. The Gate's job is to take as
much of that budget as possible through a generator instead of a damper,
without degrading ride or tire grip. How much it takes is φ, and we measure
it." Drop "the spring is the bigger reservoir", "5% of the kinetic pool",
and every P = κ·W·v vehicle table.

---

## F2. At the prototype's spring ratio and the gate-twin drive ratio, the frame stage barely moves

**What AKS says.** First-principles doc and gate-twin baseline: screw lead
1 in/rev, step-up ~6:1 (r ≈ 1484 rad/m), rotor inertia 3×10⁻⁴ kg m².

**What the repo finds.** While a clutch is engaged the rotor inertia is
reflected onto the frame stroke as an inertance J r² = 660 kg. The soft
stage, whose whole purpose is to move first, is then stiffer in effect than
the main spring and strokes 3.7 mm RMS on ISO C at 60 mph; electrical
output 3 W per corner (smoke run, `experiments/001` baseline corner r=1484,
J=3e-4). Reducing r to 300 rad/m (J r² = 27 kg) restores the stroke
(10 mm RMS) and raises output to ~11 W at the same load before any
optimisation. The drive ratio and flywheel inertia are therefore not free
"generator-side" choices; they set whether the frame stage works at all.
Quantified in experiments 001, 004 and 006.

**How sure.** The mechanism (inertance of a geared rotor) is textbook
(Smith 2002) and was observed in Li/Zuo 2013; the magnitude depends on r
and J, both open parameters.

**What to say instead.** Nothing publicly yet; internally: the mechanism
must be designed as an impedance-matching problem with J r² as a first-class
variable, and the bench must measure the engaged-mode inertance directly
(a frequency sweep at fixed amplitude will show it as a mass-like term).

---

## F3. A soft stage with 2–5 in of travel binds at a few percent of corner-load variation

**What AKS says.** Patent: the first 2–5 in of travel go to the bias
spring. Diligence Response: vehicle-scale bias rate 18–30 lbf/in against a
150–250 lbf/in main spring (ratio 8.35:1), "preloaded to corner static
load".

**What the repo finds.** The force the frame can take before a stop is
k_b × (travel to that stop). With k_b = k_m/8.35 and 4 in of travel centred
on equilibrium, that is about ±5% of the static corner load for a 1600 kg
car (`01_physics.md` §3.3) and dynamic spring-force variation on ISO C at
60 mph is 10–20% RMS. Experiment 005 maps time-on-stop and stop contacts
per km against ratio and travel. Preloading to the static load, as
proposed, puts the equilibrium *at* the extension stop and makes the device
half-wave (rebound cannot expand a frame that is already fully expanded).

**How sure.** Arithmetic for the static part; the dynamic rates come from
the model. (To be completed with experiment 005 numbers.)

**What to say instead.** The travel/ratio/preload triple is a design
decision with a hard trade-off, not a feature; the patent's "2–5 in" is a
range to be chosen against measured stop rates.

---

## F4. No measured AKS power number exists yet

**What AKS says.** The kickoff brief refers to "~14 W per corner from
early prototype data, tagged measured". The pitch deck shows "287 W …
interactive model".

**What the repo finds.** No dated test record, data file, or note
containing a measured AKS output was found in the uploads or in Drive. The
Proof-of-Concept plan dates instrumentation to Aug–Oct 2026 and the
Diligence Response states the prototype had not been run. The 287 W figure
came from a browser simulation whose file is not available for audit.

**What to say instead.** The README states that there are zero measured
AKS numbers as of 2026-10-17 and lists what the first bench run will
produce. When the 14 W record is supplied, it goes in
`data/prototype/` with its conditions and the README is updated.

---

*(Entries F5+ are appended as the experiments complete.)*
