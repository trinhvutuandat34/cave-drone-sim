// Run with: node tests/test_keyboard.mjs
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";

const source = readFileSync(new URL("../viewer/main.js", import.meta.url), "utf8");
const listeners = {}, sent = [];
// Exercise the production listeners without loading Three.js or opening a browser.
runInNewContext(source.slice(source.indexOf("const PILOT_KEYS"), source.indexOf("// One separate window per sensor")), {
  addEventListener: (type, callback) => { listeners[type] = callback; },
  ws: { readyState: 1, send: (raw) => sent.push(JSON.parse(raw)) },
});
const event = (code, key, tagName = "CANVAS") => ({ code, key, target: { tagName }, preventDefault() {} });
listeners.keydown(event("KeyW", "ㅈ"));
assert.deepEqual(sent.at(-1).keys, ["w"]);
listeners.keyup(event("KeyW", "ㅈ", "SELECT"));
assert.deepEqual(sent.at(-1).keys, []);
listeners.keydown(event("KeyA", "a", "INPUT"));
assert.equal(sent.length, 2);
listeners.keydown(event("ArrowUp", "ArrowUp"));
assert.deepEqual(sent.at(-1).keys, ["arrowup"]);
listeners.blur();
assert.deepEqual(sent.at(-1).keys, []);
console.log("Keyboard layout, focus changes, arrows and blur: passed");
