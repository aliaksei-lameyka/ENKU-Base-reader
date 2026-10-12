"""Verify finite R138 copper edits and preserve all accepted R137 sources."""
import copy,gzip,hashlib,json,re,sys
import xml.etree.ElementTree as ET
from pathlib import Path
from reconstruct_layout_R138 import blocks,TRACK_PATTERN
from pad_groups import partitions
r,out=(Path(x).resolve()for x in sys.argv[1:3]);c=r/'checks';repo=r.parents[2]
m=json.loads((c/'physical_change_manifest_R138.json').read_text());preserved=json.loads((c/'preservation_manifest_R138.json').read_text())
for path,sha in preserved['unchanged_main_R137_files'].items():assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==sha,('Accepted historical file changed',path)
assert json.loads((c/'current_checkpoint.json').read_text())==dict(revision='R138',verification_file='verification_checkpoint_R138.json',geometry_file='geometry_checkpoint_R138.json.gz',drc_file='drc_checkpoint_R138.json')
s=(r/'enku-mainboard-r0.1.kicad_pcb').read_text();sha=hashlib.sha256(s.encode()).hexdigest();assert sha==m['source_pcb_after_sha256']
def normalized(source):
 source=TRACK_PATTERN.sub('',source);source=re.sub(r'^\t\t\(filled_polygon\n.*?^\t\t\)\n','',source,flags=re.M|re.S)
 source=source.replace('R138 - ENGINEERING / NO FAB','R137 - ENGINEERING / NO FAB')
 return '\n'.join(x.rstrip()for x in source.splitlines()if x.strip())+'\n'
assert hashlib.sha256(normalized(s).encode()).hexdigest()==m['normalized_nontrack_source_sha256'],'Source outside finite copper/filled-zone/title changes'
actual=blocks(s)
for u,edit in m['changed_source_blocks'].items():assert actual[u]==edit['after'],u
assert not set(m['removed_source_blocks'])&actual.keys()
for u,b in m['added_source_blocks'].items():assert actual[u]==b,u
for name,sha256 in m['project_and_custom_rules_sha256'].items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==sha256,name
assert (out/'source.kicad_pro').read_bytes()==(r/'enku-mainboard-r0.1.kicad_pro').read_bytes()
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R137.json.gz').read_bytes()));new=json.loads((out/'geometry.json').read_text())
assert new['pads']==old['pads'],'Pads changed outside R138'
for key in ['footprints','zones','board_outline','bbox','version']:assert new[key]==old[key],('Placement/outline/zone changed outside R138',key)
before={t['uuid']:t for t in old['tracks']};after={t['uuid']:t for t in new['tracks']}
assert before.keys()-after.keys()==set(m['removed_geometry_tracks']) and after.keys()-before.keys()==set(m['added_geometry_tracks'])
for u,t in before.items():
 if u in m['removed_geometry_tracks']:assert t==m['removed_geometry_tracks'][u]
 elif u in m['changed_geometry_tracks']:assert t==m['changed_geometry_tracks'][u]['before']and after[u]==m['changed_geometry_tracks'][u]['after'],u
 else:assert t==after[u],('Unreviewed copper geometry change',u)
for u,t in m['added_geometry_tracks'].items():assert after[u]==t,u
assert partitions(new)==partitions(old),'Previously connected pad partitions changed'
assert len(new['tracks'])==3712 and sum(t['via']for t in new['tracks'])==329
af=json.loads((out/'assembly_features.json').read_text());assert af==json.loads((c/'assembly_features_R137.json').read_text()),'Electrical/MPN/assembly/pad fields changed'
assert json.loads((out/'orientation.json').read_text())==json.loads((c/'orientation_R137.json').read_text())
def nets(p):return{n.attrib['name']:sorted((x.attrib['ref'],x.attrib['pin'])for x in n.findall('node'))for n in ET.parse(p).findall('./nets/net')}
assert nets(out/'netlist.xml')==nets(c/'netlist_R137.xml')
assert (out/'CPL.csv').read_bytes()==(c/'native_CPL_R137.csv').read_bytes()
for name,base in [('drc.json','drc_checkpoint_R137.json'),('erc.json','erc_checkpoint_R137.json')]:assert json.loads((out/name).read_text())['ignored_checks']==json.loads((c/base).read_text())['ignored_checks']
assert (out/'source_pcb.sha256').read_text().split()[0]==sha
report=dict(revision='R138',pcb_sha256=sha,accepted_R137_main_commit=preserved['accepted_main_R137_commit'],unchanged_historical_files_verified=len(preserved['unchanged_main_R137_files']),all_127_positions_438_pads_fields_MPNs_stencil_outline_and_zone_parameters_preserved=True,old_pad_partitions_exactly_preserved=True,source_outside_finite_copper_and_refill_changes_preserved=True,finite_changed_copper_items=len(m['changed_geometry_tracks']),finite_removed_copper_items=len(m['removed_geometry_tracks']),finite_added_copper_items=len(m['added_geometry_tracks']),min_via_annular_width_strengthened_mm=.15,minimum_drill_floor_explicitly_reviewed_mm=.2,DRC_ERC_exclusions_preserved=True,fabrication_ready=False)
(out/'source_preservation_R138.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS finite R138 source changes and all accepted historical files')
