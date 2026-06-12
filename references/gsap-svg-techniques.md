# GSAP × SVG techniques (vendored plugins)

The job dir vendors `gsap.min.js`, `DrawSVGPlugin.min.js`, `MotionPathPlugin.min.js`,
`MorphSVGPlugin.min.js` (load Morph only when morphing). Register before use:

```js
gsap.registerPlugin(DrawSVGPlugin, MotionPathPlugin);
```

## DrawSVG — edge draw-on

```js
tl.from(".edge", { drawSVG: "0%", duration: 0.6, stagger: 0.12 });
// partial reveals: drawSVG: "20% 80%" (a moving segment)
```

- Works on stroked `path/line/polyline/circle/rect/ellipse` — `fill` is untouched.
- **Overrides `stroke-dasharray`** — never use on dotted `edge--flow` lines;
  animate those with `stroke-dashoffset` instead:

```js
// dotted flow drift: one dash cycle = dasharray period (2+12=14 here)
tl.to(".edge--flow", { strokeDashoffset: -14 * 12, duration: 6, ease: "none" }, 4);
```

- `marker-end` arrowheads appear before the draw starts (verified) — use
  separate `.edge-head` triangles, faded in at the right moment:

```js
tl.from("#edge-a-b", { drawSVG: "0%", duration: 0.6 }, 3.0)
  .from("#head-a-b", { opacity: 0, scale: 0, transformOrigin: "50% 50%",
                       duration: 0.25, ease: "back.out(2)" }, 3.45); // ~when draw lands
```

## MotionPath — pulses riding edges

```js
tl.set("#pulse-1", { opacity: 1 }, 5.0)
  .to("#pulse-1", {
    motionPath: { path: "#edge-a-b", align: "#edge-a-b", alignOrigin: [0.5, 0.5] },
    duration: 1.2, ease: "none", repeat: 2,        // bounded repeats only
  }, 5.0)
  .set("#pulse-1", { opacity: 0 });                 // park it when done
```

- `align` + `alignOrigin: [0.5,0.5]` centers the particle on the path.
- Chain hops: after edge A→B completes, start a second tween along `#edge-b-c`.
- Multiple particles on one edge: same tween, different start offsets
  (`start: 0.0 / end: 1.0` defaults; or stagger separate tweens by 0.4s).
- Give pulses `filter="url(#glow)"` and the theme `--accent` color.

## MorphSVG — shape-to-shape

```js
gsap.registerPlugin(MorphSVGPlugin);
tl.to("#icon-state-a", { morphSVG: { shape: "#icon-state-b", type: "rotational" }, duration: 0.8 });
```

Use sparingly (state machines, icon swaps). Both shapes must be `<path>`
(`MorphSVGPlugin.convertToPath("circle, rect")` converts primitives).

## Camera rig

`#camera` wraps the whole scene; HUD lives outside it.

```js
// zoom to a target group, centered, then return
function zoomTo(tl, sel, zoom, at, dur = 1.2) {
  const W = 1920, H = 1080;                         // composition size
  const b = document.querySelector(sel).getBBox();
  const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
  tl.to("#camera", {
    scale: zoom, x: W / 2 - cx * zoom, y: H / 2 - cy * zoom,
    transformOrigin: "0 0", duration: dur, ease: "power3.inOut",
  }, at);
  return tl;
}
zoomTo(tl, "#node-api", 1.5, 8.0);
tl.to("#camera", { scale: 1, x: 0, y: 0, duration: 1.1, ease: "power3.inOut" }, ">1.4");
```

`getBBox()` is layout-independent and deterministic — safe under the renderer.

## SVG transform pitfalls

- Always set `transformOrigin` explicitly on SVG tweens; default origin for SVG
  elements is the SVG canvas origin, not the element center.
- **Camera origin gotcha (verified)**: on SVG elements `transformOrigin: "0 0"`
  resolves to the element's *bounding box* top-left, not the canvas origin —
  camera framing drifts by `bbox × (1 − zoom)`. The template fixes this with
  `#cam-anchor`, an invisible 0.01px rect at (0,0) inside `#camera` that pins
  the group's bbox origin to the canvas origin. NEVER remove it, and keep all
  camera tweens on `transformOrigin: "0 0"`. Element-level pops/scales keep
  using `transformOrigin: "50% 50%"`.
- Scale node *groups* (`<g class="node">`), not individual rects, so icon +
  text move together.
- `gsap.from(...)` with `scale` needs `transformOrigin: "50% 50%"` or nodes fly
  in from the corner.
- Prefer transforms (x/y/scale) over animating `x=`/`cx=` attributes — but when
  needed, attribute tweens work: `gsap.to(el, { attr: { "stop-offset": ... } })`.

## Performance / determinism notes

- Glow = animate the **opacity of a glow-filtered copy** (or the filtered
  element), never tween `stdDeviation` per-frame (slow, can shimmer).
- Filters are expensive: ≤ ~12 filtered elements visible at once at 1080p.
- `will-change`/CSS transitions are useless here — the renderer screenshots
  seeked frames; only the GSAP timeline matters.
- Fonts: wait for `document.fonts.ready` before measuring text (the template's
  preview fallback already does); the renderer itself waits for fonts.
