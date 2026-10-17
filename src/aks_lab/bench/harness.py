"""Single-DOF bench harness: the Gate's frame stroke is PRESCRIBED x_b(t).

This is the Duke shaker configuration and the hand-derivation anchor
(docs/01_physics.md §11): with the stroke imposed, the only dynamics are the
rotor + sprag pair + generator.

States: [omega, E_work_in, E_clutch, E_elec, E_genloss, E_fric, E_stop, E_gate, phi_A, phi_B]
E_work_in integrates F_actuator * xdot: the mechanical power the shaker
delivers through the frame stage (bias spring + friction + stops + drive).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ..elements.gate import ENG_A, ENG_B, FREE, SIGN, SLIP_A, SLIP_B, Gate
from ..solvers.hybrid import integrate

OM, E_WORK, E_CLUTCH, E_ELEC, E_GENLOSS, E_FRIC, E_STOP, E_GATE, PHA, PHB = range(10)
NSTATE = 10


def raised_cosine(amplitude: float, freq: float):
    """x(t) = A/2 (1 - cos 2 pi f t): starts at rest, x in [0, A]."""
    w = 2 * math.pi * freq
    return lambda t: (0.5 * amplitude * (1 - math.cos(w * t)),
                      0.5 * amplitude * w * math.sin(w * t),
                      0.5 * amplitude * w * w * math.cos(w * t))


def sine_stroke(amplitude: float, freq: float, offset: float = 0.0):
    w = 2 * math.pi * freq
    return lambda t: (offset + amplitude * math.sin(w * t),
                      amplitude * w * math.cos(w * t),
                      -amplitude * w * w * math.sin(w * t))


def still():
    return lambda t: (0.0, 0.0, 0.0)


@dataclass
class BenchResult:
    t: np.ndarray
    y: np.ndarray
    gate: Gate
    x_fn: object
    segments: list
    events: list
    warnings: list = field(default_factory=list)

    @property
    def omega(self):
        return self.y[OM]

    def stroke(self):
        return np.array([self.x_fn(t)[0] for t in self.t])

    def stroke_rate(self):
        return np.array([self.x_fn(t)[1] for t in self.t])

    def actuator_force(self):
        return np.gradient(self.y[E_WORK], self.t) / np.where(np.abs(self.stroke_rate()) > 1e-9, self.stroke_rate(), np.nan)

    def engage_counts(self):
        c = {"A": 0, "B": 0}
        for _t, lab, _i in self.events:
            if lab in ("engA", "lockA"):
                c["A"] += 1
            if lab in ("engB", "lockB"):
                c["B"] += 1
        return c

    def energy_audit(self) -> dict:
        y, p = self.y, self.gate.p
        x0, x1 = self.x_fn(self.t[0])[0], self.x_fn(self.t[-1])[0]
        d_storage = 0.5 * p.J * (y[OM, -1] ** 2 - y[OM, 0] ** 2) + 0.5 * p.k_b * (x1**2 - x0**2)
        f0, pen0 = self.gate.stop_force(x0, 0.0)
        f1, pen1 = self.gate.stop_force(x1, 0.0)
        d_storage += 0.5 * p.k_stop * (pen1**2 - pen0**2)
        e = {k: y[i, -1] - y[i, 0] for k, i in
             (("E_work_in", E_WORK), ("E_clutch", E_CLUTCH), ("E_elec", E_ELEC),
              ("E_genloss", E_GENLOSS), ("E_fric", E_FRIC), ("E_stop", E_STOP), ("E_gate", E_GATE))}
        e["dE_storage"] = d_storage
        diss = e["E_clutch"] + e["E_elec"] + e["E_genloss"] + e["E_fric"] + e["E_stop"]
        e["residual"] = e["E_work_in"] - diss - d_storage
        e["closure"] = abs(e["residual"]) / max(abs(e["E_work_in"]), diss + abs(d_storage), 1e-12)
        return e

    def mean_powers(self, t_from: float) -> dict:
        m = self.t >= t_from
        i0 = int(np.argmax(m))
        T = self.t[-1] - self.t[i0]
        return {"P_work_in": (self.y[E_WORK, -1] - self.y[E_WORK, i0]) / T,
                "P_gate": (self.y[E_GATE, -1] - self.y[E_GATE, i0]) / T,
                "P_elec": (self.y[E_ELEC, -1] - self.y[E_ELEC, i0]) / T,
                "P_clutch": (self.y[E_CLUTCH, -1] - self.y[E_CLUTCH, i0]) / T,
                "T": T}


class BenchRig:
    def __init__(self, gate: Gate, x_fn, lock: bool = False, force_freewheel: bool = False):
        self.g, self.p, self.x_fn = gate, gate.p, x_fn
        self.lock, self.force_free = lock, force_freewheel
        self.nstate = NSTATE

    def rhs(self, mode, t, y):
        p, g = self.p, self.g
        x, xd, xdd = self.x_fn(t)
        om = y[OM]
        f_pass, f_stop, pen = g.passive_force(x, xd)
        dy = np.zeros(NSTATE)
        if mode == FREE:
            t_a, t_b, f_ax, p_drag = g.overrun(xd, om)
            t_r, p_elec, p_gl = g.resist_torque(om)
            dom = (t_a + t_b - t_r) / p.J
            f_act = f_pass + f_ax
            p_clutch, p_gate = p_drag, 0.0
        else:
            s = SIGN[mode]
            om_other = -s * p.r * xd
            t_other = p.c_od * (om_other - om)
            f_other = -s * p.r * t_other
            p_drag = t_other * (om_other - om)
            t_r, p_elec, p_gl = g.resist_torque(om)
            if mode in (ENG_A, ENG_B):
                dom = s * p.r * xdd                      # rotor follows the race exactly
                t_c = p.J * dom + t_r - t_other
                f_act = f_pass + f_other + s * p.r * t_c
                p_clutch, p_gate = p_drag, t_c * om
            else:
                t_cap = p.T_cap
                dom = (t_cap + t_other - t_r) / p.J
                f_act = f_pass + f_other + s * p.r * t_cap
                p_clutch, p_gate = p_drag + t_cap * (s * p.r * xd - om), t_cap * om
        dy[OM] = dom
        dy[E_WORK] = f_act * xd
        dy[E_CLUTCH] = p_clutch
        dy[E_ELEC] = p_elec
        dy[E_GENLOSS] = p_gl
        dy[E_FRIC] = p.c_b * xd * xd
        dy[E_STOP] = g.stop_loss_rate(f_stop, pen, xd)
        dy[E_GATE] = p_gate
        if p.theta_bl > 0:
            ga, gb = p.r * xd - om, -p.r * xd - om
            dy[PHA] = ga if ga > 0 else 0.0
            dy[PHB] = gb if gb > 0 else 0.0
        return dy

    def _tc(self, s, t, y):
        p = self.p
        x, xd, xdd = self.x_fn(t)
        om_other = -s * p.r * xd
        t_other = p.c_od * (om_other - y[OM])
        t_r, _, _ = self.g.resist_torque(y[OM])
        return p.J * s * p.r * xdd + t_r - t_other

    def events(self, mode):
        if self.lock or self.force_free:
            return []
        p, g = self.p, self.g
        ev = []
        if mode == FREE:
            for s, lab in ((+1.0, "A"), (-1.0, "B")):
                if p.theta_bl > 0:
                    ev.append((lambda t, y, s=s: g.engage_gap(s, self.x_fn(t)[1], y[OM]), +1.0, "arm" + lab))
                    idx = PHA if s > 0 else PHB
                    ev.append((lambda t, y, idx=idx: y[idx] - p.theta_bl, +1.0, "lock" + lab))
                else:
                    ev.append((lambda t, y, s=s: g.engage_gap(s, self.x_fn(t)[1], y[OM]), +1.0, "eng" + lab))
        elif mode in (ENG_A, ENG_B):
            s = SIGN[mode]
            lab = "A" if s > 0 else "B"
            ev.append((lambda t, y, s=s: self._tc(s, t, y), -1.0, "dis" + lab))
            if math.isfinite(p.T_cap):
                ev.append((lambda t, y, s=s: self._tc(s, t, y) - p.T_cap, +1.0, "slip" + lab))
        else:
            s = SIGN[mode]
            lab = "A" if s > 0 else "B"
            ev.append((lambda t, y, s=s: g.engage_gap(s, self.x_fn(t)[1], y[OM]) + p.eps_engage, -1.0, "unslip" + lab))
        return ev

    def transition(self, mode, label, t, y):
        p = self.p
        y = y.copy()
        kind, lab = label[:-1], label[-1]
        s = +1.0 if lab == "A" else -1.0
        eng_mode = ENG_A if lab == "A" else ENG_B
        slip_mode = SLIP_A if lab == "A" else SLIP_B
        if kind == "arm":
            y[PHA if lab == "A" else PHB] = 0.0
            return FREE, y, None
        if kind in ("eng", "lock"):
            xd = self.x_fn(t)[1]
            # prescribed stroke = infinite end masses: the rotor is snapped to race speed
            d_om = s * p.r * xd - y[OM]
            e_lost = 0.5 * p.J * d_om * d_om if d_om > 0 else 0.0
            y_try = y.copy()
            y_try[OM] = s * p.r * xd
            t_c = self._tc(s, t, y_try)
            if t_c < -1e-12:
                return mode, y, {"rejected": True}
            if math.isfinite(p.T_cap) and t_c > p.T_cap:
                return slip_mode, y, None
            y_try[E_CLUTCH] += e_lost
            # the lock-up impulse J*d_om is reacted by the (kinematic) actuator at race speed
            y_try[E_WORK] += p.J * d_om * (s * p.r * xd) if d_om > 0 else 0.0
            y_try[PHA if lab == "A" else PHB] = 0.0
            return eng_mode, y_try, {"E_lost": e_lost, "impulse": p.J * d_om}
        if kind in ("dis", "unslip"):
            return FREE, y, None
        if kind == "slip":
            return slip_mode, y, None
        raise ValueError(label)

    def initial_mode(self, t, y):
        if self.lock:
            y[OM] = self.p.r * self.x_fn(t)[1]
            return ENG_A
        if self.force_free:
            return FREE
        xd = self.x_fn(t)[1]
        for mode, s in ((ENG_A, +1.0), (ENG_B, -1.0)):
            if self.g.engage_gap(s, xd, y[OM]) > 0:
                y_try = y.copy()
                y_try[OM] = s * self.p.r * xd
                if self._tc(s, t, y_try) >= 0:
                    y[OM] = y_try[OM]
                    return mode
        return FREE

    def simulate(self, t_end, omega0=0.0, rtol=1e-9, atol=1e-11, dt_out=1e-3, max_step=2e-3) -> BenchResult:
        y0 = np.zeros(NSTATE)
        y0[OM] = omega0
        tr = integrate(self, y0, t_end, rtol=rtol, atol=atol, dt_out=dt_out, max_step=max_step)
        return BenchResult(tr.t, tr.y, self.g, self.x_fn, tr.segments, tr.events, tr.warnings)
