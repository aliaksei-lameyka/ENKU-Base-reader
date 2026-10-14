"""Compare actual proposed source and independently rendered copper, retaining R138."""
import gzip,hashlib,json,sys
from pathlib import Path
import shapely as sh
from shapely.geometry import Point,Polygon,LineString,box
from shapely import affinity
from gerbonara import GerberFile
from pad_groups import partitions
from full_copper_R138 import layer_shape,normalize_copper,discrete_hausdorff

def audit(root,out):
 sha=hashlib.sha256((root/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
 g=json.loads((out/'geometry.json').read_text())
 native=json.loads(gzip.decompress((out/'native_copper_R138.json.gz').read_bytes()));curve=json.loads((root/'enku-mainboard-r0.1.kicad_pro').read_text())['board']['design_settings']['rules']['max_error'];assert curve==.005;tol=curve+.0002;results={}
 for key,layer in [('F_Cu',0),('In1_Cu',4),('In2_Cu',6),('B_Cu',2)]:
  p=out/'manufacturing_review_R143/gerber'/('enku-mainboard-r0.1-'+key+'.gbr');gerber=affinity.scale(layer_shape(GerberFile.open(p)),1,-1,origin=(0,0));objects=[sh.make_valid(Polygon(z['shell'],z['holes']))for z in native['filled_zones'][str(layer)]]
  for pad in g['pads']:
   if str(layer)not in pad['polygons']or pad['attribute']==3 and pad['size']==pad['drill']:continue
   objects.extend(Polygon(q)for q in pad['polygons'][str(layer)])
  for t in g['tracks']:
   if t['via']:objects.append(Point(t['start']).buffer(t['width']/2,quad_segs=128))
   elif t['layer']==layer:objects.append(LineString([t['start'],t['end']]).buffer(t['width']/2,quad_segs=128))
  copper=sh.union_all(objects);added=gerber.difference(copper.buffer(tol)).area;missing=copper.difference(gerber.buffer(tol)).area;distance=discrete_hausdorff(gerber,copper);assert added<1e-6 and missing<1e-6 and distance<tol,(key,added,missing,distance)
  results[key]=dict(normalized_stream_sha256=hashlib.sha256(normalize_copper(p.read_bytes())).hexdigest(),added_outside_curve_budget_mm2=added,missing_outside_curve_budget_mm2=missing,Hausdorff_distance_mm=distance);print('PASS current complete copper',key,flush=True)
 (out/'proposal_copper_R143.json').write_text(json.dumps(dict(pcb_sha256=sha,layers=results,comparison_tolerance_mm=tol,fabrication_ready=False),indent=2)+'\n')
if __name__=='__main__':audit(*(Path(v).resolve()for v in sys.argv[1:3]))
