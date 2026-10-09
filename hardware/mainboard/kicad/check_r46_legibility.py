#!/usr/bin/env python3
"""R46 verify literal on-board service/RF user text quality, not global silkscreen release."""
from pathlib import Path
import re
from check_r46_assembly import PCB,footprints
fps=footprints()
probes={f"TP{i}" for i in range(1,15)}
for ref in sorted(probes):
    assert ref in fps,ref
    body=fps[ref]["txt"]
    assert re.search(r'\(fp_text user "[^"]+" \(at 0 1\.8 0\) \(layer "B\.SilkS"\)\s+\(effects \(font \(size 0\.8 0\.8\) \(thickness 0\.12\)\)',body),ref
rf=fps['U1']['txt']
assert '(fp_text user "RF ANTENNA" (at 0 -9.7 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))' in rf
assert '(gr_text "ENKU BASE / OPEN HARDWARE" (at 47 112.4) (layer "B.SilkS")' in PCB
assert '(effects (font (size 0.8 0.8) (thickness 0.12)) (justify mirror))' in PCB
assert 'OPEN HARDWARE — VERIFY DRC/ERC BEFORE FAB' not in PCB
assert 'ANTENNA / KEEP OUT' not in PCB
assert len(re.findall(r'(?m)^  \(segment ',PCB))==483
assert len(re.findall(r'(?m)^  \(via ',PCB))==128
print("R46 LABEL SOURCE PASS: 14 rear repair/service probes 0.8mm; RF ANTENNA 0.8mm; ENKU Base board legend 0.8mm, source copper unchanged.")
print("Native KiCad DRC must still independently reject text_height and all critical clearance/mask errors; no Gerber release.")
