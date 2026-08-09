/* STAKKA headless logic test — node Stakka/test.js */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');
const src = html.match(/<script>([\s\S]*?)<\/script>/)[1];
// 내부 상태를 테스트로 노출 (프로덕션 코드는 그대로)
const probed = src.replace(
  /\}\)\(\);\s*$/,
  `globalThis.__T = {
     get state(){return state}, get blocks(){return blocks}, get mover(){return mover},
     get combo(){return combo}, get score(){return score}, get debris(){return debris},
     BASE, BH, AMP, PERFECT, MIN_SIZE, update, render, tap
   };
})();`
);

/* ── DOM stubs ── */
const noop = () => {};
const ctxStub = new Proxy({}, {
  get(_, k) {
    if (k === 'createLinearGradient' || k === 'createRadialGradient') return () => ({ addColorStop: noop });
    if (k === 'setTransform' || k === 'canvas') return k === 'canvas' ? {} : noop;
    return typeof k === 'string' ? noop : undefined;
  },
  set() { return true; }
});
const mkEl = () => ({
  style: {}, textContent: '',
  classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
               toggle(c, v) { v ? this._s.add(c) : this._s.delete(c); }, contains(c) { return this._s.has(c); } },
  addEventListener: noop
});
const canvas = { getContext: () => ctxStub, style: {}, width: 0, height: 0 };
const els = {};
const store = new Map();
let rafQ = [];

const sandbox = {
  console,
  document: {
    hidden: false,
    getElementById: id => (id === 'c' ? canvas : (els[id] || (els[id] = mkEl()))),
    addEventListener: noop
  },
  localStorage: {
    getItem: k => (store.has(k) ? store.get(k) : null),
    setItem: (k, v) => store.set(k, v)
  },
  navigator: {},
  performance: { now: () => Date.now() },
  requestAnimationFrame: fn => { rafQ.push(fn); return rafQ.length; },
  setTimeout: (fn) => { fn(); return 0; },
  innerWidth: 390, innerHeight: 844, devicePixelRatio: 2,
  addEventListener: noop,
  AudioContext: undefined
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(probed, sandbox);
const T = sandbox.__T;

/* ── assert ── */
let pass = 0, failN = 0;
const ok = (c, msg) => { if (c) { pass++; } else { failN++; console.log('  FAIL: ' + msg); } };

const step = (n = 1, dt = 1 / 60) => { for (let i = 0; i < n; i++) T.update(dt); };
const alignPerfect = () => { // 완벽 정렬 강제
  const p = T.blocks[T.blocks.length - 1];
  if (T.mover.axis === 'x') T.mover.x = p.x; else T.mover.z = p.z;
};
const offsetBy = v => {
  const p = T.blocks[T.blocks.length - 1];
  if (T.mover.axis === 'x') T.mover.x = p.x + v; else T.mover.z = p.z + v;
};

/* 1. 시작 */
ok(T.state === 'menu', 'boot state is menu');
T.tap();
ok(T.state === 'play', 'tap starts game');
ok(T.blocks.length === 1, 'reset leaves only base block');
ok(T.mover !== null, 'mover spawned');
ok(T.mover.axis === 'x', 'level 1 moves on x');

/* 2. 왕복 범위 */
let minP = Infinity, maxP = -Infinity;
for (let i = 0; i < 900; i++) { step(); const v = T.mover.axis === 'x' ? T.mover.x : T.mover.z; minP = Math.min(minP, v); maxP = Math.max(maxP, v); }
const base = T.blocks[0];
const center = T.mover.axis === 'x' ? base.x : base.z;
ok(Math.abs(minP - (center - T.AMP)) < 6, 'sweep min within amplitude');
ok(Math.abs(maxP - (center + T.AMP)) < 6, 'sweep max within amplitude');

/* 3. 퍼펙트 콤보 & 회복 */
alignPerfect(); T.tap();
ok(T.combo === 1, 'first perfect sets combo 1');
ok(T.blocks.length === 2 && T.blocks[1].w === T.BASE, 'perfect keeps full size');
ok(T.score === 1, 'score follows height');
ok(T.mover.axis === 'z', 'axis alternates');

/* 4. 잘림 */
offsetBy(40); T.tap();
const cut = T.blocks[T.blocks.length - 1];
ok(Math.abs(cut.d - (T.BASE - 40)) < 0.001, 'sliced size = overlap');
ok(T.combo === 0, 'miss resets combo');
ok(T.debris.length === 1, 'debris spawned on slice');

/* 5. 회복(grow-back): 연속 퍼펙트로 다시 커진다 */
const before = T.blocks[T.blocks.length - 1].d;
alignPerfect(); T.tap();          // combo 1 (회복 없음)
alignPerfect(); T.tap();          // combo 2 → 성장
alignPerfect(); T.tap();          // combo 3 → 성장
const grown = T.blocks[T.blocks.length - 1];
ok(T.combo === 3, 'combo chains to 3');
ok(grown.d > before || grown.w > before, 'grow-back enlarges block');
ok(grown.w <= T.BASE + 1e-9 && grown.d <= T.BASE + 1e-9, 'growth capped at BASE');

/* 6. 완전 빗나감 → 게임오버 */
offsetBy(T.BASE + 5); T.tap();
ok(T.state === 'over', 'no overlap ends run');
ok(sandbox.__T.mover === null, 'mover cleared on fail');
ok(store.get('stakka.best') === String(T.score), 'best persisted');

/* 7. 즉시 재시작(쿨다운 후) */
T.tap();
ok(T.state === 'over', 'restart blocked during cooldown');
sandbox.performance.now = () => Date.now() + 5000;
T.tap();
ok(T.state === 'play', 'restart allowed after cooldown');

/* 8. 장기 실행 안정성: 퍼펙트 300연타 + 렌더 */
for (let i = 0; i < 300; i++) { step(3); alignPerfect(); T.tap(); }
ok(T.state === 'play', '300 perfect placements survive');
ok(T.blocks[T.blocks.length - 1].w > 0 && T.blocks[T.blocks.length - 1].d > 0, 'block dims stay positive');
ok(T.mover.speed <= 385 + 1e-9, 'speed capped');
step(120); T.render();
ok(true, 'render runs without throwing');

/* 9. 얇은 블록 생존 하한 — 허용오차가 크기에 비례하므로 반드시 끝난다 */
let guard = 0;
while (T.state === 'play' && guard++ < 200) {
  const last = T.blocks[T.blocks.length - 1];
  offsetBy((T.mover.axis === 'x' ? last.w : last.d) * 0.5);
  T.tap();
}
ok(T.state === 'over', 'repeated halving ends run (no infinite grow-back loop)');
ok(guard < 40, 'halving terminates quickly (' + guard + ' steps)');

console.log(`\n${pass} passed, ${failN} failed`);
process.exit(failN ? 1 : 0);
