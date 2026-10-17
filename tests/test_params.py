"""Provenance and parameter-integrity tests (foundation principle: every number carries its source)."""

import math

from aks_lab import gate_from_yaml, load_gate_raw
from aks_lab.params import missing_provenance
from aks_lab.vehicles import corner, load_vehicles


def test_every_gate_parameter_has_provenance():
    assert missing_provenance(load_gate_raw()) == []


def test_every_vehicle_parameter_has_provenance():
    for name, raw in load_vehicles().items():
        for key, node in raw.items():
            if key == "note":
                continue
            assert isinstance(node, dict) and "value" in node and node.get("provenance"), (name, key)


def test_patent_constraint_soft_first():
    """Claims 2/11: bias spring rate strictly lower than the main spring rate."""
    for name in load_vehicles():
        c, _ = corner(name)
        g = gate_from_yaml(c.k_m)
        assert g.p.k_b < c.k_m, name


def test_vehicle_modes_sane():
    for name in load_vehicles():
        c, _ = corner(name)
        assert 0.9 <= c.body_hz <= 2.2, (name, c.body_hz)
        assert 7.0 <= c.hop_hz <= 20.0, (name, c.hop_hz)
        zeta = c.c_s / (2 * math.sqrt(c.k_m * c.m_s))
        zmax = load_vehicles()[name].get("zeta_max", {}).get("value", 0.45)
        assert 0.2 <= zeta <= zmax, (name, zeta)


def test_overrides_apply():
    c, _ = corner("midsize_car")
    g = gate_from_yaml(c.k_m, {"r": 300.0, "J": 1e-3, "c_gen": 0.01, "k_b_over_k_m": 0.25})
    assert g.p.r == 300.0 and g.p.J == 1e-3 and g.gen.c_gen == 0.01
    assert math.isclose(g.p.k_b, 0.25 * c.k_m)
