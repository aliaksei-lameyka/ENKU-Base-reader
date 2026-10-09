#!/usr/bin/env python3
"""R48 full source-copper graph for all four ENKU Base reading buttons.

Production approval still requires Native KiCad filled zone/DRC and actual
manufacturer-qualified case-edge button footprints/ESP32 RF keepout.
"""
import re
from check_r48_sd_connectivity import connected,geom,B,pads
assert B.count('(footprint "')==132
traces=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([-\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)',B)
vias=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([-\d.]+)\) \(drill ([-\d.]+)\) \(layers "F.Cu" "B.Cu"\) \(net (\d+)\)',B)
assert len(traces)==515,len(traces)
assert len(vias)==132,len(vias)
assert len(re.findall(r'(?m)^  \(zone \(net 1\)',B))==2
for net,mpin,sw,coords,layer in [
 (48,"4","SW3",[(31.5,51.75),(27,60.75)],"In1.Cu"),
 (49,"5","SW4",[(32.75,51.75),(28,72.75)],"In1.Cu"),
 (50,"6","SW5",[(34,50.5),(68,60.75)],"B.Cu"),
 (51,"7","SW6",[(36.5,51.5),(69.75,72.75)],"B.Cu"),
]:
 connected(net,[('U1',mpin),(sw,'1')])
 assert any(int(s[-1])==net and s[-2]==layer for s in traces),(net,layer)
 assert any(int(s[-1])==net and s[-2]=="F.Cu" for s in traces),(net,"F.Cu")
 for x,y in coords:
  assert any(int(v[-1])==net and abs(float(v[0])-x)<1e-6 and abs(float(v[1])-y)<1e-6 and float(v[2])==.7 and float(v[3])==.3 for v in vias),(net,x,y)
for sw,net in [('SW3','BTN_L1'),('SW4','BTN_L2'),('SW5','BTN_R1'),('SW6','BTN_R2')]:
 assert any(p[0]==sw and p[1]=='1' and p[3]==net for p in pads),(sw,net)
connected(96,[('SW1','1'),('Q2','1'),('R40','2')])
assert not any(int(t[-1]) in (6,7,57,58) for t in traces),"Native USB2 differential pair must remain un-routed pending stackup"
print('R48 FOUR READER BUTTONS SOURCE PASS: all ESP32 pads4..7 connected on F/B/In1 to SW3..SW6 pad1; 8 signal plated via transitions.')
print('BLOCKERS: actual side-switch MPN and actuator/housing, module underside RF keepout, 90-ohm USB2, full fab DRC, EPD supplier FPC response.')
