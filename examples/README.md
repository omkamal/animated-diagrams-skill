# Sample outputs

Real, unedited deliverables produced by the skill's render pipeline — committed
so you can see exactly what you get before installing anything.

Each folder is a **runnable project**: its `index.html` is the authoring source,
and it references the repo's shared `../../assets/` (fonts + vendored GSAP), so
after cloning you can open any `index.html` directly in a browser, or re-render
it with `node scripts/render.mjs --project examples/<name>`. The
`*.interactive.html` players are fully self-contained (no dependencies at all).

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

## `concept-demo/` — concept illustration + voice-over sync

A concept strip (💡 Idea → 🛠️ Build → 🚀 Launch) built with **noto color-emoji
cliparts**, with **real narration** (generated with TTS) where every beat fires
exactly on its SRT cue and the audio is **muxed into the MP4** (h264 + aac).
Idea appears as *"Every product begins with an idea"* is spoken, Build as
*"you build it, piece by piece"*, Launch on *"and then — you launch."*

| File | What it is |
|---|---|
| [`index.html`](concept-demo/index.html) | Authoring source — the `<symbol id="clip-noto-*">` emoji defs, the `<audio id="narration">` clip, and beats placed at the cue start times. |
| [`audio/narration.srt`](concept-demo/audio/narration.srt) · [`audio/narration.wav`](concept-demo/audio/narration.wav) | The narration script (SRT cues) and the spoken audio that drives the timing. |
| [`renders/concept-narrated.mp4`](concept-demo/renders/concept-narrated.mp4) | The narrated render — **turn your sound on**: each station appears as it's spoken. |
| [`renders/concept-narrated.interactive.html`](concept-demo/renders/concept-narrated.interactive.html) | Self-contained interactive player. |

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
