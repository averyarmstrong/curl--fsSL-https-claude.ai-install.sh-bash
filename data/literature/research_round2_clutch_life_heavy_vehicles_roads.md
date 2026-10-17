# Research round 2 — clutch life, heavy-vehicle corner data, open road profiles, heavy-vehicle regen numbers

Date: 2026-10-17. Method: web search (standard + extended) only. **Every WebFetch to a primary host failed under the network policy** (formsprag.com, stieberclutch.com, gmn.de, tsubaki.ca, renold.com, rosap.ntl.bts.gov, infopave.fhwa.dot.gov, par.nsf.gov, vtechworks, SAE, MDPI, DOAJ, Zenodo, arXiv, DTIC, hvttforum, TRB, Wikipedia, etc.). Therefore nothing below was read in full text; all quotes are search-engine snippets of the named page.

Grades used:
- **[P]** quote/number appears in a search snippet taken from the primary page (manufacturer catalogue/manual, the paper's own abstract page, the patent text, or a .gov repository page).
- **[S]** number comes from a secondary source (review paper, distributor page, press, forum, textbook mirror) or from a snippet that paraphrases rather than quotes.
- **[NV]** not verified — could not find; stated so.

Where a snippet was explicitly flagged as garbled/misaligned by the search tool, I say so and grade down.

---

## 1. One-way clutch life in oscillatory / indexing duty

### 1(a) Manufacturer rating basis for indexing service

**What manufacturers actually publish.** None of Formsprag, Stieber, GMN, Tsubaki, Renold or Ringspann publishes an L10-style "cycles to failure" rating for sprag or roller freewheels in the material that surfaced. The industry convention is: (1) a nominal/maximum torque per size; (2) an application-type **service factor** (overrunning / indexing / backstop) that multiplies the design torque, with the indexing factor stepped by **indexing rate in strokes/min** and by **index angle**; (3) a **maximum indexing rate** (strokes/min or Hz) per family; (4) a lubrication regime (oil fill level, no EP additives, shorter intervals above ~150 strokes/min). The link between factor and life is stated only qualitatively ("rate of indexing and the desired life").

**Formsprag (Altra).**
- P-956-FC / application sheet, indexing service factors, split at 150 strokes/min [P, but the search tool flagged the table's column alignment as garbled — verify against the PDF]: for "less than 90° or less than 150 strokes/min": **3** for FSR-3 and -5, **2** for FSR 6–16, HPI, FSO and roller design; for "over 150 strokes/min": **4** for FSR-3 and -5, N/A for HPI, **3** for roller design. Source snippets: documents.mrosupply.com/.../p-956-fc_selection_guide.pdf and p-956-fc_application_data_form.pdf.
- Separate application-manual language (P-1052 family, mirrored at ipcd-inc.com and hvhindustrial.com) [P-snippet]: indexing "service factor will range from 2 to 4", tied to "the rate of indexing and the desired life"; "when torsional or linear vibration is present, use an FSO series clutch and increase the service factor at least 50%"; "ramp & roller clutches suit low-to-medium overrunning speeds and indexing, while sprag clutches suit high overrunning speeds and backstopping"; in indexing, "the outer race should be the oscillating member and the inner race the driven member".
- HPI family positioning [P-snippet, Purvis Industries listing quoting Formsprag]: "Formsprag Clutch recommends the use of our HPI series for indexing rates in excess of 150 strokes per minute or indexing angles in excess of 90 deg."
- GFR modular clutch [P-snippet via Rowland Co. and Clutch Engineering distributor pages]: "indexes should not exceed 350 per minute when used in an indexing application."
- FS-100/200/300 service manual P-222-09/10-FC [P-snippet]: "If the clutch is indexing in excess of 150 strokes a minute, oiling may be required at shorter intervals"; indexing clutches to be kept **completely full of oil** (overrunning/backstopping half full); check oil "monthly or every 160 hours"; avoid EP/AW lubricants; "fit key .000/.001 inches tight on width dimension to prevent loosening in indexing service". A second bulletin gives 7/8 full — conflicting; verify per model. HPI-300…700 shipped with Mobil DTE Light oil; oil-chart split at 150 strokes/min (ISO 68 ≤150 spm; ISO 46 class above).
- Rating basis / cycles: **[NV]** — no statement found of the number of engagement cycles behind a Formsprag torque rating.

**Stieber (Altra; sister company to Formsprag).**
- Catalogue selection procedure [P-snippet, meskarrulman.com mirror of Stieber 2008 catalogue]: indexing service factors — **roller type 3.0 for >150 strokes/min, 2.5 for index angle >90° above 100 strokes/min; sprag type 4.0 and 4.0** for the same conditions. The stieberclutch.com "Selection Procedure" page carries the same table (fetch blocked). Application classes: "OC overrunning clutch, IC indexing clutch, BS backstop".
- Stieber HPI described as "specially designed for high speed indexing applications"; FSO oil-lubricated, FSO-GR grease version [P-snippet, altramotion product page].
- Cycle rating basis: **[NV]**.

**GMN (Germany/USA).**
- GMN "Freewheels service life" page (gmn.de/en/?p=5564) [P-snippet]: "The constant friction contact of sprags with connecting parts during idle operation causes material wear"; "Torque-dependent distortion forces (Hertz pressures) act on relevant freewheel clutch components during indexing operation and these lead to material fatigue over the long-term. In particular, applications in which there are continuous high indexing frequencies can produce micro-fractures and material chipping." This is the clearest manufacturer statement of the two life-limiting mechanisms (overrunning wear vs indexing Hertzian fatigue).
- GMN "Indexing Clutch" page (gmn.de/en/?p=5571) [P-snippet]: freewheels with **meander springs enable indexing frequencies up to 60 Hz**.
- GMN datasheets list an explicit **"Indexing Frequency"** field [P-snippet]: FN 442 M, FP 463 M, FE 478 M = **60 Hz** (M = with cage/meander spring); FN 437 Z, FP 427 Z = **10 Hz** (Z = individual tension springs). FK 6205 / FK 6304 datasheets exist but the value was cut off in snippets [NV].
- GMN sprag-clutch guide N2 [S-snippet]: sprags "engage after a smaller rotation than rollers"; sprags run on plain cylindrical races and need less radial space; roller ramps need ramped rings.
- No cycle-count basis given [NV].

**Tsubaki.**
- Cam-clutch catalogue selection procedure for indexing [P-snippet, tsubaki.ca catalogue]: "a) Determine the design torque requirement b) Identify the maximum indexing cycles (N) per minute c) Specify the feeding angle"; the product of cycles × feed angle is compared with **20,000 and 50,000** thresholds to select series (MI-S suggested in the higher band); formula A when loads are calculable, formula B otherwise (formulas garbled in snippet).
- MIUS series: "mid-speed indexing applications up to **300 cycles a minute**"; catalogue entries list "maximum indexing rate 300 cpm" for MIUS300–900 [P-snippet]. MZEU datasheet: "contact Tsubaki for indexing applications above **50 cycles per minute**" [P-snippet, GlobalSpec datasheet].
- Cycle-life basis: [NV].

**Renold.**
- SO/SX sprag series [S-snippet, DirectIndustry/Yodify listings]: SO "for overrunning, backstopping and medium duty indexing (up to **150 indexed/minute**)"; SX "designed for medium to heavy indexing applications (over 150 indexes/minute)"; sizes 300–700 "fitted with ARO sprags to resist vibration and high transient torques and overloads".
- Life/rating basis: [NV].

**Ringspann.**
- Catalogue excerpts [P-snippet, DirectIndustry]: FA series "indexing freewheel in installations with low to medium total number of actuations"; FNR roller freewheel shown as indexing freewheel in crank-driven wire feeder; FB sealed sprag series lists "Indexing Freewheel" as an application type. No switching-frequency limit or cycle rating surfaced [NV].

**Generic engineering statement of cycle life (patent background).** US 9,810,272 B1 ("One-way clutch", 2017) background [P-snippet of patent text]: "metal fatigue limits the cycle life of roller-ramp and sprag clutches in high torque uses … cycle lifetimes of current technologies range from **a few hundred thousand to a few million high torque cycles**", attributed to shallow ramp/strut angles concentrating load at narrow line contacts. Treat as an interested party's characterisation, not a test result.

**Aerospace endurance precedent.** Avco Lycoming, USAAMRDL TR-72-49 (DTIC AD0747807, 1972) [S — DTIC OCR snippet, fetch blocked]: sprag clutch evaluation at 26,500 rpm / 1,500 hp; test list includes a "static cyclic torque fatigue test at 7,140 ± 900 in-lb" for a cycle count the OCR renders as "10'" (plausibly 10^6; **unconfirmed**); "design A had several failings and needed redesign; design B completed all tests". FAA AD in Federal Register 62 FR 148 (1997) cites "six occurrences of prematurely worn sprag clutches" (field wear evidence, no count) [S].

**Practical reading for the Gate.** At a suspension-relevant engagement rate of 1–3 Hz per clutch (60–180 engagements/min), the Gate sits exactly at the 150 strokes/min threshold where every manufacturer steps the service factor up (×3–4) and moves you to a dedicated indexing family (HPI / SX / MIUS / GMN-M). At 10–15 Hz (600–900 strokes/min) you exceed every published strokes/min limit found (350/min GFR, 300 cpm MIUS, 150/min SO) except GMN's 60 Hz meander-spring units. A 1e7-cycle target (project durability gate) is 10× above the "few million high torque cycles" generic figure — but note that figure is for *rated-torque* cycles; a Gate clutch sized with service factor 4 runs at ≤25 % of rated torque, and Hertzian fatigue life scales steeply (rolling-contact exponents of ~3–10 on load are standard; no sprag-specific exponent was found [NV]).

### 1(b) Published endurance of MMR harvesters

- **Zuo group retrofit MMR shock (Li, Zuo et al., IEEE TVT 62(3) 2013; Li's Stony Brook thesis)** [S/P-snippets]: road test on a Chevrolet Suburban replacing the left-rear shock; **15.4 W average at 15 mph** on the campus loop (slide deck) and **68 W peak / ~19 W average at 30 mph (48 km/h)** on "a fairly smooth campus road"; ">60 % efficiency at high frequency"; reliability language is limited to "utilizing a roller to guide the rack and preload on the gear transmission to reduce the backlash and friction" and "the ball screw is more reliable than rack pinion mechanism". **No endurance cycle count, no clutch-failure report found** [NV].
- **Zuo/Pan/Lin railroad MMR (Applied Energy 247 (2019) 309–321, Pan, Lin, Qian, Liu, Yu, J. Zuo, L. Zuo)** [P-snippet of abstract page]: ball-screw MMR with "embedded one-way clutches in the bevel gears"; field averages **1.12 W and 2.24 W** for a Type-A rapid-transit vehicle at **30 km/h**. Earlier Applied Energy 2018 rack-pinion track harvester: **7 W average / 56 W peak** at 64 km/h freight, 5.7 mm deflection [S]. Durability/clutch wear: not in abstracts [NV].
- **Ahmadian (Virginia Tech CVeSS) railroad work**: USDOT final report "Energy Harvester Tie for Serving the Needs of the Railroad Industry to Access Electric Power in Remote Locations" (Ahmadian & Pan, May 2024, grant 69A3551747132; rosap.ntl.bts.gov/view/dot/78527) [P-snippet of abstract]: "mechanical motion rectifier with an embedded one-way clutch in the bevel gears"; "ball-screw mechanism has reduced backlash". AAR/TTCI Technology Digest TD-14-028 (2014, D5-spring freight-car harvester) [P-snippet]: FAST (Pueblo) field output "about 1 to 2 W"; design "reliable and could be operated in conditions representative of revenue service without any significant problems". Press (Railway Age) quote: "15 to 20 watts of power" per passing wheel for the tie harvester (Norfolk Southern deployment) [S]. **No clutch life or failure quantification found** [NV].
- **Backpack MMR (Zuo group)** [S-snippets]: SPIE 10168 (2017) MMR backpack, 4.8 W max average / 12.8 W instant at 3.5 mph; Applied Energy 279 (2020) half-wave rack-pinion + one-way clutch, ~2× average power vs full-wave; bench 2.1 W at 2 Hz / 6 mm / 31.8 kg. No endurance data [NV].
- **Ocean-wave MMR PTO (Yang, Huang, Mi, Hajj, Bacelli, Zuo, Renewable Energy 2024)** — citation only; no durability data surfaced [NV].
- **Independent one-way-clutch accelerated-life bench**: Dutt, Joshi, Shah, Soni, Prajapati, "Experimental investigation of fatigue for one way power transmission clutches using accelerated life tests", *Results in Engineering* 22 (2024) 102136 [P-snippet of abstract]: a bench "to simulate one-way torque transmission … so their fatigue life can be estimated from accelerated load tests". Numbers not in snippet [NV]; worth obtaining — it is the only recent open-access OWC fatigue test found.
- **Southampton thesis (eprints.soton.ac.uk/447970)**: MMR regenerative shock with sprag clutch tested on hydraulic Instron; no failure cycles in abstract [NV].

**Bottom line for 1(b):** there is no published endurance (cycles-to-failure or hours-to-failure) test of any MMR harvester clutch in the open literature that this search could find. The strongest available field-reliability statement is AAR TD-14-028's qualitative "no significant problems" [P-snippet]. The project's #1 kill risk remains unquantified by precedent; the bench pre-registration should plan to generate this data.

### 1(c) Sprag vs roller-ramp vs ratchet-pawl at 1–15 Hz

No source directly compares the three for 1–15 Hz engagement duty [NV]. Qualitative statements found:
- Sprag: more load-bearing elements, wear spread along race rather than one contact (US 5,070,978) [P-snippet]; smallest engagement rotation (GMN) [S]; overrun wear from sliding contact (GMN service-life page; multiple patents) [P/S]; a JP/US sprag patent reports conventional sprags "readily cause a locking failure due to high-frequency (e.g., 160-Hz) slight variations in angular velocity" [P-snippet].
- Roller-ramp: tolerates more race eccentricity and costs less (US 4,828,085) [P-snippet]; Formsprag/Stieber indexing service factors are *lower* for roller than sprag (2–3 vs 3–4) [P-snippet], and Formsprag's manual pairs "ramp & roller" with "indexing" and sprags with "high overrunning speeds and backstopping" [P-snippet] — i.e., the sister companies steer indexing duty toward rollers at a given torque, contrary to the common assumption that sprags are always better for indexing.
- Ratchet-pawl: "simplest and cheapest … less suited to high-speed, quiet operation" (Cross+Morse catalogue) [S]; "uneven load distribution … heavy wear … impact stress can fracture races" (US 6,997,295) [P-snippet]; "considerable backlash on engagement" (US 8,210,331) [P-snippet]; pawls "let some reverse rotation occur before they engage" [P-snippet].
- Automotive one-way clutches (torque-converter stators, starter clutches) run tens of millions of overrun hours but relatively few torque engagements — their life data (e.g., Chesney & Kremer race-stress work, SAE 960723/970682/981092) is for that duty, not for continuous indexing [S].

### 1(d) Sprag wear / Hertzian fatigue models

- **Chesney & Kremer, "Generalized Equations for Sprag One-Way Clutch Analysis and Design", SAE 981092 (1998)** [P-snippet of SAE abstract page]: covers "theory of operation, equilibrium equations, system deflections, system stresses, and dynamic behavior"; companion roller paper SAE 970682 (1997) in dimensionless form; **"Verification of the One-Way Clutch Race Stress Equation", SAE 960723** is the race-stress validation. The abstract does not mention fatigue life; the papers give Hertz line-contact stress, which you must pair with a separate rolling-contact-fatigue law [NV whether any life equation is inside].
- **Xu & Lowen, "A Mathematical Model of an Over-running Sprag Clutch", Mech. Mach. Theory 29(1) 1994, 11–23** [S, citation confirmed via reference lists]: dynamic engagement model; wear content unconfirmed [NV].
- **Vernay, Ferraris et al., "Transient behaviour of a sprag-type over-running clutch: an experimental study", J. Sound Vib. 248(3) 2001, 567–572** [S]: experimental transient engagement; no life data claimed.
- **Chinese sprag wear/fatigue literature** [S-snippets]: "Research on the Failure Judgment of Sprag Clutch Based on Wear Loss", Appl. Mech. Mater. 378 (2013) 329 — proposes a wear-limit failure criterion; a 2023 MDPI *Applied Sciences* 13(21) 11718 review summarises "Qing et al. established the wear formula by an analytical method and proposed the failure criterion method of the wear limit value for wedge and ring wear caused by cyclic contact force" and "Liu et al. built a sprag-clutch model using Hertz contact theory that accounts for wedge centrifugal force and ring eccentricity"; Atlantis Press MME-16 (2017) "Effect Analysis of Geometry and Load Parameters on Contact Stiffness of Sprag One-way Clutch" (Hertz wedge–raceway contact model); Central South Univ. J. (2015) "logarithmic spiral type sprag" — strut angle dominates engagement dynamics. None gives a cycles-to-failure number in snippets [NV].
- **Fretting / false brinelling analogy**: standard bearing literature (NSK, STLE 2023) describes false brinelling from "very low-amplitude oscillation between rolling elements and raceways" [S]. No source applies it to sprags [NV] — but a Gate clutch that *overruns* a few degrees at 1–3 Hz with light drag is mechanically similar, and this failure mode (lubricant starvation at a small-amplitude contact) is worth listing explicitly in the FMEA.

**What can be cited with confidence:** manufacturer service-factor steps at 150 strokes/min (Formsprag/Stieber/Renold); max indexing rates (GFR 350/min, MIUS 300 cpm, MZEU 50 cpm, GMN 60 Hz/10 Hz); GMN's two-mechanism life statement; US 9,810,272's "few hundred thousand to a few million" cycles; existence and scope of SAE 981092/970682/960723.
**What cannot:** any cycles-to-failure figure for a sprag/roller clutch in reciprocating duty; any MMR harvester clutch endurance result; any 1–15 Hz three-way clutch-type comparison.

### Numbers table — Section 1

| Value | Units | Conditions | Source | Grade |
|---|---|---|---|---|
| 150 | strokes/min | threshold above which Formsprag moves to HPI and raises service factor; Renold SO→SX split | Formsprag P-956 (via Purvis/MROSupply snippets); Renold listings | P / S |
| 2 (FSR 6–16, HPI, FSO, roller); 3 (FSR-3,-5) | service factor | indexing <90° or <150 spm | Formsprag P-956 application sheet | P (table alignment flagged garbled) |
| 3 (roller); 4 (FSR-3,-5); N/A (HPI) | service factor | indexing >150 spm | Formsprag P-956 | P (same caveat) |
| 3.0 roller / 4.0 sprag | service factor | indexing >150 strokes/min | Stieber catalogue 2008 | P |
| 2.5 roller / 4.0 sprag | service factor | index angle >90°, >100 strokes/min | Stieber catalogue 2008 | P |
| 2–4 | service factor | indexing, "depends on rate of indexing and desired life" | Formsprag application manual (P-1052 family) | P-snippet |
| +50 % | service factor increase | torsional/linear vibration present (use FSO) | Formsprag application manual | P-snippet |
| 350 | indexes/min max | Formsprag GFR modular clutch | Rowland / Clutch Engineering distributor pages | S |
| 300 | cycles/min max | Tsubaki MIUS series | tsubaki catalogue entries | P |
| 50 | cycles/min | Tsubaki MZEU: "contact Tsubaki above" | GlobalSpec datasheet | P |
| 20,000 / 50,000 | cycles/min × feed-angle(°) | Tsubaki series-selection thresholds | tsubaki.ca catalogue | P (formula text garbled) |
| 60 | Hz | GMN indexing frequency, meander-spring (M) types; FN442M, FP463M, FE478M | GMN datasheets / gmn.de indexing page | P |
| 10 | Hz | GMN indexing frequency, tension-spring (Z) types; FN437Z, FP427Z | GMN datasheets | P |
| completely full (one bulletin: 7/8) | oil fill | Formsprag FS indexing service; check monthly/160 h | Formsprag P-222 manual | P (conflict noted) |
| few 10^5 – few 10^6 | high-torque cycles | roller-ramp & sprag clutch cycle life, generic | US 9,810,272 B1 background | P-snippet (interested party) |
| 7,140 ± 900 | in-lb | static cyclic torque fatigue test, helicopter sprag clutch, cycles "10'" (unreadable) | USAAMRDL TR-72-49 | S (OCR) |
| 15.4 | W avg | MMR shock, Suburban, 15 mph campus loop | Zuo group slides | S |
| 68 / 19 | W peak / avg | same, 30 mph (48 km/h) smooth campus road | Li, Zuo et al. IEEE TVT 2013 | P-snippet |
| 1.12 / 2.24 | W avg | railroad ball-screw MMR, Type-A transit car, 30 km/h | Pan et al., Appl. Energy 247 (2019) | P-snippet |
| 7 / 56 | W avg / peak | track harvester, freight 64 km/h, 5.7 mm deflection | Appl. Energy 2018 (Zuo group) | S |
| 1–2 | W | D5-spring freight-car harvester at FAST; "no significant problems" | AAR TD-14-028 (2014) | P-snippet |
| 15–20 | W per passing wheel | VT energy-harvesting tie, NS deployment | Railway Age (press) | S |
| — | — | cycles-to-failure of any MMR clutch | — | NV |

---

## 2. Heavy-vehicle tire vertical stiffness and corner data

### 2(a) Truck tire vertical stiffness

- **Wong, *Theory of Ground Vehicles*, truck-tire stiffness table (Table 1.x; mirrored at wanderlodgegurus.com "Theory of Pneumatic Tires part 5")** [S — textbook mirror]: "Michelin Radial 11R22.5 XZA (1/3 tread)" **874 kN/m (4,992 lb/in)**; four 11R22.5 XZA measurements span **≈809–874 kN/m (4,620–4,990 lb/in)**; overall tested truck-tire range **4,363–5,850 lb/in (≈764–1,025 kN/m)**; "at rated loads and inflation pressures, rolling at relatively low speed". Original data are from UMTRI flat-bed work (Tielking, Fancher & Wild, SAE 730183 "Mechanical Properties of Truck Tires", 1973) [S].
- **HVTT17 (2023) PBS paper, Bucko et al.** [P-snippet]: "Tyre stiffness, per tyre, kN/m; Duals **800**; Singles with offset wheels **914**" for 275/70R22.5 duals and 385/55R22.5 singles (load condition not stated).
- **MDPI *Actuators* 11(1):12 (2022), tractor-semitrailer air-suspension study** [P-snippet]: tractor tire stiffness **980,000 N/m** (per tire or per side not stated); tractor leaf-spring stiffness 1,400,000 N/m. A mirror of the same paper gives per-axle rear-tandem tire stiffness ≈**1.96 MN/m** (= 2 × 980 kN/m, consistent with duals) and front damping **15,000–30,000 N·s/m** [S].
- **Wits (South Africa) thesis, "Characterising the stiffness and hysteresis of single and dual truck tyres"** [P-snippet]: dual 315/80R22.5 set loading stiffness **2.550 kN/mm** (= 2.55 MN/m per dual pair ⇒ ≈1.28 MN/m per tire; unloading value truncated); single 385/65R22.5 lower.
- **Tielking, "Conventional and wide base radial truck tyres" (HVTT)** [S]: load–deflection for single 11R22.5 given graphically; spring rate "influenced by inflation pressure but essentially constant over the operating load range".
- Heavy-truck quarter-car in arXiv 1411.3305 uses **500,000 N/m** tire stiffness (2,250 kg sprung / 200 kg unsprung) — a modelling assumption, not a measurement [S].
- 295/75R22.5 specifically: **no measured stiffness found** [NV]. Manufacturer data for scaling: Firestone FS507 Plus 295/75R22.5 — max single 7,160 lb, max dual 6,610 lb at 123 psi (850 kPa), static loaded radius 18.8 in (478 mm) [P-snippet]; overall diameter ≈40 in. A load/deflection estimate from SLR vs unloaded radius (≈20.0 − 18.8 = 1.2 in at 7,160 lb ⇒ ≈6,000 lb/in secant) is an *inference*, not a source value.

Working recommendation for params.yaml: per-tire k_t = **850 kN/m [LITERATURE: Wong/UMTRI 11R22.5 XZA 809–874 kN/m; HVTT17 800 kN/m]**, range 760–1,000 kN/m; dual station 1.6–2.0 MN/m. Flag 295/75R22.5 as [ASSUMPTION: same class as 11R22.5].

### 2(b) Class 8 drive-axle unsprung mass, air-spring rate, damping

- **Unsprung mass**: MDPI Actuators 2022 model: tractor axles 2 & 3 **≈785 kg each**, semitrailer axles **≈750 kg** [S — mirror snippet]; six-axle tractor-semitrailer rollover study (ResearchGate): unsprung masses **640, 1,150, 780 kg**, suspension stiffness **250, 1,400, 2,500 kN/m**, damping **15, 30, 30 kN·s/m** by axle group [S]; arXiv 2009.00701 three-axle truck (after Wang et al.): front unsprung **900 kg**, k = 610 kN/m, c = 15.4 kN·s/m; middle/rear unsprung **1,400 kg**, k = 2,600 kN/m (rear damping not in snippet) [S]. TRB Record 1215 (1989) gives half-truck/semitrailer parameter sets in imperial units (numbers garbled in snippet) [NV].
- **Air-spring effective rate**: no measured drive-axle kN/m value surfaced [NV]. Leads: Luque & Mantaras (2003) dynamic air-spring rate vs pressure and length; SAE 931693 (1993) leaf vs air tandem characterisation on a road simulator; MDPI Actuators 2022 treats air-spring stiffness as nonlinear and leaf as constant [S]. Suspension-assembly weights (Hendrickson HTB 570 lb incl. brackets; Kenworth AG380 ~650 lb installed) are published but are *not* unsprung masses [P-snippet].
- **Damping**: 15–30 kN·s/m per axle is the recurring modelling range above [S]; no measured shock curve found [NV].

### 2(c) Military

- **HMMWV quarter-car (MR-damper study, ResearchGate "Study of a quarter model HMMWV suspension system using a magnetorheological fluid damper")** [S — parameter table quoted in snippet]: sprung **905 kg**, unsprung **181 kg**, tire stiffness **463,800 N/m** ("rear tire stiffness modeled by four identical springs … in parallel" — ambiguous whether 463.8 kN/m is the total), suspension stiffness **163,300 N/m**, OEM damper extension **27,160 N·s/m**.
- HMMWV coil springs (forum, steelsoldiers.com) [S, weak]: front springs "rated 954 lb without winch / 1,250 lb with winch"; a replacement is "~30 % (750 lb) softer". Whether these are lb/in rates or load ratings is not stated — treat as [NV].
- HMMWV wheel travel, 37×12.5R16.5 tire stiffness, TM 9-2320-280 spring data: **[NV]** (TM not reachable; GlobalSecurity gives 16 in loaded ground clearance, curb 7,700 lb for M998/M1035/M1038 — a conflicting 5,200 lb figure appears in an AI-generated page and should be ignored).
- **M-ATV / TAK-4**: Oshkosh states ">16 inches of independent wheel travel" for M-ATV; TAK-4i "20 inches" [P-snippet of Oshkosh/press]; spring rates **[NV]**.

### 2(d) F-150

- Front coil rates (forum/parts compilations, 2009–2018 trucks): **314–633 lb/in** by GAWR; e.g., 433 lb/in at 3,225–3,300 lb FGAWR; 513 lb/in at 3,600 lb [S]. Rear leaf rates: **[NV]** (only load capacities 1,600–1,900 lb listed). Unsprung mass, 275/65R18 stiffness: **[NV]**. Generic LT-tire stiffness is not a substitute; keep as [ASSUMPTION] with an explicit sensitivity band.

### Numbers table — Section 2

| Value | Units | Conditions | Source | Grade |
|---|---|---|---|---|
| 874 (4,992) | kN/m (lb/in) | Michelin 11R22.5 XZA, rated load & pressure, slow rolling | Wong, Theory of Ground Vehicles (UMTRI/SAE 730183 data) | S |
| 809–874 (4,620–4,990) | kN/m (lb/in) | four 11R22.5 XZA tests | same | S |
| 764–1,025 (4,363–5,850) | kN/m (lb/in) | range of all truck tires in table | same | S |
| 800 / 914 | kN/m per tyre | 275/70R22.5 duals / 385/55R22.5 singles | HVTT17 Bucko et al. 2023 | P |
| 980,000 | N/m | tractor tyre stiffness (model input) | MDPI Actuators 11(1):12, 2022 | P |
| 2.550 | kN/mm (loading) | dual 315/80R22.5 pair | Wits thesis | P |
| 7,160 / 6,610; 123 (850); 18.8 (478) | lb single / lb dual; psi (kPa); in (mm) SLR | Firestone FS507+ 295/75R22.5 | Firestone product page | P |
| 785 | kg | tractor axle 2 & 3 unsprung (model) | MDPI Actuators 2022 (mirror) | S |
| 640 / 1,150 / 780 | kg | unsprung by axle group, 6-axle tractor-semi | ResearchGate rollover study | S |
| 250 / 1,400 / 2,500 | kN/m | suspension stiffness by axle group | same | S |
| 15 / 30 / 30 | kN·s/m | damping by axle group | same | S |
| 900 / 1,400 | kg | 3-axle truck front / rear unsprung | arXiv 2009.00701 (after Wang et al.) | S |
| 610 / 2,600 | kN/m | 3-axle truck front / rear suspension stiffness | same | S |
| 15.4 | kN·s/m | front damping | same | S |
| 905 / 181 | kg | HMMWV quarter-car sprung / unsprung | MR-damper HMMWV paper | S |
| 463,800 / 163,300 | N/m | HMMWV tire / suspension stiffness (quarter model) | same | S |
| 27,160 | N·s/m | HMMWV OEM damper, extension | same | S |
| >16; 20 | in | M-ATV TAK-4 wheel travel; TAK-4i | Oshkosh statements | P-snippet |
| 314–633 | lb/in | F-150 front coil rates by GAWR | forums/parts sites | S (weak) |
| — | — | 295/75R22.5 k_t; air-spring kN/m; HMMWV travel & tire k; F-150 rear leaf, unsprung | — | NV |

---

## 3. Measured road profiles — open datasets

### FHWA LTPP InfoPave
- **Formats** (InfoPave AIMS storage standards pages, AIMS__2026-8-01-*) [P-snippet]: "Longitudinal profile data for LTPP Sections are provided in **ERD file format v2.0**"; a second AIMS set holds "as collected longitudinal profile data in **binary format … output from ProQual**"; "Longitudinal profile data collected over LTPP sections at **150 mm intervals** by profilers or by using a Dipstick"; "25 mm laser profile files are also included … only for equipment newer than the DNC-690". Older directive: "RSCs shall convert raw profiles to the *.ERD format"; ERD developed by UMTRI. Ancillary profile files are zipped per section (e.g., "PRF_LPF" package) [P-snippet].
- **Login**: TAC (Canada) page on C-LTPP in InfoPave [P-snippet]: "registered users must sign in to access the data, and there is no cost to register or to access the data." FHWA-HRT-18-011 describes "Data Selection and Download" as the primary extraction path and a full Standard Data Release (SDR) download for database users [P-snippet]. So: **free, but registration/sign-in required**; no evidence of anonymous bulk profile download [NV whether individual AIMS zips are anonymous]. data.gov lists the LTPP dataset and its Tools but points back to InfoPave [S].
- **Units**: ERD v2.0 headers carry units; LTPP profiles are elevation in mm (or in) at 150 mm (6 in) spacing for the SDR-era data, 25 mm for newer laser systems [P-snippet for spacing; units [S]].
- SDR tables (MON_PROFILE_MASTER etc.) hold IRI/summary statistics, not raw elevations; raw elevations live in AIMS [S].

### ERD / PPF format documentation
- UMTRI-97-51, "ERD file format for storage and analysis of road profiles" (Sayers), reproduces Appendix A of the RoadRuf manual; also indexed at core.ac.uk and SWOV [P-snippet]. Format: text header + data block (text or separate .BIN) [S, fileinfo.com].
- ProVAL (Transtec, roadprofile.com; FHWA-funded, free): native **.PPF**; imports ERD, TxDOT, K.J. Law, Ames .adf; MDOT (Mississippi) accepts .erd, .ppf, .adf [P-snippet of MDOT guide]. Whether sample .ppf files ship with the installer: **[NV]** (MDOT user guide "uses specific files in each example" — suggests example files exist but source not located).
- "The Little Book of Profiling", 2nd ed. (Karamihas & Sayers, 2025) on UMich Deep Blue [P-snippet]; sample data not confirmed [NV].

### Other open sources
- **MnROAD** (MnDOT) [P-snippet]: performance data served through InfoPave's MnROAD portal (infopave.fhwa.dot.gov/Mnroad); MnDOT states "raw ride quality … is stored offline and available on request" (contact Ben Worel, MnDOT); InfoPave ALPS ride data "averaged between the two wheel paths". So raw per-wheelpath profiles = on request, not open download.
- **Zenodo 17202006 / 17232645 "Benchmark vehicle suspension data based on ISO 8608 road profiles"** (CC BY 4.0; companion paper in *Control Engineering Practice* 2025, DOI 10.5281/zenodo.17242919) [P-snippet]: ~40 MB `suspension_dataset.mat` with body/tyre displacements for ISO classes A–E — **synthetic** ISO 8608 inputs, not measured roads.
- **Zenodo 13236902** "Road-Profile-Generation-by-ISO-8608" (MATLAB generator, GitHub source) — generator, not data [P-snippet].
- Kaggle "road roughness" datasets: nothing with longitudinal elevation profiles surfaced; typical Kaggle items are smartphone-accelerometer/IRI classification sets [NV].
- ISO 8608:2016 is a paid standard (~US$241) and contains the PSD classification method, not example profile files [S].
- Zenodo "Measured profiles and run-up dataset" (15178956) is coastal beach profiles — not roads (listed to prevent a false lead) [P-snippet].

**Recommendation:** register (free) on InfoPave, pull a handful of GPS/SPS sections' ERD files (150 mm spacing, mm elevation) spanning IRI ≈ 1–4 m/km, and use them as measured counterparts to the synthetic ISO 8608 A–D inputs. Document in the lab notebook that profiler data are high-pass filtered (long-wavelength content >~100 m is attenuated), which matters little at 1–15 Hz body/axle frequencies but should be stated.

### Numbers table — Section 3

| Value | Units | Conditions | Source | Grade |
|---|---|---|---|---|
| 150 | mm | LTPP profile sample interval (profiler or Dipstick) | InfoPave AIMS standards page | P |
| 25 | mm | laser profile files, equipment newer than DNC-690 | InfoPave directive | P |
| ERD v2.0; ProQual binary; PRF_LPF zips | format | LTPP AIMS longitudinal profile | InfoPave AIMS pages | P |
| free, sign-in required | access | InfoPave data download | TAC C-LTPP page; FHWA-HRT-18-011 | P-snippet |
| .ppf (native), .erd, .adf, TxDOT, KJ Law | formats | ProVAL import/export | FHWA ProVAL brief; MDOT guide | P |
| on request (offline) | access | MnROAD raw ride/profile data | MnDOT MnROAD data page | P |
| ~40 MB .mat, CC BY 4.0 | dataset | ISO 8608 synthetic classes A–E + suspension responses | Zenodo 17202006/17232645 | P |
| — | — | anonymous (no-login) LTPP raw profile download; ProVAL sample .ppf | — | NV |

---

## 4. Regenerative-suspension field numbers for heavy trucks, buses, military (2010–2026)

**Headline finding:** no peer-reviewed *measured* per-corner harvested-power figure for a Class 8 truck, transit bus or military vehicle on the road was found in the open literature. What exists is (i) one industry SAE paper with Class 8 measurements behind a paywall, (ii) press/company claims, (iii) simulations.

### Measured or semi-measured
- **Mossberg, Anderson, Tucker (Levant Power / Jacobs Vehicle Systems), "Recovering Energy from Shock Absorber Motion on Heavy Duty Commercial Vehicles", SAE 2012-01-0814** [P-snippet of SAE abstract]: two GenShock prototype generations built and tested; suspension motion "sampled on a highway route (I-75, Detroit to Toledo)" and fed into a system model; on a test Class 8 truck "reduced alternator load lowered fuel consumption". **Per-shock watts and the fuel-economy % are in the paywalled body [NV].** Trade press paraphrase: Levant "estimates 3 to 5 percent" fuel economy for Class 8 [S].
- **MIT/Levant press (2009)** [S]: "in a 6-shock heavy truck, each shock absorber could generate up to an average of **1 kW** on a standard road"; first prototype "800 W continuous from four shocks, up to 5 kW over nasty off-road terrain" (Popular Science); Humvee lent by AM General for testing; a later review repeats "1 kW standard roads vs 5 kW rough roads" and "2–5 % fuel saving, up to 6 % military". These are hydraulic-turbine prototypes with instrumented but unpublished tests — grade **S**, and they conflict by an order of magnitude with every physics-based estimate (see below), which the repo should say plainly.
- **Zuo group, passenger-car road tests** (for scale only): 1:2-scale linear harvester **2–8 W** at ~45 mph (2010); MMR retrofit **19 W avg / 68 W peak** at 48 km/h; **15.4 W** at 15 mph (Suburban) [P/S]. Zuo UTRC report: "100–400 W average power is available in the suspensions of a middle-sized passenger car at 60 mph on good and average roads … more … for heavy-duty trucks and off-road vehicles" [P-snippet]; a Stony Brook slide band for buses that the search tool read as "~800 W to 10 kW" is **unverified** [NV].
- **Zhang, Chen, Guo, Zhang, Li, "Electro-hydraulic damper for energy harvesting suspension", Applied Energy 199 (2017) 1–12** (off-road-vehicle target): a snippet from a review attributes "measured average regenerated power **4.9, 17.7, 49.2 and 45.0 W** on A, B, C and D class roads" — the abstract page does not show these numbers; vehicle and speed unknown [S].
- **Railroad (as the only heavy-vehicle *field* MMR data)**: 1.12/2.24 W (transit, 30 km/h), 7 W avg/56 W pk (freight 64 km/h), 1–2 W (FAST, freight-car D5 spring), 15–20 W per wheel pass (tie) — see Section 1 [P/S].
- **Hydro-magneto-electric regenerative shock on a pickup "tested on a bumping road"** (J. Mech. Sci. Technol. 2020, ITS Surabaya) — numbers not in snippet [NV].

### Simulation / analysis (clearly labelled)
- **Abdelkareem et al., *Energy* 173 (2019) 332–351**, class-6 heavy-duty truck, many drive cycles: "**71–434 W** and **287–1,733 W** … for ISO road grades C and D, respectively, for a fully-loaded truck"; another snippet: "an average power of **300 W** can be harvested under road grade D and 60 mph" [P-snippet of abstract].
- **Abdelkareem et al., *Energy* 239 (2022)**, double-sided arm-toothed rotary EM dampers on a full semi-trailer (12 units): truck average **0.33, 1.33, 5.24, 21.3 W** under road classes B, C, D, E at 120 km/h (per damper, simulation; note these are far below the 2019 figures because of the specific damper's characteristics) [P-snippet].
- **Half-truck model** (review-cited): rear/front conventional truck dampers dissipate ≈**95 W / 46 W** at 30 mph (48 km/h) [S].
- Review-cited "Audi analysis: **1 kW** average from six shock absorbers of a heavy-duty truck on general highway" [S — second-hand].
- "Inflatable hydraulic-electric regenerative suspension for heavy-duty vehicles" (2023–24, ride comfort + harvesting) — citation only, numbers [NV].
- **Puliti, Galluzzi, Tessari, Amati, Tonoli, Applied Energy 358 (2024)**: electro-hydrostatic regen shock, measured peak regeneration efficiency **45 %**, simulated ≈101 W per absorber on a class-B *passenger* vehicle — not heavy [P-snippet].
- Bus: Li et al., *Applied Energy* 295 (2021) 117020 "driverless buses" — **bench** 4.25 W avg at 7 mm / 2.5 Hz, η_max 65.0 %, η_avg 39.5 % [P-snippet]; slotted-link bus ERSA, *Applied Energy* 2023 — bench [S]. No bus road test found [NV].
- Military: UT Austin CEM active EM suspension on an Army HMMWV at Yuma (SAE 2000-01-0102) — active, no harvested-power figure [S]; GenShock "defense platforms: a few hundred watts to several kilowatts" — company estimate [S]; TARDEC/GVSC measured data **[NV]**.

**Reading for the Gate:** the only heavy-vehicle *measurement* in the public domain is paywalled (SAE 2012-01-0814) and its headline press numbers (1 kW/shock) are inconsistent with the simulation consensus (tens to a few hundred W per corner on class C–D for a loaded truck at highway speed). The repo's "hundreds of watts per corner on heavy vehicles, kW only under rough duty" framing is consistent with Abdelkareem 2019 and should cite it as the anchor, while explicitly listing the 1 kW claim as unverified.

### Numbers table — Section 4

| Value | Units | Vehicle / road / speed | Source | Grade |
|---|---|---|---|---|
| ~1,000 (avg) ; 5,000 (rough) | W per shock | 6-shock heavy truck, "standard road"; rough road | MIT/Levant press 2009; review | S (unverified claim) |
| 800 cont.; 5,000 peak | W (4 shocks) | early GenShock prototype, off-road | Popular Science 2009 | S |
| measured, numbers paywalled | — | Class 8, I-75 Detroit–Toledo, GenShock | SAE 2012-01-0814 | P (existence) / NV (values) |
| 3–5 | % fuel | Class 8 estimate | Levant via trade press | S |
| 71–434 ; 287–1,733 | W | class-6 truck, fully loaded, ISO C ; ISO D (simulation) | Abdelkareem et al., Energy 173 (2019) | P-snippet |
| ~300 | W | same study, grade D, 60 mph | same | P-snippet |
| 0.33 / 1.33 / 5.24 / 21.3 | W per damper | semi-trailer, 12 rotary EM dampers, ISO B/C/D/E, 120 km/h (simulation) | Abdelkareem et al., Energy 239 (2022) | P-snippet |
| 95 / 46 | W | conventional truck rear / front damper dissipation, 30 mph (model) | review-cited half-truck model | S |
| 1,000 | W per vehicle | 6 shocks, heavy truck, highway (company analysis) | review citing Audi | S |
| 4.9 / 17.7 / 49.2 / 45.0 | W avg | electro-hydraulic damper, roads A/B/C/D (vehicle, speed unknown) | Zhang et al., Appl. Energy 199 (2017) via review | S |
| 100–400 | W | mid-size passenger car, 60 mph, good/average roads (analysis) | Zuo UTRC report | P-snippet |
| 19 / 68 ; 15.4 | W avg/peak ; W avg | passenger SUV, 48 km/h ; 15 mph | Li, Zuo et al. 2013; slides | P / S |
| 4.25 ; 65.0 / 39.5 | W ; % | bus ERSA, bench 7 mm 2.5 Hz; η_max/η_avg | Li et al., Appl. Energy 295 (2021) | P-snippet |
| 45 | % | peak regeneration efficiency, electro-hydrostatic shock (passenger class B) | Puliti et al., Appl. Energy 358 (2024) | P-snippet |
| — | — | any measured bus or military per-corner harvested power on road | — | NV |

---

## Gaps and recommended next actions

1. **Obtain full texts** (from a machine without the proxy restriction or via library): SAE 2012-01-0814 (the only Class 8 measurement); SAE 981092 / 970682 / 960723 (Chesney & Kremer); Results in Engineering 22 (2024) 102136 (OWC accelerated-life bench); USAAMRDL TR-72-49 (sprag cyclic fatigue test); Formsprag P-956-FC and Stieber catalogue selection pages (to clear the garbled-table caveat); UMTRI "Factbook of the Mechanical Properties of the Components for Single-Unit and Articulated Heavy Trucks" (Fancher et al., UMTRI-86-12) for tire spring rates and unsprung masses; SAE 931693 for air-spring tandem rates.
2. **Clutch life** cannot be closed from literature; the bench pre-registration should include a dedicated clutch-only endurance leg (e.g., 1e6 engagements at the Gate's rated torque fraction, inspecting race Hertzian spalling and sprag face wear) because no published MMR endurance exists to lean on.
3. **params.yaml provenance**: tire stiffness → [LITERATURE] (Wong/UMTRI, HVTT17); Class 8 unsprung/damping → [LITERATURE] (model tables above, flagged as modelling values); HMMWV → [LITERATURE] (MR-damper paper) with tire-stiffness interpretation flagged; 295/75R22.5, air-spring rate, F-150 rear → [ASSUMPTION] with explicit bands.
4. **Road profiles**: register on InfoPave and ingest ERD files (150 mm, mm elevation); note raw MnROAD profiles are by request.
