# Style presets — 12 visual + motion languages

Pick with `new_project.sh <slug> --theme <name>`; **`light` is the default**.
Human-browsable live gallery: open `$SKILL_DIR/assets/gallery/styles-gallery.html`
in a browser (each card loops its motion program; mixed aspect ratios shown).

Every preset defines palette + fonts + shape tokens (the base stylesheet reads
them — **never hardcode `rx`, `stroke-width`, or `font-family` on the standard
classes**) *and* a motion language for the timeline. Transparent canvas: add
`--transparent` (deliver via SVG / interactive HTML / `--format webm|mov`;
MP4 flattens transparency to black — use `light` for white-background video).

| # | `--theme` | Look | Fonts (title/body) | Shapes | Motion language |
|---|---|---|---|---|---|
| 1 | `light` ★default | white canvas, slate ink, blue accent | Inter / Inter | radius 16, medium strokes | **classic**: 5-act, `power2.out`, `back.out(1.4)` node pops |
| 2 | `dark` | deep-navy, neon strokes, glow pulses | Inter / Inter | radius 18 | **classic + glow**: same arc, glow-filter emphasis, particles shine |
| 3 | `blueprint` | blueprint blue, pale cyan linework | Space Grotesk / Plex Mono | radius 4, hairlines, dashed | **draft**: DrawSVG *everything* incl. node rects (ease `none`), text after lines |
| 4 | `sketch` | paper white, charcoal pen | Caveat / Caveat | radius 10, round caps | **hand-drawn**: draw-on heavy, slight overshoot; labels ~110% size |
| 5 | `corporate` | cool gray, indigo system | Archivo / Archivo | radius 8, solid regions | **crisp**: `power3.out` slide-ins (x not y), no bounce ever, tight staggers |
| 6 | `pastel` | cream, candy fills | Nunito / Nunito | radius 28 (region 34) | **bouncy**: `back.out(1.9)` scale-ins from 0.3, `bounce.out` settles |
| 7 | `mono` | white paper terminal | Plex Mono everywhere | radius 2, square, thin | **steps**: instant `.set`-like reveals (duration .01), `steps(n)` eases |
| 8 | `editorial` | ivory, ink + crimson accent | Fraunces / Inter | radius 3, hairline rules | **fade**: slow 0.9–1s `power1.inOut` crossfades, long overlaps, stately |
| 9 | `vivid` | white, saturated flat colors | Space Grotesk / Space Grotesk | radius 12, thick 3.5–4px | **snappy**: `expo.out` ≤0.32s moves, fast staggers (.09), confident |
| 10 | `glass` | soft gradient canvas, translucent cards | Inter / Inter | radius 20, 1.5px strokes | **floaty**: 1s `power1.inOut` drifts, gentle y-float idle, slow particles |
| 11 | `brutalist` | white+acid yellow, black borders | Archivo 800 / Archivo | radius 0, 3.5–4px, hard offset shadow | **abrupt**: instant sets, `back.out(4)` 0.14s pops, `steps()` pulses, shake accents |
| 12 | `wireframe` | white, gray dashed placeholders | Inter / Inter | radius 6, 1.5px dashed | **quickfade**: utilitarian 0.25–0.3s fades; edges are dashed → fade, don't DrawSVG |

## Per-style notes that change how the timeline is written

- **blueprint (draft)**: draw node rects with `drawSVG` too — `tl.from(".node rect", { drawSVG: "0%", ease: "none" })`, then fade node text. Region rects also drafted. No scale/bounce anywhere.
- **sketch**: keep DrawSVG durations a bit uneven (0.5/0.65/0.45…) for a human feel; `back.out(1.2)` max.
- **corporate**: entrances slide on x (−14px), never y-pop; one restrained emphasis max.
- **mono / brutalist (steps, abrupt)**: replace fades with near-instant reveals (`duration: .01` at staggered times) and `steps(n)` eases on draws/pulses; brutalist may add a 1-frame shake (`x:2 → 0`, `steps(1)`).
- **wireframe**: edges have `--dash-edge` — DrawSVG would destroy the dashes; fade edges in (`opacity`) instead.
- **glass**: add a gentle idle float after entrance (`y: -3 ↔ 0`, `sine.inOut`) — bounded repeats only.
- **editorial**: durations ≥0.8s, overlap acts by ~40%; no overshoot eases; particles slow (1.2s+/hop).
- **pastel**: scale-ins from 0.3 with `transformOrigin: "50% 50%"`; arrowheads `back.out(3)`.
- **dark**: use `filter="url(#glow)"` on pulses and on one emphasized node copy.
- **brutalist**: use a hard shadow filter (offset, `stdDeviation 0`) instead of `#card-shadow`:
  `<feDropShadow dx="6" dy="6" stdDeviation="0" flood-color="#000"/>`.

## Aspect ratios

Any `--width/--height` works; common picks: 1920×1080 (default), 1080×1920
(`portrait` — stack flows vertically, edges run top→down), 1080×1080 (square),
3840×2160 via `--resolution landscape-4k` at render time (vector = crisp).
For portrait: HUD title ~y 150, nodes in a single column, regions tall.

## Transparent background

`new_project.sh <slug> --transparent` appends `--bg: transparent`. Honest
delivery paths: SVG export (transparent by nature), interactive HTML, or
`hyperframes render --format webm` / `mov` (alpha kept) for video overlays.
Plain MP4 cannot carry alpha.
