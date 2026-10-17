# 06 — Numbers ledger

Every number any AKS document may quote, appended by the experiment that
produced it. Columns: value · units · range (5–95% over seeds, or stated) ·
road / speed / vehicle · tag (`measured` / `modeled` / `target` /
`literature`) · source or experiment ID · date. Rows are never edited,
only superseded by a later row.

| Value | Units | Range | Conditions | Tag | Source | Date |
|---|---|---|---|---|---|---|
| 1.905 / 15.902 | lbf/in | — | bias / main bench springs EB-7234 / EB-7233 | measured | Ebsco Rev 4 via Diligence Response | 2026-07-30 |
| 8.35 | — | — | main/bias rate ratio, bench articles | measured | same | 2026-07-30 |
| 122 | W per corner | exact | road supply ¼k_tW_v: k_t 180 kN/m, ISO C, 60 mph | modeled | 01_physics §7; `validate.analytic` | 2026-10-17 |
| 30 / 122 / 488 / 1952 | W per vehicle (4 corners) | exact | ISO A/B/C/D, 60 mph, k_t 180 kN/m | modeled | same (reproduces Zuo & Zhang 100–400 W band) | 2026-10-17 |
| 169 | W per corner | exact | f150 corner k_t 250 kN/m, ISO C, 60 mph | modeled | same | 2026-10-17 |
| 1220 | W per dual wheel station | exact | class8 k_t 1.8 MN/m, ISO C, 60 mph | modeled | same | 2026-10-17 |
| 1.0 | — | — | road supply sensitivity to m_s, m_u, k_m, c_s, Gate (exact invariance) | modeled | test_analytic_limits | 2026-10-17 |
| 660 | kg | — | reflected inertance J r² at r 1484 rad/m, J 3e-4 kg m² | modeled | 01_physics §4.2 | 2026-10-17 |
| 3.3 | W per corner | single seed, 20 s | mid-size car, ISO C, 60 mph, r 1484, J 3e-4, c_gen 2e-3 (smoke run) | modeled | F2 | 2026-10-17 |
| 0.0471 / 0.0942 | m/s peak | — | Li/Zuo 2013 bench race velocity at 1.5 / 3 Hz × 5 mm | literature | 04_prior_art item 1 | 2013 |
| 40.4 / 25.6 | W | — | Li/Zuo 2013 bench, 3 Hz × 5 mm, two loads | literature | same | 2013 |
| 3 / 100–150 / 613 | W per vehicle | — | Audi eROT, new freeway / German average / rough secondary | literature | press release 2016-08-10 | 2016 |
| 30–334 ; 3–25 | W per damper | — | Abdelkareem 2021 SUV off-road ; city, 10–40 km/h | literature | Measurement 179 109381 | 2021 |
| 0 | measured AKS power figures in the record | — | — | — | F4 | 2026-10-17 |

*(Experiment rows appended below by `run.py` summaries — see each
experiment's `results/RESULTS.md` for the full tables.)*
| 13 / 28 / 56 / 304 / 289 | W per corner (station) | exact (linear surrogate) | ISO C, 60 mph, ride ≤ passive & DTL ≤ 1.1×passive: midsize / F-150 / HMMWV / Class 8 loaded dual / MRAP | modeled | reports/linear_frontier.md | 2026-10-17 |
| −16 / −12 / +10 / +233 / +218 | W net per corner | exact (surrogate) | same, minus friction and gate_mass penalty (open estimate) | modeled | same | 2026-10-17 |
| 0.11 / 0.17 / 0.21 / 0.25 / 0.39 | φ (constrained ceiling) | exact (surrogate) | same vehicles | modeled | same | 2026-10-17 |
| 300–500 | N·s/m | — | optimal reflected generator damping c_gen·r², passenger car, any bias ratio 0.05–1 | modeled | same | 2026-10-17 |
| 9.7 (9.5–9.9) | W per corner | 3 seeds | nonlinear sim, midsize, ISO C 60 mph, r 300, J 3e-5, c_gen 0.01, stock damper | modeled | exp 001 | 2026-10-17 |
| 9.7 / 14.8 / 29.3 | W per corner | seed range ±3 % | ISO C 60 mph, stock damper, best load: midsize / F-150 / HMMWV | modeled | exp 002 | 2026-10-17 |
| 38.7 / 59 / 117 | W per corner | ±3 % | ISO D 60 mph, stock damper | modeled | exp 002 | 2026-10-17 |
| 19.5 / 34.8 / 79.5 | W per corner | ±3 % | ISO C 60 mph, OEM damper ×0.25 (DTL +26–53 %) | modeled | exp 002 | 2026-10-17 |
| 0.08 / 0.09 / 0.11 | φ | — | stock damper, any class A–D, 30 or 60 mph: midsize / F-150 / HMMWV | modeled | exp 002 | 2026-10-17 |
| −21 / −23 / −18 | W net per corner | — | ISO C 60 mph stock damper incl. 10/12/15 kg mass penalty | modeled | exp 002 | 2026-10-17 |
