#!/usr/bin/env node
/**
 * inline_html.mjs — build a single-file interactive HTML deliverable.
 *
 *   node inline_html.mjs --project DIR [--output FILE]
 *
 * Inlines local <script src> / <link rel=stylesheet> contents, base64-inlines
 * woff2 fonts referenced from CSS, strips HyperFrames data-* wiring, and
 * injects a minimal play/pause/scrub bar bound to the registered timeline.
 * Result opens anywhere (double-click) with zero dependencies.
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, join, basename } from "node:path";

const args = process.argv.slice(2);
let project = ".", output = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--project") project = args[++i];
  else if (args[i] === "--output" || args[i] === "-o") output = args[++i];
  else { console.error(`unknown flag: ${args[i]}`); process.exit(1); }
}
project = resolve(project);
const htmlPath = join(project, "index.html");
if (!existsSync(htmlPath)) { console.error(`no index.html in ${project}`); process.exit(1); }
output = resolve(output ?? join(project, "renders", `${basename(project)}.interactive.html`));

let html = readFileSync(htmlPath, "utf8");

// inline stylesheets (with fonts base64-embedded)
html = html.replace(/<link\s+rel="stylesheet"\s+href="([^"]+)"\s*\/?>/g, (m, href) => {
  let css = readFileSync(join(project, href), "utf8");
  css = css.replace(/url\("?\.\/([^")]+\.woff2)"?\)/g, (m2, rel) => {
    const b64 = readFileSync(join(project, rel)).toString("base64");
    return `url("data:font/woff2;base64,${b64}")`;
  });
  return `<style>\n${css}\n</style>`;
});

// inline local scripts
html = html.replace(/<script\s+src="(\.\/[^"]+)"\s*><\/script>/g, (m, src) =>
  `<script>\n${readFileSync(join(project, src), "utf8")}\n</script>`);

// scrub-bar UI bound to the registered timeline
const ui = `
<style>
  #asvg-bar { position: fixed; left: 16px; right: 16px; bottom: 14px; display: flex;
    gap: 10px; align-items: center; padding: 8px 14px; border-radius: 12px;
    background: rgba(15, 23, 42, 0.82); backdrop-filter: blur(6px);
    font-family: system-ui, sans-serif; z-index: 99; opacity: 0.25; transition: opacity .2s; }
  #asvg-bar:hover { opacity: 1; }
  #asvg-play { width: 34px; height: 34px; border: 0; border-radius: 50%; cursor: pointer;
    background: #38bdf8; color: #0b1021; font-size: 15px; }
  #asvg-scrub { flex: 1; accent-color: #38bdf8; }
  #asvg-time { color: #cbd5e1; font-size: 12px; min-width: 72px; text-align: right; }
</style>
<div id="asvg-bar">
  <button id="asvg-play">⏸</button>
  <input id="asvg-scrub" type="range" min="0" max="1000" value="0" />
  <span id="asvg-time"></span>
</div>
<script>
(function () {
  var tl = (window.__timelines || {}).main;
  if (!tl) return;
  var play = document.getElementById("asvg-play");
  var scrub = document.getElementById("asvg-scrub");
  var time = document.getElementById("asvg-time");
  var dragging = false;
  tl.eventCallback("onUpdate", function () {
    if (!dragging) scrub.value = Math.round(tl.progress() * 1000);
    time.textContent = tl.time().toFixed(1) + " / " + tl.duration().toFixed(1) + "s";
  });
  tl.eventCallback("onComplete", function () { play.textContent = "↻"; });
  play.addEventListener("click", function () {
    if (tl.progress() >= 1) { tl.restart(); play.textContent = "⏸"; }
    else if (tl.paused() || !tl.isActive()) { tl.play(); play.textContent = "⏸"; }
    else { tl.pause(); play.textContent = "▶"; }
  });
  scrub.addEventListener("pointerdown", function () { dragging = true; tl.pause(); play.textContent = "▶"; });
  scrub.addEventListener("pointerup", function () { dragging = false; });
  scrub.addEventListener("input", function () { tl.progress(scrub.value / 1000); });
})();
</script>
`;
html = html.replace("</body>", `${ui}\n</body>`);

writeFileSync(output, html);
console.log(`interactive html: ${output} (${(html.length / 1024).toFixed(0)} KB)`);
