"""Explicit R141->R142 pin/land/source delta and independent OEM surface regions."""
import hashlib,json,sys,xml.etree.ElementTree as E
from pathlib import Path
import shapely as sh
from shapely.geometry import Polygon,Point,LineString
from hirose_regions_R142 import POLYGONS,transform
r,reference,o=map(lambda x:Path(x).resolve(),sys.argv[1:4]);g=json.loads((o/'geometry.json').read_text());old=json.loads((o/'reference_R141_geometry.json').read_text());af=json.loads((o/'assembly_features.json').read_text());oa=json.loads((o/'reference_R141_assembly.json').read_text())
def nodes(file):return {(a.get('ref'),a.get('pin')):n.get('name')for n in E.parse(file).findall('./nets/net')for a in n.findall('node')}
before,after=nodes(o/'reference_R141_netlist.xml'),nodes(o/'netlist.xml');changes={('C15','1'):'3V3_SYS',('U1','32'):'SD_CD',('J2','1'):'SD_DAT2_BIAS',('J2','8'):'SD_DAT1_BIAS'};assert {k:(v,after[k])for k,v in before.items()if after[k]!=v}=={k:(before[k],v)for k,v in changes.items()}
assert {k:v for k,v in after.items()if k not in before}=={('J2','9'):'SD_CD',('J2','10'):'GND',('U11','1'):'GND',('U11','2'):'ESP_EN',('U11','3'):'3V3_SYS',('R89','1'):'CHG_TS',('R89','2'):'GND',('R90','1'):'3V3_SYS',('R90','2'):'SD_CD',**{(ref,'1'):'3V3_SYS'for ref in ['R91','R92','R93','R94']},**{(ref,'2'):net for ref,net in [('R91','SD_MOSI_CARD'),('R92','SD_MISO_CARD'),('R93','SD_DAT1_BIAS'),('R94','SD_DAT2_BIAS')]}}
assert len(g['footprints'])==134 and len(g['pads'])==453 and set(g['footprints'])-set(old['footprints'])=={'U11','R89','R90','R91','R92','R93','R94'}
fmap={f['ref']:f for f in af['footprints']};of={f['ref']:f for f in oa['footprints']}
for name,fp in old['footprints'].items():
 expected=dict(fp)
 if name=='C15':expected['pos']=[44.,63.75]
 if name in ['R14','R15']:expected['lib']='ENKU:R_RT0603_YAGEO_REFLOW'
 assert g['footprints'][name]==expected,('Unexpected placement',name)
 if name not in ['C15','R14','R15','R23']:assert fmap[name]==of[name],('Unexpected BOM field change',name)
op={p['uuid']:p for p in old['pads']}
for a in g['pads']:
 if a['uuid']not in op:continue
 b=op[a['uuid']]
 for key in ['ref','number','size','drill','shape','attribute','layers','drill_shape']:assert a[key]==b[key],(a['ref'],a['number'],key)
 net=changes.get((a['ref'],a['number']),b['net'])
 if a['ref']=='J2'and a['number']in ['9','10']:net='SD_CD'if a['number']=='9'else'GND'
 assert a['net']==net
 if a['ref']!='C15':assert a['pos']==b['pos']and a['angle']==b['angle']
assert g['board_outline']==old['board_outline']and g['bbox']==old['bbox']==[18.,20.,77.,121.]
for name in ['enku-mainboard-r0.1.kicad_pro','enku-mainboard-r0.1.kicad_dru','fp-lib-table','sym-lib-table']:assert (r/name).read_bytes()==(reference/name).read_bytes()
# KiCad numeric net codes are reindexed when the two SD bias nets are added.
# Compare UUID, named net and every physical property, excluding only that index.
usb=lambda j:sorted([{k:v for k,v in t.items()if k!='code'}for t in j['tracks']if t['net'].startswith('USB_D')],key=lambda t:t['uuid']);assert usb(g)==usb(old)
extra=[z for z in g['zones']if z['name'].startswith('R142 Hirose')];assert len(extra)==5;assert [z for z in g['zones']if not z['name'].startswith('R142 Hirose')]==old['zones']
f=g['footprints']['J2'];region=sh.union_all([Polygon([transform(q,f)for q in p])for p in POLYGONS])
def intersections(data):
 findings=[]
 for t in data['tracks']:
  if not t['via']and t['layer']!=0:continue
  geom=Point(t['start']).buffer(t['width']/2,quad_segs=128)if t['via']else LineString([t['start'],t['end']]).buffer(t['width']/2,quad_segs=128);area=geom.intersection(region).area
  if area>1e-8:findings.append(dict(uuid=t['uuid'],net=t['net'],area_mm2=area))
 for p in data['pads']:
  area=sh.union_all([Polygon(q)for q in p['polygons'].get('0',[])]).intersection(region).area
  if area>1e-8:findings.append(dict(uuid=p['uuid'],ref=p['ref'],pin=p['number'],area_mm2=area))
 return findings
assert not intersections(g);oldfind=intersections(old);assert any(z.get('net')=='VBUS_USB'for z in oldfind)and any(z.get('net')=='SD_CS_CARD'for z in oldfind)
for i,z in enumerate(sorted(extra,key=lambda z:z['name'])):
 assert z['rule']and z['layers']==[0]and all(z[key]for key in ['no_tracks','no_vias','no_pads','no_zone_fills']);assert z['polygons']==[[transform(q,f)for q in POLYGONS[i]]]
lv=json.loads((o/'layer_visibility_audit_R142.json').read_text());assert not lv['unnamed_layers']and not lv['disabled_documentation_layers']and not lv['copper_graphics_without_net_semantics'];lv['revision']='R142';lv['netless_disposition']={'rule_areas':'Original antenna plus rear Tag-Connect exclusion +five Hirose surface exclusions','NPTH':'Nine mechanical/guide holes','SMT':'Six mechanical switch/connector lands','J2_switch':'Both contacts assigned in R142'};(o/'layer_visibility_audit_R142.json').write_text(json.dumps(lv,indent=2)+'\n')
process=json.loads((o/'via_process_R138.json').read_text())['vias'];exc={x['uuid']for x in process if x['fill_requested']or x['cap_requested']};assert len(exc)==6;lands=[sh.union_all([Polygon(q)for rings in p['polygons'].values()for q in rings])for p in g['pads']if p['attribute']==1 and p['number']];gaps=[]
for t in g['tracks']:
 if not t['via']:continue
 assert (t['width']-t['drill'])/2>=.15-1e-8
 if t['uuid']not in exc:
  gap=min(s.distance(Point(t['start']))-t['width']/2 for s in lands);assert gap>=.1-1e-6,(t['uuid'],gap);gaps.append(gap)
report=dict(revision='R142',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),original_438_lands_numbering_size_holes_preserved=True,added_refs=['U11','R89','R90','R91','R92','R93','R94'],only_original_moved_component='C15',existing_changed_nets=[dict(ref=k[0],pin=k[1],before=before[k],after=v)for k,v in changes.items()],USB_data_copper_unchanged=True,board_outline_antenna_and_original_zones_preserved=True,minimum_ordinary_via_SMD_gap_mm=min(gaps),six_fill_cap_sites_retained=True,Hirose_R141_intersections=oldfind,Hirose_R142_intersections=[],unnamed_layers=0,disabled_documentation_objects=0,physical_and_manufacturer_process_qualification='NOT RUN',fabrication_ready=False)
(o/'source_invariants_R142.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source/land/pin preservation, OEM exclusions and layer inventory',flush=True)
