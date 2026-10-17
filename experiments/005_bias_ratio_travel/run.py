"""Experiment 005: bias-spring ratio x travel. See config.yaml / README.md."""
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
        for kb in CFG["k_b_over_k_m"]:
            for tr in CFG["travel_m"]:
                for cg in CFG["c_gen"]:
                    cs.append(gate_case(base, seed, {"c_gen": cg, "r": CFG["r"], "J": CFG["J"],
                                                     "k_b_over_k_m": kb, "travel": tr}, kb_ratio=kb, travel=tr))
    return cs


def analyse(df):
    g = attach_deltas(df)
    g["travel_in"] = (g["travel"] * 39.37).round(1)
    summ = standard_summary(g, ["kb_ratio", "travel_in", "c_gen"])
    summ.to_csv(OUT / "summary.csv", index=False)
    best = summ.loc[summ.groupby(["kb_ratio", "travel_in"])["P_elec"].idxmax()]
    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    g["tr_label"] = g["travel_in"].map(lambda t: f"travel {t} in")
    for ax, y in zip(axs.flat, ["P_elec", "phi", "t_stop_frac", "N_stop_comp_per_km", "d_a_w_rms_pct", "d_dtl_rms_frac_pct"]):
        bb = g.loc[g.groupby(["kb_ratio", "travel_in", "seed"])["P_elec"].idxmax()]
        plot_band(ax, bb, "kb_ratio", y, group="tr_label", logx=True)
        ax.legend(fontsize=6)
    save(fig, OUT / "fig_ratio_travel.png", CFG, "exp005 best-load metrics vs k_b/k_m and travel")
    cols = ["kb_ratio", "travel_in", "c_gen", "P_elec", "P_elec_lo", "P_elec_hi", "phi", "P_net", "t_stop", "N_stop_km",
            "x_b_rms", "d_a_w_pct", "d_dtl_pct", "closure"]
    txt = ["## Results (auto-generated)", "", "### Best load per (ratio, travel)", "", md_table(best, cols, STD_FMT),
           "", "### All", "", md_table(summ, cols, STD_FMT)]
    (OUT / "RESULTS.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:6]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int); ap.add_argument("--analyse-only", action="store_true")
    a = ap.parse_args()
    df = pd.read_parquet(OUT / "results.parquet") if a.analyse_only else run_sweep(cases(), OUT, workers=a.workers)
    analyse(df)
