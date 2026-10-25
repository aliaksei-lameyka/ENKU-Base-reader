# ENKU Reader — R149-P0 M03 integration / 2026-10-25
**State: MECHANICAL PLACEMENT REVIEW ONLY — HOLD / NO FAB.**

## Provenance
- Electrical base: R148 KiCad (source PCB SHA256 `bb0aa41324b73ec13c087ab1c669c57c6bc6fd449621bf3aa34a53d3901b9476`).
- Physical M03 mockup created 2026-10-17. On 2026-10-25 user physically printed it and confirmed panel position and flex reach to J3. This DOES NOT qualify populated PCB, final case assembly, contact orientation, electrical routing or production.
- M03 STEP assembly is **MECHANICAL ONLY**. Never fabricate from M03 STEP or from R148 Gerbers for the M03 case.

## Agreed footprint position transformations (KiCad coordinates, mm)
| Ref | R148 X/Y | R149-P0 X/Y | Rotation |
|---|---|---|---|
| J3 (FH34SRJ 24-pin FPC) | 69.27, 34.00 | **69.46, 94.22** | 0° |
| J5 (USB-C) | 47.00, 117.325 | **65.00, 117.325** | 0° |
| SW3 (left upper) | 21.55, 73.00 | **21.55, 68.00** | -90° |
| SW4 (left lower) | 21.55, 85.00 | **21.55, 80.00** | -90° |
| SW5 (right upper) | 73.45, 73.00 | **73.45, 68.00** | 90° |
| SW6 (right lower) | 73.45, 85.00 | **73.45, 80.00** | 90° |

J3 coordinate inferred from the preserved M03 STEP body location and R148 OEM Hirose model comparison; confirmed mechanically via the user's printed mockup. PCB outline remains 59 x 101 x 1.6 mm. STEP datum: X=KiCad X-18, Y=20-KiCad Y.

## R149 mechanical obstruction audit against ALL R148 footprints
Native KiCad F.CrtYd rectangles or pad bounding boxes, transformed using each footprint rotation. This is a **custom 2D proximity screen, NOT a native KiCad DRC**:
- J3 at its M03 position directly overlaps **J1 battery wire pads courtyard (14.000 mm²)**, **C12 (3.985 mm²)**, **J8 NTC pads (0.105 mm²)** and **L1 (0.101 mm²)**; adjacent **R97 clearance 0.17 mm**, **C11 clearance 0.61 mm**.
- J5 USB-C relocated +18 mm: no direct footprint overlap, **0.83 mm courtyard/pad gap to H4 mounting-hole perimeter**; screw head/standoff still need a stackup sweep and actual Fastener trial.
- SW3-6 raised 5 mm: no direct courtyard overlaps in the screen.
- No rerouting has been conducted. R148 had 2,963 segments, 389 vias and eight zones, which must NOT be passed off as valid routing at the shifted footprints. Schematics, BOM and original manufacturing exports are not a released R149 candidate.

## NEXT (R149-P1 onward)
1. Resolve all J3 overlaps without moving the physically fit-approved M03 J3, subject to pad1/latch/FPC constraints. Move J1 battery solder lands and the NTC J8 away from J3 and retain a guarded wire-clamp region; re-home C12 and L1 while respecting high-current regulator return geometry.
2. Confirm USB-C +18 mm placement versus H4 screw-head clearance and four-layer USB DP/DM, CC/VBUS/ESD path; if unacceptable, adjust hole/mechanics with explicit approval.
3. Place/reroute each relocated switch and all J3 24-pin nets from updated footprints; remove stale tracks/vias, flood zones, and verify signal returns, EPD HV and power/NTC.
4. Run native KiCad ERC/DRC, independent connectivity/copper/gerber comparison and manufacturing/BOM/CPL audits; **none have passed on the moved PCB**.
5. Validate real FPC contact1 and actuator, protected battery/NTC, enclosure crush/strain and board sample tests before PCBWay release.

**Invariant:** Preserve R148 as an immutable qualified routing reference; treat R149-P0 as a mechanical integration hold until the whole placement and copper closure.
