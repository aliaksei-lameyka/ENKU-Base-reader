#!/usr/bin/env python3
"""ENKU mechanical release audit of physical PCB placements.

Reads the actual KiCad PCB. Default mode lists manufacturing blockers while
allowing exploratory electrical CI to continue; --release exits nonzero if
the design has unresolved mechanical fabrication blockers.

Does NOT replace a fitted 3D CAD stackup, manufacturer drawings or native DRC.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
KICAD = BASE / "kicad"
sys.path.insert(0, str(KICAD))
from check_pcb_placement import footprint_blocks, parse_ref_and_at  # noqa: E402

PCB = KICAD / "enku-mainboard-r0.1.kicad_pcb"
BOARD = (18.0, 20.0, 77.0, 121.0)
DISPLAY_PORTRAIT = (56.24, 96.62)
USB_EDGE_OFFSET = 3.675
BUTTON_BODY_HALF_WIDTH = 1.9   # placeholder FP rectangle; NOT an actuator dimension
SIDE_BUTTON_CANDIDATE = "GT-TC035A-H0195-L3"
SIDE_BUTTON_LCSC_CODE = "C915811"
# R22 bodies are documentation on Dwgs.User only. No manufacturer land-pattern claim.
CANDIDATE_BODIES = (
    "(gr_rect (start 18.30 61.60) (end 20.95 64.40)",
    "(gr_rect (start 18.30 73.60) (end 20.95 76.40)",
    "(gr_rect (start 74.05 61.60) (end 76.70 64.40)",
    "(gr_rect (start 74.05 73.60) (end 76.70 76.40)",
)

def inventory(source: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for block in footprint_blocks(source):
        parsed = parse_ref_and_at(block)
        if not parsed:
            continue
        ref, x, y, angle = parsed
        label = block.split('"', 2)[1]
        result[ref] = dict(x=x, y=y, angle=angle, footprint=label)
    return result

def audit(pcb: str) -> tuple[dict, list[str], list[str]]:
    found = inventory(pcb)
    blockers: list[str] = []
    manual: list[str] = []
    x0, y0, x1, y1 = BOARD
    outline = f"(gr_rect (start {x0:g} {y0:g}) (end {x1:g} {y1:g})"
    if outline not in pcb:
        blockers.append("Unrecognized Edge.Cuts: mechanical audit cannot establish board outline")

    if any(pcb.count(body) != 1 for body in CANDIDATE_BODIES):
        blockers.append("R22 side-switch concept not symmetric: expected four documented miniature body envelopes")
    if ("R22 EDGE-BUTTON STUDY ONLY - C915811 - NOT A LAND PATTERN" not in pcb):
        blockers.append("No R22 side-button candidate annotation; confirm source mechanical study")
    for ref in ("SW3", "SW4", "SW5", "SW6"):
        if ref not in found:
            blockers.append(f"{ref}: missing side-button footprint")
            continue
        item = found[ref]
        if "PLACEMENT" in item["footprint"]:
            edge = x0 if ref in ("SW3", "SW4") else x1
            gap = ((item["x"] - BUTTON_BODY_HALF_WIDTH) - edge
                   if ref in ("SW3", "SW4") else
                   edge - (item["x"] + BUTTON_BODY_HALF_WIDTH))
            blockers.append(f"{ref}: placeholder side switch; approximate body-to-edge gap {gap:.2f} mm, "
                            "actuator direction/travel not verifiable")
    if all(r in found for r in ("SW3", "SW4", "SW5", "SW6")):
        angles = [found[r]["angle"] for r in ("SW3", "SW4", "SW5", "SW6")]
        if angles.count(angles[0]) == 4:
            manual.append("All four button footprints share the same nominal rotation; "
                          "outward-facing left/right actuator orientations are NOT demonstrated")

    if "J5" not in found:
        blockers.append("J5 USB-C missing")
    else:
        u = found["J5"]
        if abs(u["angle"]) > 0.01:
            blockers.append("J5 rotated; USB exit direction is unverified")
        else:
            nominal_port_edge = u["y"] + USB_EDGE_OFFSET
            recess = y1 - nominal_port_edge
            if abs(recess) > 1.0:
                blockers.append(f"J5 USB-C datum is {recess:.2f} mm behind the lower board edge; "
                                "relocate and reroute connector OR engineer a verified Edge.Cuts opening")

    midx, midy = ((x0 + x1)/2, (y0 + y1)/2)
    dw, dh = DISPLAY_PORTRAIT
    display_rect = (midx-dw/2, midy-dh/2, midx+dw/2, midy+dh/2)
    overlapping_holes = []
    for ref in ("H1", "H2", "H3", "H4"):
        if ref not in found:
            blockers.append(f"{ref}: mount hole missing")
            continue
        x, y = found[ref]["x"], found[ref]["y"]
        if display_rect[0] <= x <= display_rect[2] and display_rect[1] <= y <= display_rect[3]:
            overlapping_holes.append(ref)
    if overlapping_holes:
        blockers.append("Under a nominal CENTERED portrait display registration, mounting holes "
                        + ", ".join(overlapping_holes) + " lie within the display MODULE projection. "
                        "Independent structural load path + full FPC/screen 3D overlay required.")
    if "J2" in found:
        sd = found["J2"]
        # In this exact Hirose socket, the pads/terminal row is at local Y=-7.725,
        # while the microSD entry mouth is opposite at local Y approximately +8.125.
        # KiCad +90° rotation maps local +Y toward global +X, so the card enters
        # from the interior of the board, NOT from the exterior left edge.
        if "MICROSD_DM3AT_ENKU" in sd["footprint"] and abs(sd["angle"]-90.0) < 0.1:
            slot_x = sd["x"] + 8.125
            blockers.append(f"J2 Hirose microSD: rotation 90 degrees projects card mouth toward "
                            f"+X, approximately x={slot_x:.2f} mm, i.e. toward BOARD INTERIOR "
                            f"rather than the left edge x={x0:.1f}; rotate/replace and reroute "
                            "the full SD breakout after validating official Hirose drawing.")
    manual.append("Centered display overlay is a conservative hypothesis; actual registered FPC "
                  "fold, backing, glass and allowed support perimeter remain unverified.")

    if "J1" in found and "PLACEMENT" in found["J1"]["footprint"]:
        blockers.append("J1 3-pin LiPo/NTC socket is a generic placeholder, NOT an orderable JST footprint")
    if "SW1" in found and "PLACEMENT" in found["SW1"]["footprint"]:
        blockers.append("SW1 hard-power slide switch is a placeholder, NOT a selected part; "
                        "candidate G-Switch MK-12C03-G015 C2890358 is 3-pin SPDT, 500mA "
                        "and must be qualified for the actual LiPo disconnect load")
    manual += [
        "J2 microSD: after correcting entrance direction, recheck push-push ejection stroke and housing entry cutout with official Hirose STEP.",
        "J3 24p FPC: contact side, insertion vector, bend radius and display-to-PCB origin unapproved.",
        "J6 dock: 4 contact pads on rear PCB; no qualified pogo-mating hardware / magnet stack.",
        "U1 ESP32-S3: antenna metal/copper clearance must be checked in the assembled shell.",
        "LiPo: protected cell size, NTC pinout, pouch swelling and 10-mm enclosure thickness unapproved.",
        "L2 5x5 mm inductor and cable/connector Z heights require a mechanical tolerance stack.",
        "C915811 G-Switch recessed mount: supplier drawing/pad pinout/STEP and PCBWay edge milling constraints NOT certified.",
    ]
    return found, blockers, manual

def main() -> int:
    arg = argparse.ArgumentParser(description=__doc__)
    arg.add_argument("--release", action="store_true", help="enforce physical manufacturing release")
    arg.add_argument("--json", type=Path, help="optional machine-readable artifact")
    opts = arg.parse_args()
    if not PCB.is_file():
        print("MISSING PCB", file=sys.stderr)
        return 2
    found, blockers, manual = audit(PCB.read_text(encoding="utf-8"))
    print(f"ENKU physical placement audit: {len(found)} footprints; "
          f"{len(blockers)} manufacturing blockers; {len(manual)} manual CAD gates")
    for item in blockers: print("BLOCKER:", item)
    for item in manual: print("REVIEW:", item)
    print("Manufacturing release:", "BLOCKED" if blockers or manual else "CANDIDATE")
    if opts.json:
        opts.json.parent.mkdir(parents=True, exist_ok=True)
        opts.json.write_text(json.dumps({"board_mm":[59,101],
                           "footprints":len(found),"blockers":blockers,"manual_checks":manual,
                           "release_ready":not blockers and not manual},indent=2)+"\n")
    if opts.release and (blockers or manual):
        print("RELEASE GATE FAILED: still requires resolved CAD and manufacturer checks")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
