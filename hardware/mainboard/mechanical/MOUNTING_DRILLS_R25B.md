# R25B — drill, mounting and access-hole register

**Engineering layout only; not a PCBWay fabrication approval.** Checked against Good Display GDEY0397T81P nominal **56.24 × 96.62 × 0.92 mm** module size ([Good Display](https://www.good-display.com/product/613.html)). The drawing on `Dwgs.User` centers the display nominally on the 59 × 101 mm PCB; the real FPC origin, module adhesive zones, hard shell and mounting interface are **not yet registered**.

## Real PCB M2 mounting holes in `enku-mainboard-r0.2-placement.kicad_pcb`

| Reference | Center in PCB CAD (mm) | Drill | PCB edge minimum axis distance | Proposed use |
|---|---|---|---|---|
| H1 | (23, 25) | **2.2 mm NPTH** | **5 mm** | rear access, top left |
| H2 | (72, 25) | **2.2 mm NPTH** | **5 mm** | rear access, top right |
| H3 | (23, 116.5) | **2.2 mm NPTH** | **4.5 mm** | rear access, bottom left, moved below microSD |
| H4 | (72, 116.5) | **2.2 mm NPTH** | **4.5 mm** | rear access, bottom right, outside USB-C |

All four have marked **5.5mm nominal diameter** study envelope on **`Dwgs.User`**, representing 2.75mm radius for rear-facing screw head / structural bearing land. This value is a *design allowance*, not selected screw-head dimensions, enclosure boss geometry or vendor-certified keepout.

**Critical:** the entire four-hole set sits **within** the *nominal centered display-module rectangle* x19.38…75.62 y22.19…118.81. This is NOT an error concealed by moving holes: the panel almost fills the PCB. The only plausible use is a **rear-loaded attachment** with its load taken by the plastic chassis/PCB and a non-contact gap or independent saddle under the screen. The screws may never bear on, lift, touch or bend the glass/laminate; the FPC and battery pouch also must not contact heads. If this cannot be demonstrated in CAD, use a different fastening scheme instead of moving screw holes 1mm at a time. A rear snap/rail and two bottom fasteners is a fallback.

## Other real holes provided by component footprints

**J5 GCT USB4105** is now at (47,117.325), 0°, with nominal port board-edge datum y=121.

| Physical feature | Global origin in R25 (mm) | Physical aperture | Notes |
|---|---|---|---|
| J5 NPTH locating left | (44.11,114.720) | 0.65 mm round NPTH | *part of J5 footprint*, never manually place separately |
| J5 NPTH locating right | (49.89,114.720) | 0.65 mm round NPTH | same |
| J5 shield anchor left/upper | (42.68,114.220) | 0.6 × 1.7 mm plated oval | ground/shield per schematic |
| J5 shield anchor left/lower | (42.68,118.400) | 0.6 × 1.4 mm plated oval | verify board-edge tolerance |
| J5 shield anchor right/upper | (51.32,114.220) | 0.6 × 1.7 mm plated oval | same |
| J5 shield anchor right/lower | (51.32,118.400) | 0.6 × 1.4 mm plated oval | same |

The **two NPTH plus four PTH slots remain in the exact J5 manufacturer footprint** and were preserved when shifting J5. This is why mount holes cannot be allowed to overlap USB-C.

## Connector and control access openings — housing vs PCB

- **microSD J2** at (26.1,100.7), 270°, card-mouth nominal left-facing, requires a **left wall case opening** and insertion/push-push ejection clearance. Body/courtyard projects ~0.8mm outside x18 board edge; confirm actual Hirose STEP and case wall before acceptance. No new PCB drill for card insertion.
- **USB-C J5** at bottom, nominal y121 edge: requires a **case bottom opening** for full plug boot clearance, not a random circular PCB hole. Its existing SMT/NPTH/PTH features already form the mounting pattern.
- **SW1 hard power** on upper/left case: actual slide actuator + 3D travel and required case slit must be designed once an orderable part is selected; no fictional PCB hole for a two-pad placeholder.
- **SW3–SW6 navigation**: two per side, selected miniature recessed-switch candidate requires manufacturer-exact **open-sided PCB edge milling and case push-key travel**. No PCB Edge.Cuts slots created until PCBWay confirms machining. Never use the old 3.8mm 2-pad rectangles as true production switches.
- **J3 FPC**: panel FPC insertion direction and routing gap require a cable corridor, NOT a drilled hole through glass or a change to existing FPC pads.
- **Dock J6 / Tag-Connect J7**: rear copper pads must be reachable through controlled case features, but this does not imply PCB drilling. Ensure service access, magnetic keeper, keyed orientation and safe power polarity.
- **TP1…TP14**: test points, not holes; preserve accessible probing clearance on the rear.

## Manufacturing review
- Screw specification: actual M2 thread length, head diameter, stack, nut/insert/pilot diameter and preload; PCB NPTH tolerance and head electrical insulation. PCBWay notes holes require clearance for drill + laminate registration, not just bare 2.2mm drill width ([PCBWay fabrication guidance](https://www.pcbway.com/project/question/How_to_Design_the_PCB_Board.html)).
- Structural check `check_r25_mounting_drills.py` checks edge, mounting footprint, connector PTH/NPTH existence and 2D keepout distances. It intentionally does **not** certify screw/display/battery 3D clearance.
- **No Gerbers until** screen/FPC and battery mounting datum is locked, independent screw load path proven, supplier connector 3D imported, side keys final, full native ERC+DRC green, PCBWay DFM reviewed.
