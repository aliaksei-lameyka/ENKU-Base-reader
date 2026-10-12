# ENKU Base R33 — switched VIN regulator experiment

**Not fabrication ready; not fully battery isolated.** Variant `engineering/r33-switched-vin-power-gate` sets physical switch SW1 between BQ25185 SYS output (VSYS) and the main buck-boost's complete input domain (legacy SYS_EN net): U4 TPS63802 VIN pin 10, EN pin 1, C9 10uF and C10 100nF. R13 100k discharges/grounds SYS_EN when off. U4 output remains 3V3_SYS. Charger BQ25185 SYS and VBAT remain connected to supply charger and permit battery charging while mechanical switch is off (test physically).

Prior R32 mechanically switched only EN, while U4 VIN and C9/C10 stayed live. This revision **really opens the reader load feed** ahead of the converter; it is *not* a galvanic battery disconnect and must never be advertised as one. Real switch pad/MPN ratings, LiPo-side inrush and turnoff/discharge remain unverified.

### Critical off-state hazard, NOT corrected
Direct VBAT->R26 2M->BAT_ADC->R27 680k->GND divider remains powered when ESP32 supply 3V3_SYS=0. It can leak a small DC current and may bias/phantom-power MCU GPIO via its clamps. Power-state measurements (3V3_SYS, BAT_ADC, CHG_STATs, USB, dock) plus viable switched-divider circuit needed before fabrication. In addition, verify BQ25185 pushbutton/TS/MR charger mode and quiescent battery current, protected pack, NTC and matching PH cable.

### Good Display 3.97 inch
Panel GDEY0397T81P spec page 6 pin5 **VDHR**, but vendor typical application schematic page19 calls corresponding contact **VSH2**. Our J3 pin5 is currently EPD_VSH2. No unapproved change; written vendor confirmation required. J3 pin15 VDDIO 3V3_SYS, pin16 VCI EPD_VCI are joined by **populated R28 0R**, complying with vendor requirement; all NC pins 1,4,6,7,19 kept unconnected.

### R33 source and checks
- `power.kicad_sch`: exactly three SYS_EN vs VSYS corrections on regulator input and two input capacitors. Charger SYS and switch input are VSYS.
- `enku-mainboard-r1.0-base-switched-vin.kicad_pcb`: U4 pad10, C9 pad1, C10 pad1 now electrically on switched SYS_EN net, no copper routing. 120 components.
- CI `check_r33_power_domains.py` guards the topology and entire 24-pin FPC; `check_r33_assembly.py` reruns R32 all-pad clearance checks **against R33 active board**; native KiCad ERC and schematic parity/DRC diagnostic in separate workflow.

**Do not increase PCBWay percentage until hardware sign-off.** No 3D FPC fold, switch selected footprint, RF antenna physical keepout, actual glass-safe bolts, routed 4-layer board, production BOM or Gerbers.
