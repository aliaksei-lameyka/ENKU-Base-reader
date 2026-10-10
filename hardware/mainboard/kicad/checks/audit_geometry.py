"""Check manufacturability constraints that same-net native DRC can miss."""
import json,sys,hashlib
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,Point,LineString
r=Path(sys.argv[1]).resolve();c=r/'checks';g=json.loads((c/'geometry_current.json').read_text());old=json.loads((c/'geometry_R120_baseline.json').read_text()) if (c/'geometry_R120_baseline.json').exists() else json.loads(__import__('gzip').decompress((c/'geometry_checkpoint_R120.json.gz').read_bytes()));old_ids={t['uuid'] for t in old['tracks']};prior=json.loads((c/'physical_geometry_audit_R120.json').read_text());prior_ids={x['via_uuid'] for x in prior['findings']};vias=[t for t in g['tracks'] if t['via'] and (t['uuid'] not in old_ids or t['uuid'] in prior_ids)];lands={p['uuid']:sh.union_all([Polygon(q) for ps in p['polygons'].values() for q in ps]) for p in g['pads'] if p['layers'] and p['number'] and not max(p['drill'])};bad=[];measures=[]
for v in vias:
 near=min(((shape.distance(Point(v['start']))-v['width']/2,u) for u,shape in lands.items()),key=lambda q:q[0]);p=next(p for p in g['pads'] if p['uuid']==near[1]);measures.append({'via_uuid':v['uuid'],'net':v['net'],'pos':v['start'],'nearest_land':p['ref']+':'+p['number'],'annulus_to_land_mm':near[0]})
 if near[0]<.1-1e-6:bad.append(measures[-1])
tag=[p for p in g['pads'] if p['ref']=='J7' and p['number']];tag_bad=[];min_tag=1000
for t in g['tracks']:
 if not t['via'] and t['layer']!=2:continue
 shape=Point(t['start']) if t['via'] else LineString([t['start'],t['end']])
 for p in tag:
  if t['net']==p['net']:continue
  gap=shape.distance(lands[p['uuid']])-t['width']/2;min_tag=min(min_tag,gap)
  if gap<.508-1e-6:tag_bad.append({'uuid':t['uuid'],'net':t['net'],'contact':p['number'],'gap_mm':gap})
result={'revision':r.name.removeprefix('ENKU_'),'pcb_sha256':hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),'baseline':'R120 geometry plus the preserved R120 audit of vias added since R118','new_vias_checked':len(vias),'new_via_to_SMD_annulus_minimum_mm':min(x['annulus_to_land_mm'] for x in measures),'required_annulus_to_land_mm':.1,'new_via_land_violations':bad,'all_B_side_foreign_tracks_and_vias_to_Tag_Connect_minimum_mm':min_tag,'required_Tag_Connect_foreign_copper_mm':.508,'Tag_Connect_violations':tag_bad,'findings':measures,'fabrication_ready':False}
(c/('physical_geometry_audit_'+r.name.removeprefix('ENKU_')+'.json')).write_text(json.dumps(result,indent=2));assert not bad and not tag_bad,result
print(json.dumps({k:v for k,v in result.items() if k!='findings'},indent=2))

