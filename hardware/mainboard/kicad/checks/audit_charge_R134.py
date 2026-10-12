"""Check native charger network and bounded primary-source math, retaining unknowns."""
import hashlib,itertools,json,math,sys,xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';out=Path(sys.argv[2]).resolve()
g=json.loads((out/'geometry.json').read_text());af=json.loads((out/'assembly_features.json').read_text());fps={x['ref']:x for x in af['footprints']}
xml=ET.parse(out/'netlist.xml');comps={x.attrib['ref']:x for x in xml.findall('./components/comp')}
nodes={(a.attrib['ref'],a.attrib['pin']):n.attrib['name'] for n in xml.findall('./nets/net') for a in n.findall('node')}
expected=['CHG_TS','VBAT','VBAT','CHG_CE_N','CHG_EN2','CHG_EN1','CHG_STAT1','GND','CHG_STAT2','VSYS','VSYS','CHG_ILIM_VSET','VBUS_USB','CHG_TMR','GND','CHG_ISET','GND']
assert fps['U3']['fields']['MPN']=='BQ24072TRGTR'
for n,net in enumerate(expected,1):assert nodes[('U3',str(n))]==net
assert nodes[('J1','1')]=='VBAT' and nodes[('J1','2')]=='GND' and ('J1','3') not in nodes
assert nodes[('J8','1')]=='BAT_TS' and nodes[('J8','2')]=='GND'
assert fps['J8']['attributes']==12 and not fps['J8']['fields'].get('MPN')
support={'R8':('3.48k 1%','RC0603FR-073K48L',['CHG_ILIM_VSET','GND']),
 'R9':('2k 1%','RC0603FR-072KL',['CHG_ISET','GND']),
 'R10':('100k','RC0603FR-07100KL',['CHG_CE_N','GND']),
 'R11':('10k','RC0603FR-0710KL',['3V3_SYS','CHG_STAT1']),
 'R12':('10k','RC0603FR-0710KL',['3V3_SYS','CHG_STAT2']),
 'R80':('31.6k 1%','RC0603FR-0731K6L',['VBUS_USB','BAT_TS']),
 'R81':('19.6k 1%','RC0603FR-0719K6L',['BAT_TS','GND']),
 'R82':('100k 1%','RC0603FR-07100KL',['BAT_TS','CHG_TS']),
 'R83':('69.8k 1%','RC0603FR-0769K8L',['CHG_TMR','GND'])}
groups=partitions(g)
for ref,(value,mpn,pins) in support.items():
 assert fps[ref]['value']==comps[ref].findtext('value')==value
 assert fps[ref]['fields']['MPN']==mpn and not fps[ref]['dnp']
 assert [nodes[(ref,str(n))] for n in [1,2]]==pins
 for net in pins:assert len(groups[net])==1,(ref,net,'Split physical network')
for ref in ['C7','C8']:
 assert fps[ref]['value']=='22uF 10V' and fps[ref]['fields']['MPN']=='CC0805MKX5R6BB226'
 assert fps[ref]['fields']['Datasheet']=='https://yageogroup.com/download/specsheet/CC0805MKX5R6BB226'
# SLUS937C p7-9: thresholds0.245..0.255VIN and0.12..0.13VIN, KISET797..975.
# Semitec103JT-050 nominal R/T table. ln(R) interpolation does not give a guaranteed tolerance envelope.
rt={0:27700,10:18070,20:12110,25:10000,30:8301,40:5811,50:4147,60:3011,70:2224,80:1668,85:1451,90:1267}
def table_inverse(res):
 for (a,ra),(b,rb) in zip(list(rt.items()),list(rt.items())[1:]):
  if rb<=res<=ra:return a+(b-a)*math.log(res/ra)/math.log(rb/ra)
 raise ValueError('Outside table')
def R_at_fraction(f,up,parallel):return 1/(1/(up*f/(1-f))-1/parallel)
def trip_beta(f,up,parallel,r25,beta):
 resistance=R_at_fraction(f,up,parallel)
 return 1/(1/298.15+math.log(resistance/r25)/beta)-273.15
cold_nom=table_inverse(R_at_fraction(.25,31600,19600));hot_nom=table_inverse(R_at_fraction(.125,31600,19600))
def trip_corners(thresholds):
 return sorted(trip_beta(f,u,v,rt,b) for f,u,v,rt,b in itertools.product(thresholds,[31600*.99,31600*1.01],[19600*.99,19600*1.01],[9900,10100],[3435*.99,3435*1.01]))
cold=trip_corners([.245,.255]);hot=trip_corners([.12,.13])
assert cold[0]>0 and hot[-1]<45 and 4<cold_nom<6 and 39<hot_nom<41
open_min=(19600*.99)/(31600*1.01+19600*.99);assert open_min>.255
def fraction(R,u=31600,v=19600):
 parallel=1/(1/R+1/v);return parallel/(u+parallel)
assert fraction(rt[0])>.255 and fraction(math.sqrt(rt[40]*rt[50]))<.12
assert .255>fraction(10000)>.13
Imin,Ityp,Imax=797/(2000*1.01),890/2000,975/(2000*.99)
timer=[10*69.8*.99*35/3600,10*69.8*45/3600,10*69.8*1.01*55/3600]
assert 18<69.8*.99<69.8*1.01<72
report=dict(revision='R134',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],
 primary_datasheet='TI SLUS937C December2019, RGT0016C4222419/E07/2025; PDF SHA2566f09e139e13a7bca407b4e8608ed0c387e43ba8c1d3705b4f9872b82495ea71c',
 independent_native_17_pin_map_and_support_network_verified=True,
 sensor='Semitec103JT-050 real cell sensor;10k1%,B25/85=3435K1%,max film0.5mm',
 direct_PH2_and_separate_sensor_retained=True,CHG_CE_GPIO_control_TD_low_timer_enabled=True,reset_OFF_input_mode_high_Z_model="USB100",
 USB500_input_limit_min_typ_max_mA=[450,475,500],
 current_min_typ_max_mA=[1000*a for a in [Imin,Ityp,Imax]],fast_timer_min_typ_max_hours=timer,
 precharge_timer_min_typ_max_hours=[a/10 for a in timer],
 TS_nominal_cold_hot_table_C=[cold_nom,hot_nom],TS_constant_beta_cold_corner_C=[cold[0],cold[-1]],
 TS_constant_beta_hot_corner_C=[hot[0],hot[-1]],TS_open_minimum_ratio=open_min,TS_short_ratio=0,
 modeled_open_short_0C_45C_inhibit=True,modeled_25C_allows_charge=True,
 TS_series100k_protection_retained=True,
 leakage_TS_input_series_drop_guarantee=None,guaranteed_full_NTC_R_T_tolerance_envelope=None,
 temperature_attachment_lag_self_heating_and_fault_bench_qualified=False,charge_window_0_45C_qualified=False,
 fast_full_capacity_before_min_timer_proved=False,automatic_timer_restart_workaround=False,
 PGOOD_CHG_firmware_contract_changed=True,USB_enumeration_suspend_and_inrush_qualified=False,
 SYS_tracks_VBAT_plus225mV=True,SYS_FET_hard_switch_retained=True,
 peak_current_PCM_harness_polarity_and_supplier_pack_qualified=False,
 capacitors_effective_minimum_qualified=False,charger_thermal_spreading_qualified=False,
 prototype_fault_tests_passed=False,fabrication_ready=False)
(out/'charge_audit_R134.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
