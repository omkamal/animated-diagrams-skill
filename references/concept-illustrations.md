# Concept illustrations — cliparts, emojis & icon libraries

Beyond the bundled stylized shapes (`assets/icons/`), the skill can pull from
the **Iconify network** — 200k+ open-licensed icons, emojis and cliparts —
downloaded at authoring time **into the working project directory** (renders
stay fully local/deterministic).

## Workflow

```bash
# 1. search the universe (200k+ icons across all sets)
node $SKILL_DIR/scripts/fetch_clipart.mjs --search "rocket launch" --limit 24
node $SKILL_DIR/scripts/fetch_clipart.mjs --search "database" --prefixes lucide,tabler

# 2. fetch into the project — saves cliparts/<set>-<name>.svg AND auto-injects
#    a <symbol id="clip-<set>-<name>"> into index.html <defs>
node $SKILL_DIR/scripts/fetch_clipart.mjs --project ./animated-svg-<slug> \
     noto:rocket noto:light-bulb lucide:database twemoji:fire

# 3. place in the scene
<use href="#clip-noto-rocket" x="860" y="380" width="200" height="200"/>
```

## Recommended sets (license table — all prefixes verified on the API)

### Professional UI / tech icon sets (crisp, corporate-grade)

| Prefix | What | License | Notes |
|---|---|---|---|
| `fa6-solid` / `fa6-regular` / `fa6-brands` | **Font Awesome 6 Free** (2000+) | CC-BY 4.0 | the classic professional look; FA5 also available as `fa-solid` / `fa-regular` / `fa-brands` |
| `material-symbols` | Google Material Symbols (10k+) | Apache-2.0 | Google product look; `-outline`/`-rounded` variants in names |
| `mdi` | Material Design Icons community (7000+) | Apache-2.0 | broadest coverage of any set |
| `fluent` | Microsoft Fluent UI System (16k+) | MIT | sized names (`cloud-24-filled`/`-regular`); very polished |
| `carbon` | IBM Carbon (2000+) | Apache-2.0 | **best for enterprise/data/cloud diagrams** (kubernetes, bare-metal, data-lake…) |
| `bi` | Bootstrap Icons (2000+) | MIT | clean neutral UI look |
| `heroicons` | Tailwind Heroicons | MIT | minimal, modern (`-solid`/`-outline` suffixes) |
| `ri` | Remix Icon (3000+) | Apache-2.0 | balanced line+fill pairs |
| `solar` | Solar (7000+, 6 weights) | CC-BY 4.0 | `-bold`/`-linear`/`-duotone`… suffixes |
| `lucide` / `tabler` | line icons (1500/5800+) | ISC / MIT | hairline style — pairs with light/mono/wireframe |
| `ph` (Phosphor) | line+fill family | MIT | weights: `ph:x`, `ph:x-fill`, `ph:x-duotone` |

All of these are monochrome → set `color="var(--c-…)"` on the `<use>` so they
follow the theme like the bundled icons.

### Color cliparts, emoji & brand sets

| Prefix | What | License | Notes |
|---|---|---|---|
| `noto` | Google Noto color emoji (3000+) | Apache-2.0 | **safe default** for colorful concept art |
| `flat-color-icons` | Icons8 Flat Color (business/office) | MIT | professional *colored* cliparts — idea, approval, org chart, statistics… |
| `fluent-emoji` / `fluent-emoji-flat` | Microsoft Fluent emoji (glossy / flat) | MIT | modern, friendly |
| `twemoji` | Twitter emoji | CC-BY 4.0 | attribution required in published work |
| `openmoji` | OpenMoji (huge, incl. concepts/tech) | CC-BY-SA 4.0 | share-alike — avoid for client work |
| `logos` | official tech/product logos in full color (AWS, React, Stripe…) | mixed/trademarks | nominative use only — labeling the actual service in an architecture |
| `devicon` | developer tools/languages logos | MIT (logos trademarked) | python, docker, postgres… same nominative-use rule |
| `healthicons` | health/medical | MIT | |
| `game-icons` | 4000+ rich pictograms (metaphors!) | CC-BY 3.0 | great for abstract concepts |
| `simple-icons` | brand glyphs, monochrome | CC0, **logos trademarked** | only for "integrates with X" contexts |

