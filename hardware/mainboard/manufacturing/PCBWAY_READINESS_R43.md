# ENKU Base R43 — verified reading control return grounds

**PCBWay Ready 30/100 (planning estimate, no increase). MANUFACTURING / ASSEMBLY RELEASE BLOCKED.**

## Source and actual Native proof

- Active branch `engineering/r43-reading-button-ground-returns`. Editable KiCad board: `hardware/mainboard/kicad/enku-mainboard-r2.0-base-reading-ground-returns.kicad_pcb`.
- **132 placed footprints, 442 KiCad copper segment records, 121 plated vias, 2 inner GND zones.** Four SW3..SW6 GND return vias and three nearby C26/C18/C19 local GND links are real PCB data, not only documentation.
- [Native KiCad 8 zone fill / ERC / DRC run 37843277589](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37843277589): **SUCCESS**, verified ERC 0 errors / 0 warnings, PCB↔schematic parity 0, priority shorts / clearance / mask / via / track dangling errors 0, **SW3..SW6 pad2 GND native unconnected 0** after native zone refill. **146 remaining unconnected items, 239 other DRC violations**. Full board DRC still FAILS.
- [Structural/component/geometry tests 37843220711](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37843220711): **SUCCESS**, pad collision 0, **zero new via drills intersect SMD pad lands**, existing R42 power/USB VBUS/microSD connected-component regressions pass.
- DRC non-unrouted 239 remains the active **manufacturer release debt**, not a harmless warning count; previous R42 239 and 152 unconnected.

## Defect found during DFM iteration

Initial SW3 stitch at (28,65.2) **intersected C31 pad1 EPD_VCI**; the first structural/native runs correctly failed on via-in-SMD-land. Moved SW3 via to **(28,67)**, changed short F.Cu return angle and reverified Native KiCad. Initial failed attempts were not treated as approval. Active Native gate now also explicitly checks all four switch-pad GND connectivity after fill.

## Remaining high-priority issues

- **146 unconnected connections**. Four button signal nets BTN_L1/L2/R1/R2 are still physically unrouted because dense U1 lower-pad power/BOOT fanout and module/antenna clearance require careful escape. SW3..SW6 are **placement-only** switch footprints, not yet actual MPN/actuator qualified. Do not order assembled PCB with them.
- **SW1 power switch PWR_GATE physical copper not complete** (remote x27.3,y29 to Q2 gate at x54.5,y81.55); opening switch controls PMOS gate only, charger and cell remain alive. SW1's matching actual slide MPN/case dimensions unqualified.
- USB2 full-speed native D+/D− pins J5 ↔ U8 ↔ R64/R65 ↔ ESP32 are netlisted but **UNROUTED** and require controlled 90-ohm nominal differential routing against actual PCBWay 4-layer stackup, plus USB host MSC firmware/storage ownership tests. VBUS-safe comparator exists but requires OFF/backfeed/threshold runtime bench verification.
- 239 non-unrouted DRC, custom footprint library deviations, repairable readable silkscreen, voltage and layout integrity, LiPo thermal/charge, mechanical SD insertion, GDEY0397T81P pin5 VDHR vs VSH2 manufacturer confirmation and actual FPC/connector fold. Good Display written answer still outstanding.
- Real PCBWay-ready package requires full native DRC 0 (not only priority), ERC0, netlist parity0, validated 3D/mechanics, BOM/MPN, PnP/CPL and Gerber/NC drill and assembly review. Never make manufacturing package from this source yet.

Development hours: no trustworthy automated stopwatch source; do not invent time spent.