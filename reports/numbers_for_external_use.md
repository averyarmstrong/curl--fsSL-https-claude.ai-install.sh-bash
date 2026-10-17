# Numbers AKS can use outside the building — and the ones it cannot (2026-10-17)

Everything below is traceable to `docs/06_numbers_ledger.md` and the
experiment READMEs. Tags follow the Website Blueprint's claim ladder.
"Modeled" means reproducible from a command in this repo with a closed
energy ledger; no AKS number is "measured" yet.

## What is established physics (say freely)

- The road delivers a fixed power budget to each wheel station:
  P = ¼·k_t·W_v = π²·G_d(n₀)·n₀²·V·k_t. It depends on road roughness,
  speed and tire stiffness only — not on springs, dampers, vehicle weight
  or any device in the suspension. (`docs/01_physics.md` §7, exact.)
- That budget per corner at 60 mph: passenger car 30 W (ISO B, good
  highway), 122 W (ISO C, average), 488 W (ISO D, poor); a loaded Class 8
  dual-tire station 10× those. A conventional damper turns all of it into
  heat.
- A spring stores and returns energy; it does not supply any. The share a
  harvester can take is a share of the budget above, never more.

## What AKS can say today, tagged *modeled* (give the conditions every time)

| Statement | Conditions | Where |
|---|---|---|
| "On an average highway at 60 mph the Gate takes about a tenth of a passenger-car corner's road energy — roughly 10–15 W per corner — with ride and tire grip essentially unchanged." | ISO C, stock damper, r = 300, J r² ≈ 3 kg, η 0.85 | exp 001/002 |
| "Taking more requires softening the suspension's damping; a quarter-damper setting reaches 20–35 W per car corner at the cost of 25–50 % more dynamic tire-load variation." | ISO C, 60 mph, damper ×0.25 | exp 001/002, F5 |
| "For a passenger car the device is roughly break-even against its own mass on average roads and pays on rough roads." | 10–12 kg per corner (open estimate), ISO C → D | exp 002, F5 |
| "A loaded tractor-trailer wheel station yields about 150 W on average highways and 600 W on rough roads with stock damping — around 1.5 kW and 5.5 kW per vehicle; up to about 13 kW per vehicle if the damping is retuned toward harvest." | ISO C / D, 60 mph, 9 dual stations | exp 003, F7 |
| "Tactical vehicles on rough ground: 100–400 W per corner (MRAP), 30–120 W (HMMWV), with the HMMWV reaching 80–280 W if its damping is cut." | ISO C–D, 60 mph | exp 002/003 |
| "The clutch rectifier is mechanically 85–90 % efficient in the useful band." | r 200–800 rad/m | exp 004 |
| "The design must keep the reflected rotor inertia J·r² below about 10 kg per car corner; the generator load optimum is a reflected damping of 300–900 N·s/m." | mid-size car | exp 001/004/006, frontier |

## What AKS cannot say (and the replacement)

| Do not say | Why | Say instead |
|---|---|---|
| "The spring is a several-times-larger energy reservoir than the damper" | reactive power; mean zero (F1) | "The damper burns the road's energy budget as heat; we route part of it to a generator." |
| "~350 W per pickup / ~5 kW per semi on average roads" | ISO-C model: 60–140 W per pickup, 1.4 kW per loaded semi (F7) | the exp 002/003 ranges with road class |
| "Harvesting improves the ride with no trade-off" | every configuration that harvests more than ~10 % softens the corner and raises tire-load variation | "At stock damping ride and grip change by a few percent; higher harvest trades grip for seat comfort." |
| "89 % of the energy is captured by the bias spring" | static partition of stored energy, not a harvest fraction (C18) | "The soft stage carries most of the stack's elastic deflection; the fraction harvested is measured as φ." |
| "297 hp transmission capacity", "109 J per inch of stroke" | non-physical (C19, C20) | drop |
| "~14 W measured on the prototype", "287 W in the live simulation" | no record; file unavailable (F4, C13) | "First bench results: [date], [conditions]" when they exist |
| "The only patented art that charges a vehicle in motion" | Schenavar 1977, Hyundai 2016, Levant 2014, Zuo lineage (04_prior_art) | "A patented arrangement built around the spring rather than the damper" |
| any service-life figure for the clutches | no literature basis; ~170 engagements per km per set (F6) | "Endurance is the first bench test." |

## What the first bench run will add (05_bench_protocol)

Measured c_eq = c_gen·r², J·r², full-wave confirmation, open-circuit
friction loop, and (T6) clutch engagements to 10⁶. After that, and only
after that, the column "measured" in the ledger gets its first AKS row.
