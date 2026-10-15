"""Independent, source-bound static corners; not a converter or bench model."""
from pathlib import Path
import copy,hashlib,itertools,json,math,re,sys,xml.etree.ElementTree as E
import numpy as np
k,o=map(lambda s:Path(s).resolve(),sys.argv[1:3]);xml=E.parse(o/'netlist.xml');cs={c.get('ref'):c for c in xml.findall('./components/comp')};ns={(a.get('ref'),a.get('pin')):n.get('name')for n in xml.findall('./nets/net')for a in n.findall('node')}
def fields(c):return {f.get('name'):f.text or ''for f in c.findall('./fields/field')}
def value(c):
 s=c.findtext('value').split()[0];m=re.fullmatch(r'([\d.]+)([kMmunpR]?)(?:[FHA])?',s);assert m,s;return float(m[1])*{'':1,'R':1,'k':1e3,'M':1e6,'m':1e-3,'u':1e-6,'n':1e-9,'p':1e-12}[m[2]]
expected={('U11','1'):'RESET_SENSE',('U11','2'):'GND',('U11','3'):'3V3_SYS',('U11','4'):'3V3_SYS',('U11','5'):'RESET_CT',('U11','6'):'ESP_EN',('U4','2'):'REG_MODE',('U4','3'):'GND',('R14','1'):'REG_FB_TOP',('R14','2'):'REG_FB',('R15','1'):'REG_FB',('R15','2'):'GND'}
for ref,a,b in [('R95','3V3_SYS','RESET_SENSE'),('R96','RESET_SENSE','GND'),('R97','3V3_SYS','REG_MODE'),('R98','3V3_SYS','REG_FB_TOP'),('R99','REG_MODE','GND'),('C15','3V3_SYS','GND'),('C40','RESET_CT','GND'),('C41','RESET_SENSE','GND')]:expected[(ref,'1')]=a;expected[(ref,'2')]=b
parts={'U11':'TPS389001DSER','R14':'RT0603BRB0727K4L','R15':'RT0603BRB075K11L','R95':'RT0603BRB0716K5L','R96':'RT0603BRB0710KL','R98':'RT0603BRB07402RL','R97':'RC0603JR-070RL','R99':'RC0603JR-070RL','C40':'CC0603KRX7R9BB104','C41':'CC0603JRNPO9BN102'}
values={'R14':27400,'R15':5110,'R95':16500,'R96':10000,'R97':0,'R98':402,'R99':0,'C15':1e-7,'C40':1e-7,'C41':1e-9}
def contract(nodes,comps):
 assert all(nodes.get(q)==v for q,v in expected.items()),'Critical R144 pin mismatch'
 for ref,mpn in parts.items():assert fields(comps[ref])['MPN']==mpn,(ref,'MPN')
 for ref,v in values.items():assert math.isclose(value(comps[ref]),v,rel_tol=1e-12),(ref,'value')
 assert fields(comps['R97'])['Assembly']=='FIT'and fields(comps['R99'])['Assembly']=='DNP','Mode stuffing interlock'
 assert comps['U11'].findtext('footprint')=='ENKU:TPS3890_TI_DSE0006A_SMD_LEFT'
 assert {q for q,n in nodes.items()if n=='ESP_EN'}=={('U11','6'),('R17','2'),('U1','3'),('J7','6')}
 for pin in ['15','16','26','28','29','30']:assert nodes[('U1',pin)].startswith('unconnected-'),'Reserved/strap pin assigned'
contract(ns,cs);faults=[]
for name,key,wrong in [('MODE_ground',('U4','2'),'GND'),('AGND_MODE_swap',('U4','3'),'REG_MODE'),('U11_reset_ground',('U11','6'),'GND'),('U11_supply_battery',('U11','4'),'VBAT'),('MR_float',('U11','3'),'unconnected-test'),('sense_divider_short',('R96','1'),'3V3_SYS'),('CT_not_grounded',('C40','2'),'ESP_EN'),('PSRAM_pin_used',('U1','28'),'RESET_SENSE'),('strap45_used',('U1','26'),'RESET_CT')]:
 n=dict(ns);n[key]=wrong
 try:contract(n,cs)
 except AssertionError:faults.append(dict(case=name,result='REJECTED'))
 else:raise AssertionError('Ineffective negative case '+name)
for name,ref,key,v in [('old_R15','R15','value','4.99k 0.1% 10ppm'),('wrong_C40','C40','value','1nF'),('wrong_supervisor','U11','MPN','TLV803EA30DBZR'),('both_mode_links_fitted','R99','Assembly','FIT'),('PWM_link_missing','R97','Assembly','DNP')]:
 c=copy.deepcopy(cs);item=c[ref].find(key)if key=='value'else c[ref].find('./fields/field[@name="'+key+'"]');item.text=v
 try:contract(ns,c)
 except AssertionError:faults.append(dict(case=name,result='REJECTED'))
 else:raise AssertionError(name)
