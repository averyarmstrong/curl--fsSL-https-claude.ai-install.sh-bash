"""Ride- and handling-constrained ceiling of the Gate (linear surrogate, exact H2).

For each vehicle and road class at 60 mph (and 30 mph for the heavy set):
grid over reflected generator damping c_eq = c_gen r^2, OEM damper scale, and
bias ratio; report (a) unconstrained max P_elec, (b) max P_elec subject to
W_k-proxy sprung acceleration <= passive and dynamic tire load <= passive
(+10%), (c) the Pareto frontier figure.  Milliseconds per point, so this is
the map the nonlinear sweeps are checked against.  Output: reports/linear_frontier.md + figures.
"""

from __future__ import annotations

import pathlib

import numpy as np
import pandas as pd

from aks_lab.metrics.net import mass_penalty
from aks_lab.validate.analytic import linear_gate_power, mean_road_power
from aks_lab.vehicles import corner, load_vehicles
from aks_lab.viz.plots import md_table, plt, save

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
R_REF, J_REF = 300.0, 3e-5          # low-inertance drive point (exp 001)


def grid(c, klass, speed, m_f=8.0, c_b=100.0, b=J_REF * R_REF**2):
    rows = []
    for ratio in (0.05, 0.12, 0.25, 0.5, 1.0):
        for sc in (1.0, 0.75, 0.5, 0.35, 0.25, 0.15, 0.1):
            for ce in np.logspace(1.5, 4.5, 31):
                r = linear_gate_power(c, klass, speed, c.k_m * ratio, ce, m_f=m_f, b_inert=b, c_s_scale=sc, c_b=c_b)
                rows.append({"ratio": ratio, "c_s_scale": sc, "c_eq": ce, **r})
    return pd.DataFrame(rows)


def frontier(df, pas, tol_dtl=1.10):
    ok = (df["rms_sprung_accel"] <= pas["rms_sprung_accel"]) & (df["rms_dyn_tire_load_frac"] <= tol_dtl * pas["rms_dyn_tire_load_frac"])
    best_free = df.loc[df["P_elec"].idxmax()]
    best_ok = df[ok].loc[df[ok]["P_elec"].idxmax()] if ok.any() else None
    return best_free, best_ok


