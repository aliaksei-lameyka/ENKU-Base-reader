#!/usr/bin/env python3
"""R45 remote slide gate to Q2 and GND return source-graph integrity.
Native KiCad after zone fill owns clearance, electrical continuity and 3D fit.
"""
from pathlib import Path
import math,re
from check_r45_sd_connectivity import connected,geom,B,pads
assert B.count('(footprint "')==132
segments=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([-\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)',B)
vias=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([-\d.]+)\) \(drill ([-\d.]+)\) \(layers "F.Cu" "B.Cu"\) \(net (\d+)\)',B)
assert len(segments)==471,len(segments)
assert len(vias)==124,len(vias)
assert len(re.findall(r'(?m)^  \(zone \(net 1\)',B))==2
assert re.search(r'\(net 96 "PWR_GATE"\)',B)
connected(96,[('SW1','1'),('Q2','1'),('R40','2')])
def via(n,x,y):
    assert any(int(v[4])==n and abs(float(v[0])-x)<1e-6 and abs(float(v[1])-y)<1e-6 and float(v[2])==.7 and float(v[3])==.3 for v in vias),(n,x,y)
via(96,26,31);via(96,53,79.5);via(1,47.5,36.5)
for n,layer,x,y,a,b in [
 (96,"F.Cu",27.3,29,26,31),(96,"F.Cu",53,79.5,53,81.55),
 (1,"F.Cu",33.7,29,45,29),(1,"F.Cu",45,29,47.5,31.5),
 (1,"F.Cu",47.5,31.5,47.5,36.5)
]:
 assert any(int(s[6])==n and s[5]==layer and list(map(float,s[:4]))==[x,y,a,b] for s in segments),(n,layer,x,y,a,b)
# The gate run is electrically high impedance. Do not mistake route continuity for
# EMC/noise qualification, PMOS safe turn-on or true pack isolation.
gate=[s for s in segments if int(s[6])==96 and s[5]=="B.Cu"]
length=sum(math.hypot(float(s[2])-float(s[0]),float(s[3])-float(s[1])) for s in gate)
assert 95<length<110,length
assert not any(int(s[6]) in (48,49,50,51) for s in segments),"Button signal routes must not be fictitiously claimed"
print("R45 PMOS GATE SOURCE PASS: SW1.1 -> Q2.1/R40.2 actual copper, remote gate B.Cu length_mm",round(length,2),"with two plated vias.")
print("R45 GND SOURCE PASS: SW1.2 -> plated GND via inside In1/In2 return polygons.")
print("BLOCKERS: very-long high-impedance gate EMI/noise and 100k bias, actual switch mechanical MPN, off power leakage/charging, 4 reader signal GPIOs, USB differential pair and full DRC.")
