# Prior-art and reference-data dossier for US 12,409,695 B2 (Armstrong Gate)

Prepared 2026-10-17 for the gate-twin repo. Scope: thirteen items requested (prior-art documents, anchor papers, catalog data, standards tables), each with citation, disclosure summary, quantitative content, and a claim-element comparison against the '695 independent/dependent claims as summarised in the task brief.

## 0. Access limitations and evidence grading (read first)

The session's network policy blocked direct fetches of every primary-document host tried: `patents.google.com`, `image-ppubs.uspto.gov`, `patents.justia.com`, `freepatentsonline.com`, `iopscience.iop.org`, `asmedigitalcollection.asme.org`, `ieeexplore.ieee.org`, `sciencedirect.com`, `osti.gov`, `trid.trb.org`, `formsprag.com`, `documents.mrosupply.com`, `jniosh.johas.go.jp`, `pmc.ncbi.nlm.nih.gov`, `arxiv.org`, `wikipedia.org`, `researchgate.net`, `semanticscholar.org`, `phys.org`, `automotiveworld.com`. Only `github.com` resolved. Web search (which returns indexed snippets of those same primary pages) worked.

Consequently every statement below is graded:

- **[S-primary]** text quoted or paraphrased by the search engine directly from the primary document's page (patent full text at USPTO/Justia/Google Patents, publisher abstract page, manufacturer catalog PDF). Reliable for the specific wording returned; not a full read of the document.
- **[S-secondary]** statement from a citing paper, review, or news article found by search.
- **[code]** parameter values read from open-source implementations on GitHub (used only for standards tables; see items 12 and 13).
- **[not verified]** could not be confirmed from any retrieved source. Treat as a to-do, not a fact.

No numbers have been invented. Where the task brief supplied a value that the sources did not confirm, this is stated explicitly.

---

## 1. Li, Zuo, Kuang, Luhrs (2013) — MMR shock absorber, and the related Zuo patent filings

**Citation [S-primary].** Z. Li, L. Zuo, J. Kuang, G. Luhrs, "Energy-harvesting shock absorber with a mechanical motion rectifier," *Smart Materials and Structures* **22**(2), 025008 (2013), DOI 10.1088/0964-1726/22/2/025008. Companion paper: Z. Li, L. Zuo, G. Luhrs, L. Lin, Y. Qin, "Electromagnetic energy-harvesting shock absorbers: design, modeling, and road tests," *IEEE Trans. Veh. Technol.* **62**(3), 2013 [S-secondary, from a citing reference list].

**Mechanism/topology [S-primary + S-secondary].**
- Retrofit telescopic shock absorber replacing the hydraulic damper; it is therefore a **damper in parallel with the main suspension spring** (not in series with it), acting on the full suspension stroke.
- Rack-and-pinion converts stroke to rotation; the pinion shaft carries **two one-way roller clutches**, each driving a large bevel gear; a third (small) bevel gear on the generator shaft is driven by whichever large bevel gear is currently engaged, so the generator always spins one way. Search snippet from a citing review: "a pair of rack and pinion, one shaft and three bevel gears. Because of the one-way roller clutches, at an instant only one large bevel gear is engaged and driven by the shaft." [S-secondary]
- The authors state the earlier (non-rectified) prototype had rack teeth "worn out and broken quickly due to large impact forces"; the MMR was introduced to remove the impact of direction reversal and to let the generator freewheel through velocity zero-crossings (generator inertia acts as a flywheel; the paper refers to this as the "disengagement" phase) [S-secondary].
- Generator: rotary DC/PM generator with internal resistance 6.6 Ω [S-primary, abstract/body snippet].
- Gear ratio / pinion pitch radius / bevel ratio: **[not verified]** from retrieved text. The ratio was not visible in any snippet.

**Quantitative results.**
- ">60% efficiency at high frequency" (abstract) [S-primary].
- Bench: at **1.5 Hz, 5 mm amplitude** mechanical efficiency ≈ 60%, levelling off at ≈ 62% at higher frequencies [S-primary, body snippet].
- Electrical efficiency 82–94% for external load R_e = 30–100 Ω [S-primary].
- Bench: at **3 Hz, 5 mm amplitude**, average electrical power **40.4 W and 25.6 W** for the two loads [S-primary]. Load values differ between versions: the IOP text describes external resistors of 30 Ω and 100 Ω (total circuit 36.6 Ω and 106.6 Ω with the 6.6 Ω internal resistance); a ResearchGate copy was reported as listing 23.4 Ω and 94.6 Ω. The task brief's "23.4 and 93.4 Ω" was not found verbatim. Record the condition as "3 Hz / 5 mm, external load ≈ 23–30 Ω and ≈ 94–100 Ω" until the PDF is read.
- Road test: "more than 15 W" at 15 mph on a smooth paved road (abstract) [S-primary]; a presentation on the same work gives 15.4 W average on a loop at Stony Brook in a Chevrolet Suburban [S-secondary].

