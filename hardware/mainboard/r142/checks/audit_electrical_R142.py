"""Actual-netlist independent linear MNA, corners, fault insertion and RC behavior.
Not SPICE, a manufacturer macromodel, a startup guarantee or a prototype test.
"""
import copy,hashlib,itertools,json,math,re,sys,xml.etree.ElementTree as E
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r,o=map(lambda x:Path(x).resolve(),sys.argv[1:3]);xml=E.parse(o/'netlist.xml');cs={x.get('ref'):x for x in xml.findall('./components/comp')};ns={(a.get('ref'),a.get('pin')):n.get('name')for n in xml.findall('./nets/net')for a in n.findall('node')}
def val(ref,components=cs):
 text=components[ref].findtext('value').split()[0];m=re.match(r'^([0-9.]+)([kMmunp]?)(?:[FHA]|ohm)?$',text);assert m,(ref,text);return float(m[1])*{'':1,'k':1e3,'M':1e6,'m':1e-3,'u':1e-6,'n':1e-9,'p':1e-12}[m[2]]
def fields(ref,components=cs):return {x.get('name'):x.text or''for x in components[ref].findall('./fields/field')}
expected={('U11','1'):'GND',('U11','2'):'ESP_EN',('U11','3'):'3V3_SYS',('C15','1'):'3V3_SYS',('C15','2'):'GND',('U1','3'):'ESP_EN',('R17','1'):'3V3_SYS',('R17','2'):'ESP_EN',('J7','6'):'ESP_EN',('J7','5'):'BOOT',('J7','3'):'UART_TX',('J7','4'):'UART_RX',('R18','1'):'3V3_SYS',('R18','2'):'BOOT',('U1','27'):'BOOT',('U1','32'):'SD_CD',('J2','9'):'SD_CD',('J2','10'):'GND',('R90','1'):'3V3_SYS',('R90','2'):'SD_CD',('R89','1'):'CHG_TS',('R89','2'):'GND'}
def contract(nodes,components):
 assert all(nodes[k]==v for k,v in expected.items()),'Critical reset/recovery/detection pin mismatch'
 assert components['U11'].findtext('value')==fields('U11',components)['MPN']=='TLV803EA30DBZR'
 for pin in ['15','16','26','28','29','30']:assert nodes[('U1',pin)].startswith('unconnected-'),'Strap/reserved memory pin used'
 assert {k for k,v in nodes.items()if v=='ESP_EN'}=={('U11','2'),('R17','2'),('U1','3'),('J7','6')}
 assert {k for k,v in nodes.items()if v=='SD_CD'}=={('J2','9'),('U1','32'),('R90','2')}
 assert all(val(ref,components)==10000 for ref in ['R23','R91','R92','R93','R94'])
 assert val('R17',components)==10000 and math.isclose(val('C15',components),1e-7,rel_tol=1e-14)
 assert val('R14',components)==27400 and val('R15',components)==4990
 assert fields('R14',components)['MPN']=='RT0603BRB0727K4L' and fields('R15',components)['MPN']=='RT0603BRB074K99L'
for ref,net in [('R23','SD_CS_CARD'),('R91','SD_MOSI_CARD'),('R92','SD_MISO_CARD'),('R93','SD_DAT1_BIAS'),('R94','SD_DAT2_BIAS')]:
 expected[(ref,'1')]='3V3_SYS';expected[(ref,'2')]=net
contract(ns,cs);negative=[]
for name,key,wrong in [('U11_GND_swap',('U11','1'),'3V3_SYS'),('U11_RESET_swap',('U11','2'),'GND'),('U11_raw_battery_supply',('U11','3'),'VBAT'),('old_RC_cap_on_EN',('C15','1'),'ESP_EN'),('UART_EN_lost',('J7','6'),'GND'),('BOOT_lost',('J7','5'),'3V3_SYS'),('SD_detect_wrong_GPIO',('U1','32'),'GND'),('SD_detect_ground_lost',('J2','10'),'SD_CD'),('TS_bias_ground_lost',('R89','2'),'BAT_TS'),('PSRAM_GPIO35_used',('U1','28'),'SD_CD'),('strap_GPIO45_used',('U1','26'),'SD_CD'),('SD_CMD_pullup_missing',('R91','2'),'GND'),('SD_unused_DAT1_floating',('R93','2'),'GND'),('SD_unused_DAT2_floating',('R94','2'),'GND')]:
 n=dict(ns);n[key]=wrong
 try:contract(n,cs)
 except AssertionError:negative.append(dict(case=name,result='REJECTED'))
 else:raise AssertionError('Ineffective fault '+name)
