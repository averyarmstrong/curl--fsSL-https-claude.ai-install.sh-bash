"""Provenance-enforcing parameter loading.

params/gate_baseline.yaml is the single source of truth for the Gate unit.
Every leaf is {value, units, provenance}; loading fails loudly otherwise.
"""

from __future__ import annotations

import math
import pathlib

import yaml

from .elements.gate import Gate, GateParams
from .elements.generator import LinearGenerator

ROOT = pathlib.Path(__file__).resolve().parents[2]
GATE_YAML = ROOT / "params" / "gate_baseline.yaml"


def missing_provenance(raw: dict, prefix: str = "") -> list[str]:
    bad: list[str] = []
    for key, node in raw.items():
        path = f"{prefix}{key}"
        if key == "meta":
            continue
        if isinstance(node, dict) and "value" in node:
            if not str(node.get("provenance", "")).strip():
                bad.append(path)
        elif isinstance(node, dict):
            bad.extend(missing_provenance(node, prefix=path + "."))
        else:
            bad.append(path)
    return bad


def load_gate_raw(path=GATE_YAML) -> dict:
    raw = yaml.safe_load(pathlib.Path(path).read_text())
    bad = missing_provenance(raw)
    if bad:
        raise ValueError(f"parameters missing provenance: {bad}")
    return raw


def _v(node, key):
    return node[key]["value"]


def gate_from_yaml(k_m: float, overrides: dict | None = None, path=GATE_YAML) -> Gate:
    """Build a Gate for a host whose main spring rate is k_m. overrides: {field: value}."""
    raw = load_gate_raw(path)
    o = dict(overrides or {})
    ratio = o.pop("k_b_over_k_m", _v(raw, "k_b_over_k_m"))
    travel = o.pop("travel", _v(raw, "travel"))
    eqf = o.pop("eq_fraction", _v(raw, "eq_fraction"))
    c_gen = o.pop("c_gen", _v(raw["generator"], "c_gen"))
    eta = o.pop("eta", _v(raw["generator"], "eta"))
    t_cap = _v(raw, "T_cap")
    fields = dict(
        k_b=ratio * k_m,
        c_b=_v(raw, "c_b"), x_c=eqf * travel, x_e=(1 - eqf) * travel,
        k_stop=_v(raw, "k_stop"), c_stop=_v(raw, "c_stop"), r=_v(raw, "r"), J=_v(raw, "J"),
        c_w=_v(raw, "c_w"), c_od=_v(raw, "c_od"), theta_bl=_v(raw, "theta_bl"),
        T_cap=math.inf if t_cap is None else float(t_cap),
        sprag_liftoff_rpm=_v(raw, "sprag_liftoff_rpm"),
    )
    if "k_b" in o:
        fields["k_b"] = o.pop("k_b")
    fields.update(o)
    return Gate(GateParams(**fields), LinearGenerator(c_gen, eta))
