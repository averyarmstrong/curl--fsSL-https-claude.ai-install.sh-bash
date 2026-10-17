"""Closed-form results for the linear passive quarter car (validation anchors).

1. Frequency response / transmissibility H(f) from road displacement to
   sprung displacement, suspension stroke, tire deflection.
2. Mean road input power under an ISO 8608 road via the exact H2 norm
   (Lyapunov equation), eq. (7.1) of docs/01_physics.md and its fixed-body
   limit.  This reproduces Zuo & Zhang (2013) and is the gate for
   validation (b) in the brief.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.linalg import solve_continuous_lyapunov

from ..roads.iso8608 import white_velocity_level
from ..vehicles.quarter_car import CornerParams


def transmissibility(c: CornerParams, f_hz: np.ndarray) -> dict:
    """|H| and phase of z_s/z_r, (z_s-z_u)/z_r, (z_u-z_r)/z_r for the passive linear corner."""
    w = 2 * np.pi * np.asarray(f_hz, float)
    s = 1j * w
    m_s, m_u, k, c_s, k_t, c_t = c.m_s, c.m_u, c.k_m, c.c_s, c.k_t, c.c_t
    g_s = c_s * s + k              # suspension impedance*s
    g_t = c_t * s + k_t
    # [m_s s^2 + g_s, -g_s; -g_s, m_u s^2 + g_s + g_t] [z_s; z_u] = [0; g_t] z_r
    a11 = m_s * s**2 + g_s
    a12 = -g_s
    a22 = m_u * s**2 + g_s + g_t
    det = a11 * a22 - a12 * a12
    z_s = (-a12 * g_t) / det
    z_u = (a11 * g_t) / det
    return {"f": np.asarray(f_hz, float), "H_zs": z_s, "H_stroke": z_s - z_u, "H_tire": z_u - 1.0}


def _state_space(c: CornerParams):
    """x = [r_s = z_s - z_u, v_s, r_t = z_u - z_r, v_u]; input w = ground velocity (white).

    Tire damping is excluded (c_t -> 0) because white velocity through a
    dashpot has infinite mean power; the theorem is stated for c_t = 0.
    """
    m_s, m_u, k, cs, k_t = c.m_s, c.m_u, c.k_m, c.c_s, c.k_t
    A = np.array([
        [0.0, 1.0, 0.0, -1.0],
        [-k / m_s, -cs / m_s, 0.0, cs / m_s],
        [0.0, 0.0, 0.0, 1.0],
        [k / m_u, cs / m_u, -k_t / m_u, -cs / m_u],
    ])
    B = np.array([[0.0], [0.0], [-1.0], [0.0]])
    return A, B


def mean_road_power(c: CornerParams, klass: str, speed: float) -> dict:
    """Exact mean power dissipated (= delivered by the road) for the passive linear corner.

    Steady-state covariance S solves A S + S A^T + B Q B^T = 0 with Q = W_v/2
    (two-sided intensity of the one-sided white level W_v).  Then
    P = c_s E[(v_s - v_u)^2].  Returns also the RMS metrics used in Q3.
    """
    W_v = white_velocity_level(klass, speed)
    A, B = _state_space(c)
    Q = B @ B.T * (W_v / 2.0)
    S = solve_continuous_lyapunov(A, -Q)
    # E[(v_s - v_u)^2] = S11 + S33 - 2 S13  (indices of v_s=1, v_u=3)
    e_dv2 = S[1, 1] + S[3, 3] - 2 * S[1, 3]
    P = c.c_s * e_dv2
    # sprung acceleration: a_s = (-k r_s - cs (v_s - v_u))/m_s  -> variance from S
    g = np.array([-c.k_m / c.m_s, -c.c_s / c.m_s, 0.0, c.c_s / c.m_s])
    var_as = g @ S @ g
    return {"P_road": P, "W_v": W_v, "rms_susp_vel": math.sqrt(e_dv2),
            "rms_stroke": math.sqrt(S[0, 0]), "rms_tire_defl": math.sqrt(S[2, 2]),
            "rms_sprung_accel": math.sqrt(var_as),
            "rms_dyn_tire_load_frac": math.sqrt(S[2, 2]) * c.k_t / c.static_load,
            "P_fixed_body": fixed_body_power(c.k_m, c.k_t, W_v),
            "P_ceiling": W_v * c.k_t / 4.0}


def fixed_body_power(k_eff: float, k_t: float, W_v: float) -> float:
    """Eq. (7.1): P = W_v k_t^2 / (4 (k_t + k_eff)), m_s -> infinity."""
    return W_v * k_t**2 / (4.0 * (k_t + k_eff))


def zuo_baseline(c: CornerParams, speed: float = 26.82) -> dict:
    """Four-corner mean dissipated power on ISO B, C, D at 60 mph — the Zuo & Zhang 2013 check."""
    return {k: 4.0 * mean_road_power(c, k, speed)["P_road"] for k in ("A", "B", "C", "D")}


# ---------------------------------------------------------------------------
# Linearised corner-with-Gate: exact H2 surrogate for the nonlinear hybrid model
# ---------------------------------------------------------------------------
def linear_gate_power(c: CornerParams, klass: str, speed: float, k_b: float, c_eq: float,
                      m_f: float = 8.0, b_inert: float = 0.0, c_s_scale: float = 1.0,
                      c_b: float = 0.0, eta: float = 0.85, damper_span: str = "full") -> dict:
    """Mean powers and ride/handling variances for the LINEARISED Gate corner.

    Frame stage between sprung mass and plate m_f: spring k_b in parallel with a
    dashpot c_eq (= c_gen r^2, the full-wave-rectified generator seen from the
    stroke when the rotor tracks the race) plus guide friction c_b, and an
    inerter b_inert (= J r^2 when a clutch is engaged; 0 ignores it).  Main
    spring k_m between m_f and m_u; OEM damper c_s*c_s_scale across the whole
    corner ('full') or across the main stage ('main').  No stops, no clutch
    freewheeling: this is the ceiling of the architecture for small motions,
    and the exact answer for the question "what load should the generator
    present".  States x = [r_b, r_m, r_t, v_s, v_f, v_u], input = ground velocity.
    """
    W_v = white_velocity_level(klass, speed)
    m_s, m_u, k_m, k_t = c.m_s, c.m_u, c.k_m, c.k_t
    cs = c.c_s * c_s_scale
    cf = c_eq + c_b
    b = b_inert
    M = np.array([[m_s + b, -b, 0.0], [-b, m_f + b, 0.0], [0.0, 0.0, m_u]])
    # force rows on (v_s, v_f, v_u) from positions [r_b, r_m, r_t] and velocities [v_s, v_f, v_u]
    Kq = np.array([[-k_b, 0.0, 0.0], [k_b, -k_m, 0.0], [0.0, k_m, -k_t]])
    if damper_span == "full":
        Cd = np.array([[-cs, 0.0, cs], [0.0, 0.0, 0.0], [cs, 0.0, -cs]])
    else:
        Cd = np.array([[0.0, 0.0, 0.0], [0.0, -cs, cs], [0.0, cs, -cs]])
    Cf = np.array([[-cf, cf, 0.0], [cf, -cf, 0.0], [0.0, 0.0, 0.0]])
    Minv = np.linalg.inv(M)
    A = np.zeros((6, 6))
    A[0, 3], A[0, 4] = 1.0, -1.0          # r_b' = v_s - v_f
    A[1, 4], A[1, 5] = 1.0, -1.0          # r_m' = v_f - v_u
    A[2, 5] = 1.0                         # r_t' = v_u - w
    A[3:, :3] = Minv @ Kq
    A[3:, 3:] = Minv @ (Cd + Cf)
    B = np.zeros((6, 1))
    B[2, 0] = -1.0
    S = solve_continuous_lyapunov(A, -(B @ B.T) * (W_v / 2.0))
    e_vb2 = S[3, 3] + S[4, 4] - 2 * S[3, 4]
    if damper_span == "full":
        e_vd2 = S[3, 3] + S[5, 5] - 2 * S[3, 5]
    else:
        e_vd2 = S[4, 4] + S[5, 5] - 2 * S[4, 5]
    p_gate = c_eq * e_vb2
    p_damper = cs * e_vd2
    p_fric = c_b * e_vb2
    accel_row = (Minv @ Kq)[0, :].tolist() + (Minv @ (Cd + Cf))[0, :].tolist()
    g = np.array(accel_row)
    p_supply = 0.25 * k_t * W_v
    return {"P_supply": p_supply, "P_gate": p_gate, "P_elec": eta * p_gate, "P_damper": p_damper,
            "P_friction": p_fric, "closure": abs(p_supply - p_gate - p_damper - p_fric) / p_supply,
            "phi": eta * p_gate / p_supply, "damper_share": p_damper / p_supply,
            "rms_frame_stroke": float(np.sqrt(S[0, 0])), "rms_susp_stroke": float(np.sqrt(S[0, 0] + S[1, 1] + 2 * S[0, 1])),
            "rms_sprung_accel": float(np.sqrt(g @ S @ g)), "rms_dyn_tire_load_frac": float(np.sqrt(S[2, 2]) * k_t / c.static_load),
            "rms_frame_vel": float(np.sqrt(e_vb2))}


def optimise_linear_gate(c: CornerParams, klass: str, speed: float, k_b: float, m_f: float = 8.0,
                         b_inert: float = 0.0, c_s_scales=(1.0, 0.5, 0.25, 0.1, 0.0), c_eq_grid=None,
                         **kw):
    """Grid over reflected generator damping and OEM damper scale; returns a tidy table."""
    import pandas as pd
    c_eq_grid = np.logspace(1, 5, 41) if c_eq_grid is None else np.asarray(c_eq_grid)
    rows = []
    for sc in c_s_scales:
        for ce in c_eq_grid:
            r = linear_gate_power(c, klass, speed, k_b, ce, m_f=m_f, b_inert=b_inert, c_s_scale=sc, **kw)
            rows.append({"c_s_scale": sc, "c_eq": ce, **r})
    return pd.DataFrame(rows)
