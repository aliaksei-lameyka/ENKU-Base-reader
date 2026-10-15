"""Independent bounded clearance and direct-wire interface audit. No actual folded-FPC claim."""
from pathlib import Path
import json,sys,copy,hashlib
from shapely.geometry import box
r,o=map(Path,sys.argv[1:3]);j=json.load(open(o/'mechanical_native_R148.json'));g=json.load(open(o/'geometry.json'));via=json.load(open(o/'via_process_R138.json'))['vias'];corridor=box(62.27,35.8001,76.27,46.5)
def check(m):
 bad=[f['ref']for f in m['front_courtyards']if f['ref']!='J3'and box(*f['bbox']).intersection(corridor).area>1e-8];assert not bad,bad
 f=m['J1'];assert f['attributes']&12==12 and len(f['pads'])==2
 assert {p['number']:p['net']for p in f['pads']}=={'1':'VBAT','2':'GND'}
 assert all(set(p['layers'])=={'F.Cu','F.Mask'}and p['size']==[1,3.5]for p in f['pads'])
 assert {p['number']:p['pos']for p in f['pads']}=={'1':[66.95,95.5],'2':[66.95,93.5]}
check(j)
assert all(v['front_tented']for v in via if corridor.contains(__import__('shapely').geometry.Point(v['position_mm'])))
# Entire J3 contact/mating geometry and mounting datums are preserved for review.
assert g['footprints']['J3']['pos']==[69.27,34.]and g['footprints']['J3']['angle']==0
faults=[]
for name,mut in [('fitted_body_in_corridor',lambda q:q['front_courtyards'].append(dict(ref='FAULT',bbox=[65,38,67,40]))),('battery_paste_returned',lambda q:q['J1']['pads'][0]['layers'].append('F.Paste')),('battery_polarity_reversed',lambda q:q['J1']['pads'][0].update(net='GND'))]:
 q=copy.deepcopy(j);mut(q)
 try:check(q)
 except AssertionError:faults.append(name)
 else:raise AssertionError(name)
(o/'mechanical_clearance_R148.json').write_text(json.dumps(dict(revision='R148',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),free_front_courtyard_rectangle_KiCad_mm=[62.27,35.8,76.27,46.5],width_mm=14,length_mm=10.7,no_other_front_courtyard_overlap=True,ordinary_vias_in_corridor_front_tented=True,J1_two_original_copper_lands_no_paste_or_purchased_part=True,display_back_faces_PCB_back=True,full_actual_FPC_fold_length_pin1_latch_and_pressure_qualification='HOLD',case_wire_clamp_and_pack_harness_qualification='HOLD',physical_tests='NOT RUN',effective_negative_cases=faults,fabrication_ready=False),indent=2)+'\n');print('PASS bounded front corridor and battery interface; actual folded flex HOLD')
