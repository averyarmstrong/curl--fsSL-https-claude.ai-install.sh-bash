"""Bench data reduction: raw shaker CSV -> cleaned -> the same metrics the model reports.

Expected raw CSV columns (any order, header names configurable):
    t [s], x [m] frame stroke (positive = collapse), F [N] actuator force
    (positive = resisting collapse), omega [rad/s] rotor speed (optional),
    v_dc [V], i_dc [A] (optional, electrical output)
Outputs a dict with the same keys as BenchResult.mean_powers + loop metrics,
so `bench/compare.py` can put model and measurement side by side.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt


def load_raw(path, cols=None) -> pd.DataFrame:
    cols = {"t": "t", "x": "x", "F": "F", "omega": "omega", "v": "v_dc", "i": "i_dc", **(cols or {})}
    df = pd.read_csv(path)
    out = pd.DataFrame({"t": df[cols["t"]].values, "x": df[cols["x"]].values, "F": df[cols["F"]].values})
    for k in ("omega", "v", "i"):
        if cols[k] in df:
            out[k] = df[cols[k]].values
    return out


def clean(df: pd.DataFrame, f_cut: float = 50.0, detrend: bool = True) -> pd.DataFrame:
    """Uniform resample, low-pass (zero-phase), remove static offsets of x and F."""
    t = df["t"].values
    dt = float(np.median(np.diff(t)))
    tu = np.arange(t[0], t[-1], dt)
    out = pd.DataFrame({"t": tu})
    b, a = butter(4, f_cut / (0.5 / dt))
    for c in df.columns:
        if c == "t":
            continue
        y = np.interp(tu, t, df[c].values)
        y = filtfilt(b, a, y)
        if detrend and c in ("x", "F"):
            y = y - np.mean(y)
        out[c] = y
    out["xdot"] = np.gradient(out["x"].values, dt)
    out.attrs["dt"] = dt
    return out


def cycles(df: pd.DataFrame, f_drive: float, n_skip: int = 3):
    """Split into drive cycles by zero-upcrossings of x; drop the first n_skip (start-up)."""
    x = df["x"].values
    up = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    return [(up[i], up[i + 1]) for i in range(n_skip, len(up) - 1)]


def reduce_run(df: pd.DataFrame, f_drive: float, k_b: float | None = None) -> dict:
    """Loop area per cycle, mean mechanical power in, electrical power, efficiency, rotor stats."""
    dt = df.attrs.get("dt", float(np.median(np.diff(df["t"]))))
    cyc = cycles(df, f_drive)
    if not cyc:
        raise ValueError("no complete cycles found")
    i0, i1 = cyc[0][0], cyc[-1][1]
    T = (i1 - i0) * dt
    x, F, xd = df["x"].values[i0:i1], df["F"].values[i0:i1], df["xdot"].values[i0:i1]
    w_in = float(np.trapezoid(F * xd, dx=dt))
    areas = [float(np.trapezoid(df["F"].values[a:b] * df["xdot"].values[a:b], dx=dt)) for a, b in cyc]
    out = {
        "n_cycles": len(cyc), "T": T, "f_drive": f_drive,
        "x_amp": float(0.5 * (x.max() - x.min())), "xdot_rms": float(np.std(xd)),
        "P_work_in": w_in / T, "loop_area_J_mean": float(np.mean(areas)), "loop_area_J_std": float(np.std(areas)),
    }
    if k_b is not None:
        # elastic component removed: F - k_b x is the non-conservative force
        out["P_nonconservative"] = float(np.trapezoid((F - k_b * x) * xd, dx=dt)) / T
    if "v" in df and "i" in df:
        p = df["v"].values[i0:i1] * df["i"].values[i0:i1]
        out["P_elec"] = float(np.mean(p))
        out["eta_bench"] = out["P_elec"] / out["P_work_in"] if out["P_work_in"] > 0 else np.nan
    if "omega" in df:
        om = df["omega"].values[i0:i1]
        out.update({"omega_mean": float(np.mean(om)), "omega_min": float(np.min(om)), "omega_max": float(np.max(om)),
                    "rpm_ripple_frac": float(np.std(om) / np.mean(om)) if np.mean(om) > 0 else np.nan,
                    "one_way": bool(np.min(om) > -1e-3)})
    # equivalent reflected damping: fit F_nc = c_eq * xdot  (c_eq ~ c_gen r^2 when engaged)
    if k_b is not None:
        fnc = F - k_b * x
        out["c_eq_fit"] = float(np.dot(fnc, xd) / np.dot(xd, xd))
    return out


def compare(model: dict, meas: dict, keys=("P_work_in", "P_elec", "omega_mean", "rpm_ripple_frac")) -> pd.DataFrame:
    rows = []
    for k in keys:
        if k in model and k in meas:
            m, b = model[k], meas[k]
            rows.append({"metric": k, "model": m, "bench": b, "bench/model": b / m if m else np.nan})
    return pd.DataFrame(rows)
