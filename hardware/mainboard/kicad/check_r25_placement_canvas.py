#!/usr/bin/env python3
"""R25 placement-first scaffold checks. NOT a fabrication release gate.

The R25 PCB is deliberately unrouted and must NEVER be substituted
for the routed R0.1 design or offered to PCBWay.
"""
from __future__ import annotations
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE/"enku-mainboard-r0.1.kicad_pcb"
NEW=HERE/"enku-mainboard-r0.2-placement.kicad_pcb"

def ref_data(board: str) -> dict[str,tuple]:
    # The existing PCB has one origin for each footprint before Reference.
    pat=r'\(footprint "([^"]+)"\s+\(layer "([FB])\.Cu"\)\s+\(at ([\d.]+) ([\d.]+)(?: ([\d.]+))?\)[\s\S]*?\(property "Reference" "([^"]+)"'
    out={}
    for m in re.finditer(pat,board):
        lib,side,x,y,angle,ref=m.groups()
        if ref in out:
            raise AssertionError(f"Duplicate {ref}")
        out[ref]=(lib,side,float(x),float(y),float(angle or 0))
    return out

def main():
    source=OLD.read_text(encoding="utf-8")
    cand=NEW.read_text(encoding="utf-8")
    a,b=ref_data(source),ref_data(cand)
    assert len(a)==len(b)==122 and set(a)==set(b), "Footprints lost or duplicated"
    assert cand.count('(gr_rect (start 18 20) (end 77 121)')==1
    for category in ("segment","via","zone"):
        assert re.search(r'(?m)^  \('+category+r'\b',cand) is None, category
    allowed={"J2":(26.1,100.7,270.0),"J5":(47.0,117.325,0.0)}
    for ref in a:
        assert a[ref][0:2]==b[ref][0:2],ref+" part package changed"
        if ref in allowed:
            assert b[ref][2:]==allowed[ref],ref+" provisional target moved"
        else:
            assert a[ref]==b[ref],ref+" changed without mechanical review"
    assert 'PLACEMENT STUDY - NO ROUTING' in cand
    print("R25 placement study gate: PASS")
    print("PCB: 59x101 mm; 122 footprints conserved; 717 tracks + 217 vias + 2 zones stripped from independent copy")
    print("Moved: J2 left-mouth provisional 270deg; J5 7mm toward new lower edge")
    print("NOT PRODUCTION: provisional SW3-SW6, battery, mounts, FPC, antenna, supplier footprint/CAD validation")
if __name__=="__main__":
    main()
