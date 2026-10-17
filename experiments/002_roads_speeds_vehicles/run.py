"""Experiment 002: roads x speeds x light vehicles. See config.yaml / README.md."""
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
    plt,
    run_sweep,
    save,
    standard_summary,
)

HERE = pathlib.Path(__file__).resolve().parent
CFG = load_cfg(HERE)
OUT = HERE / "results"


def cases():
    cs = []
    for v in CFG["vehicles"]:
        for k in CFG["classes"]:
            for s in CFG["speeds_mps"]:
                base = dict(vehicle=v, klass=k, speed=s, duration=CFG["duration_s"], damper_span="full", m_f=8.0)
                for seed in CFG["seeds"]:
                    cs.append(passive_case(base, seed))
                    for cg in CFG["c_gen"]:
                        for sc in CFG.get("c_s_scale", [1.0]):
                            cs.append(gate_case(base, seed, {"c_gen": cg, "r": CFG["r"], "J": CFG["J"],
                                                             "k_b_over_k_m": CFG["k_b_over_k_m"], "travel": CFG["travel_m"]},
                                                c_s_scale=sc))
    return cs


def analyse(df):
    g = attach_deltas(df)
    g["mph"] = (g["speed"] * 2.237).round(0)
    summ = standard_summary(g, ["vehicle", "klass", "mph", "c_s_scale", "c_gen"])
    best = summ.loc[summ.groupby(["vehicle", "klass", "mph", "c_s_scale"])["P_elec"].idxmax()]
    summ.to_csv(OUT / "summary.csv", index=False)
    best.to_csv(OUT / "best_load.csv", index=False)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=False)
    for ax, v in zip(axs, CFG["vehicles"]):
        b = best[best.vehicle == v]
        for (mph, sc), d in b.groupby(["mph", "c_s_scale"]):
            ax.errorbar(d["klass"], d["P_elec"], yerr=[d["P_elec"] - d["P_elec_lo"], d["P_elec_hi"] - d["P_elec"]],
                        marker="o", capsize=3, label=f"P_elec {mph:.0f} mph, damper x{sc:g}")
            if sc == 1.0:
                ax.plot(d["klass"], d["P_supply"], ls="--", marker="x", label=f"road supply {mph:.0f} mph")
        ax.set_title(v); ax.set_yscale("log"); ax.set_xlabel("ISO 8608 class"); ax.set_ylabel("W per corner")
        ax.legend(fontsize=6)
    save(fig, OUT / "fig_power_by_class.png", CFG, "exp002 power by class")
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, y in zip(axs, ["d_a_w_pct", "d_dtl_pct"]):
        for v in CFG["vehicles"]:
            for sc, b in best[(best.vehicle == v) & (best.mph == 60)].groupby("c_s_scale"):
                ax.plot(b["klass"], b[y], marker="o", label=f"{v}, damper x{sc:g}")
        ax.axhline(0, color="k", lw=0.8); ax.set_xlabel("ISO class (60 mph)"); ax.set_ylabel(y + " vs passive"); ax.legend(fontsize=7)
    save(fig, OUT / "fig_ride_handling_delta.png", CFG, "exp002 ride/handling deltas")
    cols = ["vehicle", "klass", "mph", "c_s_scale", "c_gen", "P_supply", "P_elec", "P_elec_lo", "P_elec_hi", "phi", "P_net",
            "d_a_w_pct", "d_dtl_pct", "t_stop", "rpm", "closure"]
    txt = ["## Results (auto-generated)", "", "### Best load per vehicle / class / speed (median over seeds; lo/hi = seed range)", "",
           md_table(best, cols, STD_FMT), "", "### All loads", "", md_table(summ, cols, STD_FMT)]
    (OUT / "RESULTS.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:6]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int); ap.add_argument("--analyse-only", action="store_true")
    a = ap.parse_args()
    df = pd.read_parquet(OUT / "results.parquet") if a.analyse_only else run_sweep(cases(), OUT, workers=a.workers)
    analyse(df)
