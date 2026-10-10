"""Read-only triage of native library warnings; never replace embedded footprints."""
import json,sys,re,collections,hashlib
from pathlib import Path
import pcbnew as p
r=Path(sys.argv[1]).resolve();c=r/'checks';board=p.LoadBoard(str(r/'enku-mainboard-r0.1.kicad_pcb'))
libs={a:b.replace('${KIPRJMOD}',str(r)) for a,b in re.findall(r'\(name "([^"]+)"\).*?\(uri "([^"]+)"\)',(r/'fp-lib-table').read_text())}
d=json.loads((c/'drc_checkpoint_R121.json').read_text());wanted={i['uuid'] for v in d['violations'] if v['type']=='lib_footprint_mismatch' for i in v['items']}
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def pads(f):
 out=[]
 for a in f.Pads():
  layers=[l for l in a.GetLayerSet().Seq() if p.IsCopperLayer(l) and board.GetEnabledLayers().Contains(l)]
  out.append({'number':a.GetNumber(),'position_mm':xy(a.GetPosition()),'size_mm':xy(a.GetSize()),'angle_deg':round(a.GetOrientationDegrees()%(90 if a.GetSize().x==a.GetSize().y and a.GetDrillSize().x==a.GetDrillSize().y else 180),6),'drill_mm':xy(a.GetDrillSize()),'drill_shape':a.GetDrillShape(),'pad_shape':a.GetShape(),'attribute':a.GetAttribute(),'copper_layers':layers,'local_mask_margin_IU':a.GetLocalSolderMaskMargin(),'local_paste_margin_IU':a.GetLocalSolderPasteMargin(),'local_paste_ratio':a.GetLocalSolderPasteMarginRatio()})
 return sorted(out,key=lambda a:(a['number'],a['position_mm']))
aux=p.BOARD();aux.SetCopperLayerCount(4);results=[]
for f in board.GetFootprints():
 if f.m_Uuid.AsString() not in wanted:continue
 nick=str(f.GetFPID().GetLibNickname());item=str(f.GetFPID().GetLibItemName());file=Path(libs[nick])/(item+'.kicad_mod');row={'ref':f.GetReference(),'library':nick+':'+item}
 if not file.exists():row.update(category='reference_missing',differences=[]);results.append(row);continue
 lib=p.FootprintLoad(str(file.parent),item);aux.Add(lib)
 if lib.IsFlipped()!=f.IsFlipped():lib.Flip(lib.GetPosition(),False)
 lib.SetOrientation(f.GetOrientation());lib.SetPosition(f.GetPosition());a,b=pads(f),pads(lib);diff=[]
 if len(a)!=len(b):diff.append({'field':'pad_count','embedded':len(a),'library':len(b)})
 else:
  for x,y in zip(a,b):
   for k in x:
    if x[k]!=y[k]:diff.append({'pad_number':x['number'],'field':k,'embedded':x[k],'library':y[k]})
 geometry=[x for x in diff if x['field'] not in ('number','attribute','local_mask_margin_IU','local_paste_margin_IU','local_paste_ratio')]
 numbering=[x for x in diff if x['field'] in ('number','attribute')]
 row.update(reference_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),category='pad_or_drill_difference' if geometry else 'pin_number_or_attribute_difference' if numbering else 'mask_or_stencil_override_difference' if diff else 'pad_properties_equal_other_footprint_difference',differences=diff)
 results.append(row)
assert len(results)==111,len(results)
report={'revision':'R121','pcb_sha256':hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),'native_library_warnings':111,'categories':dict(collections.Counter(x['category'] for x in results)),'scope':'Read-only comparison after placing/flipping each library reference at the actual footprint pose. Symmetric rectangular-pad angles are normalized modulo180 degrees (90 for square/circular symmetric geometry). Compare pad count, numbers, position/orientation, size, shape, attribute, drills, copper layers and local mask/paste overrides. Equality does not certify custom primitives, footprint-level overrides, graphics, MPN or manufacturer fit. Native warnings remain active.','fabrication_ready':False,'footprints':sorted(results,key=lambda x:x['ref'])}
(c/'library_mismatch_triage_R121.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='footprints'},indent=2));print('Pad/drill review:',[(x['ref'],x['library']) for x in results if x['category']=='pad_or_drill_difference'])
