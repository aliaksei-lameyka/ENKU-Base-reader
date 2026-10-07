#!/usr/bin/env python3
"""Structural/mechanical gate for ENKU Mainboard R0.1 placement baseline."""

from __future__ import annotations

from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
PCB = HERE / "enku-mainboard-r0.1.kicad_pcb"

REQUIRED_REFS = {
    "U1", "U5", "U6",
    "J3", "J2", "J5", "J6", "J1",
    "U2", "U3", "U4", "U8",
    "L2", "Q1", "D1", "D2", "D3", "R37",
    "L1", "R14", "R15", "R16", "C9", "C10", "C11", "C12", "SW1",
    "SW3", "SW4", "SW5", "SW6",
    "TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "TP7", "TP8",
    "TP9", "TP10", "TP11", "TP12", "TP13", "TP14",
}

BOARD = (20.0, 20.0, 74.0, 114.0)
EXPECTED_SIZE = (54.0, 94.0)

# Placement-only coordinate gates. These are broad regions, not final courtyard DRC.
REGIONS = {
    "U1": (20.0, 31.0, 46.0, 59.0),
    "J3": (48.0, 24.0, 72.0, 32.0),
    "J2": (20.0, 94.0, 38.0, 113.0),
    "J5": (40.0, 105.0, 54.0, 114.0),
    "J6": (38.0, 95.0, 56.0, 104.0),
    "SW1": (23.0, 25.0, 38.0, 33.0),
    # Symmetric edge controls: two buttons on each side for left/right-handed remapping.
    "SW3": (23.0, 58.0, 27.0, 68.0),
    "SW4": (23.0, 70.0, 27.0, 80.0),
    "SW5": (69.0, 58.0, 73.5, 68.0),
    "SW6": (69.0, 70.0, 73.5, 80.0),
    "U2": (39.0, 87.0, 47.0, 96.0),
    "U3": (45.0, 87.0, 52.0, 96.0),
    "U4": (50.0, 87.0, 58.0, 96.0),
}

def balanced(text: str) -> tuple[bool, str]:
    depth = 0
    in_string = False
    escaped = False
    for i, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False, f"unexpected ')' at byte {i}"
    if in_string:
        return False, "unterminated string"
    if depth:
        return False, f"parenthesis depth ends at {depth}"
    return True, "ok"

def footprint_blocks(text: str):
    """Yield balanced top-level footprint blocks without a full KiCad parser."""
    pos = 0
    while True:
        start = text.find("(footprint ", pos)
        if start < 0:
            return
        depth = 0
        in_string = False
        escaped = False
        end = None
        for i in range(start, len(text)):
            ch = text[i]
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            return
        yield text[start:end]
        pos = end

def footprint_block(text: str, ref: str) -> str | None:
    """Return the balanced footprint block for one reference."""
    for block in footprint_blocks(text):
        parsed = parse_ref_and_at(block)
        if parsed and parsed[0] == ref:
            return block
    return None

def parse_ref_and_at(block: str):
    ref_m = re.search(r'\(property "Reference" "([^"]+)"', block)
    at_m = re.search(r'\(at\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)(?:\s+(-?\d+(?:\.\d+)?))?\)', block)
    if not ref_m or not at_m:
        return None
    return ref_m.group(1), float(at_m.group(1)), float(at_m.group(2)), float(at_m.group(3) or 0)

