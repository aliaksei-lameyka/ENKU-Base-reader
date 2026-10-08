# ENKU Reader R0.1 — 10 mm mechanical packaging study (2026-10-08)

Status: **engineering targets, not manufacturing approval**.

## Reference
- Display: Good Display GDEY0397T81P, active 86.40 x 51.84 mm; module 96.62 x 56.24 mm (landscape). Portrait module footprint 56.24 x 96.62 mm. Verify FPC fold, contact face and supplier tolerances using official drawing.
- R16 PCB Edge.Cuts trial: x=18..77, y=20..121 -> 59 x 101 mm (extended 7 mm at the bottom; copper/components not automatically relocated). Width is 2.76 mm wider than the portrait module. This is NOT a mechanically approved production outline.
- PCB placements (KiCad coordinates): FPC J3 (58,28), USB-C J5 (47,110.325), microSD J2 (28.9,100.7;90deg), battery J1 (66,93.5;90deg), power SW1 (30.5,29), buttons SW3/SW4 (25,63)/(25,75), SW5/SW6 (71.2,63)/(71.2,75).
- SW1 and SW3–SW6 are placeholder footprints; exact side-actuated switch and power-slide switch must be chosen before final routing.
- PCB origin is not the display origin: a mechanically registered assembly model is needed before asserting FPC reach.

## Battery candidates for envelope studies (not approved BOM)
| Option | Cell envelope (mm) | Advertised capacity | Caveat |
|---|---|---|---|
| LP304060 | 3.0 x 40 x 60 | ~950 mAh | Supplier-specific |
| LP384060 | 3.8 x 40 x 60 | ~1200 mAh | Preferred prototype envelope |
| LP404060 | 4.0 x 40 x 60 | ~1200-1400 mAh | Protected pack may reach ~62 mm length |
| LP505060 | 5.0 x 50 x 60 | ~2000 mAh | Original candidate; harder to package at 10 mm |

Sources: https://koosay.com/pages/lipo-battery-models-54 and https://www.fpbattery.com/product/3-7v-1200mah-404060-lithium-polymer-battery/ . Supplier capacity claims are not qualification evidence. Check charging termination voltage: some cells specify 4.35 V, which MUST be compatible with charger configuration; do not assume 4.2 V or 4.35 V. Require protected pack, verified connector polarity and NTC matching PMU. Battery dimensions must include protection circuit, pouch swelling clearance, wiring and tolerances.

## Mechanical constraints
1. Target external thickness 10.0 mm; stretch goal <=11.0 mm. NOT validated yet.
2. No battery contact against solder joints, exposed copper, hard component edges or display glass.
3. Retain independent battery pocket, noncompressive retention and removable back cover; do not rigidly clamp the pouch.
4. Screen supported by continuous controlled frame / compliant strips at approved support regions, never point loads on glass.
5. Prefer low-profile PCB face toward display, tall components toward back, subject to FPC bend and actual placement.
6. Use defined bosses/standoffs (prototype PETG/ASA) and insulating PET/Kapton where needed; no loose foam as primary structure.
7. Mechanical section must include bezel, glass, adhesive, clearance, PCB, component heights, pouch worst-case, rear shell, tolerance stack.
8. Verify USB-C shell opening, microSD ejection clearance, and four short side-button actuators with selected real switch footprint.
9. FPC reach is NOT validated: check 3D bend radius, strain relief, contact side, connector insertion orientation, and collision with enclosure.
10. Do not send PCBWay manufacturing package until DRC/ERC, FPC, footprint orientation, assembly stack and Gerber/drill/BOM/CPL validation pass.

## Required next deliverables
- Parametric CAD assembly: display + flexible tail + board + battery pack + real switches + USB/microSD + top/bottom shell.
- Overlay of display and board coordinate systems; compare alternative board widths and button actuation clearances.
- Battery pack sourcing sheet with exact supplier datasheet, protection/NTC, connector, tolerances and availability.
- After mechanical freeze, systematic electrical reroute, then native KiCad DRC and fabrication review.

## Mandatory side-button edge registration (2026-10-08)
- Four side-actuated tactile switches SW3/SW4 left and SW5/SW6 right. Switch bodies sit at the PCB side edge, not inboard behind long pushrods.
- The native actuator in its unpressed position must end flush with the PCB edge or protrude about 0.3–0.8 mm past the PCB edge (design target; validate against the selected part's mechanical drawing and tolerances).
- Only the moving actuator may project past the PCB edge; the switch body and solder joints remain supported on PCB. Avoid board-edge milling or copper exposure without manufacturer confirmation.
- Opposing left/right actuators must point outward; mirror placement and verify footprint rotation, pad numbering, solder access and enclosure clearance.
- External case key should have a short, guided travel with positive stops and no preload in the released state. Verify switch travel, actuation force, housing deflection and assembly tolerances in CAD.
- Current SW3–SW6 footprints are placeholders. Their current x=25 and x=71.2 coordinates do NOT demonstrate edge alignment with the trial x=18..77 mm board. Do not freeze mechanical or route to manufacturing until real side-actuated switch models are selected and edge registration is validated.

## Four shared M2 fasteners — display exclusion rule (2026-10-08)
- Assembly direction: four rear-access M2 screws through rear cover and PCB H1–H4 into front-shell structural bosses. The screws must NOT penetrate, contact, or clamp the e-paper glass, flex tail, active area or display metal backing.
- Front shell supports display independently on manufacturer-permitted perimeter areas; front shell is the load-bearing chassis, back shell removable.
- Existing H1 (30,23), H2 (71,23), H3 (23,111), H4 (71,111) use 2.2 mm M2 drills; DO NOT assume valid after board-outline expansion to 59x94 mm.
- Display portrait footprint is 56.24 x 96.62 mm. The R16 101 mm PCB nominally leaves only 4.38 mm of total longitudinal difference (2.19 mm per end if centered), before shell walls, FPC exclusion and tolerances. This does NOT prove space for top/bottom screw bosses or validate existing H1–H4. Four rear-access through-board bosses outside the display footprint require a registered 3D display-to-PCB overlay and likely a mechanical fastening redesign; do not move holes by coordinates alone.
- Candidate architecture A: extend PCB and shell length for top/bottom fastening tabs beyond the display, while maintaining narrow side bezels. Candidate B: side-offset fastening tabs outside display width, which widens case and conflicts with side buttons. Compare with full display outline including FPC tail and shell wall thickness.
- For M2 inserts, boss outer diameter and insertion depth MUST come from chosen insert datasheet and print process; 4–5 mm is only an early envelope. Validate minimum edge distance, copper keepout, drill tolerances and driver access.
- Do not relocate H1–H4 by coordinates alone; preserve connectivity, zone refill and run KiCad DRC after a complete mechanical overlay. Freeze no Gerbers until checked.

## R16 integration checkpoint (2026-10-08)
- PCB outline extended to 59 x 101 mm; R6 GND pad now has a candidate F.Cu route around its MUX_OV1 pad to existing via (70.4,81.2), pending native DRC and copper-zone refill.
- No change to frozen two-left/two-right side-button ergonomics. The button footprints remain placeholders and lack checked actuator direction/edge registration.
- Current screw holes H1–H4 remain provisional; **do not** claim they clear the display or make PCBWay fabrication outputs from this trial.
- One native CI run is required to assess any newly introduced copper-edge, drill and routing violations; previous failures are not automatically cleared by enlarging the outline.
