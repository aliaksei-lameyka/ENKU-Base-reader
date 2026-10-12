#!/usr/bin/env python3
"""R30 pre-DFM geometry checks for service contacts; NOT fabrication approval."""
from pathlib import Path
import re
import argparse
PCB = (Path(__file__).parent / "enku-mainboard-r0.7-base-dfm-prep.kicad_pcb").read_text()
def fp(ref):
    i=PCB.index('(property "Reference" "'+ref+'"')
    start=PCB.rfind('(footprint ',0,i)
    depth=0; quote=False; escape=False
    for j in range(start,len(PCB)):
        c=PCB[j]
        if quote:
            if escape: escape=False
            elif c=="\\": escape=True
            elif c=='"': quote=False
        else:
            if c=='"': quote=True
            elif c=='(': depth+=1
            elif c==')':
                depth-=1
                if depth==0:return PCB[start:j+1]
    raise AssertionError("Unbalanced KiCad footprint")
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--release",action="store_true")
    args=ap.parse_args()
    assert PCB.count('(footprint "')==120
    assert not re.search(r'(?m)^  \((?:segment|via|zone)\b',PCB)
    for forbidden in ('HALL_INT','DRV5032FBDBZR','QI COIL KEEPOUT'):
        assert forbidden not in PCB,forbidden
    j7=fp('J7'); j6=fp('J6'); sw2=fp('SW2')
    assert '(at 35 87)' in j7 and '(layer "B.Cu")' in j7.splitlines()[0]
    assert '(at 35.5 79)' in sw2, "SW2 must clear the through-board guide holes"
    assert '(attr exclude_from_bom exclude_from_pos_files)' in j7
    assert '(attr exclude_from_bom exclude_from_pos_files)' in j6
    assert 'B.Paste' not in j7 and 'B.Paste' not in j6
    matches=re.findall(r'\(pad "([1-6])" smd circle \(at ([-\d.]+) ([-\d.]+)\) \(size ([\d.]+) ([\d.]+)\) \(layers "B.Cu" "B.Mask"\) \(net \d+ "([^"]+)"\)\)',j7)
    expected=[('1',-1.27,0.635,'3V3_SYS'),('2',-1.27,-0.635,'GND'),('3',0,0.635,'UART_TX'),('4',0,-0.635,'UART_RX'),('5',1.27,0.635,'BOOT'),('6',1.27,-0.635,'ESP_EN')]
    assert len(matches)==6,matches
    for n,x,y,net in expected:
        hits=[m for m in matches if m[0]==n]
        assert len(hits)==1
        m=hits[0]
        assert float(m[1])==x and float(m[2])==y and float(m[3])==float(m[4])==0.7874 and m[5]==net
    holes=re.findall(r'\(pad "" np_thru_hole circle \(at ([-\d.]+) ([-\d.]+)\) \(size ([\d.]+) ([\d.]+)\) \(drill ([\d.]+)\)',j7)
    assert len(holes)==3
    assert {(float(h[0]),float(h[1])) for h in holes}=={(2.54,-1.016),(2.54,1.016),(-2.54,0)}
    assert all(float(h[2])==float(h[3])==float(h[4])==0.9906 for h in holes)
    assert not re.search(r'\(pad "[1-6]" thru_hole',j7), "contact pin must not be plated drilled PTH"
    assert sw2.count('F.Cu')>0
    print("R30 source geometry PASS: 120 footprints, J7 six no-paste SMT + 3 NPTH, SW2 moved, J6 paste disabled.")
    print("Do not fabricate: Native KiCad DRC, FPC and physical pogo-pin1 / backface mirror and battery access not qualified.")
    if args.release: raise SystemExit("FAB BLOCKED: no full native DRC, physical jig, FPC, sourced BOM or copper routing")
if __name__=="__main__":main()
