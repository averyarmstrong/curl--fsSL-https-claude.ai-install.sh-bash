# Experiment 009 — results (all `modeled` on `asserted` toy parameters)

## 1. Spin-up, baseline toy (lead 25 mm/rev, 15 N hand, 1 m/s hand limit)

| push | W_hand [J] | ΔKE_rotor [J] | losses [J] | ω_end [rad/s] | v_peak [m/s] | r·v_peak [rad/s] |
|---|---|---|---|---|---|---|
| 1 | 0.604 | 0.350 | 0.254 | 74.8 | 0.30 | 75.3 |
| 2 | 0.599 | 0.283 | 0.315 | 100.7 | 0.40 | 101.4 |
| 3 | 0.542 | 0.227 | 0.315 | 117.3 | 0.47 | 118.1 |
| 4 | 0.507 | 0.189 | 0.318 | 129.5 | 0.52 | 130.5 |
| 5 | 0.482 | 0.161 | 0.321 | 139.2 | 0.56 | 140.2 |
| 6 | 0.464 | 0.140 | 0.324 | 147.0 | 0.59 | 148.1 |
| 7 | 0.450 | 0.122 | 0.328 | 153.5 | 0.62 | 154.7 |
| 8 | 0.439 | 0.108 | 0.331 | 159.0 | 0.64 | 160.3 |
| 9 | 0.431 | 0.096 | 0.335 | 163.8 | 0.66 | 165.1 |
| 10 | 0.424 | 0.086 | 0.338 | 167.9 | 0.67 | 169.3 |
| 11 | 0.418 | 0.077 | 0.341 | 171.5 | 0.69 | 173.0 |
| 12 | 0.413 | 0.069 | 0.344 | 174.7 | 0.70 | 176.2 |
| 13 | 0.408 | 0.062 | 0.346 | 177.5 | 0.71 | 179.1 |
| 14 | 0.405 | 0.056 | 0.348 | 180.0 | 0.72 | 181.6 |
| 15 | 0.402 | 0.051 | 0.351 | 182.3 | 0.73 | 183.9 |
| 16 | 0.399 | 0.046 | 0.353 | 184.3 | 0.74 | 185.9 |
| 17 | 0.396 | 0.042 | 0.354 | 186.1 | 0.75 | 187.8 |
| 18 | 0.394 | 0.038 | 0.356 | 187.8 | 0.75 | 189.4 |
| 19 | 0.393 | 0.035 | 0.358 | 189.3 | 0.76 | 190.9 |
| 20 | 0.391 | 0.032 | 0.359 | 190.6 | 0.77 | 192.3 |


Ledger over 12 s: hand 8.96 J = rotor KE 2.27 + screw 0.85 + bearing 0.62 + air 0.52 + bottom/top stop 4.70 + pawl 0.000; closure 1.6e-08.

ω never exceeds r·v_peak of the same push (the race ceiling); the hand's velocity limit, not its force, sets the top speed.

## 2. Lead (helix pitch) sweep

| lead [mm/rev] | r [rad/m] | J·r² [kg] | ω after 20 pushes [rad/s] | rpm | ceiling r·v_hand,max | KE [J] | stop-loss / hand work |
|---|---|---|---|---|---|---|---|
| 12.5 | 503 | 31.58 | 241 | 2304 | 503 | 3.64 | 0.38 |
| 25.0 | 251 | 7.90 | 191 | 1820 | 251 | 2.27 | 0.52 |
| 50.0 | 126 | 1.97 | 148 | 1418 | 126 | 1.38 | 0.68 |
| 100.0 | 63 | 0.49 | 116 | 1108 | 63 | 0.84 | 0.80 |


Finer lead = larger r = higher ceiling and larger reflected mass J·r²; the hand then pushes a heavier 'plunger'.

## 3. One pawl vs two opposed pawls (the Gate's full-wave rectifier on the toy)

| pawls | hand work [J] | rotor KE [J] | stop losses [J] | screw+bearing+air [J] | ω after 20 pushes | closure |
|---|---|---|---|---|---|---|
| one (half-wave) | 8.96 | 2.27 | 4.70 | 1.99 | 191 | 1.6e-08 |
| two (full-wave) | 8.13 | 4.21 | 0.15 | 3.77 | 259 | 2.1e-08 |


The second pawl harvests the return spring's stroke that the one-pawl toy wastes against the top stop and the hand. Hand work is not higher; capture is. Nothing exceeds the hand's work.

## 4. Put a generator on the top (steady state, pushes 11–20)

| c_load [N·m·s] | hand power [W] | load power [W] | load / hand | ω steady [rad/s] |
|---|---|---|---|---|
| 0e+00 | 0.67 | 0.00 | 0.00 | 182 |
| 2e-05 | 0.84 | 0.31 | 0.37 | 121 |
| 5e-05 | 0.96 | 0.44 | 0.46 | 88 |
| 1e-04 | 1.06 | 0.54 | 0.51 | 64 |
| 2e-04 | 1.15 | 0.63 | 0.54 | 43 |
| 5e-04 | 0.92 | 0.58 | 0.63 | 16 |


The loaded top settles where load + losses per push equal hand work per push. Output is bounded by hand power; heavier load, slower top.

## 5. Hand stops

ω at 0 / 2 / 5 / 10 s after the last push: 168 / 158 / 146 / 127 rad/s; hand work after the stop 0.0e+00 J. The top is a store, not a source.

## 6. Stronger vs faster hand

| hand F0 [N] | hand v_max [m/s] | ω after 20 [rad/s] | W_hand per push [J] | v_peak [m/s] |
|---|---|---|---|---|
| 15 | 1.0 | 191 | 0.391 | 0.77 |
| 30 | 1.0 | 213 | 0.414 | 0.85 |
| 15 | 2.0 | 236 | 0.512 | 0.95 |
| 30 | 2.0 | 304 | 0.704 | 1.23 |


Doubling the hand's speed limit does more for the top than doubling its force: the ceiling is kinematic.
