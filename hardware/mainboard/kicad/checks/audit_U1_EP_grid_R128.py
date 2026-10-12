"""Independent native U1 EP copper/mask/paste, reserved-pin and exact-MPN audit.

Drawing constants are independently transcribed from Espressif v1.8 p45
Figure11-1 and p3/p12. This guard does not read the mutation recipe.
"""
import hashlib, json, math, sys, xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import box, Point
from pad_groups import partitions

r = Path(sys.argv[1]).resolve(); c = r / 'checks'
server = len(sys.argv) > 2; out = Path(sys.argv[2]).resolve() if server else c
g = json.loads((out / 'geometry.json' if server else c / 'geometry_current.json').read_text())
af = json.loads((out / 'assembly_features.json' if server else c / 'assembly_features_R128.json').read_text())
ap = {x['uuid']: x for x in af['pads']}
fp = next(x for x in af['footprints'] if x['ref'] == 'U1')
f = g['footprints']['U1']
assert f['pos'] == [33, 45] and f['angle'] == 90
assert f['lib'] == 'ENKU:ESP32_S3_WROOM_1_N16R8_EP_GRID_03_TENT_REQUEST'
assert fp['value'] == fp['fields']['MPN'] == 'ESP32-S3-WROOM-1-N16R8'
assert fp['fields']['Manufacturer'] == 'Espressif'
assert '-40..65C' in fp['fields']['Module Ambient'] and 'ECC' in fp['fields']['Module Ambient']

u = [x for x in g['pads'] if x['ref'] == 'U1']
ep = [x for x in u if x['number'] == '41' and x['attribute'] == 1]
vias = [x for x in u if x['number'] == '41' and x['attribute'] == 0]
paste = [x for x in af['pads'] if x['ref'] == 'U1' and not x['number'] and 'F.Paste' in x['layers']]
grid = {(x, y) for x in [34.06, 35.46, 36.86] for y in [45.1, 46.5, 47.9]}
via_grid = {(x, y) for x in [34.76, 36.16] for y in [45.1, 46.5, 47.9]} | {(x, y) for x in [34.06, 35.46, 36.86] for y in [45.8, 47.2]}
assert len(ep) == 9 and {tuple(x['pos']) for x in ep} == grid
assert all(x['net'] == 'GND' and x['size'] == [.9, .9] and x['shape'] == 1 and x['drill'] == [0, 0] and x['layers'] == [0] for x in ep)
for x in ep:
    a = ap[x['uuid']]
    assert set(a['layers']) == {'F.Cu', 'F.Mask'}
    assert a['local_mask_margin_IU'] == -50000
    assert not a['local_paste_margin_IU'] and not a['local_paste_ratio']
    # Every copper vertex must belong to its own independently specified square.
    expected = box(x['pos'][0] - .45, x['pos'][1] - .45, x['pos'][0] + .45, x['pos'][1] + .45)
    from shapely.geometry import Polygon
    assert all(Polygon(poly).symmetric_difference(expected).area < 1e-10 for poly in x['polygons']['0'])
assert len(vias) == 12 and {tuple(x['pos']) for x in vias} == via_grid
for x in vias:
    assert x['net'] == 'GND' and x['drill'] == [.3, .3] and x['size'] == [.6, .6] and x['shape'] == 0
    assert all(layer.endswith('.Cu') for layer in ap[x['uuid']]['layers'])
    assert {'F.Cu', 'In1.Cu', 'In2.Cu', 'B.Cu'} <= set(ap[x['uuid']]['layers'])
assert len(paste) == 9 and {tuple(x['position_mm']) for x in paste} == grid
assert all(x['size_mm'] == [.8, .8] and x['layers'] == ['F.Paste'] and not x['local_paste_margin_IU'] and not x['local_paste_ratio'] for x in paste)

