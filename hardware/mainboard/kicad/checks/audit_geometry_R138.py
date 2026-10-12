"""Check every via against every SMD land; six finite fill/cap exceptions only."""
import json,sys
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,Point,LineString
r,out=(Path(x).resolve()for x in sys.argv[1:3]);c=r/'checks'
g=json.loads((out/'geometry.json').read_text());vias={v['uuid']:v for v in g['tracks']if v['via']}
pm={v['uuid']:v for v in json.loads((out/'via_process_R138.json').read_text())['vias']}
u3=json.loads((c/'thermal_via_manifest_R138.json').read_text())['added_vias'];r28=json.loads((c/'R28_via_in_pad_manifest_R138.json').read_text())
caps={v['uuid']:dict(v,ref='U3',pin='17')for v in u3};caps[r28['uuid']]=r28
assert len(vias)==329 and len(caps)==6
assert {u for u,v in pm.items()if v['fill_requested']or v['cap_requested']}==caps.keys(),'Unexpected via process exception'
all_lands={p['uuid']:sh.union_all([Polygon(q)for ps in p['polygons'].values()for q in ps])for p in g['pads']if p['layers']and p['number']and not max(p['drill'])}
# SMD lands receive solder; bare-PCB Tag Connect contacts have their own
# independent0.508mm foreign-copper contact guard below.
lands={p['uuid']:all_lands[p['uuid']]for p in g['pads']if p['attribute']==1 and p['number']}
rows=[]
for u,v in vias.items():
 if u in caps:
  m=caps[u];p=next(p for p in g['pads']if p['ref']==m['ref']and p['number']==m['pin'])
  assert v['start']==m['position_mm']and v['width']==m['land_mm']and v['drill']==m['drill_mm']and v['net']==m['net']
  assert lands[p['uuid']].covers(Point(v['start']).buffer(v['width']/2,quad_segs=128)),'Filled capped via must be wholly inside its nominated land'
  a=pm[u];assert a['fill_requested']and a['cap_requested']and not a['front_tented']and a['back_tented'],'Exact filled capped construction request missing'
 else:
  gap,pad=min((shape.distance(Point(v['start']))-v['width']/2,pad)for pad,shape in lands.items())
  assert gap>=.1-1e-6,('Ordinary via too close to SMD land',u,pad,gap)
  rows.append(dict(uuid=u,position_mm=v['start'],net=v['net'],nearest_land_uuid=pad,annulus_to_SMD_gap_mm=gap))
assert len(rows)==323
tag=[p for p in g['pads']if p['ref']=='J7'and p['number']];tag_min=1000
for t in g['tracks']:
 if not t['via']and t['layer']!=2:continue
 shape=Point(t['start'])if t['via']else LineString([t['start'],t['end']])
 for p in tag:
  if t['net']==p['net']:continue
  gap=shape.distance(all_lands[p['uuid']])-t['width']/2;tag_min=min(tag_min,gap)
  assert gap>=.508-1e-6,('Tag Connect foreign copper gap',t['uuid'],gap)
report=dict(revision='R138',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],all_native_vias_checked=329,ordinary_vias_checked=323,ordinary_minimum_SMD_gap_mm=min(x['annulus_to_SMD_gap_mm']for x in rows),required_SMD_gap_mm=.1,exact_U3_five_and_R28_one_filled_capped_requests_verified=True,all_B_side_foreign_copper_to_Tag_Connect_minimum_mm=tag_min,findings=rows,actual_fill_cap_process_approved=False,fabrication_ready=False)
(out/'physical_geometry_audit_R138.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS all329 via-land clearances and six finite process requests')
