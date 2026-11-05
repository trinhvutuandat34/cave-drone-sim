# Team 1 rescue agent

The autonomous implementation is `agents/team1.py`, adapted from the owner's earlier
`viewer-upgrade` branch (commit `51104a8`).
It does not load a recorded route, map geometry, artifact truth, or the reference planner.
The recorded-route PID exercise remains separate in `agents/team1_pid.py`.

## Run

From the project directory on this Mac:

```bash
runs/env/bin/python -m cavesim.run --agent agents.team1 --map rescue_easy --drones 1 --lidar lite --wait
```

Evaluate reproducibly without the browser:

```bash
runs/env/bin/python -m agents.eval_rescue --seeds 0 1
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
   regions where the drone has stopped progressing. Exclusions use 3D distance so
   a failed search does not hide a passage on another level.
4. Follow the planned path with velocity commands, local steering, LiDAR braking and
   ceiling/floor limits. A direction outside measured LiDAR coverage is not assumed free.
5. Use the survivor detector to refine the goal. A sighting alone is insufficient:
   approach within 2 m before returning, leaving margin for the referee's 3 m rule.
   Near an inaccurate hint, visit nearby ground outside the camera's recorded coverage.
6. Return using the map or the drone's own breadcrumbs. Match scans to earlier
   keyframes on return, then use reacquired GPS for the landing approach.

## Verification status

The current agent completed both tested seeds with default noise and disturbances,
one drone, LiDAR lite, and zero added target error:

| Seed | Rescue time | Mission time | Landing distance from base |
| --- | ---: | ---: | ---: |
| 0 | 363.3 s | 640.6 s | 2.73 m |
| 1 | 451.2 s | 720.6 s | 0.92 m |

Both results have `finished: true`, `success: true`, `returned: [0]`, matching hashes
of the current agent and controller, and no crash, course departure or exhausted battery.
Minor contacts were recorded: one at up to 0.39 m/s on seed 0, two at up to 0.92 m/s
on seed 1. These two successes do not establish performance on other seeds or the
optional 20 m target-error challenge.

The local result files are `runs/team1_rescue_easy_seed0_20261105_223227.json` and
`runs/team1_rescue_easy_seed1_20261105_220956.json`. Generated recordings and the local
Python environment are ignored by Git; run the evaluator to create your own results.

To view a saved trajectory, start a local HTTP server from the project directory:

```bash
runs/env/bin/python -m http.server 8000 --bind 127.0.0.1
```

Open `/viewer/?record=/runs/<your-result-file>.json` on that server.
The bottom replay controls scrub the recorded positions. Heading is reconstructed from
movement; full attitude, LiDAR and video were not recorded. At 16×, the replay takes about 40 s.

The original trajectory replay above shows an earlier successful agent version at
639.6 s. Its source is preserved locally in `runs/team1_first_success.py`.

The latest manual recording, `runs/manual_20261105_221651.jsonl`, completed the mission
in 369.5 s, rescued at 195.4 s, had no collisions and landed 2.09 m from base.
Its full viewer history and score are saved locally in
`runs/manual_20261105_221651_mission.json`.
The separate recorded-route PID exercise has not been validated using that new recording.

Focused checks:

```bash
runs/env/bin/python -m pytest -q tests/test_team1_rescue.py tests/test_team1_pid.py tests/test_session.py
node tests/test_keyboard.mjs
node tests/test_recording.mjs
```

The Mac compatibility changes only reduce PyBullet mesh/ray batch sizes to fit the
installed build. Mission geometry, scoring, battery, crash thresholds and sensor noise
have not been relaxed for the agent.
