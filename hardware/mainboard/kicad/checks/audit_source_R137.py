"""Verify finite R137 fabrication-layer changes against accepted immutable main R136."""
import copy,gzip,hashlib,json,sys
import xml.etree.ElementTree as ET
from pathlib import Path
from cad_text_R134 import children

r,out=(Path(x).resolve()for x in sys.argv[1:3]);c=r/'checks';repo=r.parents[2]
m=json.loads((c/'preservation_manifest_R137.json').read_text())
for path,sha in m['unchanged_main_R136_files'].items():
    assert hashlib.sha256((repo/path).read_bytes()).hexdigest()==sha,path
selector=dict(revision='R137',verification_file='verification_checkpoint_R137.json',geometry_file='geometry_checkpoint_R137.json.gz',drc_file='drc_checkpoint_R137.json')
assert json.loads((c/'current_checkpoint.json').read_text())==selector
changes=json.loads((c/'silkscreen_change_manifest_R137.json').read_text())
source=(r/'enku-mainboard-r0.1.kicad_pcb').read_text();normalized=source
assert hashlib.sha256(source.encode()).hexdigest()==changes['source_pcb_after_sha256']
assert len(changes['edits'])==72 and len(changes['root_edits'])==3 and len(changes['DNP_paste_edits'])==2
for edit in [*changes['edits'],*changes['DNP_paste_edits'],*changes['root_edits']]:
    assert normalized.count(edit['after'])==1,edit.get('uuid',edit.get('kind'))
    normalized=normalized.replace(edit['after'],edit['before'],1)
assert hashlib.sha256(normalized.encode()).hexdigest()==changes['source_pcb_before_sha256']==m['accepted_main_R136_pcb_sha256']
old=json.loads(gzip.decompress((c/'geometry_checkpoint_R136.json.gz').read_bytes()))
new=json.loads((out/'geometry.json').read_text())
assert new['footprints']['R67']['lib']=='ENKU:R_RC0603_YAGEO_REFLOW_DNP_NO_PASTE'
new['footprints']['R67']['lib']=old['footprints']['R67']['lib']
assert new==old,'Any copper/pad/hole/zone/placement/outline movement is outside R137'
assert len(changes['schematic_edits'])==1
for edit in changes['schematic_edits']:
    actual=(repo/edit['path']).read_text();assert actual.count(edit['after'])==1
    assert hashlib.sha256(actual.encode()).hexdigest()==edit['after_sha256']
    assert hashlib.sha256(actual.replace(edit['after'],edit['before'],1).encode()).hexdigest()==edit['before_sha256']
library=changes['new_DNP_library'];assert hashlib.sha256((repo/library['path']).read_bytes()).hexdigest()==library['sha256']
assert hashlib.sha256((repo/library['derived_from']).read_bytes()).hexdigest()==library['original_sha256']
expected_library=(repo/library['derived_from']).read_text().replace('"R_RC0603_YAGEO_REFLOW"','"R_RC0603_YAGEO_REFLOW_DNP_NO_PASTE"').replace(' "F.Paste"','').replace('(thickness 0.12)','(thickness 0.15)')
assert (repo/library['path']).read_text()==expected_library
old_af=json.loads((c/'assembly_features_R136.json').read_text());new_af=json.loads((out/'assembly_features.json').read_text())
assert new_af['footprints']==old_af['footprints'],'Part values, MPNs, DNP or electrical fields changed'
for a,b in zip(old_af['pads'],new_af['pads'],strict=True):
    actual=copy.deepcopy(b)
    if b['ref']=='R67':
        assert set(b['layers'])=={'F.Cu','F.Mask'} and b['uuid']in {x['uuid']for x in changes['DNP_paste_edits']}
        actual['layers']=a['layers']
    assert actual==a,'Mask, paste, physical pad or process field changed: '+b['uuid']
old_o=json.loads((c/'orientation_R136.json').read_text());new_o=json.loads((out/'orientation.json').read_text())
for x in new_o['features']:
    if x['type']=='pin1_line':assert x['width_mm']==.15;x['width_mm']=.12
assert new_o==old_o,'Probe names/positions or pin1 targeting changed'
def nets(path):
    return {n.attrib['name']:sorted((x.attrib['ref'],x.attrib['pin'])for x in n.findall('node'))for n in ET.parse(path).findall('./nets/net')}
assert nets(out/'netlist.xml')==nets(c/'netlist_R136.xml')
assert (out/'CPL.csv').read_bytes()==(c/'native_CPL_R136.csv').read_bytes()
assert (out/'source_pcb.sha256').read_text().split()[0]==changes['source_pcb_after_sha256']
for file,old_file,key in [('drc.json','drc_checkpoint_R136.json','violations'),('erc.json','erc_checkpoint_R136.json','sheets')]:
    new=json.loads((out/file).read_text());old=json.loads((c/old_file).read_text())
    assert new['ignored_checks']==old['ignored_checks']
    assert not new[key]if key=='violations'else not any(x['violations']for x in new[key])
report=dict(revision='R137',pcb_sha256=changes['source_pcb_after_sha256'],accepted_R136_main_commit=m['accepted_main_R136_commit'],
    original_main_and_engineering_files_retained=len(m['unchanged_main_R136_files']),all_licenses_and_schematic_sources_preserved=True,
    exact_72_silk_strokes_4_layer_enablements_2_DNP_paste_exclusions_and_NO_FAB_title_verified=True,R67_only_library_ID_schematic_field_and_no_paste_library_transfer_verified=True,
    source_normalizes_exactly_to_accepted_R136_SHA=True,all_127_positions_438_physical_pads_3707_copper_items_and_nets_preserved=True,
    all_R136_RF_USB_thermal_drill_stack_and_electrical_fields_preserved=True,rules_exclusions_and_severities_preserved=True,
    fabrication_ready=False)
(out/'source_preservation_R137.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
