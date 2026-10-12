#!/usr/bin/env python3
"""R33 source-level switched VIN + Good Display 24-pin hard release block."""
import argparse
import re
from pathlib import Path
HERE=Path(__file__).parent
PCB=(HERE/"enku-mainboard-r1.1-base-gated-battery-adc.kicad_pcb").read_text()
SCH=(HERE/"power.kicad_sch").read_text()
EPD=(HERE/"epd_hv.kicad_sch").read_text()
def balanced(src,start):
    depth=0; quoted=False; escaped=False
    for i in range(start,len(src)):
        c=src[i]
        if quoted:
            if escaped: escaped=False
            elif c=="\\": escaped=True
            elif c=='"': quoted=False
        elif c=='"': quoted=True
        elif c=='(': depth+=1
        elif c==')':
            depth-=1
            if depth==0:return src[start:i+1]
    raise ValueError("Unbalanced footprint")
def fp(ref):
    p=PCB.index('(property "Reference" "'+ref+'"')
    return balanced(PCB,PCB.rfind("(footprint ",0,p))
def pad(ref,num):
    lines=[l for l in fp(ref).splitlines() if '(pad "'+str(num)+'" ' in l]
    assert len(lines)==1,(ref,num,len(lines))
    m=re.search(r'\(net \d+ "([^"]+)"\)',lines[0])
    return m[1] if m else "NC"
def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--release",action="store_true")
    args=cli.parse_args()
    assert PCB.count('(footprint "')==123
    assert not re.search(r'(?m)^  \((segment|via|zone)\b',PCB)
    nets={("SW1","1"):"VSYS",("SW1","2"):"SYS_EN",
          ("U4","1"):"SYS_EN",("U4","10"):"SYS_EN",
          ("C9","1"):"SYS_EN",("C9","2"):"GND",
          ("C10","1"):"SYS_EN",("C10","2"):"GND",
          ("R13","1"):"SYS_EN",("R13","2"):"GND",
          ("U3","1"):"VSYS",("TP5","1"):"VSYS",("TP7","1"):"SYS_EN",
          ("R26","1"):"BAT_ADC_SW",("R26","2"):"BAT_ADC",
          ("R27","1"):"BAT_ADC",("R27","2"):"GND",
          ("U9","1"):"BAT_ADC_SW",("U9","2"):"VBAT",("U9","3"):"GND",("U9","4"):"3V3_SYS",("U9","5"):"VBAT",
          ("C37","1"):"VBAT",("C37","2"):"GND",("R39","1"):"3V3_SYS",("R39","2"):"GND"}
    for (ref,num),expected in nets.items():
        assert pad(ref,num)==expected,(ref,num,pad(ref,num),expected)
    for coord in ("187.96 57.15","243.84 62.23","243.84 85.09"):
        assert f'(global_label "SYS_EN" (shape input) (at {coord} 0)' in SCH,coord
    pins={1:"NC",2:"EPD_GDR",3:"EPD_RESE",4:"NC",5:"EPD_VSH2",
          6:"NC",7:"NC",8:"EPD_BS1",9:"EPD_BUSY",10:"EPD_RST_PANEL",
          11:"EPD_DC_PANEL",12:"EPD_CS_PANEL",13:"EPD_SCLK_PANEL",
          14:"EPD_MOSI_PANEL",15:"3V3_SYS",16:"EPD_VCI",17:"GND",
          18:"EPD_VDD",19:"NC",20:"EPD_VSH1",21:"EPD_VGH",
          22:"EPD_VSL",23:"EPD_VGL",24:"EPD_VCOM"}
    for num,expected in pins.items():
        assert pad("J3",str(num))==expected,(num,pad("J3",str(num)),expected)
    assert pad("R28","1")=="3V3_SYS" and pad("R28","2")=="EPD_VCI"
    assert '(property "Value" "0R"' in fp("R28")
    r28=balanced(EPD,EPD.index('(symbol (lib_id "ENKU:R") (at 190.5 44.45'))
    assert '(dnp no)' in r28
    print("R34 POWER/ADC/EPD PASS: 123 parts, SW1 switches U4 VIN/EN/CIN, TMUX1101 isolates VBAT divider when 3V3 off, full 24-pin J3 gate.")
    print("RELEASE BLOCKED: unmeasured TMUX1101 off leakage and reverse injection, switch MPN/current, charger STAT backfeed, J3 pin5 VDHR/VSH2 contradiction, 3D FPC and off-state bench.")
    if args.release:raise SystemExit("FAB BLOCKED: physical electrical signoff required")
if __name__=="__main__":main()