def rv(ref,sign,dt,tol=.001):return value(cs[ref])*(1+sign*tol)*(1+sign*10e-6*dt)
def supply(dt,tol=.001):
 vv=[]
 for a,b,c,f,ib in itertools.product([-1,1],repeat=5):
  r1,r2,rb=rv('R14',a,dt,tol),rv('R98',b,dt,tol),rv('R15',c,dt,tol);vf=.5*(1+f*.01);ii=ib*100e-9;vo=vf*(1+(r1+r2)/rb)+ii*(r1+r2);vv.append(vo)
  # Independent nodal solve including the series junction, not a copied ratio.
  mat=np.array([[1/r1+1/r2,-1/r1],[-1/r1,1/r1+1/rb]]);rhs=np.array([vo/r2,-ii]);sol=np.linalg.solve(mat,rhs);assert abs(sol[1]-vf)<1e-12
 return [min(vv),max(vv)]
def threshold(dt,ref=1.15,tol=.001):
 vv=[]
 for a,b,v,ib in itertools.product([-1,1],repeat=4):
  rt,rb=rv('R95',a,dt,tol),rv('R96',b,dt,tol);vv.append(ref*(1+v*.01)*(1+rt/rb)+ib*100e-9*rt)
 return [min(vv),max(vv)]
corners=[]
for temp in [-40,0,25,45,65,85,125]:
 dt=abs(temp-25);reg=supply(dt);fall=threshold(dt);rise_direct=threshold(dt,1.157);rise_conservative=fall[1]*1.00825
 corners.append(dict(temperature_C=temp,regulator_PWM_V=reg,reset_falling_V=fall,reset_rising_direct_V=rise_direct,reset_max_rising_conservative_V=rise_conservative,release_margin_mV=1000*(reg[0]-rise_conservative),panel_ceiling_margin_mV=1000*(3.3-reg[1])))
worst=min(x['release_margin_mV']for x in corners);ceiling=min(x['panel_ceiling_margin_mV']for x in corners);assert worst>=50 and ceiling>=25 and min(x['reset_falling_V'][0]for x in corners)>=3.0
scenario=[]
for label,tol in [('initial_only',.001),('initial_plus_0p1percent_solder_shift',.002),('initial_plus_0p1percent_solder_plus_0p5percent_life_shift',.007)]:
 reg=supply(100,tol);fall=threshold(100,tol=tol);scenario.append(dict(scenario=label,total_resistor_independent_tolerance=tol,regulator_PWM_V=reg,reset_falling_V=fall,maximum_rising_V=fall[1]*1.00825,initial_50mV_25mV_reserves_met=reg[0]-fall[1]*1.00825>=.05 and 3.3-reg[1]>=.025,conditional_slow_ramp_release_at_or_above_module_min=fall[0]>=3.0,interpretation='Declared independent adverse shifts; not a proven field-aging distribution or actual-lot acceptance'))
assert scenario[1]['initial_50mV_25mV_reserves_met'], 'Solder-shift reserve not met'
ct=value(cs['C40']);delay=dict(nominal_ms=1000*(ct*1e6*1.07+25e-6),scenario_min_ms=1000*ct*.9*.85*.9*1.17/1.35e-6,scenario_max_ms=1000*ct*1.1*1.15*1.29/.9e-6,effective_capacitance_and_leakage_are_guaranteed=False,physical_delay_test='NOT RUN')
report=dict(revision='R144',pcb_sha256=hashlib.sha256((k/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),method='Independent linear nodal solve and complete adversarial initial static corners',primary_sources=['TI TPS63802 SLVSEU9D','TI TPS3890 SLVSD65A','Yageo RT v17','Exact supplied GDEY0397T81P','Espressif WROOM v1.8'],nominal_output_V=.5*(1+(value(cs['R14'])+value(cs['R98']))/value(cs['R15'])),initial_static_corners=corners,minimum_initial_release_margin_mV=worst,minimum_initial_panel_margin_mV=ceiling,initial_declared_50mV_25mV_targets='PASS',life_and_solder_scenarios=scenario,CT=delay,sense_RC_nominal_us=1e6*value(cs['C41'])/(1/value(cs['R95'])+1/value(cs['R96'])),sense_divider_nominal_uA=1e6*(.5*(1+(value(cs['R14'])+value(cs['R98']))/value(cs['R15'])))/(value(cs['R95'])+value(cs['R96'])),forced_PWM_default_verified=True,initial_converter_soft_start_PFM_not_excluded=True,independent_effective_negative_cases=faults,physical_tests='NOT RUN',lifetime_and_dynamic_qualification='HOLD',fabrication_ready=False)
(o/'startup_envelope_R144.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS R144 source-bound initial static corners and',len(faults),'effective faults; dynamic/life/physical HOLD')
