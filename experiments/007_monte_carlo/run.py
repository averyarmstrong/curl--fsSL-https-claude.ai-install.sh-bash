"""Experiment 007: Monte Carlo bands over open parameters at the constrained design point. See config.yaml."""
import argparse
import pathlib
import sys

import numpy as np
import pandas as pd
from scipy.stats import qmc

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _common import (  # noqa: E402
    STD_FMT,
    attach_deltas,
    gate_case,
    load_cfg,
    md_table,
    passive_case,
    plt,
    run_sweep,
    save,
)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from aks_lab.vehicles import corner  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
CFG = load_cfg(HERE)
OUT = HERE / "results"
UNIFORM = {"theta_bl", "travel", "eq_fraction", "eta", "m_f", "delta_m_scale"}


def samples(vehicle=None):
    names = list(CFG["ranges"])
    ranges = dict(CFG["ranges"])
    if vehicle in CFG.get("c_eq_target_by_vehicle", {}):
        ranges["c_eq_target"] = CFG["c_eq_target_by_vehicle"][vehicle]
    u = qmc.LatinHypercube(d=len(names), seed=7).random(CFG["n_samples"])
    rows = []
    for k, row in enumerate(u):
        s = {}
        for j, n in enumerate(names):
            lo, hi = ranges[n]
            s[n] = float(lo + (hi - lo) * row[j]) if n in UNIFORM else float(np.exp(np.log(lo) + (np.log(hi) - np.log(lo)) * row[j]))
        s["sample"] = k
        rows.append(s)
    return rows


def cases():
    d = CFG["design"]
    cs = []
    for v in CFG["vehicles"]:
        _, gm = corner(v)
        for klass in CFG["classes"]:
            base = dict(vehicle=v, klass=klass, speed=CFG["speed_mps"], duration=CFG["duration_s"], damper_span="full")
            for s in samples(v):
                seed = 100 + s["sample"]
                cs.append(passive_case({**base, "m_f": 8.0}, seed, delta_m=gm * s["delta_m_scale"]))
                over = {"r": d["r"], "c_gen": s["c_eq_target"] / d["r"] ** 2, "J": s["J"], "c_b": s["c_b"], "c_od": s["c_od"],
                        "c_w": s["c_w"], "theta_bl": s["theta_bl"], "k_b_over_k_m": s["k_b_over_k_m"], "travel": s["travel"],
                        "eq_fraction": s["eq_fraction"], "eta": s["eta"]}
                cs.append(gate_case({**base, "m_f": s["m_f"]}, seed, over, c_s_scale=d["c_s_scale"],
                                    delta_m=gm * s["delta_m_scale"], sample=s["sample"]))
    return cs


def analyse(df):
    from aks_lab.sweeps.cases import case_id
    live = {case_id(c) for c in cases()}
    df = df[df["case_id"].isin(live)]          # drop rows superseded by a config correction
    g = attach_deltas(df)
    rows = []
    for (v, k), d in g.groupby(["vehicle", "klass"]):
        q = lambda col, p: float(np.nanpercentile(d[col], p))  # noqa: E731
        rows.append({"vehicle": v, "klass": k, "n": len(d), "P_supply": d["P_supply_exact"].iloc[0],
                     "P_elec_p05": q("P_elec", 5), "P_elec_p50": q("P_elec", 50), "P_elec_p95": q("P_elec", 95),
                     "phi_p50": q("phi", 50), "P_net_p05": q("P_net", 5), "P_net_p50": q("P_net", 50), "P_net_p95": q("P_net", 95),
                     "d_a_w_pct_p50": q("d_a_w_rms_pct", 50), "d_dtl_pct_p50": q("d_dtl_rms_frac_pct", 50),
                     "t_stop_p50": q("t_stop_frac", 50), "t_stop_p95": q("t_stop_frac", 95),
                     "N_eng_km_p50": q("N_eng_A_per_km", 50), "T_c_p99_p95": q("T_c_p99", 95), "closure_max": d["closure"].max()})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "bands.csv", index=False)
    fig, axs = plt.subplots(1, 3, figsize=(14, 4))
    for ax, y in zip(axs, ["P_elec", "P_net", "d_a_w_rms_pct"]):
        for v, d in g.groupby("vehicle"):
            med = d.groupby("klass")[y].median()
            lo = d.groupby("klass")[y].quantile(0.05)
            hi = d.groupby("klass")[y].quantile(0.95)
            ax.errorbar(med.index, med.values, yerr=[med - lo, hi - med], marker="o", capsize=3, label=v)
        ax.set_xlabel("ISO class, 60 mph"); ax.set_ylabel(y); ax.legend(fontsize=7)
        if y != "d_a_w_rms_pct":
            ax.set_yscale("symlog", linthresh=10)
    save(fig, OUT / "fig_bands.png", CFG, "exp007 Monte Carlo bands")
    # rank parameter influence on P_elec by Spearman correlation
    import json
    gg = g.copy()
    ov = gg["gate"].map(json.loads)
    for n in ("J", "c_gen", "c_b", "c_od", "c_w", "theta_bl", "k_b_over_k_m", "travel", "eq_fraction", "eta"):
        gg[n] = ov.map(lambda o, n=n: o[n])
    corr = (gg.groupby(["vehicle", "klass"])[["P_elec", "J", "c_gen", "c_b", "c_od", "c_w", "theta_bl", "k_b_over_k_m", "travel", "eq_fraction", "eta", "m_f"]]
            .corr(method="spearman")["P_elec"].unstack().drop(columns="P_elec"))
    corr.to_csv(OUT / "spearman_P_elec.csv")
    fmt = {**STD_FMT, "P_elec_p05": "{:.1f}", "P_elec_p50": "{:.1f}", "P_elec_p95": "{:.1f}", "phi_p50": "{:.3f}",
           "P_net_p05": "{:.1f}", "P_net_p50": "{:.1f}", "P_net_p95": "{:.1f}", "d_a_w_pct_p50": "{:+.1f}", "d_dtl_pct_p50": "{:+.1f}",
           "t_stop_p50": "{:.2f}", "t_stop_p95": "{:.2f}", "N_eng_km_p50": "{:.0f}", "T_c_p99_p95": "{:.2f}", "closure_max": "{:.1e}"}
    txt = ["## Results (auto-generated)", "", f"Bands = 5–95% over {CFG['n_samples']} Latin-hypercube samples of the open parameters "
           "(each with its own road seed) at the constrained design point; 60 mph.", "",
           md_table(t, list(t.columns), fmt), "", "### Spearman rank correlation of P_elec with each open parameter", "",
           md_table(corr.round(2).reset_index(), list(corr.reset_index().columns), {c: "{:+.2f}" for c in corr.columns})]
    (OUT / "RESULTS.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:6]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int); ap.add_argument("--analyse-only", action="store_true")
    a = ap.parse_args()
    df = pd.read_parquet(OUT / "results.parquet") if a.analyse_only else run_sweep(cases(), OUT, workers=a.workers)
    analyse(df)
