"""Energy metrics: phi, phi_s, efficiencies, reactive spring power, kappa (legacy shorthand)."""

from __future__ import annotations

import numpy as np


def energy_metrics(res) -> dict:
    r = res.rates()
    m = res.mask()
    k_m = res.corner.k_m
    r_m = res.main_stroke[m]
    dr_m = np.gradient(r_m, res.t[m])
    p_spring_cycle = float(np.mean(np.abs(k_m * r_m * dr_m)))
    p_road = r["P_road"]
    out = {
        "P_road": p_road,
        "P_elec": r["P_elec"],
        "P_gate": r["P_gate"],
        "P_frame": r["P_frame"],
        "P_damper": r["P_damper"],
        "P_friction_total": r["P_friction"] + r["P_clutch"] + r["P_genloss"] + r["P_stop"],
        "P_friction_guide": r["P_friction"],
        "P_clutch": r["P_clutch"],
        "P_genloss_windage": r["P_genloss"],
        "P_stop": r["P_stop"],
        "P_spring_cycle": p_spring_cycle,
        "phi": r["P_elec"] / p_road if p_road > 0 else np.nan,
        "phi_s": r["P_elec"] / p_spring_cycle if p_spring_cycle > 0 else np.nan,
        "eta_mech": r["P_gate"] / r["P_frame"] if r["P_frame"] > 0 else np.nan,
        "eta_chain": r["P_elec"] / r["P_gate"] if r["P_gate"] > 0 else np.nan,
        "damper_share": r["P_damper"] / p_road if p_road > 0 else np.nan,
    }
    v_susp = float(np.std(np.gradient(res.susp_stroke[m], res.t[m])))
    out["v_susp_rms"] = v_susp
    out["kappa"] = r["P_elec"] / (res.corner.static_load * v_susp) if v_susp > 0 else np.nan
    return out
