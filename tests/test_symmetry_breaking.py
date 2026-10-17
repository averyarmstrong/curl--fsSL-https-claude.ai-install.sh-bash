"""docs/03_symmetry_breaking_first_principles.md §6–7: the worked single cycle and the 1 kW table.

Bench springs (Ebsco EB-7234 bias, `measured`), 1 in amplitude at 3 Hz.
"""

import math

from aks_lab import BenchRig, Gate, GateParams, NullGenerator, linear_gate, sine_stroke

LBF_IN = 4.44822 / 0.0254
K_B = 1.905 * LBF_IN          # 333.6 N/m
A, F = 0.0254, 3.0
W = 2 * math.pi * F
R = 300.0


def _rig(c_eq, J=1e-9):
    if c_eq == 0:
        g = Gate(GateParams(k_b=K_B, c_b=0.0, c_od=0.0, c_w=0.0, r=R, J=J, x_c=1.0, x_e=1.0), NullGenerator())
        return BenchRig(g, sine_stroke(A, F), force_freewheel=True)
    g = linear_gate(k_b=K_B, c_gen=c_eq / R**2, eta=1.0, r=R, J=J, c_od=0.0, c_w=0.0, c_b=0.0, x_c=1.0, x_e=1.0)
    return BenchRig(g, sine_stroke(A, F))


def test_spring_alone_zero_loop_area():
    b = _rig(0).simulate(3.0)
    assert abs(b.mean_powers(1.0)["P_work_in"]) < 1e-9
    assert abs(0.5 * K_B * A**2 - 0.1076) < 1e-3          # stored, and returned, each cycle


def test_rectified_loop_area_is_pi_c_w_A2():
    for c_eq, p_doc in ((100.0, 11.5), (500.0, 57.3)):
        b = _rig(c_eq).simulate(3.0)
        mp = b.mean_powers(1.0)
        w_cycle = math.pi * c_eq * W * A**2
        assert abs(mp["P_gate"] - w_cycle * F) / (w_cycle * F) < 2e-3
        assert abs(mp["P_work_in"] - mp["P_gate"]) < 1e-3 * mp["P_gate"]   # all of it came through the rod
        assert abs(mp["P_gate"] - p_doc) < 0.1
        assert b.energy_audit()["closure"] < 1e-8


def test_flywheel_smooths_but_does_not_add():
    b0 = _rig(500.0).simulate(6.0)
    b1 = _rig(500.0, J=10.0 / R**2).simulate(6.0)          # J r^2 = 10 kg
    p0, p1 = b0.mean_powers(3.0)["P_gate"], b1.mean_powers(3.0)["P_gate"]
    assert abs(p1 - p0) / p0 < 0.01
    om = b1.omega[b1.t > 3.0]
    assert om.min() > 0.0 and om.max() < 1.01 * R * W * A  # never above race peak, never stops
    assert b1.energy_audit()["closure"] < 1e-8


def test_one_kw_rod_force_table():
    def f_peak(P, f, A):
        return 2 * P / (2 * math.pi * f * A)
    assert abs(f_peak(1000, 3, 0.0254) - 4178) < 10
    assert abs(f_peak(1000, 3, 0.127) - 836) < 5
    assert abs(f_peak(1000, 1, 0.0127) - 25069) < 50
