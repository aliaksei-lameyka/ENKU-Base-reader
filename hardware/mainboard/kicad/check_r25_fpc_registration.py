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
 "drawing_revision_confirmed":True,
 "manufacturer_step_tail_exit_confirmed":True,
 "panel_front_contact_order_confirmed":True,
 "tail_folding_and_3D_registration_confirmed":False,
 "terminal_stiffener_fit_confirmed":False,
 "insert_vector_confirmed":False,
 "pin5_VDHR_to_VSH2_design_confirmed":False,
 "VDDIO_VCI_power_topology_confirmed":False,
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
    # Verified against Good Display GDEY0397T81P rev1.0 pp5,6,19
    # Caution: module pin5 is called VDHR (pp5-6) and VSH2 (p19).
    nets=["NC","EPD_GDR","EPD_RESE","NC","EPD_VSH2","NC","NC",
          "EPD_BS1","EPD_BUSY","EPD_RST_PANEL","EPD_DC_PANEL",
          "EPD_CS_PANEL","EPD_SCLK_PANEL","EPD_MOSI_PANEL",
          "3V3_SYS","EPD_VCI","GND","EPD_VDD","NC",
          "EPD_VSH1","EPD_VGH","EPD_VSL","EPD_VGL","EPD_VCOM"]
    for n,target in enumerate(nets,1):
        line=re.search(r'\(pad "'+str(n)+r'" smd[^\n]*',fp)
        assert line,("no J3 pad",n)
        found=re.search(r'\(net \d+ "([^"]+)"\)',line[0])
        actual=found[1] if found else "NC"
        assert actual==target,("Good Display pad/net map drift",n,actual,target)
    # Front-view contact-end width 12.50mm and nominal 56.24mm glass width
    # conditional panel 180-degree orientation gives the 2D lateral projection.
    candidate_x=19.38+56.24-12.50/2
    assert abs(candidate_x-69.37)<.02
    assert "(gr_rect (start 62.12 31.75) (end 76.62 36.05)" in src
    # H2 (72,25), radius 2.75mm, overlaps an x69.37,y28 J3 courtyard.
    # This is a confirmed plan-view clash, not a claim of impossible 3D assembly.
    print(f"FPC top-exit conditional projection x={candidate_x:.2f}mm; J3 x58.0mm; J3 x69.37/y28 overlaps H2 head allowance")
    print("WARNING: Good Display pp5-6 pin5 VDHR, p19 pin5 VSH2; ENKU has EPD_VSH2")
    print("WARNING: VDDIO pin15 and VCI pin16 are separate KiCad nets; validate supply topology")
    assert src.count("J3 FPC ROUTE NOT VERIFIED")==1,"Missing engineering J3 blocked marker"
    print("J3 geometric inventory: PASS; 24 SMT signal pads, nominal 0.5-mm pitch, F.Cu at 58 x 28mm")
    pending=[k for k,v in CONFIG.items() if isinstance(v,bool) and not v]
    print("GDEY0397T81P FPC MECHANICAL RELEASE: BLOCKED ("+str(len(pending))+" gates unverified)")
    for issue in pending:print("FPC REQUIRED:",issue)
    if args.release:return 1 if pending else 0
    return 0
if __name__=="__main__":
    raise SystemExit(main())