Discover anything: `fetch_clipart.mjs --search "<term>" --prefixes fa6-solid,carbon,material-symbols`.
Browse visually at https://icon-sets.iconify.design. Bundled fallback
(offline, always available): `assets/icons/*.svg` stylized sets.

### Picking a set by style preset

**Defaults: `fa6-solid` for generic/service icons; `logos`/`devicon` for
vendor products.** A 26-icon FA6 offline pack ships at
`assets/icons/fa6-common.svg` (ids `icon-fa-*`). Deviate by style:

- `corporate`, `light`, `glass` → `fa6-solid` (default), or `material-symbols` / `fluent` / `carbon`
- `mono`, `wireframe`, `blueprint` → `lucide`, `tabler`, `carbon` (hairlines beat FA6 solids here)
- `vivid`, `brutalist` → `fa6-solid`, `bi` (strong solid shapes)
- `pastel`, concept scenes → `noto`, `fluent-emoji`, `flat-color-icons`
- `sketch` → bundled stylized line glyphs (hand-drawn consistency)
- tech-architecture with real products → `logos` / `devicon` (default; nominative use)

## Color vs line — match the style preset

- **Color cliparts/emoji** (`noto`, `fluent-emoji`, `twemoji`): bring their own
  colors — do NOT recolor. Best on `light`, `pastel`, `glass`, `vivid`. On
  `dark`, prefer flat sets and add a subtle white-glow halo circle behind the
  clipart for contrast.
- **Line icons** (`lucide`, `tabler`, `ph`): render in `currentColor` — set
  `color="var(--c-blue)"` on the `<use>` so they theme like bundled icons.
  Best on `mono`, `wireframe`, `corporate`, `editorial`, `blueprint`, `sketch`.
- `brutalist`: line icons stroked black, or emoji at large size for irony.

## Concept-scene patterns (illustrating ideas, not architectures)

1. **Hero metaphor**: one large clipart (200–320px) center/golden-ratio, title
   + one-line caption in HUD, 2–4 small satellite cliparts orbiting in.
   Entrance: hero `scale 0 → 1, back.out(1.6)`; satellites stagger-pop after.
2. **Idea → outcome strip**: 3–4 cliparts left→right joined by `.edge` arrows
   (💡 → ⚙️ → 🚀 → 📈): treat cliparts as nodes — same edge/arrowhead contract,
   `.from()` pops in narrative order, pulse rides the strip.
3. **Concept map**: central clipart, radial spokes to labeled mini-cliparts;
   draw spokes with DrawSVG after center lands; gentle idle float on center
   (`y ±4`, `sine.inOut`, bounded repeats).
4. **Before/after split**: vertical divider; left scene dims (`opacity .35`)
   as right scene pops; camera nudges right (`camPanTo`).
5. **Emoji annotations on diagrams**: small (44–64px) cliparts as badges on
   node corners (⚠️ 🔒 ✅ ⏱️) — pop in with `back.out(2.5)` AFTER the node
   lands, never simultaneously.

## Animating cliparts (multi-path color SVGs)

- Animate the `<use>` (or a wrapping `<g>`) — scale/rotate/float the whole
  clipart; per-path animation inside fetched emoji is unreliable.
- Always `transformOrigin: "50% 50%"` for pops/wiggles.
- Wiggle accent: `rotation: -6 → 6 → 0`, `duration .5`, once — not looping.
- Floating idle: `y: -6`, `sine.inOut`, `repeat: 3, yoyo: true` (bounded).
- Don't mix more than 2 emoji sets in one scene — visual style clashes.

## Determinism rules

Fetch ONLY at authoring time (network at render time is forbidden). Fetched
files live in the project's `cliparts/` dir + injected symbols, so re-renders
and the zip-able project stay self-contained. Record attribution for CC-BY
sets in the delivery message when the user will publish the result.
