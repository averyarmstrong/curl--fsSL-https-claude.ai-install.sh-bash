# Experiment 008 — what the road-power theorem leaves out: body forces and wheel lift-off

**Question.** The theorem (`01_physics` §7) covers the road-through-tire
channel. Two things it does not: forces applied directly to the body (wind
buffeting, powertrain vibration, payload) and loss of tire contact. How many
watts do they add or remove, per corner, for a car and a tactical vehicle?
(Gravity and vehicle weight are covered by `tests/test_gravity_body_force_liftoff.py`:
a full-coordinate model with g and preloads reproduces the perturbation
model to 10⁻⁶; weight sets the operating point and does no net work.)

**Setup.** `config.yaml`. Mid-size car and HMMWV, ISO A–E, 60 mph, 40 s, 2
seeds, stock damper, Gate at r = 300 / J = 3e-5 / c_gen 0.01. Body-force
channel: band-limited white force on the sprung mass per corner — "wind_lo"
25 N RMS 0.2–3 Hz (~100 N per vehicle, gusty highway), "wind_hi" 100 N RMS
(~400 N per vehicle: strong crosswind on a tall van), "powertrain" 100 N
RMS 20–40 Hz. One-sided tire (contact lost when total tire force reaches
zero) on the road-only case. 200 cases, 0 errors, closures < 10⁻⁵; the
ledger now carries `E_body` as an input beside `E_road`.

**Answer** (`results/summary.csv`; medians).

| channel | car, ISO C: P_body → ΔP_elec | HMMWV, ISO C | analytic bracket (linear) |
|---|---|---|---|
| wind_lo 25 N RMS | 0.23 W → +0.05 W | 0.20 W → +0.02 W | 0.13 / 0.06 W |
| wind_hi 100 N RMS | 2.3 W → +0.54 W | 1.5 W → +0.15 W | 2.0 / 0.9 W |
| powertrain 100 N, 20–40 Hz | 0.00 W → 0.00 W | 0.00 W → 0.00 W | 0.00 W |
| road supply, same row | 122 W → 9.6 W | 271 W → 27.8 W | 122 / 271 W |

| lift-off (one-sided tire) | car | HMMWV |
|---|---|---|
| ISO D: airborne fraction (linear tire) → ΔP_road, ΔP_elec | 0.4 % → −1.4 W, −0.04 W | 1.1 % → −6.6 W, −0.6 W |
| ISO E: | 9.9 % → −228 W, −4.9 W | 13.3 % → −714 W, −50 W |

1. **Wind is a 1–2 % channel at the extreme.** Even 400 N RMS of gust
   load on the whole vehicle — more than a passenger car sees on a
   highway — delivers ~2 W per corner into the suspension and raises the
   Gate's output by half a watt. At realistic levels it is 0.1–0.2 W. The
   road channel on ISO A (the smoothest class) is still 4–8× larger.
2. **Powertrain vibration delivers nothing** to the suspension: at 20–40 Hz
   the body is above both its modes and does not move; the force does no
   work. (It is a real NVH input; it is not an energy input.)
3. **Lift-off removes supply.** With a one-sided tire the road channel is
   unchanged on A–C (no lift-off), drops 1 % on D and 12–16 % on E (the
   wheel is off the ground 10–13 % of the time and no power flows through
   an open contact). The theorem's ¼·k_t·W_v is an upper bound once contact
   can be lost — F1's direction is confirmed, not weakened.
4. **Gravity.** Carrying g, free lengths and preloads explicitly gives the
   same trajectories to 10⁻⁶ (test). A deterministic bump dissipates *less*
   energy in a 4× heavier corner at matched ride tune (153 → 108 J): weight
   is not the lever; tire stiffness is.

**Caveats.** Wind modelled as a vertical body force with a flat spectrum in
band; aerodynamic lift on a car is mostly steady with gust content below
1 Hz, so even "wind_hi" is generous. No pitch/roll (half-car would route
part of a gust through two corners). Powertrain forcing acts on the body
only; a driveline mounted to the axle would act on m_u (hop mode) — small
and not harvestable at the frame stage either.

**Ledger.** +0.05 / +0.54 W per corner (car, ISO C) for 25 / 100 N RMS
gust load; 0 W powertrain; lift-off −1 % (D), −12 % (E) of road supply.
Tag modeled, exp 008, 2026-10-17. Figure `results/fig_channels.png`.
