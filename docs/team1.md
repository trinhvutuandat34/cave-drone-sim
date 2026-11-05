# Team 1 rescue agent

The autonomous implementation is `agents/team1.py`, adapted from this project's
[`viewer-upgrade` branch](https://github.com/trinhvutuandat34/cave-drone-sim/tree/viewer-upgrade).
It does not load a recorded route, map geometry, artifact truth, or the reference planner.
The recorded-route PID exercise remains separate in `agents/team1_pid.py`.

## Run

From the project directory on this Mac:

```bash
runs/env/bin/python -m cavesim.run --agent agents.team1 --map rescue_easy --drones 1 --lidar lite --wait
```

Evaluate reproducibly without the browser:

```bash
runs/env/bin/python -m agents.eval_rescue --seeds 0 1 2
```

The evaluator uses the standard 1,200-second rescue rules, default sensor noise,
odometry and aerodynamic disturbances. It saves timestamped scores, trails and
10-second progress snapshots in `runs/`. Each result includes hashes of the agent
and shared flight controller. A failed mission produces a nonzero exit status;
an interrupted evaluation is marked `finished: false`.

The optional location-error experiment is:

```bash
runs/env/bin/python -m agents.eval_rescue --seeds 0 1 2 --target-error 20
```

## Approach

1. Follow the public entrance route using outdoor GPS and downward range for height.
2. Integrate LiDAR and downward-range measurements into a 0.5 m log-odds occupancy grid.
3. Plan through observed free cells with `MCP_Geometric`, preferring clearance from rock.
   Choose unexplored tunnel frontiers using travel cost and distance to the supplied
   survivor location. Distinguish scan gaps from an unexplored face, and remember
   regions where the drone has stopped progressing.
4. Follow the planned path with velocity commands, local steering, LiDAR braking and
   ceiling/floor limits. A direction outside measured LiDAR coverage is not assumed free.
5. Use the survivor detector to refine the goal. A sighting alone is insufficient:
   approach within 2 m before returning, leaving margin for the referee's 3 m rule.
6. Return using the map or the drone's own breadcrumbs. Match scans to earlier
   keyframes on return, then use reacquired GPS for the landing approach.

## Verification status

Seed 0 completed an autonomous rescue and landing in **639.6 s**, rescuing at 363.5 s
and landing 0.93 m horizontally from base with 43.4% battery remaining. The saved
[`result`](../runs/team1_rescue_easy_seed0_20261105_211109.json) has matching source hashes,
`finished: true`, no crash, no course departure and no exhausted battery.
Other seeds are still being evaluated; this single success does not establish reliability.
The agent used for that recording is preserved in `runs/team1_first_success.py`.
Seed 1 returned safely without a rescue at 844.7 s. Its map exposed a recovery bug:
horizontal exclusions also hid observed passages above a failed search. The current
agent uses 3D distance for those exclusions; repeat mission tests are in progress.
Passing unit tests does not establish rescue or landing success. A qualifying result must have `finished: true`,
`success: true`, `returned: [0]`, a survivor rescue time, no crash, no course departure,
no exhausted battery, and a lap time below 1,200 s.

To view a saved trajectory, start a local HTTP server from the project directory:

```bash
runs/env/bin/python -m http.server 8000 --bind 127.0.0.1
```

Open `/viewer/?record=/runs/team1_rescue_easy_seed0_20261105_211109.json` on that server.
The bottom replay controls scrub the recorded positions. Heading is reconstructed from
movement; full attitude, LiDAR and video were not recorded. At 16×, the replay takes about 40 s.

The pilot recording rescued the survivor at 521.1 s but landed outside the base radius.
An intermediate PID run rescued at 479.7 s, then stalled near the entrance and exhausted
its battery. These are diagnostic results, not completed missions.

Focused checks:

```bash
runs/env/bin/python -m pytest -q tests/test_team1_rescue.py tests/test_team1_pid.py tests/test_session.py
node tests/test_keyboard.mjs
```

The Mac compatibility changes only reduce PyBullet mesh/ray batch sizes to fit the
installed build. Mission geometry, scoring, battery, crash thresholds and sensor noise
have not been relaxed for the agent.
