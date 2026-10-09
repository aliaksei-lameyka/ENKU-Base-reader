#!/usr/bin/env python3
"""Active-board VBUS pin map + conservative DC/RC calculation. Not a bench test."""
from pathlib import Path
import re,math,itertools,json
import check_r45_assembly as geom
B=geom.PCB;fps=geom.footprints()
def pin(ref,n):
 t=fps[ref]['txt'];m=re.search(r'\(pad "'+str(n)+r'"[^\n]*\(net \d+ "([^"]+)"\)',t)
 assert m,(ref,n);return m[1]
expected={('U1',10):'USB_VBUS_VALID',('U10',1):'USB_VBUS_VALID',('U10',2):'GND',('U10',3):'USB_VBUS_DIV',('U10',4):'USB_VBUS_REF',('U10',5):'USB_VBUS_REF',('U10',6):'3V3_SYS',('R70',1):'VBUS_USB',('R70',2):'USB_VBUS_DIV',('R71',1):'USB_VBUS_DIV',('R71',2):'GND',('R72',1):'USB_VBUS_VALID',('R72',2):'GND',('R73',1):'VBUS_USB',('R73',2):'GND',('C38',1):'3V3_SYS',('C38',2):'GND',('C39',1):'USB_VBUS_DIV',('C39',2):'GND'}
for (ref,n),net in expected.items():assert pin(ref,n)==net,(ref,n,pin(ref,n),net)
assert 'TLV3012BIDBVR' in fps['U10']['txt'], 'Non-B comparator is NOT fail-safe'
assert '26.7k 0.1% 25ppm' in fps['R70']['txt']
assert '10k 0.1% 25ppm' in fps['R71']['txt']
assert '1uF 10V' in fps['C2']['txt'], '10uF raw VBUS hold-up invalidates disconnect budget'
assert '3.3k 1%' in fps['R73']['txt']
assert len(re.findall(r'^  \(zone ',B,re.M))==2
# TI SBOS300C 6.9: reference range, 100 ppm/K drift, 9mV offset, 8mV hysteresis.
# Reference range is at 25C; temperature envelope -40..85C used here; all variations adversarial.
tempdelta=65; rt=.001+25e-6*tempdelta
qmin=1+26700*(1-rt)/(10000*(1+rt));qmax=1+26700*(1+rt)/(10000*(1-rt))
threshold_min=(1.223-1.242*100e-6*tempdelta-.009-.008)*qmin
threshold_max=(1.260+1.242*100e-6*tempdelta+.009+.008)*qmax
assert 4.35<threshold_min<threshold_max<4.75,(threshold_min,threshold_max)
# Input remains far below 5.5V fail-safe limit at USB 5.5V; no input clamp to switched V+.
vinmax=5.5/qmin
assert vinmax<5.5
# Bound TOTAL local raw-VBUS capacitance <=1.5uF including C2 tolerance and ESD/parasitics.
# No cable-side reservoir or external source may hold VBUS up; TPS2121 reverse block must be bench-tested.
rdis=1/(1/(3300*1.01)+1/((26700+10000)*(1+rt)))
tdis=1.5e-6*rdis*math.log(5.5/threshold_min)+4e-6+5*(26700*10000/(26700+10000))*1e-9
assert tdis<.003,tdis
# Existing mux divider also consumes USB current: the total is a separate measurement gate.
result=dict(temperature_c=[-40,85],threshold_min_v=threshold_min,threshold_max_v=threshold_max,sense_max_v=vinmax,local_disconnect_bound_ms=tdis*1000,bleeder_max_ma=5.5/(3300*.99)*1000,raw_vbus_capacitance_bound_uf=1.5)
print('R45 VBUS DESIGN CALCULATION:',json.dumps(result,sort_keys=True))
print('PASS: fail-safe B-version, common switched 3V3 rail with MCU, output pulldown, DC corner bounds and conditional RC budget.')
print('UNPROVEN: soldered prototype OFF/backfeed, dock+USB removal, actual C2 capacitance, hotplug ringing and complete USB suspend current/charger policy.')
