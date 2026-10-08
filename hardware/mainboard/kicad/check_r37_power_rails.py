#!/usr/bin/env python3
"""R37 source integrity: charger SYS -> high-side PMOS + output decouplers.

This verifies track records and their intended pad/via topology, not DRC,
thermal capability, plane connectivity or fab readiness. Native KiCad owns DRC.
"""
from pathlib import Path
import re
from collections import Counter
HERE=Path(__file__).resolve().parent
PCB=(HERE/"enku-mainboard-r1.4-base-charger-output-trial.kicad_pcb").read_text()
TR=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([\d.]+)\) \(layer "(F|B)\.Cu"\) \(net (\d+)\)\)',PCB)
VIA=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([\d.]+)\) \(drill ([\d.]+)\) \(layers "F\.Cu" "B\.Cu"\) \(net (\d+)\)\)',PCB)
assert PCB.count('(footprint "')==125,PCB.count('(footprint "')
assert len(TR)==38,len(TR)
assert len(VIA)==6,len(VIA)
assert Counter(int(x[6]) for x in TR)=={32:12,74:9,96:2,2:15},Counter(int(x[6]) for x in TR)
assert Counter(int(x[4]) for x in VIA)=={32:3,2:3},Counter(int(x[4]) for x in VIA)
assert not re.search(r'(?m)^  \(zone\b',PCB),"No real filled return plane yet"
def trpoint(net,layer,x,y):
    return any(int(t[6])==net and t[5]==layer and (t[0]==str(x) and t[1]==str(y) or t[2]==str(x) and t[3]==str(y)) for t in TR)
def viapoint(net,x,y):
    return any(int(v[4])==net and float(v[0])==x and float(v[1])==y for v in VIA)
# Actual KiCad BQ25185 copper output pin, two input caps and testpoint:
for net,layer,x,y in [
    (32,"F",49.6,91.8),  # U3.1 = VSYS
    (32,"F",51,94.5),    # C7.1 = VSYS
    (32,"B",49.8,92.3), # charger breakout via
    (32,"B",48.6,83.7), # join earlier PMOS source trunk
    (2,"F",58.75,92),   # U4.6 3V3 output
    (2,"F",59.1,94.4),  # C11.1 3V3
    (2,"F",62.3,94.4),  # C12.1 3V3
    (2,"F",55.3,89.1),  # R14.1 feedback source
    (2,"B",60,88.5),    # TP6, exposed B.Cu
    (2,"B",59,92.6)     # deliberate B.Cu tee
]:
    assert trpoint(net,layer,x,y),(net,layer,x,y)
for net,x,y in [(32,49.8,92.3),(32,51,96.5),(2,58.1,96.4),(2,62.3,95.9),(2,56.3,89.1)]:
    assert viapoint(net,x,y),(net,x,y)
for t in TR:
    x1,y1,x2,y2,w,layer,net=t
    for x,y in ((float(x1),float(y1)),(float(x2),float(y2))):
        assert 18<=x<=77 and 20<=y<=121
    assert float(w)>=.18
assert 'EPD_VSH2' in PCB
print("R37 SOURCE PASS: 38 tracks, 6 plated vias, 125 components; charger SYS/PMOS and local 3V3 links present, no EPD routing or GND plane.")
print("FAB BLOCKED: native DRC/courtyard/3D, charger stability/off leakage, 260+ unrouted, 4-layer return plane, panel vendor pin5/flex.")
