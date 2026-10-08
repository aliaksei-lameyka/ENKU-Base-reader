#!/usr/bin/env python3
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
PCB_PATH = BASE / "enku-mainboard-r0.1.kicad_pcb"
LIB_DIR = BASE / "ENKU.pretty"

SPECS = {
    "U2": ("power.kicad_sch", "TPS2121_RUX0012A", {str(i) for i in range(1, 13)}),
    "U3": ("power.kicad_sch", "BQ25185_DLH0010A", {str(i) for i in range(1, 12)}),
    "U4": ("power.kicad_sch", "TPS63802_DLA0010A", {str(i) for i in range(1, 11)}),
    "L1": ("power.kicad_sch", "Murata_DFE201612E", {"1", "2"}),
    "U5": ("mcu_io.kicad_sch", "BMI270_Bosch_LGA14", {str(i) for i in range(1, 15)}),
    "J3": ("epd_hv.kicad_sch", "FH34SRJ-24S-0.5SH", {*(str(i) for i in range(1, 25)), "S1", "S2"}),
    "L2": ("epd_hv.kicad_sch", "TYS5040_5x5", {"1", "2"}),
    "J6": ("connectors.kicad_sch", "DOCK_POGO_4", {"1", "2", "3", "4"}),
    "SW3": ("mcu_io.kicad_sch", "GT_TC035A_H0195_L3_C915811_EVAL", {"1", "2", "3", "4"}),
    "SW4": ("mcu_io.kicad_sch", "GT_TC035A_H0195_L3_C915811_EVAL", {"1", "2", "3", "4"}),
    "SW5": ("mcu_io.kicad_sch", "GT_TC035A_H0195_L3_C915811_EVAL", {"1", "2", "3", "4"}),
    "SW6": ("mcu_io.kicad_sch", "GT_TC035A_H0195_L3_C915811_EVAL", {"1", "2", "3", "4"}),
}

ALLOWED_PROVISIONAL_PLACEHOLDERS = {
    "J1",
    "SW1",
}


def sexpr_end(text: str, start: int) -> int:
    depth = 0
    in_string = False
    escaped = False
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
                return i + 1
    raise ValueError(f"unbalanced S-expression at offset {start}")


def balanced(text: str) -> bool:
    try:
        pos = 0
        while True:
            pos = text.find("(", pos)
            if pos < 0:
                return True
            end = sexpr_end(text, pos)
            if end <= pos:
                return False
            pos = end
    except ValueError:
        return False


def pcb_footprint_block(text: str, ref: str) -> str:
    marker = f'(property "Reference" "{ref}"'
    m = text.find(marker)
    if m < 0:
        raise ValueError(f"PCB missing reference {ref}")
    start = text.rfind("(footprint ", 0, m)
    if start < 0:
        raise ValueError(f"PCB cannot locate footprint start for {ref}")
    return text[start:sexpr_end(text, start)]


def pad_numbers(text: str) -> set[str]:
    return {
        m.group(1)
        for m in re.finditer(r'\(pad\s+"?([^"\s()]+)"?', text)
        if m.group(1)
    }


def schematic_footprint(sheet_text: str, ref: str) -> str:
    marker = f'(property "Reference" "{ref}"'
    m = sheet_text.find(marker)
    if m < 0:
        raise ValueError(f"schematic missing reference {ref}")
    tail = sheet_text[m : m + 2200]
    fm = re.search(r'\(property "Footprint" "([^"]+)"', tail)
    if not fm:
        raise ValueError(f"schematic {ref} has no Footprint property")
    return fm.group(1)


def all_pcb_footprints(text: str):
    pos = 0
    while True:
        start = text.find("(footprint ", pos)
        if start < 0:
            return
        end = sexpr_end(text, start)
        block = text[start:end]
        name_m = re.match(r'\(footprint "([^"]+)"', block)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block)
        yield (ref_m.group(1) if ref_m else "?", name_m.group(1) if name_m else "?", block)
        pos = end


