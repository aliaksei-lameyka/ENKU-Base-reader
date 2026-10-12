"""Check exact U3 thermal construction requests and real refilled spreading copper.

The 50 mm2 continuous B-copper objective is reported even if not reached;
temperature/heat spreading acceptance stays HOLD. Local inner islands and
actual spreading areas are reported, not treated as a thetaJA rating. This guard
checks constructed geometry/connectivity and retains the unmet design goal.
"""
import gzip, hashlib, json, math, sys
from pathlib import Path
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import unary_union
from pad_groups import partitions

r, out = map(lambda s: Path(s).resolve(), sys.argv[1:3]); c=r/'checks'
g=json.loads((out/'geometry.json').read_text())
process=json.loads((out/'via_process_R138.json').read_text());pm={x['uuid']:x for x in process['vias']}
m=json.loads((c/'thermal_via_manifest_R138.json').read_text());wanted={x['uuid']:x for x in m['added_vias']}
assert len(wanted)==5
positions={(48.5,91.)}|{(48.5+x,91.+y)for x in [-.53,.53]for y in [-.53,.53]}
assert {tuple(v['position_mm'])for v in wanted.values()}==positions
native={x['uuid']:x for x in g['tracks'] if x['via']}
ep=next(x for x in g['pads'] if x['ref']=='U3' and x['number']=='17')
ep_shape=unary_union([Polygon(p)for p in ep['polygons']['0']])
assert ep['net']=='GND' and ep['size']==[1.68,1.68]
for uid,v in wanted.items():
    a=native[uid];p=pm[uid]
    assert a['start']==v['position_mm'] and a['net']=='GND' and a['drill']==.3 and a['width']==.6
    assert ep_shape.covers(Point(a['start']).buffer(.3))
    assert p['fill_requested'] and p['cap_requested'] and p['back_tented'] and not p['front_tented']
assert len(partitions(g)['GND'])==1
assert min(math.dist(a,b)-.3 for a in positions for b in positions if a!=b)>.25
thermal=json.loads(gzip.decompress((out/'thermal_planes_R138.json.gz').read_bytes()))
rows=thermal['2'];polys=[Polygon(x['shell'],x['holes'])for x in rows]
spreading=next(p for p in polys if p.covers(Point(48.5,91)))
assert spreading.area>ep_shape.area, 'No spreading copper beyond the thermal land'
assert all(row['zone']=='R133_U3_GND_THERMAL_SPREAD_NO_FAB' and row['solid_connection_requested']for row in rows)
for pos in positions:
    assert Point(pos).buffer(.3).difference(spreading).area<.0001, ('Via not solidly covered by B GND',pos)
assert ep_shape.difference(spreading).area<.0001
usb=[LineString([t['start'],t['end']]).buffer(t['width']/2)for t in g['tracks']if not t['via']and t['layer']==2 and t['net'].startswith('USB_D')]
min_USB=unary_union(polys).distance(unary_union(usb))
assert min_USB>=1.-.00001
local={}
for l in ['4','6']:
    ps=[Polygon(x['shell'],x['holes'])for x in thermal[l]]
    u=unary_union(ps)
    local[l]=dict(EP_shadow_GND_coverage_fraction=u.intersection(ep_shape).area/ep_shape.area,
                  EP_center_contiguous_GND_area_mm2=next(p.area for p in ps if p.covers(Point(48.5,91))))
report=dict(revision='R138',pcb_sha256=(out/'source_pcb.sha256').read_text().split()[0],
    native_five_under_EP_vias_verified=True,manufacturer_example_positions_mm_offset=.58,project_positions_mm_offset=.53,
    project_drill_mm=.3,manufacturer_example_drill_mm=.2,land_mm=.6,
    project_drill_adaptation_is_SLUA271_starting_point_not_factory_approval=True,
    exact_native_fill_and_copper_cap_requests_verified=True,back_mask_tenting_request_verified=True,
    all_GND_pads_and_thermal_vias_electrically_connected=True,
    B_continuous_GND_spreading_area_mm2=spreading.area,B_EP_coverage_fraction=1.,
    continuous_B_spreading_objective_mm2=50.,continuous_B_spreading_objective_met=spreading.area>=50.,
    minimum_B_coplanar_GND_to_preserved_USB_copper_mm=min_USB,
    small_inner_GND_regions=local,
    example_stencil_and_EPad_lands_unchanged=True,
    construction_required='Resin fill and copper cap under U3 paste; factory must approve flatness/finish/voiding; no ordinary tent substitute accepted by this revision',
    actual_filled_capped_construction_accepted=False,
    thetaJA_temperature_charge_curve_and_battery_heat_qualified=False,
    manufacturing_release=False,fabrication_ready=False)
(out/'U3_thermal_audit_R138.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