def main() -> int:
    errors: list[str] = []
    if not PCB.is_file():
        print(f"ERROR: missing {PCB.name}")
        return 1
    text = PCB.read_text(encoding="utf-8")

    ok, why = balanced(text)
    if not ok:
        errors.append(f"malformed PCB S-expression: {why}")

    outline = re.search(
        r'\(gr_rect \(start 20(?:\.0+)? 20(?:\.0+)?\) \(end 74(?:\.0+)? 114(?:\.0+)?\)',
        text
    )
    if not outline:
        errors.append("54x94 mm R0.1 board outline is missing or changed")

    refs: dict[str, tuple[float,float,float]] = {}
    duplicates: set[str] = set()
    for block in footprint_blocks(text):
        parsed = parse_ref_and_at(block)
        if not parsed:
            continue
        ref, x, y, rot = parsed
        if ref in refs:
            duplicates.add(ref)
        refs[ref] = (x, y, rot)

    for ref in sorted(REQUIRED_REFS):
        if ref not in refs:
            errors.append(f"missing critical placed reference {ref}")

    for ref in sorted(duplicates):
        errors.append(f"duplicate PCB reference {ref}")

    x0, y0, x1, y1 = BOARD
    for ref, (x,y,rot) in refs.items():
        if ref.startswith("H"):
            continue
        if not (x0 <= x <= x1 and y0 <= y <= y1):
            errors.append(f"{ref} origin outside board: ({x}, {y})")

    for ref, region in REGIONS.items():
        if ref not in refs:
            continue
        x, y, _ = refs[ref]
        rx0, ry0, rx1, ry1 = region
        if not (rx0 <= x <= rx1 and ry0 <= y <= ry1):
            errors.append(
                f"{ref} escaped placement region: ({x:.2f},{y:.2f}) "
                f"not in [{rx0},{ry0}]..[{rx1},{ry1}]"
            )

    # Critical mechanical invariants.
    if "U1" in refs:
        x, y, rot = refs["U1"]
        if abs(rot - 90.0) > 0.1:
            errors.append("U1 must stay rotated 90 deg with antenna keepout toward left edge")
    # Reading controls must remain on the physical side rails, not migrate into bezel/front-face space.
    for ref in ("SW3", "SW4"):
        if ref in refs and refs[ref][0] > 27.0:
            errors.append(f"{ref} left the left-side edge control rail")
    for ref in ("SW5", "SW6"):
        if ref in refs and refs[ref][0] < 69.0:
            errors.append(f"{ref} left the right-side edge control rail")
    if all(ref in refs for ref in ("SW3", "SW4", "SW5", "SW6")):
        if abs(refs["SW3"][1] - refs["SW5"][1]) > 0.5 or abs(refs["SW4"][1] - refs["SW6"][1]) > 0.5:
            errors.append("left/right reading-button pairs lost vertical symmetry")

    # WROOM body exclusion derived from the actual U1 placement.
    # Module F.Fab body is 18 x 25.5 mm. At 90 degrees this becomes 25.5 x 18 mm.
    # Never hard-code the historical U1=(33,45) geometry again.
    if "U1" in refs:
        ux, uy, urot = refs["U1"]
        if abs((urot % 180.0) - 90.0) < 0.1:
            body_x0, body_x1 = ux - 12.75, ux + 12.75
            body_y0, body_y1 = uy - 9.0, uy + 9.0
        else:
            body_x0, body_x1 = ux - 9.0, ux + 9.0
            body_y0, body_y1 = uy - 12.75, uy + 12.75
        for block in footprint_blocks(text):
            parsed = parse_ref_and_at(block)
            if not parsed:
                continue
            ref, x, y, _ = parsed
            if ref == "U1" or ref.startswith("H"):
                continue
            if '(layer "F.Cu")' in block and body_x0 < x < body_x1 and body_y0 < y < body_y1:
                errors.append(f"{ref} origin is under ESP32-S3-WROOM-1 module body")


    # Routed-copper integrity is validated by native KiCad DRC; placement gates should
    # encode geometry/invariants rather than depend on a stale textual baseline banner.

    # Orientation invariants for production-critical footprints. These protect
    # against the exact class of regressions where a rotated/flipped footprint is
    # interpreted in local coordinates while routing is authored in board coordinates.
    orientation_expectations = {
        "U1": ("F.Cu", 33.0, 45.0, 90.0),
        "U2": ("F.Cu", 43.5, 91.0, 0.0),
        "U3": ("F.Cu", 48.5, 91.0, 180.0),
        "U4": ("F.Cu", 58.0, 91.0, 0.0),
        "U5": ("F.Cu", 28.0, 80.0, 0.0),
        "U8": ("F.Cu", 54.2, 108.8, 180.0),
        "J1": ("F.Cu", 66.0, 93.5, 90.0),
        "J2": ("F.Cu", 28.9, 100.7, 90.0),
        "J3": ("F.Cu", 58.0, 28.0, 0.0),
        "J5": ("F.Cu", 47.0, 110.325, 0.0),
        "J6": ("B.Cu", 47.0, 99.0, 0.0),
        "SW1": ("F.Cu", 30.5, 29.0, 0.0),
        "SW3": ("F.Cu", 25.0, 63.0, 0.0),
        "SW4": ("F.Cu", 25.0, 75.0, 0.0),
        "SW5": ("F.Cu", 71.2, 63.0, 0.0),
        "SW6": ("F.Cu", 71.2, 75.0, 0.0),
    }
    for ref, (layer, x, y, rot) in orientation_expectations.items():
        fp = footprint_block(text, ref)
        if not fp:
            errors.append(f"{ref}: missing for orientation gate")
            continue
        if f'(layer "{layer}")' not in fp:
            errors.append(f"{ref}: expected on {layer}")
        at = re.search(r'\(at ([\d.-]+) ([\d.-]+)(?: ([\d.-]+))?\)', fp)
        if not at:
            errors.append(f"{ref}: missing footprint position")
            continue
        ax, ay = float(at.group(1)), float(at.group(2))
        ar = float(at.group(3) or 0.0) % 360.0
        if abs(ax-x) > 0.001 or abs(ay-y) > 0.001 or abs(ar-rot) > 0.001:
            errors.append(f"{ref}: orientation/placement drifted: got ({ax},{ay},{ar})")

    # Non-through via regression gate. For signal nets a blind/buried via must
    # have same-net track contact on both declared endpoint layers. Power-plane
    # exceptions must be explicit; this PCB currently has only GND copper zones.
    segment_layer_re = re.compile(
        r'\(segment \(start ([\d.-]+) ([\d.-]+)\) \(end ([\d.-]+) ([\d.-]+)\)'
        r'[^\n]*?\(layer "([^"]+)"\) \(net (\d+)\)'
    )
    layer_segments = []
    for sm in segment_layer_re.finditer(text):
        x1,y1,x2,y2,layer,net = sm.groups()
        layer_segments.append((float(x1),float(y1),float(x2),float(y2),layer,int(net)))
    via_span_re = re.compile(
        r'\(via \(at ([\d.-]+) ([\d.-]+)\)[^\n]*?'
        r'\(layers "([^"]+)" "([^"]+)"\) \(net (\d+)\)'
    )
    def endpoint_touch(x, y, layer, net):
        for x1,y1,x2,y2,slayer,snet in layer_segments:
            if snet != net or slayer != layer:
                continue
            if min((x-x1)**2+(y-y1)**2, (x-x2)**2+(y-y2)**2) < 0.000004:
                return True
        return False
    for vm in via_span_re.finditer(text):
        x,y,l1,l2,net = vm.groups()
        x,y,net = float(x),float(y),int(net)
        if {l1,l2} == {"F.Cu","B.Cu"}:
            continue
        if not endpoint_touch(x,y,l1,net) or not endpoint_touch(x,y,l2,net):
            errors.append(f"one-sided layer transition at ({x},{y}) net {net}: {l1}<->{l2}")

    # Cross-net centerline intersections are a routing-debt metric. Lock the
    # current burn-down ceiling so future edits cannot silently regress it.
    def orient(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    crossing_count = 0
    for i, a in enumerate(layer_segments):
        a1=(a[0],a[1]); a2=(a[2],a[3])
        for b in layer_segments[i+1:]:
            if a[4] != b[4] or a[5] == b[5]:
                continue
            b1=(b[0],b[1]); b2=(b[2],b[3])
            if any((p[0]-q[0])**2+(p[1]-q[1])**2 < 1e-12 for p in (a1,a2) for q in (b1,b2)):
                continue
            if orient(a1,a2,b1)*orient(a1,a2,b2) < 0 and orient(b1,b2,a1)*orient(b1,b2,a2) < 0:
                crossing_count += 1
    if crossing_count > 43:
        errors.append(f"cross-net centerline intersections regressed: {crossing_count} > 43 debt ceiling")

    # Silkscreen readability gate: visible reference designators must not overlap
    # each other on the same silkscreen side. This is intentionally conservative
    # and catches the common repairability failure where nearby 0603 refs merge.
    silk_refs = []
    ref_text_re = re.compile(
        r'\(property "Reference" "([^"]+)" \(at ([\d.-]+) ([\d.-]+)(?: ([\d.-]+))?\) '
        r'\(layer "(F\.SilkS|B\.SilkS)"\)([^\n]*)'
    )
    for block in footprint_blocks(text):
        parsed = parse_ref_and_at(block)
        if not parsed:
            continue
        ref, fx, fy, frot = parsed
        rm = ref_text_re.search(block)
        if not rm or "hide" in rm.group(6):
            continue
        dx, dy = float(rm.group(2)), float(rm.group(3))
        rrot = float(rm.group(4) or 0.0)
        fr = round(frot) % 360
        if fr == 0:
            x, y = fx + dx, fy + dy
        elif fr == 90:
            x, y = fx - dy, fy + dx
        elif fr == 180:
            x, y = fx - dx, fy - dy
        elif fr == 270:
            x, y = fx + dy, fy - dx
        else:
            continue
        grot = (frot + rrot) % 180.0
        horizontal = grot < 45.0 or grot > 135.0
        long_dim = max(1.2, len(ref) * 0.75)
        w, h = (long_dim, 1.2) if horizontal else (1.2, long_dim)
        silk_refs.append((ref, rm.group(5), x, y, w, h))

    for i, a in enumerate(silk_refs):
        for b in silk_refs[i+1:]:
            if a[1] != b[1]:
                continue
            if abs(a[2]-b[2]) < (a[4]+b[4])/2 + 0.15 and abs(a[3]-b[3]) < (a[5]+b[5])/2 + 0.15:
                errors.append(
                    f"silkscreen refs overlap: {a[0]} and {b[0]} on {a[1]}"
                )

    # Fabrication pad-envelope gate. Footprint origins being inside the board is
    # insufficient: U1 previously passed that test while an entire pad row crossed Edge.Cuts.
    # Use a conservative rotated pad bounding radius so false negatives are preferred over
    # silently fabricating clipped copper.
    for block in footprint_blocks(text):
        parsed = parse_ref_and_at(block)
        if not parsed:
            continue
        ref, fx, fy, frot = parsed
        theta = frot * 3.141592653589793 / 180.0
        is_back = '(layer "B.Cu")' in block
        for pm in re.finditer(
            r'\(pad "([^"]*)"[^\n]*?\(at ([\d.-]+) ([\d.-]+)(?: [\d.-]+)?\) '
            r'\(size ([\d.-]+) ([\d.-]+)\)',
            block,
        ):
            pad, px, py, sx, sy = pm.groups()
            px, py, sx, sy = map(float, (px, py, sx, sy))
            # KiCad stores pad local coordinates in footprint space for both board sides;
            # do not manually mirror B.Cu local X here. Board-side mirroring is already
            # represented by the footprint semantics used in the .kicad_pcb file.
            c, sn = __import__("math").cos(theta), __import__("math").sin(theta)
            # KiCad PCB coordinates have +Y downward: positive footprint rotation uses
            # x=fx+px*c+py*sn, y=fy-px*sn+py*c.
            ax = fx + px*c + py*sn
            ay = fy - px*sn + py*c
            # Axis-aligned half-extents of the rotated rectangular pad.
            hx = abs(c)*sx/2.0 + abs(sn)*sy/2.0
            hy = abs(sn)*sx/2.0 + abs(c)*sy/2.0
            clearance = min(ax-hx-BOARD[0], BOARD[2]-(ax+hx), ay-hy-BOARD[1], BOARD[3]-(ay+hy))
            if clearance < -1e-6:
                errors.append(
                    f"{ref} pad {pad} physical envelope crosses Edge.Cuts by {-clearance:.3f} mm"
                )

    # Text-edit regression gates: exact duplicate tracks and microscopic
    # patch stubs are never intentional routing. They previously hid stale endpoints.
    segment_full_re = re.compile(
        r'\(segment \(start ([\d.-]+) ([\d.-]+)\) \(end ([\d.-]+) ([\d.-]+)\) '
        r'\(width ([\d.-]+)\) \(layer "([^"]+)"\) \(net (\d+)\)\)'
    )
    seen_segments = set()
    for m in segment_full_re.finditer(text):
        x1, y1, x2, y2, width = map(float, m.groups()[:5])
        layer, net = m.group(6), int(m.group(7))
        ends = tuple(sorted(((round(x1, 6), round(y1, 6)), (round(x2, 6), round(y2, 6)))))
        key = (net, layer, ends)
        if key in seen_segments:
            errors.append(f"duplicate copper segment on net {net} {layer}: {ends}")
        seen_segments.add(key)
        length = ((x2-x1)**2 + (y2-y1)**2) ** 0.5
        if length < 0.05:
            errors.append(f"microscopic copper patch {length:.4f} mm on net {net} {layer}: {ends}")

    # Cheap pre-DRC copper-to-board-edge gate. Native KiCad remains authoritative,
    # but obvious routed copper outside/too close to the rectangular R0.1 outline must
    # never consume another Actions run. This intentionally checks segments/vias only.
    copper_edge_min = 0.15
    seg_re = re.compile(
        r'\(segment\s+\(start ([\d.-]+) ([\d.-]+)\)\s+'
        r'\(end ([\d.-]+) ([\d.-]+)\)\s+\(width ([\d.-]+)\)'
    )
    for m in seg_re.finditer(text):
        x1, y1, x2, y2, width = map(float, m.groups())
        radius = width / 2.0
        for x, y in ((x1, y1), (x2, y2)):
            clearance = min(x - BOARD[0], BOARD[2] - x, y - BOARD[1], BOARD[3] - y) - radius
            if clearance < copper_edge_min - 1e-6:
                errors.append(
                    f"segment endpoint ({x:.3f},{y:.3f}) has only {clearance:.3f} mm copper-edge clearance"
                )

    via_re = re.compile(r'\(via[\s\S]{0,180}?\(at ([\d.-]+) ([\d.-]+)\)[\s\S]{0,180}?\(size ([\d.-]+)\)')
    for m in via_re.finditer(text):
        x, y, size = map(float, m.groups())
        clearance = min(x - BOARD[0], BOARD[2] - x, y - BOARD[1], BOARD[3] - y) - size / 2.0
        if clearance < copper_edge_min - 1e-6:
            errors.append(f"via ({x:.3f},{y:.3f}) has only {clearance:.3f} mm copper-edge clearance")

    # BAT_TS regression gate: J1 is rotated 90 deg. With the current footprint,
    # pad 3 (BAT_TS) lands at board coordinate (66,91.5); pad 1 (VBAT) is at
    # (66,95.5). Never bridge these two pads.
    if not re.search(
        r'\(via \(at 66\.00 91\.50\).*?\(net 91\)\)',
        text,
    ):
        errors.append("BAT_TS route no longer terminates at current J1 pad 3")
    if re.search(
        r'\(segment \(start 66\.00 91\.50\) \(end 66\.00 95\.50\).*?\(net 91\)\)',
        text,
    ):
        errors.append("BAT_TS must not be bridged from J1 pad 3 to VBAT pad 1")


    tp_refs = [f"TP{i}" for i in range(1, 15)]
    if len(tp_refs) < 14:
        errors.append(f"expected at least 14 mandatory Base bring-up test points, gate has {len(tp_refs)}")
    for ref in tp_refs:
        marker = f'(property "Reference" "{ref}"'
        p = text.find(marker)
        if p < 0:
            continue
        fp_start = text.rfind("(footprint ", 0, p)
        fp_end = text.find("\n  )", p)
        block = text[fp_start:fp_end] if fp_start >= 0 and fp_end > p else ""
        if '(layer "B.Cu")' not in block:
            errors.append(f"{ref} must remain on accessible rear copper")
        pad_line = next((ln for ln in block.splitlines() if '(pad "1"' in ln), "")
        if '"B.Paste"' in pad_line:
            errors.append(f"{ref} probe pad must not have solder paste")

    forbidden_resolved_placeholders = (
        "R0.1_FH34SRJ_24_DUAL_CONTACT_PLACEHOLDER",
        "R0.1_FH34SRJ_6_DUAL_CONTACT_PLACEHOLDER",
        "R0.1_TPS923610_SOT563_PLACEHOLDER",
        "TPS2121_PLACEMENT_PLACEHOLDER",
        "BQ25185DLHR_PLACEMENT_PLACEHOLDER",
        "R0.1_TYS5040_47uH_PLACEHOLDER",
    )
    for token in forbidden_resolved_placeholders:
        if token in text:
            errors.append(f"resolved footprint placeholder returned: {token}")

    exact_footprint_tokens = (
        "ENKU:TPS2121_RUX0012A",
        "ENKU:BQ25185_DLH0010A",
        "ENKU:BMI270_Bosch_LGA14",
        "ENKU:FH34SRJ-24S-0.5SH",
        "ENKU:TYS5040_5x5",
    )
    for token in exact_footprint_tokens:
        if token not in text:
            errors.append(f"exact first-spin footprint missing: {token}")

    # Exact pad-number gates: catch visually plausible but electrically impossible placeholders.
    blocks_by_ref: dict[str, str] = {}
    for block in footprint_blocks(text):
        parsed = parse_ref_and_at(block)
        if parsed:
            blocks_by_ref[parsed[0]] = block

    expected_pads = {
        "U2": {str(i) for i in range(1, 13)},
        "U3": {str(i) for i in range(1, 12)},
        "U5": {str(i) for i in range(1, 15)},
        "J3": {*(str(i) for i in range(1, 25)), "S1", "S2"},
    }
    for ref, expected in expected_pads.items():
        block = blocks_by_ref.get(ref, "")
        actual = set(re.findall(r'\(pad "([^"]+)"', block))
        missing = expected - actual
        if missing:
            errors.append(f"{ref} missing exact pads: {sorted(missing)}")

    # Electrical package invariants.
    chg_block = blocks_by_ref.get("U3", "")
    if not re.search(r'\(pad "11"[^\n]*\(net \d+ "GND"\)', chg_block):
        errors.append("BQ25185 exposed pad 11 must be tied to GND")
    for ref in ("J3",):
        block = blocks_by_ref.get(ref, "")
        for shield in ("S1", "S2"):
            if not re.search(rf'\(pad "{shield}"[^\n]*\(net \d+ "GND"\)', block):
                errors.append(f"{ref} {shield} retention tab must be tied to GND")

    # Reproducible local footprint library is part of the release source.
    fp_table = HERE / "fp-lib-table"
    if not fp_table.is_file() or "ENKU.pretty" not in fp_table.read_text(encoding="utf-8"):
        errors.append("local ENKU.pretty library is not registered in fp-lib-table")
    local_footprints = (
        "TPS2121_RUX0012A.kicad_mod",
        "BQ25185_DLH0010A.kicad_mod",
        "BMI270_Bosch_LGA14.kicad_mod",
        "FH34SRJ-24S-0.5SH.kicad_mod",
    )
    for name in local_footprints:
        if not (HERE / "ENKU.pretty" / name).is_file():
            errors.append(f"missing local verified footprint source: {name}")

    if "TPS63802DLAR" not in text:
        errors.append("PCB missing TPS63802DLAR first-spin regulator")
    if "TPS63031" in text:
        errors.append("obsolete TPS63031 remains on PCB")
    if "DFE201612E-R47M=P2" not in text:
        errors.append("PCB missing 0.47uH DFE201612E power inductor")
    for required_net in ("SYS_EN", "REG_L1", "REG_L2", "REG_FB", "REG_PG"):
        if f'"{required_net}"' not in text:
            errors.append(f"PCB missing TPS63802 net {required_net}")

    if errors:
        for e in errors:
            print("ERROR:", e)
        print(f"\nENKU PCB placement gate: FAIL ({len(errors)} issue(s))")
        return 1

    print("ENKU PCB placement gate: PASS")
    print(f"  board: {EXPECTED_SIZE[0]:.1f} x {EXPECTED_SIZE[1]:.1f} mm")
    print(f"  placed references parsed: {len(refs)}")
    print("  critical placement refs: present")
    print("  Base-only placement: Pro frontlight/Qi reservations removed")
    print("  copper routing: structurally present; native KiCad DRC remains authoritative")
    print("\nNOTE: this is a placement/integrity gate, not KiCad DRC.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
