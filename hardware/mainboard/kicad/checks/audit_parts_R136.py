"""Independent Laird/JST/Murata drawing constants and actual native solder windows."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import box,Point,Polygon
from shapely.ops import unary_union
from native_svg_shapes_R130 import actual_shapes
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());af=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R136.json').read_text())
fps={x['ref']:x for x in af['footprints']};ap={x['uuid']:x for x in af['pads']};groups=partitions(g)
xml=ET.parse(out/'netlist.xml' if server else c/'netlist_R136.xml');comps={x.attrib['ref']:x for x in xml.findall('./components/comp')}
# These constants are manufacturer drawing transcriptions, independent of the mutator.
expected={'J1':('JST','S2B-PH-SM4-TB(LF)(SN)'), 'J2':('Hirose','DM3AT-SF-PEJM5'),
 'J5':('GCT','USB4215-03-A'),'L1':('Murata','DFE201612E-R47M=P2'),
 'L2':('Laird Performance Materials','TYS5040470M-10'),'Q1':('Infineon','IRLML6346TRPBF'),
 'Q2':('Alpha & Omega Semiconductor','AO3401A'),'SW1':('G-Switch','MK-12C03-G015')}
for ref in ['SW3','SW4','SW5','SW6']:expected[ref]=('E-Switch','TL1016AAF160QG')
for ref,(maker,mpn) in expected.items():
 assert (fps[ref]['fields']['Manufacturer'],fps[ref]['fields']['MPN'])==(maker,mpn)
 sf={x.attrib['name']:x.text or '' for x in comps[ref].findall('./fields/field')}
 assert (sf['Manufacturer'],sf['MPN'])==(maker,mpn) and comps[ref].findtext('footprint')==g['footprints'][ref]['lib']
assert sum(bool(x['fields'].get('MPN')) for x in fps.values())==108
lands={}
for ref,size,positions,nets,angle in [
 ('L2',[1.4,4.2],[[56.15,43],[59.85,43]],['EPD_VCI','EPD_SW'],0),
 ('L1',[.8,1.8],[[61.2,90.2],[61.2,91.8]],['REG_L1','REG_L2'],-90)]:
 ps=sorted((x for x in g['pads'] if x['ref']==ref),key=lambda x:x['number']);assert len(ps)==2
 for q,pos,net in zip(ps,positions,nets):
  assert q['pos']==pos and q['size']==size and q['net']==net and (q['angle']-angle)%360==0 and q['shape']==1 and q['attribute']==1 and q['drill']==[0,0]
  assert set(ap[q['uuid']]['layers'])=={'F.Cu','F.Mask','F.Paste'} and not ap[q['uuid']]['local_mask_margin_IU'] and not ap[q['uuid']]['local_paste_margin_IU'] and not ap[q['uuid']]['local_paste_ratio']
  assert len(groups[net])==1
  lands[ref+':'+q['number']]=unary_union([Polygon(z) for z in q['polygons']['0']])
assert abs(lands['L2:1'].distance(lands['L2:2'])-2.3)<1e-9
via=next(t for t in g['tracks'] if t['uuid']=='0bad18f5-f207-4458-93c2-434f62be69d3');assert via['via'] and via['start']==[57.4,44.8] and via['width']==.5 and via['drill']==.3
vgap=lands['L2:1'].distance(Point(via['start']))-via['width']/2;assert abs(vgap-.3)<1e-9
native_apertures={}
for layer in ['F_Mask','F_Paste']:
 path=out/(layer+'.svg' if server else 'native_'+layer+'_R136.svg')
 roi=box(36.7,19.5,44.5,26.5);actual=unary_union(actual_shapes(path,roi))
 expected_shape=unary_union([box(37.45,20.9,38.85,25.1),box(41.15,20.9,42.55,25.1)])
 assert actual.symmetric_difference(expected_shape).area<.002,(layer,'Incorrect Laird aperture or extra opening')
 native_apertures[layer]=dict(ROI_mm=[36.7,19.5,7.8,7],aperture_count=2,area_mm2=actual.area,tented_relocated_via_not_in_solder_window=True)
j={x['number']:x for x in g['pads'] if x['ref']=='J1' and x['number'] in ['1','2']}
assert j.keys()=={'1','2'} and j['1']['pos']==[66.95,95.5] and j['2']['pos']==[66.95,93.5] and j['1']['net']=='VBAT' and j['2']['net']=='GND'
assert all(x['size']==[1,3.5] and x['angle']==90 for x in j.values())
mp=sorted(x['pos'] for x in g['pads'] if x['ref']=='J1' and x['number']=='MP');assert mp==[[72.7,91.15],[72.7,97.85]]
assert g['footprints']['J1']['pos']==[69.8,94.5] and g['footprints']['J1']['angle']==90
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R136',pcb_sha256=sha,explicit_native_board_and_schematic_MPN_fields=108,twelve_previous_missing_part_fields_closed=True,L2_Laird_RevA_G42_T14_H23_lands_verified=True,L2_interland_gap_mm=2.3,L2_via_annulus_to_land_mm=vgap,L2_native_mask_and_paste=native_apertures,L1_Murata_nominal_lands_and_pin_axis_verified=True,J1_JST_PH2_nominal_signal_and_bracket_lands_verified=True,J1_pin1_VBAT_pin2_GND_verified=True,J1_opening_direction='+boardX; mounting-side view, pin1 is south of pin2',connector_2A_current_and_polarity_harness_qualification=False,assembly_process_qualified=False,fabrication_ready=False)
(out/('parts_audit.json' if server else 'parts_audit_R136.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
