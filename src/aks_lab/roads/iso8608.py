"""Road inputs: ISO 8608 synthetic profiles (and later: measured-profile ingest).

ISO 8608:2016 one-sided displacement PSD:
    Gd(n) = Gd0 * (n/n0)^-2 ,  n0 = 0.1 cycles/m
with Gd0 the class geometric center (A=16e-6 ... E=4096e-6 m^3).

Synthesis: sum of N cosines with uniform random phases on a linear spatial-
frequency grid; amplitude_i = sqrt(2*Gd(n_i)*dn).  A raised-cosine ramp over
the first `ramp` seconds removes the startup step so the energy audit starts
from a quiescent state.  z(t) and dz/dt come from one cubic spline so the
audit's road-power integral is self-consistent.
"""

from __future__ import annotations

import numpy as np
from scipy.interpolate import CubicSpline

ISO8608_GD0 = {
    "A": 16.0e-6,
    "B": 64.0e-6,
    "C": 256.0e-6,
    "D": 1024.0e-6,
    "E": 4096.0e-6,
}
N0 = 0.1  # reference spatial frequency, cycles/m


class RoadProfile:
    """Time-domain road elevation with consistent derivative."""

    def __init__(self, t: np.ndarray, z: np.ndarray, meta: dict | None = None):
        self._spline = CubicSpline(t, z)
        self._dspline = self._spline.derivative()
        self.t_max = float(t[-1])
        self.meta = meta or {}

    def z(self, t: float) -> float:
        return float(self._spline(t))

    def zdot(self, t: float) -> float:
        return float(self._dspline(t))

    @classmethod
    def zero(cls, duration: float = 1e6) -> "RoadProfile":
        t = np.array([0.0, duration])
        return cls(t, np.zeros(2), meta={"class": "none"})


def iso8608_profile(
    klass: str,
    speed: float,
    duration: float,
    dt: float = 1.0e-3,
    n_min: float = 0.011,
    n_max: float = 2.83,
    n_components: int = 1024,
    seed: int | None = None,
    ramp: float = 0.5,
) -> RoadProfile:
    """Synthesize an ISO 8608 class-`klass` profile traversed at `speed` m/s."""
    gd0 = ISO8608_GD0[klass.upper()]
    rng = np.random.default_rng(seed)

    n = np.linspace(n_min, n_max, n_components)
    dn = n[1] - n[0]
    gd = gd0 * (n / N0) ** -2
    amp = np.sqrt(2.0 * gd * dn)
    phase = rng.uniform(0.0, 2.0 * np.pi, n_components)

    t = np.arange(0.0, duration + dt, dt)
    # z(t) = sum_i amp_i cos(2 pi n_i v t + phi_i)
    arg = 2.0 * np.pi * speed * np.outer(t, n) + phase
    z = np.cos(arg) @ amp
    z -= z[0]

    if ramp > 0.0:
        env = np.where(t < ramp, 0.5 * (1.0 - np.cos(np.pi * t / ramp)), 1.0)
        z = z * env

    meta = {
        "class": klass.upper(),
        "Gd0": gd0,
        "speed": speed,
        "seed": seed,
        "n_band": (n_min, n_max),
        "provenance": "ISO 8608:2016 Gd(n)=Gd0*(n/n0)^-2, n0=0.1 cycles/m",
    }
    return RoadProfile(t, z, meta=meta)
