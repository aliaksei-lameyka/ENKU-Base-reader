"""Native netlist/assembly-backed numeric budgets; unknown guarantees stay unknown.

The 10% ageing reserve and leakage/parasitic allowances are engineering scenarios,
not manufacturer guarantees. A successful audit verifies inputs and arithmetic,
not capacitance, USB compliance, panel rails or bench behavior.
"""
import hashlib,json,math,sys,xml.etree.ElementTree as ET
from pathlib import Path
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
xml=ET.parse(out/'netlist.xml' if server else c/'netlist_R136.xml')
comps={x.attrib['ref']:x for x in xml.findall('./components/comp')}
af=json.loads((out/'assembly_features.json' if server else c/'assembly_features_R136.json').read_text())
fps={x['ref']:x for x in af['footprints']}
pinmap={(x.attrib['ref'],x.attrib['pin']):n.attrib['name'] for n in xml.findall('./nets/net') for x in n.findall('node')}
# Independently transcribed exact-part capacitance/tolerance/voltage tables.
parts={
 'CC0805KKX7R6BB105':(1,10,10,'X7R',['C2']),
 'CC0805KKX5R6BB106':(10,10,10,'X5R',['C13','C16']),
 'CC0805KKX7R8BB475':(4.7,10,25,'X7R',['C5','C24','C25','C26','C27','C28','C29','C31']),
 'CC0603KRX7R9BB104':(.1,10,50,'X7R',['C6','C10','C14','C17','C18','C19','C21','C37','C38']),
 'CC0805MKX5R6BB226':(22,20,10,'X5R',['C7','C8','C9','C11','C12']),
 'CC0603KRX7R9BB472':(.0047,10,50,'X7R',['C35']),
 'CC0603KRX7R8BB105':(1,10,25,'X7R',['C15','C22','C23']),
 'CC0805KKX7R8BB105':(1,10,25,'X7R',['C4','C30']),
 'CC0603JRNPO9BN102':(.001,5,50,'C0G',['C39'])
}
caps={}
for mpn,(nom,tol,v,diel,refs) in parts.items():
 for ref in refs:
  sf={x.attrib['name']:x.text or '' for x in comps[ref].findall('./fields/field')}
  assert sf['MPN']==mpn==fps[ref]['fields']['MPN']
  assert sf['Voltage']==str(v)+'V'==fps[ref]['fields']['Voltage']
  temp=.15 if diel!='C0G' else 30e-6*100 # C0G +/-30ppm/K, -55..125 relative25
  age=.9 if diel!='C0G' else 1.
  caps[ref]=dict(MPN=mpn,nominal_uF=nom,tolerance_percent=tol,rated_V=v,dielectric=diel,
    terminals={n:pinmap[(ref,n)] for n in ['1','2']},
    tolerance_temperature_ageing_scenario_before_DC_uF=nom*(1-tol/100)*(1-temp)*age,
    guaranteed_DC_retention=None,guaranteed_effective_uF=None,assembly_and_Ceff_qualified=False)
assert set(caps)=={ref for ref in comps if ref.startswith('C')} and len(caps)==32
for ref,net in [('C9','SYS_EN'),('C11','3V3_SYS'),('C12','3V3_SYS'),('C7','VSYS'),('C8','VBAT')]:
 assert pinmap[(ref,'1')]==net and pinmap[(ref,'2')]=='GND'
assert comps['U3'].findtext('value')=='BQ24072TRGTR' and comps['U4'].findtext('value')=='TPS63802DLAR'
def requirement(refs,minimum,source,bias):
 pre=sum(caps[x]['tolerance_temperature_ageing_scenario_before_DC_uF'] for x in refs)
 return dict(refs=refs,required_effective_uF=minimum,source=source,DC_test_V=bias,
    pre_DC_scenario_uF=pre,minimum_weighted_DC_retention_for_scenario=minimum/pre,
    guaranteed_effective_uF=None,qualified=False)
