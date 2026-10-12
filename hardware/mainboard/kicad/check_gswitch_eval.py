#!/usr/bin/env python3
"""Validate four-terminal C915811 EVAL footprint and world-space handedness.

Uses LCSC/G-Switch drawing C915811 (2019-05-29):
overall land width 3.2mm, left/right gap 0.92mm,
pad upper/lower heights 0.65/0.40mm, total pattern depth 1.50mm.
The un-dimensioned vertical spacing is DERIVED from drawing and requires
confirmation with physical supplier file; EVAL footprint NOT production.
"""
from __future__ import annotations
import re
from pathlib import Path

FP = Path(__file__).resolve().parent / "ENKU.pretty/GT_TC035A_H0195_L3_C915811_EVAL.kicad_mod"

def main() -> int:
    src = FP.read_text(encoding="utf-8")
    m = re.findall(r'\(pad "([1-4])" smd rect \(at (-?[0-9.]+) (-?[0-9.]+)\) '
                   r'\(size ([0-9.]+) ([0-9.]+)\)', src)
    pads = {int(p): tuple(float(v) for v in (x,y,w,h)) for p,x,y,w,h in m}
    assert set(pads) == {1,2,3,4}, pads
    for p in (1,2):
        assert pads[p][0] == pads[1][0], "Contact bank A not aligned"
    for p in (3,4):
        assert pads[p][0] == pads[3][0], "Contact bank B not aligned"
    assert pads[1][0] < pads[3][0]
    assert pads[1][1] == pads[3][1] and pads[2][1] == pads[4][1]
    assert abs((pads[3][0] + pads[3][2]/2) - (pads[1][0] - pads[1][2]/2) - 3.2) < 1e-7
    assert abs((pads[3][0]-pads[3][2]/2) - (pads[1][0]+pads[1][2]/2) - 0.92) < 1e-7
    assert abs((pads[2][1] + pads[2][3]/2) - (pads[1][1] - pads[1][3]/2) - 1.5) < 1e-7
    assert "EVAL" in src and "POCKET TBC" in src
    # KiCad positive 90deg: local +Y moves to board +X; opposite for +270.
    def world(x:float,y:float,cx:float,cy:float,deg:int)->tuple[float,float]:
        if deg == 90: return cx+y,cy-x
        if deg == 270: return cx-y,cy+x
        raise ValueError(deg)
    # Left face uses +270 so PUSH +Y -> exterior -X.
    # Right face uses +90 so PUSH +Y -> exterior +X.
    for side, deg, cx, outer in (("left",270,20.0,-1),("right",90,75.0,1)):
        center=(0.0,0.0)
        p0=world(*center,cx,63.0,deg)
        pushed=world(0.0,1.0,cx,63.0,deg)
        assert (pushed[0]-p0[0])*outer > 0, side
    print("PASS: C915811 EVAL land dimensions and 1/2 vs 3/4 bank symmetry")
    print("PASS: left/right physical actuation vectors opposite")
    print("WARNING: EVAL not fabrication-qualified; PCB pocket, land Y spacing, STEP, DFM remain open")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
