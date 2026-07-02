"""V1 gate evidence — prints the numbers behind each analytic-limit test.

Run:  python notebooks/v1_evidence.py
This is the human-readable companion to tests/test_v1_gates.py.
"""

import dataclasses

import numpy as np

from gatetwin import (
    BenchRig,
    NullGenerator,
    Params,
    PMGenerator,
    QuarterCarGate,
    iso8608_profile,
    raised_cosine,
    still,
)

P = Params()
print(f"baseline: Gt = {P.Gt:.1f} (rad/s)/(m/s), reflected inertance Jr = {P.Jr:.0f} kg\n")

# V1a — locked kinematic ratio
rig = BenchRig(P, PMGenerator(), raised_cosine(0.04, 1.5))
r = rig.simulate(4.0, lock=True, rtol=1e-10, atol=1e-12)
err = np.max(np.abs(r.omega - P.Gt * r.stroke_rate())) / np.max(np.abs(r.omega))
print(f"V1a bench locked ratio     max|omega - Gt*xdot| / max|omega| = {err:.2e}")

road = iso8608_profile("C", speed=20.0, duration=3.0, seed=7)
r = QuarterCarGate(P, PMGenerator(), road).simulate(3.0, lock="A", rtol=1e-9)
kin = P.Gt * r.frame_stroke_rate
err = np.max(np.abs(r.omega - kin)) / max(np.max(np.abs(kin)), 1.0)
print(f"V1a full-model locked      relative drift                    = {err:.2e}")

# V1b — spin-down
p = dataclasses.replace(P, c_od=0.0, c_w=5e-4)
r = BenchRig(p, PMGenerator(R_load=None), still()).simulate(1.2, omega0=300.0, rtol=1e-11, atol=1e-13)
rel = np.max(np.abs(r.omega - 300.0 * np.exp(-p.c_w * r.t / p.J)) / 300.0)
print(f"V1b spin-down vs exp(-c t/J)  max rel error                  = {rel:.2e}")

# V1c — pure spring zero area
p = dataclasses.replace(P, c_b=0.0, c_od=0.0)
r = BenchRig(p, NullGenerator(), raised_cosine(0.04, 1.5), force_freewheel=True).simulate(
    5 / 1.5, rtol=1e-10, atol=1e-12
)
w = r.y[1, -1]
print(f"V1c spring-only loop area  net work over 5 cycles           = {w:+.2e} J "
      f"(elastic scale {0.5 * p.k_b * 0.04**2:.1f} J)")

# V1d — rectified positive area
r = BenchRig(P, PMGenerator(), raised_cosine(0.05, 1.5)).simulate(8.0, rtol=1e-9, atol=1e-11)
a = r.energy_audit()
w_last = r.y[1, -1] - np.interp(r.t[-1] - 1 / 1.5, r.t, r.y[1])
print("\nV1d rectified bench (stroke 50 mm pp @ 1.5 Hz, PM gen, R_load=1 ohm):")
print(f"    engagements A/B = {r.engage_counts['A']}/{r.engage_counts['B']}, "
      f"min omega = {r.omega.min():.2e} rad/s (one-way), peak = {r.omega.max():.0f} rad/s "
      f"({r.omega.max() * 60 / 2 / np.pi:.0f} rpm)")
print(f"    loop work last cycle = {w_last:.2f} J  ->  mean mech power {w_last * 1.5:.1f} W")
print(f"    ledger: work in {a['E_work_in']:.2f} J = elec {a['E_elec']:.2f} "
      f"+ genloss {a['E_genloss']:.2f} + clutch {a['E_clutch']:.2f} "
      f"+ damp {a['E_damp']:.2f} + dStorage {a['dE_storage']:.2f} J")
print(f"    closure = {a['closure']:.2e}   elec fraction of input = {a['E_elec'] / a['E_work_in']:.1%}")

# V1e — full system audit
road = iso8608_profile("C", speed=25.0, duration=6.0, seed=42)
r = QuarterCarGate(P, PMGenerator(), road).simulate(6.0, rtol=1e-8)
a = r.energy_audit()
print("\nV1e full quarter-car, ISO 8608 class C @ 25 m/s (56 mph), 6 s:")
print(f"    engagements A/B = {r.engage_counts['A']}/{r.engage_counts['B']}, "
      f"min omega = {r.omega.min():.2e}, peak screw race speed = {r.screw_rpm.max():.0f} rpm "
      f"(lift-off limit {P.sprag_liftoff_rpm:.0f} rpm)")
print(f"    road work in = {a['E_road_in']:.1f} J over 6 s")
print(f"    -> elec {a['E_elec']:.1f} J ({a['E_elec'] / 6:.1f} W mean), "
      f"damper {a['E_damper']:.1f} J, genloss {a['E_genloss']:.1f} J, "
      f"clutch {a['E_clutch']:.2f} J, dStorage {a['dE_storage']:.2f} J")
print(f"    closure = {a['closure']:.2e}  (<1% gate)")
print(f"    RMS main-damper velocity = {np.std(np.gradient(r.y[2] - r.y[4], r.t)):.3f} m/s, "
      f"RMS frame-stroke rate = {np.std(r.frame_stroke_rate):.3f} m/s")
