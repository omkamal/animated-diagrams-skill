#!/usr/bin/env python3
"""svg_prep.py — normalize Graphviz/Mermaid SVG output for GSAP animation.

Usage:
  svg_prep.py --from graphviz raw.svg -o scene.svg      # dot -Tsvg output
  svg_prep.py --from mermaid  raw.svg -o scene.svg      # mmdc flowchart (htmlLabels:false!)
  svg_prep.py --from mermaid-seq raw.svg -o scene.svg   # mmdc sequenceDiagram
  svg_prep.py --report scene.svg                        # print animatable id inventory
  svg_prep.py --wrap-camera scene.svg -o scene.svg      # wrap content in <g id="camera">

mermaid-seq normalization: messages get id msg-NN (+ class msg, msg--reply for
dashed replies) with data-dir="ltr|rtl" from x1/x2; labels msgtext-NN;
activation bars act-NN; lifelines class lifeline. Animate messages with
fade+directional slide (NOT drawSVG — mermaid keeps marker-end arrowheads,
which show at full length during a draw).

Normalization gives every node/edge a stable, predictable id:
  node-<name>   edge-<src>-<dst>   (lowercased, non-alnum → '-')
and strips fixed width/height (keeps viewBox) so the SVG scales in the
composition. Pure stdlib — no dependencies.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def q(tag):
    return f"{{{SVG_NS}}}{tag}"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-") or "x"


def strip_dimensions(root):
    for attr in ("width", "height"):
        if attr in root.attrib:
            del root.attrib[attr]


def prep_graphviz(root):
    """dot -Tsvg: <g class="node|edge"><title>a</title>… / <title>a->b</title>…"""
    count = {"node": 0, "edge": 0}
    for g in root.iter(q("g")):
        cls = g.get("class", "")
        title = g.find(q("title"))
        if title is None or title.text is None:
            continue
        name = title.text
        if cls == "node":
            g.set("id", f"node-{slug(name)}")
            count["node"] += 1
        elif cls == "edge":
            m = re.match(r"(.+?)\s*-[->]\s*(.+)", name)
            if m:
                g.set("id", f"edge-{slug(m.group(1))}-{slug(m.group(2))}")
                count["edge"] += 1
            # mark the path inside as the drawable edge
            p = g.find(q("path"))
            if p is not None:
                p.set("class", (p.get("class", "") + " edge").strip())
        g.remove(title)  # <title> renders as tooltip; not needed
    return count


def prep_mermaid(root):
    """mmdc output: nodes have id="flowchart-<name>-N"; edges class="edge …" or
    id like L-<src>-<dst>. Mermaid versions vary — normalize what we find."""
    count = {"node": 0, "edge": 0}
    for el in root.iter():
        eid = el.get("id", "")
        cls = el.get("class", "")
        m = re.match(r"^(?:flowchart|state|entity)-(.+?)-\d+$", eid)
        if m:
            el.set("id", f"node-{slug(m.group(1))}")
            el.set("class", (cls + " node").strip())
            count["node"] += 1
            continue
        m = re.match(r"^L[-_]([A-Za-z0-9_]+)[-_]([A-Za-z0-9_]+)(?:[-_]\d+)?$", eid)
        if m and (el.tag == q("path") or "edge" in cls):
            el.set("id", f"edge-{slug(m.group(1))}-{slug(m.group(2))}")
            el.set("class", (cls + " edge").strip())
            count["edge"] += 1
            continue
        if el.tag == q("path") and "flowchart-link" in cls:
            count["edge"] += 1
            el.set("class", (cls + " edge").strip())
    if root.find(f".//{q('foreignObject')}") is not None:
        print(
            "WARN: <foreignObject> labels found — re-run mmdc with config "
            '{"flowchart":{"htmlLabels":false}} so labels are real SVG <text>.',
            file=sys.stderr,
        )
    return count


def prep_mermaid_seq(root):
    """mmdc sequenceDiagram: lines class=messageLine0|1, texts class=messageText,
    rects class=activation*, actor lifelines class=actor-line (or *actor-line*)."""
    counts = {"msg": 0, "label": 0, "act": 0, "lifeline": 0}
    for el in root.iter():
        cls = el.get("class", "")
        if "messageLine" in cls:
            counts["msg"] += 1
            n = counts["msg"]
            el.set("id", f"msg-{n:02d}")
            extra = " msg--reply" if "messageLine1" in cls else ""
            el.set("class", (cls + " msg" + extra).strip())
            try:
                x1, x2 = float(el.get("x1", 0)), float(el.get("x2", 0))
                el.set("data-dir", "ltr" if x2 >= x1 else "rtl")
            except (TypeError, ValueError):
                pass
        elif "messageText" in cls:
            counts["label"] += 1
            el.set("id", f"msgtext-{counts['label']:02d}")
        elif "activation" in cls:
            counts["act"] += 1
            el.set("id", f"act-{counts['act']:02d}")
        elif "actor-line" in cls:
            counts["lifeline"] += 1
            el.set("class", (cls + " lifeline").strip())
    print(f"normalized: {counts['msg']} messages, {counts['label']} labels, "
          f"{counts['act']} activations, {counts['lifeline']} lifelines",
          file=sys.stderr)
    return counts


def wrap_camera(root):
    if any(g.get("id") == "camera" for g in root.iter(q("g"))):
        return False
    children = list(root)
    defs = [c for c in children if c.tag == q("defs")]
    rest = [c for c in children if c.tag != q("defs")]
    for c in rest:
        root.remove(c)
    cam = ET.SubElement(root, q("g"), {"id": "camera"})
    for c in rest:
        cam.append(c)
    # keep defs first
    for d in defs:
        root.remove(d)
        root.insert(0, d)
    return True


def report(root):
    nodes, edges, labels, other = [], [], [], []
    for el in root.iter():
        eid = el.get("id")
        if not eid:
            continue
        if eid.startswith("node-"):
            nodes.append(eid)
        elif eid.startswith("edge-"):
            edges.append(eid)
        elif eid.startswith("label-"):
            labels.append(eid)
        elif eid not in ("camera", "scene", "hud") and not eid.startswith("layer-"):
            other.append(eid)
    vb = root.get("viewBox", "?")
    print(f"viewBox: {vb}")
    print(f"nodes  ({len(nodes)}): {' '.join(sorted(nodes))}")
    print(f"edges  ({len(edges)}): {' '.join(sorted(edges))}")
    if labels:
        print(f"labels ({len(labels)}): {' '.join(sorted(labels))}")
    if other:
        print(f"other  ({len(other)}): {' '.join(sorted(other)[:40])}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("svg", help="input SVG file")
    ap.add_argument("--from", dest="source", choices=["graphviz", "mermaid", "mermaid-seq"])
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--wrap-camera", action="store_true")
    ap.add_argument("-o", "--output")
    args = ap.parse_args()

    tree = ET.parse(args.svg)
    root = tree.getroot()
    changed = False

    if args.source:
        strip_dimensions(root)
        if args.source == "graphviz":
            counts = prep_graphviz(root)
            print(f"normalized: {counts['node']} nodes, {counts['edge']} edges", file=sys.stderr)
        elif args.source == "mermaid":
            counts = prep_mermaid(root)
            print(f"normalized: {counts['node']} nodes, {counts['edge']} edges", file=sys.stderr)
        else:
            prep_mermaid_seq(root)
        changed = True
    if args.wrap_camera:
        if wrap_camera(root):
            print("wrapped content in <g id='camera'>", file=sys.stderr)
        changed = True
    if args.report:
        report(root)

    if changed:
        out = args.output or args.svg
        tree.write(out, encoding="unicode", xml_declaration=False)
        print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
