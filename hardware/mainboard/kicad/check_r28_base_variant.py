#!/usr/bin/env python3
"""R28 Base-only PCB/schematic hardware segregation gate.

Original R27 studies remain untouched; the new Board and MCU sheet must
exclude Hall, magnetic-cover, Qi power and frontlight components entirely.
Never confuse integrity gate with KiCad ERC, native DRC or release approval.
"""
from pathlib import Path
import re

HERE=Path(__file__).parent
BEFORE=(HERE/"enku-mainboard-r0.4-stepped-fpc-trial.kicad_pcb").read_text()
BASE=(HERE/"enku-mainboard-r0.5-base-only.kicad_pcb").read_text()
MCU=(HERE/"mcu_io.kicad_sch").read_text()
def fp_inventory(s):
    pat=r'\\(footprint "([^"]+)"\\s+\\(layer "(F|B)\\.Cu"\\)\\s+\\(at (-?[\\d.]+) (-?[\\d.]+)(?: ([\\d.]+))?\\)'
    matches=list(re.finditer(pat,s))
    result={}
    for idx,m in enumerate(matches):
        block=s[m.start():matches[idx+1].start() if idx+1<len(matches) else len(s)]
        ref=re.search(r'\\(property "Reference" "([^"]+)"',block)
        assert ref,("missing reference",idx)
        result[ref[1]]=(m[1],m[2],float(m[3]),float(m[4]),float(m[5] or 0))
    return result

def main():
    a,b=fp_inventory(BEFORE),fp_inventory(BASE)
    assert len(a)==122 and len(b)==120,(len(a),len(b))
    assert set(a)-set(b)=={"U6","C20"},set(a)-set(b)
    for ref in b:assert a[ref]==b[ref],(ref,a[ref],b[ref])
    for blocked in ("HALL_INT","QI COIL KEEPOUT","DRV5032FBDBZR"):
        assert blocked not in BASE,blocked
    for blocked in ('(symbol (lib_id "ENKU:DRV5032FB")','(property "Reference" "U6"',
                    '(property "Reference" "C20"','HALL_INT'):
        assert blocked not in MCU,blocked
    assert '(no_connect (at 60.96 81.28)' in MCU
    assert re.search(r'\\(pad "10" smd rect \\(at -8.75 6.17 90\\)[^\\n]+\\(layers "F.Cu" "F.Paste" "F.Mask"\\)\\)',BASE)
    for token in ('(property "Reference" "U5"','(property "Reference" "J3"',
                  '(property "Reference" "H1"','(property "Reference" "H2"',
                  '(property "Reference" "H3"','(property "Reference" "H4"'):
        assert token in BASE,token
    for kind in ('segment','via','zone'):
        assert not re.search(r'(?m)^  \\('+kind+r'\\b',BASE),kind
    assert BASE.count('(gr_rect (start 18 20) (end 77 121)')==1
    print("R28 BASE SEPARATION: PASS")
    print("Physical: 120 vs 122 placements; removed U6 Hall and dedicated C20 entirely; no Qi/frontlight.")
    print("Electrical: Hall net and MCU GPIO link removed; previously occupied MCU pin marked NC.")
    print("Not fabrication approved: FPC, connector, mounting, supplier and native KiCad checks remain.")
if __name__=="__main__":
    main()