**Important note for the repo's V2 gate.** CLAUDE.md states the V2 anchor as "~40 W @ 0.047 m/s RMS". The sources tie the 40.4 W figure to **3 Hz / 5 mm**, whose peak velocity is 2π·3·0.005 = 0.094 m/s (RMS 0.067 m/s for a sinusoid). The value 0.047 m/s equals the **peak** velocity at **1.5 Hz / 5 mm** (2π·1.5·0.005 = 0.0471 m/s), which is the condition quoted for the ~60% mechanical efficiency, not for 40 W. Either the gate's velocity label or its power target should be corrected after reading the paper's figure captions (expected: Fig. 12–14 region of the IOP paper; page numbers not verified).

**Related Zuo patents [mostly not verified].** Retrieved references cite only provisional filings: US 61/368,846 (2010, "Regenerative shock absorbers with high energy density," Zuo, Tang, Zhang) and US 61/476,019 (2011, "High-efficiency energy generator for harnessing mechanical vibration power," Zuo, Penamalli, Wang et al.) [S-secondary]. Neither "US 2013/0127175" nor "US 9,118,487" could be confirmed as a Zuo/Li MMR document from any retrieved source; Justia's Zuo inventor page surfaced a later grant, US 12,088,180 ("kinetic energy-harvesting device using a half-wave mechanical motion rectification mechanism," pub. 2022/0337124) [S-primary snippet, assignee not confirmed]. **Do not cite US 9,118,487 or US 2013/0127175 as Zuo MMR patents until checked.**

**Comparison with '695.**
- Collapsible frame between chassis and suspension: absent (telescopic damper body).
- Biasing spring softer than main spring, in series: absent; the device is parallel to the main spring and has no load-bearing spring of its own.
- Hollow generator shaft with drive rod inserted: absent (rack-pinion plus bevel train; generator shaft is a normal solid shaft).
- Two opposed one-way clutches rectifying both strokes: **present** (two roller clutches on the pinion shaft, opposite senses, both strokes drive the generator one way).
- Flyweights keeping the generator spinning through transition: **partial** — relies on generator rotor inertia (and in later railroad MMR versions an explicit flywheel), not on added fly weights as claimed in '695 claim 8.
- Generator: present (PM DC).
- Drop-in height / heights sum to original spring height: absent.

---

## 2. Zuo & Zhang (2013) — analytic harvestable power, ride comfort, handling

**Citation [S-primary].** L. Zuo, P.-S. Zhang, "Energy harvesting, ride comfort, and road handling of regenerative vehicle suspensions," *ASME J. Vib. Acoust.* **135**(1), 011002 (2013), DOI 10.1115/1.4007562 (paper 011002; some reference lists give pp. 48–65 or the year 2011/2012 for the online version).

**What it does [S-primary abstract].** Quarter-car and full-car models; road irregularity modelled as a stationary random process with the ISO roughness spectrum; the H2 norm is used to obtain the mean generated power; "for a quarter car model, an analytical solution of the mean power is obtained." Headline: "At 60 mph on good and average roads, 100–400 W average power is available in the suspensions of a middle-sized vehicle." Sensitivity statement (abstract): "road roughness, tire stiffness, and vehicle driving speed have great influence on the harvesting power potential, where the suspension stiffness, absorber damping, and vehicle masses are insensitive."

**Closed-form expression: [not verified].** No retrieved snippet contained the equation. Secondary reviews paraphrase it as "proportional to the tire stiffness and road vertical excitation spectrum only" and "independent of all masses and suspension parameters" [S-secondary]. Dimensional note for whoever reads the PDF: with the ISO displacement PSD G_d(n) = G_d(n0)(n/n0)^-2 the ground **velocity** PSD at vehicle speed V is white, 4π²n0²G_d(n0)V (one-sided, (m/s)²/Hz), and a quantity with units of watts that depends only on that spectrum and tire stiffness k_t is proportional to G_d(n0)·V·k_t (m³ · m/s · N/m = W). The expression in the task brief, π G_r v k_t² / (2(m_s+m_u)), does not have units of watts (it carries an extra N/kg·s factor) and should not be used. The repo's PHYSICS.md should carry the equation number from the paper once obtained.

**Vehicle parameters used, exact road classes: [not verified]** (abstract only says "middle-sized vehicle," "good and average roads"; one review renders this as 96 km/h on ISO class B and C roads [S-secondary]).

**Comparison with '695.** This is an analysis paper, not a device: no frame, spring, clutch, shaft, or flyweight elements. Its relevance is as the **road-energy-input ceiling** against which any Gate prediction must be checked (consistent with CLAUDE.md's "binding constraint is road energy input"). One further point: because the paper's quarter-car assumes a parallel damper, its "insensitive to suspension stiffness/damping" conclusion does **not** automatically transfer to a series-spring rectifier like the Gate, whose engaged-mode inertance and softer series spring change the transfer function; the κ shorthand in V4 should be validated against a direct series-topology H2 calculation, not borrowed from this paper.

---

## 3. Hsu (1996) — power recovery of electrical active suspension

**Citation [S-primary, IEEE Xplore record 553393].** P. Hsu, "Power recovery property of electrical active suspension systems," *Proc. 31st Intersociety Energy Conversion Engineering Conference (IECEC 96)*, Washington DC, Aug. 1996, pp. 1899–1904.

