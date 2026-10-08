#!/usr/bin/env python3
"""Silkscreen readability gate for ENKU Mainboard R0.1.

Checks visible footprint references and board text on F/B.SilkS for:
- text-to-text overlap on the same silkscreen layer;
- text bounding boxes too close to / outside the board edge.

This is intentionally conservative. Final release still requires Gerber visual review.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import re
import sys

HERE = Path(__file__).resolve().parent
PCB = HERE / "enku-mainboard-r0.1.kicad_pcb"
BOARD = (20.0, 20.0, 74.0, 114.0)
EDGE_MARGIN = 0.40
TEXT_MARGIN = 0.15

@dataclass(frozen=True)
class Text:
    label: str
    layer: str
    x: float
    y: float
    rot: float
    sx: float
    sy: float

def balanced_blocks(text: str, token: str):
    pos = 0
    while True:
        start = text.find(token, pos)
        if start < 0:
            return
        depth = 0
        ins = False
        esc = False
        end = None
        for i in range(start, len(text)):
            ch = text[i]
            if ins:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    ins = False
                continue
            if ch == '"':
                ins = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            return
        yield text[start:end]
        pos = end

def at_of(s: str):
    m = re.search(r'\(at\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)(?:\s+(-?\d+(?:\.\d+)?))?\)', s)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0.0)

def font_size(s: str):
    m = re.search(r'\(font\s+\(size\s+([\d.]+)\s+([\d.]+)\)', s)
    return (float(m.group(1)), float(m.group(2))) if m else (1.0, 1.0)

def rot_point(x, y, deg):
    t = math.radians(deg)
    c, sn = math.cos(t), math.sin(t)
    return x*c-y*sn, x*sn+y*c

def bbox(t: Text):
    # Approximate KiCad stroke-font text envelope. Width factor is deliberately generous.
    w = max(t.sx, len(t.label) * t.sx * 0.68)
    h = t.sy
    r = abs(t.rot % 180.0)
    if 45.0 < r < 135.0:
        w, h = h, w
    return (t.x-w/2, t.y-h/2, t.x+w/2, t.y+h/2)

def overlaps(a, b, margin=0.0):
    return not (
        a[2] + margin <= b[0] or b[2] + margin <= a[0] or
        a[3] + margin <= b[1] or b[3] + margin <= a[1]
    )

def footprint_texts(text: str):
    out = []
    for fp in balanced_blocks(text, "(footprint "):
        fa = at_of(fp)
        if not fa:
            continue
        fx, fy, frot = fa
        for prop in balanced_blocks(fp, '(property "Reference" '):
            if " hide" in prop:
                continue
            lm = re.search(r'\(layer "(F\.SilkS|B\.SilkS)"\)', prop)
            nm = re.search(r'\(property "Reference" "([^"]+)"', prop)
            pa = at_of(prop)
            if not lm or not nm or not pa:
                continue
            lx, ly, lrot = pa
            rx, ry = rot_point(lx, ly, frot)
            sx, sy = font_size(prop)
            out.append(Text(nm.group(1), lm.group(1), fx+rx, fy+ry, (frot+lrot)%360, sx, sy))
    return out

def board_texts(text: str):
    out = []
    for g in balanced_blocks(text, "(gr_text "):
        lm = re.search(r'\(layer "(F\.SilkS|B\.SilkS)"\)', g)
        nm = re.match(r'\(gr_text "([^"]*)"', g)
        ga = at_of(g)
        if not lm or not nm or not ga:
            continue
        sx, sy = font_size(g)
        out.append(Text(nm.group(1), lm.group(1), ga[0], ga[1], ga[2], sx, sy))
    return out

def main():
    if not PCB.is_file():
        print(f"ERROR: missing {PCB}")
        return 1
    raw = PCB.read_text(encoding="utf-8")
    texts = footprint_texts(raw) + board_texts(raw)
    errors = []
    x0,y0,x1,y1 = BOARD
    for t in texts:
        b = bbox(t)
        if b[0] < x0+EDGE_MARGIN or b[1] < y0+EDGE_MARGIN or b[2] > x1-EDGE_MARGIN or b[3] > y1-EDGE_MARGIN:
            errors.append(f"{t.layer}: '{t.label}' too close to board edge: bbox={tuple(round(v,2) for v in b)}")
    for i,a in enumerate(texts):
        ba=bbox(a)
        for b in texts[i+1:]:
            if a.layer != b.layer:
                continue
            bb=bbox(b)
            if overlaps(ba,bb,TEXT_MARGIN):
                errors.append(
                    f"{a.layer}: text overlap '{a.label}' @({a.x:.2f},{a.y:.2f}) "
                    f"with '{b.label}' @({b.x:.2f},{b.y:.2f})"
                )
    if errors:
        print("Silkscreen readability gate failed:")
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"Silkscreen readability gate passed: {len(texts)} visible labels checked")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
