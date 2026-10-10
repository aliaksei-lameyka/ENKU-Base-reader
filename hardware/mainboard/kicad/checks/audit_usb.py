"""Verify USB topology, coupled geometry and actual native filled ground references."""
import json,sys,gzip,hashlib,math,collections,heapq
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,LineString,Point
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
fill=json.loads(gzip.decompress((out/'reference_planes_R121.json.gz').read_bytes()))
planes={int(k):sh.union_all([sh.make_valid(Polygon(a['shell'],a['holes'])) for a in v]) for k,v in fill.items()}
plan=json.loads((c/'accepted_usb_add.json').read_text());center=LineString(plan['centerline']);groups=partitions(g)
pads={(a['ref'],a['number']):a for a in g['pads'] if a['number']}
pin_map={('U1','13'):'USB_DM',('U1','14'):'USB_DP',('R64','1'):'USB_DP_CONN',('R64','2'):'USB_DP',('R65','1'):'USB_DM_CONN',('R65','2'):'USB_DM',('U8','1'):'USB_DP_CONN',('U8','6'):'USB_DP_CONN',('U8','3'):'USB_DM_CONN',('U8','4'):'USB_DM_CONN',('U8','2'):'GND',('U8','5'):'VBUS_USB',('J5','A6'):'USB_DP_CONN',('J5','B6'):'USB_DP_CONN',('J5','A7'):'USB_DM_CONN',('J5','B7'):'USB_DM_CONN'}
for key,net in pin_map.items():assert pads[key]['net']==net,(key,pads[key]['net'])
for net in ['USB_DM','USB_DP','USB_DM_CONN','USB_DP_CONN']:assert len(groups[net])==1,(net,groups[net])
usb=[t for t in g['tracks'] if t['net'].startswith('USB_D')]
# Expected own signal-via antipads: native zone clearance 0.25 mm plus 0.01 mm polygon margin.
voids=sh.union_all([Point(t['start']).buffer(t['width']/2+.26) for t in usb if t['via']]);missing=[]
for t in usb:
 if t['via'] or t['layer'] not in [0,2]:continue
 ref=4 if t['layer']==0 else 6;shape=LineString([t['start'],t['end']]).buffer(t['width']/2)
 delta=shape.difference(voids).difference(planes[ref])
 if delta.area>1e-6:missing.append({'uuid':t['uuid'],'net':t['net'],'signal_layer':t['layer'],'reference_layer':ref,'uncovered_area_mm2':delta.area,'bounds':list(delta.bounds)})
core_missing=center.buffer(.5,join_style=2).difference(planes[6]).area
def pt(v):return tuple(round(x,6) for x in v)
core={}
for net,side in [('USB_DM_CONN','left'),('USB_DP_CONN','right')]:
 coords=list(center.parallel_offset(.2,side,join_style=2).coords)
 if math.dist(coords[0],plan['centerline'][0])>math.dist(coords[-1],plan['centerline'][0]):coords.reverse()
 expected={frozenset((pt(a),pt(b))) for a,b in zip(coords,coords[1:])}
 actual=[t for t in usb if t['net']==net and not t['via'] and t['layer']==2 and frozenset((pt(t['start']),pt(t['end']))) in expected]
 assert len(actual)==len(expected) and all(t['width']==.2 for t in actual),('Coupled USB core geometry differs',net)
 core[net]=sh.union_all([LineString([t['start'],t['end']]) for t in actual])
gap=core['USB_DM_CONN'].distance(core['USB_DP_CONN'])-.2;assert abs(gap-.2)<2e-6,('USB core gap changed',gap)
def distances(net,source):
 edges=collections.defaultdict(list)
 for t in g['tracks']:
  if t['net']!=net or t['via']:continue
  a,b=pt(t['start']),pt(t['end']);length=math.dist(a,b);edges[a].append((b,length));edges[b].append((a,length))
 start=pt(source);best={start:0};q=[(0,start)]
 while q:
  d,k=heapq.heappop(q)
  if d!=best[k]:continue
  for nxt,l in edges[k]:
   if d+l<best.get(nxt,1e100):best[nxt]=d+l;heapq.heappush(q,(d+l,nxt))
 return best
lengths={};counts={};esd={}
for net,res,pin,contacts in [('USB_DM_CONN','R65','3',['A7','B7']),('USB_DP_CONN','R64','1',['A6','B6'])]:
 ds=distances(net,pads[(res,'1')]['pos']);lengths[net]={p:ds.get(pt(pads[('J5',p)]['pos'])) for p in contacts};esd[net]=ds[pt(pads[('U8',pin)]['pos'])]
 counts[net]=sum(t['via'] for t in usb if t['net']==net);assert counts[net]==2
 assert all(v is not None for v in lengths[net].values()),lengths
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
result={'revision':'R121','pcb_sha256':sha,'all_USB_pad_groups_connected':True,'polarity_and_ESD_pin_map_verified':True,'signal_vias_per_net':counts,'long_pair_layer':'B.Cu','reference_layer':'In2.Cu','coupled_width_mm':.2,'coupled_gap_mm':gap,'coupled_core_geometry_verified':True,'core_reference_strip_width_mm':1.0,'core_reference_missing_area_mm2':core_missing,'all_USB_trace_reference_missing_regions':missing,'centreline_lengths_from_series_resistors_to_ESD_mm':esd,'excluded_signal_via_antipads':'Via radius + 0.25 mm native zone clearance + 0.01 mm polygon approximation margin; exported zones are unfractured with native hole recovery','centreline_lengths_from_series_resistors_to_USB_contacts_mm':lengths,'orientation_A_skew_mm':lengths['USB_DP_CONN']['A6']-lengths['USB_DM_CONN']['A7'],'orientation_B_skew_mm':lengths['USB_DP_CONN']['B6']-lengths['USB_DM_CONN']['B7'],'length_measurement_scope':'Track centreline only, without pad spreading, package/via delay or stackup electromagnetic model. USB-C contact branches remain for impedance/bench review.','factory_stackup_confirmed':False,'impedance_qualified':False,'fabrication_ready':False}
(out/'usb_geometry_audit_R121.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
assert core_missing<1e-6 and not missing,'USB trace/reference projection must stay on filled GND outside declared signal-via antipads'
