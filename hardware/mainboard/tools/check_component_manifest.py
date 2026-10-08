#!/usr/bin/env python3
"""Audit every ENKU Reader PCB footprint against a vendor-qualification manifest.

Normal CI enforces data integrity, not fabrication fitness.
--release fails until every purchasable component is vendor/PCBWay-qualified.
"""
from __future__ import annotations
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"kicad"))
from check_pcb_placement import footprint_blocks,parse_ref_and_at
PCB=ROOT/"kicad/enku-mainboard-r0.1.kicad_pcb"
MANIFEST=ROOT/"procurement/COMPONENT_AUDIT_R24.csv"
FIELDS="ref value footprint side x_mm y_mm rotation_deg manufacturer mpn_candidate preferred_source manufacturer_drawing status footprint_checked pinout_checked orientation_checked cad_checked pcbway_sourcing_confirmed review_note".split()
GATES="footprint_checked pinout_checked orientation_checked cad_checked pcbway_sourcing_confirmed".split()
STATES={"IDENTIFIED","UNSELECTED","PCB_FEATURE","PLACEHOLDER","QUALIFIED"}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release",action="store_true")
    args=parser.parse_args()
    actual={}
    for block in footprint_blocks(PCB.read_text(encoding="utf-8")):
        parsed=parse_ref_and_at(block)
        if not parsed:continue
        ref,x,y,rot=parsed
        import re
        shape=re.match(r'\(footprint "([^"]+)" \(layer "(F|B)\.Cu"\)',block)
        if not shape:raise ValueError(f"{ref}: no footprint/side")
        if ref in actual:raise ValueError(f"Duplicate PCB footprint: {ref}")
        actual[ref]=(shape[1],shape[2],x,y,rot)
    with MANIFEST.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if reader.fieldnames!=FIELDS:raise ValueError("CSV columns do not match versioned template")
        rows=list(reader)
    seen=Counter(row["ref"] for row in rows)
    errors=[]
    for ref in actual:
        if seen[ref]!=1:errors.append(f"{ref} requires exactly one BOM review row")
    for ref in seen:
        if ref not in actual:errors.append(f"{ref} not on board")
    counts=Counter();pending=0
    for row in rows:
        ref=row["ref"]
        if ref not in actual:continue
        fp,side,x,y,rot=actual[ref]
        if (fp,side)!=(row["footprint"],row["side"]):
            errors.append(f"{ref}: footprint or side changed")
        try:
            xyz=[float(row[k]) for k in ("x_mm","y_mm","rotation_deg")]
            if any(abs(a-b)>0.02 for a,b in zip(xyz,(x,y,rot))):
                errors.append(f"{ref}: position/rotation changed; reconfirm part geometry")
        except (TypeError,ValueError):
            errors.append(f"{ref}: invalid placement coordinates")
        state=row["status"];counts[state]+=1
        if state not in STATES:errors.append(f"{ref}: invalid status {state}")
        if state!="PCB_FEATURE" and state!="QUALIFIED":pending+=1
        if state=="QUALIFIED":
            if not row["mpn_candidate"] or any(row[k]!="YES" for k in GATES):
                errors.append(f"{ref}: cannot qualify without MPN, pinout, CAD and PCBWay evidence")
        if "PLACEMENT" in fp and state=="QUALIFIED":
            errors.append(f"{ref}: cannot qualify schematic footprint placeholder")
        if state=="PCB_FEATURE" and row["pcbway_sourcing_confirmed"]=="YES":
            errors.append(f"{ref}: a hole/testpad is not an SMT part to procure")
    print(f"ENKU provenance audit: {len(actual)} actual PCB footprints, {len(rows)} manifest entries")
    for state,n in sorted(counts.items()):print(f"{state}: {n}")
    print(f"Remaining not qualified: {pending}")
    for err in errors:print("ERROR:",err)
    if args.release and (errors or pending):
        print("PCBWAY HANDOFF BLOCKED: supplier/datasheet/footprint/pinout/rotation/3D not all approved")
    if errors or (args.release and pending):return 1
    print("Provenance register integrity: PASS (not a manufacturing approval)")
    return 0
if __name__=="__main__":raise SystemExit(main())
