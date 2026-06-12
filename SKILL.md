---
name: animated-svg
description: This skill should be used when the user asks to "animate this diagram", "create an animated architecture diagram", "animated AWS/GCP/Azure diagram", "animated sequence diagram", "animated flowchart", "turn this PNG/SVG into an animation", "schematic animation", "data flow animation", "animate this SVG", "show the diagram style gallery", "illustrate a concept with cliparts/emojis", "animated concept illustration", "animate a large flow with pan and zoom", "code walkthrough animation", "Arabic animated diagram", "رسم متحرك", "animate this with my voiceover/SRT", "sync animation to narration timestamps", "animated Python code walkthrough", "highlight code as I narrate", "animate this sequence diagram", "animate PlantUML/Mermaid sequence", "make a video explaining this architecture", or wants any 2D technical diagram (cloud architecture, sequence, flowchart, network/data-flow schematic, technical illustration, concept illustration) brought to life as a video. Creates visually stunning animated schematics from a textual description OR an input diagram image (PNG or SVG), in one of 12 style presets (light/white default, also dark, hand-drawn sketch, corporate, pastel, terminal, editorial serif, bold geometric, glass, brutalist, blueprint, wireframe — live gallery included), any aspect ratio including portrait, with optional transparent background. Can illustrate with 200k+ open-licensed cliparts/emojis fetched from Iconify (Noto, Twemoji, OpenMoji, Lucide, Tabler…) into the working directory, and ships a camera rig with 6 pan/zoom patterns (guided tour, follow-cam, vertical scroll, conveyor, pulse-zoom, reveal-pan) for flows larger than the canvas. Full Arabic/RTL support (Cairo, Amiri, Tajawal, Reem Kufi fonts; mirrored right-to-left flows and arrows via --lang ar) and a voice-over sync mode: given an SRT/VTT narration script, every animation beat fires exactly at its cue's timestamp, holds while its narration plays, and the audio is muxed into the MP4. Authors semantic SVG, choreographs it with GSAP 3 timelines (DrawSVG edge draw-on, MotionPath data-flow pulses, camera pan/zoom), and delivers MP4 + GIF + SVG by default (plus WebM and a self-contained interactive HTML with scrubber), rendered deterministically via HyperFrames. All outputs are created in the calling directory.
---

# animated-svg — animated 2D schematic diagrams

Turn a description or an existing diagram (PNG/SVG) into a choreographed,
cinema-quality animation: semantic SVG scene + GSAP 3 timeline + HyperFrames
deterministic rendering (HTML → frame-seeked headless Chrome → FFmpeg).

## Companion agent

For **batch jobs or delegation** (multiple artifacts with one consistent
style, or another skill needing an animation produced) launch the
**`diagram-animator`** agent (`agents/diagram-animator.md`, installed at
`~/.claude/agents/`) via the Agent tool — it operates this skill end-to-end,
decides unspecified options (mode/style/icons/duration), keeps a batch
visually consistent, and returns a manifest of MP4/GIF/SVG/interactive-HTML
(+ alpha WebM) paths, all under one subdirectory of the calling directory.

## Paths

```bash
SKILL_DIR=~/.claude/skills/animated-svg          # resolve via this SKILL.md's location
HF=$SKILL_DIR/node_modules/.bin/hyperframes
```

**Setup gate**: if `$HF` does not exist, run `bash $SKILL_DIR/scripts/setup.sh`
first (installs hyperframes + gsap, vendors GSAP plugins, ensures Chrome,
smoke-renders). One-time, then everything is offline.

## Workflow

### 1. Classify the request

- Diagram type: cloud-arch / sequence / flowchart / network / illustration.
- Style: one of 12 presets — **`light` (default)**, `dark`, `blueprint`,
  `sketch`, `corporate`, `pastel`, `mono`, `editorial`, `vivid`, `glass`,
  `brutalist`, `wireframe` — each is a palette + fonts + shapes + motion
  language. Read `references/style-presets.md` before choosing; the user can
  browse the live gallery at `$SKILL_DIR/assets/gallery/styles-gallery.html`.
