"""Verify server native geometry/results against the committed local checkpoint."""
import collections,gzip,hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);c=root/'checks'
manifest=json.loads((c/'current_checkpoint.json').read_text()) if (c/'current_checkpoint.json').exists() else {'verification_file':'verification_checkpoint_R119.json','geometry_file':'geometry_checkpoint_R119.json.gz','drc_file':'drc_checkpoint_R119.json'}
expected=json.loads((c/manifest['verification_file']).read_text())
with gzip.open(c/manifest['geometry_file'],'rt') as f:old=json.load(f)
new=json.loads((out/'geometry.json').read_text());drc=json.loads((out/'drc.json').read_text());erc=json.loads((out/'erc.json').read_text());saved=json.loads((c/manifest['drc_file']).read_text())
assert (out/'source_pcb.sha256').read_text().split()[0]==expected['pcb_sha256'],'Wrong source PCB'
assert (out/'version.txt').read_text().strip()=='10.0.7','Wrong native KiCad version'
before={p['uuid']:p for p in old['pads']};after={p['uuid']:p for p in new['pads']};assert before.keys()==after.keys()
for u,p in before.items():
 for key in ('ref','number','net','pos','size','drill','angle','layers'):assert p[key]==after[u][key],(u,key)
before={t['uuid']:t for t in old['tracks']};after={t['uuid']:t for t in new['tracks']};assert before.keys()==after.keys()
for u,t in before.items():
 for key in ('net','start','end','width','layer','via','drill'):assert t[key]==after[u][key],(u,key)
assert old['footprints']==new['footprints']
types=dict(collections.Counter(x['type'] for x in drc['violations']));opens=len(drc['unconnected_items']);parity=len(drc['schematic_parity']);ec=sum(len(s['violations']) for s in erc['sheets'])
assert types==expected['drc_types'],(types,expected['drc_types'])
assert opens==expected['opens'] and parity==expected['parity'] and ec==expected['erc']
assert drc['ignored_checks']==saved['ignored_checks'],'Changed DRC exclusions'
report={'native_kicad':'10.0.7','committed_pcb_sha256':expected['pcb_sha256'],'server_matches_local_checkpoint':True,'pads':len(new['pads']),'footprints':len(new['footprints']),'opens':opens,'drc_types':types,'ERC':ec,'schematic_parity':parity,'fabrication_ready':not (opens or drc['violations'] or parity or ec)}
(out/'server_comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
print('PASS: server matches committed local geometry and native results. Fabrication readiness is evaluated separately.')
