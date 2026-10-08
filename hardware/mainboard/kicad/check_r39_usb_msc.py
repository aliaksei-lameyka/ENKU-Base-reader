#!/usr/bin/env python3
"""R39 ENKU Base USB-C native USB / SPI microSD MSC hardware contract.

Fails on pin inversions, missing card power, missing CC resistors or USB ESD.
This checks source and pilot routing; NOT 90-ohm USB signal integrity or firmware.
"""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
B=(HERE/"enku-mainboard-r1.6-base-usb-msc-sd-power.kicad_pcb").read_text()
MCU=(HERE/"mcu_io.kicad_sch").read_text()
USB=(HERE/"connectors.kicad_sch").read_text()
def expr(s,start):
    d=0;q=False;e=False
    for i in range(start,len(s)):
        c=s[i]
        if q:
            if e:e=False
            elif c=="\\":e=True
            elif c=='"':q=False
        elif c=='"':q=True
        elif c=='(':d+=1
        elif c==')':
            d-=1
            if d==0:return s[start:i+1]
    raise AssertionError("KiCad expression not balanced")
def footprint(ref):
    i=B.index(f'(property "Reference" "{ref}"')
    return expr(B,B.rfind('(footprint ',0,i))
def pin(ref,n):
    f=footprint(ref)
    lines=[v for v in f.splitlines() if re.search(r'\(pad "'+re.escape(str(n))+r'" ',v)]
    assert len(lines)==1,(ref,n,len(lines))
    m=re.search(r'\(net \d+ "([^"]+)"\)',lines[0])
    return m.group(1) if m else "NC"
expected={
    ("U1","13"):"USB_DM", ("U1","14"):"USB_DP",
    ("J5","A6"):"USB_DP_CONN",("J5","B6"):"USB_DP_CONN",
    ("J5","A7"):"USB_DM_CONN",("J5","B7"):"USB_DM_CONN",
    ("J5","A5"):"USB_CC1",("J5","B5"):"USB_CC2",
    ("U8","1"):"USB_DP_CONN",("U8","3"):"USB_DM_CONN",
    ("U8","2"):"GND",("U8","5"):"VBUS_USB",
    ("R62","1"):"USB_CC1",("R62","2"):"GND",
    ("R63","1"):"USB_CC2",("R63","2"):"GND",
    ("R64","1"):"USB_DP_CONN",("R64","2"):"USB_DP",
    ("R65","1"):"USB_DM_CONN",("R65","2"):"USB_DM",
    ("J2","2"):"SD_CS_CARD",("J2","3"):"SD_MOSI_CARD",
    ("J2","4"):"3V3_SYS",("J2","5"):"SD_SCLK_CARD",
    ("J2","7"):"SD_MISO_CARD",
    ("R19","1"):"SD_CS",("R19","2"):"SD_CS_CARD",
    ("R20","1"):"SPI_MOSI",("R20","2"):"SD_MOSI_CARD",
    ("R21","1"):"SPI_SCLK",("R21","2"):"SD_SCLK_CARD",
    ("R22","1"):"SD_MISO_CARD",("R22","2"):"SPI_MISO",
    ("U1","18"):"SD_CS",("U1","19"):"SPI_MOSI",
    ("U1","20"):"SPI_SCLK",("U1","21"):"SPI_MISO",
    ("C16","1"):"3V3_SYS",("C16","2"):"GND",
    ("C17","1"):"3V3_SYS",("C17","2"):"GND"
}
for (ref,num),net in expected.items():
    assert pin(ref,num)==net,(ref,num,pin(ref,num),net)
assert '(property "Value" "5.1k 1%"' in footprint("R62")
assert '(property "Value" "5.1k 1%"' in footprint("R63")
assert '(property "Value" "USBLC6-2SC6"' in footprint("U8")
assert 'GPIO19"' in MCU and 'GPIO20"' in MCU
assert 'USB_DP_CONN' in USB and 'USB_DM_CONN' in USB
assert B.count('(footprint "')==125
segs=re.findall(r'(?m)^  \(segment \(start ([-\d.]+) ([-\d.]+)\) \(end ([-\d.]+) ([-\d.]+)\) \(width ([-\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)\)',B)
vias=re.findall(r'(?m)^  \(via \(at ([-\d.]+) ([-\d.]+)\) \(size ([-\d.]+)\) \(drill ([-\d.]+)\) \(layers "F\.Cu" "B\.Cu"\) \(net (\d+)\)\)',B)
assert len(segs)==52,len(segs)
assert len(vias)==14,len(vias)
add=[
("34.725","100.175","36.3","100.175","2"),
("36.3","100.175","36.3","96.95","2"),
("36.3","96.95","39","96.95","2"),
("39","95.05","40.8","95.05","1")
]
for a,b,c,d,n in add:
    assert any(t[0]==a and t[1]==b and t[2]==c and t[3]==d and t[5]=="F.Cu" and t[6]==n for t in segs),(a,b,c,d,n)
assert ("40.8","95.05","0.70","0.30","1") in vias
assert re.search(r'(?m)^  \(zone \(net 1\) \(net_name "GND"\) \(layer "In2.Cu"\)',B)
# Reserve GPIO17 / module pad10 for VBUS valid sensing; source pin remains NC on R39.
assert pin("U1","10")=="NC","GPIO17 VBUS-sense reservation overwritten; require review"
print("R39 USB-MSC BOARD CONTRACT PASS: native USB GPIO19/20; USB-C reversible D+/D-; CC1/2 Rd; USB ESD; SD SPI4; card 3V3 and GND pilot.")
print("RELEASE BLOCKER: battery-powered USB requires VBUS-valid monitor on GPIO17 and fail-safe/off-state electrical qualification; pad10 reserved only, NOT implemented.")
print("USB differential impedance, cable plug orientation, R64/R65 tuning, block-device ownership/MSC software and full copper remain unapproved.")
