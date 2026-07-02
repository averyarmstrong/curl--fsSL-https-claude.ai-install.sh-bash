"""ISO 8608 road synthesis checks."""

import numpy as np
from scipy.signal import welch

from gatetwin import ISO8608_GD0, iso8608_profile


def test_psd_matches_iso_target():
    """Temporal PSD of the synthetic profile must track Gd(n)/v in-band."""
    v, dur, dt = 20.0, 60.0, 1e-3
    road = iso8608_profile("C", speed=v, duration=dur, dt=dt, seed=3)
    t = np.arange(5.0, dur, dt)  # skip the startup ramp
    z = np.array([road.z(ti) for ti in t])
    f, s = welch(z, fs=1.0 / dt, nperseg=2**14)
    for f_chk in (0.5, 1.0, 2.0, 5.0, 10.0):
        n = f_chk / v
        target = ISO8608_GD0["C"] * (n / 0.1) ** -2 / v
        got = np.interp(f_chk, f, s)
        assert 0.4 < got / target < 2.5, (f_chk, got, target)


def test_class_ordering():
    """Rougher classes must carry more displacement variance."""
    stds = []
    for k in "ABCDE":
        road = iso8608_profile(k, speed=20.0, duration=20.0, seed=11)
        t = np.arange(2.0, 20.0, 1e-2)
        stds.append(np.std([road.z(ti) for ti in t]))
    assert all(a < b for a, b in zip(stds, stds[1:])), stds


def test_ramp_starts_quiescent():
    road = iso8608_profile("D", speed=25.0, duration=10.0, seed=5)
    assert abs(road.z(0.0)) < 1e-12
    # spline fit of the ramped samples leaves a few-µm/s residual — quiescent
    assert abs(road.zdot(0.0)) < 5e-5
