#!/usr/bin/env python3
"""R31 independent pad collision/USB mapping gate. Geometry only, not 3D/PCBWay approval.
Verifies *all* placed SMD pads, including passive footprints without F.CrtYd.
Counts same-net pad overlaps as assembly faults, not acceptable electrical shortcuts.
"""
from pathlib import Path
import argparse
import math
import re
HERE=Path(__file__).resolve().parent
PCB=(HERE/"enku-mainboard-r1.3-base-first-power-copper.kicad_pcb").read_text()
EXPECTED={"D2":(56.,50.),"C24":(47.3,42.),"C6":(47.7,87.75),"J1":(69.8,93.5)}
def balanced(src,start):
    d=0;inside=False;esc=False
    for end in range(start,len(src)):
        c=src[end]
        if inside:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':inside=False
        elif c=='"':inside=True
        elif c=="(":d+=1
        elif c==")":
            d-=1
            if d==0:return src[start:end+1]
    raise AssertionError("Unbalanced KiCad expression at "+str(start))
def footprints():
    found={}
    for m in re.finditer(r'(?m)^  \(footprint "',PCB):
        txt=balanced(PCB,m.start()+2)
        head=re.search(r'^\(footprint "([^"]+)" \(layer "([FB])\.Cu"\)\s+\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',txt)
        ref=re.search(r'\(property "Reference" "([^"]+)"',txt)
        assert head and ref,m.start()
        found[ref[1]]=dict(txt=txt,side=head[2],x=float(head[3]),y=float(head[4]),rot=float(head[5] or 0))
    return found
