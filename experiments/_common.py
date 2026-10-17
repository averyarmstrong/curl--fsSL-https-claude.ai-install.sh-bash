"""Shared helpers for experiments: case construction, passive-delta analysis, standard figures."""

from __future__ import annotations

import pathlib
import sys

import pandas as pd
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from aks_lab.sweeps.runner import run_sweep  # noqa: E402,F401
from aks_lab.validate.analytic import mean_road_power  # noqa: E402
from aks_lab.vehicles import corner  # noqa: E402
from aks_lab.viz.plots import md_table, plot_band, plt, save  # noqa: E402,F401

DELTA_COLS = (("a_w_rms", "d_a_w_rms"), ("sws_rms", "d_sws_rms"), ("dtl_rms_frac", "d_dtl_rms_frac"),
              ("a_s_rms", "d_a_s_rms"))


def load_cfg(here: pathlib.Path) -> dict:
    return yaml.safe_load((here / "config.yaml").read_text())


def gate_case(base: dict, seed: int, overrides: dict, tag="gate", **extra) -> dict:
    return {**base, "seed": seed, "tag": tag, "gate": overrides, **extra}


def passive_case(base: dict, seed: int, **extra) -> dict:
    return {**base, "seed": seed, "tag": "passive", "gate": None, **extra}


def attach_deltas(df: pd.DataFrame, keys=("vehicle", "klass", "speed", "seed")) -> pd.DataFrame:
    """Gate rows minus the passive row with the same (vehicle, road class, speed, seed)."""
    df = df[df["error"].isna()].copy() if "error" in df else df.copy()
    pas = df[~df["is_gate"]].set_index(list(keys))
    g = df[df["is_gate"]].copy()
    idx = pd.MultiIndex.from_frame(g[list(keys)])
    for col, new in DELTA_COLS:
        ref = pas.loc[idx, col].values
        g[new] = g[col].values - ref
        g[new + "_pct"] = 100 * g[new] / ref
    g["P_damper_passive"] = pas.loc[idx, "P_damper"].values
    g["Jr"] = g["gate_J"] * g["gate_r"] ** 2
    if "c_s_scale" not in g:
        g["c_s_scale"] = 1.0
    g["c_s_scale"] = g["c_s_scale"].fillna(1.0)
    g["P_supply_exact"] = [mean_road_power(corner(v)[0], k, s)["P_road"]
                           for v, k, s in zip(g["vehicle"], g["klass"], g["speed"])]
    return g


def standard_summary(g: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    return (g.groupby(by)
            .agg(P_supply=("P_supply_exact", "first"), P_road=("P_road", "median"),
                 P_elec=("P_elec", "median"), P_elec_lo=("P_elec", "min"), P_elec_hi=("P_elec", "max"),
                 phi=("phi", "median"), P_net=("P_net", "median"), eta_mech=("eta_mech", "median"),
                 damper_share=("damper_share", "median"), d_a_w_pct=("d_a_w_rms_pct", "median"),
                 d_dtl_pct=("d_dtl_rms_frac_pct", "median"), t_stop=("t_stop_frac", "median"),
                 N_stop_km=("N_stop_comp_per_km", "median"), x_b_rms=("x_b_rms", "median"),
                 rpm=("rpm_mean", "median"), rpm_p95=("rpm_p95", "median"), T_c_p99=("T_c_p99", "median"),
                 N_eng_km=("N_eng_A_per_km", "median"), kappa=("kappa", "median"),
                 closure=("closure", "max"), n=("P_elec", "size"))
            .reset_index())


STD_FMT = {"P_supply": "{:.0f}", "P_road": "{:.0f}", "P_elec": "{:.1f}", "P_elec_lo": "{:.1f}", "P_elec_hi": "{:.1f}",
           "phi": "{:.3f}", "P_net": "{:.1f}", "eta_mech": "{:.2f}", "damper_share": "{:.2f}",
           "d_a_w_pct": "{:+.1f}", "d_dtl_pct": "{:+.1f}", "t_stop": "{:.2f}", "N_stop_km": "{:.0f}",
           "x_b_rms": "{:.4f}", "rpm": "{:.0f}", "rpm_p95": "{:.0f}", "T_c_p99": "{:.2f}", "N_eng_km": "{:.0f}",
           "kappa": "{:.3f}", "closure": "{:.1e}", "speed": "{:.1f}", "c_gen": "{:.4g}", "c_s_scale": "{:g}"}
