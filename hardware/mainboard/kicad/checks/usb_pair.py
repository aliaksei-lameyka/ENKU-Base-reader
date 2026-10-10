"""Route a coupled USB envelope on B.Cu; convert it into physical D+/D- copper."""
import json,math,sys,copy
from pathlib import Path
import numpy as np
from shapely.geometry import LineString
from router import Router
root=Path(sys.argv[1]);c=root/'checks';g=json.loads((c/'geometry_current.json').read_text());pg=copy.deepcopy(g)
for p in pg['pads']+pg['tracks']:
 if p['net'] in ('USB_DM','USB_DP','USB_DM_CONN','USB_DP_CONN'):p['net']='PAIR'
r=Router(pg,layers=(2,));ms,vm=r.masks('PAIR',.8);vm[:]=True
fake=lambda xy:{'uuid':'endpoint','net':'PAIR','start':xy,'end':xy,'layer':2,'via':False}
S=[43.6,59.4];A=[43.6,60.0];B=[47,104.2];T=[47,104.8]
assert r.free_line(S,A,ms[0]) and r.free_line(B,T,ms[0]),'Reserved pair entry blocked'
p=r.route('PAIR',[fake(A)],[fake(B)],width=.8,timeout=55,masks=(ms,vm))
assert p is not None,'No continuous B.Cu coupled USB corridor'
pts=[A]+[s['b'] for s in p['segments']];simple=[pts[0]];i=0
while i<len(pts)-1:
 j=len(pts)-1
 while j>i+1 and not r.free_line(pts[i],pts[j],ms[0]):j-=1
 simple.append(pts[j]);i=j
centre=LineString([S]+simple+[T]);routes=[]
for net,offset,x,via0,via1 in [('USB_DM_CONN',.2,46.05,[42.98,58.7],[46.05,106.0]),('USB_DP_CONN',-.2,47.95,[44.25,58.7],[47.95,106.0])]:
 line=centre.offset_curve(offset,join_style='mitre',mitre_limit=2);assert line.geom_type=='LineString';pts=[list(q) for q in line.coords];start,end=pts[0],pts[-1];segments=[{'a':a,'b':b,'layer':2} for a,b in zip(pts,pts[1:])]
 # Symmetric connector and MCU breakouts; all plated holes outside the SMD lands.
 segments += [{'a':[via0[0],57.3],'b':via0,'layer':0},{'a':via0,'b':[start[0],58.7+abs(start[0]-via0[0])],'layer':2},{'a':[start[0],58.7+abs(start[0]-via0[0])],'b':start,'layer':2},{'a':end,'b':[x,104.8+abs(x-end[0])],'layer':2},{'a':[x,104.8+abs(x-end[0])],'b':via1,'layer':2},{'a':via1,'b':[x,107.35],'layer':0}]
 routes.append({'net':net,'width':.2,'via_diameter':.5,'segments':segments,'vias':[via0,via1],'coupled_length_mm':line.length,'length_mm':sum(math.dist(s['a'],s['b']) for s in segments)})
(c/'plan_usb_pair.json').write_text(json.dumps({'routes':routes,'centreline':list(centre.coords),'pair_width_mm':.2,'edge_gap_mm':.2,'impedance_qualified':False,'reference_plane':'In2.Cu; continuity requires independent fill audit'},indent=2));print('Paired USB',[(r['net'],round(r['length_mm'],3),round(r['coupled_length_mm'],3)) for r in routes],len(simple),'centre segments',flush=True)
