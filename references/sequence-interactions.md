# Sequence-diagram interactions — direction-aware message animation

Mode for sequence diagrams where the story is the **interaction**: each
transaction animates in its travel direction — requests left→right,
replies right→left — one message in focus at a time.

## Getting the diagram

**Option A — hand-authored (best quality)**: the sequence pattern in
`references/diagram-svg-authoring.md` (participants as node cards, lifelines,
`msg-01…` in document order). Full theme/style control.

**Option B — Mermaid (fast path)**:

```bash
mmdc -i seq.mmd -o raw.svg -p pptr.json     # pptr.json: executablePath + --no-sandbox
python3 $SKILL_DIR/scripts/svg_prep.py --from mermaid-seq raw.svg -o scene.svg --wrap-camera
```

Normalization gives every message `id="msg-NN"` + `data-dir="ltr|rtl"`
(derived from x1/x2), labels `msgtext-NN`, activation bars `act-NN`,
lifelines `class="lifeline"`. Paste into `#camera`, restyle fills/strokes to
theme tokens (mermaid's gray defaults are not the quality bar).

**Option C — PlantUML**: `plantuml -tsvg seq.puml` renders fine but its markup
has no stable classes — use it as a *layout reference* and hand-annotate ids
(`--report` to inventory), or prefer Option A/B.

## The interaction choreography

Core rule: **animate each message in its travel direction** and give it
exclusive focus while it's "in flight":

```js
// generated (mermaid-seq) diagrams keep marker-end arrowheads, so draw-on
// shows the arrow early — use fade + directional slide instead of DrawSVG:
function playMessage(tl, n, at, dur = 1.0) {
  const id = `#msg-${String(n).padStart(2, "0")}`, label = `#msgtext-${String(n).padStart(2, "0")}`;
  const ltr = document.querySelector(id).dataset.dir !== "rtl";
  const slide = ltr ? -26 : 26;                       // slide FROM the sender side
  tl.to(".msg, .messageText", { opacity: 0.3, duration: 0.3 }, at)   // dim the rest
    .from(id,    { opacity: 0, x: slide, duration: 0.45, ease: "power2.out" }, at)
    .to(id,      { opacity: 1, duration: 0.1 }, at)
    .from(label, { opacity: 0, duration: 0.35 }, at + 0.25)
    .to(label,   { opacity: 1, duration: 0.1 }, at + 0.25);
  // pulse rides the line in the correct direction (lines support getPointAtLength)
  const line = document.querySelector(id), len = line.getTotalLength(), prog = { p: 0 };
  tl.set("#pulse-1", { opacity: 1 }, at + 0.15)
    .to(prog, { p: 1, duration: dur * 0.6, ease: "none", onUpdate() {
        const pt = line.getPointAtLength(prog.p * len);
        gsap.set("#pulse-1", { attr: { cx: pt.x, cy: pt.y } });
      } }, at + 0.15)
    .set("#pulse-1", { opacity: 0 }, at + 0.15 + dur * 0.6);
}
```

- Hand-authored diagrams (no markers, separate `.edge-head`s) may use DrawSVG
  draw-on instead of the slide — still source→destination direction.
- Replies (`.msg--reply`, dashed): keep the dash; slide from the right;
  consider a softer pulse (smaller r, no glow).
- Activation bars: grow when their first message lands —
  `tl.from("#act-NN", { scaleY: 0, transformOrigin: "50% 0%", duration: 0.3 })`.
- Strict order: messages play one at a time, top→bottom; un-dim everything
  in the final resolve.

## Camera

≤6 messages: static frame. Longer: **vertical scroll** (camera pans down with
the active message — `camPanTo(tl, centerX, msgY, 1.2…1.35)` per beat) and
finish with `camFitAll`. Tall sequences are the canonical oversized-scene
case (author beyond the canvas, set the canvas portrait if delivering 9:16).

## SRT sync

One cue = one message (or one request+reply pair): `playMessage(tl, n,
CUES[i].start + 0.15, CUES[i].dur)`, dim-release at `CUES[i].end`. All
voiceover-sync rules apply.

## RTL (Arabic) sequence diagrams

Mirror per `references/arabic-rtl.md`: first participant on the RIGHT;
requests travel right→left (`data-dir` handles slide direction automatically
for generated diagrams — verify the mermaid participant order is declared
right-first, or hand-author).
