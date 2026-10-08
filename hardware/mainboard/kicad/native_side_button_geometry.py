#!/usr/bin/env python3
"""Native KiCad coordinate and bank audit for R24 C915811, not a DFM approval.

Read resolved pad centers from pcbnew (not inferred from angle conventions).
Track endpoint distances are diagnostic; DRC determines full connectivity.
"""
from __future__ import annotations
import json
from pathlib import Path
import pcbnew

BOARD=Path(__file__).resolve().parent/"enku-mainboard-r0.1.kicad_pcb"
CONFIG={"SW3":("BTN_L1",90),"SW4":("BTN_L2",90),
        "SW5":("BTN_R1",270),"SW6":("BTN_R2",270)}

def mm(point):
    return (round(pcbnew.ToMM(point.x),4),round(pcbnew.ToMM(point.y),4))

def main():
    board=pcbnew.LoadBoard(str(BOARD))
    found={fp.GetReference():fp for fp in board.GetFootprints()}
    all_tracks=[t for t in board.GetTracks() if isinstance(t,pcbnew.PCB_TRACK)]
    out={}
    for ref,(net,angle) in CONFIG.items():
        fp=found[ref]
        if abs(fp.GetOrientationDegrees()-angle)>0.01:
            raise SystemExit(f"{ref}: bad KiCad physical rotation {fp.GetOrientationDegrees()} != {angle}")
        pins={str(p.GetNumber()):(p.GetNetname(),mm(p.GetPosition())) for p in fp.Pads()}
        expected={"1":net,"2":net,"3":"GND","4":"GND"}
        if {key:v[0] for key,v in pins.items()}!=expected:
            raise SystemExit(f"{ref}: physical pad net mapping {pins!r} != {expected!r}")
        for number,(padnet,xy) in pins.items():
            candidates=[]
            for tr in all_tracks:
                if tr.GetNetname()!=padnet or tr.GetLayerName()!="F.Cu":
                    continue
                for end in (tr.GetStart(),tr.GetEnd()):
                    pt=mm(end)
                    d=((pt[0]-xy[0])**2+(pt[1]-xy[1])**2)**.5
                    if d<1.4:
                        candidates.append((round(d,3),pt))
            pins[number]=(padnet,xy,sorted(candidates)[:4])
        print("KICAD_WORLD_PADS "+ref+" "+json.dumps(pins,sort_keys=True))
        out[ref]=pins
    file=Path("/tmp/enku-r24-physical-pad-centers.json")
    file.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS: native KiCad R24 package rotation and bank numbering; physical clearance NOT APPROVED")

if __name__=="__main__":
    main()
