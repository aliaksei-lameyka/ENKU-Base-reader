"""R148 derivative: two unused J1 mechanical lands removed. Other routing analysis retained."""
"""Read-only whole-board routing review of actual Native KiCad geometry.

No acceptance baseline is regenerated. Heuristic detours and reference gaps are
review findings, not measured signal failures. Track-only electrical models omit
pad spreading, component/via impedance and the unspecified production stackup.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import heapq
import json
import math
from pathlib import Path

import shapely as sh
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, Point, Polygon

LAYERS = {0: "F.Cu", 4: "In1.Cu", 6: "In2.Cu", 2: "B.Cu"}
FAST = {"SPI_SCLK", "SPI_MOSI", "SPI_MISO", "SD_SCLK_CARD", "SD_MOSI_CARD",
        "SD_MISO_CARD", "SD_CS", "SD_CS_CARD", "EPD_SCLK_PANEL", "EPD_MOSI_PANEL",
        "USB_DM", "USB_DP", "USB_DM_CONN", "USB_DP_CONN"}
POWER = {"3V3_SYS", "SYS_EN", "VSYS", "VBAT", "VBUS_USB", "EPD_VCI", "EPD_VDD",
         "EPD_SW", "EPD_VGH", "EPD_VGL", "EPD_VSH2", "REG_L1", "REG_L2"}
PCB_SHA = "90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971"


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def coord(v):
    return tuple(round(float(x), 6) for x in v)


def lines(shape):
    if shape.is_empty:
        return []
    if shape.geom_type == "LineString":
        return [shape]
    if hasattr(shape, "geoms"):
        return [line for part in shape.geoms for line in lines(part)]
    return []


def pad_shape(pad, layer):
    return sh.union_all([Polygon(p) for p in pad["polygons"].get(str(layer), [])])


def pad_drill_shape(pad):
    w, h = pad["drill"]
    if min(w, h) <= 0:
        return Polygon()
    radius = min(w, h)/2
    if abs(w-h) < 1e-9:
        return Point(pad["pos"]).buffer(radius, quad_segs=64)
    dx, dy = max(w-h, 0)/2, max(h-w, 0)/2
    hole = LineString([(-dx, -dy), (dx, dy)]).buffer(radius, quad_segs=64)
    hole = rotate(hole, -pad["angle"], origin=(0, 0))
    return translate(hole, *pad["pos"])


class Network:
    def __init__(self, g, net):
        self.net = net
        self.tracks = [t for t in g["tracks"] if t["net"] == net]
        self.pads = [p for p in g["pads"] if p["net"] == net and p["number"]]
        self.edges = collections.defaultdict(list)
        self.chains = []
        for layer in LAYERS:
            routed = [LineString([t["start"], t["end"]]) for t in self.tracks
                      if not t["via"] and t["layer"] == layer]
            # Unary union nodes real same-layer centreline intersections.
            for line in lines(sh.union_all(routed)):
                points = list(line.coords)
                for a, b in zip(points, points[1:]):
                    mid = Point((a[0]+b[0])/2, (a[1]+b[1])/2)
                    original = [t for t in self.tracks if not t["via"] and t["layer"] == layer
                                and LineString([t["start"], t["end"]]).distance(mid) < 1e-6]
                    assert original, (net, layer, a, b)
                    width = max(t["width"] for t in original)
                    aa, bb = (*coord(a), layer), (*coord(b), layer)
                    self.link(aa, bb, math.dist(a, b), width)
        for via in [t for t in self.tracks if t["via"]]:
            nodes = [(*coord(via["start"]), layer) for layer in LAYERS]
            for a, b in zip(nodes, nodes[1:]):
                self.link(a, b, 0, None)
        # Virtual pad contacts connect every real endpoint in the actual land.
        vertices = list(self.edges)
        for p in self.pads:
            key = ("pad", p["uuid"])
            contacts = []
            for v in vertices:
                if v[2] in p["layers"] and pad_shape(p, v[2]).buffer(1e-6).covers(Point(v[:2])):
                    contacts.append(v)
            for contact in contacts:
                self.link(key, contact, 0, None)

    def link(self, a, b, length, width):
        self.edges[a].append((b, length, width))
        self.edges[b].append((a, length, width))

    def pad(self, ref, pin):
        return next(p for p in self.pads if p["ref"] == ref and p["number"] == pin)

    def path(self, source, target):
        a = ("pad", self.pad(*source)["uuid"])
        b = ("pad", self.pad(*target)["uuid"])
        best = {a: 0.0}; previous = {}; serial = 0
        queue = [(0.0, serial, a)]
        while queue:
            distance, _, node = heapq.heappop(queue)
            if distance != best[node]:
                continue
            if node == b:
                break
            for nxt, length, width in self.edges[node]:
                value = distance + length
                if value < best.get(nxt, math.inf):
                    best[nxt] = value; previous[nxt] = (node, length, width)
                    serial += 1; heapq.heappush(queue, (value, serial, nxt))
        if b not in best:
            return dict(net=self.net, source=list(source), target=list(target),
                        status="TRACK_MODEL_UNRESOLVED_NOT_A_NATIVE_OPEN")
        edges = []; node = b
        while node != a:
            parent, length, width = previous[node]
            edges.append((parent, node, length, width)); node = parent
        resistance = sum(1.7241e-5 * length / (width * .035)
                         for _, _, length, width in edges if width)
        widths = [width for _, _, length, width in edges if width and length > 1e-6]
        straight = math.dist(self.pad(*source)["pos"], self.pad(*target)["pos"])
        result = dict(net=self.net, source=list(source), target=list(target), status="MEASURED_TRACK_PATH",
                    track_centerline_length_mm=best[b], pad_center_distance_mm=straight,
                    length_to_pad_center_chord_ratio=best[b]/straight if straight else None,
                    minimum_track_width_mm=min(widths) if widths else None,
                    conditional_35um_20C_track_resistance_ohm=resistance,
                    path_centerline_edges=[dict(start=list(a[:2]), end=list(b[:2]), layer=LAYERS[a[2]], width_mm=width)
                        for a,b,length,width in reversed(edges) if width and length > 1e-6],
                    excludes_vias_components_pad_spreading_and_actual_stackup=True)
        if self.net in POWER:
            result.update(conditional_drop_at_0p5A_V=resistance*.5,
                          conditional_drop_at_1A_V=resistance)
        return result


def validate_graph_model():
    """Independent geometric fixtures protect against false layer continuity."""
    def pad(uid, xy, layer):
        x, y = xy
        return dict(uuid=uid, ref=uid, number="1", net="fixture", pos=xy,
                    layers=[layer], polygons={str(layer): [[
                        [x-.01,y-.01], [x+.01,y-.01], [x+.01,y+.01], [x-.01,y+.01]]]})
    def track(a, b, layer):
        return dict(net="fixture", start=a, end=b, layer=layer, via=False, width=.2)
    separate = dict(tracks=[track([0,0], [1,0], 0), track([1,0], [2,0], 2)],
                    pads=[pad("source", [0,0], 0), pad("target", [2,0], 2)])
    absent = Network(separate, "fixture").path(("source","1"), ("target","1"))
    assert absent["status"] == "TRACK_MODEL_UNRESOLVED_NOT_A_NATIVE_OPEN"
    connected = dict(pads=separate["pads"], tracks=separate["tracks"]+[
        dict(net="fixture", start=[1,0], end=[1,0], via=True, width=.45)])
    real_via = Network(connected, "fixture").path(("source","1"), ("target","1"))
    assert abs(real_via["track_centerline_length_mm"]-2) < 1e-9
    crossing = dict(tracks=[track([0,0], [2,0], 0), track([1,-1], [1,1], 0)],
                    pads=[pad("source", [0,0], 0), pad("target", [1,1], 0)])
    same_layer = Network(crossing, "fixture").path(("source","1"), ("target","1"))
    assert abs(same_layer["track_centerline_length_mm"]-2) < 1e-9
    return dict(equal_xy_different_layers_without_via="UNRESOLVED_AS_EXPECTED",
                actual_through_via_connects_layers_measured_mm=real_via["track_centerline_length_mm"],
                same_layer_midsegment_intersection_measured_mm=same_layer["track_centerline_length_mm"],
                cases_passed=3)


def chains(g, net):
    tracks = [t for t in g["tracks"] if t["net"] == net and not t["via"]]
    adj = collections.defaultdict(list)
    for i, t in enumerate(tracks):
        for point in [t["start"], t["end"]]:
            adj[(*coord(point), t["layer"])].append(i)
    anchors = {(*coord(t["start"]), layer) for t in g["tracks"] if t["net"] == net and t["via"] for layer in LAYERS}
    for node in list(adj):
        if any(p["net"] == net and node[2] in p["layers"] and pad_shape(p, node[2]).buffer(1e-6).covers(Point(node[:2])) for p in g["pads"]):
            anchors.add(node)
    visited = set(); results = []
    starts = [n for n, edges in adj.items() if len(edges) != 2 or n in anchors]
    for start in starts:
        for edge in adj[start]:
            if edge in visited:
                continue
            node = start; coords = [list(node[:2])]; ids = []
            while edge not in visited:
                visited.add(edge); t = tracks[edge]; ids.append(t["uuid"])
                a, b = (*coord(t["start"]), t["layer"]), (*coord(t["end"]), t["layer"])
                node = b if node == a else a; coords.append(list(node[:2]))
                if node in anchors or len(adj[node]) != 2:
                    break
                edge = next(i for i in adj[node] if i not in visited) if any(i not in visited for i in adj[node]) else edge
            if len(ids) < 6:
                continue
            distance = sum(math.dist(a, b) for a, b in zip(coords, coords[1:]))
            chord = math.dist(coords[0], coords[-1])
            if distance-chord > .25:
                results.append(dict(net=net, layer=LAYERS[start[2]], segments=len(ids),
                    length_mm=distance, chord_mm=chord, extra_vs_unobstructed_chord_mm=distance-chord,
                    ratio_to_unobstructed_chord=distance/chord if chord else None,
                    bounds=list(LineString(coords).bounds), uuids=ids, coordinates_mm=coords,
                    straight_replacement_clearance_not_assumed=True))
    return results


def review(root, native, output):
    output.mkdir(parents=True, exist_ok=True)
    actual = hashlib.sha256((root / "enku-mainboard-r0.1.kicad_pcb").read_bytes()).hexdigest()
    assert actual == PCB_SHA == (native / "source_pcb.sha256").read_text().split()[0]
    g = json.loads((native / "geometry.json").read_text())
    assert len(g["pads"]) == 471 and len(g["footprints"]) == 141
    graph_validation = validate_graph_model()
    fill = json.loads(gzip.decompress((native / "native_copper_R138.json.gz").read_bytes()))
    drc = json.loads((native / "drc.json").read_text()); erc = json.loads((native / "erc.json").read_text())
    assert not drc["violations"] and not drc["unconnected_items"] and not drc["schematic_parity"]
    assert not any(s["violations"] for s in erc["sheets"])
    planes = {}
    for layer in LAYERS:
        shapes = [sh.make_valid(Polygon(p["shell"], p["holes"])) for p in fill["filled_zones"][str(layer)] if p["net"] == "GND"]
        for p in g["pads"]:
            if p["net"] == "GND":
                shapes.append(pad_shape(p, layer).difference(pad_drill_shape(p)))
        for t in g["tracks"]:
            if t["net"] != "GND":
                continue
            if t["via"]:
                shapes.append(Point(t["start"]).buffer(t["width"]/2, quad_segs=64).difference(Point(t["start"]).buffer(t["drill"]/2, quad_segs=64)))
            elif t["layer"] == layer:
                shapes.append(LineString([t["start"], t["end"]]).buffer(t["width"]/2, quad_segs=64))
        planes[layer] = sh.union_all(shapes)
    inner = planes[4].union(planes[6]); inventory = []; gaps = []; via_rows = []; detours = []
    ground_barrels = [(t["uuid"], t["start"]) for t in g["tracks"] if t["via"] and t["net"] == "GND"]
    ground_barrels += [(p["uuid"], p["pos"]) for p in g["pads"] if p["net"] == "GND" and max(p["drill"]) > 0 and len(p["layers"]) > 1]
    all_nets = sorted({t["net"] for t in g["tracks"]})
    for net in all_nets:
        ts = [t for t in g["tracks"] if t["net"] == net]; routed = [t for t in ts if not t["via"]]
        total = sum(math.dist(t["start"], t["end"]) for t in routed)
        row = dict(net=net, category="FAST" if net in FAST else "POWER" if net in POWER else "GND" if net == "GND" else "CONTROL",
                   segments=len(routed), vias=sum(t["via"] for t in ts), total_track_length_mm=total,
                   widths_mm=sorted({t["width"] for t in routed}),
                   layers=dict(collections.Counter(LAYERS[t["layer"]] for t in routed)),
                   pads=sorted(set(p["ref"]+":"+p["number"] for p in g["pads"] if p["net"] == net and p["number"])))
        own = sh.union_all([Point(t["start"]).buffer(t["width"]/2+.26, quad_segs=64) for t in ts if t["via"]])
        missing_lengths = [0., 0.]; area = [0., 0.]
        for t in routed:
            if t["layer"] not in [0, 2] or net == "GND":
                continue
            reference = 4 if t["layer"] == 0 else 6
            line = LineString([t["start"], t["end"]]); center = line.difference(own)
            shape = line.buffer(t["width"]/2, quad_segs=64).difference(own)
            near = center.difference(planes[reference]); both = center.difference(inner)
            near_area = shape.difference(planes[reference]).area
            both_area = shape.difference(inner).area
            missing_lengths[0] += near.length; missing_lengths[1] += both.length
            area[0] += near_area; area[1] += both_area
            if net in FAST and (near.length > .1 or both.length > .05):
                gaps.append(dict(net=net, uuid=t["uuid"], signal_layer=LAYERS[t["layer"]],
                    preferred_reference_layer=LAYERS[reference], start=t["start"], end=t["end"],
                    preferred_centerline_gap_mm=near.length, both_inner_centerline_gap_mm=both.length,
                    preferred_gap_pieces_mm=[list(part.coords) for part in lines(near)],
                    both_inner_gap_pieces_mm=[list(part.coords) for part in lines(both)],
                    reference_through_pad_via_antipads_not_counted=True,
                    field_simulation_and_actual_edge_rate_unavailable=True))
        row.update(preferred_reference_centerline_gap_mm=missing_lengths[0],
                   both_inner_GND_centerline_gap_mm=missing_lengths[1],
                   preferred_reference_missing_strip_area_mm2=area[0],
                   both_inner_GND_missing_strip_area_mm2=area[1])
        inventory.append(row)
        if net != "GND":
            detours.extend(chains(g, net))
        if net in FAST:
            for t in ts:
                if not t["via"]:
                    continue
                nearest = min((math.dist(t["start"], xy), uid, xy) for uid, xy in ground_barrels)
                via_rows.append(dict(net=net, signal_via_uuid=t["uuid"], position_mm=t["start"],
                    nearest_ground_barrel_distance_mm=nearest[0], nearest_ground_barrel_uuid=nearest[1],
                    nearest_ground_barrel_position_mm=nearest[2], spacing_is_review_metric_not_an_accepted_limit=True))
    tasks = [
        ("SPI_SCLK", ("U1", "20"), ("R21", "1")), ("SPI_SCLK", ("U1", "20"), ("R33", "1")),
        ("SPI_MOSI", ("U1", "19"), ("R20", "1")), ("SPI_MOSI", ("U1", "19"), ("R34", "1")),
        ("SPI_MISO", ("R22", "2"), ("U1", "21")),
        ("3V3_SYS", ("U4", "6"), ("U1", "2")), ("3V3_SYS", ("U4", "6"), ("J2", "4")),
        ("3V3_SYS", ("U4", "6"), ("R28", "1")),
        ("SYS_EN", ("Q2", "3"), ("U4", "10")), ("SYS_EN", ("C9", "1"), ("U4", "10")),
        ("3V3_SYS", ("U4", "6"), ("C11", "1")), ("3V3_SYS", ("U4", "6"), ("C12", "1")),
        ("VBUS_USB", ("J5", "A4"), ("U3", "13")), ("VBUS_USB", ("C5", "1"), ("U3", "13")),
        ("VBUS_USB", ("C2", "1"), ("U3", "13")), ("VBUS_USB", ("C4", "1"), ("U3", "13")),
        ("VBUS_USB", ("C6", "1"), ("U3", "13")),
        ("VSYS", ("U3", "10"), ("Q2", "2")), ("VSYS", ("U3", "10"), ("C7", "1")),
        ("VBAT", ("J1", "1"), ("U3", "2")), ("VBAT", ("C8", "1"), ("U3", "2")),
        ("REG_L1", ("U4", "9"), ("L1", "1")), ("REG_L2", ("U4", "7"), ("L1", "2")),
        ("REG_FB", ("U4", "4"), ("R14", "2")),
        ("EPD_SW", ("Q1", "3"), ("L2", "2")), ("EPD_SW", ("Q1", "3"), ("D1", "2")),
        ("EPD_SW", ("Q1", "3"), ("C25", "1")),
        ("EPD_VCI", ("C22", "1"), ("L2", "1")),
        ("CHG_TS", ("R82", "2"), ("U3", "1")),
        ("BAT_TS", ("J8", "1"), ("R82", "1")),
    ]
    networks = {}; paths = []
    for net, source, target in tasks:
        if net not in networks:
            networks[net] = Network(g, net)
        paths.append(networks[net].path(source, target))
    # These are geometric facts; there is no numeric parasitic/layout pass limit.
    hotloop = {ref: g["footprints"][ref]["pos"] for ref in ["U4", "L1", "C9", "C11", "C12", "U3", "C5", "C7", "C8", "Q1", "L2", "D1", "C25", "C22"]}
    report = dict(audit_revision="R140", physical_revision="R138", pcb_sha256=actual,
        native_kicad="10.0.7", all_track_items_reviewed=len(g["tracks"]), routed_segments_reviewed=sum(not t["via"] for t in g["tracks"]),
        vias_reviewed=sum(t["via"] for t in g["tracks"]), track_nets_reviewed=len(all_nets),
        actual_473_pads_and_141_references_verified=True, DRC=0, ERC=0, opens=0, schematic_parity=0,
        physical_source_modified=False, native_baseline_regenerated=False,
        inventory=inventory, multi_segment_detour_candidates=sorted(detours, key=lambda r:r["extra_vs_unobstructed_chord_mm"], reverse=True),
        fast_signal_reference_gaps=gaps, fast_signal_via_return_distances=via_rows,
        actual_track_paths=paths, power_placement_centers_mm=hotloop,
        independent_graph_fixture_validation=graph_validation,
        methodology={"reference": "Actual filled GND polygons plus native GND lands/tracks/via annuli, with round and oblong drill holes subtracted. Preferred reference is In1 for F and In2 for B. Both-inner coverage is an alternative projection, not an EM equivalence.",
                     "antipads": "Own signal via radius +0.25mm clearance +0.01mm explicit polygon margin excluded, matching the retained USB audit convention.",
                     "path": "Centreline graph is noded per actual layer; only real through vias and real copper lands join layers/endpoints. Virtual pad spreading has zero length. No impedance or measured propagation claim.",
                     "detour": "Six or more degree-two endpoint segments and >0.25mm extra length over a free-space chord. No clearance-safe straightening or intentional length matching is inferred.",
                     "power": "Track-only shortest-path resistance scenario: rho20C=1.7241e-5 ohm*mm,35um copper. Actual copper thickness,temperature,contact/via/component resistance,return paths,current distribution and heating are unqualified."},
        primary_sources=["https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html",
                         "https://www.ti.com/lit/ds/symlink/tps63802.pdf",
                         "https://www.ti.com/lit/ds/symlink/bq24072t.pdf"],
        SI_power_transients_and_EMC_physically_qualified=False, fabrication_ready=False)
    write_json(output / "routing_review_R140.json", report)
    with (output / "all_track_nets_R140.csv").open("w", newline="") as f:
        fields = ["net", "category", "segments", "vias", "total_track_length_mm", "widths_mm", "layers", "preferred_reference_centerline_gap_mm", "both_inner_GND_centerline_gap_mm"]
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
        writer.writerows({k:r[k] for k in fields} for r in inventory)
    print(json.dumps(dict(nets=len(inventory), segments=report["routed_segments_reviewed"], vias=report["vias_reviewed"],
        detour_candidates=len(detours), fast_reference_track_findings=len(gaps), explicit_paths=len(paths),
        unresolved_track_models=sum(p["status"] != "MEASURED_TRACK_PATH" for p in paths), no_board_mutation=True), indent=2))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("kicad", type=Path); ap.add_argument("native", type=Path); ap.add_argument("output", type=Path)
    args = ap.parse_args(); review(args.kicad.resolve(), args.native.resolve(), args.output.resolve())
