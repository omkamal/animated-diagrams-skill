# Semantic SVG authoring for animation

The SVG is the *contract* between scene and choreography. Every element that will
animate gets a stable id and a class; everything lives in the right layer so
z-order and group animations work.

## The contract

```
<g id="camera">                 ← ALL pan/zoom animates this group only
  <g id="layer-regions">  …     ← containers (VPC, zones, swimlanes) — bottom
  <g id="layer-edges">    …     ← connection paths + arrowheads
  <g id="layer-nodes">    …     ← node cards/icons
  <g id="layer-labels">   …     ← free-standing annotations
  <g id="layer-particles">…     ← data pulses (top)
</g>
<g id="hud">              …     ← title/legend — OUTSIDE camera, stays fixed
```

### Naming scheme

| Element | id | class |
|---|---|---|
| Node | `node-<name>` | `node` (+ modifier e.g. `node--db`) |
| Edge | `edge-<src>-<dst>` | `edge` (solid) or `edge--flow` (dotted data line) |
| Arrowhead | `head-<src>-<dst>` | `edge-head` |
| Region | `region-<name>` | `region` |
| Label | `label-<name>` | `label` |
| Pulse | `pulse-<n>` | `pulse` |
| Sequence message | `msg-01`, `msg-02`… (document order) | `msg` |

### Edge rules (critical for animation)

- Edges are stroked `<path>` elements, `fill="none"` — DrawSVG animates strokes only.
- **Do NOT use `marker-end` for arrowheads** — markers are visible the moment the
  path exists, before DrawSVG draws it (verified). Instead add a small separate
  `<path class="edge-head">` triangle at the end point, rotated to the edge
  direction, and fade/scale it in as the edge draw completes.
- Draw direction matters: author the `d` from source to destination so
  `drawSVG: "0%" → "100%"` grows the right way.
- Curves: prefer gentle cubic Béziers (`C`) or rounded orthogonal routes over
  straight lines; they read better and MotionPath pulses glide naturally.
- Dotted "data flow" lines use `class="edge--flow"` (dasharray from theme) and are
  animated by `stroke-dashoffset`, never DrawSVG (DrawSVG overrides dasharray).

### Node card pattern (cloud-arch services)

```svg
<g id="node-api" class="node" filter="url(#card-shadow)">
  <rect x="800" y="430" width="280" height="150"/>   <!-- NO rx/stroke attrs: the
       style preset's tokens (--radius-node, --stroke-node, fonts) drive them -->
  <use href="#clip-logos-aws-lambda" x="828" y="468" width="56" height="56"/>
  <!-- vendor logo (fetched, keeps own colors); generic alternative:
       <use href="#icon-fa-bolt" … color="var(--c-orange)"/> -->
  <text x="908" y="492" font-size="30" font-weight="600">Checkout API</text>
  <text x="908" y="528" class="label" font-size="22">AWS Lambda</text>
</g>
```

Style presets control the shape language (corner radius, stroke widths,
dashes, fonts) via CSS tokens — see `references/style-presets.md`. To give a
node a *category color*, use an inline **style** (it must beat the theme's CSS
rule — a plain `stroke="…"` attribute has zero specificity and silently
loses): `<rect … style="stroke: var(--c-green)"/>`. Never override
radius/weight/font.

### Icon strategy (defaults)

1. **Generic/service icons → Font Awesome 6** (DEFAULT). An offline starter
   pack ships in `assets/icons/fa6-common.svg` (26 symbols, ids
   `icon-fa-<name>`: server, database, cloud, gears, chart-line,
   shield-halved, user, users, globe, lock, envelope, mobile-screen, desktop,
   code, bolt, network-wired, sitemap, robot, file-lines, magnifying-glass,
   bell, key, layer-group, scale-balanced, arrows-rotate, box-archive) —
   copy needed `<symbol>`s into `<defs>`, then
   `<use href="#icon-fa-database" … color="var(--c-blue)"/>`. Any other FA6
   icon: `fetch_clipart.mjs --project DIR fa6-solid:<name>`. FA6 Free is
   CC-BY 4.0 — note attribution when the user publishes.
