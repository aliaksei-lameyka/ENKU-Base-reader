#!/usr/bin/env python3
"""Report KiCad DRC root causes and approximate routing hotspots.

A diagnostic only: NEVER turns a failed KiCad DRC into a passing gate.
Read a KiCad 8 plaintext DRC report and summarize error types, affected
nets, and approximate 5-mm location bins. Endpoint coordinates may be
reported as pad/segment anchors, not precise violation intersection points.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re

BLOCK = re.compile(r"(?ms)^\[([a-z_][a-z0-9_]*)\]:([^\n]*)(.*?)(?=^\[[a-z_][a-z0-9_]*\]:|\Z)")
POINT = re.compile(r"@\((-?\d+(?:\.\d+)?) mm, (-?\d+(?:\.\d+)?) mm\)")
NET = re.compile(r"\[([^\]]+)\]")
CRITICAL = ("shorting_items", "tracks_crossing", "clearance", "hole_clearance", "unconnected_items", "board_edge", "copper_edge_clearance")

def categorize(y: float) -> str:
    if y >= 114.0:
        return "R16 extension / bottom"
    if y >= 84.0:
        return "lower power / SD / USB"
    if y >= 55.0:
        return "button & middle"
    return "display / MCU / upper"

def analyze(report: str) -> tuple[Counter, Counter, Counter, Counter]:
    counts: Counter = Counter()
    critical_nets: Counter = Counter()
    regions: Counter = Counter()
    bins: Counter = Counter()
    for match in BLOCK.finditer(report):
        kind, heading, body = match.groups()
        counts[kind] += 1
        if kind not in CRITICAL:
            continue
        points = [(float(x), float(y)) for x, y in POINT.findall(body)]
        if points:
            # Both endpoint anchor coordinates count; do not pretend that
            # their centroid is the actual physical copper intersection.
            for x, y in points[:2]:
                regions[(kind, categorize(y))] += 1
                bins[(kind, int(x // 5) * 5, int(y // 5) * 5)] += 1
        nets = []
        for line in body.splitlines():
            if "@(" not in line:
                continue
            found = NET.findall(line)
            if found and found[0] not in nets:
                nets.append(found[0])
        if not nets and "nets " in heading:
            nets = [s.strip() for s in heading.split("nets ", 1)[1].rstrip(")").split(" and ")]
        for net in nets[:2]:
            critical_nets[(kind, net)] += 1
    return counts, critical_nets, regions, bins

def render(report: str, top: int) -> str:
    counts, nets, regions, bins = analyze(report)
    lines = [
        "# ENKU R16/R18 native KiCad DRC triage",
        "",
        "> Diagnostic output only. The native KiCad ERC/DRC gate remains authoritative.",
        "> Location bins identify reported endpoint anchors, NOT exact violation locations.",
        "",
        "## DRC issue types",
    ]
    for kind, n in counts.most_common():
        lines.append(f"- {kind}: {n}")
    lines += ["", "## Most affected critical endpoints (type / net)"]
    for (kind, net), n in nets.most_common(top):
        lines.append(f"- {kind} / {net}: {n}")
    lines += ["", "## Regional endpoint anchors (category / region)"]
    for (kind, region), n in regions.most_common(top):
        lines.append(f"- {kind} / {region}: {n}")
    lines += ["", "## Dense 5-mm endpoint bins (type / X / Y)"]
    for (kind, x, y), n in bins.most_common(top):
        lines.append(f"- {kind} / x={x}…{x+5} mm / y={y}…{y+5} mm: {n}")
    lines += ["", "**IMPORTANT:** A zero-ratsnest summary does not clear shorts, mask bridges, drill spacing or copper clearances.", ""]
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drc", type=Path, help="Text KiCad DRC report")
    parser.add_argument("--markdown", type=Path, help="Optional output file")
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()
    if not args.drc.is_file():
        parser.error(f"report not found: {args.drc}")
    output = render(args.drc.read_text(encoding="utf-8", errors="replace"), max(1, args.top))
    print(output)
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(output, encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
