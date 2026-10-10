"""Independently allow only the declared Hirose copper/stencil correction."""
import json,collections,math,sys,shutil,hashlib
from pathlib import Path
r=Path(sys.argv[1]).resolve();c=r/'checks';t=r/'trials/j3_land_pattern';a=json.loads((c/'geometry_current.json').read_text());b=json.loads((t/'geometry.json').read_text());j=json.loads((c/'j3_land_pattern_changes.json').read_text());d=json.loads((t/'drc_full.json').read_text());base=json.loads((c/'drc_reconnect.json').read_text())
ap={p['uuid']:p for p in a['pads']};bp={p['uuid']:p for p in b['pads']};assert ap.keys()<=bp.keys() and len(bp)-len(ap)==2
for u,p in ap.items():
 q=bp[u];assert all(p[k]==q[k] for k in ['ref','number','net','angle','drill','layers'])
 expected=[p['pos'][0]-.1,p['pos'][1]] if p['ref']=='J3' else p['pos'];assert math.dist(q['pos'],expected)<2e-6
 assert q['size']==([.8,.8] if p['ref']=='J3' and p['number'] in ['S1','S2'] else p['size'])
for u in bp.keys()-ap.keys():
 p=bp[u];assert p['ref']=='J3' and not p['number'] and not p['net'] and not p['layers'] and p['size']==[.8,.65] and p['drill']==[0,0]
at={p['uuid']:p for p in a['tracks']};bt={p['uuid']:p for p in b['tracks']};assert at.keys()==bt.keys();allowed={q['uuid']:q for q in j['copper_endpoint_changes']}
for u,p in at.items():
 q=bt[u];assert all(p[k]==q[k] for k in ['net','layer','width','via','drill'])
 for k,i in [('start',0),('end',1)]:assert math.dist(q[k],allowed[u]['after'][i] if u in allowed else p[k])<2e-6
sig=lambda q:(q['type'],q['description'],tuple(sorted(p['uuid'] for p in q['items'])))
assert collections.Counter(map(sig,d['violations']))==collections.Counter(map(sig,base['violations']))
assert not d['schematic_parity'] and len(d['unconnected_items'])==len(base['unconnected_items']) and d['kicad_version']=='10.0.7'
shutil.copy2(t/'enku-mainboard-r0.1.kicad_pcb',r/'enku-mainboard-r0.1.kicad_pcb');shutil.copy2(t/'geometry.json',c/'geometry_current.json');shutil.copy2(t/'drc_full.json',c/'drc_j3_land_pattern.json')
result={'revision':'R120','source':'Hirose EDC-159714-50-08 p1; supplied exact 24S drawing','native_kicad':'10.0.7','all_track_errors':True,'severity_all':True,'original_pads_preserved':400,'new_paste_only_pads':2,'reinforcement_copper_mm':[.8,.8],'signal_stencil_mm':[.25,.65],'reinforcement_stencil_mm':[.8,.65],'copper_nets_preserved':True,'only_declared_endpoint_changes':len(allowed),'opens':len(d['unconnected_items']),'parity':0,'drc_types':dict(collections.Counter(v['type'] for v in d['violations'])),'pcb_sha256':hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),'fabrication_ready':False}
(c/'accepted_j3_land_pattern.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
