"""Deterministic road / stroke inputs for hand-checkable verification."""

from __future__ import annotations

import math

import numpy as np

from .iso8608 import RoadProfile


class AnalyticRoad:
    """Road given by closed-form z(t), zdot(t)."""

    def __init__(self, z, zdot, meta=None):
        self._z, self._zd = z, zdot
        self.meta = meta or {}

    def z(self, t):
        return float(self._z(t))

    def zdot(self, t):
        return float(self._zd(t))


def flat():
    return AnalyticRoad(lambda t: 0.0, lambda t: 0.0, {"class": "flat"})


def sine(amplitude: float, freq: float, ramp: float = 0.0):
    """z = A sin(2 pi f t), optionally with a raised-cosine amplitude ramp."""
    w = 2 * math.pi * freq

    def env(t):
        return 1.0 if (ramp <= 0 or t >= ramp) else 0.5 * (1 - math.cos(math.pi * t / ramp))

    def denv(t):
        return 0.0 if (ramp <= 0 or t >= ramp) else 0.5 * math.pi / ramp * math.sin(math.pi * t / ramp)

    return AnalyticRoad(lambda t: amplitude * env(t) * math.sin(w * t),
                        lambda t: amplitude * (denv(t) * math.sin(w * t) + env(t) * w * math.cos(w * t)),
                        {"class": "sine", "A": amplitude, "f": freq})


def step(height: float, t0: float = 0.5, rise: float = 0.02):
    """Smooth (raised-cosine) step of given height over `rise` seconds."""
    def z(t):
        if t <= t0:
            return 0.0
        if t >= t0 + rise:
            return height
        return 0.5 * height * (1 - math.cos(math.pi * (t - t0) / rise))

    def zd(t):
        if t <= t0 or t >= t0 + rise:
            return 0.0
        return 0.5 * height * math.pi / rise * math.sin(math.pi * (t - t0) / rise)

    return AnalyticRoad(z, zd, {"class": "step", "h": height})


def bump(height: float, length: float, speed: float, t0: float = 0.5):
    """Half-sine bump of given height and length traversed at speed (a speed bump)."""
    T = length / speed

    def z(t):
        tau = t - t0
        return height * math.sin(math.pi * tau / T) if 0 <= tau <= T else 0.0

    def zd(t):
        tau = t - t0
        return height * math.pi / T * math.cos(math.pi * tau / T) if 0 <= tau <= T else 0.0

    return AnalyticRoad(z, zd, {"class": "bump", "h": height, "L": length, "v": speed})


def from_samples(t: np.ndarray, z: np.ndarray, meta=None) -> RoadProfile:
    """Measured profile already sampled in time (e.g. a profilometer trace at known speed)."""
    return RoadProfile(np.asarray(t, float), np.asarray(z, float), meta=meta or {"class": "measured"})


def from_spatial_profile(x_m: np.ndarray, z_m: np.ndarray, speed: float, meta=None) -> RoadProfile:
    """Measured elevation vs distance, traversed at constant speed."""
    x = np.asarray(x_m, float)
    return RoadProfile(x / speed, np.asarray(z_m, float), meta=meta or {"class": "measured", "speed": speed})
