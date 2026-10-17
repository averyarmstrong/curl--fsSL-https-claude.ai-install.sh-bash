"""Quarter-car corner models: passive baseline and corner-with-Gate.

docs/01_physics.md §1 (topology), §4 (rectifier), §6 (ledger).

State vector, Gate model (NSTATE = 18):
  0 z_s 1 v_s 2 z_f 3 v_f 4 z_u 5 v_u 6 omega 7 phi_A 8 phi_B
  9  E_damper   c_s dissipation
  10 E_friction guide friction c_b
  11 E_stop     dissipative part of stop contact
  12 E_clutch   overrun drag + impact loss + slip loss
  13 E_elec     electrical output
  14 E_genloss  generator internal loss + rotor windage
  15 E_road     road work F_t * zdot_r
  16 E_gate     mechanical work delivered through an engaged/slipping clutch
  17 E_frame    work delivered into the frame stage from the top node
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp

from ..elements.gate import ENG_A, ENG_B, FREE, SIGN, SLIP_A, SLIP_B, Gate
from ..solvers.hybrid import HybridTrace, integrate

ZS, VS, ZF, VF, ZU, VU, OM, PHA, PHB = range(9)
E_DAMP, E_FRIC, E_STOP, E_CLUTCH, E_ELEC, E_GENLOSS, E_ROAD, E_GATE, E_FRAME = range(9, 18)
NSTATE = 18
ENERGY_NAMES = ["E_damper", "E_friction", "E_stop", "E_clutch", "E_elec", "E_genloss",
                "E_road", "E_gate", "E_frame"]


@dataclass(frozen=True)
class CornerParams:
    """Passive corner (SI). Provenance in src/aks_lab/vehicles/*.yaml."""

    m_s: float          # sprung mass per corner, kg
    m_u: float          # unsprung mass per corner, kg
    k_m: float          # main spring rate, N/m
    c_s: float          # damper, N s/m
    k_t: float          # tire vertical rate, N/m
    c_t: float = 0.0    # tire damping, N s/m
    name: str = "corner"

    @property
    def static_load(self) -> float:
        return (self.m_s + self.m_u) * 9.80665

    @property
    def body_hz(self) -> float:
        k_ride = self.k_m * self.k_t / (self.k_m + self.k_t)
        return math.sqrt(k_ride / self.m_s) / (2 * math.pi)

    @property
    def hop_hz(self) -> float:
        return math.sqrt((self.k_m + self.k_t) / self.m_u) / (2 * math.pi)


@dataclass
class SimResult:
    t: np.ndarray
    y: np.ndarray
    road: object
    corner: CornerParams
    gate: Gate | None
    m_f: float
    damper_span: str
    segments: list = field(default_factory=list)
    events: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    n_rhs: int = 0
    t_stationary: float = 0.0    # metrics are computed for t >= this
    _qc: object = None           # back-reference to the model (clutch torque reconstruction)

    # -- signals --------------------------------------------------------------
    @property
    def has_gate(self) -> bool:
        return self.gate is not None

    @property
    def z_s(self): return self.y[ZS]
    @property
    def v_s(self): return self.y[VS]
    @property
    def z_f(self): return self.y[ZF] if self.has_gate else self.y[ZS]
    @property
    def v_f(self): return self.y[VF] if self.has_gate else self.y[VS]
    @property
    def z_u(self): return self.y[ZU]
    @property
    def v_u(self): return self.y[VU]
    @property
    def omega(self): return self.y[OM]
    @property
    def frame_stroke(self): return self.z_s - self.z_f
    @property
    def frame_stroke_rate(self): return self.v_s - self.v_f
    @property
    def main_stroke(self): return self.z_f - self.z_u
    @property
    def susp_stroke(self): return self.z_s - self.z_u

    def road_z(self):
        return np.array([self.road.z(ti) for ti in self.t])

    def tire_force(self):
        zr = self.road_z()
        f = self.corner.k_t * (self.z_u - zr)
        if self.corner.c_t:
            zrd = np.array([self.road.zdot(ti) for ti in self.t])
            f = f + self.corner.c_t * (self.v_u - zrd)
        return f

    def sprung_accel(self):
        return np.gradient(self.v_s, self.t)

    def mask(self):
        return self.t >= self.t_stationary

    def mode_at(self):
        """Mode label per output sample (from segments)."""
        modes = np.empty(self.t.size, dtype=object)
        modes[:] = FREE
        for m, t0, t1 in self.segments:
            modes[(self.t >= t0) & (self.t <= t1)] = m
        return modes

    def engage_counts(self) -> dict:
        c = {"A": 0, "B": 0}
        for _t, label, _info in self.events:
            if label in ("lockA", "engA"):
                c["A"] += 1
            elif label in ("lockB", "engB"):
                c["B"] += 1
        return c

    # -- energy -----------------------------------------------------------------
    def storage(self, i: int) -> float:
        c, y = self.corner, self.y[:, i]
        r_t = y[ZU] - self.road.z(self.t[i])
        e = (0.5 * c.m_s * y[VS] ** 2 + 0.5 * c.m_u * y[VU] ** 2 + 0.5 * c.k_t * r_t**2)
        if self.has_gate:
            p = self.gate.p
            r_b = y[ZS] - y[ZF]
            r_m = y[ZF] - y[ZU]
            _f, pen = self.gate.stop_force(r_b, y[VS] - y[VF])
            e += (0.5 * self.m_f * y[VF] ** 2 + 0.5 * p.J * y[OM] ** 2
                  + 0.5 * p.k_b * r_b**2 + 0.5 * c.k_m * r_m**2 + 0.5 * p.k_stop * pen**2)
        else:
            e += 0.5 * c.k_m * (y[ZS] - y[ZU]) ** 2
        return e

    def energies(self, i0: int = 0, i1: int = -1) -> dict:
        y = self.y
        d = {name: y[E_DAMP + k, i1] - y[E_DAMP + k, i0] for k, name in enumerate(ENERGY_NAMES)}
        d["dE_storage"] = self.storage(i1) - self.storage(i0)
        return d

    def energy_audit(self) -> dict:
        e = self.energies()
        diss = (e["E_damper"] + e["E_friction"] + e["E_stop"] + e["E_clutch"]
                + e["E_elec"] + e["E_genloss"])
        residual = e["E_road"] - diss - e["dE_storage"]
        denom = max(abs(e["E_road"]), diss + abs(e["dE_storage"]), 1e-12)
        e["residual"] = residual
        e["closure"] = abs(residual) / denom
        return e

    def rates(self) -> dict:
        """Mean power terms over the stationary window [W]."""
        m = self.mask()
        i0 = int(np.argmax(m))
        T = self.t[-1] - self.t[i0]
        e = self.energies(i0, -1)
        r = {k.replace("E_", "P_"): v / T for k, v in e.items() if k.startswith("E_")}
        r["T_window"] = T
        return r


# ---------------------------------------------------------------------------
# Passive corner (linear 2-DOF) — the Q3 comparator and the analytic anchor
# ---------------------------------------------------------------------------
class PassiveQuarterCar:
    def __init__(self, corner: CornerParams, road, m_extra: float = 0.0):
        """m_extra: Gate hardware mass added to the sprung mass for equal-mass comparison."""
        self.c = corner
        self.m_s = corner.m_s + m_extra
        self.road = road

    def _rhs(self, t, y):
        c = self.c
        zr, zrd = self.road.z(t), self.road.zdot(t)
        r = y[ZS] - y[ZU]
        dr = y[VS] - y[VU]
        f_s = c.k_m * r + c.c_s * dr
        f_t = c.k_t * (y[ZU] - zr) + c.c_t * (y[VU] - zrd)
        dy = np.zeros(NSTATE)
        dy[ZS], dy[ZU] = y[VS], y[VU]
        dy[VS] = -f_s / self.m_s
        dy[VU] = (f_s - f_t) / c.m_u
        dy[E_DAMP] = c.c_s * dr * dr
        dy[E_GENLOSS] = c.c_t * (y[VU] - zrd) ** 2   # tire loss booked here for the passive car
        dy[E_ROAD] = -f_t * zrd
        return dy

    def simulate(self, t_end, rtol=1e-8, atol=1e-9, dt_out=2e-3, max_step=5e-3,
                 t_stationary=None) -> SimResult:
        y0 = np.zeros(NSTATE)
        sol = solve_ivp(self._rhs, (0.0, t_end), y0, method="LSODA", t_eval=np.arange(0, t_end + 1e-12, dt_out),
                        rtol=rtol, atol=atol, max_step=max_step)
        if not sol.success:
            raise RuntimeError(sol.message)
        corner = CornerParams(self.m_s, self.c.m_u, self.c.k_m, self.c.c_s, self.c.k_t, self.c.c_t, self.c.name)
        res = SimResult(sol.t, sol.y, self.road, corner, None, 0.0, "full",
                        segments=[("passive", 0.0, t_end)], n_rhs=sol.nfev)
        res.t_stationary = _default_stationary(t_end) if t_stationary is None else t_stationary
        return res


def _default_stationary(t_end):
    return min(5.0, 0.25 * t_end)


# ---------------------------------------------------------------------------
# Corner with the Gate (hybrid)
# ---------------------------------------------------------------------------
class QuarterCarGate:
    """Chassis -> Gate frame stage -> shortened main spring (+ damper) -> axle -> tire -> road."""

    def __init__(self, corner: CornerParams, gate: Gate, road, m_f: float = 8.0,
                 damper_span: str = "full", lock: str | None = None):
        if damper_span not in ("full", "main"):
            raise ValueError("damper_span must be 'full' or 'main'")
        self.c = corner
        self.g = gate
        self.p = gate.p
        self.road = road
        self.m_f = m_f
        self.span = damper_span
        self.lock = lock
        self.nstate = NSTATE

    # -- common force assembly --------------------------------------------------
    def _common(self, t, y):
        c = self.c
        r_b = y[ZS] - y[ZF]
        dr_b = y[VS] - y[VF]
        r_m = y[ZF] - y[ZU]
        zr, zrd = self.road.z(t), self.road.zdot(t)
        f_b_pass, f_stop, pen = self.g.passive_force(r_b, dr_b)
        f_m = c.k_m * r_m
        dr_d = (y[VS] - y[VU]) if self.span == "full" else (y[VF] - y[VU])
        f_d = c.c_s * dr_d
        f_t = c.k_t * (y[ZU] - zr) + c.c_t * (y[VU] - zrd)
        return r_b, dr_b, f_b_pass, f_stop, pen, f_m, f_d, dr_d, f_t, zr, zrd

    def _ext_forces(self, f_d, f_m):
        if self.span == "full":
            return -f_d, -f_m            # top node, bottom node (excluding frame stage)
        return 0.0, -f_m - f_d

    def _fill(self, dy, y, dr_b, dr_d, f_stop, pen, f_t, zrd, f_b_total,
              p_clutch, p_elec, p_gl, p_gate):
        c, p = self.c, self.p
        dy[ZS], dy[ZF], dy[ZU] = y[VS], y[VF], y[VU]
        dy[E_DAMP] = c.c_s * dr_d * dr_d
        dy[E_FRIC] = p.c_b * dr_b * dr_b
        dy[E_STOP] = self.g.stop_loss_rate(f_stop, pen, dr_b)
        dy[E_CLUTCH] = p_clutch
        dy[E_ELEC] = p_elec
        dy[E_GENLOSS] = p_gl + c.c_t * (y[VU] - zrd) ** 2
        dy[E_ROAD] = -f_t * zrd
        dy[E_GATE] = p_gate
        dy[E_FRAME] = f_b_total * dr_b

    # -- rhs per mode -----------------------------------------------------------
    def rhs(self, mode, t, y):
        c, p, g = self.c, self.p, self.g
        (r_b, dr_b, f_b_pass, f_stop, pen, f_m, f_d, dr_d, f_t, zr, zrd) = self._common(t, y)
        om = y[OM]
        dy = np.zeros(NSTATE)
        f_top_ext, f_bot_ext = self._ext_forces(f_d, f_m)

        if mode == FREE:
            t_a, t_b, f_ax, p_drag = g.overrun(dr_b, om)
            f_b = f_b_pass + f_ax
            t_r, p_elec, p_gl = g.resist_torque(om)
            dy[VS] = (f_top_ext - f_b) / c.m_s
            dy[VF] = (f_bot_ext + f_b) / self.m_f
            dy[OM] = (t_a + t_b - t_r) / p.J
            p_clutch, p_gate = p_drag, 0.0
        else:
            s = SIGN[mode]
            # overrun drag of the non-driving race
            om_other = -s * p.r * dr_b
            t_other = p.c_od * (om_other - om)
            f_other = -s * p.r * t_other          # axial reaction on the stroke
            p_drag = t_other * (om_other - om)
            if mode in (ENG_A, ENG_B):
                a_s, a_f, dom, t_c, p_elec, p_gl = g.engaged_accels(
                    s, c.m_s, self.m_f, f_top_ext, f_bot_ext, f_b_pass + f_other, om, t_ext=t_other)
                dy[VS], dy[VF], dy[OM] = a_s, a_f, dom
                f_b = f_b_pass + f_other + s * p.r * t_c
                p_clutch, p_gate = p_drag, t_c * om
            else:  # slipping at T_cap
                t_cap = p.T_cap
                t_r, p_elec, p_gl = g.resist_torque(om)
                f_b = f_b_pass + f_other + s * p.r * t_cap
                dy[VS] = (f_top_ext - f_b) / c.m_s
                dy[VF] = (f_bot_ext + f_b) / self.m_f
                dy[OM] = (t_cap + t_other - t_r) / p.J
                p_clutch = p_drag + t_cap * (s * p.r * dr_b - om)
                p_gate = t_cap * om
        dy[VU] = (f_m + f_d - f_t) / c.m_u
        # backlash accumulators: advance only while the race leads the rotor
        if p.theta_bl > 0.0:
            ga = p.r * dr_b - om
            gb = -p.r * dr_b - om
            dy[PHA] = ga if ga > 0.0 else 0.0
            dy[PHB] = gb if gb > 0.0 else 0.0
        self._fill(dy, y, dr_b, dr_d, f_stop, pen, f_t, zrd, f_b, p_clutch, p_elec, p_gl, p_gate)
        return dy

    # -- events -----------------------------------------------------------------
    def _tc(self, s, t, y):
        (r_b, dr_b, f_b_pass, f_stop, pen, f_m, f_d, dr_d, f_t, zr, zrd) = self._common(t, y)
        f_top_ext, f_bot_ext = self._ext_forces(f_d, f_m)
        om = y[OM]
        om_other = -s * self.p.r * dr_b
        t_other = self.p.c_od * (om_other - om)
        f_other = -s * self.p.r * t_other
        return self.g.engaged_accels(s, self.c.m_s, self.m_f, f_top_ext, f_bot_ext,
                                     f_b_pass + f_other, om, t_ext=t_other)[3]

    def events(self, mode):
        if self.lock is not None:
            return []
        p, g = self.p, self.g
        ev = []
        if mode == FREE:
            for s, lab in ((+1.0, "A"), (-1.0, "B")):
                if p.theta_bl > 0.0:
                    ev.append((lambda t, y, s=s: g.engage_gap(s, y[VS] - y[VF], y[OM]), +1.0, "arm" + lab))
                    idx = PHA if s > 0 else PHB
                    ev.append((lambda t, y, idx=idx: y[idx] - p.theta_bl, +1.0, "lock" + lab))
                else:
                    ev.append((lambda t, y, s=s: g.engage_gap(s, y[VS] - y[VF], y[OM]), +1.0, "eng" + lab))
        elif mode in (ENG_A, ENG_B):
            s = SIGN[mode]
            lab = "A" if s > 0 else "B"
            ev.append((lambda t, y, s=s: self._tc(s, t, y), -1.0, "dis" + lab))
            if math.isfinite(p.T_cap):
                ev.append((lambda t, y, s=s: self._tc(s, t, y) - p.T_cap, +1.0, "slip" + lab))
        else:
            s = SIGN[mode]
            lab = "A" if s > 0 else "B"
            ev.append((lambda t, y, s=s: g.engage_gap(s, y[VS] - y[VF], y[OM]) + p.eps_engage, -1.0, "unslip" + lab))
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
                return mode, y, {"rejected": True}           # grazing: cannot sustain torque
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
            if self.g.engage_gap(s, y[VS] - y[VF], y[OM]) > 0.0:
                y_try = y.copy()
                y_try[OM] = s * self.p.r * (y[VS] - y[VF])
                if self._tc(s, t, y_try) >= 0.0:
                    y[OM] = y_try[OM]
                    return mode
        return FREE

    # -- driver ---------------------------------------------------------------------
    def simulate(self, t_end, y0=None, rtol=1e-8, atol=None, dt_out=2e-3, max_step=5e-3,
                 t_stationary=None) -> SimResult:
        y = np.zeros(NSTATE) if y0 is None else np.array(y0, dtype=float)
        if atol is None:
            atol = np.full(NSTATE, 1e-6)
            atol[[ZS, ZF, ZU]] = 1e-9
            atol[[VS, VF, VU]] = 1e-8
            atol[[PHA, PHB]] = 1e-9
        tr: HybridTrace = integrate(self, y, t_end, rtol=rtol, atol=atol, dt_out=dt_out, max_step=max_step)
        res = SimResult(tr.t, tr.y, self.road, self.c, self.g, self.m_f, self.span,
                        tr.segments, tr.events, tr.warnings, tr.n_rhs)
        res.t_stationary = _default_stationary(t_end) if t_stationary is None else t_stationary
        res._qc = self
        return res
