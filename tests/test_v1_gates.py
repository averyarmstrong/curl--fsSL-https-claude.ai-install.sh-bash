"""V1 validation gates — analytic limits (see docs/PHYSICS.md §7).

V1a  locked clutch reproduces the exact kinematic ratio (bench + full model)
V1b  no-input flywheel spin-down matches omega0*exp(-c_w*t/J)
V1c  pure spring (rectifier disconnected): F-x loop encloses ZERO area
V1d  rectified case: F-x loop area POSITIVE and equal to harvested energy
     + losses + storage change (full-wave: rotor never driven backwards)
V1e  full quarter-car on an ISO 8608 road: energy audit closes within 1%

These are hard gates: a twin that fails any of them is noise, not a model.
"""

import dataclasses
import math

import numpy as np
import pytest

from gatetwin import (
    BenchRig,
    NullGenerator,
    Params,
    PMGenerator,
    QuarterCarGate,
    iso8608_profile,
    raised_cosine,
    still,
)

P = Params()  # baseline; tests override fields explicitly where the limit requires it


# ---------------------------------------------------------------------------
# V1a — locked clutch = exact kinematic ratio
# ---------------------------------------------------------------------------
class TestV1aKinematicRatio:
    def test_bench_locked_ratio(self):
        """omega integrated as an ODE state must track Gt*xdot to solver tol."""
        rig = BenchRig(P, PMGenerator(), raised_cosine(0.04, 1.5))
        res = rig.simulate(4.0, lock=True, rtol=1e-10, atol=1e-12)
        xdot = res.stroke_rate()
        err = np.max(np.abs(res.omega - P.Gt * xdot))
        assert err < 1e-6 * np.max(np.abs(res.omega))

    def test_full_model_locked_ratio(self):
        road = iso8608_profile("C", speed=20.0, duration=3.0, seed=7)
        model = QuarterCarGate(P, PMGenerator(), road)
        res = model.simulate(3.0, lock="A", rtol=1e-9)
        kin = P.Gt * res.frame_stroke_rate
        scale = max(np.max(np.abs(kin)), 1.0)
        assert np.max(np.abs(res.omega - kin)) < 1e-6 * scale


# ---------------------------------------------------------------------------
# V1b — spin-down matches exp(-c_w t / J)
# ---------------------------------------------------------------------------
class TestV1bSpinDown:
    def test_freewheel_decay(self):
        p = dataclasses.replace(P, c_od=0.0, c_w=5e-4)  # tau = J/c_w = 0.6 s
        rig = BenchRig(p, PMGenerator(R_load=None), still())  # open circuit
        omega0 = 300.0
        res = rig.simulate(1.2, omega0=omega0, rtol=1e-11, atol=1e-13)
        analytic = omega0 * np.exp(-p.c_w * res.t / p.J)
        rel = np.max(np.abs(res.omega - analytic) / omega0)
        assert rel < 1e-6
        assert res.engage_counts == {"A": 0, "B": 0}


# ---------------------------------------------------------------------------
# V1c — pure spring: zero enclosed area
# ---------------------------------------------------------------------------
class TestV1cZeroArea:
    def test_spring_only_loop_area_zero(self):
        """Rectifier disconnected, no parasitics: net work over full cycles = 0."""
        p = dataclasses.replace(P, c_b=0.0, c_od=0.0)
        rig = BenchRig(p, NullGenerator(), raised_cosine(0.04, 1.5), force_freewheel=True)
        n_cycles, f = 5, 1.5
        res = rig.simulate(n_cycles / f, rtol=1e-10, atol=1e-12)
        w_net = res.y[1, -1] - res.y[1, 0]  # E_WORK
        elastic_scale = 0.5 * p.k_b * 0.04**2
        assert abs(w_net) < 1e-6 * elastic_scale


# ---------------------------------------------------------------------------
# V1d — rectified: positive enclosed area = harvested energy (audited)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def v1d_result():
    rig = BenchRig(P, PMGenerator(), raised_cosine(0.05, 1.5))
    return rig.simulate(8.0, rtol=1e-9, atol=1e-11)


class TestV1dRectifiedArea:
    def test_full_wave_rectification(self, v1d_result):
        result = v1d_result
        """Rotor spun the SAME direction on both stroke directions, never negative."""
        assert result.omega.min() > -1e-8
        assert result.engage_counts["A"] >= 2
        assert result.engage_counts["B"] >= 2
        assert result.omega.max() > 50.0

    def test_positive_loop_area(self, v1d_result):
        """Work per steady cycle is positive = energy leaves through the machine."""
        result = v1d_result
        f = 1.5
        t = result.t
        e_work = result.y[1]
        w_last = np.interp(t[-1], t, e_work) - np.interp(t[-1] - 1.0 / f, t, e_work)
        assert w_last > 0.0
        e_elec = result.y[3, -1]
        assert e_elec > 0.0

    def test_energy_closure(self, v1d_result):
        audit = v1d_result.energy_audit()
        assert audit["closure"] < 0.005, audit


# ---------------------------------------------------------------------------
# V1e — full system on ISO road: energy audit closes < 1%
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def v1e_result():
    road = iso8608_profile("C", speed=25.0, duration=6.0, seed=42)
    model = QuarterCarGate(P, PMGenerator(), road)
    return model.simulate(6.0, rtol=1e-8)


class TestV1eFullSystemAudit:
    def test_energy_closure(self, v1e_result):
        audit = v1e_result.energy_audit()
        assert audit["E_road_in"] > 0.0
        assert audit["closure"] < 0.01, audit

    def test_rectifier_active_and_one_way(self, v1e_result):
        assert v1e_result.omega.min() > -1e-8
        assert v1e_result.engage_counts["A"] + v1e_result.engage_counts["B"] > 10
        assert v1e_result.y[10, -1] > 0.0  # E_ELEC: some harvest on class C

    def test_body_and_wheel_modes_sane(self, v1e_result):
        """Sprung mass should move much less than the road at wheel-hop scale."""
        assert np.std(v1e_result.y[0]) < 0.1  # z_s bounded, no blow-up
        assert math.isfinite(v1e_result.storage(-1))
