# Large flows — camera pan/zoom patterns

When a diagram has many nodes (long control flows, sequence diagrams, code
walkthroughs, wide pipelines), don't shrink it to fit — **author it larger
than the canvas and let the camera tell the story**. The template ships an
inline CAMERA RIG (in every scaffolded `index.html`):

```js
camFit(tl, "#node-x", { zoom?, at, dur, pad })  // center+zoom to a group's bbox (auto zoom if omitted)
camFitAll(tl, { at, dur })                      // fit the whole scene (scale < 1 for oversized scenes)
camPanTo(tl, cx, cy, z, { at, dur })            // center on scene point at zoom z
camHome(tl, { at, dur })                        // reset to identity
camFollow(tl, "#edge-a-b", { at, dur, zoom })   // track a path, keeping it centered (pair with a pulse)
```

All tween only `#camera`; the HUD stays fixed. `getBBox`/`getPointAtLength`
are deterministic under the frame-seeking renderer.

## Authoring oversized scenes

- Author node coordinates freely beyond the viewBox (e.g. an 8-step flow at
  x 100…4200 on a 1920-wide canvas; a 40-message sequence at y 100…4800).
- Start the timeline either **fitted** (`tl.add(camFitAll(...), 0)` via a
  0-duration set, then zoom in) or **already zoomed on step 1** — never start
  on a half-cropped arbitrary framing.
- End EVERY large-flow animation with `camFitAll` + ≥1.2s hold — the final
  overview is the poster frame.
- Max zoom 2.2× (rig clamps auto-fit); keep one move at a time; 0.3–0.5s of
  rest between camera moves so viewers can read.

## The 6 variation patterns

### 1. Guided tour — *default for long control flows*
Overview → zoom to step 1 → hop stop-by-stop (camFit each group as it
activates) → final overview.
```js
camFitAll(tl, { at: 0, dur: 0.001 });
camFit(tl, "#node-step1", { at: 1.0 });           // dwell ~1.2s per stop
camFit(tl, "#node-step3", { at: 3.4 });
camFit(tl, "#node-step6", { at: 5.8 });
camFitAll(tl, { at: 8.2 }); tl.to({}, { duration: 1.4 });
```
Sync each stop with that node's entrance/emphasis. Dwell ≥ 1s per stop.

### 2. Follow-cam — *token/request traversing a long path*
The camera rides with the pulse. Pair `camFollow` with the SAME path and
duration as the pulse's motionPath tween, same `at`:
```js
tl.to("#pulse-1", { motionPath: { path: "#edge-long", align: "#edge-long",
  alignOrigin: [.5,.5] }, duration: 3, ease: "none" }, 4.0);
camFollow(tl, "#edge-long", { at: 4.0, dur: 3, zoom: 1.35 });
camFitAll(tl, { at: 7.2 });
```
Best for: message routes, packet journeys, ETL hops. One follow per video.

### 3. Vertical scroll — *sequence diagrams, code walkthroughs, chat flows*
Portrait-logic even on landscape: content extends downward; camera pans down
message-by-message (constant zoom), like reading.
```js
camPanTo(tl, 960, 420, 1.15, { at: 1.5 });        // first message block
camPanTo(tl, 960, 980, 1.15, { at: 3.5 });        // next block…
camPanTo(tl, 960, 1640, 1.15, { at: 5.5 });
camFitAll(tl, { at: 7.8 });
```
Reveal each message (draw + label) only when the camera arrives. For code
navigation: `mono` style, code lines as rows, a highlight rect slides + the
camera follows line groups; annotate with side callouts.

### 4. Conveyor — *wide pipelines (CI/CD, ETL stages)*
Constant-speed lateral slide while stages light up beneath the camera; feels
like a factory line. One long pan, not hops:
```js
camPanTo(tl, 700, 540, 1.2, { at: 1.2, dur: 0.9 });
camPanTo(tl, 3400, 540, 1.2, { at: 2.4, dur: 5.5, ease: "none" });  // the conveyor
camFitAll(tl, { at: 8.2 });
```
Stage entrances fire as the camera reaches them (stagger timed to pan speed).

### 5. Pulse-zoom (overview ↔ detail) — *architectures with hot spots*
Stay on the overview; repeatedly dive into one subsystem and back:
overview → zoom region A (dwell, micro-animation plays inside) → overview →
zoom region B → … → overview. Use when spatial context matters more than
sequence. `camFit(region)` / `camHome` alternation; dim everything outside
the focused region (`opacity .35` on siblings) while zoomed.

### 6. Reveal-pan — *the diagram is the landscape*
Start zoomed in (1.4–1.8×) on the entry point with the rest off-screen;
one slow continuous pan along the flow axis reveals structure for the first
time as it passes; end `camFitAll` for the full-map payoff. The most
cinematic option — pair with `editorial`/`glass`/`dark` styles, durations
1.5× longer than usual.

## Choosing a pattern

| Diagram | Pattern |
|---|---|
| Control flow / flowchart, 8–20 nodes | guided tour (1) |
| One request/token crossing many systems | follow-cam (2) |
| Sequence diagram, code walkthrough, chat | vertical scroll (3) |
| Linear pipeline, wide | conveyor (4) |
| Architecture with 2–4 focus areas | pulse-zoom (5) |
| First-reveal storytelling, maps | reveal-pan (6) |
| ≤ 6 nodes | **no camera at all** |

Live demos of all six: gallery → "Camera patterns" section
(`assets/gallery/styles-gallery.html`).

## Portrait notes

For 1080×1920: vertical scroll is the native pattern; guided-tour stops stack
top→down; conveyor becomes a vertical drop. Zoom factors read ~15% stronger
on portrait — reduce by 0.1–0.2.
