"""Finite R143 delta, unchanged interfaces and independent ordinary-via SMD gap."""
import copy,hashlib,json,sys,xml.etree.ElementTree as E
from pathlib import Path
import shapely as sh
from shapely.geometry import Point,Polygon
r,o,ref,scope=map(lambda v:Path(v).resolve(),sys.argv[1:5]);g=json.loads((o/'geometry.json').read_text());old=json.loads((o/'reference_R143_geometry.json').read_text());s=json.loads(scope.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(r/'enku-mainboard-r0.1.kicad_pcb')==s['current_pcb_sha256'];assert sha(ref/'enku-mainboard-r0.1.kicad_pcb')==s['reference_R143_pcb_sha256']
def contract(j):
 assert len(j['footprints'])==141 and len(j['pads'])==473
 assert set(j['footprints'])-set(old['footprints'])=={'R95','R96','R97','R98','R99','C40','C41'}
 for name,fp in old['footprints'].items():
  expected=s['moved_original_C15']if name=='C15'else s['final_new_positions']['U11']if name=='U11'else fp
  assert j['footprints'][name]==expected,('Unexpected component placement',name)
 for name,fp in s['final_new_positions'].items():assert j['footprints'][name]==fp
 assert j['board_outline']==old['board_outline']and j['bbox']==old['bbox']==[18.,20.,77.,121.]and j['zones']==old['zones']
 def copper(a):return {t['uuid']:{k:v for k,v in t.items()if k!='code'}for t in a['tracks']}
 a,b=copper(old),copper(j);assert set(a)-set(b)==set(s['old_removed_copper_UUIDs']);assert set(b)-set(a)==set(s['new_copper'])
 assert all(b[k]==v for k,v in a.items()if k in b),'Unscoped old copper modification'
 assert {k:b[k]for k in s['new_copper']}==s['new_copper'],'New copper differs from reviewed finite plan'
 op={p['uuid']:p for p in old['pads']}
 for p in j['pads']:
  if p['uuid']not in op:continue
  q=op[p['uuid']]
  if p['ref']=='U11':continue
  expected=dict(q)
  if p['ref']=='C15':expected['pos']=[q['pos'][0]+2.,q['pos'][1]+5.45];expected['polygons']=p['polygons']
  if (p['ref'],p['number'])in [('U4','2'),('R14','1')]:expected['net']='REG_MODE'if p['ref']=='U4'else'REG_FB_TOP';expected['code']=p['code']
  assert {k:v for k,v in p.items()if k!='code'}=={k:v for k,v in expected.items()if k!='code'},('Unscoped old pad change',p['ref'],p['number'])
contract(g)
assert (r/'enku-mainboard-r0.1.kicad_pro').read_bytes()==(ref/'enku-mainboard-r0.1.kicad_pro').read_bytes()
for p in ref.rglob('*'):
 if p.is_file()and (p.suffix=='.kicad_mod'or p.name in ['fp-lib-table','sym-lib-table']):assert p.read_bytes()==(r/p.relative_to(ref)).read_bytes(),p.name
via=json.loads((o/'via_process_R138.json').read_text())['vias'];exc={x['uuid']for x in via if x['fill_requested']or x['cap_requested']};assert len(exc)==6;lands=[sh.union_all([Polygon(q)for rings in p['polygons'].values()for q in rings])for p in g['pads']if p['attribute']==1 and p['number']];gaps=[]
for t in g['tracks']:
 if not t['via']:continue
 assert (t['width']-t['drill'])/2>=.15-1e-8
 if t['uuid']not in exc:
  gap=min(x.distance(Point(t['start']))-t['width']/2 for x in lands);assert gap>=.1-1e-6,(t['uuid'],gap);gaps.append(gap)
faults=[]
for label,mutate in [('removed_new_segment',lambda j:j['tracks'].pop(next(i for i,t in enumerate(j['tracks'])if t['uuid']in s['new_copper']))),('old_track_displaced',lambda j:j['tracks'][next(i for i,t in enumerate(j['tracks'])if t['uuid']not in s['new_copper'])]['start'].__setitem__(0,0)),('wrong_module_position',lambda j:j['footprints']['U1']['pos'].__setitem__(0,0)),('changed_antenna_rule',lambda j:next(z for z in j['zones']if z['rule']and z['no_tracks']).__setitem__('no_tracks',False)),('wrong_panel_land',lambda j:next(p for p in j['pads']if p['ref']=='J3'and p['number']=='1')['size'].__setitem__(0,.4))]:
 j=copy.deepcopy(g);mutate(j)
 try:contract(j)
 except AssertionError:faults.append(dict(fault=label,detected=True))
 else:raise AssertionError('Ineffective fixture '+label)
report=dict(revision='R144',pcb_sha256=sha(r/'enku-mainboard-r0.1.kicad_pcb'),finite_old_copper_removals=len(s['old_removed_copper_UUIDs']),finite_new_copper_items=len(s['new_copper']),original_USB_data_antenna_outline_J2_J3_preserved=True,minimum_ordinary_via_SMD_gap_mm=min(gaps),six_fill_cap_sites_retained=True,effective_faults=faults,fabrication_ready=False)
(o/'source_invariants_R144.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS finite delta and all ordinary via/SMD gaps')
