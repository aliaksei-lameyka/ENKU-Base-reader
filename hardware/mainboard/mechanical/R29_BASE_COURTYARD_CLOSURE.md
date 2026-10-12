# R29 Base: placement-first mechanical closure

Status: **reviewable copper-free experiment, not fabrication-ready**. Active Base architecture: dedicated no-Hall/no-Qi/no-frontlight panel, Good Display 3.97in with unusual FPC, ESP32-S3 + BMI270.

## Physical error detected and fixed

R28 board contained **three confirmed F.CrtYd collisions** with Hirose microSD J2:
- R19 (30,101) in J2 body → (37,101), rotation 0.
- R20 (30,104) in J2 body → (37,104), rotation 0.
- R21 (32.8,105.5) in J2 body → (37,107), rotation 0.

The J2 courtyard from the actual R25 KiCad footprint in left-facing 270° configuration is nominal x17.22..34.92, y92.88..108.58. Physical J2 courtyard extends 0.78mm beyond PCB x18, which is **intended card mouth**, not authorization to machine PCB or claim shell fit. R19–R21 moved to right (x37), still electrically adjacent for later SD tuning. R22 stays at (30,110) clear of J2 body. All distances need real Hirose STEP validation.

New **R29 board**: `enku-mainboard-r0.6-base-placement.kicad_pcb`. All 120 parts preserved, J3 candidate (69.37,34), M2 H2 (57.5,25), R27 stepped Good Display flex silhouette (from page 5 manufacturer PDF) preserved. No routing, via or pour.

**R29 courtyard CI** parses every native F/B.CrtYd rectangle from KiCad PCB and generates world 2D bounding boxes after rotation. It requires exactly the three expected old collisions and zero new collisions; checks screw Ø5.5mm study head/boss clearance against front-side courtyards; detects unauthorized body overhang beyond board except J2/J5 intentional mouths. This covers only those footprints with explicit CrtYd rectangles; any component without reliable supplier geometry is still a hardware sign-off blocker. Current status must never be mislabelled “all 120 3D mechanically verified.”

## Open production blockers beyond courtyard overlap

1. Good Display exact `FPC-7750` stepped ribbon contour modeled on `Dwgs.User`, **not real folded 3D**. Official DXF/DWG, fold radii and contact-facing stiffener still required. J3 x69.37 y34 is only a projected candidate, not approved.
2. Hirose J3 and J2 authentic 2D/STEP models already shared by owner in Archive.zip, but must be placed and checked with shell to resolve latch access and microSD travel. J5 body and cable boot still need physical review.
3. H1–H4 all sit under glass projection; screw preload must transfer to rear structural frame and not glass. H2 actual (57.5,25) after R26 remains unproven against stepped FPC.
4. SW3–SW6 physical recessed C915811 require real manufacturer pad numbering, dimensioned Edge.Cuts pockets, assembly tolerance and shell actuator geometry. R24 research must NOT be merged blindly.
5. PCB has initial J1 battery connector and hard SW1 placeholder, no exact approved physical vendor components. Battery expansion, insertion and service not yet modeled.
6. USB-C GCT and EPD HV real 3D/signal route, ESP32 antenna no-copper keepout, outer display FPC land and B.Cu dock access require separate test.
7. EPD **pin15 VDDIO = 3V3_SYS; pin16 VCI = EPD_VCI linked via R28 0R** (sheet epd_hv). Good Display spec p6 says VDDIO to VCI. With R28 populated, these are electrically bridged, but no-dnp/solder-incomplete and voltage sequencing must be validated. Pin5 VDHR vs VSH2 mismatch vendor pp5-6 vs p19 unresolved.
8. Run the **new variant's** native KiCad ERC, schematic parity and full DRC once placement frozen. Existing legacy R0.1 ERC/DRC checks do not certify R29.
9. Must get actual PCBWay sourced MPN and full release for every component. 120 footprints only, no manufacturer-approved assembly.

## Workflow

After mechanical freeze, re-organize local power loops and reroute copper from blank placement in controlled stages. Do not resurrect original R0.1 717 tracks / 217 vias.
