from types import SimpleNamespace

import numpy as np

from agents.team1 import Agent
from cavesim.api import Detection
from agents.flight_control import safe_velocity


def test_rescue_sensor_and_planning_contract():
    a = Agent(0, 1, {"base": [0, 0, 1.5], "target": [150, -240, 20],
                     "lidar_channels": 16, "lidar_azimuth_steps": 256, "lidar_max_range": 35, "n_artifacts": 1})
    assert a.inside(a.cell([150, -240, 20]))
    obs = SimpleNamespace(pos=np.zeros(3), roll=0, pitch=0, yaw=0,
                          detections=[Detection("survivor", np.array([5, 0, 0]))])
    a.remember(obs)
    assert not a.all_seen()
    obs.detections = [Detection("survivor", np.array([1.5, 0, 0]))]
    a.remember(obs)
    assert a.all_seen()
    obs.lidar = np.array([[1.0, 0, 0.65]])  # visible at 33 degrees; the airframe blocks steeper rays
    assert a.climb_cap(obs) == 0.0
    y, z = np.meshgrid(np.linspace(-0.3, 0.3, 5), np.linspace(0.3, 0.8, 5))
    obs.lidar = np.c_[np.ones(y.size), y.ravel(), z.ravel()]
    assert a.climb_cap(obs) == 1.5  # a vertical wall must not masquerade as a low ceiling
    x, y = np.meshgrid(np.linspace(1.0, 1.2, 5), np.linspace(-0.1, 0.1, 5))
    obs.lidar = np.c_[x.ravel(), y.ravel(), np.full(x.size, 0.65)]
    assert a.climb_cap(obs) == 0.0
    # Extrapolating a distant sloping patch must not invent a ceiling over the drone.
    x, y = np.meshgrid(np.linspace(4.0, 4.5, 7), np.linspace(-0.3, 0.3, 7))
    obs.lidar = np.c_[x.ravel(), y.ravel(), (0.6 * x + 0.2).ravel()]
    assert a.climb_cap(obs) == 1.5
    obs.range_down = np.inf
    obs.lidar = np.array([[1, 0.5, 0], [1, -0.5, 0]])
    v = safe_velocity(obs, np.array([1.0, 0, -0.1]))
    assert v[0] == 1.0 and v[2] == -0.1
    assert safe_velocity(obs, np.array([0., 0., -1.5]))[2] == -0.5
    obs.lidar_dirs = np.array([[1, 0, 0], [np.cos(np.radians(31)), 0, np.sin(np.radians(31))]])
    obs.lidar_ranges = np.array([5.0, 5.0])
    obs.lidar = obs.lidar_dirs * obs.lidar_ranges[:, None]
    directions = np.array([[1, 0, 0], [np.cos(np.radians(50)), 0, np.sin(np.radians(50))]])
    free = a.free_ahead(obs, directions)
    assert free[0] > 4.0 and free[1] == 0.0

    # A mapped corridor should advance toward its mouth instead of inspecting nearby scan gaps.
    a.origin, a.shape = np.array([0., -3., -1.]), (40, 12, 12)
    a.L = np.zeros(a.shape, dtype=np.int8)
    a.known = np.zeros(a.shape, dtype=bool)
    a.flown = np.zeros(a.shape, dtype=bool)
    a.searched = np.zeros(a.shape, dtype=bool)
    a.known[:25, 3:10, 3:9] = True
    for z in (2, 9):
        a.known[:28, 2:11, z] = True
        a.L[:28, 2:11, z] = 3
    for y in (2, 10):
        a.known[:28, y, 2:10] = True
        a.L[:28, y, 2:10] = 3
    a.lo, a.hi = np.zeros(3, dtype=int), np.array(a.shape) - 1
    a.rescue_target = np.array([20., 0., 1.])
    obs.pos = np.array([1.25, 0.25, 1.25])
    path, goal, _ = a.plan(obs)
    assert path and goal[0] > 10.0
    a.spent_regions = [np.array([12.0, 0.25, -10.0])]
    path, goal, _ = a.plan(obs)
    assert path and goal[0] > 10.0  # another level is still available to explore
    a.spent_regions = []
    hint = a.rescue_target.copy()
    a.rescue_target = np.array([10.0, 0.25, 0.25])  # occupied floor voxel
    path, goal, _ = a.plan(obs)
    assert path and np.linalg.norm(goal - a.rescue_target) < 1.0
    a.searching = True
    a.searched[:23] = True
    path, goal, _ = a.plan(obs)
    assert path and goal[0] > 11.5  # search ground beyond the camera-covered neighbourhood
    a.searching = False
    a.searched[:] = False
    a.rescue_target = hint
    y, z = np.meshgrid(np.arange(-1.75, 2.26, 0.25), np.arange(0.25, 3.76, 0.25))
    wall = np.c_[np.full(y.size, 6.0), y.ravel(), z.ravel()]
    a.surface = {tuple(p): (p, 2, a.tick) for p in wall}
    path, _, _ = a.plan(obs)
    assert not path or max(p[0] for p in path) < 6.0
    a.tick += 31
    path, goal, _ = a.plan(obs)
    assert path and goal[0] > 10.0  # stale surface points must not override current free-space evidence
    assert a.line_clear(obs.pos, np.array([10., 0.25, 1.25]))
    points = np.random.default_rng(3).uniform(-3, 3, (1500, 3))
    a.icp(points - [0.2, 0.1, 0], a.cloud(points))
    assert 0 < np.linalg.norm(a.corr[1]) < 0.1

    # A failed branch must cause a retreat along flown positions, not endless goal reselection.
    a.info.update(agent_hz=10, max_speed_xy=3, hover_endurance_s=1200, mission_time_s=1200)
    a.rescued = False
    a.rescue_target, a.target = np.array([20., 0., 1.]), np.array([19., 0., 1.])
    obs.pos, obs.vel, obs.t, obs.battery = np.array([10., 0., 1.]), np.zeros(3), 100., 1.
    obs.landed, obs.gps = False, None
    obs.range_down = 2.
    a.motion.extend([obs.pos.copy() for _ in range(400)])
    a.headway = (0., 0.)
    a.crumbs = [np.array([float(x), 0., 1.]) for x in range(11)]
    for name in ("track_drift", "receive", "integrate", "mark_searched", "remember"):
        setattr(a, name, lambda obs: None)
    a.correct = lambda obs: obs
    a.reports, a.broadcast = lambda obs: [], lambda obs: []
    a.climb_cap, a.roof_gap = lambda obs: 1.5, np.inf
    a.follow = lambda obs, **kw: np.zeros(3)
    a.avoid = lambda obs: np.zeros(3)
    a.avoid_mates = lambda obs, v: v
    a.step(obs)
    assert a.recover_until > obs.t and a.target[0] < obs.pos[0] - 6
    assert any(np.allclose(p, [19, 0, 1]) for p in a.spent_regions)
    a.approach = [obs.pos.copy()]
    a.step(obs)
    assert a.enter_i == 1  # hand over to the map at the public entrance, without a blind extra leg
