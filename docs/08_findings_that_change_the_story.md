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

**How sure.** Certain for the stated model (it is an identity). Tire
damping was checked directly: it increases the power the road delivers
(+50 % at c_t = 300 N·s/m, +150 % at 1000) but the increase is dissipated
in the tire at high frequency and the Gate's output *falls* (9.5 → 7.8 W).
Enveloping reduces the high-frequency supply further. A road spectrum that
is not ∝ n⁻² (ISO 8608 allows w ≠ 2) changes the number, not the
conclusion. Nothing opens a reservoir "several times" larger for the
suspension.

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

**How sure.** Arithmetic for the static part. **Experiment 005 narrows the
regime:** with the OEM damper in place the frame stage is dominated by the
reflected generator damping, strokes only 7–9 mm RMS on ISO C at 60 mph,
and never reaches a stop at any ratio (0.05–0.8) or travel (2–5 in).
Stops become real when the damper is reduced or on class D (experiment
002: 5–12 % of the time, 22–58 contacts/km). The static few-percent load
margin is correct but is not the operating regime on paved roads.

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

## F5. With ride and tire grip held at stock levels, a passenger-car corner nets single-digit to low-double-digit watts; positive net benefit starts at ISO D or on heavy wheel stations

**What AKS says.** Diligence Response: 30–100 W average per corner on
ISO C for a 1500–2000 kg car; 70–175 W on ISO D; deck: ~350 W per pickup,
~5 kW per loaded Class 8 on average roads.

**What the repo finds (linear surrogate, exact; `reports/linear_frontier.md`).**
The Gate's frame stage is a spring k_b in parallel with the reflected
generator damping c_eq = c_gen·r², in *series* with the main spring. Three
consequences follow from the exact H₂ solution of that corner:

1. The best generator load is c_eq ≈ 300–500 N·s/m for a passenger car
   and is nearly independent of the bias ratio (0.05–1.0) — the ratio
   sets stroke, not power.
2. Taking more of the budget requires removing the OEM damper, and a
   series stage cannot replace it: as c_s → 0 the body mode goes
   undamped (sprung acceleration ×7). The unconstrained maximum φ ≈
   0.33–0.50 is reached only with the damper at 10% and dynamic tire load
   up 50–90% — not a vehicle anyone would ship.
3. Holding sprung-acceleration RMS ≤ passive **and** tire-load RMS ≤ 1.1 ×
   passive, the ceiling is φ ≈ 0.11 (mid-size car), 0.17 (F-150), 0.21
   (HMMWV), 0.25 (loaded Class 8 station), 0.39 (MRAP). **Tire-load
   variation, not ride, is the binding constraint**: the soft series
   stage lets the wheel follow the road less closely.

| vehicle, 60 mph | supply ISO C | P_elec ceiling ISO C | P_net (with gate mass) | P_net ISO D |
|---|---|---|---|---|
| mid-size car corner | 122 W | 13 W | −16 W | +14 W |
| F-150 corner | 169 W | 28 W | −12 W | +48 W |
| HMMWV corner | 271 W | 56 W | +10 W | +158 W |
| Class 8 loaded dual station | 1220 W | 304 W | +233 W | +1129 W |
| MRAP corner | 745 W | 289 W | +218 W | +1068 W |

(mass penalty at the `gate_mass` estimate: 26 W for 10 kg at 60 mph on a
car; the estimate is open.) The nonlinear sweeps (001–003) include stops,
freewheeling and partial engagement and can only come in at or below these
numbers; experiment 001 at the surrogate's load point gives 9.7 W vs the
surrogate's 10.6 W.

**Damper placement (experiment 006).** Mounting the OEM shock between the
frame's bottom plate and the axle, so it no longer bridges the Gate, raises
the mid-size-car corner from 9.7 W to 46.8 W (φ 0.38) on ISO C at 60 mph —
with tire-load RMS +40 % and W_k −39 %, the same trade the retrofit pays
for cutting its damper. The harvest-vs-grip curve is one curve; layout and
damper scale move along it.

**Uncertainty bands (experiment 007, 1,152 runs, 48 Latin-hypercube
draws of every open parameter per cell).** Mid-size car ISO C at 60 mph:
P_elec 5.6–12.3 W (5–95 %), P_net −45 to −13 W; F-150 9.4–20 W; HMMWV
17–34 W. The spread is set by the Gate's own friction and overrun drag,
then generator efficiency — all bench-measurable — not by the road.

**Nonlinear confirmation (experiment 002, 504 runs).** φ with the stock
damper: 0.08 (car), 0.09 (F-150), 0.11 (HMMWV) on every class and speed;
P_net at 60 mph on ISO C: −21 / −23 / −18 W; positive only on ISO D (−3 /
+3 / +48 W) or, for the HMMWV, with the damper cut to 25 % (+8 W on C,
+114 W on D, with tire load +34 % and the frame on a stop 12 % of the
time). Full table in `experiments/002_roads_speeds_vehicles/README.md`.

