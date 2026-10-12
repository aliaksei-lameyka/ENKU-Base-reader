"""Independent nominal manufacturer-hole distances, kept active under .25mm rule.

No hole/pad dimensions, exclusion, severity or clearance rule are changed by
this audit. Duplicate USB-C ground pads are distinguished from physical gaps.
"""
import collections, hashlib, json, math, sys
from pathlib import Path
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

r = Path(sys.argv[1]).resolve(); c = r / 'checks'
server = len(sys.argv) > 2; out = Path(sys.argv[2]).resolve() if server else c
g = json.loads((out / 'geometry.json' if server else c / 'geometry_current.json').read_text())
af = json.loads((out / 'assembly_features.json' if server else c / 'assembly_features_R130.json').read_text())
a = {x['uuid']: x for x in af['pads']}
d = json.loads((out / 'drc.json' if server else c / 'drc_checkpoint_R130.json').read_text())
rules = json.loads((r / 'enku-mainboard-r0.1.kicad_pro').read_text())['board']['design_settings']['rules']
assert rules['min_hole_clearance'] == .25

def local(f, pos):
    dx, dy = [v - w for v, w in zip(pos, f['pos'])]
    angle = math.radians(f['angle'])
    return [round(math.cos(angle) * dx - math.sin(angle) * dy, 6), round(math.sin(angle) * dx + math.cos(angle) * dy, 6)]
def copper(q): return unary_union([Polygon(poly) for poly in q['polygons']['0']])
rows = []
for ref in ['SW3', 'SW4', 'SW5', 'SW6']:
    f = g['footprints'][ref]
    ps = [x for x in g['pads'] if x['ref'] == ref]
    holes = [x for x in ps if x['attribute'] == 3]
    assert len(holes) == 2 and {tuple(local(f, x['pos'])) for x in holes} == {(-2.125, 0), (2.125, 0)}
    assert all(x['drill'] == [.9, .9] for x in holes)
    for hole in holes:
        distances = sorted((copper(q).distance(Point(*hole['pos'])) - .45, q['uuid'], q['number']) for q in ps if not max(q['drill']))
        close = [row for row in distances if row[0] < .25 - 1e-6]
        assert len(close) == 2
        assert abs(close[0][0] - .075) < 1e-6 and abs(close[1][0] - .15) < 1e-6
        rows.append({'ref': ref, 'hole_uuid': hole['uuid'], 'hole_position_mm': hole['pos'], 'signal_land_gap_mm': round(close[0][0], 6), 'bracket_land_gap_mm': round(close[1][0], 6), 'drawing_diameter_mm': .9})

usb = g['footprints']['J5']; ps = [x for x in g['pads'] if x['ref'] == 'J5']
holes = [x for x in ps if x['attribute'] == 3]
assert len(holes) == 2 and {tuple(local(usb, x['pos'])) for x in holes} == {(-2.89, -2.605), (2.89, -2.605)}
assert all(x['drill'] == [.65, .65] for x in holes)
nominal_rounded = math.hypot(.16, .65) - .15 - .325
nominal_rectangular = math.hypot(.01, .5) - .325
for hole in holes:
    near = [x for x in ps if x['number'] in ['A1', 'B12', 'A12', 'B1'] and abs(x['pos'][0] - hole['pos'][0]) < .4]
    assert len(near) == 2 and near[0]['pos'] == near[1]['pos']
    for q in near:
        assert q['net'] == 'GND' and q['size'] == [.6, 1.15] and q['shape'] == 4 and a[q['uuid']]['roundrect_radius_mm'] == .15
        measured = copper(q).distance(Point(*hole['pos'])) - .325
        assert abs(measured - nominal_rounded) < .001
    rows.append({'ref': 'J5', 'hole_uuid': hole['uuid'], 'hole_position_mm': hole['pos'], 'coincident_GND_pad_numbers': [x['number'] for x in near], 'native_rounded_land_nominal_gap_mm': nominal_rounded, 'manufacturer_rectangular_land_envelope_gap_mm': nominal_rectangular, 'drawing_diameter_mm': .65})

findings = [x for x in d['violations'] if x['type'] == 'hole_clearance']
scope = collections.Counter()
for v in findings:
    refs = {i['description'].rsplit(' of ', 1)[-1].split()[0] if ' of ' in i['description'] else i['description'].split()[-1] for i in v['items']}
    assert len(refs) == 1
    scope.update(refs)
assert dict(scope) == {'SW3': 4, 'SW4': 4, 'SW5': 4, 'SW6': 4, 'J5': 4}
assert len(findings) == 20 and all(v['severity'] == 'error' for v in findings)
sha = (out / 'source_pcb.sha256').read_text().split()[0] if server else hashlib.sha256((r / 'enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
report = {
    'revision': 'R130', 'pcb_sha256': sha,
    'manufacturer_nominal_locator_holes_and_intrinsic_distances_verified': True,
    'active_hole_clearance_errors': 20, 'active_errors_by_component': dict(scope),
    'unique_physical_inadequate_copper_to_hole_interfaces': 18,
    'USB_four_native_findings_are_two_coincident_pad_locations': True,
    'unchanged_required_hole_clearance_mm': .25,
    'hole_rows': rows,
    'holes_shrunk_moved_or_reclassified': False,
    'lands_clipped_or_shortened_to_hide_findings': False,
    'rules_exclusions_or_severity_weakened': False,
    'factory_part_specific_hole_rule_and_process_approved': False,
    'TL3340_locator_and_land_tolerances_qualified': False,
    'USB4105_actual_stake_variant_board_thickness_and_process_qualified': False,
    'fabrication_ready': False,
    'manufacturer_sources': {
        'TL3340AF160QG': 'E-Switch P021301 revisionB,2008-01-07, supplied original controlled PDF',
        'USB4105': 'GCT USB4105 revisionB4,2023-12-18, supplied original PDF, sheet1/2; current public endpoint denied403',
    },
    'scope': 'Nominal distances are below the active0.25mm board rule even with source-drawing geometry. The TL3340 drawing gives generalX.X±0.4/X.XX±0.25mm; GCT recommended layout±0.05mm. These do not grant factory drill/copper-process acceptance. Retain active findings until documented part-specific manufacturing rule or an independently accepted changed land/part design exists.',
}
(out / 'intrinsic_holes_audit_R130.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
