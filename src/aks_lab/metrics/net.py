"""Net benefit: P_net = P_elec - P_friction - dP_mass - dP_ride (docs/01_physics.md §9)."""

from __future__ import annotations

G = 9.80665


def mass_penalty(delta_m: float, speed: float, c_rr: float = 0.010, grade: float = 0.0,
                 accel: float = 0.0) -> float:
    """Propulsion power to carry delta_m [kg] at `speed` [m/s]: rolling + grade + inertial."""
    return delta_m * (G * (c_rr + grade) + accel) * speed


def p_net(energy: dict, delta_m: float, speed: float, c_rr: float = 0.010) -> dict:
    dp_mass = mass_penalty(delta_m, speed, c_rr)
    return {
        "P_elec": energy["P_elec"],
        "P_friction_total": energy["P_friction_total"],
        "dP_mass": dp_mass,
        "dP_ride": None,          # TODO(bench): no defensible W-per-(m/s^2) exchange rate; reported as metric
        "P_net": energy["P_elec"] - energy["P_friction_total"] - dp_mass,
        "P_net_note": "P_net excludes dP_ride (None); ride delta reported separately",
    }
