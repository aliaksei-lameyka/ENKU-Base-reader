"""Compare actual proposed source and independently rendered copper, retaining R138."""
import gzip,hashlib,json,sys
from pathlib import Path
import shapely as sh
from shapely.geometry import Point,Polygon,LineString,box
from shapely import affinity
from gerbonara import GerberFile
from pad_groups import partitions
from full_copper_R138 import layer_shape,normalize_copper,discrete_hausdorff

def audit(root,canonical,out):
 c=canonical/'checks';sha=hashlib.sha256((root/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
 g=json.loads((out/'geometry.json').read_text());old=json.loads(gzip.decompress((c/'geometry_checkpoint_R138.json.gz').read_bytes()))
 d=json.loads((out/'drc.json').read_text());e=json.loads((out/'erc.json').read_text())
 assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']
 assert not any(s['violations']for s in e['sheets'])
 assert (out/'source_pcb.sha256').read_text().split()[0]==sha
 assert (root/'enku-mainboard-r0.1.kicad_pro').read_bytes()==(canonical/'enku-mainboard-r0.1.kicad_pro').read_bytes()
 for p in canonical.glob('*.kicad_sch'):assert p.read_bytes()==(root/p.name).read_bytes()
 for name in ['ENKU.kicad_sym','fp-lib-table','sym-lib-table']:assert (root/name).read_bytes()==(canonical/name).read_bytes()
 af=json.loads((out/'assembly_features.json').read_text());oldaf=json.loads((c/'assembly_features_R138.json').read_text())
 assert {f['ref']:f for f in af['footprints']}=={f['ref']:f for f in oldaf['footprints']}
 oldpads={p['uuid']:p for p in oldaf['pads']}
 for p in af['pads']:
  for key,value in oldpads[p['uuid']].items():
   if key!='position_mm':assert p[key]==value,(p['ref'],p['number'],key)
 assert len(g['pads'])==438 and len(g['footprints'])==127
 assert partitions(g)==partitions(old),'Accepted native pad partitions changed'
 intended={'C5':([47.75,94.9],270.),'C7':([44.5,91.],180.),'C8':([52.5,91.],0.),'L2':([61.5,44.2],0.),'C31':([56.5,44.2],180.),'D1':([66.8,43.2],270.),'C24':([68.9,39.],90.),'C25':([67.8,52.],270.),'D2':([68.,55.5],0.),'D3':([71.3,52.9],0.),'C26':([74.,49.7],90.),'R37':([65.5,51.8],270.),'R19':([46.6,54.8],0.)}
 for ref,fp in old['footprints'].items():
  actual=g['footprints'][ref];assert fp['uuid']==actual['uuid']and fp['lib']==actual['lib']
  if ref in intended:
   pos,angle=intended[ref];assert actual['pos']==pos and abs(actual['angle']%360-angle)<1e-8,(ref,actual)
  else:assert actual==fp,('Unintended placement',ref)
 assert box(46.6-1.395,54.8-.545,46.6+1.395,54.8+.545).distance(box(20.25,36,45.75,54))>=.25-1e-9,'R19 overlaps accepted U1 body without native courtyard'
 pp={p['uuid']:p for p in old['pads']}
 for p in g['pads']:
  for key in ['ref','number','net','size','drill','shape','attribute','layers','drill_shape']:assert p[key]==pp[p['uuid']][key],(p['ref'],p['number'],key)
  if p['ref']not in intended:assert p==pp[p['uuid']]
 assert g['board_outline']==old['board_outline']and g['zones']==old['zones']
 thermal=json.loads((c/'thermal_via_manifest_R138.json').read_text())['added_vias'];exceptions={v['uuid']:v for v in thermal};r28=json.loads((c/'R28_via_in_pad_manifest_R138.json').read_text());exceptions[r28['uuid']]=r28
 process={p['uuid']:p for p in json.loads((out/'via_process_R138.json').read_text())['vias']}
 assert {u for u,v in process.items()if v['fill_requested']or v['cap_requested']}==exceptions.keys()
 lands=[sh.union_all([Polygon(q)for rings in p['polygons'].values()for q in rings])for p in g['pads']if p['attribute']==1 and p['number']];vias=[t for t in g['tracks']if t['via']];rings=[];gaps=[]
 for v in vias:
  ring=(v['width']-v['drill'])/2;assert ring>=.15-1e-9 and v['drill']>=.2 and v['width']>=.5;rings.append(ring)
  if v['uuid']in exceptions:
   expected=exceptions[v['uuid']];assert v['start']==expected['position_mm']and v['width']==expected['land_mm']and v['drill']==expected['drill_mm']and v['net']==expected['net']
   q=process[v['uuid']];assert q['fill_requested']and q['cap_requested']and not q['front_tented']and q['back_tented']
  else:
   gap=min(shape.distance(Point(v['start']))-v['width']/2 for shape in lands);assert gap>=.1-1e-6,(v['uuid'],gap);gaps.append(gap)
 usb=lambda data:sorted([t for t in data['tracks']if t['net'].startswith('USB_D')],key=lambda t:t['uuid']);assert usb(g)==usb(old)
 report=dict(revision='R141_PROPOSED',pcb_sha256=sha,native_kicad='10.0.7',DRC=0,ERC=0,opens=0,parity=0,all_438_pad_definitions_and_127_references_verified=True,all_native_pad_partitions_preserved=True,explicit_placement_changes=sorted(intended),unchanged_outline_zones_project_rules_schematics_libraries=True,unchanged_USB_copper=True,vias=len(vias),minimum_annular_ring_mm=min(rings),minimum_ordinary_via_SMD_gap_mm=min(gaps),exact_six_unapproved_fill_cap_requests=True,accepted_R138_checkpoints_regenerated=False,physical_qualification='NOT RUN',fabrication_ready=False)
 (out/'proposal_invariants_R141.json').write_text(json.dumps(report,indent=2)+'\n')
 native=json.loads(gzip.decompress((out/'native_copper_R138.json.gz').read_bytes()));curve=json.loads((root/'enku-mainboard-r0.1.kicad_pro').read_text())['board']['design_settings']['rules']['max_error'];assert curve==.005;tol=curve+.0002;results={}
 for key,layer in [('F_Cu',0),('In1_Cu',4),('In2_Cu',6),('B_Cu',2)]:
  p=out/'manufacturing_review_R138/gerber'/('enku-mainboard-r0.1-'+key+'.gbr');gerber=affinity.scale(layer_shape(GerberFile.open(p)),1,-1,origin=(0,0));objects=[sh.make_valid(Polygon(z['shell'],z['holes']))for z in native['filled_zones'][str(layer)]]
  for pad in g['pads']:
   if str(layer)not in pad['polygons']or pad['attribute']==3 and pad['size']==pad['drill']:continue
   objects.extend(Polygon(q)for q in pad['polygons'][str(layer)])
  for t in g['tracks']:
   if t['via']:objects.append(Point(t['start']).buffer(t['width']/2,quad_segs=128))
   elif t['layer']==layer:objects.append(LineString([t['start'],t['end']]).buffer(t['width']/2,quad_segs=128))
  copper=sh.union_all(objects);added=gerber.difference(copper.buffer(tol)).area;missing=copper.difference(gerber.buffer(tol)).area;distance=discrete_hausdorff(gerber,copper);assert added<1e-6 and missing<1e-6 and distance<tol,(key,added,missing,distance)
  results[key]=dict(normalized_stream_sha256=hashlib.sha256(normalize_copper(p.read_bytes())).hexdigest(),added_outside_curve_budget_mm2=added,missing_outside_curve_budget_mm2=missing,Hausdorff_distance_mm=distance);print('PASS current complete copper',key,flush=True)
 (out/'proposal_copper_R141.json').write_text(json.dumps(dict(pcb_sha256=sha,layers=results,comparison_tolerance_mm=tol,fabrication_ready=False),indent=2)+'\n')
if __name__=='__main__':audit(*(Path(v).resolve()for v in sys.argv[1:4]))
