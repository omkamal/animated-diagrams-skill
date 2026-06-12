#!/usr/bin/env bash
# One-time setup for the animated-svg skill (macOS zsh + Linux bash):
#   npm install → vendor GSAP dist files → ensure Chrome → warm-up smoke render.
#
# Run it, do NOT source it:   bash scripts/setup.sh   (or ./scripts/setup.sh)
# Sourcing (`. setup.sh`) runs it in your shell, where the script can't find its
# own path — it would resolve to "/" and npm-install at your filesystem root.

# ── Guard: must be executed, not sourced; works in zsh (macOS) and bash ──────
__sourced=0
if [ -n "${ZSH_VERSION:-}" ]; then
  case "${ZSH_EVAL_CONTEXT:-}" in *:file*) __sourced=1 ;; esac
elif [ -n "${BASH_VERSION:-}" ]; then
  [ "${BASH_SOURCE:-$0}" != "$0" ] && __sourced=1
fi
if [ "$__sourced" = 1 ]; then
  printf 'animated-svg: run this script, do not source it:\n    bash scripts/setup.sh\n' >&2
  return 1 2>/dev/null || exit 1
fi

set -euo pipefail

# Portable self-path: bash exposes BASH_SOURCE; zsh (e.g. `zsh setup.sh`) uses $0.
__self="${BASH_SOURCE:-$0}"
SKILL_DIR="$(cd "$(dirname "$__self")/.." && pwd)"
if [ ! -f "$SKILL_DIR/package.json" ]; then
  echo "ERROR: cannot locate the skill root from '$__self' (got '$SKILL_DIR')." >&2
  echo "       Run it directly:  bash scripts/setup.sh" >&2
  exit 1
fi
cd "$SKILL_DIR"

echo "==> animated-svg setup in $SKILL_DIR"

command -v node >/dev/null || { echo "ERROR: node not found (need Node >= 22). macOS: brew install node"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpeg not found. macOS: brew install ffmpeg"; exit 1; }
command -v python3 >/dev/null || { echo "ERROR: python3 not found (needed for the smoke render + authoring helpers). macOS: brew install python"; exit 1; }
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
