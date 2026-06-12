#!/usr/bin/env python3
"""code_to_svg.py — render Python source as a semantic, animatable SVG fragment.

Usage:
  code_to_svg.py file.py [-o fragment.svg] [--font-size 26] [--x 120]
                 [--y 120] [--start 1] [--end 9999] [--no-style]

Emits one <g class="code-line" id="line-N"> per source line (real line
numbers), tokens wrapped in <tspan class="tok-*"> (kw, def, builtin, str,
num, comment, deco, op), plus a ready highlight bar <rect id="code-hl">.
Paste the fragment into a layer inside #camera, then animate:
  - highlight: gsap.to("#code-hl", { attr: { y: lineY(n), height: H*k } })
  - focus:     dim .code-line groups, brighten the active range
  - camera:    camPanTo(tl, cx, lineCenterY, zoom) — vertical-scroll pattern
Line N center y = Y + (N - START) * LH + LH/2 (constants printed on exit).
Pure stdlib (tokenize) — Python only.
"""
import argparse
import builtins
import io
import keyword
import sys
import tokenize
from xml.sax.saxutils import escape

BUILTINS = set(dir(builtins))


def classify(tok_type, string, prev):
    if tok_type == tokenize.COMMENT:
        return "comment"
    if tok_type == tokenize.STRING or tok_type == tokenize.FSTRING_START:
        return "str"
    if tok_type == tokenize.NUMBER:
        return "num"
    if tok_type == tokenize.OP:
        return "deco" if string == "@" else "op"
    if tok_type == tokenize.NAME:
        if keyword.iskeyword(string) or keyword.issoftkeyword(string):
            return "kw"
        if prev in ("def", "class"):
            return "def"
        if prev == "@":
            return "deco"
        if string in BUILTINS:
            return "builtin"
    return "plain"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source")
    ap.add_argument("-o", "--output")
    ap.add_argument("--font-size", type=float, default=26)
    ap.add_argument("--x", type=float, default=120)
    ap.add_argument("--y", type=float, default=120)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=10**9)
    ap.add_argument("--no-style", action="store_true")
    args = ap.parse_args()

    src = open(args.source, encoding="utf-8").read()
    lines = src.splitlines()
    args.end = min(args.end, len(lines))
    LH = round(args.font_size * 1.6, 1)
    GUTTER = args.font_size * 3.2  # line numbers column

    # token spans per (line, col) — tokenize gives precise positions
    spans = {}  # lineno -> list[(col_start, col_end, cls)]
    prev_name = ""
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            t, string, (srow, scol), (erow, ecol), _ = tok
            if t in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                     tokenize.DEDENT, tokenize.ENDMARKER, tokenize.ENCODING):
                continue
            cls = classify(t, string, prev_name)
            if t in (tokenize.NAME, tokenize.OP):
                prev_name = string
            if srow == erow:
                spans.setdefault(srow, []).append((scol, ecol, cls))
            else:  # multi-line string: tag every covered line fully
                for r in range(srow, erow + 1):
                    line_len = len(lines[r - 1]) if r - 1 < len(lines) else 0
                    a = scol if r == srow else 0
                    b = ecol if r == erow else line_len
                    spans.setdefault(r, []).append((a, b, cls))
    except tokenize.TokenError:
        pass  # incomplete code is fine — render what we classified

    out = []
    if not args.no_style:
        out.append("""<style>
  .code-line text { font-family: var(--font-mono, "JetBrains Mono", monospace); white-space: pre; }
  .code-line .ln  { fill: var(--text-muted); opacity: .55; }
  .tok-plain   { fill: var(--text); }
  .tok-kw      { fill: var(--tok-kw, #7c3aed); font-weight: 600; }
  .tok-def     { fill: var(--tok-def, #2563eb); font-weight: 600; }
  .tok-builtin { fill: var(--tok-builtin, #0891b2); }
  .tok-str     { fill: var(--tok-str, #059669); }
  .tok-num     { fill: var(--tok-num, #ea580c); }
  .tok-comment { fill: var(--tok-comment, #94a3b8); font-style: italic; }
  .tok-deco    { fill: var(--tok-deco, #c026d3); }
  .tok-op      { fill: var(--text-muted); }
  #code-hl     { fill: var(--accent); opacity: 0; pointer-events: none; }
</style>""")
    n_shown = args.end - args.start + 1
    out.append(f'<rect id="code-hl" x="{args.x - 14}" y="{args.y - args.font_size}" '
               f'width="1400" height="{LH}" rx="6" opacity="0"/>')
    out.append('<g id="code-block">')
    for i, n in enumerate(range(args.start, args.end + 1)):
        text = lines[n - 1]
        y = args.y + i * LH
        pieces = [f'<tspan class="ln">{n:>4} </tspan>']
        col = 0
        for a, b, cls in sorted(spans.get(n, [])):
            if a > col:
                pieces.append(f'<tspan class="tok-plain">{escape(text[col:a])}</tspan>')
            pieces.append(f'<tspan class="tok-{cls}">{escape(text[a:b])}</tspan>')
            col = b
        if col < len(text):
            pieces.append(f'<tspan class="tok-plain">{escape(text[col:])}</tspan>')
        out.append(f'<g class="code-line" id="line-{n}">'
                   f'<text xml:space="preserve" x="{args.x - GUTTER}" y="{y}" '
                   f'font-size="{args.font_size}">{"".join(pieces)}</text></g>')
    out.append("</g>")

    frag = "\n".join(out)
    if args.output:
        open(args.output, "w", encoding="utf-8").write(frag)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(frag)
    print(f"lines {args.start}..{args.end} ({n_shown}) · LH={LH} · "
          f"lineY(n) = {args.y} + (n-{args.start})*{LH} · "
          f"block height ≈ {n_shown * LH:.0f}px — set canvas/scene accordingly",
          file=sys.stderr)


if __name__ == "__main__":
    main()
