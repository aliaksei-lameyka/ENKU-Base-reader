#!/usr/bin/env python3
"""Dedicated R29: physical footprint courtyard and mounting-envelope placement gate.

Reads native KiCad dimensions from footprint F/B.CrtYd rectangles and world transforms.
Not a release: the unvalidated custom connector/switch footprints and full 3D stackup
must be cleared by component STEP / supplier DFM. Does not check native copper DRC.
"""
from __future__ import annotations
import re
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OLD=(ROOT/"enku-mainboard-r0.5-base-only.kicad_pcb").read_text(encoding="utf8")
NEW=(ROOT/"enku-mainboard-r0.6-base-placement.kicad_pcb").read_text(encoding="utf8")
BOARD=(18.,20.,77.,121.)
MOUNT_BOSS=2.75
MARGIN=0.65
CHANGES={"J2":(27.,100.7,270.),"R19":(38.,101.,0.),"R20":(38.,104.,0.),"R21":(38.,107.,0.)}

def balanced(src,start):
    depth=0;quoted=False;escape=False
    for i in range(start,len(src)):
        c=src[i]
        if quoted:
            if escape: escape=False
            elif c=="\\": escape=True
            elif c=='"': quoted=False
            continue
        if c=='"': quoted=True
        elif c=='(': depth+=1
        elif c==')':
            depth-=1
            if depth==0: return src[start:i+1]
    raise ValueError("unbalanced KiCad footprint")

def parts(src):
    result={}
    for m in re.finditer(r'(?m)^  \(footprint "',src):
        block=balanced(src,m.start()+2)
        root=re.match(r'\(footprint "([^"]+)"\s+\(layer "([FB])\.Cu"\)\s+\(at (-?[\d.]+) (-?[\d.]+)(?: ([\d.]+))?\)',block)
        ref=re.search(r'\(property "Reference" "([^"]+)"',block)
        if not root or not ref: raise AssertionError("bad footprint source")
        name=ref[1]
        assert name not in result,name
        part={"ref":name,"lib":root[1],"side":root[2],
              "x":float(root[3]),"y":float(root[4]),"r":float(root[5] or 0),
              "rects":[]}
        for match in re.finditer(r'\(fp_rect \(start (-?[\d.]+) (-?[\d.]+)\) \(end (-?[\d.]+) (-?[\d.]+)\)[\s\S]{0,180}?\(layer "([FB])\.CrtYd"\)',block):
            if match[5]!=part["side"]:continue
            x0,y0,x1,y1=map(float,match.group(1,2,3,4))
            theta=math.radians(part["r"])
            pts=[(part["x"]+u*math.cos(theta)+v*math.sin(theta),
                  part["y"]-u*math.sin(theta)+v*math.cos(theta))
                 for u,v in ((x0,y0),(x0,y1),(x1,y0),(x1,y1))]
            part["rects"].append((min(p[0] for p in pts),min(p[1] for p in pts),
                                  max(p[0] for p in pts),max(p[1] for p in pts)))
        if part["rects"]:
            rects=part["rects"]
            part["box"]=(min(a[0] for a in rects),min(a[1] for a in rects),
                         max(a[2] for a in rects),max(a[3] for a in rects))
        result[name]=part
    return result

def overlap(a,b):
    return (min(a[2],b[2])-max(a[0],b[0]))>0.01 and (min(a[3],b[3])-max(a[1],b[1]))>0.01

def clearance_pt_box(px,py,b):
    return math.hypot(max(b[0]-px,0,px-b[2]),max(b[1]-py,0,py-b[3]))

def collisions(parts):
    items=list(parts.values())
    bad=[]
    for i,a in enumerate(items):
        if "box" not in a:continue
        for b in items[i+1:]:
            if a["side"]==b["side"] and "box" in b and overlap(a["box"],b["box"]):
                bad.append((a["ref"],b["ref"]))
    return bad

def main():
    old,new=parts(OLD),parts(NEW)
    assert len(old)==len(new)==120,(len(old),len(new))
    assert set(old)==set(new)
    assert NEW.count('(gr_rect (start 18 20) (end 77 121)')==1
    assert not any(re.search(r'(?m)^  \('+kind+r'\b',NEW) for kind in ("segment","via","zone"))
    changed={}
    for ref in old:
        a,b=old[ref],new[ref]
        assert a["lib"]==b["lib"] and a["side"]==b["side"],ref
        av=(a["x"],a["y"],a["r"]);bv=(b["x"],b["y"],b["r"])
        if av!=bv:changed[ref]=bv
    assert changed==CHANGES,("R29 position changes beyond reviewed J2 resistors",changed)
    before=collisions(old)
    after=collisions(new)
    assert set(tuple(sorted(x)) for x in before)=={
      ("J2","R19"),("J2","R20"),("J2","R21")
    },("R28 collision inventory changed",before)
    assert not after,("R29 still overlaps F.CrtYd/B.CrtYd",after)
    # Study head+bearing Ø5.5: measure actual rectangle footprints, not only component centers.
    for hole in ("H1","H2","H3","H4"):
        h=new[hole]
        x,y=h["x"],h["y"]
        assert min(x-BOARD[0],BOARD[2]-x,y-BOARD[1],BOARD[3]-y)>MOUNT_BOSS+1.
        for fp in new.values():
            if fp["ref"]==hole or fp["ref"].startswith("H"):continue
            if "box" not in fp or fp["side"]!="F":continue
            if clearance_pt_box(x,y,fp["box"])<MOUNT_BOSS+MARGIN:
                raise AssertionError(("M2 rear boss conflicts with placed front courtyard",
                                       hole,fp["ref"],fp["box"]))
    # J2 and J5 are allowed to overhang the board edge ONLY for their insertion mouth.
    for fp in new.values():
        b=fp.get("box")
        if not b:continue
        if b[0]<BOARD[0]-.01 or b[1]<BOARD[1]-.01 or b[2]>BOARD[2]+.01 or b[3]>BOARD[3]+.01:
            assert fp["ref"] in ("J2","J5"),("unapproved courtyard outside PCB",fp["ref"],b)
    print("R29 courtyard audit PASS: 120 footprints; old overlaps=",before,
          "; new overlap count=",len(after))
    print("Moved Hirose J2 inward by 0.9mm and R19-R21 1mm right; M2 envelopes screened")
    print("Allowed connector overhang J2/J5 remains pending manufacturer STEP/DFM.")
    print("BLOCKED for manufacturing: 78 pads without full courtyard, flex fold, all real assembly heights, switches and battery.")
if __name__=="__main__":
    main()