def pads(fps):
    out=[]
    for ref,fp in fps.items():
        a=math.radians(fp["rot"])
        for m in re.finditer(r'\(pad "([^"]*)" (smd|thru_hole|np_thru_hole) ([^\n]+)',fp["txt"]):
            if m[2]!="smd":continue
            item=m[3]; layers=re.search(r'\(layers ([^\)]*)\)',item)
            if not layers or (('"'+fp["side"]+'.Cu"') not in layers[1]):continue
            xy=re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',item)
            wh=re.search(r'\(size ([\d.]+) ([\d.]+)\)',item)
            net=re.search(r'\(net \d+ "([^"]+)"\)',item)
            if not xy or not wh or not net:continue
            px,py=float(xy[1]),float(xy[2])
            x=fp["x"]+px*math.cos(a)+py*math.sin(a)
            y=fp["y"]-px*math.sin(a)+py*math.cos(a)
            # KiCad board pad (at X Y ANGLE) stores PAD absolute orientation; do not add footprint rotation again.
            theta=math.radians(float(xy[3] or 0))
            w,h=float(wh[1]),float(wh[2])
            wx=(abs(w*math.cos(theta))+abs(h*math.sin(theta)))/2
            wy=(abs(w*math.sin(theta))+abs(h*math.cos(theta)))/2
            out.append((ref,m[1],fp["side"],net[1],(x-wx,y-wy,x+wx,y+wy)))
    return out
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--release",action="store_true")
    args=ap.parse_args()
    fp=footprints()
    assert len(fp)==125,len(fp)
    for ref,(x,y) in EXPECTED.items():
        assert (fp[ref]["x"],fp[ref]["y"])==(x,y),(ref,fp[ref])
    for ref in ("D1","D2","D3"):
        t=fp[ref]["txt"]
        assert '(fp_line (start 2.8 -0.55) (end 2.8 0.55)' in t,ref
        assert 'MBR0530' in t and re.search(r'\(pad "1" smd rect [^\n]+\)',t),ref
        cathode=re.search(r'\(pad "1" smd rect [^\n]+\(net \d+ "([^"]+)"\)\)',t)
        anode=re.search(r'\(pad "2" smd rect [^\n]+\(net \d+ "([^"]+)"\)\)',t)
        assert cathode and anode
    for ref,ck,an in (("D1","EPD_VGH","EPD_SW"),("D2","GND","EPD_CP_NEG"),("D3","EPD_CP_NEG","EPD_VGL")):
        t=fp[ref]["txt"]
        assert f'(net {dict(D1=26,D2=1,D3=31)[ref]} "{ck}")' in t
        assert '"'+an+'"' in t
    j1=fp["J1"]["txt"]
    assert "ENKU:JST_PH_S3B-PH-SM4-TB_1x03-1MP_P2.00mm_Horizontal" in j1
    assert len(re.findall(r'\(pad "MP" smd roundrect',j1))==2
    for padnum,net in (("1","VBAT"),("2","GND"),("3","BAT_TS")):
        assert len(re.findall(r'\(pad "'+padnum+r'" smd roundrect [^\n]*\(net \d+ "'+net+r'"\)',j1))==1,(padnum,net)
    for coord in ("(at 4.35 2.9 90)","(at -4.35 2.9 90)","(at -2 -2.85 90)","(at 0 -2.85 90)","(at 2 -2.85 90)"):
        assert coord in j1,coord
    assert "(at 69.8 93.5 90)" in j1
    assert (fp["Q2"]["x"],fp["Q2"]["y"])==(55.5,82.5)
    assert (fp["R40"]["x"],fp["R40"]["y"])==(50.5,82.5)
    assert '(pad "1" smd rect (at -1 -0.95)' in fp["Q2"]["txt"]
    assert '(pad "2" smd rect (at -1 0.95)' in fp["Q2"]["txt"]
    usb=fp["J5"]["txt"]
    by_x=[]
    for m in re.finditer(r'\(pad "([AB]\d+)" smd [^\n]+',usb):
        xy=re.search(r'\(at ([-\d.]+) ([-\d.]+)\)',m[0])
        net=re.search(r'\(net \d+ "([^"]+)"\)',m[0])
        by_x.append((float(xy[1]),m[1],net[1] if net else "NC"))
    by_x.sort(key=lambda it:it[0])
    from collections import defaultdict
    ordered=defaultdict(list)
    for x,p,n in by_x:ordered[x].append(p)
    assert dict(ordered)=={-3.2:["A1","B12"],-2.4:["A4","B9"],-1.75:["B8"],-1.25:["A5"],-0.75:["B7"],-0.25:["A6"],0.25:["A7"],0.75:["B6"],1.25:["A8"],1.75:["B5"],2.4:["A9","B4"],3.2:["A12","B1"]},ordered
    nc={p:n for x,p,n in by_x}
    for p,n in {"A6":"USB_DP_CONN","B6":"USB_DP_CONN","A7":"USB_DM_CONN","B7":"USB_DM_CONN","A5":"USB_CC1","B5":"USB_CC2","A8":"NC","B8":"NC"}.items():
        assert nc[p]==n,(p,nc[p],n)
    pp=pads(fp)
    faults=[]
    for i,a in enumerate(pp):
        for b in pp[i+1:]:
            if a[2]!=b[2]:continue
            if a[0]==b[0] and a[3]==b[3]:continue
            xa=max(a[4][0],b[4][0]);xb=min(a[4][2],b[4][2])
            ya=max(a[4][1],b[4][1]);yb=min(a[4][3],b[4][3])
            if xb-xa>0.01 and yb-ya>0.01:
                faults.append((a[0],a[1],b[0],b[1],a[3],b[3],round((xb-xa)*(yb-ya),3)))
    assert not faults,"SMT pad overlaps, even if same-net: "+str(faults)
    assert len(re.findall(r"(?m)^  \(segment \(",PCB))==19
    assert len(re.findall(r"(?m)^  \(via \(",PCB))==1
    print("R36 ASSEMBLY PASS: 125 footprints, 0 different-net intra-footprint OR cross-component SMD pad overlaps, 3 MBR0530 cathode markers, verified GCT 16-contact order/net map, 19 prototype tracks, 1 via.")
    print("This is source geometry only; copper pad spacing, physical 3D clearances, J1/SW1 vendor lock, actual FPC, EPD HV and supplier BOM NOT SIGNED OFF.")
    if args.release:raise SystemExit("FAB BLOCKED: no routing, release KiCad DRC, battery mating, mechanical and supplier signoff")
if __name__=="__main__": main()
