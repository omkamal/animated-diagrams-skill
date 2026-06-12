# Arabic & RTL diagrams

Scaffold with `--lang ar` — it appends the Arabic overlay (Cairo fonts, RTL
text rules) to theme.css and sets `<html lang="ar" dir="rtl">`. Typography is
handled automatically; **flow geometry must be mirrored by the author**.

## Bundled Arabic fonts

| Font | Use | Pairs with styles |
|---|---|---|
| **Cairo** (variable, default) | titles + body — modern geometric sans | light, dark, corporate, vivid, glass, blueprint |
| **Amiri** | traditional Naskh serif — formal/editorial/classical | editorial, sketch (set `--font-title: "Amiri"`) |
| **Tajawal** (400/700) | clean humanist alternative body | pastel, wireframe |
| **Reem Kufi** | geometric Kufi display — titles only, never body | brutalist, vivid titles |

Override per-project in theme.css after the overlay:
`:root { --font-title: "Amiri", serif; }`

## Typography rules (the overlay enforces most)

- `letter-spacing: 0` always — tracking breaks Arabic joining. The overlay
  zeroes `--tracking-region`; never add letter-spacing inline on Arabic text.
- `unicode-bidi: plaintext` keeps mixed Latin tokens (API, HTTP, S3) readable
  inside Arabic labels.
- Arabic reads ~10% smaller at equal px — labels ≥24px at 1080p (the overlay
  bumps `.label` 110%).
- Numerals: Western digits (1, 2, 3) are standard in tech contexts; use
  Arabic-Indic (١٢٣) only if the user asks.
- Diacritics (tashkeel) render fine in Amiri/Cairo if provided; don't strip.

## Mirrored flow geometry (author's responsibility)

Everything narrative flows **right → left, top → bottom**:

- **Entry node on the RIGHT** (user/client at far right; data stores at far
  left). The narrative order of `tl.from(...)` staggers follows the same
  right→left order.
- **Edges drawn right→left**: author the path `d` FROM source (right) TO
  destination (left) so DrawSVG grows leftward:
  `<path id="edge-client-api" class="edge" d="M 1400 540 C 1300 540 1260 540 1180 540"/>`
- **Arrowheads point LEFT**: `<path class="edge-head" d="M 1166 540 l 16 -8 v 16 z"/>`
  (apex on the left, base on the right — mirror of the LTR triangle).
- **Region titles top-RIGHT**: `<text class="region-title" x="<right-edge − 36>"
  text-anchor="end" …>`.
- **Node internals mirrored**: icon on the RIGHT of the card, text to its
  left with `text-anchor="end"` anchored near the icon.
- **Sequence diagrams**: first participant at far right; messages flow
  right→left; reply arrows left→right (dashed). Message order still top→down.
- **Flowcharts**: happy path right→left; "yes/نعم" branch continues left,
  "no/لا" drops downward.
- MotionPath pulses automatically follow the path direction — author the path
  right→left and the pulse travels correctly.

## Camera patterns mirrored

- **conveyor**: slides LEFTWARD (start camera at the right end, pan toward x=0).
- **reveal-pan**: starts at the RIGHT entry point, pans left.
- **guided tour**: stops ordered right→left.
- **vertical scroll**: unchanged (top→bottom is universal).

## HUD

Title centered is fine; if a subtitle line carries mixed content, set
`text-anchor="middle"` and let `unicode-bidi: plaintext` handle ordering.
For dual-language deliverables, render two projects (en + ar) — don't mix
directions in one scene.
