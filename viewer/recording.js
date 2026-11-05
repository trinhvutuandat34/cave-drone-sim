// Saved trajectories contain positions every 0.5 s, rather than video or attitudes.
export function recordingStates(record, progress = []) {
  const trail = record.true?.[0], odom = record.odom?.[0];
  const end = record.score?.time_s;
  if (!trail?.length || !Number.isFinite(end) || end <= 0) throw new Error("Invalid trajectory recording");
  const states = [];
  let row = 0, yaw = 0;
  const position = (points, t) => {
    const k = Math.min(Math.floor(t / 0.5), points.length - 1);
    const next = points[Math.min(k + 1, points.length - 1)], f = Math.min(1, (t - k * 0.5) / 0.5);
    return points[k].map((v, i) => v + f * (next[i] - v));
  };
  for (let tick = 0; tick <= Math.ceil(end * 10); tick++) {
    const t = Math.min(tick / 10, end), done = t >= end;
    while (row + 1 < progress.length && progress[row + 1].t <= t) row++;
    const sample = progress[row];
    const pos = position(trail, t), ahead = position(trail, Math.min(t + 0.5, end));
    if (Math.hypot(ahead[0] - pos[0], ahead[1] - pos[1]) > 0.01) yaw = Math.atan2(ahead[1] - pos[1], ahead[0] - pos[0]);
    const rescued = Object.fromEntries(Object.entries(record.score.rescued_at_s || {}).filter(([, at]) => at <= t));
    const score = done ? record.score : {
      ...(sample?.t <= t ? sample.score : {}), rescued_at_s: rescued,
      lap_time_s: null, success: false, returned: [],
    };
    states.push({ type: "state", t, score, links: [], base_links: [],
      found: Object.keys(rescued).length ? [0] : [],
      drones: [{ id: 0, pos, odom: odom?.length ? position(odom, t) : null, yaw, rp: [0, 0],
        status: done ? "landed" : "flying", battery: sample?.t <= t ? sample.battery : 1,
        vel: ahead.map((v, i) => (v - pos[i]) * 2), clear: null, aero: [0, 0, 0],
        debug: { mode: "Recorded trajectory · heading estimated · LiDAR not recorded" } }],
    });
  }
  return states;
}
