# ENKU BASE — PCBWay readiness dashboard

**Status as of 2026-10-08: ≈30% PCBWay Ready (engineering estimate).** NOT fabrication-ready; NOT equivalent to “30% of DRC tests passed”. This estimate is explicitly **milestone-weighted** and updated only after independently validated work.

Product: Base-only (no Hall, Qi or frontlight), GDEY0397T81P 3.97in, dedicated PCB. Working branch `engineering/r29-base-mechanical-closure`. No Pro board fabrication to be inferred from these results.

## Scoring model

| Stage | Full weight | Currently earned | Evidence and qualification blockers |
|---|---:|---:|---|
| Dedicated Base requirements and architecture | 10 | **9** | Two separate Base/Pro PCBs agreed, Hall removed from Base schematic and PCB |
| Electrical schematic, pinout and Native ERC | 20 | **11** | ERC diagnostic 0 and schematic PCB parity 0 in KiCad 8; EPD pin5 VDHR/VSH2 and charger/logic supply qualification still open |
| 3D/mechanical envelope, FPC, battery and fasteners | 20 | **5** | 59×101 PCB, four real M2 NPTH, original stepped FPC projection, STEP J2/J3; no verified folded flex or rear-screw load path |
| Manufacturer-qualified footprint and sourced assembly BOM | 15 | **3** | User supplied actual Hirose J2/J3 STEP/2D; **119 library mismatches**, J1 + side buttons and power control not vendor-locked, PCBWay parts sourcing absent |
| Real PCB placement, full copper layout and critical DRC | 25 | **2** | 120 footprints, 2D courtyard clean, J2 copper edge fixed, 252 connections UNROUTED, no filled pours |
| Manufacturing package, full release DRC, PCBWay DFM and build | 10 | **0** | No Gerbers, Excellon verification, full fab notes, pick-place, approved BOM or prototype bring-up |
| **TOTAL** | **100** | **30** | **PCBWay Ready is only reached at 100/100 and no release blockers** |

Rules:
1. Never compute readiness from DRC raw count or GitHub workflow status alone.
2. Only award stage points after evidence: exact parts and CAD, data sheet pin tables, real routing, KiCad native DRC with all tracks and schematic parity, manufacturer quote, enclosure glass-safe load path.
3. Percentage is a coarse engineering planning estimate, **not a certification**. Score may **decrease** when a new validation reveals faults or a redesign changes the chosen screen.
4. Update the figure at each substantive engineering report and provide both **total %** and objective observations (critical DRC classes, unconnected nets, manufacturer sourcing blockers).
5. Physical score accounts for PCB, enclosure and bill-of-material components; a bare clean PCB with wrong flex is still NOT ready.

## Last verified Native KiCad snapshot

Branch R29, full KiCad 8 on actively selected Base PCB, after the J2 movement +0.9mm:

| Measurement | Before J2 fix | After J2 fix |
|---|---:|---:|
| PCB components | 120 | 120 |
| DRC violations, excluding unrouted group | 291 | **240** (after silkscreen cleanup) |
| Copper-to-board edge clearance faults | 2 | **0** |
| Schematic parity violations | 0 | **0** |
| Unconnected_items | 252 | **252** |
| Library footprint mismatches | 119 | **119** |
| Library footprint unavailable | 1 | **1** |
| Silk over copper | 80 | **68** |
| Silk overlaps | 68 | **36** |
| Silk board edge | 1 | **0** |
| Silkscreen text height | 20 | **16** |

Two native KiCad GND shell pads of J2 were previously too close to the left board edge. J2 was moved from (26.1,100.7,270deg) to **(27.0,100.7,270deg)**, and R19-21 each moved +1mm X. Actual manufacturer pad dimensions were *not* altered. Source: Native KiCad GitHub Actions run [37783778795](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37783778795), structural gate run [37783829165](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37783829165).

Global KiCad 8 footprint library table was provisioned in a later native run; the **119 mismatches persist**, therefore they are **not** simply an absent global library table. Each production footprint requires reconciliation with the exact original manufacturer land pattern; do not automatically suppress the errors. One `Connector_Generic` library ID for the J1 battery placeholder is not installed and **J1 footprint is not accepted**.

## Explicit nonnegotiable blockers before PCBWay order

- Real GDEY0397T81P FPC-7750 **3D folded** shape including stiffener, pin1 orientation, latch and cable stress; exact display contacts verified against J3.
- Manufacturer-exact side keys SW3–SW6 plus case-milled recess, physical hard power switch SW1 and battery connector J1, with orderable supplier SKUs.
- H1–H4 screw attachment and display-glass clearance, LiPo mechanical cavity, ESP32 RF antenna clearance, dock access, microSD insertion/ejection travel and USB-C plug clearance.
- Validated EPD high voltage topology and pin5 VDHR/VSH2 discrepancy, compare controller SSD1677/reference circuit, verify PCB VDDIO–VCI populated bridge and power sequencing.
- Native KiCad ERC and DRC for final fabrication with **0 relevant violations and 0 unrouted signals**, complete all copper planes, fabrication drill NPTH/PTH, silkscreen readable, 3D interference validated.
- Real LCSC/PCBWay procurement BOM, PnP, polarity/pad 1/rotations, Gerbers/Excellon, source KiCad, electrical bring-up test.

**DO NOT PLACE MANUFACTURING ORDER** based only on these structural and Native KiCad diagnostics.

## New 2026-10-08 footprint pad geometry assessment

Native KiCad 8 `pcbnew.FootprintLoad()` compared the **physical local pad numbers, positions, dimensions, plated drill, copper shape and pad attributes** of every instantiated board footprint to its project-local or standard-library copy. From run [37784904764](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37784904764):

- **64 of 120** footprints have matching physical pad descriptors.
- **55** have materially different pad descriptors vs the cited library (including stock passives, ESP32 module U1 and USB-C J5). These are **not cleared** until exact manufacturer land-pattern and pin-numbering verification. Some may be legitimate custom geometry; never auto-replace them.
- **1** (J1 `Connector_Generic:JST_PH_3_PLACEMENT`) has no matching library and is a supplier footprint placeholder. Replace only after selected exact orderable JST+matching cable/NTC.
- **ESP32 U1** current board contains **53 pads**, while stock `RF_Module:ESP32-S3-WROOM-1` offers **62**. The missing 9 stock pads require explicit antenna/ground/exposed-pad electrical/mechanical analysis before PCB copper is routed. This count mismatch alone does not tell whether the current 53-pad part is invalid.
- **J7** current board Tag-Connect has **6 pads** vs **9** in installed stock footprint; compare pinouts, three guide holes/no-pads and exact programming jig registration rather than assuming change in electrical pin count.
- **J5** current USB-C GCT body has **22 pads**, matching count of library counterpart but differing in physical pad descriptors. Manufacturer drawing and correct mounting slots must determine acceptance.

Raw pad audit JSON is attached to Native KiCad workflow artifacts. No BOM, no Gerbers, no approval from this diagnostic.

## R29 silkscreen hygiene

17 non-manufacturing canvas legends/boxes were transferred from `F.SilkS` to `Dwgs.User`; two obsolete frontlight overlays removed (Base does not contain frontlight). Actual footprint reference/repair text remains on silkscreen for later relocation and verification. Native DRC dropped from 288 to 240 (no copper faults, schematic parity still 0). 120 remaining silkscreen issues and 120 library issues are actionable, not waived.