**Content [S-primary abstract].** Electric motors as the main actuators of an active suspension; quarter-car model with an LQ optimal controller; estimates that "an active system on a mid-size car can potentially recover up to 100 W per wheel in a highway driving condition," and that the system consumes net power in low-speed city driving. A review cites the case as a GM Impact at 16 m/s (≈ 36 mph, 58 km/h) with ≈ 100 W per suspension [S-secondary]. The task brief's "30 mph" is not supported; 16 m/s is the only speed found.

**Comparison with '695.** Parallel electromagnetic actuator; no collapsible frame, no series biasing spring, no clutches, no flywheel, no hollow shaft. Relevant only as an early per-wheel power magnitude (≈ 100 W class) that agrees with the "hundreds of watts" norm in CLAUDE.md.

---

## 4. Suda, Nakadai, Nakano (1998) — hybrid suspension with skyhook control and energy regeneration

**Citation [S-secondary, consistent across several reference lists].** Y. Suda, S. Nakadai, K. Nakano, "Hybrid suspension system with skyhook control and energy regeneration (development of self-powered active suspension)," *Vehicle System Dynamics* **29**(S1), 619–634 (1998), DOI 10.1080/00423119808969590. Precursor: Y. Suda, T. Shiiba, "A new hybrid suspension system with active control and energy regeneration," *Vehicle System Dynamics* **25**(S1), 641–654 (1996) [S-primary TRID/SWOV record].

**Content.** Abstract fragments [S-secondary]: "all the energy for active control is supplied from a damper which regenerates vibration energy"; proposes a less energy-consuming active control law using the skyhook concept. Reviews describe the hardware as two linear DC motors, one acting as an energy-regenerative damper, the other as the actuator; a frequency-dependent hybrid skyhook law. Numerical values (regenerated watts, test rig parameters): **[not verified]** — no snippet contained them. The ball-screw PM-DC-motor detail that often appears alongside this citation comes from a 2014 Montazeri-Gh & Kavianipour paper, not from Suda 1998.

**Comparison with '695.** Parallel linear electromagnetic devices; no series spring, no clutches, no rectification (electrical rectification only), no flywheel, no hollow shaft. Different class entirely; cite as background on self-powered active suspension.

---

## 5. Karnopp (1989) — PM linear motors as variable dampers

**Citation [S-primary, TRID record].** D. Karnopp, "Permanent magnet linear motors used as variable mechanical dampers for vehicle suspensions," *Vehicle System Dynamics* **18**(4), 187–200 (1989), ISSN 0042-3114.

**Content [S-secondary; TRID has no abstract].** Argues linear electromagnetic dampers for vehicle suspensions are feasible; usable passively or semi-actively (skyhook); assumes a magnetic field constant over travel, under which the damping force depends on velocity and the mass of copper rather than on turns count; force was limited by the permanent magnets available in 1989 (later work notes NdFeB changes this). No power figures retrieved.

**Comparison with '695.** Linear PM damper in parallel with the spring; no clutches, no flywheel, no series frame. Not anticipatory of any '695 element except "an electrical generator in the suspension load path" in the broadest sense.

---

## 6. Levant Power / ClearMotion — US 8,841,786 B2

**Citation [S-primary].** US 8,841,786 B2, "Integrated energy generating damper," inventors Clive Tucker, Ross Wendell, Zackary M. Anderson, Evan Moen, Johannes Schneider, Zachary J. Jackowski, Sean Morton; original assignee Levant Power Corp., current assignee ClearMotion Inc.; application 13/759,467, a continuation of 13/704,138 (filed Dec. 13, 2012, national stage of a PCT filed June 16, 2011); issued **Sep. 23, 2014**. Same specification continues as US 9,035,477; 9,689,382; 10,495,073; 10,655,612; 11,499,535; 12,264,656; EP 3643918 A1; EP 4289640 A2.

**Mechanism [S-primary description snippets].** Telescopic hydraulic damper; piston motion forces fluid from the compression volume (80) through porting (85) into a hydraulic motor (83) — a positive-displacement gerotor — and out (84) into the extension volume (79); the gerotor drives an electric generator immersed in the hydraulic fluid; the generator's back-EMF provides the damping; wiring exits through a hollow piston rod. Family abstract (EP): "an energy recovery device comprising a hydraulic motor comprising a first port and a second port; an electric generator operatively coupled to the hydraulic motor," with first and second fluid volumes in communication with the ports.

**Numbers.** None in retrieved text (the patent gives no power/efficiency figures in the snippets seen). **[not verified]** whether the specification contains any.

**Comparison with '695.** Parallel damper replacing the shock absorber; no collapsible frame; no series biasing spring; rectification is hydraulic (flow direction/motor), not by opposed one-way clutches; no flyweights; generator present; **hollow piston rod is present but used for wiring, not as a hollow generator shaft receiving a drive rod**. Different mechanism class.

---

## 7. Schenavar — US 4,032,829 (1977), "Road shock energy converter for charging vehicle batteries"