hole_clearance = min(box(x - .4, y - .4, x + .4, y + .4).distance(Point(*h)) - .15 for x, y in grid for h in via_grid)
mask_web = min(box(x - .4, y - .4, x + .4, y + .4).distance(box(xx - .4, yy - .4, xx + .4, yy + .4)) for x, y in grid for xx, yy in grid if (x, y) != (xx, yy))
assert abs(hole_clearance - .15) < 1e-8 and abs(mask_web - .6) < 1e-8
assert len(partitions(g)['GND']) == 1

# Native schematic metadata and reserved Octal-PSRAM pads are checked directly.
xml = ET.parse(out / 'netlist.xml' if server else c / 'netlist_R128.xml')
comp = next(x for x in xml.findall('./components/comp') if x.attrib['ref'] == 'U1')
sf = {x.attrib['name']: x.text or '' for x in comp.findall('./fields/field')}
assert sf['MPN'] == fp['fields']['MPN'] and sf['Manufacturer'] == 'Espressif'
assert comp.findtext('footprint') == f['lib']
reserved = {}
for number, gpio in [('28', '35'), ('29', '36'), ('30', '37')]:
    matches = [x for x in u if x['number'] == number]
    assert len(matches) == 1
    q = matches[0]
    assert q['net'].startswith('unconnected-(U1-')
    assert not any(t['net'] == q['net'] for t in g['tracks'])
    node_sets = [n.findall('node') for n in xml.findall('./nets/net') if n.attrib['name'] == q['net']]
    assert len(node_sets) == 1 and len(node_sets[0]) == 1
    assert node_sets[0][0].attrib['ref'] == 'U1' and node_sets[0][0].attrib['pin'] == number
    reserved['GPIO' + gpio] = {'module_pad': number, 'native_net': q['net'], 'external_copper_absent': True}

sha = (out / 'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r / 'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report = {
    'revision': 'R128', 'pcb_sha256': sha,
    'manufacturer_nominal_U1_EP_square_grid_matches': True,
    'EP_land_count': 9, 'EP_land_size_mm': [.9, .9], 'EP_grid_pitch_mm': 1.4,
    'EP_grid_outer_span_mm': [3.7, 3.7], 'EP_land_area_mm2': 7.29,
    'actual_EP_mask_window_size_mm': [.8, .8], 'actual_mask_web_mm': round(mask_web, 6),
    'actual_paste_aperture_count': 9, 'actual_paste_aperture_size_mm': [.8, .8],
    'actual_paste_area_mm2': 5.76, 'paste_area_fraction_of_nominal_EP_lands': 64 / 81,
    'nominal_mask_and_paste_edge_to_thermal_drill_mm': round(hole_clearance, 6),
    'thermal_via_count': 12, 'thermal_drill_mm': .3, 'thermal_annulus_land_mm': .6,
    'thermal_vias_have_no_top_or_bottom_mask_opening': True,
    'all_U1_EP_lands_connected_to_native_GND': True,
    'exact_N16R8_MPN_and_native_metadata_match': True,
    'Octal_PSRAM_reserved_GPIO35_36_37_unused': reserved,
    'default_module_ambient_rating_C': [-40, 65],
    '85C_requires_ECC_and_usable_PSRAM_reduction': True,
    '85C_firmware_and_whole_board_qualified': False,
    'mask_registration_drill_tolerance_and_tenting_qualified': False,
    'thermal_vias_filled_plugged_or_capped': False,
    'stencil_thickness_paste_transfer_voiding_and_reflow_qualified': False,
    'assembly_process_qualified': False, 'fabrication_ready': False,
    'manufacturer_source': 'https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf',
    'source_version': '1.8', 'source_pages': [3, 12, 45],
    'scope': 'Nominal copper grid and exact native mask/paste requests, connectivity and reserved pins.0.3mm old holes/0.6mm annuli,0.8mm mask/paste and both-side tenting are project process adaptations. Absence of mask openings does not prove a sealed tent; factory drill/mask registration, stencil/process, voiding and thermal/RF behavior remain unqualified.',
}
(out / 'U1_EP_grid_audit_R128.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
