#!/usr/bin/env python3
"""ENKU Base J7 supplier-driven Tag-Connect 6-pin service footprint gate.

Tag-Connect TC2030-IDC-NL original footprint drawing Rev B, 2019-12-05:
six 0.787mm nominal SMT contact pads WITHOUT solder paste, and three 0.991mm
NPTH alignment holes. PCB currently has six 0.5mm-drilled PTH pads, no
alignment holes and is directly opposite the SW2 boot button.
The script inventories the failure in normal CI and FAILS on --release.
Never convert J7 to a PCBWay production footprint without physical top/bottom
orientation, pad1-to-UART verification and clipped-cable access review.
"""
import argparse
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
PCB=(HERE/"enku-mainboard-r0.6-base-placement.kicad_pcb").read_text(encoding="utf-8")
VENDOR="TC2030-IDC-NL / TC2030-IDC-NL-FP rev B"
def block(src,start):
    n=0;quote=False;esc=False
    for i in range(start,len(src)):
        c=src[i]
        if quote:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':quote=False
            continue
        if c=='"':quote=True
        elif c=="(":n+=1
        elif c==")":
            n-=1
            if n==0:return src[start:i+1]
    raise ValueError("Unbalanced KiCad footprint")
def fp(ref):
    i=PCB.index('(property "Reference" "'+ref+'"')
    j=PCB.rfind('(footprint ',0,i)
    return block(PCB,j)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--release",action="store_true",help="Refuse fabrication until supplier geometry approved")
    args=ap.parse_args()
    j=fp("J7")
    sw=fp("SW2")
    assert '(layer "B.Cu")' in j[:120]
    assert '(at 35 87)' in j[:150]
    assert '(at 35.5 87)' in sw[:150]
    six=len(re.findall(r'\(pad "[1-6]" thru_hole ',j))
    npth=len(re.findall(r'\(pad "" np_thru_hole ',j))
    smt=len(re.findall(r'\(pad "[1-6]" smd ',j))
    fail=[]
    if six:fail.append(str(six)+" plated signal holes 0.5mm on PCB; manufacturer calls for SMT no-paste 0.787mm contact pads")
    if npth!=3:fail.append("3 x 0.991mm NPTH alignment holes missing")
    if smt!=6:fail.append("six manufacturer contact pads not implemented as SMT no-paste")
    if '(at 35 87)' in j and '(at 35.5 87)' in sw:
        fail.append("rear J7 guide holes project under front SW2 body/contacts; must relocate or redesign boot input")
    if any('F.Paste' in line or 'B.Paste' in line for line in j.splitlines() if '(pad "' in line):
        fail.append("J7 contact contains solder paste; prohibited by supplier")
    print("J7 EXACT VENDOR",VENDOR)
    print("CURRENT J7 PTH",six,"SMT",smt,"NPTH",npth)
    for line in fail: print("J7 FAB BLOCKER:",line)
    print("This normal CI inventory does not approve the board; --release must be green before Gerbers.")
    if args.release and fail:raise SystemExit(1)
    if not fail:print("J7 footprint source geometry checklist PASS; physical assembly still needs review")
if __name__=="__main__":
    main()
