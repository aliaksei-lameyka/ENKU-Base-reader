# ENKU Base R43 — PCBWay readiness and gate results

**Planning estimate: 30/100, NOT READY FOR PCBWAY.** Active source `hardware/mainboard/kicad/enku-mainboard-r2.0-base-reading-ground-returns.kicad_pcb`.

As of R42 verified Native run [37836929374](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37836929374): ERC0, PCB schematic parity0, critical0, **239 other DRC violations and 152 unconnected**. R43 changes four reading-button GND/return vias and ties C26/C18/C19 local return pads; R43 Native outcome pending. New R43 source is 132 footprints, **442 segments**, **121 vias**, two inner GND reference polygons.

**Important:** side-button signal GPIO nets, hard-power slide gate, USB-C D+/D− signal pair and most panel-related routes still unrouted. Mechanical button footprints are placeholder representations; no purchaser-validated exact MPN/3D. VBUS monitor uses fail-safe TLV3012B; test OFF backfeed and USB runtime MSC handover. Good Display pin5 VDHR/VSH2 and FPC still await written confirmation. Production DRC, 3D, pad library mismatches, silkscreen, BOM/CPL, power-up and host tests still unresolved.

**Source guards cannot replace real KiCad zone fill + ERC/DRC**. See [R43 physical return design](../mechanical/R43_BUTTON_RETURN_GROUND.md).
