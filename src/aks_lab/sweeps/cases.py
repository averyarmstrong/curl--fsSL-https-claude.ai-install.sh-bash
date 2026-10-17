"""One simulation case -> one flat result row.  Used by every experiment.

A case is a plain dict (JSON-serialisable) so it can be logged, hashed and
re-run.  Keys:
  vehicle: name in vehicles.yaml        klass: ISO class A-E     speed: m/s
  duration: s                           seed: int
  gate: None (passive baseline) or {overrides...} for gate_from_yaml
  m_f: moving plate mass (kg)           damper_span: "full" | "main"
  delta_m: added hardware mass (kg)     tag: free text
  c_s_scale: OEM damper scale on the Gate corner (baseline keeps 1.0)
  fast: use the numba model when available (default True)
  body_force: None or {"rms": N, "f_lo": Hz, "f_hi": Hz} band-limited white force on the sprung mass
  tire_oneside: bool, contact lost when total tire force would go negative
"""

from __future__ import annotations

import hashlib
import json
import time
import traceback

import numpy as np

from ..metrics import energy_metrics, handling_metrics, p_net, ride_metrics, sizing_metrics
from ..params import gate_from_yaml
from ..roads import iso8608_profile
from ..roads.body_force import band_limited_force
from ..vehicles import PassiveQuarterCar, QuarterCarGate, corner

try:  # numba-compiled RHS, equivalent to the reference to 1e-4 (tests/test_fast_equivalence.py)
    from ..vehicles.quarter_car_fast import QuarterCarGateFast as _FastModel
except Exception:  # noqa: BLE001
    _FastModel = None


def case_id(case: dict) -> str:
    return hashlib.sha1(json.dumps(case, sort_keys=True, default=str).encode()).hexdigest()[:12]


def _clean(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if isinstance(v, (np.floating, np.integer)):
            v = v.item()
        out[k] = v
    return out


def run_case(case: dict) -> dict:
    t0 = time.time()
    row = {"case_id": case_id(case), **{k: (json.dumps(v) if isinstance(v, dict) else v) for k, v in case.items()}}
    try:
        c, gm = corner(case["vehicle"])
        dm = case.get("delta_m", gm)
        road = iso8608_profile(case["klass"], case["speed"], case["duration"], seed=case["seed"])
        if case.get("tire_oneside"):
            from dataclasses import replace
            c = replace(c, tire_oneside=True)
        bf = case.get("body_force")
        f_body = None
        if bf:
            f_body = band_limited_force(bf["rms"], bf.get("f_lo", 0.2), bf.get("f_hi", 3.0),
                                        case["duration"], seed=10_000 + case["seed"])
        needs_ref = bool(bf) or bool(case.get("tire_oneside"))
        if case.get("gate") is None:
            res = PassiveQuarterCar(c, road, m_extra=dm, f_body=f_body).simulate(case["duration"])
            row["is_gate"] = False
        else:
            g = gate_from_yaml(c.k_m, case["gate"])
            cs_scale = float(case.get("c_s_scale", 1.0))
            if cs_scale != 1.0:   # the Gate corner may carry a smaller OEM damper; the baseline keeps stock
                from dataclasses import replace
                c = replace(c, c_s=c.c_s * cs_scale)
            use_fast = _FastModel is not None and case.get("fast", True) and not needs_ref
            model = _FastModel if use_fast else QuarterCarGate
            kw = {} if use_fast else {"f_body": f_body}
            res = model(c, g, road, m_f=case.get("m_f", 8.0),
                        damper_span=case.get("damper_span", "full"), **kw).simulate(case["duration"])
            row["is_gate"] = True
            row["model"] = model.__name__
            row.update({f"gate_{k}": v for k, v in g.describe().items() if k != "generator"})
            row["c_gen"] = g.gen.c_gen
            row["eta_gen"] = g.gen.eta
        audit = res.energy_audit()
        row["closure"] = audit["closure"]
        if audit["closure"] > 0.01:
            row["error"] = f"closure {audit['closure']:.3e} > 1%"
        row.update(energy_metrics(res))
        row.update(ride_metrics(res))
        row.update(handling_metrics(res))
        if res.has_gate:
            row.update(sizing_metrics(res, case["speed"]))
            pn = p_net(energy_metrics(res), dm, case["speed"])
            row["dP_mass"] = pn["dP_mass"]
            row["P_net"] = pn["P_net"]
        row["n_rhs"] = res.n_rhs
        row["n_warnings"] = len(res.warnings)
        row["static_load"] = c.static_load
        row["k_t"] = c.k_t
        row["k_m"] = c.k_m
    except Exception as exc:  # noqa: BLE001 — a failed case is a result, not a crash
        row["error"] = f"{type(exc).__name__}: {exc}"
        row["traceback"] = traceback.format_exc()[-2000:]
    row["runtime_s"] = time.time() - t0
    return _clean(row)
