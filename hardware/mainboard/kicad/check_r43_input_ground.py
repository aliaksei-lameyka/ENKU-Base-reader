#!/usr/bin/env python3
"""R43 four reading-button GND-plane fanouts: robust source-level constraints.

Native KiCad re-fill + complete ERC/priority DRC is the actual electrical authority.
The case-edge switch footprint remains provisional; these are pilot paths only.
"""
import re
from check_r43_assembly import PCB,footprints,pads
fps=footprints()
pp=pads(fps)
assert len(fps)==132
tracks=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([-\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)',PCB)
vias=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([-\d.]+)\) \(drill ([-\d.]+)\) \(layers "([^"]+)" "([^"]+)"\) \(net (\d+)\)',PCB)
assert len(tracks)==442,len(tracks)
assert len(vias)==121,len(vias)
assert len(re.findall(r'(?m)^  \(zone \(net 1\) \(net_name "GND"\)',PCB))==2
for ref,x,y,vx,vy in [
 ("SW3",25,65.2,28,65.2),("SW4",25,77.2,28,77.2),
 ("SW5",71.2,65.2,68,65.2),("SW6",71.2,77.2,68,77.2)
]:
    pad=[p for p in pp if p[0]==ref and p[1]=="2"]
    assert len(pad)==1,(ref,pad)
    assert pad[0][3]=="GND",(ref,pad)
    xmin,ymin,xmax,ymax=pad[0][4]
    assert xmin<=x<=xmax and ymin<=y<=ymax,ref
    assert any(float(a)==x and float(b)==y and float(c)==vx and float(d)==vy and layer=="F.Cu" and n=="1" for a,b,c,d,w,layer,n in tracks),ref
    assert any(float(a)==vx and float(b)==vy and size=="0.70" and drill=="0.30" and net=="1" for a,b,size,drill,l1,l2,net in vias),ref
    assert 27+0.7<vx<69-0.7,(ref,"pilot GND via outside two native-filled reference zones")
for a,b,c,d in [(25,65.2,25,64),(25,77.2,22,76.225),(25,77.2,24,79.225)]:
    assert any(float(x)==a and float(y)==b and float(u)==c and float(v)==d and lay=="F.Cu" and n=="1" for x,y,u,v,w,lay,n in tracks)
for ref,pin,net in [('C26','2','GND'),('C18','2','GND'),('C19','2','GND'),('SW3','1','BTN_L1'),('SW4','1','BTN_L2'),('SW5','1','BTN_R1'),('SW6','1','BTN_R2')]:
    assert any(p[0]==ref and p[1]==pin and p[3]==net for p in pp),(ref,pin,net)
assert not any(t[-1] in ('48','49','50','51') for t in tracks), "Do not imply physical switch signal path: real side-button MPN still TBD"
assert not any(t[-1] in ('6','7','57','58') for t in tracks),"USB D+/D- pair must remain unrouted until PCBWay stackup qualification"
print("R43 FOUR BUTTON GND SOURCE PASS: SW3..SW6 pad2 to inner GND via, near C26/C18/C19 ground joined, 132 footprints, 442 tracks, 121 vias.")
print("RELEASE HOLD: SW3..SW6 provisional mechanical land patterns not production-footprint approved, side-button GPIO nets, PWR_GATE SW1 and USB differential pair still need routing.")
