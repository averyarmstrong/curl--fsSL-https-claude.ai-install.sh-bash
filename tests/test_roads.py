"""ISO 8608 synthesis checks and the white-velocity level used by the road-power theorem."""

import numpy as np
from scipy.signal import welch

from aks_lab.roads import ISO8608_GD0, bump, iso8608_profile, sine, step, white_velocity_level


def test_psd_matches_iso_target():
    v, dur, dt = 20.0, 60.0, 1e-3
    road = iso8608_profile("C", speed=v, duration=dur, dt=dt, seed=3)
    t = np.arange(5.0, dur, dt)
    z = np.array([road.z(ti) for ti in t])
    f, s = welch(z, fs=1.0 / dt, nperseg=2**14)
    for f_chk in (0.5, 1.0, 2.0, 5.0, 10.0):
        n = f_chk / v
        target = ISO8608_GD0["C"] * (n / 0.1) ** -2 / v
        got = np.interp(f_chk, f, s)
        assert 0.4 < got / target < 2.5, (f_chk, got, target)


def test_velocity_is_white_at_the_predicted_level():
    v, dur, dt = 25.0, 120.0, 1e-3
    road = iso8608_profile("B", speed=v, duration=dur, dt=dt, seed=9)
    t = np.arange(5.0, dur, dt)
    zd = np.array([road.zdot(ti) for ti in t])
    f, s = welch(zd, fs=1.0 / dt, nperseg=2**15)
    band = (f > 0.5) & (f < 30.0)
    level = np.mean(s[band])
    assert 0.7 < level / white_velocity_level("B", v) < 1.4


def test_class_ordering():
    stds = []
    for k in "ABCDE":
        road = iso8608_profile(k, speed=20.0, duration=20.0, seed=11)
        t = np.arange(2.0, 20.0, 1e-2)
        stds.append(np.std([road.z(ti) for ti in t]))
    assert all(a < b for a, b in zip(stds, stds[1:])), stds


def test_ramp_starts_quiescent():
    road = iso8608_profile("D", speed=25.0, duration=10.0, seed=5)
    assert abs(road.z(0.0)) < 1e-12
    assert abs(road.zdot(0.0)) < 5e-5


def test_deterministic_inputs_consistent():
    """zdot integrates back to z (robust to the velocity kinks of step and bump)."""
    from scipy.integrate import cumulative_trapezoid
    for r in (sine(0.01, 2.0, ramp=1.0), step(0.02), bump(0.05, 1.0, 10.0)):
        t = np.linspace(0.0, 3.0, 300001)
        z = np.array([r.z(ti) for ti in t])
        zd = np.array([r.zdot(ti) for ti in t])
        zi = cumulative_trapezoid(zd, t, initial=0.0)
        assert np.max(np.abs(zi - z)) < 1e-3 * max(np.max(np.abs(z)), 1e-9) + 1e-7