for name,ref,value in [('wrong_supervisor_delay_variant','U11','TLV803EB30DBZR'),('old_feedback_top','R14','511k 1%'),('old_feedback_bottom','R15','91k 1%'),('old_CS_pullup','R23','47k')]:
 c=copy.deepcopy(cs);c[ref].find('value').text=value
 try:contract(ns,c)
 except AssertionError:negative.append(dict(case=name,result='REJECTED'))
 else:raise AssertionError(name)
def mna(resistors,fixed,injections={}):
 un=sorted({n for rr,a,b in resistors for n in [a,b]}-fixed.keys());ix={n:i for i,n in enumerate(un)};mat=np.zeros((len(ix),len(ix)));rhs=np.array([injections.get(n,0)for n in un],float)
 for rr,a,b in resistors:
  if math.isinf(rr):continue
  for u,v in [(a,b),(b,a)]:
   if u not in ix:continue
   mat[ix[u],ix[u]]+=1/rr
   if v in ix:mat[ix[u],ix[v]]-=1/rr
   else:rhs[ix[u]]+=fixed[v]/rr
 result=np.linalg.solve(mat,rhs);return dict(fixed,**{n:float(result[i])for n,i in ix.items()})
def feedback(top,bot,dt,tolerance=.001,tcr=10e-6):
 values=[]
 for a,b,ta,tb,f,ib in itertools.product([-tolerance,tolerance],[-tolerance,tolerance],[-tcr,tcr],[-tcr,tcr],[-.01,.01],[-100e-9,100e-9]):
  rt=top*(1+a)*(1+ta*dt);rb=bot*(1+b)*(1+tb*dt);vf=.5*(1+f);vo=vf*(1+rt/rb)+ib*rt;values.append(vo)
  solved=mna([(rt,'3V3_SYS','REG_FB'),(rb,'REG_FB','GND')],{'GND':0,'3V3_SYS':vo},{'REG_FB':-ib});assert abs(solved['REG_FB']-vf)<1e-12
 return [min(values),max(values)]
fb={str(t):feedback(val('R14'),val('R15'),abs(t-25))for t in [-40,0,25,45,85,125]};rise=3.08*1.02*1.015;old=feedback(511000,91000,65,.01,100e-6);assert old[0]<rise<min(v[0]for v in fb.values())and max(v[1]for v in fb.values())<3.3;nom=.5*(1+val('R14')/val('R15'))
rng=np.random.default_rng(142);mc=rng.uniform(-1,1,(50000,6));rt=val('R14')*(1+.001*mc[:,0])*(1+.001*mc[:,2]);rb=val('R15')*(1+.001*mc[:,1])*(1+.001*mc[:,3]);vv=.5*(1+.01*mc[:,4])*(1+rt/rb)+100e-9*mc[:,5]*rt;assert vv.min()>min(v[0]for v in fb.values())and vv.max()<max(v[1]for v in fb.values())
tau=.01;ramps=[]
for seconds,rr,cc in itertools.product([.0001,.001,.01,.1,1,10],[.99,1.01],[.9,1.1]):
 t=np.linspace(0,seconds+.15,20001);v=np.minimum(3.3,3.3*t/seconds);tm=tau*rr*cc;en=np.where(t<=seconds,3.3/seconds*(t-tm*(-np.expm1(-t/tm))),3.3-3.3/seconds*tm*(-np.expm1(-seconds/tm))*np.exp(-np.maximum(t-seconds,0)/tm));k=np.flatnonzero((en>=.75*v)&(v>.001))[0];ramps.append(dict(ramp_s=seconds,R_factor=rr,C_factor=cc,old_logical_release_supply_V=float(v[k]),release_before_3V0=bool(v[k]<3.),logic_threshold_assumption_ratio=.75))
