"""Independently check exact parts, physical pad axes, diode bands and DNP."""
import hashlib,json,math,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());af=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R126.json').read_text());ap={x['uuid']:x for x in af['pads']};fps={x['ref']:x for x in af['footprints']}
xml=ET.parse(out/'netlist.xml' if server else c/'netlist_R126.xml');comps={x.attrib['ref']:x for x in xml.findall('./components/comp')};groups=partitions(g)
# Explicit ordering codes, separately transcribed from RC_L v14's code table.
rs={
 '18k':('RC0603FR-0718KL',['R8']), '1k':('RC0603FR-071KL',['R9']),
 '100k':('RC0603FR-07100KL',['R10','R13','R16','R40','R72','R35','R36']),
 '10k':('RC0603FR-0710KL',['R11','R12','R17','R18']),
 '511k':('RC0603FR-07511KL',['R14']), '91k':('RC0603FR-0791KL',['R15']),
 '0R':('RC0603JR-070RL',['R19','R20','R21','R22','R28','R29','R64','R65','R67']),
 '47k':('RC0603FR-0747KL',['R23']), '4.7k':('RC0603FR-074K7L',['R24','R25']),
 '2M':('RC0603FR-072ML',['R26']), '680k':('RC0603FR-07680KL',['R27']),
 '1M':('RC0603FR-071ML',['R39','R38','R66']), '3.3k':('RC0603FR-073K3L',['R73']),
 '22R':('RC0603FR-0722RL',['R30','R31','R32','R33','R34']),
 '5.1k':('RC0603FR-075K1L',['R62','R63'])
}
caps={
 'CC0805KKX7R6BB105':(10,['C2']), 'CC0805KKX5R6BB106':(10,['C4','C9','C13']),
 'CC0805KKX7R8BB475':(25,['C5','C24','C25','C26','C31']),
 'CC0603KRX7R9BB104':(50,['C6','C10','C37']), 'CC0805KKX5R8BB106':(25,['C7']),
 'CC0805KKX5R6BB475':(10,['C8']), 'CC0805MKX5R6BB226':(10,['C11','C12']),
 'CC0603KRX7R9BB472':(50,['C35'])
}
expected={ref:(mpn,'Yageo','ENKU:R_RC0603_YAGEO_REFLOW') for _,(mpn,refs) in rs.items() for ref in refs}
for mpn,(v,refs) in caps.items():
 for ref in refs:expected[ref]=(mpn,'Yageo','ENKU:C_CC'+mpn[2:6]+'_YAGEO_REFLOW_TRANSFER')
for ref in ['D1','D2','D3']:expected[ref]=('MBR0530T1G','onsemi','ENKU:MBR0530T1G_ONSEMI_CASE425H')
expected['SW2']=('TL3342F160QG','E-Switch','ENKU:TL3342F160QG_ESWITCH_P010632J')
assert len(expected)==61
for ref,(mpn,maker,lib) in expected.items():
 assert g['footprints'][ref]['lib']==lib
 fields=fps[ref]['fields'];assert fields['MPN']==mpn and fields['Manufacturer']==maker,(ref,fields)
 sf={x.attrib['name']:x.text or '' for x in comps[ref].findall('./fields/field')}
 assert sf['MPN']==mpn and sf['Manufacturer']==maker and comps[ref].findtext('footprint')==lib,(ref,'native netlist metadata')
 assert fields['Assembly']==('DNP' if ref in ['R12','R67'] else 'FIT')
 # DNP is exported independently through the native KiCad FP_DNP flag.
 assert bool(fps[ref]['dnp'])==(ref in ['R12','R67']),(ref,'DNP changed')
 pads=[x for x in g['pads'] if x['ref']==ref]
 assert all(set(ap[x['uuid']]['layers'])=={'F.Cu','F.Mask','F.Paste'} and not ap[x['uuid']]['local_paste_margin_IU'] and not ap[x['uuid']]['local_paste_ratio'] for x in pads)
 assert all(len(groups[x['net']])==1 for x in pads if x['net']),(ref,'net disconnected')
 f=g['footprints'][ref];a=math.radians(f['angle']);co,si=math.cos(a),math.sin(a)
 def global_xy(x,y):return [round(f['pos'][0]+x*co+y*si,6),round(f['pos'][1]+y*co-x*si,6)]
 if ref=='SW2':
  exp=sorted((n,global_xy(x,y)) for n,x,y in [('1',-3.15,-1.9),('1',3.15,-1.9),('2',-3.15,1.9),('2',3.15,1.9)])
  assert sorted((x['number'],x['pos']) for x in pads)==exp
  assert all(x['size']==[1.7,1] and x['net']==('BOOT' if x['number']=='1' else 'GND') for x in pads)
 else:
  if ref.startswith('R'):pitch,size=1.7,[.9,.8]
  elif ref.startswith('D'):pitch,size=3.27,[.91,1.22]
  elif mpn.startswith('CC0603'):pitch,size=1.5,[.8,.9]
  else:pitch,size=1.85,[.95,1.4]
  assert len(pads)==2
  for q in pads:
   assert q['pos']==global_xy(-pitch/2 if q['number']=='1' else pitch/2,0) and q['size']==size and q['shape']==1,(ref,q)
   assert abs((q['angle']-f['angle'])%180)<1e-8,(ref,'Rectangular pad axes detached from package')
for ref,k,a in [('D1','EPD_VGH','EPD_SW'),('D2','GND','EPD_CP_NEG'),('D3','EPD_CP_NEG','EPD_VGL')]:
 q={x['number']:x for x in g['pads'] if x['ref']==ref};assert q['1']['net']==k and q['2']['net']==a
for mpn,(v,refs) in caps.items():
 for ref in refs:assert fps[ref]['fields']['Voltage']==str(v)+'V'
for ref in ['R20','R21','R22','R64','R65']:
 assert fps[ref]['fields']['Tuning MPN']=='RC0603FR-0722RL'
 assert '0R' in fps[ref]['value'] and 'tune' in fps[ref]['value']
# Neither a precision resistor nor the EPD pulse-current sense resistor is
# silently replaced by general RC0603 parts.
assert fps['R70']['value']=='26.7k 0.1% 25ppm' and fps['R71']['value']=='10k 0.1% 25ppm' and fps['R37']['value']=='2.2R 1% 0805'
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R126',pcb_sha256=sha,exact_MPNs_checked=61,resistors_checked=40,capacitors_checked=17,diodes_checked=3,switches_checked=1,all_physical_rectangular_pad_axes_match_package=True,all_MPNs_match_native_schematic_and_board=True,all_component_pad_net_groups_connected=True,D1_D2_D3_cathode_band_pin1_maps_verified=True,SW2_horizontal_common_rows_verified=True,R12_R67_DNP_preserved=True,five_0R_22R_tuning_options_preserved=True,precision_divider_and_EPD_sense_resistor_preserved=True,CC_land_patterns_are_engineering_transfer=True,CC_specific_assembly_land_approval=False,CC_effective_capacitance_under_DC_bias_qualified=False,diode_transient_reverse_voltage_thermal_and_leakage_qualified=False,dense_courtyard_assembly_process_qualified=False,fabrication_ready=False)
(out/'component_pass_audit_R126.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
