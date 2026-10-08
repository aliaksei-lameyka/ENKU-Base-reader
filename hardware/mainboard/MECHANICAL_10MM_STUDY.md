# ENKU Reader R0.1 — 10 mm mechanical packaging study (2026-10-08)

Status: **engineering targets, not manufacturing approval**.

## Reference
- Display: Good Display GDEY0397T81P, active 86.40 x 51.84 mm; module 96.62 x 56.24 mm (landscape). Portrait module footprint 56.24 x 96.62 mm. Verify FPC fold, contact face and supplier tolerances using official drawing.
- Current PCB Edge.Cuts: x=18..77, y=20..114 -> 59 x 94 mm. This is a trial width, NOT mechanically approved; 59 mm is 2.76 mm wider than the portrait display.
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
