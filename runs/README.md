# Run archive

Portable evidence from the 2026-11-05 development session. See the [autonomous test report](../AUTONOMOUS_TEST_RESULTS.md) for the verified final results and interpretation.

This archive contains **79 data files (12.77 MiB)**, plus this index. Mission times are simulated seconds.

## Start with the final autonomous tests

- Seed 0: [result](team1_rescue_easy_seed0_20261105_223227.json) and [progress](team1_rescue_easy_seed0_20261105_223227_progress.jsonl).
- Seed 1: [result](team1_rescue_easy_seed1_20261105_220956.json) and [progress](team1_rescue_easy_seed1_20261105_220956_progress.jsonl).

Only those two completed tests belong to the final tested source version. Earlier results, PID experiments and manual flights are kept as separate evidence.

## Result-file index

- **Final autonomous pass:** finished successfully with the current recorded agent/controller hashes.
- **Earlier-version pass / completed failure:** a completed test of an earlier version.
- **Interrupted:** `finished: false`; neither a completed pass nor a completed failure.
- **Legacy:** no explicit `finished` field. Any terminal condition shown is taken directly from score flags; otherwise completion is unknown.
- **Manual pass:** flown with keyboard control; excluded from the autonomous pass count.

| Result file | Seed | Status | Rescue (s) | End (s) | Lap (s) | Progress |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| [manual_20261105_221651_mission.json](manual_20261105_221651_mission.json) | 0 | Manual pass | 195.4 | 369.5 | 369.5 | — |
| [team1_pid_rescue_easy_seed0.json](team1_pid_rescue_easy_seed0.json) | 0 | Legacy: battery exhausted | 479.7 | 1144.1 | — | [log](team1_pid_rescue_easy_seed0_progress.jsonl) |
| [team1_pid_rescue_easy_seed0_20261105_191942.json](team1_pid_rescue_easy_seed0_20261105_191942.json) | 0 | Legacy: completion not recorded | — | 85.7 | — | [log](team1_pid_rescue_easy_seed0_20261105_191942_progress.jsonl) |
| [team1_pid_seed0.json](team1_pid_seed0.json) | 0 | Legacy: completion not recorded | — | 674.6 | — | — |
| [team1_pid_seed0_retry.json](team1_pid_seed0_retry.json) | 0 | Legacy: completion not recorded | — | 904.1 | — | — |
| [team1_rescue_easy_seed0.json](team1_rescue_easy_seed0.json) | 0 | Legacy: crash | — | 197.7 | — | [log](team1_rescue_easy_seed0_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_191518.json](team1_rescue_easy_seed0_20261105_191518.json) | 0 | Legacy: course departure | — | 490.0 | — | [log](team1_rescue_easy_seed0_20261105_191518_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_192300.json](team1_rescue_easy_seed0_20261105_192300.json) | 0 | Legacy: completion not recorded | — | 352.8 | — | [log](team1_rescue_easy_seed0_20261105_192300_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_192546.json](team1_rescue_easy_seed0_20261105_192546.json) | 0 | Legacy: completion not recorded | — | 378.4 | — | [log](team1_rescue_easy_seed0_20261105_192546_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_193046.json](team1_rescue_easy_seed0_20261105_193046.json) | 0 | Legacy: completion not recorded | — | 339.9 | — | [log](team1_rescue_easy_seed0_20261105_193046_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_194218.json](team1_rescue_easy_seed0_20261105_194218.json) | 0 | Interrupted; not a completed test | — | 235.7 | — | [log](team1_rescue_easy_seed0_20261105_194218_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_194505.json](team1_rescue_easy_seed0_20261105_194505.json) | 0 | Completed failure: crash | — | 128.7 | — | [log](team1_rescue_easy_seed0_20261105_194505_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_194847.json](team1_rescue_easy_seed0_20261105_194847.json) | 0 | Interrupted; not a completed test | — | 408.6 | — | [log](team1_rescue_easy_seed0_20261105_194847_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_195232.json](team1_rescue_easy_seed0_20261105_195232.json) | 0 | Interrupted; not a completed test | — | 443.1 | — | [log](team1_rescue_easy_seed0_20261105_195232_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_195637.json](team1_rescue_easy_seed0_20261105_195637.json) | 0 | Interrupted; not a completed test | — | 337.0 | — | [log](team1_rescue_easy_seed0_20261105_195637_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_200537.json](team1_rescue_easy_seed0_20261105_200537.json) | 0 | Interrupted; not a completed test | — | 664.4 | — | [log](team1_rescue_easy_seed0_20261105_200537_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_202132.json](team1_rescue_easy_seed0_20261105_202132.json) | 0 | Completed failure: course departure | — | 436.9 | — | [log](team1_rescue_easy_seed0_20261105_202132_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_203939.json](team1_rescue_easy_seed0_20261105_203939.json) | 0 | Interrupted; not a completed test | — | 327.0 | — | [log](team1_rescue_easy_seed0_20261105_203939_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_204350.json](team1_rescue_easy_seed0_20261105_204350.json) | 0 | Interrupted; not a completed test | — | 501.3 | — | [log](team1_rescue_easy_seed0_20261105_204350_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_205203.json](team1_rescue_easy_seed0_20261105_205203.json) | 0 | Interrupted; not a completed test | 463.5 | 793.8 | — | [log](team1_rescue_easy_seed0_20261105_205203_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_211109.json](team1_rescue_easy_seed0_20261105_211109.json) | 0 | Earlier-version pass | 363.5 | 639.6 | 639.6 | [log](team1_rescue_easy_seed0_20261105_211109_progress.jsonl) |
| [team1_rescue_easy_seed0_20261105_223227.json](team1_rescue_easy_seed0_20261105_223227.json) | 0 | Final autonomous pass | 363.3 | 640.6 | 640.6 | [log](team1_rescue_easy_seed0_20261105_223227_progress.jsonl) |
| [team1_rescue_easy_seed1.json](team1_rescue_easy_seed1.json) | 1 | Legacy: crash | — | 56.2 | — | [log](team1_rescue_easy_seed1_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_192710.json](team1_rescue_easy_seed1_20261105_192710.json) | 1 | Legacy: completion not recorded | — | 790.2 | — | [log](team1_rescue_easy_seed1_20261105_192710_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_194506.json](team1_rescue_easy_seed1_20261105_194506.json) | 1 | Interrupted; not a completed test | — | 246.8 | — | [log](team1_rescue_easy_seed1_20261105_194506_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_200000.json](team1_rescue_easy_seed1_20261105_200000.json) | 1 | Interrupted; not a completed test | — | 294.5 | — | [log](team1_rescue_easy_seed1_20261105_200000_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_205203.json](team1_rescue_easy_seed1_20261105_205203.json) | 1 | Interrupted; not a completed test | — | 370.7 | — | [log](team1_rescue_easy_seed1_20261105_205203_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_210713.json](team1_rescue_easy_seed1_20261105_210713.json) | 1 | Interrupted; not a completed test | — | 229.8 | — | [log](team1_rescue_easy_seed1_20261105_210713_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_211109.json](team1_rescue_easy_seed1_20261105_211109.json) | 1 | Completed failure: returned without rescue | — | 844.7 | — | [log](team1_rescue_easy_seed1_20261105_211109_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_215030.json](team1_rescue_easy_seed1_20261105_215030.json) | 1 | Interrupted; not a completed test | 482.6 | 564.4 | — | [log](team1_rescue_easy_seed1_20261105_215030_progress.jsonl) |
| [team1_rescue_easy_seed1_20261105_220956.json](team1_rescue_easy_seed1_20261105_220956.json) | 1 | Final autonomous pass | 451.2 | 720.6 | 720.6 | [log](team1_rescue_easy_seed1_20261105_220956_progress.jsonl) |
| [team1_rescue_easy_seed2_20261105_193347.json](team1_rescue_easy_seed2_20261105_193347.json) | 2 | Legacy: completion not recorded | — | 435.4 | — | [log](team1_rescue_easy_seed2_20261105_193347_progress.jsonl) |
| [team1_rescue_easy_seed2_20261105_210054.json](team1_rescue_easy_seed2_20261105_210054.json) | 2 | Interrupted; not a completed test | — | 458.0 | — | [log](team1_rescue_easy_seed2_20261105_210054_progress.jsonl) |
| [team1_rescue_easy_seed2_20261105_211109.json](team1_rescue_easy_seed2_20261105_211109.json) | 2 | Interrupted; not a completed test | — | 419.1 | — | [log](team1_rescue_easy_seed2_20261105_211109_progress.jsonl) |
| [team1_rescue_easy_seed2_20261105_212448.json](team1_rescue_easy_seed2_20261105_212448.json) | 2 | Interrupted; not a completed test | — | 283.2 | — | [log](team1_rescue_easy_seed2_20261105_212448_progress.jsonl) |
| [team1_rescue_seed0.json](team1_rescue_seed0.json) | 0 | Legacy: completion not recorded | 323.3 | 493.8 | — | — |

