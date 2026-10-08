# ENKU Reader — proposed mechanical-correct placement plan R21

**No PCB coordinates changed in this document.** These are staging targets for a **coordinated KiCad reroute**, not released footprints. The only production footprint commitments remain the verified parts.

## Geometries and orientations grounded in actual PCB + manufacturer drawings

Current board x=18…77, y=20…121 mm; portrait 59×101 mm.

| Ref | Current | Candidate corrective placement | Critical implications |
|---|---|---|---|
| J2 — Hirose DM3AT | (28.9,100.7,90°) | **(26.1,100.7,270°)**, *provisional* | Original mouth local Y~+8.125 maps toward **+X** at 90°. Rotating to 270° maps opening toward **-X**; shifting the nominal origin left 2.8mm puts its nominal mouth close to x18.0 for left-edge access. **Full pad pinout rotation, CD contacts, all microSD breakout tracks, component courtyards, mounting-hole exclusion and ejection clearance must be recalculated in native KiCad/STEP.** Do not patch routes with text offsets. |
| J5 — GCT USB4105 | (47,110.325,0°) | **(47,117.325,0°)**, *provisional* | Mating/edge datum becomes y121 vs board y121. Pads, plated support tabs and 2 NPTH must be moved as one locked footprint. Reroute CC1/CC2/DP/DM/USB VBUS, GND, shield, USBLC6-2, associated traces/ESD; remove/relocate lower GND stitches (42,117.5)/(54,117.5). Check rear shell thickness, connector mechanical overhang and support. |
| SW3/SW4 left | (25,63/75) placeholder | **body inside x18, actuator projects toward -X**, candidate G-Switch C915811 with board-edge recess, exact x TBD | Select a real horizontally side-actuated switch with verified 3D envelope, operating force and travel; mirror native actuator to exterior. The x reference will vary by the selected manufacturer's land pattern. |
| SW5/SW6 right | (71.2,63/75) placeholder | **body inside x77, actuator projects toward +X**, candidate G-Switch C915811 with board-edge recess, exact x TBD | Must be mirrored/opposite actuation direction; both sides should feel identical. |
| SW1 | (30.5,29) 2-pad placeholder | exact side-slide SKU + location TBD | Selected SPDT/2/3 terminal switch must be checked for actual OFF disconnection vs PMU power architecture. |
| J1 | (66,93.5,90°) 3-pad placeholder | exact mated battery socket and cable exit TBD | Protected 1S cell and NTC connector polarity / manufacturer STEP necessary. |
| H1–H4 | (30/71,23) and (23/71,111) | chassis screw/clip axes **not in display glass/FPC envelope** | Nominal centered module 56.24×96.62 mm leaves only (101−96.62)/2 = 2.19mm board length margin each end. Current four through-board M2 holes cannot be considered clear of the module. Prefer chassis bearing load outside glass; 2 bottom M2 + 2 upper engagements or alternate fastening architecture must be rechecked. |

**Display/FPC datum is not mechanically registered** to PCB yet. All coordinate targets depend on the real GDEY0397T81P drawing and actual FPC exit geometry, not just its outline rectangle.

## Coordinated reroute order (do not release partial)

1. Load official J2, J3 and J5 STEP models and correct button/battery connector candidate footprint in KiCad + CAD.
2. Update connector positions in a single branch; regenerate affected pad coordinates, redo USB and SD differential/signal/ESD topology. Recheck USB data length matching/return continuity and channel protection placement.
3. Decide physical screw axes and revised case shell after registered screen + FPC + battery pockets.
4. Reroute all critical electrical nets in **one large scope**: VBAT/VSYS/3V3 and GND first; then lower SD/USB and EPD HV, then signals/controls. Remove conflicting old copper segments instead of piling repair stubs.
5. Native KiCad ERC+DRC+schematic parity, refill zones; reject shorts, hole clearance and track crossing. Verify 4-layer stackup and return plane integrity.
6. Run `mechanical_release_audit.py --release` (must fail until physical parts and CAD validation are complete). Fab exports blocked until it passes plus native DRC and BOM/CPL review.

## Why J2 matters

Official Hirose drawing: [DM3AT-SF-PEJM5](https://www.hirose.com/en/product/p/CL0609-0031-0-00), card enters opposite the contacts. Actual KiCad J2 footprint pads are at local Y=-7.725; card body/open mouth toward local Y=+8.125; KiCad 90° converts positive local Y into +global X. Current interior-pointing opening is not fixed by moving a casing hole.

**These are proposed coordinates, not confirmed replacement positions.** Use supplier STEP insertion/ejection stroke and verify mechanical stack before changing the approved PCB geometry.

## R22 button model correction
- Reject old C&K PTS645V (too large). Preferred shortlist is G-Switch `GT-TC035A-H0195-L3`, **LCSC C915811**, 2.8 mm side button, 1.6 N, 300k specified cycles, **recessed** PCB mount. A 0.98-mm recessed height is quoted by the manufacturer, not a ready-to-fabricate cutout depth. Full vendor land pattern, cavity and STEP still required.
- KiCad `Dwgs.User` now carries four nominal body silhouettes near both side rails, marked **STUDY ONLY**. This does **not** change SW3…SW6 pads or their routing, and does not make electrical/PCBWay release ready.
- PCBWay RFQ must carry the exact MPN and LCSC C-code, Chinese supplier preference, and explicit approval of substitutes. Do not assume they buy exclusively from LCSC.
