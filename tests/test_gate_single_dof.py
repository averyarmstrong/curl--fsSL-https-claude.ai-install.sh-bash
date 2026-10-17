"""Gate element on the prescribed-stroke bench: hand derivation, full-wave, conservation, limits.

docs/01_physics.md §11 (hand derivation) and §4 (events, impact, slip).
"""

import math

import numpy as np

from aks_lab import BenchRig, Gate, GateParams, NullGenerator, linear_gate, sine_stroke, still

A, F, R = 0.0127, 2.5, 1484.0
CGEN = 2e-3


def _gate(**kw):
    base = dict(k_b=333.6, c_gen=CGEN, eta=0.85, r=R, J=1e-9, c_od=0.0, c_w=0.0, c_b=0.0, x_c=1.0, x_e=1.0)
    base.update(kw)
    return linear_gate(**base)


def test_hand_derivation_J_to_zero():
    b = BenchRig(_gate(), sine_stroke(A, F)).simulate(4.0)
    pred = 0.5 * CGEN * R**2 * (2 * math.pi * F * A) ** 2
    got = b.mean_powers(2.0)["P_gate"]
    assert abs(got - pred) / pred < 0.005, (got, pred)
    assert b.energy_audit()["closure"] < 1e-6


def test_full_wave_both_clutches_rotor_never_negative():
    b = BenchRig(_gate(J=3e-4, c_od=2e-4, c_w=5e-5), sine_stroke(A, F)).simulate(6.0)
    c = b.engage_counts()
    assert c["A"] >= 5 and c["B"] >= 5
    assert b.omega.min() > -1e-9
    assert b.energy_audit()["closure"] < 1e-6


def test_power_monotone_in_inertia_fraction_engaged():
    """Larger J -> rotor coasts above race speed near reversals -> less of the cycle engaged."""
    fr = []
    for J in (1e-9, 1e-4, 1e-3):
        b = BenchRig(_gate(J=J), sine_stroke(A, F)).simulate(6.0)
        m = b.t >= 3.0
        modes = np.empty(b.t.size, dtype=object)
        modes[:] = "free"
        for mode, t0, t1 in b.segments:
            modes[(b.t >= t0) & (b.t <= t1)] = mode
        fr.append(np.mean(modes[m] != "free"))
    assert fr[0] > 0.98 and fr[0] >= fr[1] >= fr[2], fr


def test_pure_spring_zero_loop_area():
    g = Gate(GateParams(k_b=333.6, c_b=0.0, c_od=0.0, c_w=0.0, r=R, J=1e-9, x_c=1.0, x_e=1.0), NullGenerator())
    b = BenchRig(g, sine_stroke(A, F), force_freewheel=True).simulate(5 / F)
    w_net = b.y[1, -1] - b.y[1, 0]
    assert abs(w_net) < 1e-6 * (0.5 * 333.6 * A**2)


def test_spin_down_exponential():
    g = Gate(GateParams(k_b=333.6, c_od=0.0, c_w=5e-4, J=3e-4, x_c=1.0, x_e=1.0), NullGenerator())
    b = BenchRig(g, still()).simulate(1.2, omega0=300.0)
    analytic = 300.0 * np.exp(-5e-4 * b.t / 3e-4)
    assert np.max(np.abs(b.omega - analytic)) / 300.0 < 1e-6
    assert b.engage_counts() == {"A": 0, "B": 0}


def test_backlash_impact_dissipates_and_closes():
    b0 = BenchRig(_gate(J=3e-4), sine_stroke(A, F)).simulate(6.0)
    b1 = BenchRig(_gate(J=3e-4, theta_bl=0.02), sine_stroke(A, F)).simulate(6.0)
    e0, e1 = b0.energy_audit(), b1.energy_audit()
    assert e1["closure"] < 1e-5 and e0["closure"] < 1e-5
    assert e1["E_clutch"] > e0["E_clutch"] >= 0.0
    imp = [ev[2]["impulse"] for ev in b1.events if ev[2] and "impulse" in ev[2]]
    assert max(imp) > 0.0
    assert b1.engage_counts()["A"] >= 5 and b1.engage_counts()["B"] >= 5


def test_torque_capacity_slip_closes():
    b = BenchRig(_gate(J=3e-4, T_cap=0.05), sine_stroke(A, F)).simulate(6.0)
    e = b.energy_audit()
    assert e["closure"] < 1e-5
    labels = {ev[1][:-1] for ev in b.events}
    assert "unslip" in labels
    assert e["E_clutch"] > 0.0
    assert b.mean_powers(3.0)["P_gate"] < BenchRig(_gate(J=3e-4), sine_stroke(A, F)).simulate(6.0).mean_powers(3.0)["P_gate"]


def test_hard_stop_closes_ledger():
    g = _gate(J=3e-4, x_c=0.006, x_e=0.006, c_od=2e-4, c_w=5e-5)
    b = BenchRig(g, sine_stroke(A, F)).simulate(4.0)
    e = b.energy_audit()
    assert e["closure"] < 1e-4
    assert e["E_stop"] > 0.0
