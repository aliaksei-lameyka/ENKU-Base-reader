#!/usr/bin/env python3
"""Classify native KiCad library mismatch: pad geometry vs annotations.

Diagnostic not a manufacturer footprint qualification. A footprint is not
approved merely because its pads numerically match a KiCad stock library.
Check exact vendor drawing, row orientation, contacts, shell tabs, soldermask.
Runs inside KiCad8 container with pcbnew.
"""
import collections
import json
from pathlib import Path
import pcbnew

ROOT=Path(__file__).resolve().parent
PCB=ROOT/"enku-mainboard-r0.1.kicad_pcb"
OUTPUT=Path("/tmp/r29-footprint-pad-audit.json")
SYSTEM=Path("/usr/share/kicad/footprints")
LOCAL=ROOT/"ENKU.pretty"

def pad_descriptor(p):
    position=p.GetFPRelativePosition()
    size=p.GetSize()
    drill=p.GetDrillSize()
    return (
        p.GetNumber(),
        int(position.x),int(position.y),
        int(size.x),int(size.y),
        int(drill.x),int(drill.y),
        int(p.GetShape()),int(p.GetAttribute())
    )

def signature(fp):
    return sorted([pad_descriptor(p) for p in fp.Pads()])

def main():
    board=pcbnew.LoadBoard(str(PCB))
    results=[]
    for fp in board.GetFootprints():
        id=fp.GetFPID()
        nick=str(id.GetLibNickname())
        name=str(id.GetLibItemName())
        ref=fp.GetReference()
        if not nick or not name:
            results.append({"reference":ref,"library":str(id),"status":"missing_id"})
            continue
        loc=LOCAL if nick=="ENKU" else SYSTEM/(nick+".pretty")
        if not loc.is_dir():
            results.append({"reference":ref,"library":nick+":"+name,"status":"library_absent"})
            continue
        try:
            source=pcbnew.FootprintLoad(str(loc),name)
            if source is None:
                results.append({"reference":ref,"library":nick+":"+name,"status":"source_absent"})
                continue
            a,b=signature(fp),signature(source)
            if a==b:
                status="pads_match"
            else:
                status="pads_differ"
            results.append({"reference":ref,"library":nick+":"+name,
                            "status":status,
                            "placed_pad_count":len(a),"reference_pad_count":len(b),
                            "pad_numbers_current":sorted({x[0] for x in a}),
                            "pad_numbers_library":sorted({x[0] for x in b})})
        except Exception as ex:
            results.append({"reference":ref,"library":nick+":"+name,
                            "status":"compare_error","error":str(ex)})
    OUTPUT.write_text(json.dumps(results,indent=2))
    counts=collections.Counter(x["status"] for x in results)
    print("FOOTPRINT PAD AUDIT",dict(sorted(counts.items())))
    for x in results:
        if x["status"]!="pads_match":
            print("PADS_TO_REVIEW",x["reference"],x["library"],x["status"],
                  "current",x.get("placed_pad_count"),"vendorlib",x.get("reference_pad_count"),
                  x.get("error",""))
    print("Report",OUTPUT)
    print("WARNING: custom ENKU footprints remain unqualified until manufacturer drawing/3D alignment.")
if __name__=="__main__":
    main()
