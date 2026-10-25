#!/usr/bin/env python3
"""Rebuild M03 placement-only board from R148. Legacy copper remains STALE. NO FAB."""
import hashlib
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"r148"/"kicad"/"enku-mainboard-r0.1.kicad_pcb"
OUT=ROOT/"r149"/"kicad"
OLD="bb0aa41324b73ec13c087ab1c669c57c6bc6fd449621bf3aa34a53d3901b9476"
NEW="764cbe8258df7e76f14936407ecabc2fa86e8a80bdc42c01774b26bb23dcc977"
MOVES={
 "J3":("69.27 34","69.4600 94.2200"),
 "J5":("47 117.325","65.0000 117.3250"),
 "SW3":("21.55 73 -90","21.5500 68.0000 -90"),
 "SW4":("21.55 85 -90","21.5500 80.0000 -90"),
 "SW5":("73.45 73 90","73.4500 68.0000 90"),
 "SW6":("73.45 85 90","73.4500 80.0000 90")}
raw=BASE.read_bytes()
assert hashlib.sha256(raw).hexdigest()==OLD,"R148 base changed; abort"
s=raw.decode("utf-8")
starts=[m.start() for m in re.finditer(r"^\t\(",s,re.M)]+[len(s)]
edits=[];found=set()
for i,j in zip(starts,starts[1:]):
    b=s[i:j]
    if not b.startswith("\t(footprint"):continue
    m=re.search(r'\(property "Reference" "([^"]+)"',b)
    if m and m.group(1) in MOVES:
        ref=m.group(1);p,q=MOVES[ref]
        assert "(at "+p+")" in b[:m.start()],ref
        edits.append((i,j,b.replace("(at "+p+")","(at "+q+")",1)))
        found.add(ref)
assert found==set(MOVES),found
for i,j,b in reversed(edits):s=s[:i]+b+s[j:]
s=s.replace('(rev "R148 - ENGINEERING / NO FAB")',
            '(rev "R149-P0 M03 PLACEMENT ONLY / NO FAB")',1)
s=s.replace('(date "2026-10-15")','(date "2026-10-25")',1)
out=s.encode("utf-8")
assert hashlib.sha256(out).hexdigest()==NEW,"R149 output differs; abort"
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"enku-mainboard-r0.1.kicad_pcb").write_bytes(out)
print("R149-P0 staged (UNROUTED/NO FAB):",NEW)
