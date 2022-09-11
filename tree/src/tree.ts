import { Path, path } from "d3-path";

import { line, curveCatmullRom } from "d3-shape";
import { SeedRandom } from "./rand";

/**
 * Returns an SVG path rendering a random tree.
 */
export default function treePath(w: number, h: number): string {
  const rng = SeedRandom(216);
  const t = tree([w * 0.05, h / 2], [w * 0.3, h / 2], 5, rng);
  const lines = [].concat(t.trunks, t.leaves);

  const p = path();
  for (const ln of lines) {
    const lineFunc = line()
      .x((d: Pt) => d[0])
      .y((d: Pt) => d[1])
      .curve(curveCatmullRom.alpha(0.5))
      .context(p as any);
    lineFunc(ln);
  }

  return p.toString();
}

interface Tree {
  trunks: Pt[][];
  leaves: Pt[][];
}

function tree(start: Pt, end: Pt, level: number, rng: () => number): Tree {
  if (level === 0) {
    return { trunks: [[start, end]], leaves: [] };
  }
  const sprouts = (2 + rng() * 2) | 0;
  const spread = 0.4 + level * 0.15 + rng() * 0.1;
  const bend = 0.5 * (rng() - 0.5);
  const fwd = mul(0.55 + rng() * 0.08, sub(end, start));
  const up: Pt = [fwd[1], -fwd[0]];

  const ret: Tree = { trunks: [], leaves: [] };
  for (let i = 0; i < sprouts; i++) {
    const rho = (i - sprouts / 2 + 0.5) * spread + bend; // radians
    const next = add(end, add(mul(Math.cos(rho), fwd), mul(Math.sin(rho), up)));
    const subtree = tree(end, next, level - 1, rng);

    // All subtree leaves remain leaves
    ret.leaves.push(...subtree.leaves);

    // Some subtree trunks become leaves, others extend further upward.
    ret.trunks.push(...subtree.trunks.filter((_, i) => i % 2 === 0));
    ret.leaves.push(...subtree.trunks.filter((_, i) => i % 2 > 0));
  }

  // Spread subtrees apart
  const up0 = mul(3 / l2(up), up);
  for (let i = 0; i < ret.trunks.length; i++) {
    const steps = i - ret.trunks.length / 2;
    const trunk = ret.trunks[i];
    trunk[0] = add(trunk[0], mul(steps * 1, up0));
    trunk.unshift(add(start, mul(steps, up0)));
  }
  return ret;
}

type Pt = [number, number];

function l2(a: Pt): number {
  return Math.sqrt(dot(a, a));
}

function dot(a: Pt, b: Pt): number {
  return a[0] * b[0] + a[1] * b[1];
}

function mul(a: number, v: Pt): Pt {
  return [a * v[0], a * v[1]];
}

function add(a: Pt, b: Pt): Pt {
  return [a[0] + b[0], a[1] + b[1]];
}

function sub(a: Pt, b: Pt): Pt {
  return [a[0] - b[0], a[1] - b[1]];
}
