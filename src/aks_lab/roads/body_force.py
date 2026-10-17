"""Direct body-force inputs (wind buffeting, powertrain vibration, payload motion).

A separate input channel from the road: F_body(t) acts on the sprung mass and
its work is booked in E_body (docs/01_physics.md §5b).  Band-limited white
noise of a given RMS between f_lo and f_hi, synthesised like the road (sum of
cosines, random phases), served through one cubic spline.
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline


class ForceSeries:
    def __init__(self, t: np.ndarray, f: np.ndarray, meta: dict | None = None):
        self._s = CubicSpline(t, f)
        self.meta = meta or {}

    def __call__(self, t: float) -> float:
        return float(self._s(t))


def band_limited_force(rms: float, f_lo: float, f_hi: float, duration: float, dt: float = 2e-3,
                       n_components: int = 512, seed: int | None = None, ramp: float = 0.5) -> ForceSeries:
    if rms <= 0.0:
        return ForceSeries(np.array([0.0, duration]), np.zeros(2), {"rms": 0.0})
    rng = np.random.default_rng(seed)
    f = np.linspace(f_lo, f_hi, n_components)
    amp = rms * np.sqrt(2.0 / n_components)
    phase = rng.uniform(0.0, 2.0 * np.pi, n_components)
    t = np.arange(0.0, duration + dt, dt)
    x = (np.cos(2.0 * np.pi * np.outer(t, f) + phase) * amp).sum(axis=1)
    if ramp > 0.0:
        x = x * np.where(t < ramp, 0.5 * (1.0 - np.cos(np.pi * t / ramp)), 1.0)
    return ForceSeries(t, x, {"rms": rms, "band": (f_lo, f_hi), "seed": seed})
