"""Numba-compiled right-hand sides for the corner-with-Gate (same physics as quarter_car.py).

Scope: linear generator load only (T = c_gen w), which is what every sweep uses.
Equivalence to the reference implementation is enforced to solver tolerance in
tests/test_fast_equivalence.py; the reference stays the normative model.
"""

from __future__ import annotations

import math

import numpy as np

try:
    from numba import njit
except ImportError:  # pragma: no cover
    njit = None

from ..elements.gate import ENG_A, ENG_B, FREE, SIGN, SLIP_A, SLIP_B, Gate
from ..solvers.hybrid import integrate
from .quarter_car import (
    E_CLUTCH,
    E_DAMP,
    E_ELEC,
    E_FRAME,
    E_FRIC,
    E_GATE,
    E_GENLOSS,
    E_ROAD,
    E_STOP,
    NSTATE,
    OM,
    PHA,
    PHB,
    VF,
    VS,
    VU,
    ZF,
    ZS,
    ZU,
    CornerParams,
    SimResult,
    _default_stationary,
)

# parameter vector layout
(P_MS, P_MF, P_MU, P_KM, P_CS, P_KT, P_CT, P_KB, P_CB, P_XC, P_XE, P_KSTOP, P_CSTOP, P_R, P_J, P_CW, P_COD,
 P_THBL, P_TCAP, P_CGEN, P_ETA, P_SPAN, P_EPS) = range(23)


def pack(c: CornerParams, g: Gate, m_f: float, span: str) -> np.ndarray:
    p = g.p
    gen = g.gen
    if not hasattr(gen, "c_gen"):
        raise TypeError("fast model supports LinearGenerator loads only")
    P = np.zeros(23)
    P[P_MS], P[P_MF], P[P_MU] = c.m_s, m_f, c.m_u
    P[P_KM], P[P_CS], P[P_KT], P[P_CT] = c.k_m, c.c_s, c.k_t, c.c_t
    P[P_KB], P[P_CB], P[P_XC], P[P_XE] = p.k_b, p.c_b, p.x_c, p.x_e
    P[P_KSTOP], P[P_CSTOP], P[P_R], P[P_J] = p.k_stop, p.c_stop, p.r, p.J
    P[P_CW], P[P_COD], P[P_THBL] = p.c_w, p.c_od, p.theta_bl
    P[P_TCAP] = p.T_cap if math.isfinite(p.T_cap) else 1e300
    P[P_CGEN], P[P_ETA] = gen.c_gen, gen.eta
    P[P_SPAN] = 1.0 if span == "full" else 0.0
    P[P_EPS] = p.eps_engage
    return P


def spline_arrays(road):
    """Breakpoints and coefficient matrix of the road's CubicSpline (scipy PPoly layout)."""
    sp = road._spline
    return np.ascontiguousarray(sp.x), np.ascontiguousarray(sp.c)


