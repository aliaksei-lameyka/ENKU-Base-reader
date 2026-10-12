"""Check manufacturability constraints that same-net native DRC can miss."""
import json,sys,hashlib
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,Point,LineString
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
thermal=json.loads((c/"thermal_via_manifest_R134.json").read_text());thermal_ids={x["uuid"] for x in thermal["added_vias"]}
assert len(thermal_ids)==5
process=json.loads((out/"via_process_R134.json").read_text());process_map={x["uuid"]:x for x in process["vias"]}
revision=json.loads((c/'current_checkpoint.json').read_text())['revision']
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());old=json.loads((c/'geometry_R120_baseline.json').read_text()) if (c/'geometry_R120_baseline.json').exists() else json.loads(__import__('gzip').decompress((c/'geometry_checkpoint_R120.json.gz').read_bytes()));old_ids={t['uuid'] for t in old['tracks']};old_tracks={t['uuid']:t for t in old['tracks']};prior=json.loads((c/'physical_geometry_audit_R120.json').read_text());prior_ids={x['via_uuid'] for x in prior['findings']};vias=[t for t in g['tracks'] if t['via'] and (t['uuid'] not in old_ids or t['uuid'] in prior_ids or t['start']!=old_tracks[t['uuid']]['start'])];lands={p['uuid']:sh.union_all([Polygon(q) for ps in p['polygons'].values() for q in ps]) for p in g['pads'] if p['layers'] and p['number'] and not max(p['drill'])};bad=[];measures=[]
for v in vias:
 if v['uuid'] in thermal_ids:
  requested=next(x for x in thermal['added_vias'] if x['uuid']==v['uuid'])
  assert v['net']=='GND' and v['width']==.5 and v['drill']==.3 and v['start']==requested['position_mm']
  ep=next(x for x in g['pads'] if x['ref']=='U3' and x['number']=='17')
  assert lands[ep['uuid']].covers(Point(v['start']).buffer(.25)), 'Thermal annulus must lie wholly within EP'
  assert process_map[v['uuid']]['fill_requested'] and process_map[v['uuid']]['cap_requested'], 'Under-paste via requires explicit fill/cap requests'
  other_lands={u:z for u,z in lands.items() if u!=ep['uuid']}
 else:other_lands=lands
 near=min(((shape.distance(Point(v['start']))-v['width']/2,u) for u,shape in other_lands.items()),key=lambda q:q[0]);p=next(p for p in g['pads'] if p['uuid']==near[1]);measures.append({'via_uuid':v['uuid'],'net':v['net'],'pos':v['start'],'nearest_land':p['ref']+':'+p['number'],'annulus_to_land_mm':near[0]})
 if near[0]<.1-1e-6:bad.append(measures[-1])
tag=[p for p in g['pads'] if p['ref']=='J7' and p['number']];tag_bad=[];min_tag=1000
for t in g['tracks']:
 if not t['via'] and t['layer']!=2:continue
 shape=Point(t['start']) if t['via'] else LineString([t['start'],t['end']])
 for p in tag:
  if t['net']==p['net']:continue
  gap=shape.distance(lands[p['uuid']])-t['width']/2;min_tag=min(min_tag,gap)
  if gap<.508-1e-6:tag_bad.append({'uuid':t['uuid'],'net':t['net'],'contact':p['number'],'gap_mm':gap})
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
assert {v['uuid'] for v in vias if v['uuid'] in thermal_ids}==thermal_ids
result={'revision':revision,'exact_U3_five_filled_capped_under_EP_requests_verified':True,'ordinary_via_land_guard_unchanged_mm':.1,'U3_under_EP_process_approved':False,'pcb_sha256':sha,'baseline':'R120 geometry plus the preserved R120 audit of vias added since R118','new_vias_checked':len(vias),'new_or_relocated_vias_checked':len(vias),'new_via_to_SMD_annulus_minimum_mm':min(x['annulus_to_land_mm'] for x in measures),'required_annulus_to_land_mm':.1,'new_via_land_violations':bad,'all_B_side_foreign_tracks_and_vias_to_Tag_Connect_minimum_mm':min_tag,'required_Tag_Connect_foreign_copper_mm':.508,'Tag_Connect_violations':tag_bad,'findings':measures,'fabrication_ready':False}
(out/('physical_geometry_audit_'+revision+'.json')).write_text(json.dumps(result,indent=2));assert not bad and not tag_bad,result
print(json.dumps({k:v for k,v in result.items() if k!='findings'},indent=2))
