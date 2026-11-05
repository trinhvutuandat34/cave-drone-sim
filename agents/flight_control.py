"""Position PID and LiDAR braking shared by the exercise and live-mapping agent."""
import numpy as np

from cavesim.api import body_rotation


class PID:
    def __init__(self, kp=1.2, ki=0.02, kd=0.25, i_limit=2.0):
        self.kp, self.ki, self.kd, self.i_limit = kp, ki, kd, i_limit
        self.integral = np.zeros(3)

    def update(self, error, velocity, dt):
        if dt <= 0:
            raise ValueError("PID timestep must be positive")
        self.integral = np.clip(self.integral + error * dt, -self.i_limit, self.i_limit)
        return self.kp * error + self.ki * self.integral - self.kd * velocity


def safe_velocity(obs, v):
    pts = obs.lidar @ body_rotation(obs.roll, obs.pitch, obs.yaw).T
    d = np.linalg.norm(pts, axis=1)
    keep = d > (0.6 if obs.range_down < 1.0 else 0.25)
    pts, d = pts[keep], d[keep]
    speed = np.linalg.norm(v)
    if speed > 1e-6 and len(pts):
        along = pts @ (v / speed)
        tube = (along > 0) & (d * d - along * along < 0.3 ** 2)
        if tube.any():
            cap = max(0.0, np.sqrt(4 * max(along[tube].min() - 0.6, 0)) - 0.3)
            v = v * min(1.0, cap / speed)
    # Infinity also means the ground is beyond the rangefinder's 12 m reach.
    # Descend slowly until it returns, with the planned path providing enclosure.
    v[2] = max(v[2], 0.8 - obs.range_down) if np.isfinite(obs.range_down) else max(v[2], -0.5)
    return v