**Citation [S-primary, Google Patents/USPTO/Justia records].** US 4,032,829 A, title verified as "Road shock energy converter for charging vehicle batteries," inventor Harold E. Schenavar (listed as both inventor and assignee), priority/filing 1975-08-22, issued 1977-06-28; legal status expired. Filing date was shown only as the priority date; a separate filing date was not displayed.

**Disclosure [S-primary snippets of summary and claims].**
- Mounted at an **axle coupling** ("attaches to a vehicle axle"), i.e., it reads axle-to-body relative motion. The summary describes "oppositely-acting relatively-sliding inertia-operative racks and pinions in a shock-moved axle coupling, with unidirectional clutches linking the axle to a shaft that drives flywheels and a generator armature"; the detailed description refers to **two motion-transformer units, one for downward and one for upward axle movement, whose clutches drive the same shaft in one direction**.
- Claim 1 (as summarised by the search engine from USPTO full text, not quoted verbatim): a converter with an axle coupling, a rack housing and rack, a pinion meshing with the rack, **a unidirectional clutch** drivingly connecting the pinion to a shaft, **a flywheel** on the shaft to smooth the intermittent torque, and an electric generator charging the vehicle batteries. Dependent claim 2 adds a **rack-stroke-cushioning spring** inside the rack housing between one end of the rack and the housing (described elsewhere as optional).
- Later patents characterise it as "a mechanical device which employs rack and pinion gears, drive shafts, springs, flywheels and clutches"; Tufts' US 6,952,060 cites it and remarks that it "apparently relies on natural resonance."

**Is it cited on '695?** The '695 reference list given in the task brief (US 3,507,580; 3,799,481; 3,921,746; 3,980,152; 4,018,052; 4,098,083; 4,098,144; 4,223,532; 4,295,538; JP2012062884A) does **not** include 4,032,829. The '695 front page itself could not be fetched, so this is confirmed only against the list supplied. Search did confirm 4,032,829 is cited by US 6,952,060 (Tufts) and US 9,597,965.

**Why it matters.** Of all documents in this dossier, Schenavar is the closest to '695 claim 4 (both-stroke unidirectional drive via one-way clutches) and claim 8 (flywheel keeping rotation through transitions), and it predates everything else by decades. Its mechanism is rack-pinion with clutches on the pinion side, a solid shaft, flywheels, and a generator; its spring is a rack-end cushion, not a load-bearing series spring.

**Comparison with '695.**
- Collapsible frame between chassis and suspension, carrying load: absent (axle-coupled rack unit alongside the existing suspension; it does not carry sprung weight).
- Biasing spring softer than main spring, in series, frame heights summing to original spring height: absent (cushion spring only).
- Hollow generator shaft with drive mechanism inserted: absent (rack-pinion, external shaft).
- Two opposed one-way clutches rectifying both strokes: **present in substance** (two oppositely acting units with unidirectional clutches driving one shaft in one direction). Exact claim wording not verified; verify whether claim 1 recites one or two clutches.
- Fly weights / flywheel maintaining rotation through transition: **present** (flywheel on the shaft, recited in claim 1 per the summary).
- Generator and energy storage (battery): present.
- Drop-in replacement height: absent.

---

## 8. Hyundai — US 9,205,716 B2

**Citation [S-primary].** US 9,205,716 B2, "Energy regeneration device of suspension system for vehicle," Hyundai Motor Company; inventors include Un Koo Lee; application 14/096,479, filed Dec. 2013; granted Feb. 23, 2016. Family: US 9,030,033; US 9,270,153; KR 101484195 B1; publications 2012/0146339, 2014/0132007, 2014/0183873.

**Mechanism [S-primary abstract/description snippets].** A suspension link (control arm) connects wheel carrier to body; a **bush unit** at the body-side joint converts the link's hinge rotation into rotation of an output gear; a **one-way power transmission mechanism** (one-way clutch plus speed-up gear with idle gears, inside inner/outer cases) passes only one rotational sense; a **speed-up mechanism** (dependent claims: three single-pinion planetary sets) between the one-way mechanism and the generator; generator feeds a rectifier and battery. Clutch behaviour: the description covers the clutch engaging on bump, with a variant engaging on rebound; one family member says it "operates the generator when the suspension link arm moves up (rebound), and when it moves down (bump)" — whether 9,205,716 itself claims both-stroke drive with a single clutch arrangement is **[not verified]**; the task brief's characterisation "single one-way clutch" is consistent with the retrieved description. Claim 1 verbatim: **[not verified]**.

**Numbers.** None retrieved.

**Comparison with '695.** Rotary pickup at the control-arm pivot, in parallel with the spring (does not carry load); no collapsible frame; no series biasing spring; no hollow shaft with inserted rod; **one** one-way clutch (half-wave) with a speed-up gearbox, versus '695's two opposed clutches; no flyweights; generator present; no drop-in height feature.

---

## 9. Audi eROT (2016)

**Primary release: not fetched.** The Audi MediaCenter page was not reachable and did not appear in search results; the figures below come from syndicated copies of the release (Automotive World "news-releases" reprint, Charged EVs, Autocar Professional dated 12 Aug 2016, S&P Global AutoTechInsight which states the press release was dated **10 August 2016**, Engineering.com, Drive, Saudi Gazette) [S-secondary, but multiple independent reprints of the same release text].

