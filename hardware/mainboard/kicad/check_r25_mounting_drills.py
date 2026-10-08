#!/usr/bin/env python3
"""R25 hole registry and mechanical envelope gate — not manufacturing approval.

Validates native drill footprint coordinates, rear-screw-head exclusion envelope,
critical connector courtyards, and user-visible drill registry. Does not prove
3D screw stackup, e-paper glass clearance, or enclosure stability.
"""
from __future__ import annotations
import math
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PCB=ROOT/"kicad/enku-mainboard-r0.2-placement.kicad_pcb"
HOLES={"H1":(23.0,25.0),"H2":(72.0,25.0),
       "H3":(23.0,116.5),"H4":(72.0,116.5)}
BOARD=(18.0,20.0,77.0,121.0)
# 5.5mm study envelope for rear screw head / mechanical boss, not a vendor spec.
BOSS_RADIUS=2.75
ASSEMBLY_GAP=0.65
DISPLAY=(19.38,22.19,75.62,118.81)
# Manufacturer-footprint local courtyards; R25 test placement from PCB source.
# All are F.Cu. For x/y see COMPONENT_VISUAL_CATALOG_R20 and actual PCB.
CRITICAL={
  "J2":(26.1,100.7,270,(-7.82,-8.82,7.88,8.88)),
  "J3":(58.0,28.0,0,(-7.25,-2.25,7.25,2.05)),
  "J5":(47.0,117.325,0,(-5.32,-4.76,5.32,4.18)),
  "SW1":(30.5,29.0,0,(-4.5,-1.5,4.5,1.5))
}
def fp_block(src:str,ref:str)->str:
    pos=src.find('(property "Reference" "'+ref+'"')
    if pos<0:raise AssertionError("missing physical reference "+ref)
    left=src.rfind('(footprint ',0,pos)
    if left<0:raise AssertionError("invalid footprint block "+ref)
    return src[left:pos]
def between_rect_and_circle(x:float,y:float,rect:tuple)->float:
    x0,y0,x1,y1=rect
    return math.hypot(max(x0-x,0,x-x1),max(y0-y,0,y-y1))
def transformed_rect(cx,cy,ang,rect):
    x0,y0,x1,y1=rect
    a=math.radians(ang)
    # KiCad +90 local Y projects toward board +X.
    pts=[(cx+xx*math.cos(a)+yy*math.sin(a),
          cy-xx*math.sin(a)+yy*math.cos(a))
         for xx,yy in ((x0,y0),(x0,y1),(x1,y0),(x1,y1))]
    return min(v[0] for v in pts),min(v[1] for v in pts),max(v[0] for v in pts),max(v[1] for v in pts)
def main():
    pcb=PCB.read_text(encoding="utf-8")
    assert pcb.count('(gr_rect (start 18 20) (end 77 121)')==1
    assert pcb.count('(gr_rect (start 19.38 22.19) (end 75.62 118.81)')==1
    for ref,(x,y) in HOLES.items():
        block=fp_block(pcb,ref)
        assert 'MountingHole:MountingHole_2.2mm_M2' in block,ref
        found=re.search(r'\(at ([\d.]+) ([\d.]+)\)',block)
        assert found and (float(found[1]),float(found[2]))==(x,y),ref
        assert 'np_thru_hole circle (at 0 0) (size 2.2 2.2) (drill 2.2)' in block + pcb[pcb.find('(property "Reference" "'+ref+'"'):pcb.find('(property "Reference" "'+ref+'"')+450],ref
        dist=min(x-BOARD[0],BOARD[2]-x,y-BOARD[1],BOARD[3]-y)
        assert dist>BOSS_RADIUS+1.0,(ref,"boss too close to board edge",dist)
        assert DISPLAY[0]<x<DISPLAY[2] and DISPLAY[1]<y<DISPLAY[3],ref
        for name,(cx,cy,angle,courtyard) in CRITICAL.items():
            rect=transformed_rect(cx,cy,angle,courtyard)
            d=between_rect_and_circle(x,y,rect)
            assert d>=BOSS_RADIUS+ASSEMBLY_GAP,(ref,name,round(d,2))
        print(f"{ref}: M2 NPTH 2.2mm at ({x:g}, {y:g}), rear boss envelope diameter >=5.5mm; EDGE+C3D CHECK ONLY")
    usb=fp_block(pcb,"J5")
    assert usb.count('np_thru_hole circle (at ') == 2,"USB-C locating holes missing"
    assert usb.count('thru_hole oval (at ') == 4,"USB-C shell anchors missing"
    assert '(at 47 117.325)' in usb
    print("J5: kept 2x NPTH locating holes + 4x plated shield anchor slots; coordinates move with footprint")
    print("J2/J3: SMT connector retention details and card/FPC insertion gaps still need supplier STEP audit")
    print("PASS: four provisional M2 holes with clearance to critical J2/J3/J5/SW1 courtyards")
    print("BLOCKED FOR FAB: nominal display overlays ALL screws; rear-only load path & cell/fastener Z stack require physical CAD.")
if __name__=="__main__":
    main()
