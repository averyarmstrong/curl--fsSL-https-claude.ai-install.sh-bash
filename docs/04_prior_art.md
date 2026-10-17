# 04 — Prior-art separation, claim by claim

Scope: how each element of US 12,409,695 B2 relates to the documents the
brief names (Li/Zuo 2013 MMR; Hsu 1996; Suda 1998; Karnopp 1989; one
Levant/ClearMotion patent) plus the two documents the intake surfaced as
most relevant (Schenavar 1977; Hyundai 2016) and the two measured anchors
(Audi eROT 2016; Abdelkareem 2021). This is a technical separation, not a
legal opinion; counsel should read the primary documents.

**Evidence grade.** The container's network policy blocked every primary
host (patents.google.com, USPTO, IOP, ASME, IEEE, ScienceDirect, Formsprag,
GMN); evidence is search-engine snippets of those pages and citing papers.
Each statement below carries the grade from the raw dossier
(`data/literature/prior_art_dossier_raw.md`): **[P]** primary-page snippet,
**[S]** secondary, **[NV]** not verified. Nothing is invented; eight open
items that need the PDFs are listed at the end.

## '695 elements (shorthand used below)

| # | Element | Claims |
|---|---|---|
| E1 | Vertically collapsible frame *in the load path* between chassis and suspension | 1, 5–7, 10, 14–16 |
| E2 | Frame biasing spring, rate lower than the (replacement) main spring, in series; heights add to the original spring height | 2–3, 11–12 |
| E3 | Rotatable **hollow** generator shaft with the drive mechanism inserted in it | 1, 10 |
| E4 | Spin imparted on both collapse and expansion | 1, 10 |
| E5 | Sprag (one-way) clutch drive giving unidirectional drive during both collapse and expansion | 4, 13 |
| E6 | Fly weights keeping the generator rotating through the transition | 8, 17 |
| E7 | Generator / alternator; energy storage | 1, 9, 18 |

## 1. Li, Zuo, Kuang, Luhrs 2013 — MMR shock absorber [P]

*Smart Mater. Struct.* 22 025008. Retrofit telescopic damper (parallel with
the main spring, full suspension stroke). Rack-and-pinion → pinion shaft
with **two one-way roller clutches** of opposite sense driving two large
bevel gears → one small bevel gear on the generator shaft, so the generator
turns one way on both strokes. PM DC generator, R_int = 6.6 Ω. Rotor inertia
used as the flywheel through zero-crossings ("disengagement").
Numbers: mechanical efficiency ≈ 60% at 1.5 Hz × 5 mm (peak race velocity
0.047 m/s), plateau ≈ 62%; electrical efficiency 82–94% at 30–100 Ω; 40.4 W
and 25.6 W at **3 Hz × 5 mm** (peak 0.094 m/s) on two loads (30/100 Ω per
the IOP text, 23.4/94.6 Ω per another copy [NV]); > 15 W (15.4 W) on a
Suburban at 15 mph on smooth pavement.
Separation: E4, E5 present (two opposed clutches); E6 partial (rotor
inertia, no added flyweights); E7 present. **E1, E2, E3 absent** — no
load-bearing frame, no series spring, solid shaft with a bevel train.
Note: the gate-twin anchor "40 W @ 0.047 m/s RMS" conflated two conditions
and is withdrawn.

## 2. Zuo & Zhang 2013 — analytic harvestable power [P abstract]

*J. Vib. Acoust.* 135(1) 011002. H₂-norm quarter- and full-car analysis
with ISO roughness; "100–400 W average power is available in the suspensions
of a middle-sized vehicle at 60 mph on good and average roads"; power is
sensitive to roughness, tire stiffness and speed, insensitive to suspension
stiffness, damping and masses. Closed form and parameter table **[NV]**
(not retrievable). `01_physics.md` §7 derives the exact statement
independently (P̄ = ¼ k_t W_v) and the repo reproduces the 100–400 W band
(B 122 W, C 488 W per car for the mid-size parameter set). No device
elements; this is the supply ceiling against which every Gate number is
reported.

## 3. Hsu 1996 — electrical active suspension power recovery [P abstract]

IECEC 1996, pp. 1899–1904. Electric-motor active suspension with LQ control;
"up to 100 W per wheel in a highway driving condition" for a mid-size car
(a review places it at 16 m/s ≈ 36 mph, not 30 mph [S]); net consumption in
city driving. Parallel electromagnetic actuator. None of E1–E6.

## 4. Suda, Nakadai, Nakano 1998 — self-powered hybrid suspension [S]

*Veh. Syst. Dyn.* 29(S1) 619–634. Two linear DC motors per corner, one as a
regenerative damper, one as actuator; skyhook law; all control energy from
regeneration. Watts **[NV]**. Parallel EM devices, electrical rectification
only. None of E1–E6.

## 5. Karnopp 1989 — PM linear motors as variable dampers [S]

*Veh. Syst. Dyn.* 18(4) 187–200. Feasibility of linear PM dampers; force set
by copper mass under a constant-field assumption; limited by 1989 magnets.
Parallel linear damper. None of E1–E6.

## 6. Levant Power / ClearMotion — US 8,841,786 B2 [P]

