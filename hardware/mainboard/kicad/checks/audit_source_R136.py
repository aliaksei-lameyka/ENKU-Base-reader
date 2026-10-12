"""Verify the merge and finite C9 replacement against immutable R135 bytes."""
import copy, gzip, hashlib, json, sys
import xml.etree.ElementTree as ET
from pathlib import Path
from cad_text_R134 import children, instance, prop

r, out = (Path(s).resolve() for s in sys.argv[1:3])
c, repo = r / 'checks', r.parents[2]
m = json.loads((c / 'preservation_manifest_R136.json').read_text())
for name, expected in {**m['unchanged_R135_files'], **m['main_license_sha256']}.items():
    assert hashlib.sha256((repo / name).read_bytes()).hexdigest() == expected, name
assert json.loads((c / 'current_checkpoint.json').read_text()) == {
    'revision': 'R136', 'verification_file': 'verification_checkpoint_R136.json',
    'geometry_file': 'geometry_checkpoint_R136.json.gz', 'drc_file': 'drc_checkpoint_R136.json',
}
before_fields = {
    'Value': '10uF 10V', 'MPN': 'CC0805KKX5R6BB106',
    'Datasheet': 'https://yageogroup.com/download/specsheet/CC0805KKX5R6BB106',
    'Description': '10uF 10V',
}
after_fields = {
    'Value': '22uF 10V', 'MPN': 'CC0805MKX5R6BB226',
    'Datasheet': 'https://yageogroup.com/download/specsheet/CC0805MKX5R6BB226',
    'Description': 'R136 TPS63802 input 22uF; modeled DC-bias margin; max height1.45mm; Ceff/fit qualification pending',
}
for path, expected in m['checked_R136_source_sha256'].items():
    data = (repo / path).read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected, path
    text = data.decode()
    if path.endswith('.kicad_pcb'):
        candidates = [(a, z, p) for a, z, p in children(text)
                      if p.startswith('(footprint ') and '(property "Reference" "C9"' in p]
        assert len(candidates) == 1
        a, z, part = candidates[0]
    else:
        a, z, part = instance(text, 'C9')
    for name, value in after_fields.items():
        assert '(property ' + json.dumps(name) + ' ' + json.dumps(value) in part
        part = prop(part, name, before_fields[name])
    normalized = text[:a] + part + text[z:]
    assert hashlib.sha256(normalized.encode()).hexdigest() == m['normalized_R135_source_sha256'][path], path

old = json.loads(gzip.decompress((c / 'geometry_checkpoint_R135.json.gz').read_bytes()))
new = json.loads((out / 'geometry.json').read_text())
assert old == new, 'Any change to copper, pad, zone, hole, placement or outline is outside R136'
old_af = json.loads((c / 'assembly_features_R135.json').read_text())
new_af = json.loads((out / 'assembly_features.json').read_text())
old_f = {f['ref']: f for f in old_af['footprints']}
new_f = {f['ref']: f for f in new_af['footprints']}
assert old_f.keys() == new_f.keys()
for ref in old_f:
    actual = copy.deepcopy(new_f[ref])
    if ref == 'C9':
        assert actual['value'] == after_fields['Value']
        for name, value in after_fields.items():
            assert actual['fields'][name] == value
            actual['fields'][name] = before_fields[name]
        actual['value'] = before_fields['Value']
    assert actual == old_f[ref], ref
assert old_af['pads'] == new_af['pads'], 'Mask/paste/pad process changed'
def nodes(path):
    return {n.attrib['name']: sorted((p.attrib['ref'], p.attrib['pin']) for p in n.findall('node'))
            for n in ET.parse(path).findall('./nets/net')}
assert nodes(c / 'netlist_R135.xml') == nodes(out / 'netlist.xml')
assert (out / 'source_pcb.sha256').read_text().split()[0] == m['checked_R136_source_sha256']['hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb']
drc = json.loads((out / 'drc.json').read_text())
erc = json.loads((out / 'erc.json').read_text())
assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
assert not any(s['violations'] for s in erc['sheets'])
assert drc['ignored_checks'] == json.loads((c / 'drc_checkpoint_R135.json').read_text())['ignored_checks']
assert erc['ignored_checks'] == json.loads((c / 'erc_checkpoint_R135.json').read_text())['ignored_checks']
report = dict(revision='R136', pcb_sha256=(out / 'source_pcb.sha256').read_text().split()[0],
              unchanged_R135_files=len(m['unchanged_R135_files']), main_licenses_preserved=True,
              only_C9_four_properties_changed_in_PCB_and_power_sheet=True,
              all_127_positions_438_pads_3707_copper_items_and_native_nets_preserved=True,
              all_mask_paste_drills_RF_stack_USB_and_thermal_requests_preserved=True,
              rules_exclusions_and_severities_preserved=True,
              native_DRC_ERC_opens_parity_zero=True,
              mechanical_fit_and_fabrication_qualified=False, fabrication_ready=False)
(out / 'source_preservation_R136.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
