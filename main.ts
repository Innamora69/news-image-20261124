// News-image entry for Tuesday 24 November 2026 (Node 22, stdlib only).
// The front page is rendered offline by draw.py and committed as
// entry.png. This program only copies that file into the grader's
// output directory, so both runs write exactly the same bytes.
// It never runs draw.py, never touches the network, and never
// writes anything but /output/entry.png. The copy is byte-exact,
// so the two grading runs produce identical output by construction.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);
const target = join(outDir, "entry.png");

const before = statSync(source);
if (before.size === 0 || before.size > 1048576) {
  throw new Error(`entry.png size ${before.size} is outside 1..1048576 bytes`);
}
const magic = readFileSync(source).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!magic.equals(pngMagic)) {
  throw new Error("entry.png is not a PNG file");
}
copyFileSync(source, target);
const after = statSync(target);
if (after.size !== before.size) {
  throw new Error("copied entry.png differs in size from the source");
}
