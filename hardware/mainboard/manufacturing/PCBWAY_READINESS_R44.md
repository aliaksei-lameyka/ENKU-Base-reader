# ENKU Base PCBWay manufacturing readiness R44

**Planning score: 30/100; NOT FAB READY.** Active source `enku-mainboard-r2.1-base-sw1-gate-trial.kicad_pcb`.

R44 implements preliminary, fully connected KiCad PWR_GATE copper from case SW1.1 to high-side Q2.1/R40.2 and remote SW1.2 to the two inner GND fills. Board holds 132 footprints, 470 track records, 124 PTH vias, two editable In1/In2 GND polygon definitions. Native KiCad R44 validation pending at this commit; do not treat source topology checks as full DRC proof.

R43 audited baseline [Native 37843277589](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37843277589): ERC0, parity0, critical0, **239 non-unrouted DRC** and **146 unconnected**.

**Major blockers:** 4 side-button input signals U1→SW3..SW6 still unrouted, long high-Z SW1 gate/ESD/off leakage needs measured qualification and final footprint MPN, USB-C D+/D− differential routing 90Ω per actual PCBWay stackup, firmware MSC and SD ownership host tests, GoodDisplay manufacturer pin5 VDHR/VSH2/FPC hold, full DRC and grounded return plane, supplier/case/repairability BOM/PnP/Gerbers. **No Gerber and no percentage increase.**
