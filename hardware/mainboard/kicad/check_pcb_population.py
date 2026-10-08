#!/usr/bin/env python3
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
# Select the newest active Base experiment if present. Historical R29 remains a
# fallback for old branches only; comparing live schematics to the R29 PCB would
# incorrectly report newly added power-domain parts as unplaced.
CURRENT = BASE / "enku-mainboard-r1.3-base-first-power-copper.kicad_pcb"
LEGACY = BASE / "enku-mainboard-r0.6-base-placement.kicad_pcb"
PCB = CURRENT if CURRENT.is_file() else LEGACY
SHEETS = (
    "power.kicad_sch",
    "mcu_io.kicad_sch",
    "epd_hv.kicad_sch",
    "connectors.kicad_sch",
)

# Placement debt discovered before routing on 2026-10-03.
# This is a ceiling, not an acceptance list: refs may disappear from this set only by
# being placed on PCB. Any NEW missing ref is an immediate CI failure.
KNOWN_UNPLACED = {
    "C22","C23","C27","C28","C29","C30",
    "C21","C8","C5","C6","C36","C3","C15",
    "C14","C18","C19","C4",
    "C1","C16","C17","C2","C35","J7",
    "R27","R26","R62","R63","R10","R8","R9",
    "R4","R5","R69","R68","R29","R32",
    "R35","R31","R34","R30","R36","R33",
    "R28",
    "R25","R24","R1","R6","R7","R3",
    "R2","R19","R23","R22","R20","R21","R11",
    "R12","R13","R65","R64","R66","R67",
    "SW2",
}


def schematic_refs() -> set[str]:
    refs: set[str] = set()
    for sheet in SHEETS:
        text = (BASE / sheet).read_text(encoding="utf-8")
        refs.update(
            r for r in re.findall(r'\(reference "([^"]+)"\)', text)
            if r and not r.startswith("#")
        )
    return refs


def pcb_refs() -> set[str]:
    text = PCB.read_text(encoding="utf-8")
    return {
        r for r in re.findall(r'\(property "Reference" "([^"]+)"', text)
        if r and r != "REF**"
    }


def main() -> int:
    sch = schematic_refs()
    pcb = pcb_refs()
    if PCB == CURRENT and len(pcb) != 125:
        print("ERROR: R36 expected 125 KiCad footprints including four board-only M2 mounting holes, got",len(pcb))
        return 1
    missing = sch - pcb
    unexpected = missing - KNOWN_UNPLACED
    retired = KNOWN_UNPLACED - missing

    errors: list[str] = []
    if unexpected:
        errors.append(
            "new schematic refs missing from PCB: " + ", ".join(sorted(unexpected))
        )

    # Mounting holes are board-only mechanics and are intentionally not schematic refs.
    board_only = pcb - sch - {"H1", "H2", "H3", "H4"}
    if board_only:
        errors.append(
            "unexpected PCB-only references: " + ", ".join(sorted(board_only))
        )

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        print(f"ENKU PCB population gate: FAIL ({len(errors)} issue(s))")
        return 1

    print("ENKU PCB population gate: PASS")
    print("PCB source:",PCB.name)
    print(f"Schematic refs: {len(sch)}")
    print(f"PCB refs: {len(pcb)}")
    print(f"Known refs still awaiting placement: {len(missing)}")
    if missing:
        print("UNPLACED: " + ", ".join(sorted(missing)))
    if retired:
        print(f"Placement progress since baseline: {len(retired)} ref(s)")
        print("PLACED_FROM_DEBT: " + ", ".join(sorted(retired)))
    if not missing:
        print("PCB population complete: zero schematic refs missing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
