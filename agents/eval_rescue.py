"""Reproducible headless rescue runs with progress, failures and scored results.

python -m agents.eval_rescue --agent agents.team1 --seeds 0 1 2
"""
import argparse
import importlib
import hashlib
import json
import gzip
import pickle
from datetime import datetime
from pathlib import Path

import numpy as np

from cavesim.sim import Simulator
from cavesim.config import SimConfig


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agent", default="agents.team1")
    ap.add_argument("--map", default="rescue_easy")
    ap.add_argument("--seeds", type=int, nargs="+", default=[0])
    ap.add_argument("--target-error", type=float, default=0.0)
    ap.add_argument("--snapshot", action="store_true", help="save the agent and its last observation for offline diagnostics")
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = root / "runs"
    out.mkdir(exist_ok=True)
    module = importlib.import_module(args.agent)
    agent = module.Agent
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
               [Path(module.__file__), root / "agents/flight_control.py"]}
    failed = False
    for seed in args.seeds:
        name = f"{args.agent.rsplit('.', 1)[-1]}_{args.map}_seed{seed}_{datetime.now().astimezone():%Y%m%d_%H%M%S}"
        sim = Simulator(root / "maps" / args.map, 1, agent, lidar="lite", seed=seed,
                        cfg=SimConfig(target_error_m=args.target_error))
        try:
            with (out / f"{name}_progress.jsonl").open("w", buffering=1) as trace:
                while True:
                    running = sim.step()
                    d, a = sim.drones[0], sim.agents[0]
                    if d.error:
                        raise RuntimeError(d.error)
                    if sim.tick % 100 == 0 or not running:
                        roof_gap = getattr(a, "roof_gap", np.inf)
                        row = {"t": round(sim.t, 1), "status": d.status, "debug": a.debug(),
                               "pos": np.round(d.last_obs.pos, 2).tolist(), "battery": round(d.battery, 3),
                               "velocity": np.round(d.last_obs.vel, 3).tolist(), "command": np.round(d.cmd.vel, 3).tolist(),
                               "range_down": float(d.last_obs.range_down) if np.isfinite(d.last_obs.range_down) else None,
                               "gps": None if d.last_obs.gps is None else np.round(d.last_obs.gps, 2).tolist(),
                               "roof_gap": float(roof_gap) if np.isfinite(roof_gap) else None,
                               "score": sim.score()}
                        trace.write(json.dumps(row, default=lambda x: np.asarray(x).tolist()) + "\n")
                        print(json.dumps({"t": row["t"], "status": row["status"], "mode": row["debug"].get("mode"),
                                          "pos": row["pos"], "goal": row["debug"].get("goal"), "battery": row["battery"]},
                                         default=lambda x: np.asarray(x).tolist()), flush=True)
                    if not running:
                        break
        finally:
            if args.snapshot:
                with gzip.open(out / f"{name}_agent.pkl.gz", "wb") as f:
                    pickle.dump((sim.agents[0], sim.drones[0].last_obs), f)
            finished = not any(d.active for d in sim.drones) or sim.t >= sim.cfg.mission_time_s
            result = {"agent": args.agent, "map": args.map, "seed": seed, "target_error_m": args.target_error,
                      "sources": sources, "finished": finished, "score": sim.score(), **sim.trails()}
            (out / f"{name}.json").write_text(json.dumps(result))
            print(json.dumps(result["score"], indent=1), flush=True)
            sim.close()
        failed |= not result["score"]["success"]
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