if njit is not None:

    @njit(cache=True, fastmath=False)
    def _road(t, xb, cc):
        n = xb.shape[0]
        i = np.searchsorted(xb, t) - 1
        if i < 0:
            i = 0
        if i > n - 2:
            i = n - 2
        dx = t - xb[i]
        c0, c1, c2, c3 = cc[0, i], cc[1, i], cc[2, i], cc[3, i]
        z = ((c0 * dx + c1) * dx + c2) * dx + c3
        zd = (3.0 * c0 * dx + 2.0 * c1) * dx + c2
        return z, zd

    @njit(cache=True)
    def _stop(r, dr, P):
        if r > P[P_XC]:
            pen = r - P[P_XC]
            f = P[P_KSTOP] * pen + P[P_CSTOP] * dr
            if f < 0.0:
                f = 0.0
        elif r < -P[P_XE]:
            pen = r + P[P_XE]
            f = P[P_KSTOP] * pen + P[P_CSTOP] * dr
            if f > 0.0:
                f = 0.0
        else:
            pen, f = 0.0, 0.0
        return f, pen

    @njit(cache=True)
    def _common(t, y, P, xb, cc):
        r_b = y[ZS] - y[ZF]
        dr_b = y[VS] - y[VF]
        r_m = y[ZF] - y[ZU]
        zr, zrd = _road(t, xb, cc)
        f_stop, pen = _stop(r_b, dr_b, P)
        f_b_pass = P[P_KB] * r_b + P[P_CB] * dr_b + f_stop
        f_m = P[P_KM] * r_m
        dr_d = (y[VS] - y[VU]) if P[P_SPAN] > 0.5 else (y[VF] - y[VU])
        f_d = P[P_CS] * dr_d
        f_t = P[P_KT] * (y[ZU] - zr) + P[P_CT] * (y[VU] - zrd)
        return r_b, dr_b, f_b_pass, f_stop, pen, f_m, f_d, dr_d, f_t, zr, zrd

    @njit(cache=True)
    def _eng_core(s, y, P, f_top_ext, f_bot_ext, f_b_pass, t_ext):
        om = y[OM]
        r = P[P_R]
        t_gen = P[P_CGEN] * om
        p_mech = t_gen * om
        p_elec = P[P_ETA] * p_mech
        p_loss = (1.0 - P[P_ETA]) * p_mech + P[P_CW] * om * om
        t_r = t_gen + P[P_CW] * om - t_ext
        jr = P[P_J] * r * r
        m_top, m_bot = P[P_MS], P[P_MF]
        b1 = f_top_ext - f_b_pass - s * r * t_r
        b2 = f_bot_ext + f_b_pass + s * r * t_r
        det = m_top * m_bot + jr * (m_top + m_bot)
        a_top = ((m_bot + jr) * b1 + jr * b2) / det
        a_bot = (jr * b1 + (m_top + jr) * b2) / det
        domega = s * r * (a_top - a_bot)
        t_c = P[P_J] * domega + t_r
        return a_top, a_bot, domega, t_c, p_elec, p_loss

    @njit(cache=True)
    def rhs_njit(mode_code, t, y, P, xb, cc):
        """mode_code: 0 free, +1/-1 engaged A/B, +2/-2 slipping A/B."""
        r_b, dr_b, f_b_pass, f_stop, pen, f_m, f_d, dr_d, f_t, zr, zrd = _common(t, y, P, xb, cc)
        om = y[OM]
        r = P[P_R]
        dy = np.zeros(NSTATE)
        if P[P_SPAN] > 0.5:
            f_top_ext, f_bot_ext = -f_d, -f_m
        else:
            f_top_ext, f_bot_ext = 0.0, -f_m - f_d
        if mode_code == 0:
            om_a, om_b = r * dr_b, -r * dr_b
            t_a = P[P_COD] * (om_a - om)
            t_b = P[P_COD] * (om_b - om)
            f_b = f_b_pass + r * (t_a - t_b)
            t_gen = P[P_CGEN] * om
            p_mech = t_gen * om
            p_elec = P[P_ETA] * p_mech
            p_gl = (1.0 - P[P_ETA]) * p_mech + P[P_CW] * om * om
            dy[VS] = (f_top_ext - f_b) / P[P_MS]
            dy[VF] = (f_bot_ext + f_b) / P[P_MF]
            dy[OM] = (t_a + t_b - t_gen - P[P_CW] * om) / P[P_J]
            p_clutch = t_a * (om_a - om) + t_b * (om_b - om)
            p_gate = 0.0
        else:
            s = 1.0 if mode_code > 0 else -1.0
            om_other = -s * r * dr_b
            t_other = P[P_COD] * (om_other - om)
            f_other = -s * r * t_other
            p_drag = t_other * (om_other - om)
            if mode_code == 1 or mode_code == -1:
                a_s, a_f, dom, t_c, p_elec, p_gl = _eng_core(s, y, P, f_top_ext, f_bot_ext, f_b_pass + f_other, t_other)
                dy[VS], dy[VF], dy[OM] = a_s, a_f, dom
                f_b = f_b_pass + f_other + s * r * t_c
                p_clutch = p_drag
                p_gate = t_c * om
            else:
                t_cap = P[P_TCAP]
                t_gen = P[P_CGEN] * om
                p_mech = t_gen * om
                p_elec = P[P_ETA] * p_mech
                p_gl = (1.0 - P[P_ETA]) * p_mech + P[P_CW] * om * om
                f_b = f_b_pass + f_other + s * r * t_cap
                dy[VS] = (f_top_ext - f_b) / P[P_MS]
                dy[VF] = (f_bot_ext + f_b) / P[P_MF]
                dy[OM] = (t_cap + t_other - t_gen - P[P_CW] * om) / P[P_J]
                p_clutch = p_drag + t_cap * (s * r * dr_b - om)
                p_gate = t_cap * om
        dy[VU] = (f_m + f_d - f_t) / P[P_MU]
        dy[ZS], dy[ZF], dy[ZU] = y[VS], y[VF], y[VU]
        if P[P_THBL] > 0.0:
            ga = r * dr_b - om
            gb = -r * dr_b - om
            dy[PHA] = ga if ga > 0.0 else 0.0
            dy[PHB] = gb if gb > 0.0 else 0.0
        dy[E_DAMP] = P[P_CS] * dr_d * dr_d
        dy[E_FRIC] = P[P_CB] * dr_b * dr_b
        dy[E_STOP] = (f_stop - P[P_KSTOP] * pen) * dr_b
        dy[E_CLUTCH] = p_clutch
        dy[E_ELEC] = p_elec
        dy[E_GENLOSS] = p_gl + P[P_CT] * (y[VU] - zrd) ** 2
        dy[E_ROAD] = -f_t * zrd
        dy[E_GATE] = p_gate
        dy[E_FRAME] = f_b * dr_b
        return dy

    @njit(cache=True)
    def tc_njit(s, t, y, P, xb, cc):
        r_b, dr_b, f_b_pass, f_stop, pen, f_m, f_d, dr_d, f_t, zr, zrd = _common(t, y, P, xb, cc)
        if P[P_SPAN] > 0.5:
            f_top_ext, f_bot_ext = -f_d, -f_m
        else:
            f_top_ext, f_bot_ext = 0.0, -f_m - f_d
        om = y[OM]
        om_other = -s * P[P_R] * dr_b
        t_other = P[P_COD] * (om_other - om)
        f_other = -s * P[P_R] * t_other
        return _eng_core(s, y, P, f_top_ext, f_bot_ext, f_b_pass + f_other, t_other)[3]