**How sure.** Exact for the linear model; the model's assumptions (small
motion, no stops, white road velocity, point-contact tire) all err on the
generous side. The tire-load constraint threshold (10%) is a choice;
loosening it to 25% raises the car ceiling to roughly φ 0.2.

**What to say instead.** For passenger cars: "tens of watts per corner on
average roads at highway speed, net of hardware mass roughly zero; the
device pays for itself only on rough roads." For heavy and tactical
vehicles on rough duty: "hundreds of watts per wheel station, about a
kilowatt per station on ISO D" — which is where the Military Brief already
put it (60–300 W per corner, 0.25–1.2 kW per vehicle). The deck's 350 W
pickup and 5 kW average-road semi are not reachable under any ride or grip
constraint in this model.

---

## F6. Clutch life has no literature basis — the first test must be an endurance test

**What AKS says.** Pitch deck: "two clutches, a flywheel, a generator;
soldiers can service it with hand tools." Diligence Response: sprag
rectifier efficiency 96–98 %. Military Brief: rating basis 1e6 cycles →
139 h at 2 Hz (its own derived figure).

**What the repo finds.** (a) The model's engagement rate is ≈ 170 per km
per clutch set on ISO C at 60 mph (both sets, symmetric), i.e. 1.7×10⁵
indexing cycles per set per 1000 km, 10⁶ per ~6000 km — at 15 mph on rough
ground the per-km count rises. (b) No sprag or roller freewheel
manufacturer publishes a cycles-to-failure basis for its torque rating;
practice is nominal torque × an indexing service factor (2–4, stepped at
150 strokes/min; +50 % with vibration), with fatigue micro-chipping named
as the indexing failure mode (GMN). (c) No endurance or failure data exist
for any mechanical-motion-rectifier harvester in fifteen years of
publications; the one railcar field program reports only "no significant
problems" at low power. (d) The "1e6 cycles" basis in the Military Brief is
**not verified** by any catalog text found.

**How sure.** The engagement rate is a robust model output (it is set by
the road's zero-crossing rate, not by the load). The absence of life data
is an absence of evidence after a targeted search of ~40 primary hosts by
snippet; full catalog PDFs were not readable from this environment.

**What to say instead.** Nothing about service life until measured. Add a
clutch-only endurance leg to the bench (T6 in `05_bench_protocol.md`):
cycle the rectifier at 2–3 Hz at the modeled T_c,p99 for ≥ 10⁶
engagements, monitor drag torque and backlash, and publish the hours.

---

## F7. The kilowatt story is real — on rough roads and heavy stations, with the "average roads" label removed

**What AKS says.** Deck slide 10: "Loaded Class-8 semi: ~5 kW average ·
10–16 kW rough-road peaks"; "Full-size pickup: ~350 W average roads."
Military Brief: 60–300 W per corner on rough ground, 0.25–1.2 kW per
vehicle, near zero on pavement.

**What the repo finds (experiments 002–003, 952 runs).** Per wheel station
at 60 mph with the stock damper: loaded Class 8 dual station 153 W on
ISO C, 614 W on ISO D; MRAP 95 / 381 W; HMMWV 29 / 117 W; F-150 15 / 59 W.
Per vehicle (9 dual stations) a loaded tractor-trailer harvests ~1.4 kW
gross on ISO C and ~5.5 kW on ISO D; with damping reduced to 25 % (tire
load +19 %) 3.3 / 13 kW. Net of hardware mass, heavy stations are positive
from ISO C at highway speed; the pickup is positive only on ISO D (+3 W at
stock damping, +42 W with damping cut).

**How sure.** Model, with literature-typical heavy-vehicle parameters and
the open hardware mass; ±3 % seed scatter; the exact theorem fixes the
supply (1.2 kW per dual station on ISO C at 60 mph), so the uncertainty is
in φ (0.11–0.13 stock, 0.28–0.33 reduced), the parasitics (±35 %, F6
tornado) and the mass.

**What to say instead.** "Hundreds of watts per wheel station on average
highways, around a kilowatt per station on rough roads, for heavy trucks
and tactical vehicles; a few kilowatts per vehicle on the roads where
those vehicles actually run. For passenger cars, tens of watts per corner
and roughly break-even after the hardware is carried." The Military
Brief's framing (engine-off watts into the anti-idle battery, rough
ground, 0.25–1.2 kW per vehicle) is consistent with the model; the deck's
is not.

---

*(Entries F8+ are appended as the experiments complete.)*
