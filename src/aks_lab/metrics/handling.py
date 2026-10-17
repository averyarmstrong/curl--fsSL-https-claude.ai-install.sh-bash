"""Road-holding metrics: dynamic tire load variation and lift-off fraction."""

from __future__ import annotations

import numpy as np


def handling_metrics(res) -> dict:
    m = res.mask()
    f_t = res.tire_force()[m]
    w = res.corner.static_load
    return {
        "dtl_rms_frac": float(np.std(f_t) / w),
        "dtl_max_frac": float(np.max(np.abs(f_t)) / w),
        "liftoff_frac": float(np.mean(f_t < -w)),   # perturbation force below -static = net zero load
    }
