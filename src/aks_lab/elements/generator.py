"""Generator / electrical-load models for the Gate shaft.

Interface (all models):  gen.torque(omega) -> (T_gen, P_elec, P_loss)
  T_gen   reaction torque on the rotor, same sign as omega (applied as -T_gen)
  P_elec  electrical power delivered to the load [W]
  P_loss  internal electrical loss [W]
Invariant:  T_gen*omega == P_elec + P_loss  exactly, so the ledger can close.
Rotor windage/bearing drag is a drivetrain property (GateParams.c_w), not a
machine property, and lives in the Gate element.

See docs/01_physics.md §4.3.
"""

from __future__ import annotations

import math

import numpy as np


class NullGenerator:
    """No electrical machine (pure mechanical rig, analytic-limit tests)."""

    name = "null"

    def torque(self, omega: float):
        return 0.0, 0.0, 0.0

    def describe(self) -> dict:
        return {"type": self.name}


class LinearGenerator:
    """T = c_gen * omega with a fixed conversion efficiency eta.

    This is the brief's starting point (`T = c_gen · ω`).  It is also exactly
    a PM machine on a resistive load (see PMGenerator.as_linear).
    """

    name = "linear"

    def __init__(self, c_gen: float, eta: float = 0.85):
        if c_gen < 0.0 or not (0.0 < eta <= 1.0):
            raise ValueError("c_gen >= 0 and 0 < eta <= 1 required")
        self.c_gen = float(c_gen)
        self.eta = float(eta)

    def torque(self, omega: float):
        t = self.c_gen * omega
        p = t * omega
        return t, self.eta * p, (1.0 - self.eta) * p

    def describe(self) -> dict:
        return {"type": self.name, "c_gen": self.c_gen, "eta": self.eta}


class PMGenerator:
    """Permanent-magnet machine on a resistive load.

    e = k_e*omega, i = e/(R_int+R_load), T = k_e*i,
    P_elec = i^2 R_load, P_loss = i^2 R_int.
    Equivalent linear load: c_gen = k_e^2/(R_int+R_load), eta = R_load/(R_int+R_load).
    R_load=None or inf -> open circuit (no torque).
    """

    name = "pm"

    def __init__(self, k_e: float = 0.05, R_int: float = 0.4, R_load: float | None = 1.0):
        self.k_e = float(k_e)
        self.R_int = float(R_int)
        self.R_load = None if R_load is None else float(R_load)

    @property
    def open_circuit(self) -> bool:
        return self.R_load is None or not math.isfinite(self.R_load)

    def torque(self, omega: float):
        if self.open_circuit:
            return 0.0, 0.0, 0.0
        i = self.k_e * omega / (self.R_int + self.R_load)
        return self.k_e * i, i * i * self.R_load, i * i * self.R_int

    def as_linear(self) -> LinearGenerator:
        if self.open_circuit:
            return LinearGenerator(0.0, 1.0)
        rt = self.R_int + self.R_load
        return LinearGenerator(self.k_e**2 / rt, self.R_load / rt)

    def describe(self) -> dict:
        return {"type": self.name, "k_e": self.k_e, "R_int": self.R_int, "R_load": self.R_load}


class ClawPoleAlternator:
    """Claw-pole (Lundell) alternator, measured current curve at a fixed bus voltage.

    Below cut-in the machine free-spins.  Above it the output follows the
    measured curve; mechanical torque = P_elec/(eta*omega).  Cut-in is
    smoothed over ~30 rpm for the ODE solver.  Kept to quantify why a Lundell
    machine is a poor fit for this duty (docs/00_intake.md §6).
    """

    name = "clawpole"
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
        return gate * float(np.interp(rpm, self.curve_rpm, self.curve_amps))

    def torque(self, omega: float):
        w = abs(omega)
        p_elec = self.v_bus * self.current(w * self.RPM)
        if p_elec <= 0.0 or w < 1.0:
            return 0.0, 0.0, 0.0
        p_mech = p_elec / self.eta
        return math.copysign(p_mech / w, omega), p_elec, p_mech - p_elec

    def describe(self) -> dict:
        return {"type": self.name, "v_bus": self.v_bus, "cutin_rpm": self.cutin_rpm, "eta": self.eta}
