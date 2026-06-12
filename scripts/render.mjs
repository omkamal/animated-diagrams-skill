#!/usr/bin/env node
/**
 * render.mjs — single abstraction over the HyperFrames CLI + ffmpeg derivations.
 *
 *   node render.mjs --project DIR --output out.mp4
 *        [--fps 30] [--quality draft|standard|high] [--resolution PRESET]
 *        [--gif] [--gif-width 960] [--gif-fps 15] [--webm] [--svg]
 *        [--snapshots N] [--at t1,t2,...] [--probe] [--quiet]
 *
 * - MP4 is rendered by hyperframes (deterministic frame-seek capture).
 * - GIF/WebM are derived from the MP4 with ffmpeg (fast, no re-render).
 * - --svg exports the static resolved-state diagram via export_svg.mjs.
 * - --snapshots / --at capture PNG key frames + contact-sheet.jpg via
 *   `hyperframes snapshot` for visual verification (Read the contact sheet!).
 * - --probe prints an ffprobe summary and asserts the output is sane.
 */
import { spawnSync } from "node:child_process";
import { existsSync, statSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, resolve, join, basename } from "node:path";
import { fileURLToPath } from "node:url";

const SKILL_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const HF = join(SKILL_DIR, "node_modules", ".bin", "hyperframes");

// ---- arg parsing ----
const args = process.argv.slice(2);
const opt = {
  project: ".", output: null, fps: "30", quality: "standard", resolution: null,
  gif: false, gifWidth: "960", gifFps: "15", webm: false, svg: false,
  snapshots: null, at: null, probe: false, quiet: false,
};
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  const next = () => args[++i];
  switch (a) {
    case "--project":    opt.project = next(); break;
    case "--output": case "-o": opt.output = next(); break;
    case "--fps":        opt.fps = next(); break;
    case "--quality":    opt.quality = next(); break;
    case "--resolution": opt.resolution = next(); break;
    case "--gif":        opt.gif = true; break;
    case "--gif-width":  opt.gifWidth = next(); break;
    case "--gif-fps":    opt.gifFps = next(); break;
    case "--webm":       opt.webm = true; break;
    case "--svg":        opt.svg = true; break;
    case "--snapshots":  opt.snapshots = next(); break;
    case "--at":         opt.at = next(); break;
    case "--probe":      opt.probe = true; break;
    case "--quiet":      opt.quiet = true; break;
    default: fail(`unknown flag: ${a}`);
  }
}

function fail(msg) { console.error(`render.mjs: ${msg}`); process.exit(1); }
function run(cmd, argv, label) {
  const r = spawnSync(cmd, argv, { stdio: opt.quiet ? "pipe" : "inherit" });
  if (r.status !== 0) {
    if (opt.quiet && r.stderr) console.error(String(r.stderr).slice(-2000));
    fail(`${label} failed (exit ${r.status})`);
  }
  return r;
}

if (!existsSync(HF)) fail(`hyperframes not installed — run: bash ${SKILL_DIR}/scripts/setup.sh`);
const project = resolve(opt.project);
if (!existsSync(join(project, "index.html"))) fail(`no index.html in ${project}`);
const output = resolve(opt.output ?? join(project, "renders", `${basename(project)}.mp4`));
mkdirSync(dirname(output), { recursive: true });

// ---- 1. MP4 render ----
const hfArgs = ["render", project, "-o", output, "--fps", opt.fps, "--quality", opt.quality];
if (opt.resolution) hfArgs.push("--resolution", opt.resolution);
if (opt.quiet) hfArgs.push("--quiet");
run(HF, hfArgs, "hyperframes render");

// ---- 2. derivations ----
const stem = output.replace(/\.mp4$/, "");
if (opt.gif) {
  const vf = `fps=${opt.gifFps},scale=${opt.gifWidth}:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4`;
  run("ffmpeg", ["-y", "-loglevel", "error", "-i", output, "-vf", vf, `${stem}.gif`], "gif derivation");
  console.log(`gif:  ${stem}.gif`);
}
if (opt.webm) {
  run("ffmpeg", ["-y", "-loglevel", "error", "-i", output,
    "-c:v", "libvpx-vp9", "-crf", "32", "-b:v", "0", "-an", `${stem}.webm`], "webm derivation");
  console.log(`webm: ${stem}.webm`);
}
if (opt.svg) {
  run(process.execPath, [join(SKILL_DIR, "scripts", "export_svg.mjs"),
    "--project", project, "--output", `${stem}.svg`], "svg export");
  console.log(`svg:  ${stem}.svg`);
}

// ---- 3. snapshots (visual verification) ----
if (opt.snapshots || opt.at) {
  const sArgs = ["snapshot", project, "--describe", "false"];
  if (opt.at) sArgs.push("--at", opt.at);
  else {
    // compute N evenly spaced timestamps within [0, duration] ourselves —
    // `snapshot --frames N` samples past the end (black frames)
    const m = readFileSync(join(project, "index.html"), "utf8").match(/data-duration="([\d.]+)"/);
    const dur = m ? parseFloat(m[1]) : 10;
    const n = Math.max(2, parseInt(opt.snapshots, 10));
    const ts = Array.from({ length: n }, (_, i) =>
      (0.05 + (i * (dur - 0.15)) / (n - 1)).toFixed(2));
    sArgs.push("--at", ts.join(","));
  }
  run(HF, sArgs, "hyperframes snapshot");
  console.log(`snapshots: ${join(project, "snapshots")}/ (view contact-sheet.jpg)`);
}

// ---- 4. probe + sanity assertions ----
if (opt.probe) {
  const r = spawnSync("ffprobe", ["-v", "quiet", "-print_format", "json",
    "-show_format", "-show_streams", output], { encoding: "utf8" });
  if (r.status !== 0) fail("ffprobe failed");
  const info = JSON.parse(r.stdout);
  const v = info.streams.find((s) => s.codec_type === "video");
  const dur = parseFloat(info.format.duration);
  const size = statSync(output).size;
  console.log(`probe: ${v.codec_name} ${v.width}x${v.height} @ ${v.avg_frame_rate} fps · ${dur.toFixed(2)}s · ${(size / 1024).toFixed(0)} KB`);

  if (size < 10_000) fail(`output suspiciously small (${size} bytes) — blank render?`);
  if (!(dur > 0.5)) fail(`output duration ${dur}s — timeline not registered?`);
  const expected = readFileSync(join(project, "index.html"), "utf8").match(/data-duration="([\d.]+)"/);
  if (expected && Math.abs(dur - parseFloat(expected[1])) > 0.25)
    console.warn(`WARN: duration ${dur}s != data-duration ${expected[1]}s`);
}
console.log(`mp4:  ${output}`);