**Mechanism.** "eROT": electromechanical rotary dampers replacing hydraulic telescopic dampers; a lever arm follows wheel-carrier motion and drives gears and a generator mounted horizontally near the rear axle; generator resistance provides the damping; actively controlled; operates on the 48 V electrical system; quoted spokesperson Stefan Knirsch (Board Member for Technical Development).

**Numbers (all from the release as reprinted).**
- Average recuperation on German roads: **100–150 W**.
- Range: **3 W** on a freshly paved freeway to **613 W** on a rough secondary road.
- CO2 saving under customer driving: up to **3 g/km**.
- The "0.7 L/100 km" figure belongs to the planned 2017 48-V mild-hybrid, not to eROT alone.
- Electrek's "500 W battery" is not in the release text and should not be cited.
- No production commitment.

**Comparison with '695.** Parallel rotary electromagnetic damper (lever + gearbox + generator); continuous bidirectional generator rotation with electrical rectification; no one-way clutches, no series spring, no collapsible frame, no hollow shaft, no flyweights. Relevant as the V3 anchor (3 / 100–150 / 613 W) exactly as CLAUDE.md states; note that these are per-vehicle totals for a system of (presumably four) dampers — the release does not say per damper. **Vehicle mass and number of dampers are not stated in the retrieved text**; the repo's "1800 kg sedan" is an assumption and should be tagged [ASSUMPTION].

---

## 10. Abdelkareem et al. (2021) — off-road SUV damper power

