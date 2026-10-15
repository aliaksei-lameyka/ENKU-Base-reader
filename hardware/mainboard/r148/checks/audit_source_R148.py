"""R148 strict intended-delta contract vs exact R147; independent negative fixtures."""
from pathlib import Path
import copy,hashlib,json,sys,math,xml.etree.ElementTree as E
import shapely as sh
from shapely.geometry import Point,Polygon
r,o,ref,scope=map(lambda x:Path(x).resolve(),sys.argv[1:5]);s=json.load(open(scope));g=json.load(open(o/'geometry.json'));old=json.load(open(o/'reference_R147_geometry.json'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'enku-mainboard-r0.1.kicad_pcb')==s['current_pcb_sha256'];assert sha(ref/'enku-mainboard-r0.1.kicad_pcb')==s['reference_R147_pcb_sha256']
def clean(a):return {k:v for k,v in a.items()if k!='code'}
def contract(j):
 assert len(j['footprints'])==141 and len(j['pads'])==471
 assert j['board_outline']==old['board_outline']and j['bbox']==old['bbox']==[18.,20.,77.,121.]and j['zones']==old['zones']
 for name,f in old['footprints'].items():
  q=j['footprints'][name];wanted=s['moved_footprints'].get(name,dict(pos=f['pos'],angle=f['angle']))
  assert q['pos']==wanted['pos']and(q['angle']-wanted['angle'])%360==0 and q['uuid']==f['uuid']
  assert q['lib']==('ENKU:BATTERY_WIRE_PADS_2x1x3p5_P2_NO_PASTE'if name=='J1'else f['lib'])
 op={p['uuid']:p for p in old['pads']};removed={p['uuid']for p in old['pads']if p['ref']=='J1'and p['number']=='MP'}
 assert {p['uuid']for p in j['pads']}==op.keys()-removed and len(removed)==2
 for p in j['pads']:
  q=op[p['uuid']];name=p['ref']
  if name not in s['moved_footprints']:assert clean(p)==clean(q),(name,p['number']);continue
  base=old['footprints'][name];dest=s['moved_footprints'][name];theta=math.radians(base['angle']-dest['angle']);c,d=math.cos(theta),math.sin(theta)
  def tr(pt):x,y=pt[0]-base['pos'][0],pt[1]-base['pos'][1];return [dest['pos'][0]+c*x-d*y,dest['pos'][1]+d*x+c*y]
  assert math.dist(p['pos'],tr(q['pos']))<2e-6 and abs((p['angle']-q['angle']-dest['angle']+base['angle']+180)%360-180)<1e-6
  assert {k:v for k,v in clean(p).items()if k not in ['pos','angle','polygons']}=={k:v for k,v in clean(q).items()if k not in ['pos','angle','polygons']}
  for layer,polys in q['polygons'].items():assert sh.union_all([Polygon(a)for a in p['polygons'][layer]]).symmetric_difference(sh.union_all([Polygon([tr(pt)for pt in a])for a in polys])).area<1e-7
 a={t['uuid']:clean(t)for t in old['tracks']};b={t['uuid']:clean(t)for t in j['tracks']}
 assert a.keys()-b.keys()==set(s['removed_copper_UUIDs']);assert b.keys()-a.keys()==s['new_copper'].keys()
 assert all(b[u]==v for u,v in a.items()if u in b);assert {u:b[u]for u in s['new_copper']}==s['new_copper']
 for net in ['USB_DP','USB_DM','USB_DP_CONN','USB_DM_CONN']:assert {u:t for u,t in a.items()if t['net']==net}=={u:t for u,t in b.items()if t['net']==net}
 assert {p['number']:p['net']for p in j['pads']if p['ref']=='J1'}=={'1':'VBAT','2':'GND'}
contract(g)
assert (r/'enku-mainboard-r0.1.kicad_pro').read_bytes()==(ref/'enku-mainboard-r0.1.kicad_pro').read_bytes()
assert set(s['source_file_changes'])=={str(p.relative_to(ref))for p in ref.rglob('*')if p.is_file()and(r/p.relative_to(ref)).read_bytes()!=p.read_bytes()}
assert set(s['source_file_changes'])=={'enku-mainboard-r0.1.kicad_pcb',*s['schematic_files']}
newfiles={p.relative_to(r).as_posix()for p in r.rglob('*')if p.is_file()and'checks'not in p.parts and p.suffix!='.lck'}-{p.relative_to(ref).as_posix()for p in ref.rglob('*')if p.is_file()}
assert newfiles=={'ENKU.pretty/BATTERY_WIRE_PADS_2x1x3p5_P2_NO_PASTE.kicad_mod'}
canonical=lambda path:{n.get('name'):sorted(tuple(sorted(x.attrib.items()))for x in n.findall('node'))for n in E.parse(path).findall('./nets/net')}
assert canonical(o/'netlist.xml')==canonical(o/'reference_R147_netlist.xml')
via=json.load(open(o/'via_process_R138.json'))['vias'];exc={v['uuid']for v in via if v['fill_requested']or v['cap_requested']};assert exc==set(s['six_special_via_UUIDs'])and len(exc)==6
lands=[sh.union_all([Polygon(q)for ps in p['polygons'].values()for q in ps])for p in g['pads']if p['attribute']==1 and p['number']];gaps=[]
for t in g['tracks']:
 if not t['via']:continue
 assert(t['width']-t['drill'])/2>=.15-1e-8
 if t['uuid']not in exc:
  gap=min(a.distance(Point(t['start']))-t['width']/2 for a in lands);assert gap>=.1-1e-6,(t['uuid'],gap);gaps.append(gap)
fail=[]
for label,mut in [('cap_back_in_FPC_corridor',lambda j:j['footprints']['C24']['pos'].__setitem__(0,68.9)),('battery_polarity_reversed',lambda j:next(p for p in j['pads']if p['ref']=='J1'and p['number']=='1').__setitem__('net','GND')),('retained_copper_shifted',lambda j:next(t for t in j['tracks']if t['uuid']not in s['new_copper'])['start'].__setitem__(0,0)),('new_route_removed',lambda j:j['tracks'].pop(next(i for i,t in enumerate(j['tracks'])if t['uuid']in s['new_copper']))),('panel_contact_changed',lambda j:next(p for p in j['pads']if p['ref']=='J3'and p['number']=='5')['size'].__setitem__(0,.4))]:
 j=copy.deepcopy(g);mut(j)
 try:contract(j)
 except AssertionError:fail.append(label)
 else:raise AssertionError('Ineffective fault '+label)
(o/'source_invariants_R148.json').write_text(json.dumps(dict(revision='R148',pcb_sha256=s['current_pcb_sha256'],moved_footprints=s['moved_footprints'],bare_J1_original_two_copper_lands_and_polarity_preserved=True,netlist_topology_unchanged=True,all_unmodified_source_identical=True,six_special_vias_preserved=True,minimum_ordinary_via_SMD_gap_mm=min(gaps),effective_negative_cases=fail,fabrication_ready=False),indent=2)+'\n');print('PASS strict R148 intended delta and5 effective faults')
