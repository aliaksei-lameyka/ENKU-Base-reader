"""Native battery interface and charger inputs plus explicit unqualified safety gates.

A passing audit confirms the measured CAD and arithmetic, INCLUDING detected
incompatibilities. It does not approve a battery, temperature window or charge.
"""
import hashlib,itertools,json,math,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());af=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R130.json').read_text());fps={x['ref']:x for x in af['footprints']};ap={x['uuid']:x for x in af['pads']}
xml=ET.parse(out/'netlist.xml' if server else c/'netlist_R130.xml');comps={x.attrib['ref']:x for x in xml.findall('./components/comp')};nodes={n.attrib['name']:{(a.attrib['ref'],a.attrib['pin']) for a in n.findall('node')} for n in xml.findall('./nets/net')};pinmap={a:n for n,ns in nodes.items() for a in ns}
assert pinmap[('J1','1')]=='VBAT' and pinmap[('J1','2')]=='GND' and ('J1','3') not in pinmap
assert nodes['BAT_TS']=={('U3','6'),('J8','1')} and pinmap[('J8','2')]=='GND'
assert comps['J1'].find('libsource').attrib['part']=='BAT2' and comps['J8'].find('libsource').attrib['part']=='NTC_WIRE2'
assert fps['J1']['fields']['MPN']=='S2B-PH-SM4-TB(LF)(SN)' and fps['J8']['attributes']==12 and not fps['J8']['fields'].get('MPN')
for ref,val,pins in [('R8','18k 1%',{'1':'CHG_ILIM_VSET','2':'GND'}),('R9','1k 1%',{'1':'CHG_ISET','2':'GND'}),('R10','100k',{'1':'CHG_CE_N','2':'GND'})]:
 assert fps[ref]['value']==comps[ref].findtext('value')==val
 assert {a['number']:a['net'] for a in g['pads'] if a['ref']==ref}==pins
for q in (x for x in g['pads'] if x['ref']=='J8'):
 assert set(ap[q['uuid']]['layers'])=={'F.Cu','F.Mask'} and not max(q['drill']) and q['attribute']==2
 assert len(partitions(g)[q['net']])==1
assert 'HOLD BAT-REV3' in fps['U3']['fields']['Charge Profile']
# SLUSF65B p8,p17,p18, and Semitec JT table (not a generic10k assumption).
bias=[36.5e-6,38e-6,39.5e-6];hot=[.105,.115,.125];cold=[.9575,1.0075,1.0575]
def inverse_beta(v,i,r25,b):return 1/(1/298.15+math.log(v/i/r25)/b)-273.15
def corners(v):return sorted(inverse_beta(a,i,r,b) for a,i,r,b in itertools.product([v[0],v[-1]],[bias[0],bias[-1]],[9900,10100],[3435*.99,3435*1.01]))
hot_corners=corners(hot);cold_corners=corners(cold)
# Table-based interpolation in ln(R), distinct from the constant-beta approximation.
rt={0:27700,10:18070,20:12110,25:10000,30:8301,40:5811,50:4147,60:3011,70:2224,80:1668,85:1451,90:1267}
def table_inverse(res):
 pairs=list(rt.items())
 for (ta,ra),(tb,rb) in zip(pairs,pairs[1:]):
  if rb<=res<=ra:return ta+(tb-ta)*math.log(res/ra)/math.log(rb/ra)
 raise ValueError('Outside reviewed R/T table')
hot_typ=table_inverse(hot[1]/bias[1]);cold_typ=table_inverse(cold[1]/bias[1])
r45=math.sqrt(rt[40]*rt[50]);ratio_needed=(cold[1]/bias[1])/(hot[1]/bias[1]);ratio_actual=rt[0]/r45
assert 59<hot_typ<61 and 0<cold_typ<2 and bias[0]*r45>hot[-1] and ratio_actual<ratio_needed
charge=[]
for q in [2000,2500]:charge.append(dict(capacity_mAh=q,nominal_charge_mA=300,ideal_Q_over_I_hours=q/300,fast_charge_timer_hours=6,nominal_six_hour_Q_mAh=1800,charge_complete_before_timer_proved=False))
faults=[
 dict(case='ambient25C, attached sensor',resistance_ohm=10000,nominal_TS_V=.38,expected='Temperature window permits charging; does not prove cell or timer safety'),
 dict(case='cell45C, attached103JT',approx_R_from_table_ohm=r45,expected='Still permits charging; does NOT enforce Akyga45C maximum'),
 dict(case='sensor open',expected='Floating TS clamp is documented; verify charge-inhibit and status on prototype. RevB electrical table gives no numerical VTS_CLAMP guarantee',bench_passed=False),
 dict(case='sensor short / TS-ground',expected='Hot/button charge inhibit. After10s with VIN present, removing VIN enters factory mode; valid VIN wakes. Qualify this fault',bench_passed=False),
 dict(case='sensor displaced from hot pouch',expected='Ambient10k is electrically indistinguishable from correctly attached cool cell. Mechanical retention and replacement inspection required',bench_passed=False),
 dict(case='battery unplugged with USB present',expected='BAT capacitor can cycle charge/complete; STAT2 toggles. Verify hot-swap, SYS stability and contact handling',bench_passed=False),
 dict(case='wrong pack polarity',expected='PH key does not standardize vendor wire polarity; reverse-polarity protection is unqualified; verify each harness pin-by-pin',bench_passed=False)]
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R130',battery_request='BAT-REV3',pcb_sha256=sha,native_PH2_and_separate_sensor_nodes_verified=True,actual_NTC_is_external_not_a_fixed_resistor=True,sensor_candidate=dict(MPN='103JT-050',R25_ohm=10000,R25_tolerance_percent=1,B25_85_K=3435,B_tolerance_percent=1,max_thickness_mm=.5,qualified=False),
 NTC=dict(hot_entry_nominal_C_from_manufacturer_RT_table=hot_typ,cold_entry_nominal_C_from_manufacturer_RT_table=cold_typ,constant_beta_hot_corner_scenario_C=[hot_corners[0],hot_corners[-1]],constant_beta_cold_corner_scenario_C=[cold_corners[0],cold_corners[-1]],corner_model_is_not_a_guaranteed_full_RT_tolerance_envelope=True,required_nominal_Rcold_Rhot_ratio=ratio_needed,actual_R0_R45_table_interpolation_ratio=ratio_actual,positive_series_parallel_resistors_cannot_increase_the_ratio=True,charge_window_0_45C_qualified=False),
 BQ25185=dict(source='SLUSF65B revisedAugust2026',battery_regulation_nominal_V=4.2,input_limit_nominal_mA=500,charge_current_nominal_mA=300,safety_timer_minutes=360,precharge_timer_minutes=90,safety_timer_reset='CE toggle or input power; not an approved automatic restart strategy',timer_pauses_on_TS_fault=True,precharge_has_a_separate_timer=True),
 charge_capacity_scenarios=charge,charge_time_note='Q/I is an optimistic reference. Precharge capacity, CV taper, system load, DPPM and thermal regulation require real cell-cycle data;1800mAh is nominal fast-stage input, not a universal total pack-capacity ceiling.',fault_matrix=faults,input_and_arithmetic_review_passed=True,thermal_window_redesign_required=True,full_capacity_charge_design_review_required=True,mechanical_NTC_retention_qualified=False,connector_2A_peak_current_and_harness_qualified=False,battery_vendor_and_PCM_qualified=False,prototype_fault_tests_passed=False,fabrication_ready=False)
(out/('battery_audit.json' if server else 'battery_audit_R130.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
