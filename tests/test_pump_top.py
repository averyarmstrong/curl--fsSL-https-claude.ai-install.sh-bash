"""docs/03a_pump_top_first_principles.md: the toy, modeled, with its ledger and ceilings."""

from dataclasses import replace

import numpy as np

from aks_lab.toy import PumpTop, PumpTopParams

BASE = PumpTopParams()


def test_ledger_closes_half_and_full_wave():
    for fw in (False, True):
        r = PumpTop(replace(BASE, full_wave=fw)).simulate(3.0)
        a = r.energy_audit()
        assert a["closure"] < 1e-6, a
        assert a["E_hand"] > 0 and a["dKE_rotor"] > 0
        assert all(a[k] >= -1e-9 for k in ("E_screw", "E_bearing", "E_aero", "E_pawl", "E_stoploss"))


def test_race_ceiling_rotor_never_faster_than_plunger_race():
    """The pawl can only push the rotor UP TO r*v; whatever the hand force, omega_max <= r*v_max (per push)."""
    r = PumpTop(replace(BASE, hand_force=60.0)).simulate(6.0)
    for q in r.per_push():
        assert q["omega_peak"] <= BASE.r * q["v_peak_down"] * (1 + 1e-6) + 1e-9
    assert r.omega.max() <= BASE.r * BASE.hand_vmax


def test_speed_limit_beats_force():
    f2 = PumpTop(replace(BASE, hand_force=30.0)).simulate(6.0).per_push()[-1]["omega_end"]
    v2 = PumpTop(replace(BASE, hand_vmax=2.0)).simulate(6.0).per_push()[-1]["omega_end"]
    base = PumpTop(BASE).simulate(6.0).per_push()[-1]["omega_end"]
    assert v2 > f2 > base


def test_full_wave_captures_more_but_not_more_than_the_hand_gives():
    h = PumpTop(BASE).simulate(6.0).energy_audit()
    f = PumpTop(replace(BASE, full_wave=True)).simulate(6.0).energy_audit()
    assert f["dKE_rotor"] > h["dKE_rotor"]
    assert f["dKE_rotor"] <= f["E_hand"] and h["dKE_rotor"] <= h["E_hand"]


def test_loaded_top_output_bounded_by_hand_power():
    r = PumpTop(replace(BASE, c_load=1e-4)).simulate(9.0)
    late = r.per_push()[5:]
    hand = sum(q["W_hand"] for q in late)
    load = sum(q["E_load"] for q in late)
    assert 0 < load < hand


def test_hand_stops_top_only_decays():
    y0 = PumpTop(BASE).simulate(3.0).y[:, -1]
    q = PumpTop(replace(BASE, hand_force=0.0)).simulate(4.0, y0=y0)
    assert np.all(np.diff(q.omega) <= 1e-9)
    assert abs(q.energy_audit()["E_hand"]) < 1e-12
    assert q.energy_audit()["closure"] < 1e-6
