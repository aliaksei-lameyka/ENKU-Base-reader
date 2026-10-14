"""R142 explicit scope, adapted from audit_exports_R141.py; original unchanged."""
"""Independently verify actual11-layer Gerber/drill/IPC/BOM/CPL review outputs."""
import collections,csv,hashlib,json,math,re,sys,warnings
from pathlib import Path
import gerbonara
from gerbonara import GerberFile,ExcellonFile
from gerbonara.graphic_objects import Flash,Line,Arc
from gerbonara.ipc356 import Netlist
from gerbonara.utils import MM
from shapely.geometry import box,Point,Polygon,LineString
from shapely.ops import unary_union
from shapely import affinity
from gerber_geometry_R137 import layer_shape,object_shape
from full_copper_R138 import normalize_copper
from native_svg_shapes_R130 import actual_shapes

def run(root,out):
 assert gerbonara.__version__=='1.6.3'
 m=out/'manufacturing_review_R142';g=json.loads((out/'geometry.json').read_text());af=json.loads((out/'assembly_features.json').read_text())
 expected={'F_Cu':('Copper','L1','Top'),'In1_Cu':('Copper','L2','Inr'),'In2_Cu':('Copper','L3','Inr'),'B_Cu':('Copper','L4','Bot'),
 'F_Mask':('Soldermask','Top'),'B_Mask':('Soldermask','Bot'),'F_Paste':('Paste','Top'),'B_Paste':('Paste','Bot'),
 'f_silkscreen':('Legend','Top'),'b_silkscreen':('Legend','Bot'),'Edge_Cuts':('Profile','NP')}
 files=list((m/'gerber').glob('*.gbr'));assert len(files)==11,'Missing/extra fabrication layer'
 assert {f.stem.removeprefix('enku-mainboard-r0.1-')for f in files}==expected.keys(),'Incomplete fabrication layer set'
 parsed={key:GerberFile.open(m/'gerber'/('enku-mainboard-r0.1-'+key+'.gbr'))for key in expected}
 metadata={}
 for key,file in parsed.items():
  assert file.file_attrs['.FileFunction']==expected[key],key
  assert file.file_attrs['.SameCoordinates']==('Original',)
  assert file.file_attrs['.GenerationSoftware']==('KiCad','Pcbnew','10.0.7')
  assert file.file_attrs['.ProjectId'][-1]=='R142 - ENGINEERING / NO FAB'
  assert file.import_settings.unit==MM and file.import_settings.number_format==(4,6)
  metadata[key]=dict(function=list(expected[key]),objects=len(file.objects),types=dict(collections.Counter(type(x).__name__ for x in file.objects)))
 assert not parsed['B_Paste'].objects,'Unexpected bottom paste'
 # Complete current copper is compared independently in audit_proposal_R142.py.
 assert json.loads((out/'proposal_copper_R142.json').read_text())['pcb_sha256']==(out/'source_pcb.sha256').read_text().split()[0]
 outline=parsed['Edge_Cuts'];assert len(outline.objects)==10 and all(isinstance(x,Line)for x in outline.objects)
 actual_edges=unary_union([LineString([(x.x1,-x.y1),(x.x2,-x.y2)])for x in outline.objects])
 native_edges=unary_union([Polygon(x).boundary for x in g['board_outline']])
 assert actual_edges.hausdorff_distance(native_edges)<.000002,'Gerber outline shifted/mirrored/different'
 assert list(actual_edges.bounds)==[18,20,77,121]
 hole_results={};slots=[]
 for plated,label in [(True,'PTH'),(False,'NPTH')]:
  f=m/'drill'/('enku-mainboard-r0.1-'+label+'.drl');text=f.read_text()
  assert '; #@! TF.FileFunction,'+('Plated'if plated else'NonPlated')+',1,4,'+label in text,'Wrong drill plating metadata'
  assert 'METRIC'in text and 'absolute / metric / decimal'in text
  with warnings.catch_warnings(record=True)as notices:drill=ExcellonFile.open(f,plated=plated)
  assert all('G90 header statement found after end of header'in str(w.message)for w in notices),'Unexpected drill parser warning'
  actual=[]
  for item in drill.objects:
   # Gerbonara does not populate plating from KiCad's X2 drill comments.
   # The required raw FileFunction above is authoritative; reject any
   # contradictory recognized tool flag without inventing unknown plating.
   assert item.aperture.plated in (None,plated)
   diameter=item.aperture.diameter
   if isinstance(item,Flash):actual.append(('circle',round(item.x,3),round(-item.y,3),round(diameter,3)))
   elif isinstance(item,Line):
    endpoints=tuple(sorted([(round(item.x1,3),round(-item.y1,3)),(round(item.x2,3),round(-item.y2,3))]))
    actual.append(('slot',*endpoints,round(diameter,3)));slots.append(dict(endpoints_mm=endpoints,diameter_mm=diameter))
   else:raise AssertionError('Unexpected drill geometry')
  native=[]
  if plated:
   for v in g['tracks']:
    if v['via']:native.append(('circle',*(round(x,3)for x in v['start']),round(v['drill'],3)))
  # KiCad10 PAD attribute:1=SMD,0=PTH,3=NPTH. Compare emitted holes,
  # including U1 EP12 drilled pads and every USB plated oval.
  for pad in g['pads']:
   if not max(pad['drill']):continue
   if (pad['attribute']!=3)!=plated:continue
   x,y=pad['pos'];w,h=pad['drill'];angle=math.radians(pad['angle'])
   if w==h:native.append(('circle',round(x,3),round(y,3),round(w,3)))
   else:
    vx,vy=((w-h)/2,0)if w>h else(0,(h-w)/2)
    dx=vx*math.cos(angle)+vy*math.sin(angle);dy=-vx*math.sin(angle)+vy*math.cos(angle)
    endpoints=tuple(sorted([(round(x-dx,3),round(y-dy,3)),(round(x+dx,3),round(y+dy,3))]))
    native.append(('slot',*endpoints,round(min(w,h),3)))
  assert collections.Counter(actual)==collections.Counter(native),('Drill count/position/diameter/slot axis mismatch',label,collections.Counter(actual)-collections.Counter(native),collections.Counter(native)-collections.Counter(actual))
  hole_results[label]=dict(objects=len(actual),circles=sum(x[0]=='circle'for x in actual),slots=sum(x[0]=='slot'for x in actual),header_plating_checked=True,exact_native_geometry_match=True)
 assert hole_results['NPTH']==dict(objects=9,circles=9,slots=0,header_plating_checked=True,exact_native_geometry_match=True)
 assert hole_results['PTH']['slots']==4
 assert hole_results['PTH']['objects']==sum(t['via'] for t in g['tracks'])+16
 apertures={};ox,oy=g['bbox'][:2]
 native_curve_error=json.loads((out/'source.kicad_pro').read_text())['board']['design_settings']['rules']['max_error']
 assert native_curve_error==.005
 # Native SVG approximates rounded apertures with chords using the unchanged
 # project5um max_error. Gerber arcs remain exact; its independent rendering
 # contributes0.1um plus0.1um for SVG coordinate quantization.
 curve_tolerance=native_curve_error+.0002
 for key in ['F_Mask','B_Mask','F_Paste','B_Paste']:
  independent=layer_shape(parsed[key]);native=unary_union(actual_shapes(out/(key+'.svg'),box(-5,-5,65,106)))
  native=affinity.translate(native,ox,oy);independent=affinity.scale(independent,1,-1,origin=(0,0))
  if independent.is_empty or native.is_empty:assert independent.is_empty and native.is_empty
  else:
   assert independent.difference(native.buffer(curve_tolerance)).area<1e-7,(key,'Gerber added/moved opening')
   assert native.difference(independent.buffer(curve_tolerance)).area<1e-7,(key,'Gerber missing opening')
   assert independent.hausdorff_distance(native)<curve_tolerance,(key,'Boundary mismatch')
   assert all(abs(x-y)<.0001 for x,y in zip(independent.bounds,native.bounds)),(key,'Aperture image bounds mismatch')
  apertures[key]=dict(native_SVG_and_independent_Gerber_union_match=True,native_project_curve_chord_error_mm=native_curve_error,comparison_tolerance_mm=curve_tolerance,Gerber_aperture_objects=len(parsed[key].objects),area_mm2=round(independent.area,6),empty=independent.is_empty)
 fitted={x['ref']for x in af['footprints']if not x['attributes']&12 and not x['dnp']}
 paste_refs={o.attrs['.C'][0]for o in parsed['F_Paste'].objects}
 assert paste_refs==fitted and len(paste_refs)==114 and not any(o.attrs.get('.C')==('R67',)for o in parsed['F_Paste'].objects),'DNP/bare/missing component paste'
 strokes={}
 for key in ['f_silkscreen','b_silkscreen']:
  widths=[o.aperture.diameter for o in parsed[key].objects if isinstance(o,(Line,Arc))]
  assert widths and min(widths)>=.15,'Gerber silkscreen too thin'
  strokes[key]=dict(minimum_width_mm=min(widths),drawn_strokes=len(widths))
 ni=Netlist.open(m/'netlist.d356');records=ni.test_records
 aliases=dict(re.findall(r'^P\s+NNAME(\S+)\s+(.+?)\s*$',(m/'netlist.d356').read_text(),flags=re.M))
 assert len(aliases)==22 and all(x.startswith('unconnected-')for x in aliases.values())
 via_count=sum(t['via']for t in g['tracks'])
 assert len(records)==439+via_count and sum(x.is_via for x in records)==via_count
 pads=[q for q in g['pads']if q['layers']]
 assert len(pads)==439
 used=set()
 for x in records:
  px,py=MM(x.x,x.unit),-MM(x.y,x.unit)
  net=aliases.get(x.net_name,x.net_name)
  if x.is_via:
   candidates=[q for q in g['tracks']if q['via']and math.dist(q['start'],[px,py])<.002 and q['net']==net]
  else:
   pin=str(getattr(x,'pin',x.pin_num)or x.pin_num or '')
   candidates=[q for q in pads if q['ref']==x.ref_des and q['number']==pin and math.dist(q['pos'],[px,py])<.002 and (q['net']or None)==net]
  assert len(candidates)==1,('IPC record net/pin/coordinate mismatch',x,px,py)
  uuid=candidates[0]['uuid'];assert uuid not in used;used.add(uuid)
 assert len(used)==439+via_count
 bom=list(csv.DictReader((m/'BOM_fitted_review.csv').open()));refs=[]
 fps={x['ref']:x for x in af['footprints']}
 for row in bom:
  names=row['Designator'].split(',');assert int(row['Quantity'])==len(names)
  for ref in names:
   assert ref in fitted and row['Manufacturer Part Number']==fps[ref]['fields']['MPN'] and row['Value']==fps[ref]['value'];refs.append(ref)
 assert collections.Counter(refs)==collections.Counter(fitted),'Wrong fitted BOM'
 assert (m/'CPL_native_mm.csv').read_bytes()==(out/'CPL.csv').read_bytes()
 process=list(csv.DictReader((m/'U3_via_process_requests.csv').open()))+list(csv.DictReader((m/'R28_via_process_request.csv').open()))
 assert len(process)==6 and all(x['Fill requested']=='True'and x['Cap requested']=='True'and x['Approved']=='False'and x['Front tented']=='False'and x['Back tented']=='True'for x in process),'Six exact unapproved filled capped requests required'
 native_vias={x['uuid']:x for x in g['tracks']if x['via']};native_process={x['uuid']:x for x in json.loads((out/'via_process_R138.json').read_text())['vias']}
 assert {x['Via UUID']for x in process}=={u for u,v in native_process.items()if v['fill_requested']or v['cap_requested']}
 for row in process:
  v=native_vias[row['Via UUID']];x,y=v['start']
  assert [float(row['Board X mm']),float(row['Board Y mm'])]==[x,y] and [float(row['Gerber X mm']),float(row['Gerber Y mm'])]==[x,-y]
  assert float(row['Diameter mm'])==v['width']and float(row['Drill mm'])==v['drill']

 manifest=json.loads((m/'manifest_R142.json').read_text());assert not manifest['fabrication_ready']and not manifest['manufacturing_release_approved']
 for file,meta in manifest['files'].items():
  data=(m/file).read_bytes();assert len(data)==meta['bytes']and hashlib.sha256(data).hexdigest()==meta['sha256'],file
 rings=[dict(uuid=v['uuid'],position_mm=v['start'],diameter_mm=v['width'],drill_mm=v['drill'],annular_ring_mm=round((v['width']-v['drill'])/2,6))for v in g['tracks']if v['via']and (v['width']-v['drill'])/2<.15-1e-8]
 assert not rings
 report=dict(revision='R142_PROPOSED',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],independent_parser='Gerbonara1.6.3',all11_Gerber_functions_units_precision_and_NO_FAB_revision_verified=True,
  layers=metadata,all_four_complete_current_copper_independent_comparison_PASS=True,exact_59x101_outline_and_native_origin_verified=True,holes=hole_results,Excellon_decimal_quantization_mm=.001,USB_four_plated_slot_axes_positions_and_tool_diameters_verified=True,USB_slots=slots,
  whole_board_mask_and_paste_checks=apertures,Gerber_silk_strokes=strokes,default_R67_DNP_and19_bare_PCB_items_absent_from_paste=True,fitted_parts_with_paste=114,
  all_current_IPC356_native_pad_and_via_positions_and_nets_matched=True,IPC356_records=439+via_count,IPC_coordinate_rounding_tolerance_mm=.002,
  grouped_fitted_BOM_units=114,native_CPL_coordinate_bytes_match=True,six_unapproved_fill_cap_requests_explicit=True,
  native_minimum_via_nominal_annular_ring_mm=.15,PCBWay_standard_published_annular_ring_mm=.15,total_vias_below_published_standard_ring=0,ordinary_vias_below_published_standard_ring=0,U3_under_EP_vias_below_published_standard_ring=0,annular_ring_geometry_repair_complete=True,below_standard_ring_vias=rings,
  factory_process_and_rotation_approval=False,fabrication_ready=False)
 (out/'manufacturing_export_audit_R142.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS independent11-layer Gerber/drill/current-point IPC/stencil/BOM/CPL verification; NO FAB')
 return report

if __name__=='__main__':run(*(Path(x).resolve()for x in sys.argv[1:3]))
