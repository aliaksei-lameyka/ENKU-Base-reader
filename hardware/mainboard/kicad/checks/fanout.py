import json,sys,math
from pathlib import Path
root=Path(sys.argv[1]);c=root/'checks';g=json.loads((c/'geometry_current.json').read_text());routes=[]
def r(net,points,l=0,via=(),w=.2):routes.append({'net':net,'width':w,'via_diameter':.5,'segments':[{'a':a,'b':b,'layer':l} for a,b in zip(points,points[1:])],'vias':list(via)})
for pad in g['pads']:
 if pad['ref']=='J3' and pad['number'].isdigit() and not pad['net'].startswith('unconnected-'):
  x,y=pad['pos'];v=[x,31.6 if int(pad['number'])%2 else 33.85];r(pad['net'],[[x,y],v],via=[v])
for ref,pin,v in [('U1','5',[32.82,51.8]),('U1','7',[35.36,51.8])]:
 pad=next(p for p in g['pads'] if p['ref']==ref and p['number']==pin);r(pad['net'],[pad['pos'],v],via=[v])
for ref,pin,v in [('J3','S2',[62,35.25]),('C28','2',[73.9,27.55])]:
 pad=next(p for p in g['pads'] if p['ref']==ref and p['number']==pin);r(pad['net'],[pad['pos'],v],via=[v])
for net,x,res in [('USB_DM',42.98,'R65'),('USB_DP',44.25,'R64')]:
 a=next(p for p in g['pads'] if p['ref']=='U1' and p['net']==net);b=next(p for p in g['pads'] if p['ref']==res and p['number']=='2');r(net,[a['pos'],b['pos']])
for net,x in [('USB_DM_CONN',46.05),('USB_DP_CONN',47.95)]:r(net,[[x,107.35],[x,109.65]])
(c/'plan_fanout.json').write_text(json.dumps({'routes':routes},indent=2));print('fanout',len(routes))
