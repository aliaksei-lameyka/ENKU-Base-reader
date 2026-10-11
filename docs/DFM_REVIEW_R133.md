# ENKU R133 fabrication review draft — NO FAB

This is a review checklist, not a manufacturing submission. Nothing was sent to a supplier and no parts were ordered. The complete fixed-thickness enclosure and protected battery have not been accepted.

## Hole-to-copper findings requiring a process or component decision

The unchanged full-severity KiCad rule requires 0.25 mm copper-to-hole clearance. All 20 errors remain active. The source drawing dimensions, hole classifications, lands, severities and exclusions are unchanged.

| Part | Native findings | Physical interfaces | Nominal recommended geometry | Decision required |
|---|---:|---:|---|---|
| SW3–SW6, E-Switch TL3340AF160QG | 16 | 16 | Two 0.90 mm NPTH locator holes per switch; 0.075 mm signal-land gap and 0.150 mm bracket-land gap | Verify actual locator/land tolerances, NPTH drilling order and registration. Accept an explicitly documented part-specific process, or choose a different switch and revalidate actuator geometry. |
| J5, GCT USB4105-GF-A-120 | 4 | 2 | Two 0.65 mm NPTH locator holes; 0.1944 mm with actual rounded lands, 0.1751 mm for the drawing's rectangular envelope | Confirm the exact 1.20 mm stake option on the 1.60 mm PCB, locator fit, soldering and guaranteed copper-to-NPTH registration. Coincident ground pad numbers do not make four physical holes. |

References: E-Switch P021301 revision B, supplied controlled drawing; GCT USB4105 B4 dated 2023-12-18, supplied controlled drawing. General dimension tolerances on those drawings do not guarantee the PCB factory's drilling/etch registration. Do not reduce holes, omit locating features, clip lands or disable DRC to obtain a clean report.

## New U3 thermal construction

U3 is BQ24072TRGTR, TI RGT0016C. The unchanged copper/mask EP is 1.68 mm square and the unchanged single paste aperture is 1.55 mm square with 0.05 mm rounded corners. The stencil example is for 0.125 mm thickness.

R133 requests **five resin-filled, copper-capped through vias** under the paste: 0.30 mm drill, 0.50 mm land, center at X48.50/Y91.00 mm and four positions at ±0.58 mm from that center in both axes. TI's specific land example shows these positions with a 0.20 mm via. The project's 0.30 mm drill preserves the existing board constraint and follows the general SLUA271C starting point; it is a process adaptation, not factory approval.

The native PCB explicitly requests fill and cap, top exposed metal and bottom mask coverage. The fabrication review must confirm which output conveys these individual requests, fill material, cap thickness, flatness, finish, allowed voiding and the assembly inspection method. Ordinary solder-mask tenting is not accepted as proof of a flat sealed via beneath paste. Ask for the cost of the required process before authorizing prototypes.

A new solid-connect B.Cu GND zone spreads heat locally. Its actual filled area and continuous region touching U3 are measured by `audit_U3_thermal_R133.py`; fragmented inner areas are separately reported. The 50 mm² continuous-region objective remains a design goal if the reported boolean is false. Neither total copper area nor five vias proves a junction temperature or a full charge cycle inside the case.

Sources: [TI BQ24072T](https://www.ti.com/lit/ds/symlink/bq24072t.pdf), pages 33–34 and RGT drawings; [SLUA271C](https://www.ti.com/lit/an/slua271c/slua271c.pdf), section 3.4.1.

## USB and assembly

The original differential pair and reference-plane requirements remain guarded. The new B.Cu ground is kept at least 1 mm from the preserved B-side USB copper. A controlled 90-ohm differential stackup, impedance calculation, actual fabrication tolerance and USB current/inrush/suspend behavior still need acceptance.

EN1 is tied to VBUS, EN2 to GND and CE is statically low. **The current hardware cannot select USB100 or USB suspend through firmware.** Resolving host-port power policy requires a hardware control decision as well as firmware and bench tests; changing a status-pin interpretation cannot change the input-current mode.

The fitted BOM/CPL has no component substitutions in R133. Preserve the 102 fitted positions, 19 bare PCB items and R67 DNP. Approve the exact panel/FPC, effective C7/C8 capacitance, U1 and U3 stencil/process details, and final manufacturing outputs before any release.
