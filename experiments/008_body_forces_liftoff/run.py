"""Experiment 008: body-force channel and tire lift-off. See config.yaml / README.md."""
import argparse
import pathlib
import sys

import pandas as pd

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

HERE = pathlib.Path(__file__).resolve().parent
CFG = load_cfg(HERE)
OUT = HERE / "results"


def cases():
    cs = []
    for v in CFG["vehicles"]:
        for k in CFG["classes"]:
            base = dict(vehicle=v, klass=k, speed=CFG["speed_mps"], duration=CFG["duration_s"], damper_span="full", m_f=8.0)
            for seed in CFG["seeds"]:
                for name, bf in CFG["body_forces"].items():
                    for one in CFG["tire_oneside"]:
                        if one and name != "none":
                            continue
                        extra = dict(body_force=bf, tire_oneside=one, bf_name=name)
                        cs.append(passive_case(base, seed, **extra))
                        cs.append(gate_case(base, seed, dict(CFG["gate"]), c_s_scale=CFG["c_s_scale"], **extra))
    return cs


def analyse(df):
    df = df[df["error"].isna()] if "error" in df else df
    g = attach_deltas(df, keys=("vehicle", "klass", "speed", "seed", "bf_name", "tire_oneside"))
    cols = ["vehicle", "klass", "bf_name", "tire_oneside"]
    summ = (g.groupby(cols).agg(P_supply=("P_supply_exact", "first"), P_road=("P_road", "median"),
                                P_body=("P_body", "median"), P_elec=("P_elec", "median"),
                                phi_total=("phi_total", "median"), liftoff=("liftoff_frac", "median"),
                                d_a_w_pct=("d_a_w_rms_pct", "median"), closure=("closure", "max")).reset_index())
    base = summ[(summ.bf_name == "none") & (~summ.tire_oneside)].set_index(["vehicle", "klass"])
    summ["dP_elec_vs_base"] = summ["P_elec"].values - base.loc[pd.MultiIndex.from_frame(summ[["vehicle", "klass"]]), "P_elec"].values
    summ.to_csv(OUT / "summary.csv", index=False)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    for ax, v in zip(axs, CFG["vehicles"]):
        d = summ[summ.vehicle == v]
        for (bf, one), dd in d.groupby(["bf_name", "tire_oneside"]):
            ax.plot(dd["klass"], dd["P_elec"], marker="o", label=f"{bf}{' + one-sided tire' if one else ''}")
        ax.plot(d[(d.bf_name == "none") & (~d.tire_oneside)]["klass"], d[(d.bf_name == "none") & (~d.tire_oneside)]["P_supply"],
                "k--", lw=0.8, label="road supply")
        ax.set_yscale("log"); ax.set_title(v); ax.set_xlabel("ISO class, 60 mph"); ax.set_ylabel("W per corner"); ax.legend(fontsize=6)
    save(fig, OUT / "fig_channels.png", CFG, "exp008 body forces and lift-off")
    fmt = {**STD_FMT, "P_body": "{:.2f}", "phi_total": "{:.3f}", "liftoff": "{:.4f}", "dP_elec_vs_base": "{:+.2f}", "P_elec": "{:.2f}"}
    txt = ["## Results (auto-generated)", "", "P_body = mean power the body-force channel delivers (per corner); dP_elec_vs_base = change in "
           "electrical output vs the road-only linear-tire case; liftoff = fraction of time the wheel is off the ground.", "",
           md_table(summ, cols + ["P_supply", "P_road", "P_body", "P_elec", "dP_elec_vs_base", "phi_total", "liftoff", "d_a_w_pct", "closure"], fmt)]
    (OUT / "RESULTS.md").write_text("\n".join(txt) + "\n")
    print("\n".join(txt[:6]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int); ap.add_argument("--analyse-only", action="store_true")
    a = ap.parse_args()
    df = pd.read_parquet(OUT / "results.parquet") if a.analyse_only else run_sweep(cases(), OUT, workers=a.workers)
    analyse(df)