- Background: white/light by default; `--transparent` for a transparent
  canvas (deliver via SVG / interactive HTML / webm-mov; MP4 can't hold alpha).
- Resolution: 1920×1080 default; 1080×1920 portrait for shorts/reels;
  1080×1080 square. Duration: 8–20s unless asked.

### 2. Acquire the SVG scene → read `references/diagram-svg-authoring.md`

- **Text input**: author semantic SVG by hand (the reference has per-type
  patterns and the id/class naming contract). For dense graphs (≥ ~10 nodes)
  use the Graphviz/Mermaid layout-assist appendix + `scripts/svg_prep.py`.
- **Input SVG**: run `python3 $SKILL_DIR/scripts/svg_prep.py --report` on it,
  add missing `node-*`/`edge-*` ids, restyle to theme tokens.
- **Input PNG**: Read the image, enumerate nodes/edges/regions, then *rebuild*
  cleanly on the design system — never trace pixel geometry.

### 3. Scaffold a project (ALWAYS in the calling directory)

**All project directories, renders, and deliverables are created in the
user's current working directory — NEVER inside `$SKILL_DIR`.** The skill
directory is read-only tooling; outputs belong to the user's workspace.

```bash
bash $SKILL_DIR/scripts/new_project.sh <slug> [--theme light] [--width 1920] \
     [--height 1080] [--duration 12] [--transparent]
```

Creates `./animated-svg-<slug>/` with `index.html` (composition skeleton:
camera rig + layers + HUD + a marked inline TIMELINE script), merged
`theme.css`, vendored GSAP, fonts. Edit one file — **index.html**: SVG scene
into the layer groups, choreography into the inline TIMELINE script.
**Default icons**: Font Awesome 6 for generic/service icons (offline pack
`$SKILL_DIR/assets/icons/fa6-common.svg`, ids `icon-fa-*`; others via
`fetch_clipart.mjs … fa6-solid:<name>`) and **official `logos:`/`devicon:`
marks for vendor products** (AWS/GCP/Azure services, Kafka, Redis, Postgres…
— fetched, keep their own colors). Bundled stylized glyphs in
`assets/icons/*.svg` remain the offline/trademark-free fallback (best for
sketch/blueprint/wireframe styles).
The timeline MUST stay inline — `hyperframes snapshot` does not execute
external local scripts (verified), and snapshots are the verification loop.

### 4. Choreograph → read `references/animation-choreography.md` + `references/gsap-svg-techniques.md`

Five acts: Establish → Build (staggered node entrances) → Connect (DrawSVG
edge draw-on + separate arrowhead pops) → Flow/Focus (MotionPath pulses,
camera zoom) → Resolve (return + hold ≥1s). **Match the style's motion
language** (per-style timing/easing rules in `references/style-presets.md` —
e.g. corporate never bounces, mono uses stepped reveals, wireframe fades
dashed edges instead of drawing them). Keep `data-duration` ==
`tl.duration()`. Hard rules: paused timeline on `window.__timelines["main"]`,
no wall-clock motion, bounded repeats only, arrowheads are separate
`.edge-head` elements (never `marker-end`).

### 5. Render + verify (mandatory loop)

```bash
node $SKILL_DIR/scripts/render.mjs --project ./animated-svg-<slug> \
  --output ./animated-svg-<slug>/renders/<slug>.mp4 \
  --gif --svg --snapshots 5 --probe
```

Then **Read `snapshots/contact-sheet.jpg`** and check: clean first frame,
visible progression, complete resolved last frame, legible labels, no
overlaps. Iterate (use `--at t1,t2` to zoom into one moment) until it meets
the checklist in `references/animation-choreography.md`. For live iteration
with the user: launch `$HF preview` from the project dir with
`run_in_background: true` (it is a long-running server).

### 6. Deliver (default: MP4 + GIF + SVG, plus interactive HTML)

```bash
node $SKILL_DIR/scripts/inline_html.mjs --project ./animated-svg-<slug>
```

Standard deliverables in `./animated-svg-<slug>/renders/` (the calling
directory tree, never the skill dir): **`<slug>.mp4`** (video),
**`<slug>.gif`** (embeds), **`<slug>.svg`** (static resolved diagram —
scalable, fonts embedded), **`<slug>.interactive.html`** (the animation with
play/scrub controls, single file). Report all paths + the probe summary.
WebM, transparent overlays, 4K, PNG sequences: `references/output-formats.md`.

## Concept illustrations — cliparts, emojis, icon libraries

For illustrating *ideas* (not just architectures) — or whenever a request
mentions cliparts/emojis/illustrations — read
`references/concept-illustrations.md`. Search and fetch from the Iconify
network (200k+ open-licensed icons/emojis: noto, fluent-emoji, twemoji,
openmoji, lucide, tabler, game-icons…) **into the working project dir**:

```bash
node $SKILL_DIR/scripts/fetch_clipart.mjs --search "rocket"            # discover
node $SKILL_DIR/scripts/fetch_clipart.mjs --project ./animated-svg-<slug> \
     noto:rocket lucide:database          # downloads + injects <symbol>s
# then: <use href="#clip-noto-rocket" x=".." y=".." width="180" height="180"/>
```

Color emoji (noto = safe Apache-2.0 default) keep their own colors; line sets
(lucide/tabler) take `color="var(--c-…)"`. Network is touched ONLY at
authoring time — renders stay offline. Scene patterns (hero metaphor, idea
strip, concept map, badges) and license table are in the reference.

## Large flows — camera pan/zoom (control flow, sequence, code walkthroughs)

When a flow won't fit comfortably (> ~8 nodes, long sequences, code
navigation), author the scene **larger than the canvas** and drive the
camera — read `references/camera-large-flows.md`. Every scaffolded
`index.html` includes the inline camera rig:

