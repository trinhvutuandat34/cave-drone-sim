import json

import numpy as np
import pytest

from agents.team1_pid import PID, prepare_route


def test_pid_damps_motion_limits_integral_and_trims_the_failed_landing(tmp_path):
    pid = PID(kp=1, ki=1, kd=1, i_limit=0.5)
    assert np.allclose(pid.update(np.ones(3), np.ones(3), 1), 0.5)
    assert np.allclose(pid.update(np.ones(3), np.zeros(3), 1), 1.5)
    with pytest.raises(ValueError):
        pid.update(np.ones(3), np.zeros(3), 0)
    rows = [{"t": i, "pos": [i, 0, 1], "yaw": 0, "gps": [i, 0, 1] if i in (0, 4, 5) else None,
             "survivor": i == 2} for i in range(6)]
    log = tmp_path / "pilot.jsonl"
    log.write_text("\n".join(json.dumps(r) for r in rows))
    route = prepare_route(log, tmp_path / "route.json")
    assert route["times"][-1] == 4
    assert route["times"][route["survivor_waypoint"]] == 2
