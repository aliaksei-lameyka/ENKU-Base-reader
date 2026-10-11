"""Independent manufacturer geometry and assembly-layer checks, local or CI."""
import hashlib,json,sys
from pathlib import Path
from shapely.geometry import box,Point
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text())
revision=json.loads((c/'current_checkpoint.json').read_text())['revision']
af=json.loads((out/'assembly_features.json' if server else c/('assembly_features_'+revision+'.json')).read_text());a={x['uuid']:x for x in af['pads']};groups=partitions(g)
# Constants are independently transcribed from the visually inspected drawings,
# not read from the implementation recipe or generic KiCad footprint library.
maps={
 'Q1':('ENKU:IRLML6346_INFINEON_MICRO3',[.972,.802],1,{'1':('EPD_GDR',[66.115,47.05]),'2':('EPD_RESE',[66.115,48.95]),'3':('EPD_SW',[67.885,48])}),
 'Q2':('ENKU:AO3401A_AOS_SOT23',[.8,.8],1,{'1':('PWR_GATE',[54.3,81.55]),'2':('VSYS',[54.3,83.45]),'3':('SYS_EN',[56.7,82.5])}),
 'U9':('ENKU:TMUX1101_TI_DBV0005A',[1.1,.6],4,{'1':('BAT_ADC_SW',[34.2,69.05]),'2':('VBAT',[34.2,70]),'3':('GND',[34.2,70.95]),'4':('3V3_SYS',[36.8,70.95]),'5':('VBAT',[36.8,69.05])})
}
for ref,(lib,size,shape,pins) in maps.items():
 assert g['footprints'][ref]['lib']==lib
 pads={x['number']:x for x in g['pads'] if x['ref']==ref};assert pads.keys()==pins.keys()
 for n,(net,pos) in pins.items():
  q=pads[n];z=a[q['uuid']];assert (q['net'],q['pos'],q['size'],q['shape'],q['attribute'],q['layers'],q['drill'])==(net,pos,size,shape,1,[0],[0,0]),(ref,n)
  assert set(z['layers'])=={'F.Cu','F.Mask','F.Paste'} and not z['local_paste_margin_IU'] and not z['local_paste_ratio']
  assert len(groups[net])==1,(ref,n,'Disconnected net')
  if ref=='U9':assert z['roundrect_radius_mm']==.05
u=[x for x in af['pads'] if x['ref']=='U1'];paste=[x for x in u if 'F.Paste' in x['layers'] and x['number']==''];assert len(paste)==9
expected={(x,y) for x in [34.06,35.46,36.86] for y in [45.1,46.5,47.9]}
assert {tuple(x['position_mm']) for x in paste}==expected
assert all(x['size_mm']==[.9,.9] and x['layers']==['F.Paste'] and not x['local_paste_margin_IU'] and not x['local_paste_ratio'] for x in paste)
ep=[x for x in u if x['number']=='41'];assert len(ep)==13 and all('F.Paste' not in x['layers'] for x in ep)
solid=[x for x in ep if x['attribute']==1];assert len(solid)==1 and solid[0]['size_mm']==[3.9,3.9]
holes=[x for x in ep if x['attribute']==0];assert len(holes)==12 and all(x['drill_mm']==[.3,.3] and x['size_mm']==[.6,.6] for x in holes)
gap=min(box(x-.45,y-.45,x+.45,y+.45).distance(Point(*h['position_mm']))-h['drill_mm'][0]/2 for x,y in expected for h in holes)
assert gap>=.1-1e-9,('Paste aperture overlaps nominal thermal via hole',gap)
j=[x for x in af['pads'] if x['ref']=='J7' and x['number']];assert len(j)==6
assert all(set(x['layers'])=={'B.Cu','B.Mask'} and x['size_mm']==[.7874,.7874] for x in j)
shield=[x for x in g['pads'] if x['ref']=='J5' and x['number']=='S'];assert len(shield)==4 and all(x['net']=='USB_SHIELD' for x in shield)
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision=revision,pcb_sha256=sha,manufacturer_nominal_Q1_Q2_U9_lands_match=True,manufacturer_Q1_Q2_U9_pin_maps_match=True,all_changed_component_net_groups_connected=True,U9_TMUX1101_DBV_pinout_verified=True,U1_nine_paste_apertures_verified=True,U1_EP_paste_aperture_size_mm=[.9,.9],U1_nominal_paste_to_thermal_hole_gap_mm=round(gap,6),U1_EP_paste_area_mm2=7.29,U1_EP_solid_copper_area_mm2=15.21,U1_EP_solid_copper_and_03_drill_process_adaptation=True,U1_manufacturer_island_copper_pattern_not_reproduced=True,U1_thermal_via_mask_and_wicking_process_qualified=False,J7_six_contact_pads_have_no_paste=True,J5_four_S_shield_pad_mappings_verified=True,nominal_geometry_review_passed=True,assembly_process_qualified=False,fabrication_ready=False)
(out/('component_lands_audit_'+revision+'.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
