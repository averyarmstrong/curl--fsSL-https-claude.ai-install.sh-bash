"""Generator/alternator models.

Interface: gen.torque(omega) -> (T_gen, P_elec, P_loss)
  T_gen   shaft reaction torque, same sign as omega (applied as -T_gen on rotor)
  P_elec  electrical power delivered to the load, W
  P_loss  electrical/internal loss inside the machine, W
Mechanical shaft power always satisfies T_gen*omega = P_elec + P_loss exactly,
which is what makes the energy ledger closable.
Rotor windage c_w is a property of the drivetrain (Params), not the machine.
"""

from __future__ import annotations

import math

import numpy as np


class NullGenerator:
    """No electrical machine — pure mechanical rig (V1 limit tests)."""

    def torque(self, omega: float):
        return 0.0, 0.0, 0.0


class PMGenerator:
    """Permanent-magnet machine on a resistive load.

    EMF e = k_e*omega; i = e/(R_int+R_load); T = k_e*i.
    P_elec = i^2*R_load, P_loss = i^2*R_int.
    Peak conversion efficiency = R_load/(R_load+R_int) (85-90% at design point
    for the baseline parameters); off-design degradation enters through the
    fixed R_int as the operating point moves — matching the brief's PM spec.
    R_load=None or inf models open circuit (no torque).
    """

    def __init__(self, k_e: float = 0.05, R_int: float = 0.4, R_load: float | None = 1.0):
        self.k_e = k_e
        self.R_int = R_int
        self.R_load = R_load

    def torque(self, omega: float):
        if self.R_load is None or not math.isfinite(self.R_load):
            return 0.0, 0.0, 0.0
        i = self.k_e * omega / (self.R_int + self.R_load)
        return self.k_e * i, i * i * self.R_load, i * i * self.R_int


class ClawPoleAlternator:
    """Claw-pole (Lundell) alternator: measured current curve at fixed bus voltage.

    Below cut-in the machine free-spins (field produces no net output).  Above
    cut-in, output current follows the measured curve; mechanical torque is
    P_elec/(eta*omega).  The cut-in step is smoothed over ~30 rpm for the ODE
    solver; smoothing width is far below any result's sensitivity.
    """

    RPM = 60.0 / (2.0 * math.pi)

    def __init__(
        self,
        v_bus: float = 14.0,
        cutin_rpm: float = 1600.0,
        curve_rpm=(1600.0, 2000.0, 2500.0, 3500.0, 6000.0),
        curve_amps=(77.0, 100.0, 117.0, 138.0, 152.0),
        efficiency: float = 0.52,
        smooth_rpm: float = 30.0,
    ):
        self.v_bus = v_bus
        self.cutin_rpm = cutin_rpm
        self.curve_rpm = np.asarray(curve_rpm, dtype=float)
        self.curve_amps = np.asarray(curve_amps, dtype=float)
        self.eta = efficiency
        self.smooth_rpm = smooth_rpm

    def current(self, rpm: float) -> float:
        gate = 0.5 * (1.0 + math.tanh((rpm - self.cutin_rpm) / self.smooth_rpm))
        i = float(np.interp(rpm, self.curve_rpm, self.curve_amps))
        return gate * i

    def torque(self, omega: float):
        w = abs(omega)
        rpm = w * self.RPM
        i = self.current(rpm)
        p_elec = self.v_bus * i
        if p_elec <= 0.0 or w < 1.0:
            return 0.0, 0.0, 0.0
        p_mech = p_elec / self.eta
        t = math.copysign(p_mech / w, omega)
        return t, p_elec, p_mech - p_elec
