# ENKU Reader R25 — Placement-first re-layout (59 × 101 mm)

**Status: mechanical/electrical placement study; not ready for manufacturing.**
Branch: `mechanical/r25-placement-first`, base `validation/base-r01-import` @ `a74bf83`.

## Why restart only PCB routing

R0.1 board has 122 physical footprints, 717 line segments, 217 vias, 2 GND zones, and 659 native DRC violations at the last checked baseline. The DRC violations include shorted unrelated nets, crossings, bad hole clearances and routing conflicts. A clean mechanical placement has to fix currently inward-facing J2 microSD entry, recessed J5 USB-C, provisional side buttons and screw-hole/display overlap. Preserving the previous copper adds constraint but no product value.

Preserve existing **schematic**, net names, chosen power architecture for engineering review, device functionality, BOM register, sourcing evidence, test tooling, footprint libraries and version history. Audit schematic electrical correctness before routing; green structural ERC is not power-integrity validation.

## New real KiCad artifact

`enku-mainboard-r0.2-placement.kicad_pcb` is a separate copy, not a destructive edit of R0.1:
- Board outline retains x18…77, y20…121 = **59 × 101 mm**.
- All **122** footprints copied unchanged except the two provisional access-critical moves below.
- Strip all **717** existing copper segments, **217** vias, **2** GND pour zones from the R25 copy. Net names/pad connectivity remain associated with schematic, but physically all nets unrouted by design.
- J2 microSD candidate: **x26.1 y100.7, 270°**, to face opening toward left side; correct mating distance, body courtyard, ejection stroke, pin-1 and holes must be checked with Hirose STEP before locking.
- J5 USB-C candidate: **x47.0 y117.325, 0°**, moves connector **7 mm down** so its original documented board-edge datum aligns with new y121.0; verify body overhang, NPTH tabs, enclosure thickness, J2 and mounts before locking.
- All other footprints, including SW3…SW6, J1, SW1, H1…H4, remain **provisional** and must be re-placed. No claim that board is placed correctly yet.
- GND zones must be drawn AFTER the mechanical positions are approved; 4-layer return planes and EPD high voltage still need a coordinated stack design.

## Mandatory mechanical constraints / sequence

### Step 1 — lock global geometry and assembly datum
1. Actual Good Display GDEY0397T81P 56.24 × 96.62 mm module incl. FPC origin, tail bend and connector insertion axis.
2. Compact portrait geometry with no wide front side grips; board size 59 × 101 is a **candidate**, not irrevocable if engineering dictates a change.
3. 1S protected LiPo pocket, NTC/cable/plug direction and 10 mm nominal case thickness; locate battery relative to stacked PCB and display, not inside its copper regions.
4. Approved plastic screw boss / rear screw architecture independent of display glass. Existing H1–H4 overlie **nominal centered display projection**: may not be retained as screen-bearing screw axes without proven independent mechanical standoffs.
5. Shell edge controls: two page buttons on **each left/right side**; left handed and right handed. True side actuation. Recessed C915811 with LCSC ID C915811 remains EVAL until vendor pocket/land drawing, 3D and PCBWay DFM approval.

### Step 2 — place externally constrained parts
Place/verify J3 FPC, J2 microSD, J5 USB-C, side buttons, SW1 hard power, dock contacts J6, battery J1, antennas/keepouts, Hall sensor and selected magnet. Check connector cable/card/plug directions with supplier CAD.

### Step 3 — place dependent circuit blocks (without routing)
- MCU U1 with antenna overhang/keepout clear of metal and battery.
- PMU/power mux/charger/buck-boost U2–U4, their power inductors and capacitors in **actual datasheet application layout proximity and pin-1 direction**. Verify thermals/loop current.
- EPD high-voltage converter and its isolated local loop, signal interface and frontlight connector/cable.
- IMU away from magnets, EMI hotspots and board flex.
- ESD immediately at actual J5 VBUS/D+/D− connector entrance.

### Step 4 — DFM / fit audit BEFORE routing
Mechanical CAD overlay: display FPC, battery, board, mount hardware, all SMT Z heights, SD insert/remove direction, USB plug and shell wall, finger button travel, soldering access and antenna no-metal exclusion. Reconcile all 122 BOM/footprint/polarity orientations by original manufacturer drawing, prefer China/PCBWay supply.

### Step 5 — routing from an actually frozen placement
Power VBAT/VSYS/3V3, ground return and decoupling, sensitive USB data/ESD, EPD HV, SD, MCU/control, remaining signals. Rebuild ground planes with proper return-path continuity; route and DRC in milestones. Use schematic parity and visual 3D each phase.

## Non-negotiable validation gates
- `python hardware/mainboard/kicad/check_r25_placement_canvas.py`: asserts new board has 122 footprints, valid 59×101 outline, zero copper or zones, only two provisional connector shifts. This is **not** a DRC gate.
- `check_component_manifest.py --release` applies only after it has been updated for new R25 coordinates and supplier proof; **current R0.1 registry stays unchanged**.
- Before manufacturing: native ERC+full DRC + schematic parity; KiCad zone refill; mechanical release audit; real manufacturer STEP/PnP, Gerber/NC drill, BOM/CPL, PCBWay DFM. Existing PR #2 switch EVAL must not be merged indiscriminately.

## Legacy references retained
- `enku-mainboard-r0.1.kicad_pcb` still exists and is untouched in this branch, for forensic comparison and circuit routing clues.
- The 4-contact C915811 button trial remains separate in `research/r24-c915811-4pin`; that experiment had a poorer DRC and should not be treated as production baseline.

**Do not attempt PCBWay fabrication or send Gerbers from this placement study.**

## R25B — holes and fastening anchors (physical in KiCad)

Moved and preserved four **2.2mm NPTH M2**: H1 (23,25), H2 (72,25), H3 (23,116.5), H4 (72,116.5). Added 5.5mm nominal boss/head study circles and the centered 56.24×96.62mm display outline on `Dwgs.User`. J5 includes its existing **2 NPTH + 4 shield PTH slots** at the new location. No unnecessary drilled 'button holes' or microSD hole inserted in PCB; those require case cutouts and vendor-qualified edge pockets.

**All four screw axes project beneath the nominal centered display**. These are rear-access *candidate* load paths only, not screen-bearing screws. The enclosure must keep the screen unstrained and maintain FPC and battery clearances; otherwise revise to rear rails/clips or move attachment to another layer of the enclosure. See [R25B holes, access and fastening register](MOUNTING_DRILLS_R25B.md).
