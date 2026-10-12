"""Compare all four complete raw Gerber copper images with native copper."""
import gzip,hashlib,json,sys
from pathlib import Path
import shapely as sh
from shapely import affinity
from shapely.geometry import Point,Polygon,LineString
from gerbonara import GerberFile
from full_copper_R138 import layer_shape,normalize_copper
r,out=(Path(x).resolve()for x in sys.argv[1:3]);c=r/'checks';m=out/'manufacturing_review_R138';g=json.loads((out/'geometry.json').read_text());native=json.loads(gzip.decompress((out/'native_copper_R138.json.gz').read_bytes()));baseline=json.loads((c/'copper_Gerber_baseline_R138.json').read_text());sha=(out/'source_pcb.sha256').read_text().split()[0]
assert baseline['pcb_sha256']==sha and baseline['native_kicad']=='10.0.7'
curve=json.loads((out/'source.kicad_pro').read_text())['board']['design_settings']['rules']['max_error'];assert curve==.005;tol=curve+.0002
results={}
for key,layer in [('F_Cu',0),('In1_Cu',4),('In2_Cu',6),('B_Cu',2)]:
 p=m/'gerber'/('enku-mainboard-r0.1-'+key+'.gbr');digest=hashlib.sha256(normalize_copper(p.read_bytes())).hexdigest();assert digest==baseline['normalized_copper_sha256'][key],('Complete copper stream changed',key)
 gerber=affinity.scale(layer_shape(GerberFile.open(p)),1,-1,origin=(0,0))
 objects=[sh.make_valid(Polygon(z['shell'],z['holes']))for z in native['filled_zones'][str(layer)]]
 for pad in g['pads']:
  if str(layer)not in pad['polygons']:continue
  # NPTH holes whose land equals their drill have no emitted copper.
  if pad['attribute']==3 and pad['size']==pad['drill']:continue
  objects.extend(Polygon(p)for p in pad['polygons'][str(layer)])
 for t in g['tracks']:
  if t['via']:objects.append(Point(t['start']).buffer(t['width']/2,quad_segs=128))
  elif t['layer']==layer:objects.append(LineString([t['start'],t['end']]).buffer(t['width']/2,quad_segs=128))
 copper=sh.union_all(objects)
 added=gerber.difference(copper.buffer(tol)).area;missing=copper.difference(gerber.buffer(tol)).area;distance=gerber.hausdorff_distance(copper)
 assert added<1e-6 and missing<1e-6 and distance<tol,(key,'Native/Gerber copper mismatch',added,missing,distance)
 results[key]=dict(normalized_stream_sha256=digest,native_area_mm2=copper.area,independent_Gerber_area_mm2=gerber.area,added_outside_curve_budget_mm2=added,missing_outside_curve_budget_mm2=missing,Hausdorff_distance_mm=distance,native_zone_regions=len(native['filled_zones'][str(layer)]))
report=dict(revision='R138',pcb_sha256=sha,all_four_complete_copper_images_independently_verified=True,independent_parser='Gerbonara1.6.3',native_curve_error_mm=curve,comparison_tolerance_mm=tol,only_two_creation_timestamps_normalized=True,layers=results,actual_factory_stackup_and_impedance_approval=False,fabrication_ready=False)
(out/'full_copper_audit_R138.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS complete four-layer Gerber images against actual refilled native copper')
