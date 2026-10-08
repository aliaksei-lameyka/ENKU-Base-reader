# ENKU Base — PCBWay readiness R30

**2026-10-08: 30/100% (engineering estimate, unchanged). Fabrication BLOCKED.**

Weighted inherited R29 baseline: architecture 9/10; schematic/power 11/20; mechanical 5/20; source footprints 3/15; routing 2/25; production 0/10.

Proposed R30 source corrections: J7 rear manufacturer no-paste contact pads + 3 NPTH registration holes, SW2 move to y79, J6 exposed dock pad stencil exclusion, CI guard and Native KiCad R30 input. **New native counts not yet measured.**

Last genuinely measured R29: 120 components, 240 non-unrouted DRC issues, 252 unconnected, schematic parity 0, 119 footprint library mismatches, 55 pad differences, 1 missing J1 library.

NEXT: Native R30 DRC+ERC, contact pad and hole clearance, physical backward/mirrored programming cable pin1, battery/jig clash, complete copper routing and full PCBWay approved AVL/BOM/gerber/NPTH drill package.

No Pro Qi/Hall/frontlight production features belong on Base.
## R30 parity correction

Schematic J6 `in_bom no` aligns with bare dock pad J6 PCB BOM exclusion. PCB J7 value restored to `Tag-Connect TC2030-IDC-NL`, matching its original symbol while no-paste/DNL manufacturing stays enforced. Both corrections are pending a new Native KiCad parity run; this is not yet DRC signoff.

## Verified R30 Native KiCad snapshot (commit 4da1648)

Run [37790938942](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37790938942): 120 PCB footprints, 252 unrouted connections, 0 schematic parity violations, 0 critical shorts/copper-edge clearance faults, 240 other DRC violations (119 lib_footprint_mismatch; 1 lib_footprint_issues J1; 68 silk_over_copper; 36 silk_overlap; 16 text_height), footprint_errors 0. Schematic/structure CI [37790938828](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37790938828) passed. Native job success is a **diagnostic success, not a DRC pass**. Native ERC output also exists in workflow artifact; no production signoff.

The initial R30 Native run had 2 PCB/schematic parity errors (J6 BOM attribute, J7 value) and the next verified Native run has 0 after a targeted schematic + PCB fix.

Espressif-source inspection establishes that U1's apparent +3mm local-Y pad offset compared with Espressif's library is also present in the entire F.Fab body reference, so a translated local footprint origin is **not evidence of pad displacement**. Do not shift U1 pads alone. Still vendor-check pin 41's custom 12 drilled GND via-in-pad features and stencil/tenting; manufacturing-qualified antenna keepout remains open. See [manufacturer-relative U1 audit](../mechanical/R30_ESP32_FOOTPRINT_AUDIT.md).
