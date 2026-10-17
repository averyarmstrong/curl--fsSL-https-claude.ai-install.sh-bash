"""Ride metrics: sprung-mass acceleration (raw and ISO 2631-1 W_k weighted), working space.

W_k realised from the standard's transfer functions (ISO 2631-1:1997 Table 3;
parameters as tabulated by Rimell & Mansfield 2007):
  band-limit  Hh(f1=0.4 Hz, Q=1/sqrt2) high-pass, Hl(f2=100 Hz, Q=1/sqrt2) low-pass
  a-v transition Ht: f3 = 12.5, f4 = 12.5, Q4 = 0.63
  upward step    Hs: f5 = 2.37, Q5 = 0.91, f6 = 3.35, Q6 = 0.91
Checked against the tabulated weights at 1, 4, 8, 16 Hz in tests/test_metrics.py.
"""

from __future__ import annotations

import numpy as np

WK = dict(f1=0.4, f2=100.0, f3=12.5, f4=12.5, Q4=0.63, f5=2.37, Q5=0.91, f6=3.35, Q6=0.91)


def wk_weight(f_hz):
    """Complex W_k(f) for frequencies in Hz (array)."""
    f = np.asarray(f_hz, float)
    s = 2j * np.pi * f
    w1, w2 = 2 * np.pi * WK["f1"], 2 * np.pi * WK["f2"]
    w3, w4 = 2 * np.pi * WK["f3"], 2 * np.pi * WK["f4"]
    w5, w6 = 2 * np.pi * WK["f5"], 2 * np.pi * WK["f6"]
    q1 = 1 / np.sqrt(2)
    Hh = s**2 / (s**2 + w1 / q1 * s + w1**2)
    Hl = w2**2 / (s**2 + w2 / q1 * s + w2**2)
    Ht = (s + w3) / w3 * w4**2 / (s**2 + w4 / WK["Q4"] * s + w4**2)
    Hs = (s**2 + w5 / WK["Q5"] * s + w5**2) / (s**2 + w6 / WK["Q6"] * s + w6**2)
    return Hh * Hl * Ht * Hs


def iso2631_wk_rms(a: np.ndarray, dt: float) -> float:
    """Frequency-weighted RMS acceleration (vertical, seated: W_k)."""
    a = np.asarray(a, float)
    a = a - a.mean()
    n = a.size
    A = np.fft.rfft(a)
    f = np.fft.rfftfreq(n, dt)
    W = wk_weight(f)
    W[0] = 0.0
    aw = np.fft.irfft(A * W, n=n)
    return float(np.sqrt(np.mean(aw**2)))


def resample_uniform(t, x, dt=None):
    if dt is None:
        dt = float(np.median(np.diff(t)))
    tu = np.arange(t[0], t[-1], dt)
    return tu, np.interp(tu, t, x), dt


def ride_metrics(res, dt=2e-3) -> dict:
    """Sprung acceleration RMS (raw, W_k), working space, frame stroke stats."""
    m = res.mask()
    t = res.t[m]
    tu, vs, dt = resample_uniform(t, res.v_s[m], dt)
    a_s = np.gradient(vs, dt)
    out = {
        "a_s_rms": float(np.sqrt(np.mean((a_s - a_s.mean()) ** 2))),
        "a_w_rms": iso2631_wk_rms(a_s, dt),
        "sws_rms": float(np.std(res.susp_stroke[m])),
        "sws_max": float(np.max(np.abs(res.susp_stroke[m]))),
    }
    if res.has_gate:
        rb = res.frame_stroke[m]
        p = res.gate.p
        on_stop = (rb > p.x_c) | (rb < -p.x_e)
        out.update({
            "x_b_rms": float(np.std(rb)),
            "x_b_max": float(np.max(rb)), "x_b_min": float(np.min(rb)),
            "t_stop_frac": float(np.mean(on_stop)),
            "t_stop_comp_frac": float(np.mean(rb > p.x_c)),
            "t_stop_ext_frac": float(np.mean(rb < -p.x_e)),
        })
    return out
