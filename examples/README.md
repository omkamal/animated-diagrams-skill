# Sample outputs

Real, unedited deliverables produced by the skill's render pipeline — committed
so you can see exactly what you get before installing anything.

## `architecture-demo/` — cloud architecture animation

A "Serverless Checkout" AWS request path (Users → CDN → Load Balancer →
Lambda → DynamoDB) in the **dark** style, with staggered node entrances,
DrawSVG edge draw-on, a MotionPath request pulse riding the whole path, and a
camera zoom into the compute + data pair.

| File | What it is |
|---|---|
| [`index.html`](architecture-demo/index.html) | The **authoring source** — the one file you edit: semantic SVG scene + inline GSAP timeline. Read it to see how a project is written. |
| [`renders/demo.mp4`](architecture-demo/renders/demo.mp4) | Primary video deliverable (h264, 1920×1080 @ 30 fps, 14 s). |
| [`renders/demo.svg`](architecture-demo/renders/demo.svg) | Static resolved-state SVG — scalable, fonts embedded, drop into docs/wikis. |
| [`renders/demo.interactive.html`](architecture-demo/renders/demo.interactive.html) | **Self-contained** interactive player — download and open in any browser: play/pause + scrub bar, no dependencies. |

The animated GIF deliverable for this same scene is the hero at the top of the
[main README](../README.md) (`docs/media/hero.gif`).

> `index.html` references its scaffold-local `theme.css` / `vendor/` / `fonts/`
> directories, so it is committed here as a *source listing* to read — to run it
> live, scaffold a project with `scripts/new_project.sh` and copy the file in.

## `concept-demo/` — concept illustration + voice-over sync

A minimal concept strip (💡 Idea → Build → 🚀 Launch) built with **cliparts
fetched from Iconify** (noto color emojis keep their own colors, the lucide
database icon takes the theme color), animated with camera moves, and — in the
narrated MP4 — every beat fired on its SRT cue with the **narration audio muxed
into the video** (h264 + aac).

| File | What it is |
|---|---|
| [`index.html`](concept-demo/index.html) | Authoring source — note the `<symbol id="clip-*">` defs injected by `fetch_clipart.mjs` and the `<audio id="narration">` clip. |
| [`renders/concept-narrated.mp4`](concept-demo/renders/concept-narrated.mp4) | The narrated render — **turn your sound on**: animation beats land exactly on the narration cues. |

The silent GIF version is embedded in the main README's concept-illustration
section (`docs/media/concept.gif`).

## `code-walkthrough/` — Python code walkthrough

A 15-line `process_order()` function in the **dark** style: a stylized editor
panel (chrome dots + filename tab), real syntax highlighting from
`scripts/code_to_svg.py`, a highlight bar that glides between line ranges
(guard → loop → out-of-stock raise → reserve+charge), focus-dimming of inactive
lines, and a camera that zooms to each focused range.

| File | What it is |
|---|---|
| [`index.html`](code-walkthrough/index.html) | Authoring source — note the `code_to_svg.py` fragment (`<g class="code-line" id="line-N">`, `tok-*` tspans, `#code-hl` bar) and the `focus(a, b, at)` beat helper. |
| [`renders/code.mp4`](code-walkthrough/renders/code.mp4) | The walkthrough video (1920×1080, 13 s). |
| [`renders/code.interactive.html`](code-walkthrough/renders/code.interactive.html) | Self-contained interactive player. |

GIF in the main README's [code-walkthrough section](../README.md) (`docs/media/code-walkthrough.gif`).

## `sequence-diagram/` — login & token issuance

A hand-authored sequence diagram (Client → API Gateway → Auth Service →
Database) in the **light** style: lifelines, activation bars that grow as calls
land, and direction-aware messages — solid requests draw left→right, dashed
replies come back right→left — each in exclusive focus while in flight.

| File | What it is |
|---|---|
| [`index.html`](sequence-diagram/index.html) | Authoring source — participant cards, `lifeline` lines, `msg-NN`/`head-NN` with `data-dir`, `activation` bars, and the `play(n, at)` message beat. |
| [`renders/seq.mp4`](sequence-diagram/renders/seq.mp4) | The sequence video (1920×1080, 14 s). |
| [`renders/seq.interactive.html`](sequence-diagram/renders/seq.interactive.html) | Self-contained interactive player. |

GIF in the main README's [sequence-diagram section](../README.md) (`docs/media/sequence.gif`).

## `arabic-architecture/` — RTL data-flow (العربية)

**رحلة الطلب** — an Arabic right-to-left architecture in the **corporate** style:
المستخدم → البوابة → الخدمة → قاعدة البيانات. Note the mirrored geometry — the
entry node is on the **right**, edge paths are authored right→left so DrawSVG
grows leftward, arrowheads point **left**, and the region title is anchored
top-right. Scaffolded with `--lang ar`.

| File | What it is |
|---|---|
| [`index.html`](arabic-architecture/index.html) | Source — `<html lang="ar" dir="rtl">`, the Arabic overlay appended to `theme.css`, mirrored node/edge coordinates. |
| [`renders/ar-arch.mp4`](arabic-architecture/renders/ar-arch.mp4) | The video (1920×1080, 13 s). |
| [`renders/ar-arch.interactive.html`](arabic-architecture/renders/ar-arch.interactive.html) | Self-contained interactive player. |

## `arabic-concept/` — RTL concept illustration (العربية)

**من الفكرة إلى الإطلاق** — an Arabic concept strip in the **dark** style
(فكرة → بناء → إطلاق) built from **noto color-emoji cliparts** fetched by
`fetch_clipart.mjs`, flowing right→left with left-pointing connectors.

| File | What it is |
|---|---|
| [`index.html`](arabic-concept/index.html) | Source — injected `<symbol id="clip-noto-*">` emoji defs and the RTL idea-strip layout. |
| [`cliparts/`](arabic-concept/cliparts/) | The fetched noto emoji SVGs (Apache-2.0). |
| [`renders/ar-concept.mp4`](arabic-concept/renders/ar-concept.mp4) | The video (1920×1080, 11 s). |
| [`renders/ar-concept.interactive.html`](arabic-concept/renders/ar-concept.interactive.html) | Self-contained interactive player. |

GIFs in the main README's [Arabic & RTL section](../README.md)
(`docs/media/arabic-architecture.gif`, `docs/media/arabic-concept.gif`).

## `install-walkthrough/` — the README's install animation

The animated terminal shown beside the install instructions in the main
README — a **dark** stylized terminal that reveals the four install commands
step-by-step (`$` prompts type in, italic comments, green ✓ completions). A
hand-authored "code/terminal" scene (no `code_to_svg.py`, since these are shell
commands).

| File | What it is |
|---|---|
| [`index.html`](install-walkthrough/index.html) | Source — the terminal panel, per-line `<g class="ln">` rows, and the caret-hop reveal timeline. |
| [`renders/install.mp4`](install-walkthrough/renders/install.mp4) | The video (1200×920, 12 s). |
| [`renders/install.interactive.html`](install-walkthrough/renders/install.interactive.html) | Self-contained interactive player. |

GIF in the main README's [install section](../README.md) (`docs/media/install.gif`).
