# ENKU Base R38 PCBWay readiness

**30/100 preliminary, FABRICATION BLOCKED**. Source `enku-mainboard-r1.5-base-ground-return-island.kicad_pcb`.

R38 = 48 copper track segments, 13 through vias, one bounded In2.Cu GND zone polygon, still 125 footprints. Seven local GND stitching/return vias at U3 charger, U4 regulator, C9/C10, C11/C12.

[R37 KiCad Native baseline](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37804889329): ERC0, parity0, 236 non-unrouted violations, 254 unrouted. R38 Native outcome **pending**. Do not claim GND polygon is actually filled until KiCad fill verified. R38 specifically scoped away from uncertain Good Display FPC and pin5, prior email awaiting answer.

Blockers: all 4-layer copper and complete netlist; floating/isolated ground plane islands, ground return thermal/current measurements, charger status and ESP32 ADC off current, true actual SW1 manufacturer footprint/actuator, GoodDisplay 3D FPC/pin5, cell+NTC, PMOS SOA/inrush, BOM/PnP/NPTH/drills/paste/panel.
