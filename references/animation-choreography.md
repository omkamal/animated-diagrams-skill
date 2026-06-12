# Animation choreography — the quality bar

"Stunning" is craft, not luck. Follow the narrative arc, the timing table, and
the don'ts. The composition should feel like a guided explanation, not a slideshow.

## Narrative arc (the five acts)

1. **Establish** (0 → ~1s): title fades in; region containers materialize
   (opacity + slight scale from 0.96).
2. **Build** (~1 → 3s): nodes enter with stagger, in *meaningful* order
   (request-flow order, not random) — `back.out(1.4)` gives a subtle pop.
3. **Connect** (~3 → 5s): edges draw on (DrawSVG) in flow order; arrowheads
   fade/scale in as each edge completes; labels follow.
4. **Flow / Focus** (~5 → 10s): the payoff — pulses ride the edges
   (MotionPath); camera zooms to the interesting subsystem while the HUD
   stays fixed; highlight active nodes with a glow or stroke brighten.
5. **Resolve** (last ~2s): camera returns to full view; everything settled;
   **hold the complete diagram ≥ 1s** (last frame = poster frame).

Default total: 8–20s. Match `data-duration` on `#root` to the timeline total
(`tl.duration()`); add a final `tl.to({}, { duration: X })` to pad the hold.

## Timing table

| Move | Duration | Ease |
|---|---|---|
| Title / HUD fade | 0.5–0.7s | `power2.out` |
| Region entrance | 0.6–0.8s, stagger 0.12s | `power2.out` |
| Node entrance | 0.5–0.6s, stagger 0.06–0.12s | `back.out(1.4)` |
| Edge draw-on | 0.4–0.8s each, stagger 0.1–0.25s | `power1.inOut` |
| Arrowhead pop | 0.2–0.3s | `back.out(2)` |
| Label fade | 0.3–0.4s | `power2.out` |
| Pulse along edge | 0.9–1.4s per hop | `none` (linear) |
| Camera move | 1.0–1.4s | `power3.inOut` |
| Emphasis (glow/scale) | 0.3s in, 0.5s out | `expo.out` / `power2.in` |

Easing rules: entrances `power2.out`/`back.out`, camera always `power3.inOut`,
**`linear`/`none` only for particles** riding paths. Never animate everything at
once — at most two concurrent "threads" of motion.

## Camera grammar

- Animate only `#camera` (scale + x/y, `transformOrigin: "0 0"`); HUD stays put.
- Max zoom 1.6×; one camera move per act; always return to full view at the end.
- Zoom-to-target recipe is in `gsap-svg-techniques.md` (compute from getBBox).
- For diagrams ≤ 6 nodes skip camera moves entirely — they add nothing.

## Continuous life (bounded!)

After an element's entrance, it shouldn't freeze:

- Pulses repeat their journey: `repeat: 2–4` **inside** the master timeline —
  `repeat: -1` is forbidden (the renderer needs a finite timeline).
- Dotted `edge--flow` lines drift: tween `stroke-dashoffset` by a few cycles
  over the remaining duration (linear).
- A "working" node can breathe: one or two subtle glow pulses (opacity of a
  glow-filtered copy), not constant blinking.

## Emphasis patterns

- **Active node**: brighten stroke + glow filter copy fades in, slight 1.04 scale.
- **Path walk**: dim everything (`opacity: 0.35` on a group), then restore
  elements along the narrated path as a pulse passes them.
- **Counter/metric**: animate a `<text>` with `snap: { textContent: 1 }` and an
  object tween — bounded duration.

## Don'ts

- No rotation gimmicks, no bouncing logos, no rainbow palettes.
- No motion without meaning: every move should explain structure or flow.
- No simultaneous everything; no entrance longer than 4s total.
- No `linear` ease on UI moves (only particles).
- No infinite repeats, no `Date.now()`, no `setInterval`, no CSS
  animations/transitions for anything that moves (renderer seeks the GSAP
  timeline only).
- Don't end mid-motion — resolve and hold.

## Pre-render checklist

- [ ] Entrance order = narrative order (not DOM accident)
- [ ] All edges draw source → destination
- [ ] Arrowheads appear only as their edge completes
- [ ] Pulses glide visibly (≥0.9s per hop), glow on
- [ ] Camera (if used) returns home; HUD never moves
- [ ] `tl.duration()` == `data-duration`; final hold ≥ 1s
- [ ] Text legible at 50% playback size (≥22px labels at 1080p)