req={
 'TPS63802_input':requirement(['C9'],4,'SLVSEU9D p5 section8.3',4.59),
 'TPS63802_output_local':requirement(['C11','C12'],7,'SLVSEU9D p5 section8.3: VO>2.3V',3.3),
 'BQ24072T_SYS':requirement(['C7'],4.7,'SLUS937C p31 section11; conservative effective minimum4.7uF',4.59),
 'BQ24072T_BAT':requirement(['C8'],4.7,'SLUS937C p31 section11; conservative effective minimum4.7uF',4.24)
}
# Enumerate EVERY direct VBUS/GND capacitor from native net nodes, not a selected list.
direct=sorted(ref for ref,q in caps.items() if set(q['terminals'].values())=={'VBUS_USB','GND'})
assert direct==['C2','C4','C5','C6']
nom=sum(caps[x]['nominal_uF'] for x in direct)
tolerance_max=sum(caps[x]['nominal_uF']*(1+caps[x]['tolerance_percent']/100) for x in direct)
temp_budget=tolerance_max*1.15
assert abs(nom-6.8)<1e-10 and temp_budget<10
req['BQ24072T_IN']=requirement(direct,1,'SLUS937C p31 section11;1uF',5.5)
vbus=dict(direct_capacitors=direct,R126_nominal_direct_uF=15.8,R136_nominal_direct_uF=nom,
    tolerance_only_upper_at_reference_uF=tolerance_max,tolerance_and_temperature_budget_uF=temp_budget,
    additional_parasitic_allowance_uF=.25,total_scenario_uF=temp_budget+.25,
    target_direct_capacitance_uF=10,source='TI SLVA129 p1; USB-IF USB2 electrical compliance v1.07 p2 requires inrush test',
    DC_AC_voltage_and_all_charge_path_upper_bound_qualified=False,actual_inrush_qualified=False,
    charge_scenario_uC_at_5V=(temp_budget+.25)*5,charge_scenario_uC_at_5_5V=(temp_budget+.25)*5.5,
    note='Capacitance budget is not a guaranteed inrush result; voltage-dependent C, charger/system charge paths, cable/source and operating loads are unqualified.')
# Precise RT divider, fail-safe B comparator and actual native pin maps.
for ref,mpn in [('R70','RT0603BRD0726K7L'),('R71','RT0603BRD0710KL'),('R37','CRCW08052R20FKEAHP')]:
 assert fps[ref]['fields']['MPN']==mpn
expected={('U1','10'):'USB_VBUS_VALID',('U10','1'):'USB_VBUS_VALID',('U10','2'):'GND',('U10','3'):'USB_VBUS_DIV',('U10','4'):'USB_VBUS_REF',('U10','5'):'USB_VBUS_REF',('U10','6'):'3V3_SYS',('R70','1'):'VBUS_USB',('R70','2'):'USB_VBUS_DIV',('R71','1'):'USB_VBUS_DIV',('R71','2'):'GND',('R73','1'):'VBUS_USB',('R73','2'):'GND',('C39','1'):'USB_VBUS_DIV',('C39','2'):'GND',('R37','1'):'EPD_RESE',('R37','2'):'GND'}
assert all(pinmap[k]==v for k,v in expected.items())
assert comps['U10'].findtext('value')=='TLV3012BIDBVR'
dt=65;rt=.001+25e-6*dt
qmin=1+26700*(1-rt)/(10000*(1+rt));qmax=1+26700*(1+rt)/(10000*(1-rt))
vmin=(1.223-1.242*100e-6*dt-.009-.008)*qmin
vmax=(1.260+1.242*100e-6*dt+.009+.008)*qmax
# 100nA extra board leakage is an explicit scenario, not a TI hot-leakage max.
leak=.1e-6;leak_v=26700*(1+rt)*leak
vmin-=leak_v;vmax+=leak_v
rmax=1/(1/(3300*(1+.01+100e-6*dt))+1/(36700*(1+rt)))
passive_ms=(temp_budget+.25)*1e-6*rmax*math.log(5.5/vmin)*1000
filter_tau_us=(26700*10000/36700)*caps['C39']['nominal_uF']*1e-6*1e6
i=5.5/36700
divider=dict(temperature_C=[-40,85],threshold_scenario_V=[vmin,vmax],nominal_threshold_V=1.242*3.67,
    RT_tolerance_percent=.1,RT_TCR_ppm_K=25,additional_board_leakage_scenario_nA=100,
    R70_power_mW_at_5_5V=i*i*26700*1000,R71_power_mW_at_5_5V=i*i*10000*1000,
    R73_power_mW_at_5_5V=5.5**2/3300*1000,R73_bleeder_scenario_max_mA=5.5/(3300*(1-.01-100e-6*dt))*1000,
    passive_discharge_scenario_ms=passive_ms,C39_nominal_filter_tau_us=filter_tau_us,
    historical_1_085ms_assumption_invalid_for_current_source=True,actual_disconnect_latency_qualified=False,
    note='Passive RC only: no retained source/backfeed, stated capacitance/leakage assumptions. Excludes near-threshold comparator delay, power-on timing and firmware. TI4us delay is specified with100mV overdrive, not this slow crossing.')
