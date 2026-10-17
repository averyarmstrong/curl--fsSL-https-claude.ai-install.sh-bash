"""Experiment 004: transmission ratio sweep. See config.yaml / README.md."""
import argparse
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _common import (
    STD_FMT,
    attach_deltas,
    gate_case,
    load_cfg,
    md_table,
    passive_case,
    plot_band,
    plt,
    run_sweep,
    save,
    standard_summary,
)

HERE = pathlib.Path(__file__).resolve().parent
CFG = load_cfg(HERE)
OUT = HERE / "results"


def cases():
    base = dict(vehicle=CFG["vehicle"], klass=CFG["klass"], speed=CFG["speed_mps"], duration=CFG["duration_s"],
                damper_span="full", m_f=8.0)
    cs = []
    for seed in CFG["seeds"]:
        cs.append(passive_case(base, seed))
        for r in CFG["r"]:
            for J in CFG["J"]:
                for sc in CFG["c_gen_scale"]:
                    cg = sc * CFG["c_gen_ref"] * (300.0 / r) ** 2
                    cs.append(gate_case(base, seed, {"c_gen": cg, "r": r, "J": J, "k_b_over_k_m": CFG["k_b_over_k_m"],
                                                     "travel": CFG["travel_m"]}, c_gen_scale=sc))
    return cs


def analyse(df):
    g = attach_deltas(df)
    g["c_reflected"] = g["c_gen"] * g["gate_r"] ** 2
    summ = standard_summary(g, ["gate_J", "gate_r", "c_gen_scale"])
    summ["Jr"] = summ["gate_J"] * summ["gate_r"] ** 2
    summ.to_csv(OUT / "summary.csv", index=False)
    best = summ.loc[summ.groupby(["gate_J", "gate_r"])["P_elec"].idxmax()]
    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    g["J_label"] = g["gate_J"].map(lambda j: f"J={j:.0e}")
    for ax, y in zip(axs.flat, ["P_elec", "phi", "eta_mech", "N_eng_A_per_km", "race_rpm_max", "d_a_w_rms_pct"]):
        bb = g[g["c_gen_scale"] == 1.0]
        plot_band(ax, bb, "gate_r", y, group="J_label", logx=True)
        ax.legend(fontsize=6)
    axs[1, 1].axhline(1200, color="r", ls="--", lw=0.8, label="sprag lift-off (catalog mid)")
    save(fig, OUT / "fig_ratio_sweep.png", CFG, "exp004 ratio sweep (c_gen scale 1)")
    cols = ["gate_J", "gate_r", "Jr", "c_gen_scale", "P_elec", "P_elec_lo", "P_elec_hi", "phi", "eta_mech", "P_net",
            "d_a_w_pct", "d_dtl_pct", "N_eng_km", "rpm_p95", "T_c_p99", "closure"]
    fmt = {**STD_FMT, "Jr": "{:.1f}", "gate_J": "{:.0e}", "gate_r": "{:.0f}"}
    txt = ["## Results (auto-generated)", "", "### Best load scale per (J, r)", "", md_table(best, cols, fmt), "",
           "### All", "", md_table(summ, cols, fmt)]
    (OUT / "RESULTS.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:6]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int); ap.add_argument("--analyse-only", action="store_true")
    a = ap.parse_args()
    df = pd.read_parquet(OUT / "results.parquet") if a.analyse_only else run_sweep(cases(), OUT, workers=a.workers)
    analyse(df)
