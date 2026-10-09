# PCBWay readiness R46 — left reading button I/O

**Planning readiness: 30/100. FAB RELEASE BLOCKED.** Source `enku-mainboard-r2.3-base-left-button-signals.kicad_pcb` with 132 footprints, 483 segments, 128 vias, two GND reference polygons.

R46 provides two routed left-side reader input signals (`BTN_L1` ESP32 U1 pad4 → SW3 pad1; `BTN_L2` U1 pad5 → SW4 pad1). Native R46 ERC and DRC still pending; no release claim based on source geometry alone. Right-side signals BTN_R1/BTN_R2 remain unconnected and side switch manufacturer/part identity not locked.

R45 final verified [Native 37893987801](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893987801): ERC0, priority DRC0, 224 other DRC issues including 130 library mismatches + 94 silk, 143 unrouted. R46 will report exact outcomes after full filled native DRC.

Major blockers: 2 other GPIOs, full DRC0, USB D+/D− under PCBWay stackup 90Ω, USB MSC firmware/host tests, verified footprint pad libraries/real side switch/PMOS EMI, display supplier disputed pin5 VDHR/VSH2 plus FPC, BOM/CPL/Gerber/NC drill and actual assembly tests.
