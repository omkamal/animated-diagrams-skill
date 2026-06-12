#!/usr/bin/env bash
# One-time setup for the animated-svg skill:
#   npm install → vendor GSAP dist files → ensure Chrome → warm-up smoke render.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

echo "==> animated-svg setup in $SKILL_DIR"

command -v node >/dev/null || { echo "ERROR: node not found (need Node >= 22)"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg not found"; exit 1; }
NODE_MAJOR=$(node -p "process.versions.node.split('.')[0]")
[ "$NODE_MAJOR" -ge 22 ] || { echo "ERROR: Node >= 22 required (have $(node --version))"; exit 1; }

echo "==> Installing npm dependencies (hyperframes + gsap)..."
if [ -f package-lock.json ]; then npm ci; else npm install; fi

HF="$SKILL_DIR/node_modules/.bin/hyperframes"
[ -x "$HF" ] || { echo "ERROR: hyperframes binary missing after install"; exit 1; }

echo "==> Vendoring GSAP dist files into assets/vendor/gsap/..."
mkdir -p assets/vendor/gsap
for f in gsap.min.js DrawSVGPlugin.min.js MotionPathPlugin.min.js MorphSVGPlugin.min.js; do
  cp "node_modules/gsap/dist/$f" "assets/vendor/gsap/$f"
  [ -s "assets/vendor/gsap/$f" ] || { echo "ERROR: missing gsap dist file $f"; exit 1; }
done

echo "==> Ensuring Chrome for rendering (one-time download if absent)..."
"$HF" browser ensure || true
"$HF" doctor || true

echo "==> Warm-up smoke render..."
SMOKE="$SKILL_DIR/.smoke/warmup"
rm -rf "$SMOKE"
bash "$SKILL_DIR/scripts/new_project.sh" warmup --dir "$SKILL_DIR/.smoke" --duration 2 >/dev/null
# minimal visible content + 2s timeline (timeline lives inline in index.html)
python3 - "$SMOKE" <<'EOF'
import pathlib, sys
d = pathlib.Path(sys.argv[1])
html = (d / "index.html").read_text()
html = html.replace(
    "<g id=\"layer-nodes\"><!-- nodes: <g id=\"node-*\" class=\"node\"> --></g>",
    '<g id="layer-nodes"><g id="node-a" class="node"><rect x="810" y="470" width="300" height="140" rx="18"/>'
    '<text x="960" y="550" text-anchor="middle" font-size="36">warmup</text></g></g>')
html = html.replace('window.__timelines = window.__timelines || {};',
    'tl.from("#node-a", { opacity: 0, scale: 0.8, transformOrigin: "50% 50%", duration: 1 }, 0)\n'
    '        .to({}, { duration: 1 });\n\n'
    '      window.__timelines = window.__timelines || {};', 1)
(d / "index.html").write_text(html)
EOF
node "$SKILL_DIR/scripts/render.mjs" --project "$SMOKE" --output "$SMOKE/out.mp4" --probe
rm -rf "$SMOKE"

echo
echo "==> animated-svg setup complete."
echo "    node:        $(node --version)"
echo "    hyperframes: $("$HF" --help 2>/dev/null | head -1 | grep -o 'v[0-9][0-9.]*' | head -1 || echo '?')"
echo "    gsap:        $(node -p "require('$SKILL_DIR/node_modules/gsap/package.json').version")"
echo "    ffmpeg:      $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