_CODE = {FREE: 0, ENG_A: 1, ENG_B: -1, SLIP_A: 2, SLIP_B: -2}


class QuarterCarGateFast:
    """Drop-in for QuarterCarGate (linear generator only). Same modes, events, transitions."""

    def __init__(self, corner: CornerParams, gate: Gate, road, m_f: float = 8.0,
                 damper_span: str = "full", lock: str | None = None):
        if njit is None:
            raise ImportError("numba is required for QuarterCarGateFast")
        self.c, self.g, self.p, self.road, self.m_f, self.span, self.lock = corner, gate, gate.p, road, m_f, damper_span, lock
        self.P = pack(corner, gate, m_f, damper_span)
        self.xb, self.cc = spline_arrays(road)
        self.nstate = NSTATE

    def rhs(self, mode, t, y):
        return rhs_njit(_CODE[mode], t, y, self.P, self.xb, self.cc)

    def _tc(self, s, t, y):
        return tc_njit(s, t, y, self.P, self.xb, self.cc)

    def _gap(self, s, y):
        return s * self.p.r * (y[VS] - y[VF]) - y[OM] - self.p.eps_engage

    def events(self, mode):
        if self.lock is not None:
            return []
        p = self.p
        ev = []
        if mode == FREE:
            for s, lab in ((+1.0, "A"), (-1.0, "B")):
                if p.theta_bl > 0.0:
                    ev.append((lambda t, y, s=s: self._gap(s, y), +1.0, "arm" + lab))
                    idx = PHA if s > 0 else PHB
                    ev.append((lambda t, y, idx=idx: y[idx] - p.theta_bl, +1.0, "lock" + lab))
                else:
                    ev.append((lambda t, y, s=s: self._gap(s, y), +1.0, "eng" + lab))
        elif mode in (ENG_A, ENG_B):
            s = SIGN[mode]
            lab = "A" if s > 0 else "B"
            ev.append((lambda t, y, s=s: self._tc(s, t, y), -1.0, "dis" + lab))
            if math.isfinite(p.T_cap):
                ev.append((lambda t, y, s=s: self._tc(s, t, y) - p.T_cap, +1.0, "slip" + lab))
        else:
            s = SIGN[mode]
            lab = "A" if s > 0 else "B"
            ev.append((lambda t, y, s=s: self._gap(s, y) + p.eps_engage, -1.0, "unslip" + lab))
        return ev

    def transition(self, mode, label, t, y):
        p, g = self.p, self.g
        y = y.copy()
        kind, lab = label[:-1], label[-1]
        s = +1.0 if lab == "A" else -1.0
        eng_mode = ENG_A if lab == "A" else ENG_B
        slip_mode = SLIP_A if lab == "A" else SLIP_B
        if kind == "arm":
            y[PHA if lab == "A" else PHB] = 0.0
            return FREE, y, None
        if kind in ("eng", "lock"):
            dr = y[VS] - y[VF]
            dv_s, dv_f, om_plus, lam, e_lost = g.impact(s, dr, y[OM], self.c.m_s, self.m_f)
            y_try = y.copy()
            y_try[VS] += dv_s
            y_try[VF] += dv_f
            y_try[OM] = s * p.r * (y_try[VS] - y_try[VF])
            t_c = self._tc(s, t, y_try)
            if t_c < -1e-12:
                return mode, y, {"rejected": True}
            if math.isfinite(p.T_cap) and t_c > p.T_cap:
                return slip_mode, y, {"T_c": t_c}
            y_try[E_CLUTCH] += e_lost
            y_try[PHA if lab == "A" else PHB] = 0.0
            return eng_mode, y_try, {"impulse": lam, "E_lost": e_lost, "T_c0": t_c}
        if kind in ("dis", "unslip"):
            return FREE, y, None
        if kind == "slip":
            return slip_mode, y, None
        raise ValueError(label)

    def initial_mode(self, t, y):
        if self.lock is not None:
            mode = ENG_A if self.lock.upper() == "A" else ENG_B
            y[OM] = SIGN[mode] * self.p.r * (y[VS] - y[VF])
            return mode
        for mode, s in ((ENG_A, +1.0), (ENG_B, -1.0)):
            if self._gap(s, y) > 0.0:
                y_try = y.copy()
                y_try[OM] = s * self.p.r * (y[VS] - y[VF])
                if self._tc(s, t, y_try) >= 0.0:
                    y[OM] = y_try[OM]
                    return mode
        return FREE

    def simulate(self, t_end, y0=None, rtol=1e-8, atol=None, dt_out=2e-3, max_step=5e-3, t_stationary=None) -> SimResult:
        y = np.zeros(NSTATE) if y0 is None else np.array(y0, dtype=float)
        if atol is None:
            atol = np.full(NSTATE, 1e-6)
            atol[[ZS, ZF, ZU]] = 1e-9
            atol[[VS, VF, VU]] = 1e-8
            atol[[PHA, PHB]] = 1e-9
        tr = integrate(self, y, t_end, rtol=rtol, atol=atol, dt_out=dt_out, max_step=max_step)
        res = SimResult(tr.t, tr.y, self.road, self.c, self.g, self.m_f, self.span, tr.segments, tr.events,
                        tr.warnings, tr.n_rhs)
        res.t_stationary = _default_stationary(t_end) if t_stationary is None else t_stationary
        res._qc = self
        return res
