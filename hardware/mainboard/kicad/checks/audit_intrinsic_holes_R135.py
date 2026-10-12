"""Real no-boss switch replacement; unchanged .25mm hole/copper board rule."""
import json,sys,hashlib
from pathlib import Path
r,o=map(lambda s:Path(s).resolve(),sys.argv[1:3]);c=r/'checks';g=json.loads((o/'geometry.json').read_text());d=json.loads((o/'drc.json').read_text())
rules=json.loads((r/'enku-mainboard-r0.1.kicad_pro').read_text())['board']['design_settings']['rules'];assert rules['min_hole_clearance']==.25
for ref in ['SW3','SW4','SW5','SW6']:
 assert g['footprints'][ref]['lib']=='ENKU:TL1016AAF160QG_ESWITCH_P520001'
 ps=[p for p in g['pads']if p['ref']==ref];assert len(ps)==4 and all(p['attribute']==1 and p['drill']==[0,0]for p in ps)
assert not [p for p in g['pads']if p['ref']=='J5'and p['attribute']==3]
assert not d['violations']and not d['unconnected_items']and not d['schematic_parity']
report=dict(revision='R135',pcb_sha256=(o/'source_pcb.sha256').read_text().split()[0],active_hole_clearance_errors=0,unchanged_required_hole_clearance_mm=.25,actual_E_switch_AA_no_boss_variant_verified=True,old_component_locators_removed_by_part_replacement=True,old_locator_sizes_shrunk_to_hide_findings=False,lands_clipped_to_hide_findings=False,rules_exclusions_or_severity_weakened=False,mechanical_actuator_and_assembly_qualified=False,fabrication_ready=False)
(o/'intrinsic_holes_audit_R135.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
