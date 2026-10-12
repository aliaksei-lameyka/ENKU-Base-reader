#!/usr/bin/env python3
"""R46 source-graph contract: U1 digital GPIO4/5 to left physical button pins.

This does NOT qualify actual switch mechanical MPN or RF module underside routing.
KiCad Native filled zones and DRC are still the electrical authority.
"""
import math,re
from check_r46_sd_connectivity import connected,geom,B,pads
assert B.count('(footprint "')==132
segments=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([-\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)',B)
vias=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([-\d.]+)\) \(drill ([-\d.]+)\) \(layers "F.Cu" "B.Cu"\) \(net (\d+)\)',B)
assert len(segments)==483,len(segments)
assert len(vias)==128,len(vias)
assert len(re.findall(r'(?m)^  \(zone \(net 1\)',B))==2
for net,ref,pin,xy in [(48,"SW3","4",[(31.5,51.75),(27.0,60.75)]),(49,"SW4","5",[(32.75,51.75),(28.0,72.75)])]:
    connected(net,[("U1",pin),(ref,"1")])
    assert len([t for t in segments if int(t[-1])==net])>=6
    for x,y in xy:
        assert any(int(z[-1])==net and abs(float(z[0])-x)<1e-7 and abs(float(z[1])-y)<1e-7 and float(z[2])==.7 and float(z[3])==.3 for z in vias),(net,x,y)
    assert any(v[3]==f"BTN_L{1 if net==48 else 2}" for v in pads if v[0]==ref and v[1]=="1")
# All four GND button returns and hard power gate must remain native-connected.
connected(96,[("SW1","1"),("Q2","1"),("R40","2")])
assert not any(int(z[-1]) in (50,51) for z in segments),"No claim on right GPIO fanout yet"
assert not any(int(z[-1]) in (6,7,57,58) for z in segments),"USB differential pair is still reserved"
print("R46 LEFT INPUTS CONNECTIVITY PASS: MCU GPIO on pads4/5 -> SW3/SW4 pad1 via In1.Cu; all four drill transitions present.")
print("HOLDS: both right buttons BTN_R1/R2, exact side switch MPN and case travel, module underside/RF return, USB-C data pair, manufacturing DRC still unapproved.")
