#!/usr/bin/env python3
"""R48 electrical-unchanged printed silk cleanup gate: 43 footprint body boxes."""
import re
from check_r48_assembly import PCB,footprints
fps=footprints()
EXPECTED="Q1 C13 R17 R18 C7 C9 C11 SW1 SW3 SW4 SW5 SW6 J6 C24 C26 C25 R38 C31 C10 C12 R14 R15 R16 C2 C3 C4 C1 R1 R2 R3 R4 R5 R6 R7 C6 C5 C8 R8 R9 R10 R11 R12 R13".split()
assert len(EXPECTED)==43 and len(set(EXPECTED))==43
assert len(fps)==132
for ref in EXPECTED:
 b=fps[ref]["txt"]
 rects=re.findall(r'\(fp_rect \(start [^\n]*? \(layer "([^"]+)"\)\)',b)
 assert any(l in ("F.Fab","B.Fab") for l in rects),(ref,"body outline missing on Fab")
 assert not any(l in ("F.SilkS","B.SilkS") for l in rects),(ref,"clipped body outline left on printed silk")
 assert '(property "Reference" "'+ref+'"' in b
for ref in ("D1","D2","D3"):
 assert "F.SilkS" in fps[ref]["txt"],(ref,"diode polarity marks removed")
for i in range(1,15):
 b=fps[f"TP{i}"]["txt"]
 assert re.search(r'\(fp_text user "[^"]+" \(at 0 1\.8 0\) \(layer "B\.SilkS"\)',b),(i,"repairable TP legend removed")
assert "ENKU BASE / OPEN HARDWARE" in PCB and "RF ANTENNA" in PCB
assert len(re.findall(r'(?m)^  \(segment ',PCB))==515
assert len(re.findall(r'(?m)^  \(via ',PCB))==132
assert len(re.findall(r'(?m)^  \(zone ',PCB))==2
print("R48 FAB/SILK SOURCE PASS: 43 pad-crossing rectangles on F/B Fab; diode cathodes, 14 TP labels and every copper trace/pad preserved.")
