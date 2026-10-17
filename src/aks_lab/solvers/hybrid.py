"""Event-driven hybrid ODE integration (modes + terminal events + state resets).

Hard stops are smooth-but-stiff forces (integrated); clutch engage/disengage
and slip transitions are *events* with exact state resets.  No fixed tiny
steps: scipy's LSODA (stiff-aware) with event location.

A system implements:
    nstate: int
    rhs(mode, t, y) -> dy
    events(mode) -> list of (fn(t, y) -> float, direction, label)
    transition(mode, label, t, y) -> (new_mode, y_new, info | None)
        info may carry e.g. {"E_clutch": dE, "impulse": lam}; return
        new_mode == mode to reject a transition (the integrator micro-steps).
    initial_mode(t, y) -> mode
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.integrate import solve_ivp


def _t_grid(t0: float, t1: float, dt: float) -> np.ndarray:
    n = max(int(np.floor((t1 - t0) / dt)), 0)
    ts = t0 + dt * np.arange(n + 1)
    if ts[-1] < t1 - 1e-12:
        ts = np.append(ts, t1)
    else:
        ts[-1] = t1
    return ts


@dataclass
class HybridTrace:
    t: np.ndarray
    y: np.ndarray
    segments: list                      # (mode, t_start, t_end)
    events: list                        # (t, label, info)
    warnings: list = field(default_factory=list)
    n_rhs: int = 0


def integrate(system, y0, t_end, method="LSODA", rtol=1e-8, atol=1e-8, dt_out=2e-3,
              max_step=5e-3, t0=0.0, zeno_limit=200, micro=1e-8) -> HybridTrace:
    y = np.array(y0, dtype=float)
    t = float(t0)
    mode = system.initial_mode(t, y)
    ts_out, ys_out = [np.array([t])], [y.copy()[:, None]]
    segments, evlog, warnings = [], [], []
    zeno, last_te, n_rhs = 0, -1.0, 0

    while t < t_end - 1e-12:
        evs = system.events(mode)
        funcs = []
        for fn, direction, _label in evs:
            def _ev(tt, yy, fn=fn):
                return fn(tt, yy)
            _ev.terminal = True
            _ev.direction = direction
            funcs.append(_ev)
        sol = solve_ivp(lambda tt, yy, m=mode: system.rhs(m, tt, yy), (t, t_end), y,
                        method=method, events=funcs, t_eval=_t_grid(t, t_end, dt_out),
                        rtol=rtol, atol=atol, max_step=max_step)
        n_rhs += sol.nfev
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
        t = te
        label = evs[which][2]
        if te - last_te < 1e-10:
            zeno += 1
            if zeno > zeno_limit:
                warnings.append(f"zeno guard tripped at t={te:.6f} ({label})")
                y = y + micro * system.rhs(mode, t, y)
                t += micro
                zeno, last_te = 0, te
                continue
        else:
            zeno = 0
        last_te = te
        new_mode, y_new, info = system.transition(mode, label, t, y)
        evlog.append((t, label, info))
        if new_mode == mode:
            # rejected transition: nudge past the event to avoid re-triggering
            y_new = y_new + micro * system.rhs(mode, t, y_new)
            t += micro
        y = y_new
        ts_out.append(np.array([t]))
        ys_out.append(y.copy()[:, None])
        mode = new_mode

    return HybridTrace(np.concatenate(ts_out), np.concatenate(ys_out, axis=1),
                       segments, evlog, warnings, n_rhs)
