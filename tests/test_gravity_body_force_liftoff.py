"""Three objections to the road-power theorem, each turned into a test.

1. Gravity: a full-coordinate model carrying g and the spring preloads
   reproduces the perturbation model to solver tolerance.  Weight does no
   net work over a cycle; it only sets the operating point.
2. Body forces (wind, powertrain): a separate input channel; the ledger
   books it and closes; the road channel is unchanged.
3. Tire lift-off: with a one-sided tire the ledger still closes and the
   road supply is reduced, not increased.
"""

import numpy as np
from scipy.integrate import solve_ivp

from aks_lab import (
    CornerParams,
    PassiveQuarterCar,
    QuarterCarGate,
    corner,
    gate_from_yaml,
    iso8608_profile,
)
from aks_lab.roads import band_limited_force
from aks_lab.validate.analytic import mean_road_power

G = 9.80665
C, _ = corner("midsize_car")


def _full_gravity_passive(c: CornerParams, road, t_end, dt=2e-3):
    """Absolute coordinates: heights above the road datum, free lengths, gravity and preloads explicit."""
    H_t, H_s = 0.10, 0.30                      # tire and spring free lengths (arbitrary)
    d_t = (c.m_s + c.m_u) * G / c.k_t          # static tire compression
    d_s = c.m_s * G / c.k_m                    # static spring compression

    def rhs(t, y):
        zs, vs, zu, vu = y
        zr, zrd = road.z(t), road.zdot(t)
        f_spring = c.k_m * (H_s - (zs - zu)) + c.c_s * (vu - vs)   # upward on sprung mass
        f_tire = c.k_t * (H_t - (zu - zr)) + c.c_t * (zrd - vu)      # upward on unsprung mass
        return [vs, (f_spring - c.m_s * G) / c.m_s, vu, (f_tire - f_spring - c.m_u * G) / c.m_u]

    y0 = [(H_t - d_t) + (H_s - d_s), 0.0, H_t - d_t, 0.0]   # equilibrium heights
    sol = solve_ivp(rhs, (0, t_end), y0, method="LSODA", t_eval=np.arange(0, t_end + 1e-12, dt),
                    rtol=1e-9, atol=1e-11, max_step=5e-3)
    return sol.t, sol.y[0] - y0[0], sol.y[2] - y0[2]


def test_gravity_formulation_is_identical():
    road = iso8608_profile("C", 26.82, 8.0, seed=4)
    t, zs_full, zu_full = _full_gravity_passive(C, road, 8.0)
    r = PassiveQuarterCar(C, road).simulate(8.0, rtol=1e-9, atol=1e-11)
    zs = np.interp(t, r.t, r.z_s)
    zu = np.interp(t, r.t, r.z_u)
    assert np.max(np.abs(zs - zs_full)) < 1e-6 * max(np.max(np.abs(zs)), 1e-9)
    assert np.max(np.abs(zu - zu_full)) < 1e-6 * max(np.max(np.abs(zu)), 1e-9)


def test_dissipation_on_a_bump_is_not_proportional_to_weight():
    """Same bump and tire, 4x the mass at matched ride tune: dissipated energy FALLS, it does not scale with W."""
    from aks_lab.roads import bump
    ws = []
    for ms in (300.0, 600.0, 1200.0):
        c = CornerParams(ms, C.m_u, C.k_m * ms / C.m_s, C.c_s * np.sqrt(ms / C.m_s), C.k_t)
        r = PassiveQuarterCar(c, bump(0.03, 1.0, 20.0)).simulate(6.0, rtol=1e-9)
        a = r.energy_audit()
        assert a["closure"] < 1e-4
        ws.append(a["E_damper"])
    # a deterministic bump is not the white-noise case of the theorem, so no exact invariance is
    # expected; what must NOT happen is E ∝ W.  Observed: 153 / 132 / 108 J for 300 / 600 / 1200 kg.
    assert ws[0] > ws[1] > ws[2], ws
    assert ws[2] / ws[0] > 0.5, ws


def test_body_force_channel_closes_and_leaves_road_channel_alone():
    road = iso8608_profile("C", 26.82, 20.0, seed=2)
    fb = band_limited_force(100.0, 0.2, 3.0, 20.0, seed=1)
    p0 = PassiveQuarterCar(C, road).simulate(20.0)
    p1 = PassiveQuarterCar(C, road, f_body=fb).simulate(20.0)
    a0, a1 = p0.energy_audit(), p1.energy_audit()
    assert a0["closure"] < 1e-3 and a1["closure"] < 1e-3
    assert a1["E_body"] > 0.0
    assert abs(a1["E_road"] - a0["E_road"]) / a0["E_road"] < 0.03     # road channel unchanged
    g = gate_from_yaml(C.k_m, {"r": 300.0, "J": 3e-5, "c_gen": 0.01})
    q = QuarterCarGate(C, g, road, f_body=fb).simulate(12.0)
    assert q.energy_audit()["closure"] < 1e-2


def test_oneside_tire_closes_and_cannot_add_supply():
    from dataclasses import replace
    c1 = replace(C, tire_oneside=True)
    # severe road to force lift-off
    road = iso8608_profile("E", 26.82, 20.0, seed=3)
    lin = PassiveQuarterCar(C, road).simulate(20.0)
    one = PassiveQuarterCar(c1, road).simulate(20.0)
    a_lin, a_one = lin.energy_audit(), one.energy_audit()
    assert a_lin["closure"] < 1e-3 and a_one["closure"] < 1e-3
    f = one.tire_force()
    assert np.any(f <= -c1.static_load + 1e-6), "test road did not lift the wheel"
    assert a_one["E_road"] < a_lin["E_road"]
    exact = mean_road_power(C, "E", 26.82)["P_road"]
    assert one.rates()["P_road"] < 1.05 * exact
    g = gate_from_yaml(C.k_m, {"r": 300.0, "J": 3e-5, "c_gen": 0.01})
    q = QuarterCarGate(c1, g, road).simulate(10.0)
    assert q.energy_audit()["closure"] < 1e-2
