# Output formats & verification

## Deliverable matrix (default set: MP4 + GIF + SVG + interactive HTML)

| Format | How | When |
|---|---|---|
| **MP4** | `render.mjs` → hyperframes (h264, 1080p30, quality `standard`) | always (default) |
| **GIF** | `render.mjs --gif` (ffmpeg palettegen from the MP4, 960px @ 15fps) | always (default) — READMEs, PRs, chat |
| **SVG** | `render.mjs --svg` (or `export_svg.mjs`) — static **resolved-state** diagram, theme CSS + fonts embedded, no scripts | always (default) — docs, wikis, design tools |
| **Interactive HTML** | `inline_html.mjs` → single self-contained file, plays the animation with play/pause/scrub | always (default) — the "animated SVG in the browser" artifact |
| **WebM** | `render.mjs --webm` (vp9 from MP4) | web embeds, smaller files |
| **Transparent WebM/MOV** | `hyperframes render --format webm\|mov` directly (re-render, alpha kept) | overlays on other videos |
| **PNG sequence** | `hyperframes render --format png-sequence` | After Effects / Nuke ingest |

Why the SVG is static: embedding the GSAP runtime in a bare `.svg` is
unreliable — gsap's SVG transform/motion-path math requires `document.body`,
which standalone SVG documents lack (verified: pulses pin to the origin and
seeking throws). The export lifts authored `opacity="0"` everywhere except
`#layer-particles`, so it shows the complete resolved diagram (HUD visible,
transient pulses hidden). The animated single-file artifact is the
interactive HTML.

Resolution: composition-defined (template default 1920×1080). Vertical
(1080×1920) via `new_project.sh --width 1080 --height 1920`. 4K: render with
`--resolution landscape-4k` (DPR upscale of a 1920×1080 composition — crisp
because everything is vector).

## Standard render command

```bash
node $SKILL_DIR/scripts/render.mjs --project ./animated-svg-<slug> \
  --output ./animated-svg-<slug>/renders/<slug>.mp4 \
  --gif --svg --snapshots 5 --probe [--webm]
node $SKILL_DIR/scripts/inline_html.mjs --project ./animated-svg-<slug>
```

All outputs land under the project dir in the **calling directory** — never
inside the skill directory.

## Mandatory verification (every render)

1. `--probe` passes: sane size, duration ≈ `data-duration`.
2. **Read `snapshots/contact-sheet.jpg`** (one image, all key frames):
   - first frame = clean pre-entrance state (no stray arrowheads/particles)
   - middle frames show progression (draws, pulses, camera)
   - last frame = complete resolved diagram (this is the poster frame)
3. Fix and re-render until the contact sheet looks right — typical issues:
   overlap/collision, illegible labels, dead time (long static gaps), motion
   not matching narrative order.
4. Iterating on one moment? `--at 4.2,4.6,5.0` beats re-rendering everything.

## Manual ffmpeg recipes (what render.mjs runs)

```bash
# high-quality GIF
ffmpeg -y -i in.mp4 -vf "fps=15,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" out.gif
# WebM (vp9)
ffmpeg -y -i in.mp4 -c:v libvpx-vp9 -crf 32 -b:v 0 -an out.webm
# poster frame
ffmpeg -y -sseof -0.1 -i in.mp4 -frames:v 1 poster.png
```

File-size guidance @1080p30: MP4 ~50–120 KB/s of animation; GIF balloons fast —
keep ≤ 12s or drop to 720px/12fps; interactive HTML ≈ 200–400 KB total.
