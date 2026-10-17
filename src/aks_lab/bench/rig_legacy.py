"""Shaker-bench rig: the Gate's frame stroke x_b(t) is PRESCRIBED.

This is the configuration of the planned Duke bench article (single unit on a
shaker) and the workhorse for the V1 analytic-limit gates: with the stroke
kinematically imposed, the only dynamics left are the rotor + sprag pair +
generator, so every limit has a closed form to test against.

States: [omega, E_work_in, E_clutch, E_elec, E_genloss, E_damp]
E_work_in integrates F_actuator * xdot — the mechanical power the shaker must
deliver through the frame stage (spring k_b + parasitic c_b + stops + screw
reaction).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp

from .params import Params

OM, E_WORK, E_CLUTCH, E_ELEC, E_GENLOSS, E_DAMP = range(6)
NSTATE = 6

FREE, ENG_A, ENG_B, LOCKED = "free", "engA", "engB", "locked"
_SIGN = {ENG_A: +1.0, ENG_B: -1.0, LOCKED: +1.0}


def raised_cosine(amplitude: float, freq: float):
    """Stroke x(t) = A/2*(1-cos(2 pi f t)): starts at rest, x in [0, A]."""
    w = 2.0 * math.pi * freq

    def x_fn(t: float):
        return (
            0.5 * amplitude * (1.0 - math.cos(w * t)),
            0.5 * amplitude * w * math.sin(w * t),
            0.5 * amplitude * w * w * math.cos(w * t),
        )

    return x_fn


def sine(amplitude: float, freq: float):
    w = 2.0 * math.pi * freq

    def x_fn(t: float):
        return (
            amplitude * math.sin(w * t),
            amplitude * w * math.cos(w * t),
            -amplitude * w * w * math.sin(w * t),
        )

    return x_fn


def still():
    return lambda t: (0.0, 0.0, 0.0)


@dataclass
class BenchResult:
    t: np.ndarray
    y: np.ndarray
    segments: list
    engage_counts: dict
    params: Params
    gen: object
    x_fn: object
    warnings: list = field(default_factory=list)

    @property
    def omega(self) -> np.ndarray:
        return self.y[OM]

    def stroke(self) -> np.ndarray:
        return np.array([self.x_fn(t)[0] for t in self.t])

    def stroke_rate(self) -> np.ndarray:
        return np.array([self.x_fn(t)[1] for t in self.t])

    def storage(self, i: int) -> float:
        p = self.params
        x = self.x_fn(self.t[i])[0]
        pen = max(0.0, x - p.x_b_max) + min(0.0, x + p.x_b_max)
        return 0.5 * p.J * self.y[OM, i] ** 2 + 0.5 * p.k_b * x**2 + 0.5 * p.k_stop * pen**2

    def energy_audit(self) -> dict:
        y = self.y
        e_in = y[E_WORK, -1] - y[E_WORK, 0]
        d_storage = self.storage(-1) - self.storage(0)
        terms = {
            "E_work_in": e_in,
            "E_clutch": y[E_CLUTCH, -1] - y[E_CLUTCH, 0],
            "E_elec": y[E_ELEC, -1] - y[E_ELEC, 0],
            "E_genloss": y[E_GENLOSS, -1] - y[E_GENLOSS, 0],
            "E_damp": y[E_DAMP, -1] - y[E_DAMP, 0],
            "dE_storage": d_storage,
        }
        residual = e_in - (
            d_storage + terms["E_clutch"] + terms["E_elec"] + terms["E_genloss"] + terms["E_damp"]
        )
        denom = max(
            abs(e_in),
            terms["E_elec"] + terms["E_genloss"] + terms["E_damp"] + abs(d_storage),
            1e-12,
        )
        terms["residual"] = residual
        terms["closure"] = abs(residual) / denom
        return terms


class BenchRig:
    def __init__(self, p: Params, gen, x_fn, force_freewheel: bool = False):
        self.p = p
        self.gen = gen
        self.x_fn = x_fn
        self.force_freewheel = force_freewheel
        self.Gt = p.Gt

    def _stop(self, x: float, dx: float):
        p = self.p
        if x > p.x_b_max:
            pen = x - p.x_b_max
            f = max(0.0, p.k_stop * pen + p.c_stop * dx)
        elif x < -p.x_b_max:
            pen = x + p.x_b_max
            f = min(0.0, p.k_stop * pen + p.c_stop * dx)
        else:
            pen, f = 0.0, 0.0
        return f, pen

    def _rhs_free(self, t: float, y: np.ndarray) -> np.ndarray:
        p = self.p
        x, dx, _ = self.x_fn(t)
        om = y[OM]
        om_a = self.Gt * dx
        om_b = -om_a
        t_a = p.c_od * (om_a - om)
        t_b = p.c_od * (om_b - om)
        f_stop, pen = self._stop(x, dx)
        f_act = p.k_b * x + p.c_b * dx + f_stop + self.Gt * (t_a - t_b)
        t_gen, p_elec, p_gl = self.gen.torque(om)

        dy = np.zeros(NSTATE)
        dy[OM] = (t_a + t_b - t_gen - p.c_w * om) / p.J
        dy[E_WORK] = f_act * dx
        dy[E_CLUTCH] = t_a * (om_a - om) + t_b * (om_b - om)
        dy[E_ELEC] = p_elec
        dy[E_GENLOSS] = p_gl + p.c_w * om**2
        dy[E_DAMP] = p.c_b * dx**2 + (f_stop - p.k_stop * pen) * dx
        return dy

    def _eng_core(self, t: float, y: np.ndarray, s: float):
        p = self.p
        x, dx, ddx = self.x_fn(t)
        om = y[OM]
        t_gen, p_elec, p_gl = self.gen.torque(om)
        domega = s * self.Gt * ddx
        t_c = p.J * domega + t_gen + p.c_w * om
        return x, dx, domega, t_c, p_elec, p_gl, om

    def _rhs_eng(self, t: float, y: np.ndarray, s: float) -> np.ndarray:
        p = self.p
        x, dx, domega, t_c, p_elec, p_gl, om = self._eng_core(t, y, s)
        f_stop, pen = self._stop(x, dx)
        f_act = p.k_b * x + p.c_b * dx + f_stop + s * self.Gt * t_c

        dy = np.zeros(NSTATE)
        dy[OM] = domega
        dy[E_WORK] = f_act * dx
        dy[E_CLUTCH] = 0.0
        dy[E_ELEC] = p_elec
        dy[E_GENLOSS] = p_gl + p.c_w * om**2
        dy[E_DAMP] = p.c_b * dx**2 + (f_stop - p.k_stop * pen) * dx
        return dy

    def _ev_engage(self, t, y, s: float) -> float:
        return s * self.Gt * self.x_fn(t)[1] - y[OM] - self.p.eps_engage

    def _ev_disengage(self, t, y, s: float) -> float:
        return self._eng_core(t, y, s)[3]

    def simulate(
        self,
        t_end: float,
        omega0: float = 0.0,
        method: str = "LSODA",
        rtol: float = 1e-9,
        atol: float = 1e-11,
        dt_out: float = 1e-3,
        max_step: float = 2e-3,
        lock: bool = False,
    ) -> BenchResult:
        """lock=True: permanently engaged bidirectional coupling (V1 ratio limit)."""
        y = np.zeros(NSTATE)
        y[OM] = omega0
        t = 0.0
        counts = {"A": 0, "B": 0}
        segments: list = []
        ts_out = [np.array([t])]
        ys_out = [y.copy()[:, None]]
        warnings: list[str] = []

        if lock:
            mode = LOCKED
            y[OM] = self.Gt * self.x_fn(0.0)[1]
        elif self.force_freewheel:
            mode = FREE
        else:
            mode = FREE
            for m, s in ((ENG_A, +1.0), (ENG_B, -1.0)):
                if self._ev_engage(t, y, s) > 0.0 and self._eng_core(t, y, s)[3] >= 0.0:
                    mode = m
                    y[OM] = s * self.x_fn(t)[1] * self.Gt
                    break

        while t < t_end - 1e-12:
            if mode == LOCKED:
                rhs = lambda tt, yy: self._rhs_eng(tt, yy, +1.0)  # noqa: E731
                events, targets = [], []
            elif mode == FREE:
                rhs = self._rhs_free
                if self.force_freewheel:
                    events, targets = [], []
                else:
                    events = [
                        lambda tt, yy: self._ev_engage(tt, yy, +1.0),
                        lambda tt, yy: self._ev_engage(tt, yy, -1.0),
                    ]
                    targets = [ENG_A, ENG_B]
                    for ev in events:
                        ev.terminal = True
                        ev.direction = +1.0
            else:
                s = _SIGN[mode]
                rhs = lambda tt, yy, s=s: self._rhs_eng(tt, yy, s)  # noqa: E731
                events = [lambda tt, yy, s=s: self._ev_disengage(tt, yy, s)]
                targets = [FREE]
                events[0].terminal = True
                events[0].direction = -1.0

            grid_t = np.arange(t, t_end, dt_out)
            grid_t = np.append(grid_t, t_end) if grid_t[-1] < t_end - 1e-12 else grid_t
            sol = solve_ivp(
                rhs,
                (t, t_end),
                y,
                method=method,
                events=events,
                t_eval=grid_t,
                rtol=rtol,
                atol=atol,
                max_step=max_step,
            )
            if not sol.success:
                raise RuntimeError(f"bench solver failed in mode {mode} at t={t}: {sol.message}")

            te, which = None, None
            for k, tev in enumerate(sol.t_events or []):
                if len(tev) and (te is None or tev[0] < te):
                    te, which = tev[0], k

            if sol.t.size > 1:
                ts_out.append(sol.t[1:])
                ys_out.append(sol.y[:, 1:])
            segments.append((mode, t, te if te is not None else t_end))
            if te is None:
                break

            y = sol.y_events[which][0].copy()
            ts_out.append(np.array([te]))
            ys_out.append(y.copy()[:, None])
            t = te

            new_mode = targets[which]
            if new_mode in (ENG_A, ENG_B):
                s = _SIGN[new_mode]
                y[OM] = s * self.Gt * self.x_fn(t)[1]
                if self._eng_core(t, y, s)[3] < -1e-12:
                    y = y + 1e-8 * self._rhs_free(t, y)
                    t += 1e-8
                    mode = FREE
                    continue
                counts["A" if new_mode == ENG_A else "B"] += 1
            mode = new_mode

        return BenchResult(
            t=np.concatenate(ts_out),
            y=np.concatenate(ys_out, axis=1),
            segments=segments,
            engage_counts=counts,
            params=self.p,
            gen=self.gen,
            x_fn=self.x_fn,
            warnings=warnings,
        )
