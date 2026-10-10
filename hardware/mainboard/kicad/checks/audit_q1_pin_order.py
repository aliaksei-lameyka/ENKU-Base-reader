"""Guard the corrected IRLML6346 top-view pin order independently of native DRC."""
import json,sys,hashlib
from pathlib import Path
from pad_groups import partitions
r=Path(sys.argv[1]).resolve();c=r/'checks';server=len(sys.argv)>2;out=Path(sys.argv[2]).resolve() if server else c
g=json.loads((out/'geometry.json' if server else c/'geometry_current.json').read_text());q={p['number']:p for p in g['pads'] if p['ref']=='Q1'};f=g['footprints']['Q1']
assert f['pos']==[67,48] and f['angle']==0 and f['lib']=='Package_TO_SOT_SMD:SOT-23'
expected={'1':('EPD_GDR',[66,47.05]),'2':('EPD_RESE',[66,48.95]),'3':('EPD_SW',[68,48])}
groups=partitions(g)
for n,(net,pos) in expected.items():assert q[n]['net']==net and q[n]['pos']==pos and q[n]['layers']==[0] and len(groups[net])==1,(n,q[n])
sha=(out/'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report={'revision':json.loads((c/'current_checkpoint.json').read_text())['revision'],'pcb_sha256':sha,'Q1_manufacturer_top_view_pin_order_verified':True,'Q1_all_pad_groups_connected':True,'pad_map':{n:{'net':v[0],'position_mm':v[1]} for n,v in expected.items()},'manufacturer_source':'https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlml6346-datasheet-en.pdf','source_pages':[1,8],'scope':'Gate/Source/Drain top-view location and native physical pad connectivity. Land dimensions, assembly process and circuit bench behavior still require qualification.','land_dimensions_qualified':False,'fabrication_ready':False}
(out/('q1_pin_order_audit_'+report['revision']+'.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
