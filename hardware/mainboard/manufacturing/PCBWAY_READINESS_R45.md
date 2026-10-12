# ENKU Base R45 — Native-verified production-readable PCB labels

**PCBWay Ready: 30/100 planning estimate (unchanged). PCB production release BLOCKED.**

Active branch `engineering/r45-silkscreen-readability`; board `hardware/mainboard/kicad/enku-mainboard-r2.2-base-silkscreen-legibility.kicad_pcb`. 132 footprints, 471 copper segment records, 124 plated vias, 2 native-filled inner GND reference zones. R44 copper topology preserved.

## Verified tests

- [R45 Native KiCad 8 run 37893987801](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893987801): **SUCCESS**, strict ERC **0 errors / 0 warnings**, PCB↔schematic parity **0**, critical shorts/mask/edge/hole/dangling **0**, both GND fills retained and control-gate source geometry checked.
- [R45 structural regression 37893987966](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893987966): **SUCCESS**, all testpoint names, RF label and rear board identity now 0.8mm, no new via drill on a SMD pad, MCU power/USB VBUS/microSD control topology unchanged.
- **0 `text_height` DRC violations**, reduced from **16 in R44**. Other DRC reduced **239→224** (net −15), because 14 probe labels and two board/antenna inscriptions were made larger without disabling the KiCad minimum.
- Remaining **224 non-unrouted violations**: **130 `lib_footprint_mismatch`**, **67 `silk_over_copper`** and **27 `silk_overlap`**. **143 unconnected items** (unchanged from R44). `footprint_errors` 0. Full native DRC still **FAILS**, despite successful strict priority gate.

## Next high-value work

1. Resolve **130 real library footprint mismatches** with original vendor drawings, especially diode cathode pads, physical switch placeholders, microSD connector and regulated ICs. Avoid blanket copy-from-library that destroys custom pad geometry/polarity or ignores current KiCad library version.
2. Repair 94 specific silk line/text collisions and mask clippings; maintain visible user-service reference labels, adequate 0.8mm height and manufacturer legibility.
3. Route four reader-input nets SW3..SW6 from ESP32, verify actual side-actuator MPN+case. USB-C D+/D− 90Ω physical differential pair still not routed pending PCBWay stackup. USB MSC software/desktop testing incomplete.
4. Validate 102mm high-impedance SW1 PWR_GATE long-run switch bounce, leakage, EMI and charging while hard OFF; confirm 1S battery+NTC/charger and thermal headroom.
5. Await Good Display written pin5 VDHR/VSH2 and stepped FPC clearance, finish panel HV and MCU peripheral routing; full DRC0/ERC0/assembly test/PCBWay verified BOM-CPL/NC drill/Gerbers required.

**Never infer fabrication-ready from priority-only successful GitHub Actions.**