def main():
    veh = load_vehicles()
    rows, figs = [], []
    for name in veh:
        c, gm = corner(name)
        speeds = (26.82,) if name in ("midsize_car", "f150", "hmmwv") else (13.41, 26.82)
        for v in speeds:
            for klass in "ABCD":
                pas = mean_road_power(c, klass, v)
                df = grid(c, klass, v)
                bf, bo = frontier(df, pas)
                dpm = mass_penalty(gm, v)
                row = {"vehicle": name, "mph": round(v * 2.237), "klass": klass, "P_supply": pas["P_road"],
                       "P_elec_max": bf["P_elec"], "phi_max": bf["phi"], "ratio_at_max": bf["ratio"], "c_s_at_max": bf["c_s_scale"],
                       "c_eq_at_max": bf["c_eq"], "accel_at_max_pct": 100 * (bf["rms_sprung_accel"] / pas["rms_sprung_accel"] - 1),
                       "dtl_at_max_pct": 100 * (bf["rms_dyn_tire_load_frac"] / pas["rms_dyn_tire_load_frac"] - 1)}
                if bo is not None:
                    row.update({"P_elec_ok": bo["P_elec"], "phi_ok": bo["phi"], "c_s_ok": bo["c_s_scale"], "c_eq_ok": bo["c_eq"],
                                "ratio_ok": bo["ratio"], "accel_ok_pct": 100 * (bo["rms_sprung_accel"] / pas["rms_sprung_accel"] - 1),
                                "dtl_ok_pct": 100 * (bo["rms_dyn_tire_load_frac"] / pas["rms_dyn_tire_load_frac"] - 1),
                                "P_net_ok": bo["P_elec"] - bo["P_friction"] - dpm, "frame_stroke_ok_mm": 1000 * bo["rms_frame_stroke"]})
                else:
                    row.update({"P_elec_ok": np.nan, "phi_ok": np.nan, "P_net_ok": np.nan})
                row["dP_mass"] = dpm
                rows.append(row)
                if name == "midsize_car" and klass == "C":
                    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
                    for sc, d in df[df.ratio == 0.12].groupby("c_s_scale"):
                        axs[0].plot(d["rms_sprung_accel"] / pas["rms_sprung_accel"], d["P_elec"], label=f"damper x{sc:g}")
                        axs[1].plot(d["rms_dyn_tire_load_frac"] / pas["rms_dyn_tire_load_frac"], d["P_elec"], label=f"damper x{sc:g}")
                    for ax, xl in zip(axs, ["sprung accel RMS / passive", "dyn tire load RMS / passive"]):
                        ax.axvline(1.0, color="k", lw=0.8); ax.set_xlabel(xl); ax.set_ylabel("P_elec [W]"); ax.set_xlim(0.3, 2.0)
                    axs[0].legend(fontsize=7)
                    fig.suptitle(f"Linear surrogate frontier — {name}, ISO {klass}, 60 mph, k_b/k_m=0.12, r={R_REF:.0f}, J={J_REF:.0e}; each curve sweeps c_eq")
                    figs.append(save(fig, OUT / "fig_linear_frontier_midsize_C.png", {"vehicle": name, "klass": klass}, "linear frontier"))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "linear_frontier.csv", index=False)
    fmt = {"P_supply": "{:.0f}", "P_elec_max": "{:.1f}", "phi_max": "{:.2f}", "c_eq_at_max": "{:.0f}", "accel_at_max_pct": "{:+.0f}",
           "dtl_at_max_pct": "{:+.0f}", "P_elec_ok": "{:.1f}", "phi_ok": "{:.2f}", "c_eq_ok": "{:.0f}", "accel_ok_pct": "{:+.0f}",
           "dtl_ok_pct": "{:+.0f}", "P_net_ok": "{:.1f}", "frame_stroke_ok_mm": "{:.1f}", "dP_mass": "{:.1f}", "c_s_at_max": "{:g}",
           "c_s_ok": "{:g}", "ratio_at_max": "{:g}", "ratio_ok": "{:g}"}
    md = ["# Linear-surrogate ceiling of the Gate (modeled; auto-generated by reports/linear_frontier.py)", "",
          "Exact H2 results for the linearised corner-with-Gate (frame stage = k_b ∥ c_eq ∥ J r² inerter; no stops, no "
          "freewheeling). Grid: bias ratio 0.05–1.0 × OEM damper scale 1.0–0.1 × c_eq 30–30,000 N·s/m. "
          f"r = {R_REF:.0f} rad/m, J = {J_REF:.0e} kg m², guide friction 100 N·s/m, η = 0.85. Two optima per row: "
          "**max** = unconstrained maximum electrical power (and what it costs in ride and tire load); "
          "**ok** = maximum subject to sprung-acceleration RMS ≤ passive and dynamic tire-load RMS ≤ 1.1 × passive. "
          "P_net_ok subtracts friction and the mass penalty of the vehicle's gate_mass estimate at that speed.", "",
          md_table(t, ["vehicle", "mph", "klass", "P_supply", "P_elec_max", "phi_max", "c_s_at_max", "accel_at_max_pct", "dtl_at_max_pct",
                       "P_elec_ok", "phi_ok", "c_s_ok", "c_eq_ok", "accel_ok_pct", "dtl_ok_pct", "frame_stroke_ok_mm", "dP_mass", "P_net_ok"], fmt),
          "", "Reading: the unconstrained maximum is reached by removing the OEM damper and letting the tire bounce "
          "(dtl +); it is not a design. The constrained optimum is the architecture's honest ceiling for small motions; "
          "the nonlinear sweeps (stops, freewheeling, inertance only when engaged) can only come in below it."]
    (OUT / "linear_frontier.md").write_text("\n".join(md) + "\n")
    print(t[["vehicle", "mph", "klass", "P_supply", "P_elec_max", "phi_max", "P_elec_ok", "phi_ok", "P_net_ok"]].round(2).to_string())


if __name__ == "__main__":
    main()
