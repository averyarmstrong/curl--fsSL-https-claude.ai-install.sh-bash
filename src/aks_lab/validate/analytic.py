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
