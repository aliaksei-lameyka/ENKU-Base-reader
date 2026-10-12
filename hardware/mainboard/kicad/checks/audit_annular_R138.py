"""All-via nominal ring/finite bore contract and conditional barrel sensitivity."""
import collections,gzip,hashlib,json,math,sys
from pathlib import Path
r,out=(Path(x).resolve()for x in sys.argv[1:3]);c=r/'checks'
g=json.loads((out/'geometry.json').read_text());gold=json.loads(gzip.decompress((c/'physical_preview_R138.json.gz').read_bytes()))
vias={v['uuid']:v for v in g['tracks']if v['via']};goldvias={v['uuid']:v for v in gold['tracks']if v['via']}
assert vias==goldvias,'Via dimensions or coordinates differ from reviewed finite source'
assert len(vias)==329
variants=collections.Counter((v['width'],v['drill'])for v in vias.values());assert variants=={(.7,.3):88,(.6,.3):150,(.5,.2):91},variants
rings=collections.Counter(round((v['width']-v['drill'])/2,6)for v in vias.values());assert rings=={.15:241,.2:88},rings
project=json.loads((out/'source.kicad_pro').read_text());rules=project['board']['design_settings']['rules'];assert rules['min_via_annular_width']==.15 and rules['min_through_hole_diameter']==.2
native=json.loads(gzip.decompress((out/'native_copper_R138.json.gz').read_bytes()));assert native['board_thickness_mm']==1.6
small=sorted(u for u,v in vias.items()if v['drill']==.2);assert len(small)==91
# Copper rho at20C, alpha and18um wall are explicit assumptions. These DC
# values neither qualify plating thickness, ampacity, heat or actual yield.
rho=1.724e-8;alpha=.00393;wall=.018;hole=.2;length=1.6
area=math.pi*((hole+2*wall)**2-hole**2)/4*1e-6
resistance_20=rho*length*.001/area;resistance_60=resistance_20*(1+alpha*40)
report=dict(revision='R138',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],all329_via_nominal_annular_rings_measured=True,minimum_nominal_annular_ring_mm=.15,ring_counts_mm={str(k):v for k,v in rings.items()},variants=[dict(diameter_mm=k[0],drill_mm=k[1],count=v)for k,v in sorted(variants.items())],exact_0_20mm_bore_UUIDs=small,nominal_board_thickness_mm=1.6,nominal_maximum_thickness_to_bore_aspect=8.,aspect_at_plus10percent_board_thickness=8.8,primary_capability_URL='https://www.pcbway.com/capabilities.html',nominal_aspect_on_published_boundary=True,finished_drill_board_thickness_registration_and_barrel_approval=False,assumed_barrel_copper_um=18,assumed_rho20_ohm_m=rho,conditional_single_barrel_resistance_milliohm_at20C=resistance_20*1000,conditional_single_barrel_resistance_milliohm_at60C=resistance_60*1000,conditional_DC_at60C=[dict(current_A=i,voltage_mV=i*resistance_60*1000,loss_mW=i*i*resistance_60*1000)for i in [.5,1,2]],actual_plating_ampacity_and_thermal_qualification=False,fabrication_ready=False)
(out/'annular_ring_audit_R138.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS all329 nominal rings and91 finite0.20mm bores; factory tolerance HOLD')
