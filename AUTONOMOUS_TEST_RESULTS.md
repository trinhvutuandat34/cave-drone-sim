# Autonomous rescue test progress and results

Report date: **2026-11-05, Asia/Seoul**. All mission times below are **simulated seconds**.

The final flight code completed **both tested seeds (0 and 1)**: it entered the cave,
rescued the survivor, returned, and landed inside the required base radius. These
results describe the two tested seeds, not reliability across all seeds.

## Final autonomous results

| Seed | Result | Rescue time | Mission time | Landing distance | Battery remaining | Contacts / maximum impact |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 0 | Pass | 363.3 s | 640.6 s | 2.73 m | 43.4% | 1 / 0.39 m/s |
| 1 | Pass | 451.2 s | 720.6 s | 0.92 m | 36.5% | 2 / 0.92 m/s |

Both results have `finished: true`, `success: true`, `returned: [0]`, a recorded
rescue time, and empty `crashed`, `out_of_course`, and `battery_dead` lists. Contacts
were minor; these were not collision-free flights. Landing distances are calculated
from the final stored true positions, rather than drifting odometry positions.
The mean lap time across these two tests is **680.6 s**.

- **Seed 0:** [score and trajectories](runs/team1_rescue_easy_seed0_20261105_223227.json),
  [progress log](runs/team1_rescue_easy_seed0_20261105_223227_progress.jsonl).
- **Seed 1:** [score and trajectories](runs/team1_rescue_easy_seed1_20261105_220956.json),
  [progress log](runs/team1_rescue_easy_seed1_20261105_220956_progress.jsonl).
- [Complete run archive and status index](runs/README.md).

## Configuration and success criteria

| Setting | Value |
| --- | --- |
| Agent / evaluator | [`agents.team1`](agents/team1.py) / [`eval_rescue.py`](agents/eval_rescue.py) |
| Map / drones | `rescue_easy` / 1 |
| LiDAR | `lite` (16 channels, 256 azimuth steps) |
| Odometry, IMU and aerodynamic disturbances | Simulator defaults |
| Added target-coordinate error | 0 m |
| Mission limit | 1,200 simulated seconds |
| Rescue | Within 3 m of the survivor with clear visibility |
| Return | Land within 3 m horizontally of base |
| Required outcome | Rescue and return, with no crash, course departure or battery exhaustion |

The agent maps observed LiDAR free space at 0.5 m resolution, plans with
`MCP_Geometric`, corrects drift against earlier scans, and uses outdoor GPS again
for landing. It does not load archived routes or map truth as flight inputs.
See the [agent guide](docs/team1.md) and [course rules](docs/student_guide.md).

## Progress during development

These records cover different code versions. They are not pooled with the final
two tests when reporting the final result.

| Stage / saved record | Observed result |
| --- | --- |
| [Recorded-route PID experiment](runs/team1_pid_rescue_easy_seed0.json) | Rescued at 479.7 s; exhausted the battery at 1,144.1 s without returning. |
| [Early live-mapping collision](runs/team1_rescue_easy_seed0_20261105_194505.json) | Completed failure: crashed at 128.7 s. |
| [Course-boundary experiment](runs/team1_rescue_easy_seed0_20261105_202132.json) | Completed failure: left the course at 436.9 s. |
| [Return-descent investigation](runs/team1_rescue_easy_seed0_20261105_205203.json) | Rescued at 463.5 s; interrupted at 793.8 s after the return stalled. `finished: false`. |
| [First complete autonomous mission, seed 0](runs/team1_rescue_easy_seed0_20261105_211109.json) | Completed success in 639.6 s using an earlier agent version. |
| [Earlier seed 1 attempt](runs/team1_rescue_easy_seed1_20261105_211109.json) | Returned and landed at 844.7 s without rescuing the survivor; mission failed. |
| [3D recovery revision, seed 1](runs/team1_rescue_easy_seed1_20261105_215030.json) | Rescued at 482.6 s; interrupted during return at 564.4 s. Not a completed mission. |
| [Final seed 1](runs/team1_rescue_easy_seed1_20261105_220956.json) | Completed success in 720.6 s. |
| [Final seed 0](runs/team1_rescue_easy_seed0_20261105_223227.json) | Completed success in 640.6 s. |

