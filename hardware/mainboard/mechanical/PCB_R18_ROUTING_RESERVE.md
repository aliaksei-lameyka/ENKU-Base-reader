# R18 — activate the 7 mm lower routing reserve

**Engineering trial; not a PCBWay manufacturing release.** Oct 8, 2026.

## What changed
- 59 × 101 mm board unchanged; **new 7 mm lower band now has F.Cu and B.Cu GND copper pours** through y=120.5 (0.5 mm from the board edge).
- Added two 0.80-mm GND stitch vias (0.40-mm drill) at **(42.0,117.5)** and **(54.0,117.5)** to tie the front/back pours in the new band. Coordinates are deliberately away from provisional lower M2 holes at (23,111) and (71,111); mechanical clearance is **not** certified.
- Before R18, **zero routed track segments** extended past y=114 despite the extended board outline. This is why increasing Edge.Cuts alone did not relieve the dense upper routing.
- The new y=114…120.5 band is now available as a **routing and ground-return reserve**, not automatically populated with signal copper; preserve appropriate signal-to-ground/via and case clearances.
- Added a diagnostic *DRC hotspot report* to the existing native KiCad workflow so large re-routing passes can target real copper collisions rather than count only ratsnest endpoints.

## Routing priorities
1. **Power and SD/USB lower quadrant:** remove VSYS ↔ VBAT shorts on In1.Cu and VSYS ↔ SD_CS_CARD crossing, then place deliberate wide, short return-safe power paths. Use bottom corridor **only where overall length and current return are defensible**.
2. **MCU signals:** replan In1/In2 crossings for ESP_EN, SPI and EPD: stop routing unrelated nets across the same layer without proper lanes and vias.
3. **R2/R5/R6 MUX straps:** physically re-place clustered resistors and redo their vias. Current 0.16-mm GND escape is a temporary diagnostic.
4. **Mechanical freeze only afterward:** validate actual buttons at x18/77 side edges, EPD FPC insertion, battery pocket and four through-hole axes against display projection.

## Existing DRC baseline before R18
| Metric | Native KiCad R17 |
|---|---:|
| Total DRC violations | 659 |
| Net-to-net shorts | 39 |
| Tracks crossing | 57 |
| Trace clearance | 124 |
| Hole clearance | 69 |
| Real unconnected after ignoring KiCad duplicate-zone self-report | 0 |

Do not interpret two GND stitches or structural PASS as a finished routing pass. CI must classify any new problems caused by the copper enlargement. The unaltered validated board remains in prior commits.

## R19 connector-edge audit (2026-10-08)
- Actual J5 footprint: `USB4105-xx-A_16P_TopMnt_Horizontal`, origin **(47.0,110.325)** at 0°.
- J5 footprint's own `Dwgs.User` reference marks a nominal `PCB Edge` at local Y **+3.675 mm**. This yields a nominal port datum at **y=114.000 mm**.
- R16/R18 board bottom Edge.Cuts is **y=121.000 mm**: USB-C nominal edge is now **7.000 mm recessed** relative to the board contour. This is **not** a viable straight bottom-edge connector alignment without cutout and proper mechanical access.
- Decision gate before any production files: **either move J5 downward 7 mm and reroute all USB/shield/CC/DP/DM/VBUS/GND connections**, or engineer an open-bottom PCB notch to the existing port face, with edge clearances, shielding and housing verified in CAD.
- Connector movement interacts with both trial GND stitching vias at (42.0,117.5)/(54.0,117.5): these remain provisional and MUST be moved/deleted as needed. MicroSD side entry and side switches require separate actuation access verification.
- The placement checker prints this as **MANUFACTURING BLOCKER** without changing the currently informative structural check status to red. Do not equate structural PASS to connector fit.
