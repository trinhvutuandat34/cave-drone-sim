import assert from "node:assert/strict";
import { recordingStates } from "../viewer/recording.js";

const score = { time_s: 1.1, success: true, returned: [0], lap_time_s: 1.1, rescued_at_s: { 0: 0.6 } };
const record = { score, true: [[[0, 0, 1], [1, 0, 1], [1, 1, 0.1]]], odom: [] };
const states = recordingStates(record);
assert.deepEqual(states[0].drones[0].pos, [0, 0, 1]);
assert.deepEqual(states[2].drones[0].pos, [0.4, 0, 1]);
assert.deepEqual(states[5].score.rescued_at_s, {});
assert.equal(states[6].score.rescued_at_s[0], 0.6);
assert.equal(states[10].score.success, false);
assert.equal(states.at(-1).t, 1.1);
assert.equal(states.at(-1).drones[0].status, "landed");
assert.deepEqual(states.at(-1).score, score);
assert.throws(() => recordingStates({}), /Invalid/);
console.log("Recording interpolation, rescue timing and final result: passed");
