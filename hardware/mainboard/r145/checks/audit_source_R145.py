"""R145 finite reviewed routing delta against immutable R144; no historical golden changes."""
from pathlib import Path
import copy,hashlib,json,sys,math,xml.etree.ElementTree as E
import shapely as sh
from shapely.geometry import Polygon,Point
r,o,ref,scope=map(lambda s:Path(s).resolve(),sys.argv[1:5]);s=json.load(open(scope));g=json.load(open(o/'geometry.json'));old=json.load(open(o/'reference_R144_geometry.json'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'enku-mainboard-r0.1.kicad_pcb')==s['current_pcb_sha256'];assert sha(ref/'enku-mainboard-r0.1.kicad_pcb')==s['reference_R144_pcb_sha256']
def cleaned(a):return {k:v for k,v in a.items()if k!='code'}
def contract(j):
 assert len(j['pads'])==473 and len(j['footprints'])==141
 assert set(j['footprints'])==set(old['footprints'])
 for name,f in old['footprints'].items():
  q=j['footprints'][name];expected=dict(f)
  if name in s['moved_footprints']:expected.update(pos=s['moved_footprints'][name]['pos'],angle=s['moved_footprints'][name]['angle'])
  assert q['pos']==expected['pos']and (q['angle']-expected['angle'])%360==0 and q['uuid']==f['uuid']and q['lib']==f['lib'],('placement',name)
 assert j['board_outline']==old['board_outline']and j['bbox']==old['bbox']==[18.,20.,77.,121.]and j['zones']==old['zones']
 a={t['uuid']:cleaned(t)for t in old['tracks']};b={t['uuid']:cleaned(t)for t in j['tracks']}
 assert set(a)-set(b)==set(s['removed_copper_UUIDs']);assert set(b)-set(a)==set(s['new_copper'])
 assert all(b[u]==v for u,v in a.items()if u in b),'Unplanned retained copper change'
 assert {u:b[u]for u in s['new_copper']}==s['new_copper'],'Reviewed new copper changed'
 op={p['uuid']:p for p in old['pads']};assert {p['uuid']for p in j['pads']}==op.keys()
 for p in j['pads']:
  q=op[p['uuid']];name=p['ref']
  if name not in s['moved_footprints']:assert cleaned(p)==cleaned(q),('old pad',name,p['number']);continue
  base=old['footprints'][name];dest=s['moved_footprints'][name];theta=math.radians(base['angle']-dest['angle']);c,d=math.cos(theta),math.sin(theta)
  def transform(pt):x,y=pt[0]-base['pos'][0],pt[1]-base['pos'][1];return [dest['pos'][0]+c*x-d*y,dest['pos'][1]+d*x+c*y]
  assert math.dist(p['pos'],transform(q['pos']))<.000002 and (p['angle']-q['angle']-dest['angle']+base['angle'])%360<.000001
  assert {k:v for k,v in cleaned(p).items()if k not in ['pos','angle','polygons']}=={k:v for k,v in cleaned(q).items()if k not in ['pos','angle','polygons']}
  for layer,polys in q['polygons'].items():assert sh.union_all([Polygon(a)for a in p['polygons'][layer]]).symmetric_difference(sh.union_all([Polygon([transform(pt)for pt in a])for a in polys])).area<1e-7
contract(g)
assert (r/'enku-mainboard-r0.1.kicad_pro').read_bytes()==(ref/'enku-mainboard-r0.1.kicad_pro').read_bytes()
for p in ref.rglob('*'):
 if p.is_file()and p.name!='enku-mainboard-r0.1.kicad_pcb'and p.suffix not in ['.kicad_prl','.lck']:
  now=r/p.relative_to(ref)
  if p.suffix=='.kicad_sch':assert now.read_text().replace('R145 - ENGINEERING / NO FAB','R144 - ENGINEERING / NO FAB')==p.read_text()
  else:assert now.read_bytes()==p.read_bytes(),p.name
oldnets=E.parse(o/'reference_R144_netlist.xml').findall('./nets/net');nets=E.parse(o/'netlist.xml').findall('./nets/net');canonical=lambda ns:{n.get('name'):sorted(tuple(sorted(x.attrib.items()))for x in n.findall('node'))for n in ns};assert canonical(nets)==canonical(oldnets),'Schematic topology changed'
via=json.load(open(o/'via_process_R138.json'))['vias'];exc={x['uuid']for x in via if x['fill_requested']or x['cap_requested']};assert len(exc)==6 and exc==set(s['six_special_via_UUIDs']);lands=[sh.union_all([Polygon(q)for ps in p['polygons'].values()for q in ps])for p in g['pads']if p['attribute']==1 and p['number']];gaps=[]
for t in g['tracks']:
 if not t['via']:continue
 assert (t['width']-t['drill'])/2>=.15-1e-8
 if t['uuid']not in exc:
  gap=min(x.distance(Point(t['start']))-t['width']/2 for x in lands);assert gap>=.1-1e-6,(t['uuid'],gap);gaps.append(gap)
faults=[]
for label,mut in [('new_segment_removed',lambda j:j['tracks'].pop(next(i for i,t in enumerate(j['tracks'])if t['uuid']in s['new_copper']))),('retained_track_shifted',lambda j:j['tracks'][next(i for i,t in enumerate(j['tracks'])if t['uuid']not in s['new_copper'])]['start'].__setitem__(0,0)),('wrong_C19_position',lambda j:j['footprints']['C19']['pos'].__setitem__(0,0)),('antenna_rule_disabled',lambda j:next(z for z in j['zones']if z['rule']and z['no_tracks']).__setitem__('no_tracks',False)),('wrong_panel_land',lambda j:next(p for p in j['pads']if p['ref']=='J3'and p['number']=='1')['size'].__setitem__(0,.4))]:
 j=copy.deepcopy(g);mut(j)
 try:contract(j)
 except AssertionError:faults.append(label)
 else:raise AssertionError('Ineffective negative '+label)
(o/'source_invariants_R145.json').write_text(json.dumps(dict(revision='R145',pcb_sha256=sha(r/'enku-mainboard-r0.1.kicad_pcb'),finite_removals=len(s['removed_copper_UUIDs']),finite_new_items=len(s['new_copper']),only_C18_C19_moved=True,netlist_topology_unchanged=True,all_libraries_and_rules_unchanged=True,six_fill_cap_vias_preserved=True,minimum_ordinary_via_SMD_gap_mm=min(gaps),effective_negative_cases=faults,fabrication_ready=False),indent=2)+'\n');print('PASS R145 finite delta, netlist preservation, ordinary via gaps and5 effective mutations')
