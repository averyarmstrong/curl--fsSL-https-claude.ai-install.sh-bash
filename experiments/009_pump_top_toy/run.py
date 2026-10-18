"""Experiment 009: the pump top. Spin-up ceiling, per-push ledger, half- vs full-wave, load, spin-down."""
import pathlib
from dataclasses import replace

import matplotlib
import numpy as np
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from aks_lab.toy import PumpTop, PumpTopParams  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "results"
CFG = yaml.safe_load((HERE / "config.yaml").read_text())
T = CFG["duration_s"]
BASE = PumpTopParams()


def md(rows, cols):
    s = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for r in rows:
        s += "| " + " | ".join(str(r[c]) for c in cols) + " |\n"
    return s


def main():
    OUT.mkdir(exist_ok=True)
    lines = ["# Experiment 009 — results (all `modeled` on `asserted` toy parameters)\n"]

    # 1. spin-up, per push
    r = PumpTop(BASE).simulate(T)
    pp = r.per_push()
    a = r.energy_audit()
    rows = [{"push": q["push"], "W_hand [J]": f"{q['W_hand']:.3f}", "ΔKE_rotor [J]": f"{q['dKE_rotor']:.3f}",
             "losses [J]": f"{q['losses']:.3f}", "ω_end [rad/s]": f"{q['omega_end']:.1f}",
             "v_peak [m/s]": f"{q['v_peak_down']:.2f}", "r·v_peak [rad/s]": f"{BASE.r * q['v_peak_down']:.1f}"} for q in pp]
    lines += ["## 1. Spin-up, baseline toy (lead 25 mm/rev, 15 N hand, 1 m/s hand limit)\n",
              md(rows, list(rows[0].keys())),
              f"\nLedger over {T:.0f} s: hand {a['E_hand']:.2f} J = rotor KE {a['dKE_rotor']:.2f} + screw {a['E_screw']:.2f}"
              f" + bearing {a['E_bearing']:.2f} + air {a['E_aero']:.2f} + bottom/top stop {a['E_stoploss']:.2f} + pawl {a['E_pawl']:.3f};"
              f" closure {a['closure']:.1e}.\n",
              "ω never exceeds r·v_peak of the same push (the race ceiling); the hand's velocity limit, not its force, sets the top speed.\n"]
    fig, ax = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    ax[0].plot(r.t, r.omega, label="ω rotor"); ax[0].plot(r.t, r.race_speed(), lw=0.6, label="r·v (race speed)")
    ax[0].set_ylabel("rad/s"); ax[0].legend()
    ax[1].plot(r.t, r.x * 1e3); ax[1].set_ylabel("plunger x [mm]"); ax[1].set_xlabel("t [s]")
    fig.tight_layout(); fig.savefig(OUT / "fig_spinup.png", dpi=130); plt.close(fig)

    # 2. lead sweep
    rows = []
    for lead in CFG["leads_m_per_rev"]:
        p = replace(BASE, lead=lead)
        rr = PumpTop(p).simulate(T); q = rr.per_push()[-1]; aa = rr.energy_audit()
        rows.append({"lead [mm/rev]": f"{lead * 1e3:.1f}", "r [rad/m]": f"{p.r:.0f}", "J·r² [kg]": f"{p.reflected_mass:.2f}",
                     "ω after 20 pushes [rad/s]": f"{q['omega_end']:.0f}", "rpm": f"{q['omega_end'] * 30 / np.pi:.0f}",
                     "ceiling r·v_hand,max": f"{p.r * p.hand_vmax:.0f}", "KE [J]": f"{0.5 * p.J * q['omega_end'] ** 2:.2f}",
                     "stop-loss / hand work": f"{aa['E_stoploss'] / aa['E_hand']:.2f}"})
    lines += ["## 2. Lead (helix pitch) sweep\n", md(rows, list(rows[0].keys())),
              "\nFiner lead = larger r = higher ceiling and larger reflected mass J·r²; the hand then pushes a heavier 'plunger'.\n"]

    # 3. half vs full wave
    rows = []
    for fw in (False, True):
        rr = PumpTop(replace(BASE, full_wave=fw)).simulate(T); aa = rr.energy_audit(); q = rr.per_push()[-1]
        rows.append({"pawls": "two (full-wave)" if fw else "one (half-wave)", "hand work [J]": f"{aa['E_hand']:.2f}",
                     "rotor KE [J]": f"{aa['dKE_rotor']:.2f}", "stop losses [J]": f"{aa['E_stoploss']:.2f}",
                     "screw+bearing+air [J]": f"{aa['E_screw'] + aa['E_bearing'] + aa['E_aero']:.2f}",
                     "ω after 20 pushes": f"{q['omega_end']:.0f}", "closure": f"{aa['closure']:.1e}"})
    lines += ["## 3. One pawl vs two opposed pawls (the Gate's full-wave rectifier on the toy)\n", md(rows, list(rows[0].keys())),
              "\nThe second pawl harvests the return spring's stroke that the one-pawl toy wastes against the top stop and the hand."
              " Hand work is not higher; capture is. Nothing exceeds the hand's work.\n"]

    # 4. electrical load
    rows = []
    for cl in CFG["loads_Nms"]:
        rr = PumpTop(replace(BASE, c_load=cl)).simulate(T); late = rr.per_push()[10:]
        Wh = np.mean([q["W_hand"] for q in late]); El = np.mean([q["E_load"] for q in late]); om = np.mean([q["omega_end"] for q in late])
        rows.append({"c_load [N·m·s]": f"{cl:.0e}", "hand power [W]": f"{Wh / BASE.period:.2f}", "load power [W]": f"{El / BASE.period:.2f}",
                     "load / hand": f"{El / max(Wh, 1e-12):.2f}", "ω steady [rad/s]": f"{om:.0f}"})
    lines += ["## 4. Put a generator on the top (steady state, pushes 11–20)\n", md(rows, list(rows[0].keys())),
              "\nThe loaded top settles where load + losses per push equal hand work per push. Output is bounded by hand power; heavier load, slower top.\n"]

    # 5. spin-down
    y0 = PumpTop(BASE).simulate(6.0).y[:, -1]
    q = PumpTop(replace(BASE, hand_force=0.0)).simulate(CFG["spin_down_s"], y0=y0)
    oms = [float(np.interp(tt, q.t, q.omega)) for tt in (0, 2, 5, 10)]
    lines += ["## 5. Hand stops\n", f"ω at 0 / 2 / 5 / 10 s after the last push: {oms[0]:.0f} / {oms[1]:.0f} / {oms[2]:.0f} / {oms[3]:.0f} rad/s;"
              f" hand work after the stop {q.energy_audit()['E_hand']:.1e} J. The top is a store, not a source.\n"]

    # 6. hand variants
    rows = []
    for F0, vmax in CFG["hands"]:
        rr = PumpTop(replace(BASE, hand_force=F0, hand_vmax=vmax)).simulate(T); q = rr.per_push()[-1]
        rows.append({"hand F0 [N]": F0, "hand v_max [m/s]": vmax, "ω after 20 [rad/s]": f"{q['omega_end']:.0f}",
                     "W_hand per push [J]": f"{q['W_hand']:.3f}", "v_peak [m/s]": f"{q['v_peak_down']:.2f}"})
    lines += ["## 6. Stronger vs faster hand\n", md(rows, list(rows[0].keys())),
              "\nDoubling the hand's speed limit does more for the top than doubling its force: the ceiling is kinematic.\n"]

    (OUT / "RESULTS.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
