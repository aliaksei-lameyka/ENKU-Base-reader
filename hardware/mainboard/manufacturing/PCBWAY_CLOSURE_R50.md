# R50 — PCBWay closure (single active engineering lane)

**Active branch:** `engineering/r50-pcbway-closure`, based directly on `engineering/r49-gooddisplay-mechanical-gate`. The DIANWEI connector evaluation is explicitly paused; **retain Hirose J3 and existing footprint**. No connector-related changes are allowed during R0.1 first-spin closure.

## Source-of-truth, verified 2026-10-09
- KiCad PCB: `hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb`; 168678 UTF-8 characters, SHA git blob `864387d7531dd20c0369ed42bf9970d1eb093294`, 515 segment records before the next route pass.
- R48 Native KiCad: ERC 0; schematic parity 0; priority DRC 0; 139 unrouted and 168 additional DRC (130 footprint/library, 38 silkscreen). These figures are **baseline**, not new R50 results.
- Manufacturer electrical/mechanical hold: Base panel pin 5 `VDHR` vs `VSH2`; `GDEM` vs `GDEY` model mismatch; FPC radius/contact-side and J3 mating need proof. Never waive them to rush production.
- Weighted readiness: **44/100**, production **NO-GO** until measured clearance.

## Sequential execution — avoid side projects
1. **Routing closure**: preserve all known R49 placements, keep Hirose J3, finish electrically open power/control/SD/EPD-low-voltage nets where manufacturer's unresolved pin5 is not affected. Audit copper shorts, component-body and routing keepouts after each *large* group. Use net connectivity reports instead of claiming progress by trace counts.
2. **USB-C / MSC**: complete GPIO19/20 D-/D+ via the ESD interface, with 90-ohm differential geometry calculated from confirmed PCBWay 4-layer stackup. Verify CC1/CC2, VBUS-valid monitoring, unpowered backfeed and exclusive microSD ownership in firmware.
3. **Native electrical/fab cleanup**: repair all footprint/library mismatch and silk-vs-mask violations, rerun full ERC + DRC + board/schematic parity; explicitly require **0 unconnected and 0 production DRC** with justifiable exceptions separately reviewed.
4. **Manufacturer signoffs**: close pin5, actual GDEY flex geometry, J3 mating, and HV boost BOM ratings; execute Fusion clearance review (bend loop, enclosure and component access), confirm sample purchasing.
5. **PCBWay export gate**: generate and inspect Gerber, NC drill, assembly drawings, positioned BOM with manufacturer IDs and CPL orientation, stackup/impedance order notes; verify generated files match exact approved KiCad commit. Final check must not be inferred from ERC0 alone.

## Why no copper change in this commit
The current tool session can read/write GitHub KiCad text but does not have KiCad CLI or a checked supplier stackup to validate the result. A manually inserted trace with unknown clearance would jeopardize PCBWay readiness. This is a manufacturing-critical prerequisite, not permission to mark any route complete. Do not report 139/168 as reduced without a newer measured Native run.

## Immediate next engineering action
Run actual KiCad on R50 source (local KiCad or Work cloud computer) and resolve copper groups; commit the PCB and full diagnostic artifacts to **this same branch**, not new parallel branches. Re-run CI only after grouped changes to control GitHub Actions budget.
