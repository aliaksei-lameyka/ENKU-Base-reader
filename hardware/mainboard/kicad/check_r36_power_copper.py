#!/usr/bin/env python3
"""R36 local first-copper mandatory geometry/net gate, not a production release."""
from pathlib import Path
import re
HERE=Path(__file__).parent
B=(HERE/"enku-mainboard-r1.3-base-first-power-copper.kicad_pcb").read_text()
SEG=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([\d.]+)\) \(layer "(F|B)\.Cu"\) \(net (\d+)\)\)',B)
VIA=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([\d.]+)\) \(drill ([\d.]+)\) \(layers "F\.Cu" "B\.Cu"\) \(net (\d+)\)\)',B)
assert B.count('(footprint "')==125
assert len(SEG)==18,len(SEG)
assert len(VIA)==1 and VIA[0]==("48.6","83.7","0.70","0.30","32"),VIA
assert sorted({int(s[6]) for s in SEG})==[32,74,96]
assert {int(s[6]) for s in SEG if s[5]=="B"}=={32}
assert min(float(s[4]) for s in SEG)>=0.18
for x1,y1,x2,y2,w,side,net in SEG:
    for x,y in ((float(x1),float(y1)),(float(x2),float(y2))):
        assert 47<x<70 and 79<y<92.5,(net,side,x,y)
    assert int(net) in {32,74,96}
key={(int(n),layer,round(float(x1),3),round(float(y1),3),round(float(x2),3),round(float(y2),3)) for x1,y1,x2,y2,w,layer,n in SEG}
def exists(n,layer,x,y):
    return any(k[0]==n and k[1]==layer and ((k[2],k[3])==(x,y) or (k[4],k[5])==(x,y)) for k in key)
for n,layer,x,y in [
    (96,"F",51.3,82.5),(96,"F",54.5,81.55),
    (32,"F",49.7,82.5),(32,"F",54.5,83.45),
    (32,"F",48.6,83.7),(32,"B",48.6,83.7),
    (32,"B",63.0,88.5),
    (74,"F",56.5,82.5),(74,"F",58.7,87.7),
    (74,"F",57.1,90.0),(74,"F",58.75,90.0),(74,"F",62.2,86.5)
]:
    assert exists(n,layer,x,y),(n,layer,x,y)
assert 'EPD_VSH2' in B and not any(int(s[6]) in (13,14,15,23,24,25,26,27,28,29,30,31) for s in SEG)
assert not re.search(r'(?m)^  \(zone\b',B)
print("R36 FIRST COPPER SOURCE PASS: 18 tracks (F/B) + 1 through-via; exactly gate/VSYS/SYS_EN nets; 125 footprints; no EPD/FPC copper, no filled zones.")
print("FAB BLOCKED: native DRC, thermal load currents, full power routing, 263+ other open links, FPC supplier hold and PCBWay BOM.")
