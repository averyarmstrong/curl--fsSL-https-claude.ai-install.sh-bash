"""The numba model must reproduce the reference model to solver tolerance (it is not a new physics)."""

import numpy as np
import pytest

pytest.importorskip("numba")

from aks_lab import QuarterCarGate, corner, gate_from_yaml, iso8608_profile  # noqa: E402
from aks_lab.vehicles.quarter_car_fast import QuarterCarGateFast  # noqa: E402

C, _ = corner("midsize_car")


@pytest.mark.parametrize("over,span", [({"r": 300.0, "J": 3e-5, "c_gen": 0.01}, "full"),
                                       ({"r": 300.0, "J": 3e-5, "c_gen": 0.01, "theta_bl": 0.005}, "main"),
                                       ({"r": 1484.0, "J": 3e-4, "c_gen": 0.002, "travel": 0.02, "T_cap": 2.0}, "full")])
def test_fast_matches_reference(over, span):
    road = iso8608_profile("C", 26.82, 6.0, seed=5)
    g = gate_from_yaml(C.k_m, over)
    ref = QuarterCarGate(C, g, road, damper_span=span).simulate(6.0)
    fast = QuarterCarGateFast(C, g, road, damper_span=span).simulate(6.0)
    assert fast.energy_audit()["closure"] < 0.01
    for i in (0, 2, 4, 6):
        scale = max(np.max(np.abs(ref.y[i])), 1e-9)
        assert np.max(np.abs(ref.y[i] - fast.y[i])) < 1e-4 * scale, i
    er, ef = ref.energies(), fast.energies()
    for k in ("E_elec", "E_damper", "E_road"):
        assert abs(er[k] - ef[k]) < 1e-3 * max(abs(er[k]), 1e-9), k
    assert ref.engage_counts() == fast.engage_counts()