2. **Vendor/product nodes → official logos** (DEFAULT for branded tech):
   fetch from `logos:` / `devicon:` — full-color official marks, used
   nominatively (labeling the real product). Per-service cloud icons exist:
   `logos:aws-lambda`, `logos:aws-s3`, `logos:aws-dynamodb`, `logos:aws-ec2`,
   `logos:aws-api-gateway`, `logos:aws-cloudfront`, `logos:aws-rds`,
   `logos:aws-sqs`, `logos:google-cloud`, `logos:microsoft-azure`, plus
   `logos:kafka`, `logos:redis`, `logos:nginx`, `logos:postgresql`,
   `logos:docker-icon`, `logos:kubernetes`, `devicon:python`… Color logos
   keep their own colors — never recolor, and give them a white/neutral card
   chip on dark themes for contrast.
3. **Bundled stylized line glyphs** (`generic.svg`, `cloud-aws/gcp/azure.svg`,
   48×48 `stroke="currentColor"`) — offline fallback, and the right choice
   when the user wants a fully theme-consistent / hand-drawn look (`sketch`,
   `blueprint`, `wireframe`) or a trademark-free deliverable.

## Per-type patterns

### Cloud architecture

- Regions (VPC / subnet / account boundary) are dashed rounded rects in
  `layer-regions` with a small `region-title` text in the top-left.
- Lay out left→right in request-flow order (client → edge → compute → data).
- Grid: snap node centers to a ~80px grid; min 90px gap between cards;
  edges leave/enter card midpoints on the facing side.
- Color by category, consistently: compute `--c-orange`, data `--c-blue`/`--c-green`,
  network/edge `--c-violet`, messaging `--c-rose`, security `--c-cyan`.

### Sequence diagrams

- Participants: node cards in a row at top (`node-<name>`), each with a vertical
  `<line class="lifeline">` below, all in `layer-nodes`.
- Messages: horizontal edges `msg-01`, `msg-02`… in strict top-to-bottom document
  order, each with its label above the line; replies use dashed strokes.
- Activation bars: thin `<rect class="activation">` on lifelines, revealed
  (scaleY from 0, `transformOrigin: "50% 0%"`) when their first message arrives.
- Choreography: messages animate strictly in order, one at a time
  (draw edge → pop label → extend activation), ~0.7s per message.

### Flowcharts

- Shapes: rounded rect = step, diamond = decision, stadium (`rx` = height/2)
  = start/end, parallelogram = I/O.
- Decision branches: label edges `edge-<decision>-yes` / `-no` with small
  labels near the diamond exit.
- Swimlanes are regions; keep lane headers in `layer-regions`.
- Choreography: walk the happy path first (sequential node+edge reveals),
  then reveal alternate branches dimmed (opacity 0.45), optionally
  brighten a branch while a pulse walks it.

## Layout assist for dense graphs (≥ ~10 nodes)

Hand layout beats generated layout for beauty — use assist only to get
coordinates, then restyle.

```bash
# Graphviz
dot -Tsvg graph.dot -o raw.svg
python3 $SKILL_DIR/scripts/svg_prep.py --from graphviz raw.svg -o scene.svg --wrap-camera
python3 $SKILL_DIR/scripts/svg_prep.py --report scene.svg     # id inventory for the timeline

# Mermaid — MUST disable htmlLabels (foreignObject text can't be animated/themed)
echo '{"flowchart":{"htmlLabels":false}}' > mcfg.json
printf '{"executablePath": "%s", "args": ["--no-sandbox"]}\n' \
  "$(ls -d ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome | tail -1)" > pptr.json
mmdc -i graph.mmd -o raw.svg -c mcfg.json -p pptr.json
python3 $SKILL_DIR/scripts/svg_prep.py --from mermaid raw.svg -o scene.svg --wrap-camera
```

After prep: paste the SVG inner content into the composition's `#camera` group,
re-map fills/strokes to theme classes/vars, replace generated label fonts with
Inter, and add `edge-head` arrowheads. Generated output is a starting point —
the quality bar still applies.

## Recreating from an input image (PNG)

Read the image, then **rebuild, never trace**: enumerate nodes (name, type,
grouping), edges (direction, label), and regions; choose the matching per-type
pattern above; lay out on the grid with consistent spacing even if the original
was messy. Match the original's information, not its geometry.
