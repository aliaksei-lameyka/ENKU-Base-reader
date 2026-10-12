#!/usr/bin/env python3
"""Active R42 source topology; Native KiCad remains electrical/clearance authority."""
import math,re
import check_r47_assembly as geom
B=geom.PCB
fps=geom.footprints()
pads=geom.pads(fps)
segments=[(float(a),float(b),float(c),float(d),layer,int(n)) for a,b,c,d,layer,n in re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width [\d.]+\) \(layer "([^"]+)"\) \(net (\d+)\)',B)]
vias=[(float(x),float(y),int(n)) for x,y,n in re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\).*\(net (\d+)\)',B)]
def connected(n,targets):
    parent={}
    def root(k):
        parent.setdefault(k,k)
        if parent[k]!=k:parent[k]=root(parent[k])
        return parent[k]
    def join(a,b):parent[root(a)]=root(b)
    def node(x,y,l):return (round(x,4),round(y,4),l)
    for x,y,u,v,l,net in segments:
        if net==n:join(node(x,y,l),node(u,v,l))
    for x,y,net in vias:
        if net==n:
            for l in ['F.Cu','In1.Cu','In2.Cu','B.Cu']:join(node(x,y,'F.Cu'),node(x,y,l))
    found=[]
    for ref,pin in targets:
        p=[p for p in pads if p[0]==ref and p[1]==pin]
        assert len(p)==1,(ref,pin,p)
        _,_,side,net,(x1,y1,x2,y2)=p[0]
        k=(ref,pin)
        # Pad contact based on endpoint inside copper rectangle; avoids same-net name-only false positives.
        for x,y,l in [k for k in parent if len(k)==3]:
            if l==side+'.Cu' and x1-1e-6<=x<=x2+1e-6 and y1-1e-6<=y<=y2+1e-6:join(k,(x,y,l))
        found.append(root(k))
    assert len(set(root(k) for k in found))==1,('DISCONNECTED',n,targets)
for n,targets in [(9,[('J2','2'),('R19','2'),('R23','2')]),(10,[('J2','3'),('R20','2')]),(11,[('J2','5'),('R21','2')]),(12,[('J2','7'),('R22','1')]),(2,[('J2','4'),('C16','1'),('C17','1'),('R23','1')]),(1,[('C16','2'),('C17','2')])]:connected(n,targets)
for n,targets in [(60,[('U1','18'),('R19','1')]),(61,[('U1','19'),('R20','1')]),(62,[('U1','20'),('R21','1')]),(63,[('U1','21'),('R22','2')])]:connected(n,targets)
# Execute the existing USB pin map assertions against the ACTUAL new board.
from pathlib import Path
source=(geom.HERE/'check_r40_sd_fanout.py').read_text()
source=source.replace('enku-mainboard-r1.7-base-sd-power-sclk-mosi.kicad_pcb','enku-mainboard-r2.4-base-four-reading-gpios.kicad_pcb').replace('len(segs)==63','len(segs)==515').replace('len(vias)==20','len(vias)==132').replace("B.count('(footprint \"')==125","B.count('(footprint \"')==132").replace('pin("U1","10")=="NC"','pin("U1","10")=="USB_VBUS_VALID"')
source='\n'.join(line for line in source.splitlines() if not line.startswith('print('))
exec(compile(source,'active-r47-usb-contract','exec'),{'__file__':str(geom.HERE/'check_r47_sd_connectivity.py')})
print('R47 CONNECTIVITY PASS: all four card SPI escapes reach series resistors; CS pull-up and both SD capacitors connected. All four MCU-side SPI routes also connected; reference-plane qualification remains pending.')

for n,targets in [(97,[('U10','1'),('R72','1'),('U1','10')]),(98,[('U10','3'),('R70','2'),('R71','1'),('C39','1')]),(99,[('U10','4'),('U10','5')]),(2,[('U10','6'),('C38','1'),('C16','1'),('C11','1')]),(3,[('C2','1'),('R70','1'),('R73','1')])]:connected(n,targets)
print('R47 VBUS ROUTES PASS: comparator sense/reference/output, GPIO17, switched supply, raw VBUS divider and discharge resistor are connected in source.')

for n,targets in [(4,[('J5','A5'),('R62','1')]),(5,[('J5','B5'),('R63','1')]),(3,[('J5','A4'),('J5','A9'),('C2','1'),('U2','7'),('U8','5')])]:connected(n,targets)
print('R47 USB POWER PASS: both CC pull-downs, both connector VBUS contact pairs, power mux input and ESD VBUS are routed.')
assert 'ENKU:USBLC6_2SC6_ST_SOT23_6L' in B
for pin,box in [('1',(54.75,109.45,55.95,110.05)),('2',(54.75,108.5,55.95,109.1)),('5',(52.45,108.5,53.65,109.1))]:
 actual=[p[4] for p in pads if p[0]=='U8' and p[1]==pin][0]
 assert all(abs(a-b)<1e-6 for a,b in zip(actual,box)),(pin,actual,box)
print('R47 ESD FOOTPRINT PASS: ST SOT23-6L pad numbering, 0.95 mm pitch and 1.2 x 0.6 mm lands verified on active PCB.')
