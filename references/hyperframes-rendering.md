# HyperFrames rendering — contract & CLI (verified against v0.6.91)

HyperFrames renders the composition deterministically: headless Chrome loads
`index.html`, the runtime **seeks** the registered GSAP timeline to each frame
time, screenshots it, and pipes frames to FFmpeg. Same input ⇒ identical MP4.

## Composition contract

- Project dir needs `index.html`; the root element:

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="12"
     data-width="1920" data-height="1080"> … </div>
```

- `data-duration` (seconds) defines video length — keep it equal to
  `tl.duration()` (the probe in render.mjs warns on mismatch).
- Timeline: `{ paused: true }`, registered as
  `window.__timelines["main"]` (key = `data-composition-id`), in an **inline**
  `<script>` (external local scripts are not executed by `snapshot`).
- `<meta name="viewport" content="width=1920, height=1080">` and html/body sized
  to match.
- Static content (our SVG) can live directly in `#root` — `class="clip"` +
  `data-start/duration/track-index` are only for elements that should appear /
  disappear via the runtime (multi-shot videos); a single-scene diagram doesn't
  need clips.

### Determinism rules

- No `Date.now()`, `Math.random()`, `setInterval`, rAF-driven motion, network
  fetches. All motion on the registered timeline; repeats bounded.
- All assets local + relative (`./vendor/...`, `./fonts/...`); fonts via
  `@font-face` woff2 (the renderer waits for fonts before capture).
- CSS animations/transitions on moving elements are forbidden (they run on
  wall-clock, not the seeked timeline).

## CLI (the skill's binary: `$SKILL_DIR/node_modules/.bin/hyperframes`)

```bash
hyperframes render <DIR> -o out.mp4 [--fps 30] [--quality draft|standard|high]
    [--format mp4|webm|mov|gif|png-sequence]   # webm/mov support transparency
    [--resolution landscape|portrait|square|landscape-4k|...]  # PRESET names —
        # Chrome renders at higher DPR; aspect must match the composition
hyperframes snapshot <DIR> --frames 5            # evenly spaced PNGs + contact-sheet.jpg
hyperframes snapshot <DIR> --at 0.1,3.0,11.5     # exact timestamps
hyperframes lint <DIR>                           # static composition checks
hyperframes preview                              # live studio (long-running server —
                                                 #   run in background, never foreground)
hyperframes doctor                               # env check (Chrome/ffmpeg/etc.)
hyperframes browser ensure|path|clear            # manage render Chrome
hyperframes docs <topic>    # local docs: data-attributes, gsap, compositions,
                            # rendering, examples, troubleshooting
```

Notes observed in practice:

- `lint` doesn't understand DrawSVG/MotionPath specifics — its "supported
  properties" warnings are heuristics; the renderer plays whatever GSAP renders.
  A clean smoke test with both plugins is verified working.
- ~3–4s total render for a 6s 1080p30 composition on this machine.
- `snapshot --describe false` skips the Gemini vision step (no API key needed).
- Renders land at `renders/<name>.mp4` if `-o` is omitted.

**Prefer `scripts/render.mjs` over calling the CLI directly** — it adds GIF/WebM
derivation, snapshot capture, and sanity probes in one shot.

## Troubleshooting

| Symptom | Cause → fix |
|---|---|
| Blank/black video | Timeline not registered, or registered after load error — check browser console via `hyperframes preview`; verify `window.__timelines["main"]` key matches `data-composition-id` |
| Duration 0 / tiny file | Empty timeline at registration time; or `data-duration` missing |
| Video shorter than animation | `data-duration` < `tl.duration()` — the attribute wins |
| Wrong fonts in output | woff2 path broken (must be relative to index.html); check `@font-face` URL |
| Arrowheads visible early | `marker-end` on edges — switch to separate `.edge-head` elements |
| Dotted line becomes solid while drawing | DrawSVG on `edge--flow` — use `stroke-dashoffset` |
| Snapshots show the static authored DOM (no animation states) | Timeline registered from an **external** `<script src>` — `snapshot` does not execute external local scripts (render does). Keep the timeline INLINE in index.html |
| Rendered MP4 is silent despite `<audio>` element | The `<audio>` is missing an `id` attribute — the renderer requires it to discover media (verified; `lint` flags it as `media_missing_id`) |
| First render very slow | One-time Chrome download — `hyperframes browser ensure` pre-fetches |
| `npm run dev` dies / preview broken | It's a long-running server — launch with `run_in_background: true` |
