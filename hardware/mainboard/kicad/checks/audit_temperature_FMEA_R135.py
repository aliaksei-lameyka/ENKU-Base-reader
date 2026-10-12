"""Bounded voltage-TS fault/leakage analysis; unknown RT/leakage remain gates.

R/T data: Semitec P9-JT, not a constant-beta curve presented as a guarantee.
The table-scaled B variation below is only an engineering scenario: a B25/85
tolerance does not specify the guaranteed R/T envelope at every temperature.
"""
import itertools, json, math, sys
from pathlib import Path

root, out = map(lambda s: Path(s).resolve(), sys.argv[1:3])
sha = (out/'source_pcb.sha256').read_text().split()[0]
rt = {0:27700.,10:18070.,20:12110.,25:10000.,30:8301.,40:5811.,50:4147.}
def r_table(temp):
    if temp in rt: return rt[temp]
    for a,b in zip(rt, list(rt)[1:]):
        if a < temp < b:
            return math.exp(math.log(rt[a])+(temp-a)/(b-a)*math.log(rt[b]/rt[a]))
    raise ValueError(temp)
def network(res, upper=40200., lower=33200., series=100000.):
    inv = (0 if math.isinf(res) else 1/res)+(0 if math.isinf(lower) else 1/lower)
    parallel = 1/inv
    return parallel/(upper+parallel), series+1/(1/upper+inv)
def at_temp(temp):
    return [r_table(temp)*r25*math.exp((b-3435)*(1/(temp+273.15)-1/298.15))
            for r25,b in itertools.product([.99,1.01],[3435*.99,3435*1.01])]
budgets = {}
for temp,trip in [(0,.255),(45,.12)]:
    margins = []
    for res,upper,lower,series,vin in itertools.product(at_temp(temp),[40200*.99,40200*1.01],
         [33200*.99,33200*1.01],[100000*.99,100000*1.01],[4.35,4.75,5.,5.25]):
        ratio,z = network(res,upper,lower,series)
        gap = ratio-trip if temp==0 else trip-ratio
        margins.append(vin*gap/z*1e9)
    assert min(margins)>0
    budgets[str(temp)] = min(margins)
fault_budget=[]
for res,upper,series,vin in itertools.product(at_temp(45),[40200*.99,40200*1.01],[100000*.99,100000*1.01],[4.35,4.75,5.,5.25]):
    ratio,z=network(res,upper=upper,lower=math.inf,series=series)
    fault_budget.append(vin*(.12-ratio)/z*1e9)
assert min(fault_budget)>250
budgets['R81_open_at45C']=min(fault_budget)
faults = []
for name,ratio,status in [
 ('sensor_open', network(math.inf)[0], 'cold_inhibit'),
 ('sensor_short', 0., 'hot_inhibit'),
 ('R80_open', 0., 'hot_inhibit'),
 ('R80_short', 1., 'cold_inhibit'),
 ('R81_short', 0., 'hot_inhibit'),
 ('R81_open_at45C', network(r_table(45),lower=math.inf)[0], 'hot_inhibit'),
 ('R82_open', None, 'floating_TS_not_qualified'),
 ('R82_short', None, 'series_fault_protection_lost'),
 ('sensor_detached_from_hot_cell', network(r_table(25))[0], 'unsafe_charge_possible'),
]:
    if status.endswith('_inhibit'): assert ratio<.12 or ratio>.255
    if name=='R81_open_at45C': assert ratio<.12
    faults.append(dict(fault=name,nominal_TS_VIN_ratio=ratio,model_result=status,bench_passed=False))
sweep = []
for leak_uA in [0,.1,.25,.5,1.]:
    sweep.append(dict(absolute_TS_leakage_scenario_uA=leak_uA,
        zero_C_inhibits_all_table_scaled_scenarios=leak_uA*1000<budgets['0'],
        fortyfive_C_inhibits_all_table_scaled_scenarios=leak_uA*1000<budgets['45']))
heating=[]
for t in range(0,46):
    res=r_table(t);ratio,_=network(res); power_mW=(5.25*ratio)**2/res*1000
    heating.append(power_mW/.7)
current_min=797/(2000*1.01)
timer_min=10*69.8*.99*35/3600
capacity=[dict(capacity_mAh=q,ideal_constant_current_time_at_min_I_hours=q/1000/current_min,
               minimum_fast_timer_hours=timer_min,
               remaining_ideal_CV_time_hours=timer_min-q/1000/current_min,
               charge_loss_CV_precharge_and_timer_scaling_not_proved=True)for q in [2000,2500]]
report=dict(revision='R135',pcb_sha256=sha,
    primary_sources=dict(Semitec_P9_JT_pdf_sha256='b430302b8002752e077803c594dac29ce98e86361444394faba51096d723b266',
                        TI_SLUS937C_pdf_sha256='6f09e139e13a7bca407b4e8608ed0c387e43ba8c1d3705b4f9872b82495ea71c'),
    source_voltage_scenarios_V=[4.35,4.75,5.,5.25],
    RT_envelope_is_table_scaled_B_scenario_not_manufacturer_guarantee=True,
    maximum_absolute_TS_leakage_for_stated_0C_45C_scenarios_nA=budgets,
    TI_guaranteed_TS_input_leakage_available=False,
    leakage_sweep=sweep, faults=faults,
    max_nominal_self_heating_5V25_using_approx_0p7mW_per_C=float(max(heating)),
    Semitec_approx_midair_time_constant_s=5.,attached_sensor_response_qualified=False,
    ideal_charge_time_comparison=capacity,
    sensor_polarity_error_into_battery_voltage_and_TS_clamp_not_bench_qualified=True,
    all_faults_fail_safe=False, guaranteed_charge_window_qualified=False,
    R81_open_45C_inhibits_stated_table_scaled_scenarios_with_250nA_absolute_leakage=True,actual_cell_and_fault_tests_passed=False, fabrication_ready=False)
(out/'temperature_FMEA_R135.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k]for k in ['revision','maximum_absolute_TS_leakage_for_stated_0C_45C_scenarios_nA','max_nominal_self_heating_5V25_using_approx_0p7mW_per_C','ideal_charge_time_comparison','all_faults_fail_safe','fabrication_ready']},indent=2))
