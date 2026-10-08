# ENKU Reader — PCB / case integration gate R09

Date: 2026-10-08. Branch validation/base-r01-import.

## Verified from current KiCad PCB

- Edge.Cuts rectangle x=18..77, y=20..114: **59 × 94 mm**.
- MountingHole:MountingHole_2.2mm_M2 footprints H1–H4 exist, but are not mechanically approved for the asymmetric case.
- J3 display FPC, J2 microSD, J5 USB-C, U1 ESP32-S3-WROOM-1 are placed on the PCB.
- SW1 hard power and SW3–SW6 side keys are **placement placeholder footprints**, not selected/validated manufacturer switch footprints.
- The housing's two lower M2 fasteners are independent of H1–H4; front frame carries the display. Do not move the board mounting holes into the glass footprint.

## Integration decisions

1. **Do not blindly shift H1–H4** or extend PCB to 110 mm: it would break mechanical/placement assumptions without fixing the electrical DRC. First import the real display/FPC outline, the Fusion STEP enclosure, actual switch packages, and the chosen battery pack into a single coordinate frame.
2. Design PCB retention independently of case closure. Candidate: PCB seated on molded lateral guide ledges and held by two serviceable fasteners in accessible non-display-overlap regions, or an internal carrier frame. Neither option is approved until sections prove no contact with display.
3. Preserve four side-actuated buttons with native plungers flush/slightly proud of board edges. Replace placeholders with exact switch footprints before board-edge routing and key design.
4. The 40 × 60 × 3.8 mm battery envelope collides in XY with the approximate U1 region. **No component relocation can be approved on XY alone**; determine PCB component heights and Z-side, battery swelling and protection circuit, then evaluate safe volume.
5. Prioritize manufacturing blockers: existing DRC short/crossing/clearance issues, exact connector orientation, mounting, battery pocket and enclosure stack. No Gerbers until native KiCad DRC and mechanical section are clean.

## Required next deliverables

- Component placement report with absolute KiCad XY, side and height, plus envelope overlays in Fusion.
- Side-switch selection and edge orientation with actuation envelope.
- Two candidate PCB retention schemes dimensioned in the R08 Fusion model; pick one by actual clearances.
- Battery + ESP32 packing study with exact chosen part datasheets and tolerances.
- Only then a coordinated KiCad outline/holes/placement/routing change and DRC run.

**Status:** engineering gate, not a finished PCB revision. The KiCad PCB has not been changed in this pass.
