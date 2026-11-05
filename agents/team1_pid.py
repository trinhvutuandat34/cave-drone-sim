"""Recorded-route rescue milestone. Only observations, public info and the pilot log are used.

Prepare: python -m agents.team1_pid runs/manual_YYYYMMDD_HHMMSS.jsonl
Fly: python -m cavesim.run --agent agents.team1_pid --map rescue_easy --drones 1 --lidar lite
This is the PID exercise; navigation without a recorded route is a separate agent.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

from agents.waypoints import load_log, thin
from agents.flight_control import PID, safe_velocity
from cavesim.api import Agent, Command, body_rotation

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "runs/team1_route.json"
KP, KI, KD = 1.2, 0.02, 0.25
SPEED = 1.5
ACCEPT_R = 1.2


def prepare_route(log_path, out=ROUTE):
    rows = load_log(log_path)
    seen = [i for i, r in enumerate(rows) if r.get("survivor")]
    if not seen:
        raise ValueError("The pilot log must include a survivor detection")
    # The log's landing overshot home. Stop at the recorded outdoor return; live GPS finishes it.
    end = next((i for i in range(seen[-1] + 1, len(rows)) if rows[i].get("gps") is not None), None)
    if end is None:
        raise ValueError("The pilot log must return outdoors after seeing the survivor")
    pts = np.array([r["pos"] for r in rows[:end + 1]], dtype=float)
    keep = sorted(set(thin(pts, 1.0) + [seen[-1], end]))
    route = {"source": str(log_path), "waypoints": pts[keep].tolist(),
             "yaw": [rows[i]["yaw"] for i in keep], "times": [rows[i]["t"] for i in keep],
             "survivor_waypoint": keep.index(seen[-1])}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(route, indent=1))
    print(f"{len(keep)} waypoints, return cut at {rows[end]['t']} s -> {out}")
    return route


class PIDRescueAgent(Agent):
    def __init__(self, drone_id, n_drones, info):
        super().__init__(drone_id, n_drones, info)
        if not info["odom_available"]:
            raise ValueError("The recorded-route PID exercise requires odometry")
        route = json.loads(ROUTE.read_text())
        self.wps = np.asarray(route["waypoints"], dtype=float)
        if self.wps.ndim != 2 or self.wps.shape[1] != 3 or len(self.wps) < 2 or not np.isfinite(self.wps).all():
            raise ValueError("Route must contain at least two finite 3D waypoints")
        self.yaws = route["yaw"]
        self.rescue_i = int(route["survivor_waypoint"])
        self.i, self.mode = 0, "outbound"
        self.base = np.asarray(info["base"], dtype=float)
        self.pid = PID(KP, KI, KD)
        self.last_t = None
        self.gps_offset = None
        self.goal = self.wps[0]
        self.crumbs = []
        self.log_file = (ROOT / "runs/team1_pid_log.csv").open("w", newline="", buffering=1)
        self.log = csv.writer(self.log_file)
        self.log.writerow(["t", "mode", "wp", "ex", "ey", "ez", "vx", "vy", "vz"])

    def step(self, obs):
        if obs.landed:
            return Command()
        dt = 0.1 if self.last_t is None else obs.t - self.last_t
        self.last_t = obs.t
        R = body_rotation(obs.roll, obs.pitch, obs.yaw)
        survivor = next((d for d in obs.detections if d.type == "survivor"), None)
        if self.mode == "outbound" and (not self.crumbs or np.linalg.norm(obs.pos - self.crumbs[-1]) > 1.0):
            for j, p in enumerate(self.crumbs[:-2]):
                if np.linalg.norm(obs.pos - p) < 1.0:
                    del self.crumbs[j + 1:]
                    break
            self.crumbs.append(obs.pos.copy())
        if self.mode == "outbound" and survivor is not None and np.linalg.norm(survivor.rel_pos) < 2.0:
            # Return on the path actually flown, rather than the pilot's differently drifted return.
            self.wps = np.array(self.crumbs[::-1])
            delta = np.diff(self.wps, axis=0, append=self.wps[-1:])
            self.yaws = np.arctan2(delta[:, 1], delta[:, 0])
            self.mode, self.i = "return", 0
            self.pid.integral[:] = 0
        if self.mode == "return" and obs.gps is not None:
            self.mode = "home"
        if self.mode == "home":
            if obs.gps is not None:
                off = obs.gps - obs.pos
                self.gps_offset = off if self.gps_offset is None else self.gps_offset + 0.05 * (off - self.gps_offset)
            self.goal = self.base - self.gps_offset
            self.goal[2] = obs.pos[2] + 1.0 - obs.range_down
            error = self.goal - obs.pos
            if np.linalg.norm(error[:2]) < 0.6:
                if obs.range_down < 0.6 and np.linalg.norm(obs.vel[:2]) < 0.25:
                    return Command(land=True)
                error[2] = -0.35
            yaw = obs.yaw
        else:
            limit = self.rescue_i if self.mode == "outbound" else len(self.wps) - 1
            while self.i < limit:
                delta = self.wps[self.i] - obs.pos
                near = np.linalg.norm(delta) < ACCEPT_R
                # Near the floor, its live range is a better height reference than a drifted log.
                near |= obs.range_down < 2.0 and np.linalg.norm(delta[:2]) < 1.0 and abs(delta[2]) < 2.5
                if not near:
                    break
                self.i += 1
                self.pid.integral[:] = 0
            self.goal = self.wps[self.i].copy()
            if self.mode == "outbound" and survivor is not None:
                self.goal = obs.pos + R @ survivor.rel_pos
            error = self.goal - obs.pos
            yaw = self.yaws[self.i]
        v = self.pid.update(error, np.asarray(obs.vel), dt)
        v *= min(1.0, SPEED / max(np.linalg.norm(v), 1e-9))
        v[2] = np.clip(v[2], -self.info["max_speed_z"], self.info["max_speed_z"])
        if self.mode != "home":
            v = safe_velocity(obs, v)
        turn = (yaw - obs.yaw + np.pi) % (2 * np.pi) - np.pi
        self.log.writerow([round(obs.t, 1), self.mode, self.i, *np.round(error, 3), *np.round(v, 3)])
        return Command(vel=v, yaw_rate=np.clip(1.5 * turn, -0.8, 0.8))

    def debug(self):
        return {"mode": f"PID {self.mode} {self.i}/{len(self.wps)}", "goal": self.goal.tolist(),
                "path": self.wps[self.i:self.i + 25].tolist()}


Agent = PIDRescueAgent

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m agents.team1_pid runs/manual_YYYYMMDD_HHMMSS.jsonl")
    prepare_route(sys.argv[1])
