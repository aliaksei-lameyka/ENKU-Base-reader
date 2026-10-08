#!/usr/bin/env python3
"""Check R26 trial geometry with manufacturer drawing-derived lateral datum.

Geometric engineering trial only: flattened tongue DOES NOT certify folded FPC.
The true production release fails until supplier bend, stiffener, contact side,
display stack and M2 attachment are proven in 3D and PCBWay assembly review.
"""
from __future__ import annotations
import math
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=(HERE/"enku-mainboard-r0.2-placement.kicad_pcb").read_text(encoding="utf-8")
NEW=(HERE/"enku-mainboard-r0.3-fpc-trial.kicad_pcb").read_text(encoding="utf-8")

def positions(s):
    match=list(re.finditer(r'\(footprint "([^"]+)"\s+\(layer "([FB])\.Cu"\)\s+\(at ([\d.]+) ([\d.]+)(?: ([\d.]+))?\)',s))
    result={}
    for i,m in enumerate(match):
        b=s[m.start():match[i+1].start() if i+1<len(match) else len(s)]
        z=re.search(r'\(property "Reference" "([^"]+)"',b)
        if z:
            ref=z[1]
            assert ref not in result
            result[ref]=(m[1],m[2],float(m[3]),float(m[4]),float(m[5] or 0))
    return result

def overlap(r1,r2):
    return not (r1[2]<r2[0] or r2[2]<r1[0] or r1[3]<r2[1] or r2[3]<r1[1])

def main():
    a,b=positions(OLD),positions(NEW)
    assert len(a)==len(b)==122 and set(a)==set(b)
    moved={"J3":(69.37,34.,0.),"H2":(57.5,25.,0.),"C28":(55.2,34.,90.)}
    for ref in a:
        assert a[ref][:2]==b[ref][:2],ref
        if ref in moved:
            assert b[ref][2:]==moved[ref],ref
        else: assert a[ref]==b[ref],ref+" unintended component movement"
    for name in ("segment","via","zone"):
        assert not re.search(r'(?m)^  \('+name+r'\b',NEW),name
    assert NEW.count('(gr_rect (start 18 20) (end 77 121)')==1
    j3=(69.37-7.25,34.-2.25,69.37+7.25,34.+2.05)
    assert j3[2] < 77,("J3 courtyard outside PCB",j3)
    # C28 is a rotated 0805: an intentionally conservative bbox ±1.5mm.
    c28=(55.2-1.5,34.-1.5,55.2+1.5,34.+1.5)
    assert not overlap(j3,c28),"C28 collider next to connector"
    old_h2=(72.,25.)
    h2=(57.5,25.)
    def radial_clearance(x,y,rect):
        return math.hypot(max(rect[0]-x,0,x-rect[2]),max(rect[1]-y,0,y-rect[3]))
    assert radial_clearance(*old_h2,(62.12,25.75,76.62,30.05)) < 2.75+.65
    assert radial_clearance(*h2,j3)>2.75+.65
    assert (75.62-12.50/2)==69.37
    assert '(gr_rect (start 63.12 -11.47) (end 75.62 22.19)' in NEW
    print("R26 flat FPC case: PASS 122 footprints, no copper, source GDEY pp5 12.50/33.66")
    print("R26 trial: J3=(69.37,34), H2=(57.5,25), C28=(55.2,34), no 2D J3/H2 courtyard clash")
    print("GATES BLOCKED: actual shaped-flex envelope, FPC 180 fold, contact/stiffener, H2 screw load, pin15/16 supplies")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
