#!/usr/bin/env python3
"""R25 FPC mechanical-assembly release gate for exact GDEY0397T81P.

A 24-way, 0.5mm connector alone DOES NOT establish FPC reach or mating fit.
Until the manufacturer PDF's mechanical drawing has been visually inspected
and the tail 3D routed without glass stress, --release must fail.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path

PCB=Path(__file__).with_name("enku-mainboard-r0.2-placement.kicad_pcb")
REF="J3"
PART="ENKU:FH34SRJ-24S-0.5SH"
CONFIG={
 "display":"Good Display GDEY0397T81P",
 "display_pdf":"https://v4.cecdn.yun300.cn/100001_1909185148/GDEY0397T81P.pdf",
 "controller_pdf":"https://v4.cecdn.yun300.cn/100001_1909185148/SSD1677.pdf",
 "connector":"Hirose FH34SRJ-24S-0.5SH(50)",
 "drawing_revision_confirmed":False,
 "tail_exit_datum_confirmed":False,
 "free_end_and_stiffener_confirmed":False,
 "insert_vector_confirmed":False,
 "fpc_pin1_contact_face_confirmed":False,
 "unstrained_fpc_fold_in_case_confirmed":False,
 "pcbway_assembly_access_confirmed":False,
}
def match_parenthesized(source:str,start:int)->str:
    depth=0;quote=False;esc=False
    for i in range(start,len(source)):
        ch=source[i]
        if quote:
            if esc:esc=False
            elif ch=="\\":esc=True
            elif ch=='"':quote=False
            continue
        if ch=='"':quote=True
        elif ch=="(":depth+=1
        elif ch==")":
            depth-=1
            if depth==0:return source[start:i+1]
    raise ValueError("KiCad footprint sexp is unbalanced")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--release",action="store_true",help="Fail until actual tail drawing and CAD registration are reviewed")
    args=ap.parse_args()
    src=PCB.read_text(encoding="utf-8")
    key='(property "Reference" "J3"'
    pos=src.find(key)
    assert pos>0 and src.count(key)==1,"J3 missing or duplicated"
    st=src.rfind('(footprint ',0,pos)
    fp=match_parenthesized(src,st)
    assert fp.startswith('(footprint "'+PART+'"'),"Supplier connector footprint changed; redo FPC vendor check"
    assert '(at 58 28)' in fp,"J3 moved without FPC registration"
    pads=re.findall(r'\(pad "([0-9]+)" smd ',fp)
    assert len(pads)==24 and set(pads)==set(map(str,range(1,25))),"Expected physical 24 numbered contacts"
    physical=[]
    for n in range(1,25):
        m=re.search(r'\(pad "'+str(n)+r'" smd rect \(at\s+(-?[\d.]+)\s+(-?[\d.]+)',fp)
        assert m,("Missing J3 pad",n)
        physical.append((float(m[1]),float(m[2])))
    spacings=[round(abs(physical[i][0]-physical[i-1][0]),4) for i in range(1,24)]
    assert all(abs(d-.5)<.00001 for d in spacings),"J3 pitch not 0.5mm"
    assert src.count("J3 FPC ROUTE NOT VERIFIED")==1,"Missing engineering J3 blocked marker"
    print("J3 geometric inventory: PASS; 24 SMT signal pads, nominal 0.5-mm pitch, F.Cu at 58 x 28mm")
    pending=[k for k,v in CONFIG.items() if isinstance(v,bool) and not v]
    print("GDEY0397T81P FPC MECHANICAL RELEASE: BLOCKED ("+str(len(pending))+" gates unverified)")
    for issue in pending:print("FPC REQUIRED:",issue)
    if args.release:return 1 if pending else 0
    return 0
if __name__=="__main__":
    raise SystemExit(main())
