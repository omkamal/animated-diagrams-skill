#!/usr/bin/env python3
"""srt_to_cues.py — parse an SRT/VTT voice-over script into animation cues.

Usage:
  srt_to_cues.py narration.srt                # print cue table + JS snippet
  srt_to_cues.py narration.srt --json cues.json
  srt_to_cues.py narration.srt --js           # only the JS CUES constant

Each cue drives ONE animation beat: the element/camera action for cue N fires
exactly at `start`, holds focus until `end` (while its voice-over plays), and
the NEXT beat begins at the next cue's start — never before. See
references/voiceover-sync.md. Pure stdlib.
"""
import argparse
import json
import re
import sys


def parse_time(ts):
    m = re.match(r"(\d+):(\d+):(\d+)[.,](\d+)", ts.strip())
    if not m:
        m2 = re.match(r"(\d+):(\d+)[.,](\d+)", ts.strip())  # VTT MM:SS.mmm
        if not m2:
            raise ValueError(f"bad timestamp: {ts}")
        mm, ss, ms = m2.groups()
        return int(mm) * 60 + int(ss) + int(ms.ljust(3, "0")) / 1000
    hh, mm, ss, ms = m.groups()
    return int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms.ljust(3, "0")) / 1000


def parse(path):
    text = open(path, encoding="utf-8-sig").read()
    text = re.sub(r"^WEBVTT.*?\n\n", "", text, flags=re.S)  # VTT header
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        # optional numeric index line
        if re.fullmatch(r"\d+", lines[0].strip()) and len(lines) > 1:
            lines = lines[1:]
        m = re.match(r"(.+?)\s*-->\s*(\S+)", lines[0])
        if not m:
            continue
        start, end = parse_time(m.group(1)), parse_time(m.group(2))
        body = " ".join(l.strip() for l in lines[1:])
        cues.append({"i": len(cues) + 1, "start": round(start, 3),
                     "end": round(end, 3), "dur": round(end - start, 3),
                     "text": body})
    return cues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("srt")
    ap.add_argument("--json", help="write cues JSON to this path")
    ap.add_argument("--js", action="store_true", help="print only the JS snippet")
    args = ap.parse_args()

    cues = parse(args.srt)
    if not cues:
        print("no cues parsed", file=sys.stderr)
        sys.exit(1)
    total = cues[-1]["end"]

    js = "const CUES = " + json.dumps(
        [{"i": c["i"], "start": c["start"], "end": c["end"]} for c in cues],
        separators=(",", ":")) + f";  // total {total}s"

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(cues, f, ensure_ascii=False, indent=1)
        print(f"wrote {args.json}", file=sys.stderr)
    if args.js:
        print(js)
        return

    print(f"{len(cues)} cues · total {total}s · set data-duration >= {total + 1.5:.1f}")
    print(f"{'#':>3} {'start':>8} {'end':>8} {'dur':>6}  text")
    for c in cues:
        print(f"{c['i']:>3} {c['start']:>8.2f} {c['end']:>8.2f} {c['dur']:>6.2f}  {c['text'][:70]}")
    print("\n" + js)


if __name__ == "__main__":
    main()
