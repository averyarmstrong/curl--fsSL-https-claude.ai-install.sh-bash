"""Component-sizing outputs from time histories (Q5): sprag torque & cycles, flywheel, generator, stops."""

from __future__ import annotations

import math

import numpy as np

from ..elements.gate import ENG_A, ENG_B, SIGN


def clutch_torque_history(res):
    """T_c on the output grid (0 when free)."""
    t_c = np.zeros(res.t.size)
    modes = res.mode_at()
    qc = res._qc if hasattr(res, "_qc") else None
    if qc is None:
        return t_c, modes
    for i in np.where((modes == ENG_A) | (modes == ENG_B))[0]:
        s = SIGN[modes[i]]
        t_c[i] = qc._tc(s, res.t[i], res.y[:, i])
    return t_c, modes


def sizing_metrics(res, speed: float) -> dict:
    m = res.mask()
    T = res.t[-1] - res.t[int(np.argmax(m))]
    dist_km = speed * T / 1000.0
    counts = res.engage_counts()
    ev_t = np.array([e[0] for e in res.events]) if res.events else np.zeros(0)
    stationary = ev_t >= res.t_stationary if ev_t.size else np.zeros(0, bool)
    labels = [e[1] for e in res.events]
    n_a = sum(1 for k, lab in enumerate(labels) if stationary[k] and lab in ("engA", "lockA"))
    n_b = sum(1 for k, lab in enumerate(labels) if stationary[k] and lab in ("engB", "lockB"))
    impulses = [e[2].get("impulse", 0.0) for e in res.events if e[2] and "impulse" in e[2]]
    tc0 = [e[2].get("T_c0", 0.0) for e in res.events if e[2] and "T_c0" in e[2]]
    om = res.omega[m]
    p = res.gate.p
    rpm = om * 60 / (2 * math.pi)
    race_rpm = np.abs(res.frame_stroke_rate[m]) * p.r * 60 / (2 * math.pi)
    rb = res.frame_stroke[m]
    # stop contacts: rising edges of penetration
    comp = rb > p.x_c
    ext = rb < -p.x_e
    n_stop_c = int(np.sum(np.diff(comp.astype(int)) == 1))
    n_stop_e = int(np.sum(np.diff(ext.astype(int)) == 1))
    t_c, modes = clutch_torque_history(res)
    t_c = t_c[m]
    out = {
        "N_eng_A_per_km": n_a / dist_km if dist_km > 0 else np.nan,
        "N_eng_B_per_km": n_b / dist_km if dist_km > 0 else np.nan,
        "N_eng_total": counts["A"] + counts["B"],
        "T_c_max": float(np.max(t_c)) if t_c.size else 0.0,
        "T_c_p99": float(np.percentile(t_c[t_c > 0], 99)) if np.any(t_c > 0) else 0.0,
        "T_c_at_lock_max": float(np.max(tc0)) if tc0 else 0.0,
        "impulse_max": float(np.max(impulses)) if impulses else 0.0,
        "engaged_frac": float(np.mean((modes[m] == ENG_A) | (modes[m] == ENG_B))),
        "rpm_mean": float(np.mean(rpm)), "rpm_p05": float(np.percentile(rpm, 5)),
        "rpm_p95": float(np.percentile(rpm, 95)), "rpm_max": float(np.max(rpm)),
        "rpm_ripple_frac": float(np.std(rpm) / np.mean(rpm)) if np.mean(rpm) > 0 else np.nan,
        "frac_above_1600rpm": float(np.mean(rpm > 1600.0)),
        "race_rpm_max": float(np.max(race_rpm)),
        "race_rpm_margin_vs_liftoff": float(p.sprag_liftoff_rpm - np.max(race_rpm)),
        "N_stop_comp_per_km": n_stop_c / dist_km if dist_km > 0 else np.nan,
        "N_stop_ext_per_km": n_stop_e / dist_km if dist_km > 0 else np.nan,
        "zeno_warnings": len(res.warnings),
    }
    return out
