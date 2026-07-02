"""Quarter-car + Armstrong Gate hybrid (event-driven) dynamics.

Full derivation, sign conventions and the energy ledger live in docs/PHYSICS.md.

Summary
-------
Chain (top to bottom, perturbation coordinates about static equilibrium):

    sprung mass m_s (z_s)
      |  frame stage: biasing spring k_b + parasitic c_b + hard stops
      |               + screw/sprag/generator path   (stroke r_b = z_s - z_f)
    frame node m_f (z_f)
      |  main stage: suspension spring k_s + damper c_s
    unsprung mass m_u (z_u)
      |  tire spring k_t
    road z_r(t)

The sprag pair is modelled as an exact kinematic constraint with event-driven
mode switching (modes: FREE / ENG_A / ENG_B).  Race speeds at the generator
shaft: omega_A = +Gt*dr_b, omega_B = -Gt*dr_b, with Gt = 2*pi*n_step/lead.
Clutch i engages when omega_i - omega crosses zero upward; an engaged clutch
disengages when its transmitted torque T_c drops to zero (a sprag cannot
pull).  While engaged, the rotor inertia J reflects onto the stroke DOF as
inertance Jr = J*Gt^2, coupling the (z_s, z_f) mass matrix.

Energy bookkeeping integrals are carried as ODE states so the audit closes to
solver accuracy — the <1% closure gate (V1) is enforced on every simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp

from .params import Params

# state indices
ZS, VS, ZF, VF, ZU, VU, OM = range(7)
E_DAMP, E_STOP, E_CLUTCH, E_ELEC, E_GENLOSS, E_ROAD = range(7, 13)
NSTATE = 13

FREE, ENG_A, ENG_B = "free", "engA", "engB"
_SIGN = {ENG_A: +1.0, ENG_B: -1.0}


def _t_grid(t0: float, t1: float, dt: float) -> np.ndarray:
    n = max(int(np.floor((t1 - t0) / dt)), 0)
    ts = t0 + dt * np.arange(n + 1)
    if ts[-1] < t1 - 1e-12:
        ts = np.append(ts, t1)
    else:
        ts[-1] = t1
    return ts


@dataclass
class SimResult:
    t: np.ndarray
    y: np.ndarray
    segments: list          # (mode, t0, t1)
    engage_counts: dict     # {"A": n, "B": n}
    params: Params
    road: object
    gen: object
    warnings: list = field(default_factory=list)

    # -- convenience accessors ------------------------------------------------
    @property
    def frame_stroke(self) -> np.ndarray:
        return self.y[ZS] - self.y[ZF]

    @property
    def frame_stroke_rate(self) -> np.ndarray:
        return self.y[VS] - self.y[VF]

    @property
    def omega(self) -> np.ndarray:
        return self.y[OM]

    @property
    def screw_rpm(self) -> np.ndarray:
        """Screw-shaft (sprag race) speed in rpm — lift-off design check."""
        return np.abs(self.frame_stroke_rate) * 60.0 / self.params.lead

    def storage(self, i: int) -> float:
        """Total stored (kinetic + potential) energy at sample i."""
        p, y = self.params, self.y[:, i]
        r_b = y[ZS] - y[ZF]
        r_m = y[ZF] - y[ZU]
        r_t = y[ZU] - self.road.z(self.t[i])
        pen = max(0.0, r_b - p.x_b_max) + min(0.0, r_b + p.x_b_max)
        return (
            0.5 * p.m_s * y[VS] ** 2
            + 0.5 * p.m_f * y[VF] ** 2
            + 0.5 * p.m_u * y[VU] ** 2
            + 0.5 * p.J * y[OM] ** 2
            + 0.5 * p.k_b * r_b**2
            + 0.5 * p.k_s * r_m**2
            + 0.5 * p.k_t * r_t**2
            + 0.5 * p.k_stop * pen**2
        )

    def energy_audit(self) -> dict:
        """Ledger: road work in = electrical out + losses + Delta(storage)."""
        y = self.y
        e_in = y[E_ROAD, -1] - y[E_ROAD, 0]
        d_storage = self.storage(-1) - self.storage(0)
        terms = {
            "E_road_in": e_in,
            "E_damper": y[E_DAMP, -1] - y[E_DAMP, 0],
            "E_stop": y[E_STOP, -1] - y[E_STOP, 0],
            "E_clutch": y[E_CLUTCH, -1] - y[E_CLUTCH, 0],
            "E_elec": y[E_ELEC, -1] - y[E_ELEC, 0],
            "E_genloss": y[E_GENLOSS, -1] - y[E_GENLOSS, 0],
            "dE_storage": d_storage,
        }
        residual = e_in - (
            d_storage
            + terms["E_damper"]
            + terms["E_stop"]
            + terms["E_clutch"]
            + terms["E_elec"]
            + terms["E_genloss"]
        )
        denom = max(
            abs(e_in),
            terms["E_damper"] + terms["E_elec"] + terms["E_genloss"] + abs(d_storage),
            1e-12,
        )
        terms["residual"] = residual
        terms["closure"] = abs(residual) / denom
        return terms


class QuarterCarGate:
    """Single-corner quarter car with the Armstrong Gate in the soft-first stage."""

    def __init__(self, p: Params, gen, road):
        self.p = p
        self.gen = gen
        self.road = road
        self.Gt = p.Gt
        self.Jr = p.Jr

    # -- force assembly -------------------------------------------------------
    def _stop(self, r: float, dr: float):
        p = self.p
        if r > p.x_b_max:
            pen = r - p.x_b_max
            f = max(0.0, p.k_stop * pen + p.c_stop * dr)
        elif r < -p.x_b_max:
            pen = r + p.x_b_max
            f = min(0.0, p.k_stop * pen + p.c_stop * dr)
        else:
            pen, f = 0.0, 0.0
        return f, pen

    def _common(self, t: float, y: np.ndarray):
        p = self.p
        r_b = y[ZS] - y[ZF]
        dr_b = y[VS] - y[VF]
        r_m = y[ZF] - y[ZU]
        dr_m = y[VF] - y[VU]
        zr = self.road.z(t)
        zrd = self.road.zdot(t)
        f_stop, pen = self._stop(r_b, dr_b)
        f_b_pass = p.k_b * r_b + p.c_b * dr_b + f_stop
        f_m = p.k_s * r_m + p.c_s * dr_m
        f_t = p.k_t * (y[ZU] - zr)
        return r_b, dr_b, r_m, dr_m, zrd, f_b_pass, f_m, f_t, f_stop, pen

    def _energy_rows(self, dy, dr_b, dr_m, zrd, f_t, f_stop, pen, p_clutch, p_elec, p_genloss):
        p = self.p
        dy[E_DAMP] = p.c_s * dr_m**2 + p.c_b * dr_b**2
        dy[E_STOP] = (f_stop - p.k_stop * pen) * dr_b
        dy[E_CLUTCH] = p_clutch
        dy[E_ELEC] = p_elec
        dy[E_GENLOSS] = p_genloss
        dy[E_ROAD] = -f_t * zrd

    # -- freewheel mode -------------------------------------------------------
    def _rhs_free(self, t: float, y: np.ndarray) -> np.ndarray:
        p = self.p
        (r_b, dr_b, r_m, dr_m, zrd, f_b_pass, f_m, f_t, f_stop, pen) = self._common(t, y)
        om = y[OM]
        om_a = self.Gt * dr_b
        om_b = -om_a
        t_a = p.c_od * (om_a - om)
        t_b = p.c_od * (om_b - om)
        f_b = f_b_pass + self.Gt * (t_a - t_b)
        t_gen, p_elec, p_gl = self.gen.torque(om)

        dy = np.zeros(NSTATE)
        dy[ZS], dy[ZF], dy[ZU] = y[VS], y[VF], y[VU]
        dy[VS] = -f_b / p.m_s
        dy[VF] = (f_b - f_m) / p.m_f
        dy[VU] = (f_m - f_t) / p.m_u
        dy[OM] = (t_a + t_b - t_gen - p.c_w * om) / p.J
        p_clutch = t_a * (om_a - om) + t_b * (om_b - om)
        self._energy_rows(
            dy, dr_b, dr_m, zrd, f_t, f_stop, pen, p_clutch, p_elec, p_gl + p.c_w * om**2
        )
        return dy

    # -- engaged modes --------------------------------------------------------
    def _eng_core(self, t: float, y: np.ndarray, s: float):
        """Accelerations and clutch torque with the kinematic constraint active."""
        p = self.p
        (r_b, dr_b, r_m, dr_m, zrd, f_b_pass, f_m, f_t, f_stop, pen) = self._common(t, y)
        om = y[OM]
        t_gen, p_elec, p_gl = self.gen.torque(om)
        t_r = t_gen + p.c_w * om
        jr = self.Jr
        b1 = -f_b_pass - s * self.Gt * t_r
        b2 = f_b_pass - f_m + s * self.Gt * t_r
        det = p.m_s * p.m_f + jr * (p.m_s + p.m_f)
        a_s = ((p.m_f + jr) * b1 + jr * b2) / det
        a_f = (jr * b1 + (p.m_s + jr) * b2) / det
        a_u = (f_m - f_t) / p.m_u
        domega = s * self.Gt * (a_s - a_f)
        t_c = p.J * domega + t_r
        return (a_s, a_f, a_u, domega, t_c, dr_b, dr_m, zrd, f_t, f_stop, pen, p_elec, p_gl, om)

    def _rhs_eng(self, t: float, y: np.ndarray, s: float) -> np.ndarray:
        (a_s, a_f, a_u, domega, _t_c, dr_b, dr_m, zrd, f_t, f_stop, pen, p_elec, p_gl, om) = (
            self._eng_core(t, y, s)
        )
        dy = np.zeros(NSTATE)
        dy[ZS], dy[ZF], dy[ZU] = y[VS], y[VF], y[VU]
        dy[VS], dy[VF], dy[VU] = a_s, a_f, a_u
        dy[OM] = domega
        # engaged sprag: kinematic constraint transmits torque losslessly
        self._energy_rows(dy, dr_b, dr_m, zrd, f_t, f_stop, pen, 0.0, p_elec, p_gl + self.p.c_w * om**2)
        return dy

    # -- events ---------------------------------------------------------------
    def _ev_engage(self, t, y, s: float) -> float:
        return s * self.Gt * (y[VS] - y[VF]) - y[OM] - self.p.eps_engage

    def _ev_disengage(self, t, y, s: float) -> float:
        return self._eng_core(t, y, s)[4]  # T_c

    # -- simulation driver ----------------------------------------------------
    def _default_atol(self) -> np.ndarray:
        atol = np.empty(NSTATE)
        atol[[ZS, ZF, ZU]] = 1e-9
        atol[[VS, VF, VU]] = 1e-8
        atol[OM] = 1e-6
        atol[E_DAMP:NSTATE] = 1e-6
        return atol

    def simulate(
        self,
        t_end: float,
        y0: np.ndarray | None = None,
        method: str = "LSODA",
        rtol: float = 1e-8,
        atol=None,
        dt_out: float = 2e-3,
        max_step: float = 5e-3,
        lock: str | None = None,
    ) -> SimResult:
        """Run the hybrid simulation from t=0 to t_end.

        lock='A' or 'B' forces that clutch permanently engaged (bidirectional
        coupling) — the V1 locked-ratio limit; no events fire.
        """
        p = self.p
        y = np.zeros(NSTATE) if y0 is None else np.array(y0, dtype=float)
        if atol is None:
            atol = self._default_atol()
        t = 0.0
        warnings: list[str] = []
        counts = {"A": 0, "B": 0}
        segments: list = []
        ts_out = [np.array([t])]
        ys_out = [y.copy()[:, None]]

        if lock is not None:
            mode = ENG_A if lock.upper() == "A" else ENG_B
            y[OM] = _SIGN[mode] * self.Gt * (y[VS] - y[VF])
        else:
            mode = self._resolve_mode(t, y)

        zeno = 0
        last_te = -1.0
        while t < t_end - 1e-12:
            if mode == FREE:
                rhs = self._rhs_free
                events = [
                    lambda tt, yy: self._ev_engage(tt, yy, +1.0),
                    lambda tt, yy: self._ev_engage(tt, yy, -1.0),
                ]
                targets = [ENG_A, ENG_B]
            else:
                s = _SIGN[mode]
                rhs = lambda tt, yy, s=s: self._rhs_eng(tt, yy, s)  # noqa: E731
                events = [lambda tt, yy, s=s: self._ev_disengage(tt, yy, s)]
                targets = [FREE]
            if lock is not None:
                events, targets = [], []
            for ev in events:
                ev.terminal = True
                ev.direction = +1.0 if mode == FREE else -1.0

            sol = solve_ivp(
                rhs,
                (t, t_end),
                y,
                method=method,
                events=events,
                t_eval=_t_grid(t, t_end, dt_out),
                rtol=rtol,
                atol=atol,
                max_step=max_step,
            )
            if not sol.success:
                raise RuntimeError(f"solver failed in mode {mode} at t={t}: {sol.message}")

            te, which = None, None
            for k, tev in enumerate(sol.t_events or []):
                if len(tev) and (te is None or tev[0] < te):
                    te, which = tev[0], k

            if sol.t.size > 1:
                ts_out.append(sol.t[1:])
                ys_out.append(sol.y[:, 1:])
            seg_end = te if te is not None else t_end
            segments.append((mode, t, seg_end))
            if te is None:
                break

            y = sol.y_events[which][0].copy()
            ts_out.append(np.array([te]))
            ys_out.append(y.copy()[:, None])
            t = te

            if te - last_te < 1e-10:
                zeno += 1
                if zeno > 200:
                    y = y + 1e-7 * self._rhs_free(t, y)
                    t += 1e-7
                    mode = FREE
                    warnings.append(f"zeno guard tripped at t={te:.6f}")
                    zeno = 0
                    last_te = te
                    continue
            else:
                zeno = 0
            last_te = te

            new_mode = targets[which]
            if new_mode in (ENG_A, ENG_B):
                s = _SIGN[new_mode]
                y[OM] = s * self.Gt * (y[VS] - y[VF])
                if self._eng_core(t, y, s)[4] < -1e-12:
                    # grazing contact: clutch cannot sustain torque — stay free
                    y = y + 1e-8 * self._rhs_free(t, y)
                    t += 1e-8
                    mode = FREE
                    continue
                counts["A" if new_mode == ENG_A else "B"] += 1
            mode = new_mode

        return SimResult(
            t=np.concatenate(ts_out),
            y=np.concatenate(ys_out, axis=1),
            segments=segments,
            engage_counts=counts,
            params=p,
            road=self.road,
            gen=self.gen,
            warnings=warnings,
        )

    def _resolve_mode(self, t: float, y: np.ndarray) -> str:
        for mode, s in ((ENG_A, +1.0), (ENG_B, -1.0)):
            if self._ev_engage(t, y, s) > 0.0:
                y_try = y.copy()
                y_try[OM] = s * self.Gt * (y[VS] - y[VF])
                if self._eng_core(t, y_try, s)[4] >= 0.0:
                    y[OM] = y_try[OM]
                    return mode
        return FREE
