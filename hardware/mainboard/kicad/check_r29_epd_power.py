#!/usr/bin/env python3
"""Good Display GDEY0397T81P module p6 says VDDIO pin15 ties to VCI pin16.
The Board has separate net labels but schematic connects them via R28 0R.
Check physical pad numbers and assembly value; not signal/power signoff.
"""
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
SCH=(HERE/"epd_hv.kicad_sch").read_text()
PCB=(HERE/"enku-mainboard-r0.6-base-placement.kicad_pcb").read_text()

def balanced(s,start):
    depth=0;quote=False;esc=False
    for i in range(start,len(s)):
        c=s[i]
        if quote:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':quote=False
            continue
        if c=='"':quote=True
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if depth==0:return s[start:i+1]
    raise ValueError("unbalanced KiCad S-expression")

def fp(ref):
    idx=PCB.index('(property "Reference" "'+ref+'"')
    return balanced(PCB,PCB.rfind('(footprint ',0,idx))

def main():
    start=SCH.index('(symbol (lib_id "ENKU:R") (at 190.5 44.45')
    bridge=balanced(SCH,start)
    assert '(property "Reference" "R28"' in bridge
    assert '(property "Value" "0R"' in bridge
    assert '(dnp no)' in bridge
    for sign in (
        '(global_label "3V3_SYS" (shape input) (at 182.88 44.45',
        '(global_label "EPD_VCI" (shape output) (at 198.12 44.45',
        '(global_label "3V3_SYS" (shape output) (at 247.65 77.47',
        '(global_label "EPD_VCI" (shape output) (at 247.65 80.01',
    ):
        assert sign in SCH,sign
    r28=fp("R28")
    assert '(property "Value" "0R"' in r28
    assert '(pad "1" ' in r28 and '(pad "2" ' in r28
    j3=fp("J3")
    for pin,net in (("15","3V3_SYS"),("16","EPD_VCI"),("5","EPD_VSH2")):
        m=re.search(r'\(pad "'+pin+r'" smd[^\n]*',j3)
        assert m and ('"'+net+'"') in m[0],(pin,net)
    print("SOURCE CHECK PASS: Good Display J3 pin15/16 bridged in schematic via POPULATED R28 0R")
    print("RELEASE BLOCKED: manufacturer pin5 VDHR/VSH2 ambiguity; power sequencing and original flex contact side")
if __name__=="__main__":
    main()
