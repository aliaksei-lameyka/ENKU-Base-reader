# ENKU Base PCBWay R47 manufacturing readiness

**30/100 planning readiness — NOT READY FOR FABRICATION.** Source `enku-mainboard-r2.4-base-four-reading-gpios.kicad_pcb` has 132 footprints, 515 routed segments, 132 plated vias, two GND polygons. BTN_R1 and BTN_R2 electrically routed to right SW5/SW6 provisional case-edge buttons, supplementing left SW3/SW4 complete GPIO copper on R46. **Active Native DRC not yet qualified** for this R47 source.

Verified baseline [R46 37895191252](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895191252): ERC0, priority DRC0, 224 non-unrouted violations and 141 unconnected. No yield/production claim without Native R47.

Still blocked: real side switch footprint/case clearance, RF keepout and return plane, MCU to other subsystems unconnected, full DRC=0, 90Ω USB2 pair + host USB MSC firmware, GDEY0397T81P pin5 VDHR/VSH2 manufacturer confirmation/FPC fold, all BOM/CPL/Gerbers/drill and assembly inspection.
