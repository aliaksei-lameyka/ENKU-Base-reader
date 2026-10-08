#!/usr/bin/env python3
"""R27 Good Display stepped-FPC trace integrity, strictly a flat digitization.

No claim of a correct folded 3D FPC route, pad contact orientation, PCBWay milling,
Hirose mating compatibility, glass bending strain, adhesive or stiffener fit.
"""
import math,re
from pathlib import Path
PCB=(Path(__file__).parent/"enku-mainboard-r0.4-stepped-fpc-trial.kicad_pcb").read_text(encoding="utf-8")
EXPECTED=[[58.235,22.19],[58.235,19.049],[58.235,15.527],[53.865,13.908],[53.865,5.055],[75.62,5.055],[75.62,-11.47],[63.12,-11.47],[63.27,-3.417],[36.955,-3.417],[36.955,4.865],[41.325,4.865],[41.325,13.623],[37.05,14.479],[37.05,22.19]]
def main():
    assert PCB.count('(gr_rect (start 18 20) (end 77 121)')==1
    assert PCB.count('(footprint ') == 122
    for key in ['segment','via','zone']:
        assert not re.search(r'(?m)^  \\('+key+r'\\b',PCB),key
    i=PCB.index('  (gr_poly\n    (pts')
    block=PCB[i:PCB.index('    )\n    (stroke',i)]
    verts=[tuple(map(float,m)) for m in re.findall(r'\\(xy\\s+(-?[0-9.]+)\\s+(-?[0-9.]+)\\)',block)]
    assert len(verts)==15,(len(verts),verts)
    for a,b in zip(verts,EXPECTED):
        assert all(abs(x-y)<0.001 for x,y in zip(a,b)),(a,b)
    assert abs(max(x for x,y in verts)-75.62)<0.001
    assert abs(min(y for x,y in verts)+11.47)<0.001
    tips=[p for p in verts if abs(p[1]+11.47)<0.001]
    assert len(tips)==2 and abs(abs(tips[0][0]-tips[1][0])-12.5)<0.001
    for exact in ['(at 69.37 34)','(at 57.5 25)','(at 55.2 34 90)']:
        assert exact in PCB,exact
    print('PASS R27: 15-vertex dimension-anchored stepped flat FPC p5, 33.66mm extension, 12.50mm tip')
    print('PASS R27: 122 components retained, all copper blank; J3/H2/C28 unchanged from R26 candidate')
    print('BLOCKED: supplier DXF, real 3D fold, contact face, pinout and 4-layer PCB DFM')
if __name__=='__main__':
    main()