for seconds in [.001,.1,1]:
 t=np.linspace(0,seconds+.3,12000);v=np.minimum(3.3,3.3*t/seconds);en=np.where(t<=seconds,3.3/seconds*(t-tau*(-np.expm1(-t/tau))),3.3-3.3/seconds*tau*(-np.expm1(-seconds/tau))*np.exp(-np.maximum(t-seconds,0)/tau));new=np.where(t<seconds*rise/3.3+.13,0,v);fig,ax=plt.subplots(figsize=(9,3.7));ax.plot(t*1000,v,label='Supply scenario');ax.plot(t*1000,en,label='R141 RC');ax.plot(t*1000,new,label='R142 threshold +130ms behavior');ax.axhline(3.,ls='--',color='#a33333',label='Module minimum');ax.set(xlabel='Time, ms',ylabel='V',title=f'Ramp {seconds*1000:g}ms: behavioral model, not a prototype waveform');ax.grid(alpha=.2);ax.legend(fontsize=8,ncol=2);fig.tight_layout();fig.savefig(o/f'reset_ramp_{seconds:g}s.png',dpi=160);plt.close(fig)
reset=dict(supervisor='TLV803EA30DBZR',falling_threshold_V=[3.08*.98,3.08*1.02],maximum_rising_threshold_V=rise,release_delay_ms=[130,200,270],panel_VCI_max_V=3.3,static_panel_margin_mV=(3.3-max(v[1]for v in fb.values()))*1000,feedback_resistor_tolerance_percent=.1,feedback_resistor_TCR_ppm_K=10,long_term_resistance_shift_and_PFM_limits_qualified=False,nominal_output_V=nom,feedback_ranges_by_resistor_temperature_C=fb,maximum_static_output_V=max(v[1]for v in fb.values()),minimum_PWM_static_release_margin_mV=(min(v[0]for v in fb.values())-rise)*1000,old_feedback_range_at_abs65K_V=old,reset_output_sink_max_mA=3.6/(10000*.99)*1000,reset_low_max_V_at_specified_VDD1p7V_and0p5mA=.3,UART_EN_wired_OR=True,old_RC_ramp_scenarios=ramps,old_EN_remaining_V_after_100us_zero_supply_ideal_resistive_discharge=3.3*math.exp(-.0001/tau),Monte_Carlo=dict(samples=50000,seed=142,distribution='Uniform independent scenario, not failure probability',output_range_V=[float(vv.min()),float(vv.max())]),PFM_dynamic_regulation_fast_dips_and_bench_qualification=False)
table={0:27700.,10:18070.,20:12110.,25:10000.,30:8301.,40:5811.,50:4147.}
def therm(t):
 if t in table:return table[t]
 a,b=next((a,b)for a,b in zip(table,list(table)[1:])if a<t<b);return math.exp(math.log(table[a])+(t-a)/(b-a)*math.log(table[b]/table[a]))
def ntc(t,over={},leak=0,vin=4.35):
 res=[(over.get(ref,val(ref)),ns[(ref,'1')],ns[(ref,'2')])for ref in ['R80','R81','R82','R89']]+[(over.get('NTC',therm(t)),'BAT_TS','GND')];return mna(res,{'GND':0,'VBUS_USB':vin},{'CHG_TS':leak})['CHG_TS']/vin
temps=[]
for t in [0,25,45]:
 vv=[]
 for tol in itertools.product([-.01,.01],repeat=6):
  over={ref:val(ref)*(1+tol[i])*(1+(-1 if tol[i]<0 else 1)*100e-6*abs(t-25))for i,ref in enumerate(['R80','R81','R82','R89'])};over['NTC']=therm(t)*(1+tol[4])*math.exp(3435*tol[5]*(1/(t+273.15)-1/298.15));vv.extend(ntc(t,over,l)for l in [-.1e-6,0,.1e-6])
 lo,hi=min(vv),max(vv);assert (lo>.255 if t==0 else hi<.12 if t==45 else .13<lo<hi<.245);temps.append(dict(temperature_C=t,TS_VIN_ratio=[lo,hi],guaranteed_manufacturer_RT_or_TS_leakage_envelope=False))
