"""Experiment 006: flywheel sweep and tornado sensitivity. See config.yaml / README.md."""
import argparse
import pathlib
import sys

import numpy as np
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
BASE_CASE = dict(vehicle=CFG["vehicle"], klass=CFG["klass"], speed=CFG["speed_mps"], duration=CFG["duration_s"],
                 damper_span="full", m_f=8.0)


def cases():
    cs = []
    b = CFG["baseline"]
    for seed in CFG["seeds"]:
        cs.append(passive_case(BASE_CASE, seed))
        cs.append(gate_case(BASE_CASE, seed, dict(b), sweep="baseline", param="baseline", level="base"))
        for J in CFG["J_sweep"]:
            cs.append(gate_case(BASE_CASE, seed, {**b, "J": J}, sweep="J", param="J", level=str(J)))
        for name, (lo, hi) in CFG["tornado"].items():
            for lev, val in (("lo", lo), ("hi", hi)):
                if name == "m_f":
                    cs.append(gate_case({**BASE_CASE, "m_f": val}, seed, dict(b), sweep="tornado", param=name, level=lev))
                elif name == "damper_span":
                    cs.append(gate_case({**BASE_CASE, "damper_span": val}, seed, dict(b), sweep="tornado", param=name, level=lev))
                else:
                    cs.append(gate_case(BASE_CASE, seed, {**b, name: val}, sweep="tornado", param=name, level=lev))
    return cs


def analyse(df):
    g = attach_deltas(df)
    js = g[g["sweep"].isin(["J", "baseline"])]
    sj = standard_summary(js, ["gate_J"]); sj["Jr"] = sj["gate_J"] * CFG["baseline"]["r"] ** 2
    fig, axs = plt.subplots(1, 4, figsize=(15, 3.6))
    for ax, y in zip(axs, ["P_elec", "rpm_ripple_frac", "engaged_frac", "d_a_w_rms_pct"]):
        plot_band(ax, js, "gate_J", y, logx=True)
    save(fig, OUT / "fig_flywheel.png", CFG, "exp006 flywheel sweep")
    # tornado
    base = g[g["sweep"] == "baseline"]
    tor = g[g["sweep"] == "tornado"]
    rows = []
    for metric in ("P_elec", "P_net", "d_a_w_rms_pct", "t_stop_frac"):
        b0 = base[metric].median()
        for p, d in tor.groupby("param"):
            lo = d[d.level == "lo"][metric].median(); hi = d[d.level == "hi"][metric].median()
            rows.append(dict(metric=metric, param=p, base=b0, lo=lo, hi=hi, span=abs(hi - lo)))
    tdf = pd.DataFrame(rows)
    tdf.to_csv(OUT / "tornado.csv", index=False)
    fig, axs = plt.subplots(1, 4, figsize=(16, 4.5))
    for ax, metric in zip(axs, ("P_elec", "P_net", "d_a_w_rms_pct", "t_stop_frac")):
        d = tdf[tdf.metric == metric].sort_values("span")
        y = np.arange(len(d))
        ax.barh(y, d["lo"] - d["base"], left=d["base"], color="tab:blue", label="low end")
        ax.barh(y, d["hi"] - d["base"], left=d["base"], color="tab:orange", label="high end")
        ax.set_yticks(y); ax.set_yticklabels(d["param"]); ax.axvline(d["base"].iloc[0], color="k", lw=0.8)
        ax.set_title(metric); ax.legend(fontsize=6)
    save(fig, OUT / "fig_tornado.png", CFG, "exp006 tornado")
    cols = ["gate_J", "Jr", "P_elec", "P_elec_lo", "P_elec_hi", "phi", "P_net", "rpm", "rpm_p95", "d_a_w_pct", "closure"]
    txt = ["## Results (auto-generated)", "", "### Flywheel sweep (r = %s)" % CFG["baseline"]["r"], "",
           md_table(sj, cols, {**STD_FMT, "gate_J": "{:.0e}", "Jr": "{:.1f}"}), "", "### Tornado (median over seeds)", "",
           md_table(tdf.sort_values(["metric", "span"], ascending=[True, False]), ["metric", "param", "base", "lo", "hi", "span"],
                    {"base": "{:.2f}", "lo": "{:.2f}", "hi": "{:.2f}", "span": "{:.2f}"})]
    (OUT / "RESULTS.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:6]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int); ap.add_argument("--analyse-only", action="store_true")
    a = ap.parse_args()
    df = pd.read_parquet(OUT / "results.parquet") if a.analyse_only else run_sweep(cases(), OUT, workers=a.workers)
    analyse(df)
