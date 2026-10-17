from __future__ import annotations

import pathlib

import yaml

from .quarter_car import CornerParams, PassiveQuarterCar, QuarterCarGate, SimResult

_YAML = pathlib.Path(__file__).with_name("vehicles.yaml")


def _leaf(node, key):
    v = node[key]
    if not isinstance(v, dict) or "value" not in v or not str(v.get("provenance", "")).strip():
        raise ValueError(f"vehicle parameter {key} lacks {{value, units, provenance}}")
    return v["value"]


def load_vehicles() -> dict:
    return yaml.safe_load(_YAML.read_text())


def corner(name: str) -> tuple[CornerParams, float]:
    """Return (CornerParams, gate_mass_estimate) for a named vehicle."""
    raw = load_vehicles()[name]
    c = CornerParams(m_s=_leaf(raw, "m_s"), m_u=_leaf(raw, "m_u"), k_m=_leaf(raw, "k_m"),
                     c_s=_leaf(raw, "c_s"), k_t=_leaf(raw, "k_t"), name=name)
    return c, _leaf(raw, "gate_mass")


__all__ = ["CornerParams", "PassiveQuarterCar", "QuarterCarGate", "SimResult", "corner", "load_vehicles"]