faults=[]
for name,over,t in [('NTC_open',{'NTC':math.inf},25),('NTC_short',{'NTC':1e-6},25),('R80_open',{'R80':math.inf},25),('R80_short',{'R80':1e-6},25),('R81_open_hot',{'R81':math.inf},45),('R81_short',{'R81':1e-6},25),('R82_open',{'R82':math.inf},25),('R82_short',{'R82':1e-6},25),('R89_open_hot',{'R89':math.inf},45),('R89_short',{'R89':1e-6},25),('sensor_detached_hot_cell',{},25)]:
 vv=[ntc(t,over,l)for l in [-.1e-6,0,.1e-6]];faults.append(dict(fault=name,TS_VIN_ratio=[min(vv),max(vv)],inhibit_in_stated_scenario=max(vv)<.12 or min(vv)>.255,bench_passed=False))
temperature=dict(corners=temps,faults=faults,R82_100k_protection_retained=val('R82')==100000,R89_passive_bias_ohm=val('R89'),R82_open_absolute_leakage_budget_nA=.12*4.35/(val('R89')*1.01*(1+100e-6*65))*1e9,absolute_TS_leakage_scenario_nA=100,guaranteed_TI_TS_leakage_available=False,RT_model='Semitec table scaled by R25/B scenarios; not a guaranteed envelope',sensor_detachment_not_electrically_detected=True,all_faults_fail_safe=False,qualification='HOLD')
rth=1/(1/val('R26')+1/val('R27'));adc_tau=rth*val('C21');i2c=[dict(capacitance_scenario_pF=c,rise_30_70_ns=.8473*val('R24')*1.01*1.0065*c*.001,passes_400kHz=.8473*val('R24')*1.01*1.0065*c*.001<=300)for c in [25,50,75,100,200,400]]
interfaces=dict(ADC=dict(nominal_time_constant_ms=adc_tau*1000,settle_0p1percent_conservative_scenario_ms=adc_tau*1.016565*1.265*math.log(1000)*1000,firmware_wait_after_rail_valid_ms=500,nominal_BAT4V24_ADC_V=4.24*val('R27')/(val('R26')+val('R27')),absolute100nA_leakage_error_V=rth*.1e-6,sampling_calibration_and_leakage_qualified=False),I2C=dict(bringup_clock_Hz=100000,capacitance_scenarios=i2c,fast400kHz_requires_measured_300ns_rise=True),SD=dict(GPIO39_input_disable_internal_pulldown_before_interpretation=True,inserted_pullup_current_at_nominal_mA=nom/val('R90')*1000,contact_A_B=['J2.9','J2.10'],hot_removal_USBMSC_exclusive_SPI_ownership_qualified=False),recovery=dict(UART_J7_reference_is_not_a_power_input=True,external_UART_3V3_logic_only=True,GPIO0_download_pullup='10k; manual low on J7.5',GPIO35_36_37_reserved_R8_unassigned=True,actual_ROM_flash_PSRAM_tests='NOT RUN'))
power=dict(charge_current_nom_min_max_mA=[445,797/(2000*1.01)*1000,975/(2000*.99)*1000],BQ_BAT_max_V=4.24,USB100_default_min_max_mA=[90,100],no_battery_USB100_full_reader_start_not_guaranteed=True,do_not_force_500mA_before_USB_authorization=True,first_flash_requires_qualified_battery_or_battery_simulator=True,actual_battery_PCM_harness_and_panel_SD_peak_current_unknown=True)
report=dict(revision='R142',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),method='Independent NumPy MNA + adversarial corners + Monte Carlo + analytic RC behavior; NOT SPICE/macromodel/bench',effective_negative_cases=negative,reset=reset,temperature=temperature,interfaces=interfaces,power=power,physical_tests='NOT RUN',fabrication_ready=False)
(o/'independent_electrical_R142.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS actual netlist independent calculations and',len(negative),'effective negative cases; physical HOLD',flush=True)
