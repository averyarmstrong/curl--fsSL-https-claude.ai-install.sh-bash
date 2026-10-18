"""The push-down spinning top ("pump top"), from first principles.

docs/03a_pump_top_first_principles.md.  The toy is the Gate with a hand for
a road: plunger on a return spring, helical shaft of lead L (one turn per
L metres of stroke), a one-way pawl between helix nut and top body (the
flywheel), bearing and air drag, and optionally an electrical load.

Nothing is prescribed.  The hand is a FORCE with a Hill-type force-velocity
limit; the plunger has mass; the pawl is an inequality constraint handled
as an event; the stops are Kelvin-Voigt.  The ledger
    E_hand = KE_plunger + KE_rotor + U_spring + U_stop
             + E_screw + E_bearing + E_aero + E_load + E_pawl + E_stoploss
closes to solver tolerance on every run.

Modes: FREE (pawl overrunning), ENG_DOWN (down-stroke pawl engaged),
ENG_UP (second, opposed pawl engaged; only if full_wave=True).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp

FREE, ENG_DOWN, ENG_UP = "free", "eng_down", "eng_up"
SIGN = {ENG_DOWN: +1.0, ENG_UP: -1.0}

# state indices
X, V, OM = 0, 1, 2
E_HAND, E_SCREW, E_BEAR, E_AERO, E_LOAD, E_PAWL, E_STOPLOSS = 3, 4, 5, 6, 7, 8, 9
NSTATE = 10


@dataclass
class PumpTopParams:
    """All values are `asserted` toy-scale estimates unless a run overrides them (see doc §3)."""
    lead: float = 0.025          # m per revolution of the helix (2.4 turns over a 60 mm stroke)
    stroke: float = 0.060        # m, plunger travel between top and bottom stops
    m_p: float = 0.020           # kg, plunger + helix
    k_r: float = 200.0           # N/m, return spring (zero force at top stop)
    J: float = 1.25e-4           # kg m^2, top body as a 0.1 kg disk of 50 mm radius
    eta_screw: float = 0.80      # helix/nut efficiency while transmitting (tan lam / tan(lam+phi))
    c_w: float = 2.0e-6          # N m s, bearing drag
    c_a: float = 1.0e-8          # N m s^2, air drag ~ omega^2
    c_load: float = 0.0          # N m s, electrical load torque = c_load * omega (0 for a toy)
    k_stop: float = 2.0e5        # N/m, stop stiffness
    c_stop: float = 40.0         # N s/m, stop damping (Kelvin-Voigt)
    full_wave: bool = False      # second, opposed pawl so the up-stroke also drives
    hand_force: float = 15.0     # N, hand push force at zero velocity
    hand_vmax: float = 1.0       # m/s, hand velocity at which push force falls to zero (Hill)
    t_push: float = 0.30         # s, duration of the push in each period
    period: float = 0.60         # s, pump period

    @property
    def r(self) -> float:
        """Race ratio rad/m (same role as the Gate's r)."""
        return 2 * math.pi / self.lead

    @property
    def reflected_mass(self) -> float:
        return self.J * self.r**2


def hill_hand(F0: float, vmax: float):
    """Muscle-like force–velocity law: full force when still, nothing at vmax, never pulls."""
    def f(v):
        return F0 * min(max(1.0 - v / vmax, 0.0), 1.0)
    return f


@dataclass
class PumpTopResult:
    t: np.ndarray
    y: np.ndarray
    p: PumpTopParams
    segments: list
    events: list
    warnings: list = field(default_factory=list)

    @property
    def x(self): return self.y[X]
    @property
    def v(self): return self.y[V]
    @property
    def omega(self): return self.y[OM]

    def race_speed(self):
        return self.p.r * np.abs(self.v) if self.p.full_wave else self.p.r * np.maximum(self.v, 0.0)

    def energy_audit(self) -> dict:
        p, y = self.p, self.y
        ke_p = 0.5 * p.m_p * (y[V, -1] ** 2 - y[V, 0] ** 2)
        ke_r = 0.5 * p.J * (y[OM, -1] ** 2 - y[OM, 0] ** 2)
        u_s = 0.5 * p.k_r * (y[X, -1] ** 2 - y[X, 0] ** 2)
        u_stop = 0.5 * p.k_stop * (_pen(p, y[X, -1]) ** 2 - _pen(p, y[X, 0]) ** 2)
        e = {k: y[i, -1] - y[i, 0] for k, i in (("E_hand", E_HAND), ("E_screw", E_SCREW), ("E_bearing", E_BEAR),
                                                ("E_aero", E_AERO), ("E_load", E_LOAD), ("E_pawl", E_PAWL),
                                                ("E_stoploss", E_STOPLOSS))}
        e.update(dKE_plunger=ke_p, dKE_rotor=ke_r, dU_spring=u_s, dU_stop=u_stop)
        diss = e["E_screw"] + e["E_bearing"] + e["E_aero"] + e["E_load"] + e["E_pawl"] + e["E_stoploss"]
        stored = ke_p + ke_r + u_s + u_stop
        e["residual"] = e["E_hand"] - diss - stored
        e["closure"] = abs(e["residual"]) / max(abs(e["E_hand"]), diss + abs(stored), 1e-12)
        return e

    def per_push(self) -> list[dict]:
        """Hand work, rotor KE gain and losses in each pump period."""
        p = self.p
        out = []
        n = int(math.floor(self.t[-1] / p.period + 1e-9))
        for k in range(n):
            i0 = int(np.searchsorted(self.t, k * p.period))
            i1 = int(np.searchsorted(self.t, (k + 1) * p.period)) - 1
            i1 = min(i1, self.t.size - 1)
            out.append({
                "push": k + 1,
                "W_hand": self.y[E_HAND, i1] - self.y[E_HAND, i0],
                "dKE_rotor": 0.5 * p.J * (self.y[OM, i1] ** 2 - self.y[OM, i0] ** 2),
                "omega_end": self.y[OM, i1],
                "omega_peak": self.y[OM, i0:i1 + 1].max(),
                "v_peak_down": self.y[V, i0:i1 + 1].max(),
                "E_load": self.y[E_LOAD, i1] - self.y[E_LOAD, i0],
                "losses": sum(self.y[i, i1] - self.y[i, i0] for i in (E_SCREW, E_BEAR, E_AERO, E_PAWL, E_STOPLOSS)),
            })
        return out


def _pen(p: PumpTopParams, x: float) -> float:
    if x < 0.0:
        return x
    if x > p.stroke:
        return x - p.stroke
    return 0.0


class PumpTop:
    def __init__(self, p: PumpTopParams, hand=None):
        self.p = p
        self.hand = hand if hand is not None else hill_hand(p.hand_force, p.hand_vmax)

    # ----- forces -------------------------------------------------------------------------------
    def _f_hand(self, t, v):
        tau = t % self.p.period
        return self.hand(v) if tau < self.p.t_push else 0.0

    def _f_stop(self, x, v):
        p = self.p
        pen = _pen(p, x)
        if pen == 0.0:
            return 0.0, 0.0
        f = -p.k_stop * pen - p.c_stop * v          # on the plunger (downward positive)
        # Kelvin–Voigt damping may only dissipate: clip so the contact never pulls
        if pen > 0 and f > 0:
            f = 0.0
        if pen < 0 and f < 0:
            f = 0.0
        loss = -(f + p.k_stop * pen) * v            # damper part only
        return f, max(loss, 0.0) if loss == loss else 0.0

    def _t_rotor_passive(self, om):
        p = self.p
        return p.c_w * om + p.c_a * om * abs(om) + p.c_load * om

    # ----- dynamics -----------------------------------------------------------------------------
    def rhs(self, mode, t, y):
        p = self.p
        x, v, om = y[X], y[V], y[OM]
        f_h = self._f_hand(t, v)
        f_stop, p_stoploss = self._f_stop(x, v)
        f_free = f_h - p.k_r * x + f_stop               # all plunger forces except the pawl
        t_pass = self._t_rotor_passive(om)
        dy = np.zeros(NSTATE)
        if mode == FREE:
            a = f_free / p.m_p
            dom = -t_pass / p.J
            f_c, p_screw = 0.0, 0.0
        else:
            s = SIGN[mode]
            # constraint om = s r v. Plunger: m a = f_free - f_c ; rotor: J dom = eta r' f_c - t_pass
            # with r' = lead/(2 pi) torque per newton... torque T = eta * f_c / r (r = 2 pi / lead)
            # J s r a = eta f_c / r - t_pass  ->  f_c = (J s r a + t_pass) r / eta
            # m a = f_free - (J s r^2 a + t_pass r)/eta  ->  a (m + J r^2 s/eta) = f_free - t_pass r / eta
            # for s = -1 (up-stroke pawl) the sign enters through the helix hand; reflected mass stays positive
            denom = p.m_p + p.J * p.r**2 / p.eta_screw
            a = (f_free - s * t_pass * p.r / p.eta_screw) / denom
            dom = s * p.r * a
            f_c = f_free - p.m_p * a
            p_screw = (1.0 - p.eta_screw) * f_c * v       # power lost in the nut; f_c*v >= 0 on either driving stroke
        dy[X] = v
        dy[V] = a
        dy[OM] = dom
        dy[E_HAND] = f_h * v
        dy[E_SCREW] = p_screw
        dy[E_BEAR] = p.c_w * om * om
        dy[E_AERO] = p.c_a * abs(om) ** 3
        dy[E_LOAD] = p.c_load * om * om
        dy[E_STOPLOSS] = p_stoploss
        return dy

    def _f_c(self, mode, t, y):
        """Pawl force while engaged (>= 0 means the pawl is pushing the rotor)."""
        d = self.rhs(mode, t, y)
        f_free = self._f_hand(t, y[V]) - self.p.k_r * y[X] + self._f_stop(y[X], y[V])[0]
        return f_free - self.p.m_p * d[V]

    def events(self, mode):
        p = self.p
        ev = []
        if mode == FREE:
            ev.append((lambda t, y: p.r * y[V] - y[OM], +1.0, "eng_down"))
            if p.full_wave:
                ev.append((lambda t, y: -p.r * y[V] - y[OM], +1.0, "eng_up"))
        else:
            ev.append((lambda t, y, m=mode: self._f_c(m, t, y) * SIGN[m], -1.0, "dis"))
        return ev

    def simulate(self, t_end: float, y0=None, rtol=1e-9, atol=1e-11, dt_out=1e-3) -> PumpTopResult:
        p = self.p
        y = np.zeros(NSTATE) if y0 is None else np.array(y0, float)
        t = 0.0
        mode = FREE
        ts, ys, segs, evlog, warns = [np.array([0.0])], [y.copy()[:, None]], [], [], []
        # integrate phase by phase (hand on / off) so the force switch is never inside a step
        phase_edges = []
        k = 0
        while k * p.period < t_end:
            phase_edges += [k * p.period + p.t_push, (k + 1) * p.period]
            k += 1
        phase_edges = [e for e in phase_edges if 0 < e < t_end] + [t_end]
        guard = 0
        for t_phase in phase_edges:
            while t < t_phase - 1e-12:
                evs = self.events(mode)
                funcs = []
                for fn, direction, _lab in evs:
                    def _ev(tt, yy, fn=fn):
                        return fn(tt, yy)
                    _ev.terminal, _ev.direction = True, direction
                    funcs.append(_ev)
                sol = solve_ivp(lambda tt, yy, m=mode: self.rhs(m, tt, yy), (t, t_phase), y, method="LSODA",
                                events=funcs, rtol=rtol, atol=atol, max_step=2e-3, dense_output=True)
                t_stop = sol.t[-1]
                grid = np.arange(t, t_stop, dt_out)[1:]
                if grid.size:
                    ts.append(grid)
                    ys.append(sol.sol(grid))
                ts.append(np.array([t_stop]))
                ys.append(sol.y[:, -1:].copy())
                if sol.status == 1:
                    i = next(i for i, te in enumerate(sol.t_events) if te.size)
                    t_new, y_new = sol.t_events[i][0], sol.y_events[i][0].copy()
                    lab = evs[i][2]
                    segs.append((mode, t, t_new))
                    if lab.startswith("eng"):
                        s = +1.0 if lab == "eng_down" else -1.0
                        # lock-up: plunger (m_p) and rotor (J r^2) exchange momentum through the pawl.
                        v0, om0 = y_new[V], y_new[OM]
                        m_eq = p.m_p + p.J * p.r**2
                        v1 = (p.m_p * v0 + s * p.J * p.r * om0) / m_eq
                        om1 = s * p.r * v1
                        e_lost = 0.5 * p.m_p * v0**2 + 0.5 * p.J * om0**2 - 0.5 * p.m_p * v1**2 - 0.5 * p.J * om1**2
                        y_new[V], y_new[OM] = v1, om1
                        y_new[E_PAWL] += max(e_lost, 0.0)
                        mode = ENG_DOWN if s > 0 else ENG_UP
                        evlog.append((t_new, lab, {"E_lost": e_lost}))
                    else:
                        mode = FREE
                        evlog.append((t_new, lab, None))
                    t, y = t_new, y_new
                    guard += 1
                    if guard > 5000:
                        warns.append("event guard hit")
                        break
                else:
                    segs.append((mode, t, t_phase))
                    t, y = t_phase, sol.y[:, -1].copy()
        T = np.concatenate(ts)
        Y = np.concatenate(ys, axis=1)
        order = np.argsort(T, kind="stable")
        return PumpTopResult(T[order], Y[:, order], p, segs, evlog, warns)