**Citation [S-primary, ScienceDirect/CityU record].** M. A. A. Abdelkareem et al., "Field measurements of the harvestable power potentiality of an off-road sport-utility vehicle," *Measurement* **179**, 109381 (July 2021; online 22 Apr 2021), DOI 10.1016/j.measurement.2021.109381. Full author list **[not verified]** (the CityU record omitted it; co-authors likely include L. Xu and others from the same group's 2018 SUV paper, but this is inference).

**Content [S-primary abstract/highlights].** Instrumented real-road tests of a wheeled off-road SUV (Xiao-Long XLW 5062X) with its passive telescopic damper, at 10–40 km/h, on off-road and city-road fields. Average dissipated power **30–334 W per damper off-road** and **3–25 W on city roads**; rebound-phase dissipation about **6×** compression-phase dissipation; off-road dissipation up to 12× city-road. Compression/rebound reported separately because some harvesters recover only one phase.

**Comparison with '695.** Measurement paper on a conventional damper; no device elements. Use: (a) heavy/rough-duty power magnitude anchor (hundreds of watts per corner), (b) the 6:1 rebound/compression asymmetry is a direct check on the Gate's two-stroke model (a full-wave rectifier that symmetrises engagement should be compared against a damper whose dissipation is strongly asymmetric; the asymmetry comes from the damper valving, not from the road input, so the Gate's spring-stroke energy split should be derived, not copied).

---

## 11. Sprag-clutch data (Formsprag, GMN)

Catalog PDFs could not be fetched; the following is from search snippets of those PDFs and manufacturer web pages.

**Formsprag (Regal Rexnord / Altra), catalog P-956-FC "Overrunning, Indexing, Backstopping Clutches" and "Overrunning Clutches Application Manual" [S-primary snippets].**
- Drag torque is listed as **"resistance after run-in"**, defined as the sum of seal drag, bearing drag and sprag energizing drag; HPI table values span roughly sub-1 to about 10 (units not visible in the snippet; the units column must be read from the PDF). One fragment for a size-300 unit read ".20 .33 .67" in a resistance column. **Units [not verified].**
- Lift-off: the Application Manual defines "lift-off speed" as the point at which the sprags lift off the inner or outer race; "the maximum drive speed is always less than the lift-off speed to insure positive sprag energizing"; inner-race overrunning is recommended for higher overrunning speeds; a catalog note states the overrunning shaft speed "should be greater than 400 RPM to assure C/T sprag lift-off" (applies to C/T-sprag designs). Numeric lift-off rpm per model: **[not verified]**.
- FSO maximum overrunning speeds (per size): FSO-300 3600, FSO-400 3600, FSO-500 3000, FSO-600 2400, FSO-700 2000, FSO-750 1800, FSO-800 1500, FSO-900 1350, FSO-1027 1100 rpm; rule "for O.R. > 1200 rpm, I.R. = O.R. − 50 rpm".
- Indexing: HPI series "especially designed for medium to heavy-duty indexing applications, or applications in excess of 150 strokes/min"; another note recommends HPI "for indexing rates in excess of 150 strokes per minute or indexing angles in excess of 90°"; GFR model limited to 350 indexes/min.
- Service factors: catalog states a higher service factor "possibly up to 6" where considerable vibration is present; Application Manual gives minimum 1.5 for clutch couplings and 2.0 for pulsating loads (compressors, pumps); an HPI ball-bearing-series "2.0 safety factor" fragment. A Grokipedia page quotes HPI service factors of 2.0–4.0 (low-reliability source).
- Rating basis in cycles: a snippet reads "cycles at full catalog torque" and "torque ratings are based upon using only one end face" (FSO, HPI, FSA, SB), but the cycle count was cut off. **The "1e6 cycles" basis in the task brief is [not verified].** Renold's sprag catalog ties selection to breakdown torque percentage with factors 1.0/1.2/1.5; Ringspann states max transmissible torque = 2× nominal.

**GMN (gmnbt.com pages) [S-primary].**
- FE 400 series: compact sprag insert elements for moderate-torque and indexing use; "practical speed limits due to centrifugal lift-off at high RPMs"; catalog max-rpm column exists (e.g., FE 410 Z2: 10,000 rpm) — the rule setting the limit is not shown.
- FE 8000 series: sprag centre of mass behind the pivot so centrifugal force increases engagement; "no low RPM limit, but also no high RPM limit."
- Drag torque: GMN states FE 400 and FE 8000 insert elements have "virtually no drag torque"; "assume a near 0 drag torque"; lubrication dominates drag.
- Stieber (sister brand) lists a centrifugal-lift-off sprag freewheel with 130 rpm minimum to 9,000 rpm maximum [S-primary product page].

**Implication for params.yaml.** Overrunning drag can be tagged [LITERATURE] as "≈ 0 per GMN; Formsprag 'resistance after run-in' table, units TBD." Lift-off rpm must stay [ASSUMPTION] until a model-specific catalog page is read; Formsprag's "> 400 rpm" for C/T sprags is the only number retrieved. Indexing service factor 2–4 (HPI) is supportable; a fatigue-cycle rating basis is not yet supportable from sources.

---

## 12. ISO 8608 road-class table

**Values.** Multiple independent sources agree that at n0 = 0.1 cycles/m, with G_d(n) = G_d(n0)(n/n0)^−w and w = 2, the class limits are (×10⁻⁶ m³): A < 32; B 32–128; C 128–512; D 512–2048; E 2048–8192 [S-secondary: arXiv 2506.21347 Table; Springer ETRR 2013 Table 1 (A–C: 16, 64, 256 geometric means); Múčka 2018 "Simulated road profiles according to ISO 8608 in vibration analysis"]. Geometric means therefore **16, 64, 256, 1024, 4096 ×10⁻⁶ m³** for A–E (continuing 16384, 65536, 262144 for F–H). The same values appear in numerous independent code bases [code], including one that attributes them to "ISO 8608, Table C.2".

**Caveats.** (a) The ISO 8608:2016 text itself was not read. (b) Some secondary tables quote the 1995 wording with units 10⁻⁶ m²/(cycle/m), numerically identical. (c) A few tables use a different reference (Ω0 = 1 rad/m) or list "1, 4, 16…" — these are not the same quantity; do not mix. Status for params.yaml: [LITERATURE] with the caveat that the primary standard was not consulted in this session.

---

## 13. ISO 2631-1 Wk weighting — implementable parameters

**Source status.** Rimell & Mansfield, "Design of digital filters for frequency weightings required for risk assessments of workers exposed to vibration," *Industrial Health* **45**(4), 512–519 (2007), DOI 10.2486/indhealth.45.512, is confirmed to exist and to cover Wk [S-primary J-STAGE/PubMed record]. A **corrigendum** exists (Industrial Health, later volume; PDF IH_48_5_743 and a second notice IH_48_1_129): errors in Equation 4, Table 5 and Table 8; "In Table 5, the value of G for BS 6841 Wb should be 1.024"; Table 8 Hh coefficient equations corrected [S-primary snippet]. Anyone copying coefficients from the 2007 paper must apply the corrigendum. The paper's own Wk table could not be read.

**Parameters (ISO 2631-1:1997 Annex A, Table 3 form), as implemented consistently in independent open-source code [code]:** Project Chrono `ChFilters.cpp` (projectchrono/chrono), `janiex/SimulinkMatlab/Matlab/ISO2631.m`, `Ergo-Tools/WBV_Calculator`, `jmrplens/phonometry`, and others; one implementation explicitly cites "Rimell & Mansfield (2007) Table 3."

| Weighting | f1 (Hz) | f2 (Hz) | f3 (Hz) | f4 (Hz) | Q4 | f5 (Hz) | Q5 | f6 (Hz) | Q6 | K |
|---|---|---|---|---|---|---|---|---|---|---|
| Wk (vertical z, seat) | 0.4 | 100 | 12.5 | 12.5 | 0.63 | 2.37 | 0.91 | 3.35 | 0.91 | 1 |
| Wd (horizontal x,y) | 0.4 | 100 | 2.0 | 2.0 | 0.63 | ∞ | – | ∞ | – | 1 |
| Wc (seat back) | 0.4 | 100 | 8.0 | 8.0 | 0.63 | ∞ | – | ∞ | – | 1 |
| We (rotational) | 0.4 | 100 | 1.0 | 1.0 | 0.63 | ∞ | – | ∞ | – | 1 |
| Wf (motion sickness) | 0.08 | 0.63 | ∞ | 0.25 | 0.86 | 0.0625 | 0.80 | 0.1 | 0.80 | 1 |
| Wj (head, recumbent) | 0.4 | 100 | ∞ | ∞ | – | 3.75 | 0.91 | 5.32 | 0.91 | 1 |

Q1 = Q2 = 1/√2 (second-order Butterworth band limits). One implementation lists f6 = 3.3 for Wk where others list 3.35; 3.35 is the majority value and matches the standard as commonly quoted. The gain K = 1 for all weightings in the ISO 2631-1 Annex A table is the common implementation; the Rimell & Mansfield table may list K explicitly — **[not verified]** from the paper itself.

**Transfer function (s = jω, ω_i = 2πf_i):**

- Band limiting: H_h(s) = s² / (s² + (ω1/Q1)s + ω1²); H_l(s) = ω2² / (s² + (ω2/Q2)s + ω2²)
- Acceleration–velocity transition: H_t(s) = (s/ω3 + 1) / ((s/ω4)² + s/(Q4 ω4) + 1)  (→ 1 when f3, f4 → ∞)
- Upward step: H_s(s) = (ω5/ω6)² · ((s/ω5)² + s/(Q5 ω5) + 1) / ((s/ω6)² + s/(Q6 ω6) + 1)  (→ 1 when f5, f6 → ∞)
- H_W(s) = K · H_h · H_l · H_t · H_s

Discretise each biquad by bilinear transform with per-section pre-warping (Project Chrono and the MATLAB file both do this). Sanity check after implementation: |H_Wk| should peak near 1.0 between 4 and 8 Hz and be ≈ 0.5 at ≈ 1 Hz and ≈ 16 Hz (values from the standard's tabulated weighting, not re-verified here — compute and compare with Table 3 of ISO 2631-1 once available).

---

## Numbers extracted

| Value | Units | Conditions | Source | Location / grade |
|---|---|---|---|---|
| > 60 | % (mech. efficiency) | MMR prototype, "high frequency" | Li et al. 2013 | abstract [S-primary] |
| ≈ 60; ≈ 62 plateau | % | 1.5 Hz, 5 mm; higher freq. | Li et al. 2013 | body text [S-primary]; figure no. not verified |
| 82–94 | % (elec. efficiency) | R_e = 30–100 Ω | Li et al. 2013 | body [S-primary] |
| 6.6 | Ω | generator internal resistance | Li et al. 2013 | body [S-primary] |
| 40.4 / 25.6 | W | 3 Hz, 5 mm; two loads (30/100 Ω ext. per IOP text; 23.4/94.6 Ω per RG copy) | Li et al. 2013 | body [S-primary]; load values conflict |
| > 15 (15.4) | W | 15 mph, smooth paved road, Suburban, one absorber | Li et al. 2013 (+ slides) | abstract [S-primary]; slides [S-secondary] |
| 0.0471 | m/s (peak) | derived: 2π·1.5 Hz·5 mm | this dossier | arithmetic |
| 0.0942 / 0.0666 | m/s (peak / RMS) | derived: 3 Hz, 5 mm | this dossier | arithmetic |
| 100–400 | W (avg, vehicle) | 60 mph, good/average roads, middle-sized car | Zuo & Zhang 2013 | abstract [S-primary] |
| up to 100 | W per wheel | mid-size car, highway (16 m/s per review) | Hsu 1996 | abstract [S-primary]; speed [S-secondary] |
| 100–150 | W (avg) | eROT, German roads | Audi release 10 Aug 2016 | reprints [S-secondary] |
| 3 / 613 | W (min / max) | new freeway / rough secondary road | Audi release | reprints [S-secondary] |
| ≤ 3 | g CO2/km | customer driving | Audi release | reprints [S-secondary] |
| 30–334 | W per damper | off-road, 10–40 km/h, XLW 5062X | Abdelkareem 2021 | abstract [S-primary] |
| 3–25 | W per damper | city road, 10–40 km/h | Abdelkareem 2021 | abstract [S-primary] |
| 6 | ratio | rebound / compression dissipation | Abdelkareem 2021 | abstract [S-primary] |
| 12 | ratio | off-road / city dissipation | Abdelkareem 2021 | abstract [S-primary] |
| 3600…1100 | rpm | FSO-300…FSO-1027 max overrunning | Formsprag catalog | table [S-primary snippet] |
| > 400 | rpm | overrunning speed to assure C/T sprag lift-off | Formsprag catalog | note [S-primary snippet] |
| 150 | strokes/min | threshold above which HPI recommended | Formsprag | [S-primary snippet] |
| 1.5 / 2.0 / up to 6 | – (service factor) | couplings / pulsating / heavy vibration | Formsprag App. Manual & catalog | [S-primary snippet] |
| ≈ 0 | N·m (drag) | FE 400 / FE 8000 insert elements | GMN web guide | [S-primary] |
| 10,000 | rpm | FE 410 Z2 max | GMN catalog | [S-primary snippet] |
| 130–9000 | rpm | Stieber centrifugal-lift-off sprag freewheel | Stieber product page | [S-primary] |
| 16/64/256/1024/4096 ×10⁻⁶ | m³ | G_d(n0) geometric means, A–E, n0 = 0.1 c/m, w = 2 | ISO 8608 via secondary tables | [S-secondary]/[code] |
| 32/128/512/2048/8192 ×10⁻⁶ | m³ | class upper limits A–E | same | [S-secondary] |
| 0.4, 100, 12.5, 12.5, 0.63, 2.37, 0.91, 3.35, 0.91 | Hz / – | Wk f1,f2,f3,f4,Q4,f5,Q5,f6,Q6 | ISO 2631-1 Annex A via code | [code], multiple independent |
| 1.024 | – | corrected G for BS 6841 Wb (Table 5) | Rimell & Mansfield corrigendum | [S-primary snippet] |
| Sep. 23, 2014 | date | US 8,841,786 issue | USPTO/EPO family | [S-primary] |
| Feb. 23, 2016 | date | US 9,205,716 grant | Google Patents | [S-primary] |
| 1975-08-22 / 1977-06-28 | dates | US 4,032,829 priority / issue | Google Patents | [S-primary] |

---

## Claim-element separation matrix

Rows: '695 elements (from the brief). Columns: prior-art items. Cells: **P** present, **p** partial, **–** absent, **?** not verifiable from retrieved text. Items 2, 3 (analysis only), 10–13 (data) have no device elements and are omitted; Hsu/Suda/Karnopp are collapsed into one "parallel EM damper" column because they share topology.

| '695 element | 1. Li/Zuo MMR 2013 | 4–5. Suda 1998 / Karnopp 1989 / Hsu 1996 (parallel EM) | 6. Levant US 8,841,786 | 7. Schenavar US 4,032,829 | 8. Hyundai US 9,205,716 | 9. Audi eROT |
|---|---|---|---|---|---|---|
| Vertically collapsible frame between chassis and suspension, in the load path | – (telescopic damper, parallel) | – | – | – (axle-coupled rack unit, not load-bearing) | – (pivot pickup) | – (lever on wheel carrier) |
| Frame biasing spring, rate < main spring, in series; heights add to original spring height (cl. 2–3) | – | – | – | – (rack-end cushion spring only, cl. 2) | – | – |
| Hollow rotatable generator shaft with drive mechanism inserted in it | – (solid shaft, bevel train) | – | p (hollow piston rod, but for wiring, not a drive rod in a generator shaft) | – | – | – |
| Spin imparted on both collapse and expansion (cl. 1) | P | – (bidirectional EM, electrical rectification) | P (hydraulic, both strokes) | P | ? (one clutch; family text says both strokes in some variants) | P (bidirectional rotation, electrical rectification) |
| Two opposed one-way (sprag/roller) clutches giving unidirectional drive on both strokes (cl. 4) | P (two roller clutches) | – | – (hydraulic rectification) | P in substance (two oppositely acting unidirectional-clutch units on one shaft); claim wording ? | – (single one-way clutch, half-wave) | – |
| Plates / guide bars / sleeves / housing orifice (cl. 5–7) | – | – | – | ? (rack housing; details not read) | – | – |
| Fly weights keep generator rotating through transition (cl. 8) | p (rotor inertia; explicit flywheel only in later railroad MMR) | – | – | P (flywheel on shaft, cl. 1) | – | – |
| Electrical generator | P (PM DC) | P (linear PM / EM actuator) | P (in-fluid generator via gerotor) | P | P (+ planetary speed-up) | P (rotary, 48 V) |
| Energy storage (cl. 9) | p (load resistor in tests; battery in vehicle) | p | ? | P (vehicle batteries, title) | P (rectifier + battery) | P (48 V system) |
| Drop-in replacement preserving ride height | – | – | – | – | – | – |

**Reading of the matrix.** No single retrieved document combines the series-spring collapsible frame with a hollow-shaft drive and two opposed clutches. The elements most exposed to prior art are claim 4 (both-stroke clutch rectification: Li/Zuo 2013 and Schenavar 1977) and claim 8 (flywheel through transition: Schenavar 1977). Schenavar is not on the '695 citation list supplied, which is the most significant finding for the claims audit. The distinguishing elements, on the evidence available, are the load-bearing collapsible frame with a softer series biasing spring (claims 1–3) and the hollow generator shaft receiving the drive mechanism (claim 1), neither of which appears in any item here.

---

## Open items (could not be closed in this session)

1. Read the IOP PDF of Li et al. 2013 to fix: external load values (23.4/93.4 vs 30/100 Ω), figure numbers, gear ratio, pinion radius; and correct the V2 gate label (0.047 m/s peak ↔ 1.5 Hz/5 mm; 40.4 W ↔ 3 Hz/5 mm).
2. Read Zuo & Zhang 2013 for the closed-form mean-power equation and the vehicle parameter table.
3. Read US 4,032,829 claims verbatim; confirm whether claim 1 recites one or two unidirectional clutches, and whether the '695 front page lists it (expected: no).
4. Read US 9,205,716 claim 1; confirm single-clutch scope.
5. Identify the actual granted Zuo/SUNY MMR patent number (the numbers in the brief were not confirmed).
6. Formsprag: units and values of "resistance after run-in"; per-model lift-off rpm; cycle basis of torque ratings.
7. ISO 8608:2016 Table C.2 and ISO 2631-1 Table 3 from the standards themselves.
8. Audi MediaCenter original page for the eROT release (date 10 Aug 2016 per S&P Global).
