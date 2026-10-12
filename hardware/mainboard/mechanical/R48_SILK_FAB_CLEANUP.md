# R48 — manufacturable silkscreen vs Fab documentation contours

R47 manufacturer-visible geometries contained **43 printed body rectangles** crossing soldermask exposed pads across passives, SW1/SW3..SW6, service pogo dock J6 and MOSFET Q1. Those rectangles were misplaced in **F.SilkS/B.SilkS**, so KiCad detected silk clipped by soldermask and silhouette collisions. R48 keeps each outline on **F.Fab/B.Fab** for mechanical assembly and BOM inspection, while retaining actual footprint reference designators, D1–D3 cathode indicators, 14 B.SilkS repair labels, RF antenna marker and ENKU open-hardware identity.

**No copper, pads, vias, GND zones or center coordinates changed from R47.** Board: `hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb`. 43 transferred text/graphic shapes on 43 footprints. This is a documented prototype PCB-only local adjustment; the local/reference manufacturer footprint libraries still require reconciliation before release.

Native KiCad [run 37898825797](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825797) successful ERC0, critical0, remaining 139 unconnected, **224→168 DRC** (94→38 silk), 130 footprint mismatches unchanged. [Structural 37898825577](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825577) success. Full DRC not passed.
