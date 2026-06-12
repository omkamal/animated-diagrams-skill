#!/usr/bin/env bash
# Scaffold a self-contained animation project directory from the skill template.
#
#   new_project.sh <slug> [--theme <style>] [--width N] [--height N]
#                         [--duration SECONDS] [--transparent] [--dir PARENT_DIR]
#
# Styles (12, see references/style-presets.md + assets/gallery/styles-gallery.html):
#   light (default) · dark · blueprint · sketch · corporate · pastel · mono ·
#   editorial · vivid · glass · brutalist · wireframe
# --transparent: transparent canvas (deliver via SVG / interactive HTML /
#   `hyperframes render --format webm|mov`; MP4 flattens to black).
#
# Creates <PARENT_DIR>/animated-svg-<slug>/ (default PARENT_DIR = caller's cwd;
# inside --dir the folder is named just <slug> when PARENT_DIR ends in .smoke).
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SLUG="${1:?usage: new_project.sh <slug> [--theme ..] [--width ..] [--height ..] [--duration ..] [--transparent] [--dir ..]}"
shift
THEME="light"; WIDTH=1920; HEIGHT=1080; DURATION=12; PARENT="$(pwd)"; TRANSPARENT=0; LANG_MODE="en"

while [ $# -gt 0 ]; do
  case "$1" in
    --theme)       THEME="$2";    shift 2 ;;
    --width)       WIDTH="$2";    shift 2 ;;
    --height)      HEIGHT="$2";   shift 2 ;;
    --duration)    DURATION="$2"; shift 2 ;;
    --transparent) TRANSPARENT=1; shift ;;
    --lang)        LANG_MODE="$2"; shift 2 ;;
    --dir)         PARENT="$2";   shift 2 ;;
    *) echo "unknown flag: $1"; exit 1 ;;
  esac
done

[ -f "$SKILL_DIR/assets/themes/$THEME.css" ] || {
  echo "ERROR: unknown style '$THEME'. Available: $(cd "$SKILL_DIR/assets/themes" && ls *.css | sed 's/\.css//' | tr '\n' ' ')"
  exit 1
}
[ -d "$SKILL_DIR/assets/vendor/gsap" ] && [ -s "$SKILL_DIR/assets/vendor/gsap/gsap.min.js" ] \
  || { echo "ERROR: vendored gsap missing — run: bash $SKILL_DIR/scripts/setup.sh"; exit 1; }

case "$PARENT" in *".smoke") DEST="$PARENT/$SLUG" ;; *) DEST="$PARENT/animated-svg-$SLUG" ;; esac
[ -e "$DEST" ] && { echo "ERROR: $DEST already exists"; exit 1; }

mkdir -p "$DEST/vendor" "$DEST/fonts" "$DEST/renders" "$DEST/snapshots"
cp "$SKILL_DIR"/assets/vendor/gsap/*.js "$DEST/vendor/"
cp "$SKILL_DIR"/assets/fonts/*.woff2 "$DEST/fonts/"
cat "$SKILL_DIR/assets/template/theme.css" "$SKILL_DIR/assets/themes/$THEME.css" > "$DEST/theme.css"
if [ "$LANG_MODE" = "ar" ]; then
  cat "$SKILL_DIR/assets/themes/lang-ar.css" >> "$DEST/theme.css"
fi
if [ "$TRANSPARENT" = 1 ]; then
  printf '\n/* transparent canvas override */\n:root { --bg: transparent; }\nhtml, body { background: transparent; }\n' >> "$DEST/theme.css"
fi
sed -e "s/__WIDTH__/$WIDTH/g" -e "s/__HEIGHT__/$HEIGHT/g" -e "s/__DURATION__/$DURATION/g" \
  "$SKILL_DIR/assets/template/composition.html" > "$DEST/index.html"
if [ "$LANG_MODE" = "ar" ]; then
  sed -i 's/<html lang="en">/<html lang="ar" dir="rtl">/' "$DEST/index.html"
fi
printf '{\n  "id": "%s",\n  "name": "%s"\n}\n' "$SLUG" "$SLUG" > "$DEST/meta.json"

echo "Created $DEST"
echo "  edit:    index.html — SVG scene (layer groups) + inline TIMELINE script"
echo "  style:   $THEME$([ "$TRANSPARENT" = 1 ] && echo ' (transparent)') · ${WIDTH}x${HEIGHT} · ${DURATION}s (data-duration in index.html)"
echo "  render:  node $SKILL_DIR/scripts/render.mjs --project $DEST --output $DEST/renders/$SLUG.mp4 --snapshots 5 --probe"