"Integrated energy generating damper", issued 2014-09-23; continuation
family to US 12,264,656. Telescopic hydraulic damper; piston flow drives a
gerotor hydraulic motor coupled to a generator immersed in the fluid;
back-EMF provides damping; wiring exits through a **hollow piston rod**.
Numbers in the specification **[NV]**. Separation: E4 present (hydraulic,
both strokes); E7 present; E3 superficially similar (a hollow rod) but used
for wiring, not as a generator shaft receiving a drive rod; E1, E2, E5, E6
absent.

## 7. Schenavar — US 4,032,829 (1977) "Road shock energy converter for charging vehicle batteries" [P]

Priority 1975-08-22, issued 1977-06-28, expired. Axle coupling with
oppositely acting rack-and-pinion units; **unidirectional clutches** linking
axle motion to one shaft turning one way on both up and down movement;
**flywheel(s)** on the shaft to smooth intermittent torque; generator
charging vehicle batteries; optional rack-cushion spring (claim 2). Cited by
Tufts US 6,952,060 and US 9,597,965. **Not on the '695 citation list** (as
supplied; '695 front page not fetchable — the uploaded PDF's list matches
the supplied one and does not include it).
Separation: E4, E5 (in substance — two oppositely acting units with
unidirectional clutches on one shaft; claim wording [NV]), E6 and E7
present. E1, E2, E3 absent: the unit sits beside the suspension and carries
no sprung load; its spring is a rack cushion, not a series load-bearing
stage; solid shaft. **This is the closest art to claims 4 and 8 and the most
important item for counsel.**

## 8. Hyundai — US 9,205,716 B2 (2016) [P]

Control-arm bush pickup converting link rotation to gear rotation; one-way
clutch; three-stage planetary speed-up; generator, rectifier, battery.
Whether the granted claim covers both-stroke drive **[NV]**; the
description is a single one-way clutch (half-wave). Parallel pickup, no
load path, no series spring, no hollow shaft, no flyweights. E7 present;
E5 partial (one clutch); rest absent. Live until ~2034.

## 9. Audi eROT (press release 2016-08-10) [S, multiple reprints]

Electromechanical rotary dampers: lever arm → gears → generator near the
rear axle, 48 V. 100–150 W average on German roads; 3 W on new freeway;
613 W on rough secondary road; ≤ 3 g CO₂/km. Vehicle mass and damper count
not stated (the AKS corpus's "1800 kg sedan" is an assumption). Parallel
rotary EM damper, bidirectional rotation, electrical rectification. None of
E1–E6. Anchor only.

## 10. Abdelkareem et al. 2021 — measured off-road SUV damper power [P abstract]

*Measurement* 179, 109381. Instrumented passive damper on an XLW 5062X SUV,
10–40 km/h: 30–334 W per damper off-road, 3–25 W on city roads; rebound
dissipates ≈ 6× compression; off-road ≈ 12× city. No device. The 6:1
asymmetry is a damper-valving property, not a road property; the Gate's
two-stroke split must be derived (it is, experiment 001: engagement counts
A vs B).

## Separation matrix

P present · p partial · – absent · ? not verifiable

| Element | Li/Zuo 2013 | Hsu/Suda/Karnopp | Levant '786 | Schenavar '829 | Hyundai '716 | eROT |
|---|---|---|---|---|---|---|
| E1 load-path collapsible frame | – | – | – | – | – | – |
| E2 softer series bias spring, heights add | – | – | – | – (cushion only) | – | – |
| E3 hollow generator shaft + inserted drive | – | – | p (hollow rod for wiring) | – | – | – |
| E4 both strokes drive | P | – | P | P | ? | P |
| E5 two opposed one-way clutches | P | – | – | P (substance) | – (one) | – |
| E6 flyweights through transition | p | – | – | P | – | – |
| E7 generator + storage | P | P | P | P | P | P |

**Reading.** No retrieved document combines E1–E3 with E4–E6. The
elements most exposed are E5 (Li/Zuo 2013; Schenavar 1977) and E6
(Schenavar 1977). The distinguishing elements on this evidence are the
load-bearing collapsible frame with a softer series biasing spring (E1–E2)
and the hollow generator shaft receiving the drive mechanism (E3). The AKS
public materials' phrase "the only patented art known that will …" (Sept
2026 deck) is not supportable against this matrix and is flagged in
`07_claims_audit.md`.

## Open items (need the primary PDFs)

1. Li et al. 2013: load values (23.4/93.4 vs 30/100 Ω), gear ratio, figure numbers.
2. Zuo & Zhang 2013: closed form and parameter table (to replace our literature-typical mid-size set with theirs).
3. US 4,032,829 claims verbatim; confirm one vs two clutches in claim 1.
4. US 9,205,716 claim 1 scope.
5. The granted SUNY/Zuo MMR patent number (US 9,118,487 and US 2013/0127175 **not confirmed**; US 12,088,180 surfaced).
6. Formsprag: drag-torque units, per-model lift-off rpm, cycle basis of torque ratings (the "1e6 cycles" figure in the military brief is **not** confirmed).
7. ISO 8608 Table C.2 and ISO 2631-1 Table 3 from the standards.
8. Audi MediaCenter original.
