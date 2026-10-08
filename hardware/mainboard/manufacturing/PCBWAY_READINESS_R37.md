# ENKU Base R37 — readiness to PCBWay

**30/100 planning estimate. NOT FAB READY.**

R37 implements second partial copper pass: 38 route segment objects (R36 had 19), 6 Ø0.7/0.3mm through vias (R36 had 1), 125 KiCad footprints. Local charger U3 SYS to Q2 source, VSYS bypass C7, 3V3 U4 output to C11/C12, TP6 and R14 pilot. No GND-zone or EPD/FPC routing.

R36 actual Native [37803618133](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37803618133) validated ERC 0, schematic parity0, non-unrouted DRC236, unrouted260, no short/dangling. **R37 separate Native test pending; do not carry R36 measurements as proven R37 status.**

Blocking: GND copper planes/returns, 3V3 rails to MCU/SD, LiPo/BQ current path thermal and PMOS inrush, actual slide switch MPN and footprint, EPD HV + Good Display FPC pin5 contradiction, final mechanical envelope/side buttons and full 4-layer complete routing, DRC0, Gerber/BOM/CPL.