def main() -> int:
    errors: list[str] = []

    if not PCB_PATH.exists():
        print(f"ERROR: missing {PCB_PATH}")
        return 1
    pcb = PCB_PATH.read_text(encoding="utf-8")
    if not balanced(pcb):
        errors.append("PCB S-expression is not balanced")

    sheets = {}
    for sheet, _, _ in SPECS.values():
        if sheet not in sheets:
            p = BASE / sheet
            if not p.exists():
                errors.append(f"missing schematic sheet {sheet}")
                sheets[sheet] = ""
            else:
                sheets[sheet] = p.read_text(encoding="utf-8")

    # Every project-local ENKU footprint referenced by a schematic must exist.
    for sheet_name, sheet_text in sheets.items():
        for fp in sorted(set(re.findall(r'\(property "Footprint" "ENKU:([^"]+)"', sheet_text))):
            if not (LIB_DIR / f"{fp}.kicad_mod").exists():
                errors.append(f"{sheet_name}: ENKU footprint has no local file: {fp}.kicad_mod")

    for ref, (sheet_name, fp_name, expected_pads) in SPECS.items():
        local_path = LIB_DIR / f"{fp_name}.kicad_mod"
        if not local_path.exists():
            errors.append(f"{ref}: missing local footprint {local_path.name}")
            continue

        local = local_path.read_text(encoding="utf-8")
        if not balanced(local):
            errors.append(f"{ref}: local footprint {local_path.name} has unbalanced S-expression")

        try:
            sch_fp = schematic_footprint(sheets[sheet_name], ref)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        expected_link = f"ENKU:{fp_name}"
        if sch_fp != expected_link:
            errors.append(f"{ref}: schematic footprint is {sch_fp}, expected {expected_link}")

        try:
            pcb_block = pcb_footprint_block(pcb, ref)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        name_m = re.match(r'\(footprint "([^"]+)"', pcb_block)
        pcb_link = name_m.group(1) if name_m else ""
        if pcb_link != expected_link:
            errors.append(f"{ref}: PCB footprint is {pcb_link}, expected {expected_link}")

        local_pads = pad_numbers(local)
        pcb_pads = pad_numbers(pcb_block)
        if local_pads != expected_pads:
            errors.append(
                f"{ref}: local footprint pad set {sorted(local_pads)} != expected {sorted(expected_pads)}"
            )
        if pcb_pads != expected_pads:
            errors.append(
                f"{ref}: PCB pad set {sorted(pcb_pads)} != expected {sorted(expected_pads)}"
            )
        if local_pads != pcb_pads:
            errors.append(f"{ref}: local footprint and embedded PCB pad-number sets differ")

    # Resolved parts may never silently regress to placement-only geometry.
    for ref, name, _ in all_pcb_footprints(pcb):
        if re.search(r"PLACEHOLDER|PLACEMENT", name, re.IGNORECASE):
            if ref not in ALLOWED_PROVISIONAL_PLACEHOLDERS:
                errors.append(f"{ref}: unexpected fabrication-path placeholder {name}")

    # The remaining provisional mechanics must stay explicit until exact MPNs are selected.
    seen_provisional = {
        ref
        for ref, name, _ in all_pcb_footprints(pcb)
        if re.search(r"PLACEHOLDER|PLACEMENT", name, re.IGNORECASE)
    }
    missing_provisional_markers = ALLOWED_PROVISIONAL_PLACEHOLDERS - seen_provisional
    if missing_provisional_markers:
        errors.append(
            "mechanical blockers changed without updating this gate: "
            + ", ".join(sorted(missing_provisional_markers))
        )

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        print(f"ENKU footprint consistency gate: FAIL ({len(errors)} issue(s))")
        return 1

    print("ENKU footprint consistency gate: PASS")
    print(f"Verified {len(SPECS)} schematic/local-library/PCB bindings.")
    print(
        "Intentional unresolved mechanics: "
        + ", ".join(sorted(ALLOWED_PROVISIONAL_PLACEHOLDERS))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
