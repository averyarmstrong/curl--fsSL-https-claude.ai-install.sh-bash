"""The Armstrong Gate as a reusable element (US 12,409,695 B2 mechanism only).

The element owns everything between its two end nodes (top plate, bottom
plate): bias spring, guide friction, hard stops, drive ratio r, the opposed
sprag pair, rotor inertia J with windage, and the generator.  A host model
(quarter car, bench rig, later a buoy or a leg) supplies the stroke
coordinate r_b = z_top - z_bot and the masses of the two end nodes; the
element supplies forces, the engaged-mode coupling, events and impacts.

Interface summary (docs/01_physics.md §3-4):
  passive_force(r, dr)              -> F_b_passive, F_stop, pen
  race_speeds(dr)                   -> (omega_A, omega_B) = (+r dr, -r dr)
  overrun(dr, omega)                -> (T_A, T_B, F_axial, P_clutch_drag)
  resist_torque(omega)              -> T_r = T_gen + c_w*omega, P_elec, P_loss_total
  engaged_accels(s, m_top, m_bot, F_top_ext, F_bot_ext, F_b_passive, omega)
                                    -> a_top, a_bot, domega, T_c
  impact(s, dr, omega, m_top, m_bot)-> (dv_top, dv_bot, omega_plus, Lambda, E_lost)

Modes are decided by the host's hybrid integrator using the event functions
engage_fn / disengage_fn / slip_exit_fn defined here, so the clutch logic
lives in one place.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .generator import LinearGenerator, NullGenerator

FREE, ENG_A, ENG_B, SLIP_A, SLIP_B = "free", "engA", "engB", "slipA", "slipB"
SIGN = {ENG_A: +1.0, ENG_B: -1.0, SLIP_A: +1.0, SLIP_B: -1.0}
ENGAGED = {ENG_A: ENG_A, ENG_B: ENG_B}


@dataclass(frozen=True)
class GateParams:
    """Mechanical parameters of one Gate unit (SI). Provenance lives in params/*.yaml."""

    k_b: float               # bias spring rate, N/m
    c_b: float = 100.0       # guide friction, viscous equivalent, N s/m
    x_c: float = 0.05        # compression travel to coil bind from equilibrium, m
    x_e: float = 0.05        # extension travel to retainer from equilibrium, m
    k_stop: float = 2.0e6    # stop stiffness, N/m
    c_stop: float = 8.0e3    # stop damping, N s/m
    r: float = 1484.0        # drive ratio, rad of rotor per m of stroke
    J: float = 3.0e-4        # rotor + flyweight inertia at the rotor, kg m^2
    c_w: float = 5.0e-5      # windage/bearing drag, N m s/rad
    c_od: float = 2.0e-4     # sprag overrunning drag (viscous equiv.), N m s/rad
    theta_bl: float = 0.0    # engagement backlash, rad (0 = impact-free)
    T_cap: float = math.inf  # sprag torque capacity, N m (inf = never slips)
    sprag_liftoff_rpm: float = 1200.0
    eps_engage: float = 1.0e-6

    @property
    def Jr(self) -> float:
        """Rotor inertia reflected onto the stroke DOF (an inertance), kg."""
        return self.J * self.r**2

    @property
    def travel(self) -> float:
        return self.x_c + self.x_e


@dataclass
class Gate:
    p: GateParams
    gen: object = field(default_factory=NullGenerator)

    # ---- passive frame stage ----------------------------------------------
    def stop_force(self, r: float, dr: float):
        p = self.p
        if r > p.x_c:
            pen = r - p.x_c
            f = max(0.0, p.k_stop * pen + p.c_stop * dr)
        elif r < -p.x_e:
            pen = r + p.x_e
            f = min(0.0, p.k_stop * pen + p.c_stop * dr)
        else:
            pen, f = 0.0, 0.0
        return f, pen

    def passive_force(self, r: float, dr: float):
        """Force the frame stage exerts, positive = resisting collapse (+r)."""
        f_stop, pen = self.stop_force(r, dr)
        return self.p.k_b * r + self.p.c_b * dr + f_stop, f_stop, pen

    def stop_loss_rate(self, f_stop: float, pen: float, dr: float) -> float:
        """Dissipative part of the stop force power (conservative part is storage)."""
        return (f_stop - self.p.k_stop * pen) * dr

    # ---- rectifier ---------------------------------------------------------
    def race_speeds(self, dr: float):
        return self.p.r * dr, -self.p.r * dr

    def overrun(self, dr: float, omega: float):
        """Overrunning drag torques on both races and their axial reaction on the stroke."""
        om_a, om_b = self.race_speeds(dr)
        t_a = self.p.c_od * (om_a - omega)
        t_b = self.p.c_od * (om_b - omega)
        f_axial = self.p.r * (t_a - t_b)      # adds to the force resisting the stroke
        p_drag = t_a * (om_a - omega) + t_b * (om_b - omega)
        return t_a, t_b, f_axial, p_drag

    def resist_torque(self, omega: float):
        t_gen, p_elec, p_gl = self.gen.torque(omega)
        return t_gen + self.p.c_w * omega, p_elec, p_gl + self.p.c_w * omega**2

    def engaged_accels(self, s, m_top, m_bot, f_top_ext, f_bot_ext, f_b_pass, omega, t_ext=0.0):
        """Solve the coupled 2x2 system of eq. (4.3) with reflected inertance.

        f_top_ext / f_bot_ext: external forces on the end nodes NOT including the
        frame stage (e.g. damper on the top node, main spring on the bottom node).
        t_ext: external torque on the rotor besides generator/windage (e.g. the
        other race's overrun drag), positive = accelerating.
        Returns accelerations, rotor acceleration and the clutch torque T_c.
        """
        p = self.p
        t_r, p_elec, p_loss = self.resist_torque(omega)
        t_r = t_r - t_ext
        jr = p.Jr
        b1 = f_top_ext - f_b_pass - s * p.r * t_r
        b2 = f_bot_ext + f_b_pass + s * p.r * t_r
        if math.isinf(m_top):
            a_top = 0.0
            a_bot = b2 / (m_bot + jr)
        elif math.isinf(m_bot):
            a_bot = 0.0
            a_top = b1 / (m_top + jr)
        else:
            det = m_top * m_bot + jr * (m_top + m_bot)
            a_top = ((m_bot + jr) * b1 + jr * b2) / det
            a_bot = (jr * b1 + (m_top + jr) * b2) / det
        domega = s * p.r * (a_top - a_bot)
        t_c = p.J * domega + t_r
        return a_top, a_bot, domega, t_c, p_elec, p_loss

    def impact(self, s, dr, omega, m_top, m_bot):
        """Inelastic lock-up when the race leads the rotor by d_omega (eq. 4.5)."""
        p = self.p
        d_om = s * p.r * dr - omega
        inv_m = (0.0 if math.isinf(m_top) else 1.0 / m_top) + (0.0 if math.isinf(m_bot) else 1.0 / m_bot)
        denom = 1.0 / p.J + p.r**2 * inv_m
        lam = d_om / denom
        dv_top = 0.0 if math.isinf(m_top) else -s * p.r * lam / m_top
        dv_bot = 0.0 if math.isinf(m_bot) else +s * p.r * lam / m_bot
        omega_plus = omega + lam / p.J
        e_lost = 0.5 * d_om * d_om / denom
        return dv_top, dv_bot, omega_plus, lam, e_lost

    # ---- event functions (host passes stroke rate and rotor speed) ---------
    def engage_gap(self, s, dr, omega) -> float:
        """> 0 when race s is trying to overrun the rotor in the driving sense."""
        return s * self.p.r * dr - omega - self.p.eps_engage

    def race_rpm(self, dr: float) -> float:
        return abs(dr) * self.p.r * 60.0 / (2.0 * math.pi)

    def describe(self) -> dict:
        d = {k: getattr(self.p, k) for k in self.p.__dataclass_fields__}
        d["Jr"] = self.p.Jr
        d["generator"] = self.gen.describe()
        return d


def linear_gate(k_b: float, c_gen: float, eta: float = 0.85, **kw) -> Gate:
    """Convenience: a Gate with a linear generator load."""
    return Gate(GateParams(k_b=k_b, **kw), LinearGenerator(c_gen, eta))