assert 4.35<vmin<vmax<4.75
# Device power is independent of average PWM: repeated peak, voltage and film temperature also matter.
sense=[]
for ta in [25,70,85,125]:
 pw=.5 if ta<=70 else .5*(155-ta)/(155-70)
 rr=2.2*1.01*(1+100e-6*abs(ta-25))
 sense.append(dict(ambient_C=ta,derated_average_power_W=pw,worst_resistance_scenario_ohm=rr,maximum_RMS_current_scenario_A=math.sqrt(pw/rr)))
epd={ref:dict(nets=q['terminals'],rated_V=q['rated_V'],pre_DC_scenario_uF=q['tolerance_temperature_ageing_scenario_before_DC_uF'],
    exact_panel_required_effective_uF=None,actual_differential_voltage_including_overshoot_V=None,qualified=False)
    for ref,q in caps.items() if int(ref[1:]) in range(22,32)}
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report=dict(revision='R136',pcb_sha256=sha,native_32_capacitor_metadata_and_nets_verified=True,
    assumptions=dict(classII_temperature_retention=.85,classII_ageing_reserve_retention=.9,
       ageing_reserve_is_project_scenario_not_manufacturer_spec=True,DC_bias_guaranteed_lower_bound_available=False),
    capacitor_rows=caps,power_requirements=req,VBUS=vbus,VBUS_divider_and_discharge=divider,
    R37=dict(MPN='CRCW08052R20FKEAHP',initial_tolerance_percent=1,TCR_ppm_K=100,P70_W=.5,
       source='Vishay20043 rev17-Mar-2026 p1/2/3 ratings and code; p4/5/6 power/pulse; p9 lands',
       ambient_derating_scenarios=sense,actual_peak_current_A=None,actual_pulse_duration_s=None,actual_duty=None,
       repetitive_pulse_voltage_and_film_temperature_qualified=False),EPD=epd,
    typical_DC_curve_review=dict(source='Exact Yageo generated sheets page2, visually inspected; page4 says simulation, not specification',
       C9_retention_scenario_at_4_59V=.40,C9_effective_scenario_uF=13.464*.40,
       C11_C12_retention_scenario_at_3_4V=.55,C11_C12_effective_scenario_uF=26.928*.55,
       approximate_visual_scenarios_not_guaranteed_corner_bounds=True),
    input_validation_and_arithmetic_passed=True,all_Ceff_qualified=False,USB_inrush_and_suspend_qualified=False,
    R37_actual_pulse_thermal_qualified=False,EPD_power_qualified=False,fabrication_ready=False)
(out/'power_budget_audit_R136.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