## Other archived files

| File | Contents | Size (KiB) |
| --- | --- | ---: |
| [manual_20261105_181820.jsonl](manual_20261105_181820.jsonl) | Manual observations and keyboard inputs | 0.0 |
| [manual_20261105_181850.jsonl](manual_20261105_181850.jsonl) | Manual observations and keyboard inputs | 6.9 |
| [manual_20261105_183239.jsonl](manual_20261105_183239.jsonl) | Manual observations and keyboard inputs | 839.6 |
| [manual_20261105_221651.jsonl](manual_20261105_221651.jsonl) | Manual observations and keyboard inputs | 422.8 |
| [map_diagnostic.npz](map_diagnostic.npz) | Occupancy-map diagnostic | 29.6 |
| [route.json](route.json) | Waypoint route | 24.6 |
| [team1_3d_before_search.py](team1_3d_before_search.py) | Historical agent source | 47.4 |
| [team1_before_frontier.py](team1_before_frontier.py) | Historical agent source | 46.8 |
| [team1_first_success.py](team1_first_success.py) | Historical agent source | 47.4 |
| [team1_pid_log.csv](team1_pid_log.csv) | PID telemetry | 46.4 |
| [team1_pid_rescue_easy_seed0_20261105_191942_progress.jsonl](team1_pid_rescue_easy_seed0_20261105_191942_progress.jsonl) | Progress snapshots | 8.6 |
| [team1_pid_rescue_easy_seed0_progress.jsonl](team1_pid_rescue_easy_seed0_progress.jsonl) | Progress snapshots | 125.6 |
| [team1_rescue_easy_seed0_20261105_191518_progress.jsonl](team1_rescue_easy_seed0_20261105_191518_progress.jsonl) | Progress snapshots | 36.9 |
| [team1_rescue_easy_seed0_20261105_192300_progress.jsonl](team1_rescue_easy_seed0_20261105_192300_progress.jsonl) | Progress snapshots | 27.5 |
| [team1_rescue_easy_seed0_20261105_192546_progress.jsonl](team1_rescue_easy_seed0_20261105_192546_progress.jsonl) | Progress snapshots | 28.3 |
| [team1_rescue_easy_seed0_20261105_193046_progress.jsonl](team1_rescue_easy_seed0_20261105_193046_progress.jsonl) | Progress snapshots | 33.8 |
| [team1_rescue_easy_seed0_20261105_194218_progress.jsonl](team1_rescue_easy_seed0_20261105_194218_progress.jsonl) | Progress snapshots | 25.6 |
| [team1_rescue_easy_seed0_20261105_194505_progress.jsonl](team1_rescue_easy_seed0_20261105_194505_progress.jsonl) | Progress snapshots | 14.1 |
| [team1_rescue_easy_seed0_20261105_194847_progress.jsonl](team1_rescue_easy_seed0_20261105_194847_progress.jsonl) | Progress snapshots | 35.2 |
| [team1_rescue_easy_seed0_20261105_195232_progress.jsonl](team1_rescue_easy_seed0_20261105_195232_progress.jsonl) | Progress snapshots | 40.7 |
| [team1_rescue_easy_seed0_20261105_195637_progress.jsonl](team1_rescue_easy_seed0_20261105_195637_progress.jsonl) | Progress snapshots | 42.2 |
| [team1_rescue_easy_seed0_20261105_200537_progress.jsonl](team1_rescue_easy_seed0_20261105_200537_progress.jsonl) | Progress snapshots | 151.5 |
| [team1_rescue_easy_seed0_20261105_202132_progress.jsonl](team1_rescue_easy_seed0_20261105_202132_progress.jsonl) | Progress snapshots | 52.8 |
| [team1_rescue_easy_seed0_20261105_203939_progress.jsonl](team1_rescue_easy_seed0_20261105_203939_progress.jsonl) | Progress snapshots | 28.7 |
| [team1_rescue_easy_seed0_20261105_204350_progress.jsonl](team1_rescue_easy_seed0_20261105_204350_progress.jsonl) | Progress snapshots | 48.7 |
| [team1_rescue_easy_seed0_20261105_205203_progress.jsonl](team1_rescue_easy_seed0_20261105_205203_progress.jsonl) | Progress snapshots | 437.3 |
| [team1_rescue_easy_seed0_20261105_211109_progress.jsonl](team1_rescue_easy_seed0_20261105_211109_progress.jsonl) | Progress snapshots | 278.4 |
| [team1_rescue_easy_seed0_20261105_223227_progress.jsonl](team1_rescue_easy_seed0_20261105_223227_progress.jsonl) | Progress snapshots | 280.2 |
| [team1_rescue_easy_seed0_progress.jsonl](team1_rescue_easy_seed0_progress.jsonl) | Progress snapshots | 14.1 |
| [team1_rescue_easy_seed1_20261105_192710_progress.jsonl](team1_rescue_easy_seed1_20261105_192710_progress.jsonl) | Progress snapshots | 244.3 |
| [team1_rescue_easy_seed1_20261105_194506_progress.jsonl](team1_rescue_easy_seed1_20261105_194506_progress.jsonl) | Progress snapshots | 28.4 |
| [team1_rescue_easy_seed1_20261105_200000_progress.jsonl](team1_rescue_easy_seed1_20261105_200000_progress.jsonl) | Progress snapshots | 35.6 |
| [team1_rescue_easy_seed1_20261105_205203_progress.jsonl](team1_rescue_easy_seed1_20261105_205203_progress.jsonl) | Progress snapshots | 43.1 |
| [team1_rescue_easy_seed1_20261105_210713_progress.jsonl](team1_rescue_easy_seed1_20261105_210713_progress.jsonl) | Progress snapshots | 26.1 |
| [team1_rescue_easy_seed1_20261105_211109_progress.jsonl](team1_rescue_easy_seed1_20261105_211109_progress.jsonl) | Progress snapshots | 269.0 |
| [team1_rescue_easy_seed1_20261105_215030_progress.jsonl](team1_rescue_easy_seed1_20261105_215030_progress.jsonl) | Progress snapshots | 164.6 |
| [team1_rescue_easy_seed1_20261105_220956_progress.jsonl](team1_rescue_easy_seed1_20261105_220956_progress.jsonl) | Progress snapshots | 267.7 |
| [team1_rescue_easy_seed1_progress.jsonl](team1_rescue_easy_seed1_progress.jsonl) | Progress snapshots | 3.8 |
| [team1_rescue_easy_seed2_20261105_193347_progress.jsonl](team1_rescue_easy_seed2_20261105_193347_progress.jsonl) | Progress snapshots | 45.2 |
| [team1_rescue_easy_seed2_20261105_210054_progress.jsonl](team1_rescue_easy_seed2_20261105_210054_progress.jsonl) | Progress snapshots | 53.7 |
| [team1_rescue_easy_seed2_20261105_211109_progress.jsonl](team1_rescue_easy_seed2_20261105_211109_progress.jsonl) | Progress snapshots | 49.1 |
| [team1_rescue_easy_seed2_20261105_212448_progress.jsonl](team1_rescue_easy_seed2_20261105_212448_progress.jsonl) | Progress snapshots | 32.9 |
| [team1_route.json](team1_route.json) | Waypoint route | 52.5 |

## Formats and replay

- Result JSON stores the score and true/odometry trajectories. Newer results also store completion status, seed, map, target error and flight-source hashes.
- Progress JSONL stores state/command snapshots. Some original logs use Python `Infinity` for an unmeasured `roof_gap`; the viewer supports this legacy metadata and new exports use JSON `null`.
- Manual JSONL stores observations, keys, outdoor GPS and whether the survivor was visible.
- `manual_20261105_221651_mission.json` additionally stores the original viewer history, including the available attitude and LiDAR snapshots.
- Archived agent files are historical references. The active agent is [`agents/team1.py`](../agents/team1.py).

Follow the [replay instructions](../AUTONOMOUS_TEST_RESULTS.md#reproduce-and-inspect) to inspect an autonomous trajectory in the browser.

## Kept local

`env/`, `tooling/`, `.pkl` and `.pkl.gz` debugging snapshots are excluded from Git. They are not required to read the scores or replay the autonomous trajectories. No local files have been deleted.
