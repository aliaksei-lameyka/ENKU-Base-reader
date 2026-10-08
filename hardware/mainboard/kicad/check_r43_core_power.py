#!/usr/bin/env python3
"""R43 actual copper graph + MCU placement + feeder resistance calculation; not a bench signoff."""
import json,math,re
from check_r43_sd_connectivity import connected,geom,B,pads
for net,targets in [
 (2,[('U1','2'),('C13','1'),('C14','1'),('C11','1'),('R17','1'),('R18','1'),('R14','1'),('R16','1')]),
 (47,[('U1','3'),('R17','2'),('C15','1'),('J7','6')]),
 (67,[('U1','27'),('R18','2'),('J7','5')]),
 (int(re.search(r'\(net (\d+) "REG_FB"\)',B)[1]),[('U4','4'),('R14','2'),('R15','1')]),
 (int(re.search(r'\(net (\d+) "REG_PG"\)',B)[1]),[('U4','5'),('R16','2'),('TP8','1')]),
 (int(re.search(r'\(net (\d+) "REG_L1"\)',B)[1]),[('U4','9'),('L1','1')]),
 (int(re.search(r'\(net (\d+) "REG_L2"\)',B)[1]),[('U4','7'),('L1','2')])]:connected(net,targets)
for ref in ['C13','C14','C15','R17','R18']:
 for p in pads:
  if p[0]==ref:assert p[4][0]>26.25,(ref,'antenna keepout')
# Exact main feeder is a single-layer B.Cu 0.75mm route. Copper thickness is a conditional calculation, not factory approval.
length=sum(math.hypot(float(c)-float(a),float(d)-float(b)) for a,b,c,d in re.findall(r'^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width 0.75\) \(layer "B.Cu"\) \(net 2\)',B,re.M))
assert 40<length<100,length
r20=1.724e-8*(length/1000)/(.00075*.000025);r85=r20*(1+.00393*65)
print('R43 CORE POWER CONNECTIVITY PASS: MCU bulk/bypass/pull-ups, reset/service, BOOT/service, regulator FB/PG and both inductor nodes connected.')
print('R43 FEEDER CONDITIONAL CALCULATION:',json.dumps(dict(length_mm=length,width_mm=.75,assumed_min_copper_um=25,temperature_c=85,resistance_ohm=r85,drop_at_500ma_mv=r85*.5*1000)))
print('UNPROVEN: regulator transients/thermal, cap effective value, total feeder+via+package drop, exact PCBWay copper/stackup and MCU brownout margin.')
