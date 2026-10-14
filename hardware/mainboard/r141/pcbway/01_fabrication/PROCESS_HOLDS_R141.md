# ENKU Base Reader R141 - PCBWay preliminary engineering review

**NO FAB / NO ASSEMBLY RELEASE.** This packet is prepared for a later preliminary PCBWay review. Manufacturing, purchasing and factory upload have not been released. No firmware/FCT binary is supplied.

## Identity and file selection

Working PCB: R141. Exact PCB SHA256: `b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe`. KiCad 10.0.7. The legacy `r0.1` filename is retained to preserve sheet/library references. R138 is the historical comparison source and is not a factory input for this packet. R139 qualification documents are retained test requirements, not R139 copper.

| Purpose | Directory / file |
| --- | --- |
| Bare board review | `01_fabrication/Gerber_Drill_R141_NO_FAB.zip` |
| Assembly sourcing | `02_assembly/BOM_PCBWay_R141.csv` or workbook `BOM` sheet |
| Placement review | `02_assembly/CPL_PCBWay_R141.csv` or workbook `CPL` sheet |
| Authoritative original tables | `BOM_fitted_review.csv`, `BOM_all_classified.csv`, `CPL_native_mm.csv` |
| Polarity and all native pads | `Reference_first_pad_index_R141.csv`, `Complete_pad_map_R141.csv` |
| Via-in-pad process request | `U3_via_process_requests.csv`, `R28_via_process_request.csv` |
| Report, layer/assembly drawings, five schematic sheets | `03_drawings/` |
| Editable current board and project-local libraries | `04_editable_kicad/` |
| Native and independent evidence | `05_verification/` |
| Planned physical and factory tests | `06_qualification/` |

## Coordinates and assembly

11 Gerbers contain four copper, both masks/paste/silkscreens and Edge.Cuts. Separate PTH/NPTH Excellon files, SVG drill maps, drill report and IPC-D-356 are included. Empty back paste is intentional. Manufacturing coordinates in mm are X=KiCad board X, Y=-KiCad board Y. Envelope: X18..77, Y-121..-20. Origin 0,0 is shared by Gerber/drill/IPC/native CPL and PCBWay column aliases. No origin shift or rotation normalization has been applied. The reference/pad index explicitly labels positive-down KiCad board coordinates and provides conversion where applicable.

All 107 fitted components are top/front, in 58 BOM groups. Mapped BOM/CPL preserve all source references, values, MPNs, quantities, positions and angles. Distributor fields are deliberately blank because no approved purchasing list exists. Mounting types reflect component solder leads: U1 is Surface mount, with intrinsic PCB thermal holes handled separately. J5 is Hybrid because it has plated mechanical stakes and SMD signal lands. CPL includes fitted SMT/hybrid placements; connector insertion/stake soldering needs separate process confirmation. KiCad native rotation is not an approved machine/library zero-angle convention. Confirm package zero-angle, pin 1, polarities and plated-stake process before programming assembly. Do not infer orientation from a hidden reference label. The complete pad map is authoritative for pad identity; the first-pad index is a lookup aid.

R67 is DNP and has no paste apertures. 19 BARE_PCB references are service/test/NTC pads or mechanical features, excluded from placement. J7 is bare ENKU-specific UART/BOOT/EN fixture contact geometry, not a fitted connector. J8 is bare hand-solder pads for separate cell NTC, not an SMD connector. Battery/display/FPC/case/NTC harness are off-board items and are not included in the 107 fitted units.

## Written process responses required

1. Stack: F.Cu / In1.Cu / In2.Cu / B.Cu, 59 x 101 x nominal1.6mm. Outline includes the exact side cutout. Submit actual material, dielectric thicknesses, finished copper, finish and tolerances. Board contains no qualified supplier stack. Review B-side USB geometry against In2 return reference and actual 90-ohm differential stack before any geometry change.
2. Routed vias: 346 total, land/bore counts 82 x 0.50/0.20 mm; 181 x 0.60/0.30 mm; 83 x 0.70/0.30 mm. Nominal annular ring >=0.15mm. Ordinary via-to-SMD-land gap >=0.10mm. Nominal0.20mm bores at1.6mm give aspect8; confirm actual finished bore, board tolerance, drill compensation, registration, barrel copper and inspection. Published capability is not job approval.
3. Six explicit fill/cap requests: five U3 exposed-pad vias and one R28 pin-1 supply via. Exact UUIDs/coordinates are in process CSVs. Require resin fill, copper cap, front untented and back tented. Excellon does not encode these process instructions. Approve planarity/finish/mask/stencil compatibility. Ordinary tenting is not a substitute.
4. U1: preserve 9-land/9-window exposed-pad grid and12 intrinsic0.30mm EP plated holes, with both-face tenting request. These are separate from routed-via totals. Agree stencil, wicking, reflow and appropriate joint/X-ray inspection criteria.
5. USB J5: exact GCT USB4215-03-A, four plated slots0.6x1.4/1.8mm,0.8mm stakes on1.6mm PCB. Confirm hybrid solder process and mechanical joint adequacy. No USB4105 substitute or locating-peg holes.
6. Review stencil thickness/reductions for U1, U3, TPS63802, USB and microSD. Preserve native mask/paste and R67 DNP. Confirm component polarity/orientation, solder joint acceptance, bare-board net test, AOI and joint inspection. No MPN alternatives without approval.

## Product release holds

BQ24072T charger,445mA nominal, modeled maximum492.42mA, BAT maximum4.24V. Real-pack startup/current/CC-CV/timers, NTC open/short/retention, load/thermal/EPD/SD/USB-MSC/PSRAM/firmware/FCT and consumer tests are NOT RUN. Direct PH-2 battery J1 pin1=VBAT, pin2=GND must match the qualified harness. A two-wire LiPo alone does not provide a cell NTC. Current case CAD and exact panel/FPC fit, thin interchangeable protected2000-2500mAh CN/PL packs and NTC retention remain unqualified. Case thickness must not increase.

Native DRC0/ERC0/opens0/parity0 and independent export checks are software evidence only. The preferred ground plane has short common MOSI0.741064mm/SCLK1.057355mm centreline gaps near MCU, with far-inner ground present. These results are not impedance, timing, EMI or physical qualification. Remaining SI/PI/FMEA/mechanical/process checks are listed in the included R141 pre-review plan.

Official PCBWay file requirements consulted14October2026: https://www.pcbway.com/assembly-file-requirements.html . BOM CSV/Excel, fabrication layers and X/Y/rotation/side data are included together with assembly drawings. Supplier-specific import conventions remain to be confirmed.

## Hidden-layer audit

No unnamed layers or unassigned routed copper found. Disabled User.Drawings retains45 historical objects with obsolete charger/placement notes, excluded from fabrication.79 references and120 values are hidden; supplied reference/pad maps preserve every item. Detailed inventory is in05_verification/. Clean historical notes during the next engineering pass before supplier submission. PCB and export hashes remain unchanged.