The changes leading to the final version included:

1. Fitting PyBullet mesh and ray batches to the Mac build's limits, without removing geometry.
2. Handing entrance navigation over to the map at the public entrance.
3. Bounding ceiling-plane extrapolation so distant sloping rock does not invent a low roof.
4. Allowing slow descent when the ground is beyond the downward rangefinder's 12 m reach.
5. Using 3D recovery exclusions so a failed search does not hide a passage above it.
6. Searching nearby ground outside recorded camera coverage when odometry makes the hint insufficient.
7. Using scan matching and reacquired GPS on return and landing.

Interrupted records are retained for diagnosis. They count as neither completed
successes nor completed failures. Some legacy records lack a `finished` field;
the archive index identifies that missing completion metadata explicitly.

## Tested source identity

Both final result files record the following SHA-256 values. They match the
checked-in flight sources and the flight code in commit `b469a98`:

| File | SHA-256 |
| --- | --- |
| `agents/team1.py` | `fa6a474a9b38d3f2044db313b6d9d2bcd4dbaff2b433cef23747f5a67c37d615` |
| `agents/flight_control.py` | `2bccf6e6e5f5172d96be3fb1541b77781c9f10cfa7519ebf3756a16a51f6c364` |

The archive update does not change those flight sources. It adds compatibility for
legacy progress metadata: older Python logs sometimes contain `roof_gap: Infinity`.
The viewer reads that sentinel as missing metadata; new evaluator exports use JSON
`null`. Original archived measurements, scores and trajectories remain unchanged.

## Manual reference flight

This manual flight is a separate reference, not part of the autonomous pass count.

| Mission time | Rescue time | Landing distance | Collisions | Result |
| ---: | ---: | ---: | ---: | --- |
| 369.5 s | 195.4 s | 2.09 m | 0 | Pass |

- [Manual observations and keyboard inputs](runs/manual_20261105_221651.jsonl).
- [Manual score, trajectories and original viewer history](runs/manual_20261105_221651_mission.json).

The new manual recording has not yet been used to validate the separate PID exercise.

## Reproduce and inspect

After following the [environment setup](README.md), activate the environment and run:

```bash
conda activate cave-drone
python -m agents.eval_rescue --seeds 0 1
```

The evaluator writes timestamped scores and progress logs into `runs/` and returns a
nonzero exit status if a mission fails. To check the focused regressions:

```bash
python -m pytest -q tests/test_team1_rescue.py tests/test_team1_pid.py tests/test_session.py
node tests/test_keyboard.mjs
node tests/test_recording.mjs
```

To replay an archived autonomous trajectory:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

Open [seed 0 replay](http://127.0.0.1:8000/viewer/?record=/runs/team1_rescue_easy_seed0_20261105_223227.json&main=map&inset=chase)
or [seed 1 replay](http://127.0.0.1:8000/viewer/?record=/runs/team1_rescue_easy_seed1_20261105_220956.json&main=map&inset=chase).
Press the bottom play button or scrub the timeline. At 16×, these replays take about
40 s and 45 s respectively. Autonomous headings are reconstructed from recorded
positions; full attitude, LiDAR and video were not recorded in these evaluations.

## Archive scope and limitations

The [runs folder](runs/README.md) includes scores, trajectories, progress logs, manual
recordings, routes, CSV output, small diagnostics and historical agent source snapshots.
The local `runs/env/` environment, `runs/tooling/`, and large `.pkl` / `.pkl.gz`
debugging snapshots stay local and can be regenerated when needed.

The final agent has only been fully checked on seeds 0 and 1 with zero added target
error. Seed 2 development records are incomplete or lack completion metadata. The
optional 20 m target-error challenge and broader seed reliability remain unverified.