```js
camFit(tl, "#node-x", { at, dur, zoom? })   // center+zoom to any group (auto-fit)
camFitAll(tl, { at })                        // fit the whole oversized scene
camPanTo(tl, cx, cy, z, { at, dur })         // pan to a scene point
camFollow(tl, "#edge-a-b", { at, dur, zoom })// track a path with the pulse
camHome(tl, { at })                          // reset
```

Six named patterns (pick by diagram shape, demos in the gallery's "Camera
patterns" section): **guided tour** (hop stop-by-stop), **follow-cam** (ride
with the token), **vertical scroll** (sequence diagrams / code, read
top→down), **conveyor** (wide pipelines, constant slide), **pulse-zoom**
(overview ↔ detail dives), **reveal-pan** (cinematic first reveal). Always
end on `camFitAll` + ≥1.2s hold. Keep `#cam-anchor` in `#camera` (it pins the
transform origin — removing it breaks all framing math).

## Arabic & RTL — العربية

For Arabic content (or any RTL request) read `references/arabic-rtl.md` and
scaffold with `--lang ar`: it loads the Arabic fonts (Cairo default; Amiri
serif, Tajawal, Reem Kufi display — all bundled) and applies RTL text rules
(direction, `unicode-bidi: plaintext`, zero letter-spacing). **Geometry must
be mirrored by the author**: flows run right→left top→bottom, entry node on
the RIGHT, edges drawn right→left, arrowheads point LEFT, region titles
top-right, camera conveyor/reveal pan leftward. Gallery has live Arabic cards.

## Voice-over sync — SRT-timed beats

When the user provides a narration script with timestamps (SRT/VTT) — with or
without a diagram idea, with or without an audio file — read
`references/voiceover-sync.md` and follow it exactly:

```bash
python3 $SKILL_DIR/scripts/srt_to_cues.py narration.srt   # cue table + CUES js
```

Each cue = one beat: its element/camera action fires at `cue.start` (never
before), holds focus while that narration plays, releases at `cue.end`; the
next part appears only at the next cue's start. Embed the narration audio as
`<audio id="narration" class="clip" src="./audio/x.mp3" data-start="0"
data-duration="…" data-track-index="2">` — the **id is mandatory** or the
render is silent (verified) — and the MP4 carries the voice-over (h264+aac).
Verification is boundary-based: snapshot at `start−0.1` and mid-cue of every
cue; the pre-start frame must NOT contain that cue's content.

## Code walkthroughs — stylized Python navigation

For narrating Python code (especially long files, especially with an SRT)
read `references/code-walkthrough.md`:

