# gate-twin lab notebook

Running record of what was tried, what failed, and why. Newest entries at
the bottom. Candor is the point — ugly runs get written down.

---

## 2026-07-02 — Session 1: scaffold, physics core, V1 gates

**Goal:** repo scaffold, PHYSICS.md, hybrid model, V1 analytic gates.

### Decisions

1. **Sprag model: exact kinematic constraint + event-driven mode switching**
   (modes free/engA/engB), not high-stiffness penalty coupling. Rationale:
   (a) the <1% energy-closure gate wants a ledger exact to solver tolerance —
   penalty contact adds a stiff spring whose stored energy sloshes into the
   audit; (b) the penalty stiffness reflected through Gt ≈ 1484 (rad/s)/(m/s)
   creates ~kHz modes that would force tiny steps. Engagement events occur at
   zero relative speed, so they are impact-free; disengagement is the
   physical T_c = 0 (a sprag cannot pull). Grazing engagements (T_c < 0 at
   contact) are rejected with a 1e-8 s micro-step; a Zeno counter guards
   chatter.

2. **Reflected inertance.** With patent-brief kinematics (lead 1 in/rev,
   step-up 6) a generator-shaft inertia J = 3e-4 kg·m² reflects onto the
   frame stroke as Jr = J·Gt² ≈ 660 kg. This is not a bug: MMR-class devices
   are known to behave as large inerters (Li & Zuo 2013). It WILL shape V2
   calibration and must be a headline axis of the sensitivity study. Flagged
   in PHYSICS.md §8.

3. **Energy integrals as ODE states** (damper, stop, clutch, electrical,
   generator loss, road work) so the audit is limited only by rtol. Stop
   force clipping is booked exactly by splitting conservative (½k·pen²) from
   the residual.

4. **Coordinates:** perturbations about static equilibrium → gravity cancels;
   frame travel ±x_b_max symmetric about loaded equilibrium (asymmetric
   preload deferred, noted in PHYSICS.md).

### Failures / gotchas hit

- PyYAML parses `16e-6` as a *string*; wrote `16.0e-6`. Added a params test
  that yaml and dataclass defaults agree so drift is caught.
- Loader bug: `_leaf` was indexing the dict with the dotted path label.
- **Ugly run, reported per honesty norms:** first V1d bench run passed the
  closure gate but the ledger showed **57% of input energy going to sprag
  overrun drag** (1100 J of 1914 J; electrical fraction only 29%). Cause:
  first-guess c_od = 5e-3 N·m·s/rad gives ~3.5 N·m drag at ~700 rad/s slip —
  10–70× sprag-catalog drag (0.05–0.5 N·m), and reflected through Gt² it is
  a ~22,000 N·s/m parasitic damper on the stroke. Corrected to c_od = 2e-4
  (≈0.1 N·m at 500 rad/s slip, catalog-anchored). This is a prior correction
  to published hardware data, not tuning to a power target — but it shows
  how sensitive the architecture is to overrun drag × Gt²; c_od goes on the
  tornado-sensitivity list.

### V1 status

See `tests/test_v1_gates.py` — results recorded in session summary and CI.

### Next session

V2: configure single-corner rectifier at 0.047 m/s RMS suspension velocity,
reproduce Zuo MMR ≈40 W/unit and >60% mechanical efficiency within ±25%.
Pull the actual Li/Zuo 2013 numbers via web search and cite precisely
(power level, device kinematics, test conditions) before running anything.

## 2026-10-22 — Duke Energy Week poster

**Goal:** 48×36 in landscape poster for the AKS booth at Duke Energy Week
(`reports/poster/`). Not physics work; no model code touched.

- Source material: AKS business card (logo mark extracted from the PDF),
  website screenshot of the "push-down top" analogy and patented-drive figure
  (both redrawn as inline SVG), photo of Avery and Larry with the first
  machined frame. The live website could not be fetched from the sandbox
  (proxy 403), so copy follows the screenshot and the slogan on the card.
- Honesty norms applied on the poster: every number tagged Literature /
  Predicted / Estimate; passenger-car harvest stated as "hundreds of W", kW
  class reserved for heavy vehicles; "a sedan will not charge itself".
- IP guardrail: only the granted-patent mechanism is described. No unfiled
  concepts appear.
- Render: `reports/poster/render.sh` (headless Chromium → PDF + PNG).
