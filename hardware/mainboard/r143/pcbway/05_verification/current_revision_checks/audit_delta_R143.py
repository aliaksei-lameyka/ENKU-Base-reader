"""Exact native R142 -> R143 physical delta; old evidence is an immutable control."""
from pathlib import Path
import copy,hashlib,json,sys,xml.etree.ElementTree as E
r,old,o=map(lambda v:Path(v).resolve(),sys.argv[1:4])
a=json.loads((o/'geometry.json').read_text());b=json.loads((old/'geometry.json').read_text())
ids={'1ba16f3f-5769-4d6b-a83f-1a7d9af335a8','89347092-7d63-48da-89ca-6abb4b87c9e4','8e0a10b7-edca-4212-ae0b-0bbf808acf25','461fb056-82c8-4f42-a8f7-ef7d7967dddf'}
assert a.keys()==b.keys()
for key in a:
 if key!='pads':assert a[key]==b[key],('Unapproved physical delta',key)
oldpads={p['uuid']:p for p in b['pads']};changed=[]
for p in a['pads']:
 q=oldpads[p['uuid']]
 if p['uuid'] in ids:
  assert p['ref']=='J3' and p['size']==[.4,.8]
  assert q['size']==([.8,.8]if p['number']else[.8,.65])
  assert {k:v for k,v in p.items()if k not in ['size','polygons']}=={k:v for k,v in q.items()if k not in ['size','polygons']}
  if p['number']:
   x,y=p['pos'];assert p['polygons']=={'0':[[[round(v,6) for v in xy]for xy in [[x-.2,y-.4],[x+.2,y-.4],[x+.2,y+.4],[x-.2,y+.4]]]]}
  else:assert not p['polygons']
  changed.append(p['uuid'])
 else:assert p==q,('Unapproved pad change',p['ref'],p['number'])
assert set(changed)==ids
nets=lambda f:{n.get('name'):sorted((x.get('ref'),x.get('pin'))for x in n.findall('node'))for n in E.parse(f).findall('./nets/net')}
assert nets(o/'netlist.xml')==nets(old/'netlist.xml')
reference_kicad=r.parents[1]/'r142/kicad'
if not reference_kicad.exists():reference_kicad=old.parents[1]/'kicad'
for file in ['enku-mainboard-r0.1.kicad_pro','enku-mainboard-r0.1.kicad_dru','fp-lib-table','sym-lib-table']:
 assert (r/file).read_bytes()==(reference_kicad/file).read_bytes()
report=dict(revision='R143',pcb_sha256=hashlib.sha256((r/'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest(),R142_pcb_sha256='1ce355545d21d849e924f537488b5c9b9d59e9a8fa3cbbd129839823a7493ebf',changed_pad_UUIDs=sorted(changed),every_other_pad_track_via_placement_outline_rule_area_preserved=True,electrical_topology_identical_to_R142=True,project_rules_tables_unchanged=True,historical_evidence_not_regenerated=True,fabrication_ready=False)
(o/'exact_delta_R143.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS exact R142 -> R143 four-pad-only physical delta and identical netlist')
