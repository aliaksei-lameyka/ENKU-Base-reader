# ENKU Base PCBWay readiness R46 — Native verified two left GPIO buttons

**PCBWay Ready planning 30/100. No production release.**

Active source `hardware/mainboard/kicad/enku-mainboard-r2.3-base-left-button-signals.kicad_pcb`; 132 footprints, 483 copper segments, 128 plated through-vias, 2 editable inner GND polygons.

**Native verification:** [R46 KiCad DRC/ERC 37895191252](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895191252) **SUCCESS**, KiCad ERC **0 errors / 0 warnings**, schematic parity **0**, priority shorts/clearance/hole/mask/dangling **0**, new BTN_L1/BTN_L2 Native electrical unconnected **0**. [R46 structural run 37895191246](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895191246) **SUCCESS** with full PCB pad/via collision checks and old MCU, SD, USB VBUS, SW1 regressions.

**Residual: 141 unconnected items** (R45 143), **224 other DRC violations** (130 mismatched library footprints; 67 silk-over-copper; 27 silk overlap). `text_height` remains 0. Full DRC remains **NOT PASS**.

MCU U1 pad4 BTN_L1→SW3 pad1 and U1 pad5 BTN_L2→SW4 pad1 physically routed via In1.Cu. Left and right button grounds native-connected since R43. **RIGHT BTN_R1 and BTN_R2 signals are unconnected**, do not count all 4 buttons finished. SW3–SW6 still provisional placement footprints; final component and case shaft/actuator mechanical qualification required.

Unreleased: USB 2.0 FS D+/D− 90Ω impedance qualification and copper, USB MSC firmware/card handoff tests, Good Display pin5 VDHR vs VSH2 written clarification, actual FPC mating/rotation, 141 unrouted, 224 DRC, vendor-reviewed pads/MPNs, LiPo charge/off/noise checks, manufacturing BOM/CPL/Gerber/NC drill and 3D assembly.