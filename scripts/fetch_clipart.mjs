#!/usr/bin/env node
/**
 * fetch_clipart.mjs — search & fetch open-licensed cliparts/icons/emojis from
 * the Iconify network (200k+ icons: noto, twemoji, openmoji, fluent-emoji,
 * lucide, tabler, healthicons, game-icons, …) into the WORKING project dir.
 *
 *   node fetch_clipart.mjs --search "rocket" [--limit 24] [--prefixes noto,twemoji]
 *   node fetch_clipart.mjs --project DIR noto:rocket twemoji:fire lucide:database
 *
 * Fetch mode downloads each icon to DIR/cliparts/<prefix>-<name>.svg AND
 * injects a `<symbol id="clip-<prefix>-<name>" viewBox="…">` into the
 * project's index.html <defs> (idempotent). Use in the scene with:
 *   <use href="#clip-noto-rocket" x="100" y="100" width="96" height="96"/>
 *
 * Downloads happen at AUTHORING time only — the composition stays fully local
 * and deterministic at render time. Licenses vary by set (see
 * references/concept-illustrations.md); noto (Apache-2.0) is the safe default.
 */
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { resolve, join } from "node:path";

const API = "https://api.iconify.design";
const args = process.argv.slice(2);
let project = null, search = null, limit = 24, prefixes = null;
const icons = [];
for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case "--project":  project = args[++i]; break;
    case "--search":   search = args[++i]; break;
    case "--limit":    limit = parseInt(args[++i], 10); break;
    case "--prefixes": prefixes = args[++i]; break;
    default:
      if (/^[a-z0-9-]+:[a-z0-9-]+$/.test(args[i])) icons.push(args[i]);
      else { console.error(`unrecognized arg: ${args[i]} (icons are prefix:name)`); process.exit(1); }
  }
}

async function get(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r;
}

if (search) {
  const u = new URL(`${API}/search`);
  u.searchParams.set("query", search);
  u.searchParams.set("limit", String(limit));
  if (prefixes) u.searchParams.set("prefixes", prefixes);
  const data = await (await get(u)).json();
  if (!data.icons?.length) { console.log("no results"); process.exit(0); }
  console.log(`${data.total} matches (showing ${data.icons.length}):`);
  for (const id of data.icons) console.log("  " + id);
  console.log(`\nfetch with: node fetch_clipart.mjs --project <DIR> ${data.icons.slice(0, 3).join(" ")}`);
  process.exit(0);
}

if (!icons.length) { console.error("nothing to do — pass --search or prefix:name icons"); process.exit(1); }
project = resolve(project ?? ".");
const htmlPath = join(project, "index.html");
const hasHtml = existsSync(htmlPath);
mkdirSync(join(project, "cliparts"), { recursive: true });

let html = hasHtml ? readFileSync(htmlPath, "utf8") : null;
let injected = 0;

for (const id of icons) {
  const [prefix, name] = id.split(":");
  const slug = `${prefix}-${name}`;
  const svg = await (await get(`${API}/${prefix}/${name}.svg`)).text();
  if (svg.includes("404") && !svg.includes("<svg")) { console.error(`NOT FOUND: ${id}`); continue; }
  const file = join(project, "cliparts", `${slug}.svg`);
  writeFileSync(file, svg);

  const vb = (svg.match(/viewBox="([^"]+)"/) || [])[1] ?? "0 0 24 24";
  const inner = svg.replace(/^[\s\S]*?<svg[^>]*>/, "").replace(/<\/svg>\s*$/, "");
  const symbol = `<symbol id="clip-${slug}" viewBox="${vb}">${inner}</symbol>`;

  if (html) {
    if (html.includes(`id="clip-${slug}"`)) {
      console.log(`= ${id} (already injected)`);
    } else if (html.includes("</defs>")) {
      html = html.replace("</defs>", () => `  ${symbol}\n        </defs>`);
      injected++;
      console.log(`+ ${id} → cliparts/${slug}.svg + <symbol id="clip-${slug}"> (viewBox ${vb})`);
    } else {
      console.log(`+ ${id} → cliparts/${slug}.svg (no <defs> in index.html — paste symbol manually)`);
    }
  } else {
    console.log(`+ ${id} → cliparts/${slug}.svg (viewBox ${vb})`);
  }
  console.log(`    <use href="#clip-${slug}" x="0" y="0" width="96" height="96"/>`);
}

if (html && injected) writeFileSync(htmlPath, html);
if (!hasHtml) console.log("note: no index.html in project — symbols not injected");
