# ENKU Base R45 — readability audit and PCBWay readiness

**Planning estimate 30/100; manufacturing BLOCKED.**

Active board `hardware/mainboard/kicad/enku-mainboard-r2.2-base-silkscreen-legibility.kicad_pcb`, from R44 validated [Native 37893508039](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893508039) (ERC0, parity0, critical0, 239 other DRC, 143 unconnected). Actual 132 footprints, 471 segments,124 plated vias,two inner GND zones. No copper changes in R45.

R45 changes **16 factory-out-of-range 0.55/0.6mm user service/antenna/board labels** to readable 0.8mm font without suppressing KiCad DRC minimum. Native R45 still pending. Need verify no new overlap/copper mask contact introduced.

Remaining: 143 unrouted; 4 reader GPIO inputs; USB D+/D− and PCBWay manufacturer-confirmed 90Ω impedance; hardware SW1 long gate noise/ESD; actual footprints incl switches; Good Display pin5/FPC manufacturer answer; full ERC/DRC0 incl library mismatches/silk; BOM/CPL/Gerber/NC drill, solder/power/EMC and USB MSC desktop tests.
