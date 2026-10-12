#!/usr/bin/env python3
"""R38 geometry gate; native KiCad DRC determines clearance and zone errors."""
from pathlib import Path
import re
from collections import Counter
HERE=Path(__file__).parent
PCB=(HERE/"enku-mainboard-r1.5-base-ground-return-island.kicad_pcb").read_text()
SEG=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([\d.]+)\) \(layer "(F|B)\.Cu"\) \(net (\d+)\)\)',PCB)
VIA=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([\d.]+)\) \(drill ([\d.]+)\) \(layers "F\.Cu" "B\.Cu"\) \(net (\d+)\)\)',PCB)
ZONE=re.findall(r'(?m)^  \(zone \(net (\d+)\) \(net_name "([^"]+)"\) \(layer "([^"]+)"\)',PCB)
assert PCB.count('(footprint "')==125
assert len(SEG)==48,len(SEG)
assert len(VIA)==13,len(VIA)
assert Counter(int(n) for *_,n in SEG)=={1:10,2:13,32:13,74:10,96:2}
assert Counter(int(n) for *_,n in VIA)=={1:7,2:3,32:3}
assert ZONE==[("1","GND","In2.Cu")],ZONE
assert '(polygon (pts (xy 40.5 80.2) (xy 67.0 80.2) (xy 67.0 99.5) (xy 40.5 99.5)))' in PCB
assert '(connect_pads (clearance 0.25))' in PCB
assert '(fill yes (thermal_gap 0.30) (thermal_bridge_width 0.30))' in PCB
def has_p(net,x,y):
    return any(int(v[4])==net and abs(float(v[0])-x)<0.001 and abs(float(v[1])-y)<0.001 for v in VIA)
for x,y in ((61.6,87.7),(65.1,86.5),(61.1,93.0),(65.1,94.0),(48.5,92.35),(50.6,90.9),(56,91)):
    assert has_p(1,x,y),(x,y)
assert not re.search(r'(?m)^  \(segment [^\n]+ \(net (?:1[3-9]|2\d|3[01])\)',PCB), "EPD panel HV/logic must await GoodDisplay"
print("R38 GND SOURCE PASS: 125 parts, 48 tracks, 13 vias (7 GND), single local In2.Cu GND zone; no EPD HV nets routed.")
print("NB: zone polygon present but NOT copper-filled/verified as functional plane; native KiCad clearance and plane fill still required before release.")
