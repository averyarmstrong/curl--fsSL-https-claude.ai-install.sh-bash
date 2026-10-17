"""Validation (a) and (b) of the brief: linear quarter car vs its closed forms; Zuo & Zhang 2013 baseline.

Also the road-power theorem (docs/01_physics.md §7): fixed-body limit and
insensitivity to damping.
"""

import numpy as np
import pytest

from aks_lab import CornerParams, PassiveQuarterCar, corner, iso8608_profile
from aks_lab.roads import sine
from aks_lab.validate.analytic import (
    fixed_body_power,
    mean_road_power,
    transmissibility,
    zuo_baseline,
)

C, _ = corner("midsize_car")


@pytest.mark.parametrize("f", [0.7, 1.1, 3.0, 11.0])
def test_transmissibility_matches_analytic_under_1pct(f):
    A = 0.005
    r = PassiveQuarterCar(C, sine(A, f, ramp=2.0)).simulate(16.0 + 6.0 / f, t_stationary=12.0, dt_out=1e-3)
    m = r.mask()
    amp = 0.5 * (np.max(r.z_s[m]) - np.min(r.z_s[m]))
    H = abs(transmissibility(C, [f])["H_zs"][0])
    assert abs(amp / A - H) / H < 0.01, (f, amp / A, H)
    assert r.energy_audit()["closure"] < 1e-3


def test_road_power_time_domain_matches_h2_norm():
    """Mean road power from simulation vs exact Lyapunov value, ensemble over seeds."""
    v = 26.82
    exact = mean_road_power(C, "C", v)["P_road"]
    ps = []
    for seed in (1, 2, 3):
        r = PassiveQuarterCar(C, iso8608_profile("C", v, 40.0, seed=seed)).simulate(40.0)
        assert r.energy_audit()["closure"] < 1e-3
        ps.append(r.rates()["P_road"])
    assert abs(np.mean(ps) - exact) / exact < 0.06, (ps, exact)


def test_zuo_2013_baseline_100_to_400W():
    """Validation (b): mid-size car, 60 mph, good (B) to average (C) roads, four corners."""
    z = zuo_baseline(C)
    assert 80.0 <= z["B"] <= 160.0, z
    assert 300.0 <= z["C"] <= 550.0, z
    assert z["A"] < z["B"] < z["C"] < z["D"]


def test_road_power_theorem_exact_for_linear_corner():
    """P_road = k_t W_v / 4 exactly, for arbitrary masses, stiffness and damping (01_physics §7)."""
    for ms, mu, km, cs, kt in ((400, 40, 20000, 1500, 180000), (1e9, 40, 20000, 1500, 180000),
                               (3600, 430, 360000, 22000, 1.8e6), (560, 65, 32000, 400, 250000)):
        c = CornerParams(ms, mu, km, cs, kt)
        p = mean_road_power(c, "C", 26.82)
        assert abs(p["P_road"] - 0.25 * kt * p["W_v"]) / p["P_road"] < 1e-6, (c, p)


def test_road_power_theorem_holds_with_the_gate():
    """Nonlinear corner (clutches, stops, inertance) still draws k_t W_v / 4 from the road."""
    from aks_lab import QuarterCarGate, gate_from_yaml
    v = 26.82
    exact = 0.25 * C.k_t * mean_road_power(C, "C", v)["W_v"]
    ps = []
    for seed in (1, 2):
        road = iso8608_profile("C", v, 30.0, seed=seed)
        g = gate_from_yaml(C.k_m, {"r": 400.0, "J": 2e-4, "c_gen": 0.02})
        r = QuarterCarGate(C, g, road).simulate(30.0)
        assert r.energy_audit()["closure"] < 0.01
        ps.append(r.rates()["P_road"])
    assert abs(np.mean(ps) - exact) / exact < 0.08, (ps, exact)


def test_fixed_body_formula_is_not_the_limit():
    """Documents the pitfall: a body fixed in absolute space under a Brownian road is singular."""
    p = mean_road_power(CornerParams(1e9, C.m_u, C.k_m, C.c_s, C.k_t), "C", 26.82)
    assert p["P_road"] > fixed_body_power(C.k_m, C.k_t, p["W_v"])
    assert abs(p["P_road"] - p["P_ceiling"]) / p["P_ceiling"] < 1e-6


def test_road_power_scales_with_speed_and_class_only():
    base = mean_road_power(C, "C", 26.82)["P_road"]
    assert abs(mean_road_power(C, "C", 2 * 26.82)["P_road"] / base - 2.0) < 1e-9
    assert abs(mean_road_power(C, "D", 26.82)["P_road"] / base - 4.0) < 1e-9


def test_linear_gate_surrogate_conserves_and_tracks_simulation():
    """Linearised Gate corner: dissipations sum to the supply; P_elec near the nonlinear sim at a low-inertance point."""
    from aks_lab.validate.analytic import linear_gate_power
    k_b = C.k_m / 8.35
    for b in (0.0, 27.0, 660.0):
        r = linear_gate_power(C, "C", 26.82, k_b, c_eq=900.0, b_inert=b, c_b=100.0)
        assert r["closure"] < 1e-6, r
    r = linear_gate_power(C, "C", 26.82, k_b, c_eq=0.01 * 300**2, b_inert=3e-5 * 300**2, c_b=100.0)
    # exp 001 nonlinear median at this point: 9.7 W (r=300, J=3e-5, c_gen=0.01, stock damper)
    assert 6.0 < r["P_elec"] < 16.0, r["P_elec"]