```bash
python3 $SKILL_DIR/scripts/code_to_svg.py file.py -o code_frag.svg \
        --font-size 28 --x 360 --y 230 [--start N --end M]
```

Tokenized, theme-colored source (`tok-*` tspans; `--tok-*` palettes tuned in
dark/blueprint/mono — best styles for code), one `id="line-N"` group per real
source line, plus a `#code-hl` highlight bar. ALWAYS wrap in the stylized
editor panel (chrome dots + filename tab). Choreography: highlight bar
glides between line ranges, non-focused lines dim to 0.3, camera
vertical-scrolls — each focus beat driven by its SRT cue when narrated.

## Sequence-diagram interactions

For sequence diagrams where transactions matter, read
`references/sequence-interactions.md`. Generate via Mermaid
(`mmdc` → `svg_prep.py --from mermaid-seq` gives `msg-NN` ids +
`data-dir="ltr|rtl"`), PlantUML (layout reference), or hand-author. Core
rule: **each message animates in its travel direction** — requests slide/draw
left→right, replies right→left (dashed) — one message in exclusive focus
(others dim to 0.3) with a pulse riding the line; activation bars grow as
messages land. Long sequences use the vertical-scroll camera; one SRT cue per
message when narrated. Generated diagrams: fade+directional-slide (their
`marker-end` arrows break DrawSVG); hand-authored may DrawSVG.

## Quality bar (non-negotiables)

- Entrance order tells the story (request-flow order, never DOM accident).
- Edges draw source→destination; arrowheads pop as the draw lands.
- Something always alive after entrance: pulses (bounded repeats) or drifting
  dotted flow lines — but never everything at once.
- Camera moves only for >6-node diagrams; max 1.6×; always returns home; HUD fixed.
- Labels ≥22px at 1080p; theme tokens only (no ad-hoc colors, no hardcoded
  rx/stroke-width/font-family on standard classes); end hold ≥1s.
- Light/white background is the default; honor the chosen style's motion
  language — never apply bouncy motion to corporate/editorial styles.

## Resources

| Path | What |
|---|---|
| `references/style-presets.md` | the 12 styles: palette/fonts/shapes/motion specs, aspect + transparency guidance |
| `references/concept-illustrations.md` | clipart/emoji workflow (Iconify search+fetch), license table, concept-scene patterns |
| `references/camera-large-flows.md` | camera rig API + the 6 pan/zoom patterns for large flows |
| `references/arabic-rtl.md` | Arabic fonts, RTL typography rules, mirrored flow geometry |
| `references/voiceover-sync.md` | SRT-driven beats, audio embedding contract, boundary verification |
| `references/code-walkthrough.md` | stylized Python code mode: code_to_svg.py, editor panel, highlight/focus/scroll |
| `references/sequence-interactions.md` | sequence mode: mermaid-seq normalization, direction-aware message animation |
| `assets/gallery/styles-gallery.html` | live animated gallery of all 12 styles (open in a browser; show the user) |
| `references/diagram-svg-authoring.md` | semantic SVG contract, per-type patterns, layout assist, PNG recreation |
| `references/animation-choreography.md` | narrative arc, timing/easing tables, camera grammar, checklist |
| `references/gsap-svg-techniques.md` | DrawSVG/MotionPath/Morph cookbooks, camera-rig zoomTo, pitfalls |
| `references/hyperframes-rendering.md` | determinism contract, verified CLI, troubleshooting |
| `references/output-formats.md` | deliverables matrix, ffmpeg recipes, verification procedure |
| `assets/icons/fa6-common.svg` | DEFAULT icon pack — 26 Font Awesome 6 symbols (`icon-fa-*`), offline, CC-BY 4.0 |
| `assets/icons/*.svg` | stylized icon `<symbol>` libraries (generic, AWS, GCP, Azure roles) — offline/trademark-free fallback |
| `assets/themes/*.css` | the 12 style presets (light default) |
| `scripts/` | setup.sh · new_project.sh · render.mjs · export_svg.mjs · inline_html.mjs · svg_prep.py · fetch_clipart.mjs · srt_to_cues.py · code_to_svg.py |
