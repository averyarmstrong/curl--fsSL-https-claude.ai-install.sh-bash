"""ISO 2631-1 W_k realisation against the standard's tabulated weights."""

import numpy as np
import pytest

from aks_lab.metrics import iso2631_wk_rms, wk_weight

# ISO 2631-1:1997 Table 3, W_k principal weights (1/3-octave centre frequencies)
TABLE = {1.0: 0.482, 2.0: 0.531, 4.0: 0.967, 6.3: 1.054, 8.0: 1.036, 16.0: 0.768, 31.5: 0.400}


@pytest.mark.parametrize("f,w", list(TABLE.items()))
def test_wk_matches_table(f, w):
    got = abs(wk_weight([f])[0])
    assert abs(got - w) / w < 0.05, (f, got, w)


def test_weighted_rms_of_pure_tone():
    dt, f = 1e-3, 4.0
    t = np.arange(0, 20, dt)
    a = np.sqrt(2) * np.sin(2 * np.pi * f * t)      # RMS 1
    got = iso2631_wk_rms(a, dt)
    assert abs(got - TABLE[4.0]) / TABLE[4.0] < 0.05
