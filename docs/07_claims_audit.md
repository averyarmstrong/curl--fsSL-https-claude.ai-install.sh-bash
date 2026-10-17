# 07 — Claims audit

Every quantitative or performance claim found in the patent text, the
pitch decks (Google Slides July 2026 and `AKS Deck.pptx` Sept 2026), the
Diligence Response (Aug 2026), the one-pager (Oct 2026), the Website
Blueprint (Oct 2026) and the Technical Brief (May 2026). For each: tag,
support, recommended wording. Tags: `measured` · `modeled` (reproducible
in this repo, experiment ID given) · `target` · `asserted` (stated without
calculation) · `unsupported` (contradicted or non-physical).

"Wording" follows the Website Blueprint's own Say / Do-not-say table.

| # | Claim (source) | Tag | Support | Recommended wording |
|---|---|---|---|---|
| C1 | "Converts vertical movement … into electrical energy" (patent abstract, claim 1) | modeled | Gate element rectifies both strokes; P_elec > 0 on every road class (exp 001–003) | keep |
| C2 | Bias spring compresses more than the main spring by the ratio of rates until fully compressed (patent col. 6:33–41) | modeled | series stack + coil-bind stop reproduce it; stop rates in exp 005 | keep; add that the stop is reached at a few % of load variation at the prototype ratio (F3) |
| C3 | "Most of the initial 2–5 in of suspension compression is received into the bias spring" (col. 6:65) | modeled | true between stops; exp 005 gives the fraction of time between stops | "the first inches of travel, within the frame's stroke, are taken by the bias spring" |
| C4 | Generator turns "before the energy … gets dissipated" (col. 3:3) | asserted → tested | the supply is fixed (F1); the Gate takes a share φ of it before the damper takes the rest; share reported per experiment | "diverts a share of the suspension's energy flow to a generator instead of the damper" |
| C5 | "Without placing a drag on the vehicle" (col. 8:55) | modeled (partial) | vertical harvesting imposes no first-order longitudinal drag; added mass costs ΔP_mass = Δm g C_rr V (≈ 2.6 W per kg at 60 mph) | "no propulsion drag from the harvesting itself; the hardware mass costs a few watts per kilogram" |
| C6 | "19–58 W of damper dissipation on passenger cars … the spring handles a several-times-larger flow" (deck s.4) | unsupported | F1: the larger flow is reactive; the real supply is ¼k_t W_v (≈ 122 W/corner ISO C 60 mph, 30 W ISO B) | drop |
| C7 | "Full-size pickup ~350 W average roads" (deck s.10, P = κ·W·v) | unsupported | supply for an F-150 corner (k_t 250 kN/m) on ISO C at 60 mph is 169 W/corner = 678 W/vehicle *gross*; harvested share φ from exp 002 | replace with the exp 002 range for f150 |
| C8 | "Loaded Class-8 ~5 kW average · 10–16 kW rough-road peaks" (deck s.10) | unsupported as stated | supply for a dual station (k_t 1.8 MN/m) ISO C 60 mph = 1.22 kW gross; ×9 stations = 11 kW gross; harvested share from exp 003 | replace with exp 003 ranges, per station, with road class and speed |
| C9 | "Generator side is trivial: 10 kW is 16 N·m at 6000 rpm; the binding constraint is road energy input" (deck s.10) | modeled | correct; F1 quantifies the constraint | keep |
| C10 | "40 W per corner at 0.047 m/s, >60% mechanical efficiency" (deck s.10, from Li/Zuo 2013) | asserted (mis-cited) | 40.4 W is 3 Hz × 5 mm (peak 0.094 m/s); 60% is 1.5 Hz × 5 mm (peak 0.047 m/s) | cite correctly: "40 W on a bench at 3 Hz × 5 mm; ~60% mechanical efficiency" |
| C11 | "Audi eROT 3 / ~125 / 613 W" (deck s.10) | measured-literature | press release 2016-08-10, vehicle totals | keep; say "vehicle total, German roads" |
| C12 | "The only architecture where harvesting improves the ride … no tradeoff" (deck s.12) | asserted → tested | exp 001/002 report Δa_w and ΔDTL with sign; any dissipator at the matched point damps | report the measured sign; drop "only" and "no tradeoff" |
| C13 | "LIVE PHYSICS SIM: 287 W on rough-road input, single bench unit" (deck s.9) | unsupported | simulation file not available; supply for a bench-scale article is W; see F4 | remove until the file is audited |
| C14 | "Physics calibrated — model anchored to eROT + peer-reviewed rectifier data" (deck s.15) | asserted | the κ calibration used one eROT point and a mis-cited MMR point | "model validated against the analytic quarter car and the published 100–400 W supply; AKS numbers pending bench" |
| C15 | "The only patented art known that will solve these problems by charging a vehicle while in motion" (Sept deck) | unsupported | Schenavar 1977, Hyundai 2016, Levant 2014, Zuo lineage (04_prior_art) | "a patented arrangement built around the spring rather than the damper" (Blueprint wording) |
| C16 | "THE COIL SPRING — 5% of the kinetic pool" (Sept deck) | unsupported | no derivation; F1 | drop |
| C17 | "30–100 W average electrical per corner (ISO C, 45–65 mph); 70–175 W (ISO D); 4–20 W (A/B); 600–1000 W sustained peak rating" (Diligence Response) | target | supply bounds: 122 W (C, 60 mph), 488 W (D), 8–30 W (A/B) per corner for the mid-size car; exp 001/002 give the modeled share | compare target with exp 002 `best_load.csv`; the ISO D target is feasible against supply only if φ ≥ 0.15–0.35 |
| C18 | "89.3% of the elastic energy exchange in the bias stage" (Diligence Response §2) | asserted (true statement, wrong implication) | static partition k_m/(k_m+k_b) is correct for stored energy; not a harvest fraction (01_physics §2) | "the bias spring stores most of the stack's elastic energy at any instant; the fraction harvested is a separate, measured quantity φ_s" |
| C19 | "Energy exchanged per stroke ≈ corner force × stroke ≈ 109 J per inch → 97–195 W mechanical" (Diligence Response §2) | unsupported | static preload does no net work over a cycle; the supply theorem bounds the mean | drop |
| C20 | "297.5 hp ≈ 221.9 kW per corner transmission capacity" (Diligence Response §1) | unsupported | treats a static 625 lb load as 625 lb·ft of torque; dimensionally meaningless | drop; state the sprag torque capacity from the component-sizing report instead |
| C21 | "End-to-end 65–80% target with PM generator; 41–54% with claw-pole" (Diligence Response §3) | target | stage efficiencies plausible; η_chain in the model is a parameter (0.85 default) pending the PHINIA map | keep as target with the stage table |
| C22 | "Bench prediction: Ebsco articles, 2.0 in preload, ±0.5–1.0 in at 2–3 Hz → 1.7–5.2 W mechanical, 1.2–3.6 W electrical" (Diligence Response §2) | target | `05_bench_protocol.md` re-derives: P̄ = ½ c_gen r² (2πfa)²; the number depends entirely on the load c_gen and ratio r, neither of which the document states | restate as "P = ½ c_gen r² (2πfa)² ; with r = … and c_gen = … this is … W"; the bench measures c_gen r² |
| C23 | "Levant Power measured up to 1 kW per shock on a heavy truck" (one-pager, Borland doc) | asserted | Levant's public claims were vehicle-level and were revised downward repeatedly (military brief §4) | "Levant Power reported several hundred watts to kilowatts at vehicle level on heavy trucks; the claim was later reduced" |
| C24 | Per-vehicle κ table, compact EV 110 W … tank 4.7 kW average (First-Principles §4.5) | unsupported | linear extrapolation from one eROT point; contradicts F1 (weight is not the lever, tire stiffness is) | replace with exp 002/003 tables |
| C25 | "5–25% range extension per year" (Technical Brief §5.4; the brief itself says not to publish) | unsupported | 15–100 W/corner × 4 against 15–30 kW cruise draw is 0.2–2.7% | never publish |
| C26 | "AKS keeps the battery at 100%" (withdrawn in Technical Brief §12.8) | unsupported | — | stay withdrawn |
| C27 | "Harvesting smooths the ride without placing drag on the vehicle" (Sept deck) | asserted → tested | sign of Δa_w from exp 001/002 | state the measured sign and magnitude |
| C28 | Website Blueprint: "roughly 100 W on a good road, 400 W on an average one, 1,600 W on a poor one" (four dampers, mid-size car) | modeled | repo: 30 / 122 / 488 / 1952 W for A/B/C/D at 60 mph; the Blueprint's 100/400/1600 is a B+/C+/D+ reading of the same scaling | keep; add the class and speed |
| C29 | "~14 W per corner from early prototype data (measured)" (kickoff brief) | unsupported until the record is supplied | F4 | do not state until a dated test record exists |

**Summary.** Of 29 claims, 7 are modeled and supportable as worded or with
the suggested wording, 4 are measured-literature anchors (two mis-cited), 4
are targets, 2 are asserted-but-true, and **12 are unsupported**. Every
unsupported claim traces to the same root: treating stored (reactive)
spring energy or static corner load as harvestable power. F1 closes that
root. The replacement numbers are produced by experiments 001–003 and
appended to `06_numbers_ledger.md`.
