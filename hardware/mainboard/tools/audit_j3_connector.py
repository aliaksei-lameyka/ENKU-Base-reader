#!/usr/bin/env python3
"""Read-only ENKU KiCad J3 FPC footprint audit; no external dependencies.

Outputs pad 1..24 positions, nets, pad shape/dimensions, and orientation.
Rejects duplicate or missing signal pads. Mechanical tabs are reported separately.
Does NOT validate mating, pin-5 panel semantics, or manufacturer's land pattern.
"""
import argparse
import json
import re
from pathlib import Path


def balanced_expr(source: str, start: int) -> str:
    depth, string, escaped = 0, False, False
    for i in range(start, len(source)):
        ch = source[i]
        if string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                string = False
        elif ch == '"':
            string = True
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return source[start:i + 1]
    raise ValueError("Unterminated KiCad S-expression")


def sections(source: str, name: str):
    pat = re.compile(r'\(' + re.escape(name) + r'(?=[\s\)])')
    for match in pat.finditer(source):
        yield balanced_expr(source, match.start())


def field(block: str, name: str):
    match = re.search(r'\(' + re.escape(name) + r'\s+([^()]*)\)', block)
    return match.group(1).strip() if match else None


def audit(path: Path, reference: str):
    board = path.read_text(encoding="utf-8")
    fp = next((f for f in sections(board, "footprint")
               if re.search(r'\(property\s+"Reference"\s+"' + re.escape(reference) + r'"', f)
               or re.search(r'\(fp_text\s+reference\s+"' + re.escape(reference) + r'"', f)), None)
    if fp is None:
        raise ValueError(f"Footprint {reference} missing")
    header = re.match(r'\(footprint\s+"([^"]+)"', fp)
    rotation = field(fp, "at")
    side = field(fp, "layer")
    pads = []
    for p in sections(fp, "pad"):
        m = re.match(r'\(pad\s+"?([^"\s()]*)"?\s+(smd|thru_hole|np_thru_hole)\s+([^\s()]+)', p)
        if not m:
            continue
        num, kind, shape = m.groups()
        net_match = re.search(r'\(net\s+\d+\s+"([^"]+)"\)', p)
        pads.append(dict(number=num, kind=kind, shape=shape,
                         at=field(p, "at"), size=field(p, "size"),
                         net=net_match.group(1) if net_match else None))
    sig = [p for p in pads if p["number"].isdigit() and 1 <= int(p["number"]) <= 24]
    counts = {str(i): sum(p["number"] == str(i) for p in sig) for i in range(1, 25)}
    issues = [f"pad {i}: found {counts[str(i)]} (expected 1)" for i in range(1, 25)
              if counts[str(i)] != 1]
    issues += [f"pad {p['number']}: unassigned net" for p in sig if not p["net"]]
    result = dict(source=str(path), reference=reference,
                  footprint=header.group(1) if header else None,
                  layer=side, origin=rotation,
                  signal_pads=sorted(sig, key=lambda p: int(p["number"])),
                  other_pads=[p for p in pads if p not in sig],
                  errors=issues,
                  mechanical_and_mating_status="NOT VERIFIED",
                  epd_pin5_signal_status="SUPPLIER HOLD: VDHR vs VSH2")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcb", type=Path)
    ap.add_argument("--reference", default="J3")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    report = audit(args.pcb, args.reference)
    value = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(value, encoding="utf-8")
    else:
        print(value, end="")
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
