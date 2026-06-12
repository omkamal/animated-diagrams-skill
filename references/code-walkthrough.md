# Python code walkthroughs — stylized, highlighted, SRT-driven

Mode for narrating long Python code: stylized editor panel, syntax-highlighted
source, a moving highlight bar, focus dimming, and vertical-scroll camera —
with beats driven by the narration SRT (see `references/voiceover-sync.md`).

## 1. Generate the stylized code block

```bash
python3 $SKILL_DIR/scripts/code_to_svg.py app/orders.py -o code_frag.svg \
        --font-size 28 --x 360 --y 230 [--start 40 --end 95]
```

Stdlib `tokenize`-based: emits one `<g class="code-line" id="line-N">` per
REAL source line (line numbers preserved — cues can say "line 52"), tokens in
`<tspan class="tok-kw|def|builtin|str|num|comment|deco|op">`, plus a ready
`#code-hl` highlight bar and a `<style>` block. Token colors are theme
tokens: `--tok-*` are tuned in `dark`, `blueprint`, `mono`; light themes use
the built-in fallbacks. **Best styles: `dark` (classic editor look), `mono`
(paper terminal), `blueprint`.** It prints the geometry you need:
`lineY(n) = Y + (n-START)*LH` and total block height.

## 2. Wrap it in the stylized editor panel (always)

Paste the fragment inside `#layer-labels` (inside `#camera`), wrapped in the
editor chrome — never show naked text on canvas:

```svg
<g id="code-panel" filter="url(#card-shadow)">
  <rect x="220" y="120" width="1480" height="<block+150>" rx="18"
        fill="var(--bg-raise)" stroke="var(--region-stroke)" stroke-width="1.5"/>
  <circle cx="262" cy="158" r="7" fill="#fb7185"/>
  <circle cx="288" cy="158" r="7" fill="#fbbf24"/>
  <circle cx="314" cy="158" r="7" fill="#34d399"/>
  <text x="960" y="166" text-anchor="middle" class="mono label" font-size="22">orders/process.py</text>
  <line x1="220" y1="186" x2="1700" y2="186" stroke="var(--region-stroke)" stroke-width="1"/>
</g>
<!-- code_frag.svg content here -->
```

For long files the panel extends past the canvas — that's the point: the
camera scrolls it (vertical-scroll pattern).

## 3. Choreograph: highlight + focus + scroll

```js
const LH = 44.8, Y0 = 230, START = 1;                  // from code_to_svg output
const lineY = n => Y0 + (n - START) * LH - FONT_SIZE;  // top of line n

// entrance: panel, then lines type in
tl.from("#code-panel", { opacity: 0, y: 18, duration: 0.5 }, 0.1)
  .from(".code-line", { opacity: 0, x: -14, stagger: 0.05, duration: 0.3 }, 0.4);

// FOCUS BEAT (repeat per cue): highlight lines a..b, dim the rest, camera there
function focusLines(tl, a, b, at, { zoom = 1.45, dur } = {}) {
  tl.set("#code-hl", { attr: { y: lineY(a), height: LH * (b - a + 1) } }, at)
    .to("#code-hl", { opacity: 0.16, duration: 0.3 }, at)
    .to(".code-line", { opacity: 0.3, duration: 0.4 }, at);
  for (let n = a; n <= b; n++) tl.to(`#line-${n}`, { opacity: 1, duration: 0.4 }, at);
  camPanTo(tl, 960, lineY(a) + (LH * (b - a + 1)) / 2, zoom, { at: at + 0.1, dur: 0.9 });
}
// release at the cue's end: restore opacity, camHome or pan to next block
```

With an SRT: one `focusLines(tl, a, b, CUES[i].start + 0.15)` per cue, held
until `CUES[i].end` (the voiceover-sync rules apply unchanged). Map cue text →
line ranges in the beat table ("the validation guard" → lines 12–13).

## Rules

- Highlight bar moves (tween `attr:{y,height}`) between consecutive focus
  beats instead of blinking off/on — continuity reads better.
- Dim to 0.3, never 0 — context must stay visible.
- Max zoom 1.6 on code; font ≥26px at 1080p (≥22px when zoomed 1.4+).
- Side callouts (annotations) live OUTSIDE the panel, connected by a thin
  `.edge` line to the highlighted range; pop them after the camera settles.
- Non-Python code: `code_to_svg.py` is Python-only — for other languages
  hand-write lines with `tok-*` tspans following the same structure.
