# news-image-20261124

One image summing up the world's news of **Tuesday 24 November 2026**.

- `draw.py` — renders the front page (`entry.png`, 1024×1024) with PIL.
  Run offline: `python3 draw.py`. Nine stories, all dated 24 November
  2026: Nvidia reinstates Jensen Huang (lead), EU's 22nd Russia
  sanctions package, Kyiv's claim of sinking a Russian warship off
  Libya, Iran's Gulf strikes, Russian jets in South Korea's air
  defence zone, plus Spain, Mexico, Brazil and Gaza briefs.
- `main.ts` — the entrypoint. It only copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (Node 22, standard library only).
  It never runs `draw.py` and never touches the network, so both
  grading runs write identical bytes.

Local run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`
