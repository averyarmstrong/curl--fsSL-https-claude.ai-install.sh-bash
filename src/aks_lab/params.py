"""Parameter loading with mandatory provenance.

params/params.yaml is the single source of truth.  Every leaf is a mapping
{value, units, provenance}; loading fails loudly if provenance is missing.
"""

from __future__ import annotations

import math
import pathlib
from dataclasses import dataclass

import yaml

DEFAULT_PARAMS_PATH = pathlib.Path(__file__).resolve().parents[2] / "params" / "params.yaml"


@dataclass(frozen=True)
class Params:
    """Mechanical parameters of the single-corner quarter-car + Gate model (SI)."""

    # suspension
    m_s: float = 560.0
    m_u: float = 65.0
    k_s: float = 32000.0
    c_s: float = 2900.0
    k_t: float = 250000.0
    # gate frame (soft-first series stage)
    m_f: float = 8.0
    k_b: float = 9600.0
    c_b: float = 100.0
    x_b_max: float = 0.0635
    k_stop: float = 2.0e6
    c_stop: float = 8.0e3
    # rectifier drivetrain
    lead: float = 0.0254        # m per screw revolution
    n_step: float = 6.0         # internal step-up ratio (generator shaft / screw shaft)
    J: float = 3.0e-4           # flywheel + rotor inertia at generator shaft, kg m^2
    c_w: float = 5.0e-5         # rotor windage/bearing viscous drag, N m s/rad
    c_od: float = 2.0e-4        # sprag overrunning drag (viscous equivalent), N m s/rad
    sprag_liftoff_rpm: float = 1200.0
    # numerics
    eps_engage: float = 1.0e-6  # rad/s hysteresis on engagement events

    @property
    def Gt(self) -> float:
        """Stroke-to-generator-shaft ratio, rad/s per m/s of frame stroke rate."""
        return 2.0 * math.pi * self.n_step / self.lead

    @property
    def Jr(self) -> float:
        """Rotor inertia reflected onto the frame stroke DOF, kg (inertance)."""
        return self.J * self.Gt**2


def _leaf(parent: dict, path: str) -> float:
    node = parent.get(path.rsplit(".", 1)[-1])
    if not isinstance(node, dict) or "value" not in node:
        raise ValueError(f"parameter '{path}' is not a {{value, units, provenance}} mapping")
    if "provenance" not in node or not str(node["provenance"]).strip():
        raise ValueError(f"parameter '{path}' has no provenance — forbidden (see CLAUDE.md)")
    return node["value"]


def missing_provenance(raw: dict, prefix: str = "") -> list[str]:
    """Walk the raw YAML tree; return dotted paths of leaves lacking provenance."""
    bad: list[str] = []
    for key, node in raw.items():
        path = f"{prefix}{key}"
        if key == "meta":
            continue
        if isinstance(node, dict) and "value" in node:
            if "provenance" not in node or not str(node.get("provenance", "")).strip():
                bad.append(path)
        elif isinstance(node, dict):
            bad.extend(missing_provenance(node, prefix=path + "."))
        else:
            bad.append(path)  # bare scalar leaf: no provenance possible
    return bad


def load_params(path: pathlib.Path | str = DEFAULT_PARAMS_PATH):
    """Load params.yaml -> (Params, raw dict).  Raises if any provenance is missing."""
    raw = yaml.safe_load(pathlib.Path(path).read_text())
    bad = missing_provenance(raw)
    if bad:
        raise ValueError(f"parameters missing provenance: {bad}")

    s, g = raw["suspension"], raw["gate"]
    k_s = _leaf(s, "suspension.k_s")
    p = Params(
        m_s=_leaf(s, "suspension.m_s"),
        m_u=_leaf(s, "suspension.m_u"),
        k_s=k_s,
        c_s=_leaf(s, "suspension.c_s"),
        k_t=_leaf(s, "suspension.k_t"),
        m_f=_leaf(g, "gate.m_f"),
        k_b=_leaf(g, "gate.k_b_over_k_s") * k_s,
        c_b=_leaf(g, "gate.c_b"),
        x_b_max=_leaf(g, "gate.x_b_max"),
        k_stop=_leaf(g, "gate.k_stop"),
        c_stop=_leaf(g, "gate.c_stop"),
        lead=_leaf(g, "gate.lead"),
        n_step=_leaf(g, "gate.n_step"),
        J=_leaf(g, "gate.J"),
        c_w=_leaf(g, "gate.c_w"),
        c_od=_leaf(g, "gate.c_od"),
        sprag_liftoff_rpm=_leaf(g, "gate.sprag_liftoff_rpm"),
    )
    return p, raw
