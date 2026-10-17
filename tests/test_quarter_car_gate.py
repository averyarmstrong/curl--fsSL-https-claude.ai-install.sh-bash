"""Corner-with-Gate: conservation on an ISO road, locked-ratio limit, both damper spans, metrics."""

import numpy as np
import pytest

from aks_lab import PassiveQuarterCar, QuarterCarGate, corner, gate_from_yaml, iso8608_profile
from aks_lab.metrics import energy_metrics, handling_metrics, p_net, ride_metrics, sizing_metrics

C, GM = corner("midsize_car")
ROAD = iso8608_profile("C", 26.82, 12.0, seed=42)


@pytest.fixture(scope="module")
def res():
    g = gate_from_yaml(C.k_m, {"r": 400.0, "J": 2e-4, "c_gen": 0.02})
    return QuarterCarGate(C, g, ROAD, m_f=8.0, damper_span="full").simulate(12.0)


def test_energy_closure_under_1pct(res):
    a = res.energy_audit()
    assert a["E_road"] > 0.0
    assert a["closure"] < 0.01, a


def test_full_wave_on_road(res):
    assert res.omega.min() > -1e-8
    c = res.engage_counts()
    assert c["A"] > 5 and c["B"] > 5
    assert res.energies()["E_elec"] > 0.0


def test_locked_ratio_limit():
    g = gate_from_yaml(C.k_m)
    r = QuarterCarGate(C, g, ROAD, lock="A").simulate(3.0, rtol=1e-9)
    kin = g.p.r * r.frame_stroke_rate
    assert np.max(np.abs(r.omega - kin)) < 1e-6 * max(np.max(np.abs(kin)), 1.0)


def test_damper_span_main_runs_and_closes():
    g = gate_from_yaml(C.k_m, {"r": 400.0, "J": 2e-4})
    r = QuarterCarGate(C, g, ROAD, damper_span="main").simulate(6.0)
    assert r.energy_audit()["closure"] < 0.01


def test_metrics_and_baseline(res):
    e = energy_metrics(res)
    assert 0.0 <= e["phi"] <= 1.0
    assert abs(e["P_road"] - (e["P_elec"] + e["P_damper"] + e["P_friction_total"])) / e["P_road"] < 0.05
    rm = ride_metrics(res)
    hm = handling_metrics(res)
    sz = sizing_metrics(res, 26.82)
    assert rm["a_w_rms"] > 0 and hm["dtl_rms_frac"] > 0 and sz["N_eng_total"] > 10
    base = PassiveQuarterCar(C, ROAD, m_extra=GM).simulate(12.0)
    rb = ride_metrics(base)
    assert rb["a_w_rms"] > 0
    pn = p_net(e, GM, 26.82)
    assert pn["dP_ride"] is None and pn["P_net"] < pn["P_elec"]
