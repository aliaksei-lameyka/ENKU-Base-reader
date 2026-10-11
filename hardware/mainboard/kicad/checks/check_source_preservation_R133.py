"""Preserve accepted R132 except exact declared local copper and additive B pour."""
import collections, gzip, hashlib, json, sys, xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split

r, out = map(lambda s: Path(s).resolve(), sys.argv[1:3])
c = r/'checks'; repo = r.parents[2]
m = json.loads((c/'preservation_manifest_R133.json').read_text())
for name,sha in m['unchanged_parent_repo_files'].items():
    assert hashlib.sha256((repo/name).read_bytes()).hexdigest()==sha, ('Undeclared source/evidence edit',name)
old = json.loads(gzip.decompress((c/'geometry_checkpoint_R132.json.gz').read_bytes()))
new = json.loads((out/'geometry.json').read_text())
assert old['pads']==new['pads'] and old['footprints']==new['footprints']
assert old['bbox']==new['bbox'] and old['board_outline']==new['board_outline']
assert json.loads((c/'assembly_features_R132.json').read_text())==json.loads((out/'assembly_features.json').read_text())
assert json.loads((c/'orientation_R132.json').read_text())==json.loads((out/'orientation.json').read_text())
assert_no_split(old,new)
before={x['uuid']:{k:v for k,v in x.items()if k!='code'}for x in old['tracks']}
after={x['uuid']:{k:v for k,v in x.items()if k!='code'}for x in new['tracks']}
removed={x['uuid']:x for x in m['removed_R132_copper']}
assert before.keys()-after.keys()==removed.keys()
for uid,t in before.items():
    if uid in removed: assert removed[uid]==t
    else: assert t==after[uid], ('Undeclared retained copper edit',uid)
old130=json.loads(gzip.decompress((c/'geometry_checkpoint_R130.json.gz').read_bytes()))
assert not removed.keys() & {x['uuid']for x in old130['tracks']}
added={x['uuid']:x for x in m['added_copper']}
assert after.keys()-before.keys()==added.keys()
for uid,t in added.items():
    assert t==after[uid]
    assert t['net'] in {'GND','CHG_STAT1','CHG_STAT2','CHG_ILIM_VSET','VBAT'}
    assert all(35.9<=x<=58.1 and 79.9<=y<=107.1 for x,y in [t['start'],t['end']])
assert collections.Counter(json.dumps(z,sort_keys=True)for z in new['zones'])==collections.Counter(json.dumps(z,sort_keys=True)for z in old['zones']+[m['added_zone']])
oldxml=ET.parse(c/'netlist_R132.xml');newxml=ET.parse(out/'netlist.xml')
for group in ['components','libparts','nets']:
    assert ET.tostring(oldxml.find(group))==ET.tostring(newxml.find(group)), ('Electrical netlist changed',group)
base=json.loads((c/'drc_checkpoint_R132.json').read_text());d=json.loads((out/'drc.json').read_text())
def findings(a):return collections.Counter((x['type'],x['severity'],x['description'],tuple(sorted(i['uuid']for i in x['items'])))for x in a['violations'])
assert findings(base)==findings(d) and not d['unconnected_items'] and not d['schematic_parity']
assert d['ignored_checks']==base['ignored_checks']
report=dict(revision='R133',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],
    unchanged_parent_repo_files=len(m['unchanged_parent_repo_files']),
    every_R132_pad_footprint_position_mask_paste_and_assembly_field_unchanged=True,
    exact_electrical_netlist_and_schematic_sources_unchanged=True,
    all_original_R130_copper_preserved_from_R132=True,
    preserved_R132_copper_items=len(before)-len(removed),declared_local_R132_copper_removals=len(removed),
    exact_added_copper_items=len(added),only_one_declared_B_ground_zone_added=True,
    original_rules_exclusions_thickness_RF_zones_and_outline_unchanged=True,
    exact_same20_hole_findings_and_no_new_DRC=True,fabrication_ready=False)
(out/'source_preservation_R133.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
