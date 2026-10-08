# ENKU Base R37 — readiness to PCBWay

**30/100 planning estimate. NOT FAB READY.**

R37 implements second partial copper pass: 38 route segment objects (R36 had 19), 6 Ø0.7/0.3mm through vias (R36 had 1), 125 KiCad footprints. Local charger U3 SYS to Q2 source, VSYS bypass C7, 3V3 U4 output to C11/C12, TP6 and R14 pilot. No GND-zone or EPD/FPC routing.

R36 actual Native [37803618133](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37803618133) validated ERC 0, schematic parity0, non-unrouted DRC236, unrouted260, no short/dangling. **R37 verified**: [Native KiCad run 37804889329](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37804889329) confirms ERC **0 errors / 0 warnings**, PCB↔schematic parity **0**, critical shorts / copper-edge / mask bridges / dangling tracks **0**, **236 non-unrouted DRC** and **254 unrouted**. [Structural run 37804889092](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37804889092) passed.

Blocking: GND copper planes/returns, 3V3 rails to MCU/SD, LiPo/BQ current path thermal and PMOS inrush, actual slide switch MPN and footprint, EPD HV + Good Display FPC pin5 contradiction, final mechanical envelope/side buttons and full 4-layer complete routing, DRC0, Gerber/BOM/CPL.

No filled ground plane exists in R37; ground return and load thermals remain critical blockers. **30/100 readiness unchanged.**
