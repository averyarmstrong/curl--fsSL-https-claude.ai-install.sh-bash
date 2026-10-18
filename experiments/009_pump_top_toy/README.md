# 009 — The pump top from first principles

**Question.** What does the push-down spinning top actually do with the
hand's work, and which of its features carry over to the Gate?

**Model.** `aks_lab.toy.PumpTop`: hand as a Hill force–velocity law (15 N at
rest, zero at 1 m/s), 20 g plunger on a 200 N/m return spring between two
Kelvin–Voigt stops 60 mm apart, helix lead 25 mm/rev (r = 251 rad/m), one
pawl (or two, opposed) to a 0.1 kg × 50 mm disk (J = 1.25e-4 kg·m²),
80 % screw efficiency, bearing and air drag, optional load torque. All
parameters `asserted` (no toy on the bench); conclusions are structural.

**Run.** `python experiments/009_pump_top_toy/run.py` (≈1 min, single core).
Writes `results/RESULTS.md`, `results/fig_spinup.png`.

**Findings.** See `docs/03a_pump_top_first_principles.md` §5.
