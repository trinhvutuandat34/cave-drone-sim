import assert from "node:assert/strict";
import { parseProgress, recordingStates } from "../viewer/recording.js";

assert.deepEqual(parseProgress('{"roof_gap": Infinity,"t":1}\n{"roof_gap":0.8,"t":2}\n'),
  [{ roof_gap: null, t: 1 }, { roof_gap: 0.8, t: 2 }]);
assert.deepEqual(parseProgress('{"roof_gap":-Infinity}\n{"roof_gap":NaN}'),
  [{ roof_gap: null }, { roof_gap: null }]);
assert.equal(parseProgress('{"roof_gap":"Infinity"}')[0].roof_gap, "Infinity");
assert.throws(() => parseProgress('{"invalid": Infinity}'), SyntaxError);

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
