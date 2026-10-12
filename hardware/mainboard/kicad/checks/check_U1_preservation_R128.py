"""Strict independent source/copper/assembly preservation against accepted R127."""
import gzip, hashlib, json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
from pad_groups import assert_no_split

r = Path(sys.argv[1]).resolve(); c = r / 'checks'
server = len(sys.argv) > 2; out = Path(sys.argv[2]).resolve() if server else c
old = json.loads(gzip.decompress((c / 'geometry_checkpoint_R127.json.gz').read_bytes()))
new = json.loads((out / 'geometry.json' if server else c / 'geometry_current.json').read_text())
oa = json.loads((c / 'assembly_features_R127.json').read_text())
na = json.loads((out / 'assembly_features.json' if server else c / 'assembly_features_R128.json').read_text())
plan = json.loads((c / 'applied_U1_EP_grid_R128.json').read_text())
op = {x['uuid']: x for x in old['pads']}; np = {x['uuid']: x for x in new['pads']}
oap = {x['uuid']: x for x in oa['pads']}; nap = {x['uuid']: x for x in na['pads']}
changed = {x['uuid']: x for x in plan['changed_original_pads']}
added = {x['uuid']: x for x in plan['added_EP_pads']}
assert len(op) == 417 and len(np) == 425 and len(changed) == 22 and len(added) == 8
assert np.keys() == op.keys() | added.keys() and not op.keys() & added.keys()

def state(q, a):
    return {'uuid': q['uuid'], 'number': q['number'], 'net': q['net'],
            'position_mm': q['pos'], 'size_mm': q['size'], 'drill_mm': q['drill'],
            'angle_deg': q['angle'], 'shape': q['shape'], 'attribute': q['attribute'],
            'layers': a['layers'], 'mask_margin_IU': a['local_mask_margin_IU'],
            'paste_margin_IU': a['local_paste_margin_IU'], 'paste_ratio': a['local_paste_ratio']}

for u, x in op.items():
    y = np[u]
    for key in ['ref', 'number', 'net', 'drill', 'attribute', 'drill_shape']:
        assert x[key] == y[key], (u, key, 'Original pad identity/net/drill changed')
    if u in changed:
        assert x['ref'] == 'U1'
        assert state(x, oap[u]) == changed[u]['before'], (u, 'Wrong accepted baseline')
        assert state(y, nap[u]) == changed[u]['after'], (u, 'Undeclared pad delta')
        if x['number'] == '41' and x['attribute'] == 0:
            for key in ['pos', 'size', 'shape', 'angle', 'layers', 'polygons']:
                assert x[key] == y[key], (u, key, 'Thermal drill/copper moved')
    else:
        for key in ['pos', 'size', 'shape', 'angle', 'layers', 'polygons']:
            assert x[key] == y[key], (u, key, 'Unrelated pad copper changed')
        assert oap[u] == nap[u], (u, 'Unrelated mask/paste/assembly changed')
for u, expected in added.items():
    assert np[u]['ref'] == 'U1' and np[u]['number'] == '41' and np[u]['net'] == 'GND'
    assert state(np[u], nap[u]) == expected, (u, 'Undeclared added pad')

ot = {x['uuid']: x for x in old['tracks']}; nt = {x['uuid']: x for x in new['tracks']}
assert len(ot) == 2639 and ot.keys() == nt.keys()
for u, x in ot.items():
    for key in ['net', 'start', 'end', 'width', 'layer', 'via', 'drill']:
        assert x[key] == nt[u][key], (u, key, 'Routing changed')
assert old['footprints'].keys() == new['footprints'].keys()
for ref, x in old['footprints'].items():
    expected = dict(x)
    if ref == 'U1': expected['lib'] = plan['U1_footprint_library']
    assert new['footprints'][ref] == expected, (ref, 'Footprint placement changed')
assert old['bbox'] == new['bbox'] and old['board_outline'] == new['board_outline']
assert sorted(json.dumps(x, sort_keys=True) for x in old['zones']) == sorted(json.dumps(x, sort_keys=True) for x in new['zones'])
assert_no_split(old, new)
for file, sha in plan['unchanged_files'].items():
    assert hashlib.sha256((r / file).read_bytes()).hexdigest() == sha, ('Unrelated source change', file)

def block(t, start):
    depth, quote, escaped = 0, False, False
    for i in range(start, len(t)):
        ch = t[i]
        if quote:
            if escaped: escaped = False
            elif ch == '\\': escaped = True
            elif ch == '"': quote = False
        elif ch == '"': quote = True
        elif ch == '(': depth += 1
        elif ch == ')':
            depth -= 1
            if not depth: return t[start:i + 1], i + 1
    raise ValueError('Unbalanced source')
def prop(t, key, value):
    t, n = re.subn(r'(\(property "' + re.escape(key) + r'" )"(?:\\.|[^"\\])*"', lambda m: m[1] + json.dumps(value), t, count=1)
    if not n: t = t[:-1] + '\n\t\t(property ' + json.dumps(key) + ' ' + json.dumps(value) + ' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
    return t
expected = gzip.decompress((c / 'source_R127_mcu_io.kicad_sch.gz').read_bytes()).decode()
pos = expected.index('(property "Reference" "U1"'); start = expected.rfind('(symbol (lib_id', 0, pos)
symbol, end = block(expected, start)
for key, value in plan['schematic_U1_fields'].items(): symbol = prop(symbol, key, value)
expected = expected[:start] + symbol + expected[end:]
tokens = lambda t: re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', t)
assert tokens((r / 'mcu_io.kicad_sch').read_text()) == tokens(expected), 'Undeclared schematic edit'
def nets(path):
    return {n.attrib['name']: {(x.attrib['ref'], x.attrib['pin']) for x in n.findall('node')} for n in ET.parse(path).findall('./nets/net')}
assert nets(c / 'netlist_R127_baseline.xml') == nets(out / 'netlist.xml' if server else c / 'netlist_R128.xml'), 'Native schematic net nodes changed'
d = json.loads((out / 'drc.json' if server else c / 'drc_checkpoint_R128.json').read_text())
e = json.loads((out / 'erc.json' if server else c / 'erc_checkpoint_R128.json').read_text())
assert not d['unconnected_items'] and not d['schematic_parity'] and not any(s['violations'] for s in e['sheets'])
assert d['ignored_checks'] == json.loads((c / 'drc_checkpoint_R127.json').read_text())['ignored_checks']
assert e['ignored_checks'] == json.loads((c / 'erc_checkpoint_R127.json').read_text())['ignored_checks']
sha = (out / 'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r / 'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report = {
    'revision': 'R128', 'pcb_sha256': sha,
    'original_pad_UUIDs_preserved': 417, 'original_pad_numbers_nets_and_drills_preserved': True,
    'declared_U1_existing_pad_changes': 22, 'declared_U1_EP_lands_added': 8,
    'all_other_pad_copper_mask_paste_and_attributes_preserved': True,
    'original_copper_items_preserved': len(ot), 'all_copper_geometry_and_net_names_preserved': True,
    'all_footprint_placements_preserved': True, 'all_previous_pad_groups_preserved': True,
    'all_native_schematic_net_nodes_preserved': True, 'only_declared_U1_metadata_edits': True,
    'all_previous_footprint_library_files_preserved': True,
    'project_rules_exclusions_outline_zones_and_RF_keepouts_preserved': True,
    'USB_and_button_holes_and_lands_preserved': True, 'fabrication_ready': False,
}
(out / 'source_preservation_audit_R128.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
