# ENKU Base Reader — Work handoff R41, 2026-10-08

Read this whole document and the actual sources/checks before continuing. This is an engineering checkpoint, **not production approval**. Continue substantial autonomous batches starting at R42; do not stop after each small operation or ask the owner to type “continue”.

## Exact current state

- Repository: https://github.com/aliaksei-lameyka/ENKU-Base-reader
- Active branch: **engineering/r41-sd-card-completion**, derived from `engineering/r40-sd-spi-fanout` tip `518343ce5365afe407434f52f3faf52757b787db` (adds the R40 handoff after verified routing commit `5780100cb181fd5111471152adcf042e201232fc`). R40 is retained as rollback.
- Active four-layer PCB: `hardware/mainboard/kicad/enku-mainboard-r1.8-base-sd-card-completion.kicad_pcb`.
- Root schematic: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_sch`; children `power.kicad_sch`, `mcu_io.kicad_sch`, `connectors.kicad_sch`, `epd_hv.kicad_sch`; local `ENKU.kicad_sym` and `ENKU.pretty`.
- **Last Native-verified source commit: cf04f72110456540a6bb1c9ef0a49f7621f87319.** Later report/document/register-check commits may advance the branch; do not confuse the later tip with the tested source hash. Read Git history/current Actions before changing source.
- Native KiCad **8.0.9** [run 37815837327](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37815837327): **SUCCESS**, ERC **0 errors / 0 warnings**, schematic parity **0**, priority DRC **0**, footprint_errors 0. **Full DRC NOT clean:** 241 violations (130 library footprint mismatch, 68 silk over copper, 27 silk overlap, 16 text height), **210 unconnected items**.
- [Active Base hardware checks 37816685057](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37816685057): **SUCCESS**, commit `621e9df64eae1afd63eae35c61bdd8bdacd9aea6`, including current 132-entry supplier register and active mechanical/source audits. Final documentation-only commits do not change the Native-tested copper.
- Native card gate: **0 unconnected items involving J2** (includes all GND/shell contacts). VBUS monitor gate: **0 USB_VBUS_* unconnected items**. Source graph also verifies each MCU ↔ series resistor ↔ card signal.
- Actual editable PCB: **132 footprints, 270 segments, 66 plated vias, 2 inner GND zones**. Both In1.Cu and In2.Cu were filled, saved/reopened and checked as one nonempty polygon each. The lower plane outline widens only below y=80; module antenna keepout remains intact.
- **PCBWay Ready 30/100, unchanged.** Do not infer a readiness gain from number of tracks or green priority CI.
- Full exact ERC/DRC/pad-audit/fill reports and SHA-256 manifest: `hardware/mainboard/manufacturing/r41-native/`. Original `r29-*` report filenames are legacy workflow names; contents are R41. Filled diagnostic board is [artifact 11566888024](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37815837327/artifacts/11566888024), expiry 2027-01-06. Preserve committed reports and source; never replace real diagnostic debt with a fabricated clean report.

## Product and electrical constraints

**Base and Pro have different boards. Base has NO Hall, Qi or frontlight.** Keep 59x101mm portrait 3.97-inch e-paper, ESP32-S3-WROOM-1-N16R8, removable microSD, repairable 1S LiPo+NTC, charging, BMI270, USB-C, four side buttons and dock scope. No mandatory cloud/account/subscription, no Wi-Fi requirement for USB file transfer.

- Q2 AO3401A switches local VSYS → SYS_EN. SW1 drives PMOS gate only; R40 100k pulls gate up. Charging/battery circuit remains alive in OFF; not galvanic pack isolation. SW1 remains provisional, exact mechanical MPN unqualified.
- U9 TMUX1101 remains the switched battery-ADC isolation stage; OFF leakage/injection is unmeasured.
- **Same microSD via USB-C is mandatory:** native ESP32-S3 OTG GPIO19/U1pad13 D−, GPIO20/U1pad14 D+, TinyUSB MSC with a **SPI** sector backend. No extra USB card bridge/hub. Firmware not implemented or host-tested.
- Storage must have one filesystem owner: close/flush/unmount local FatFS before host export; block reader/indexer/optional Wi-Fi storage access while host owns sectors; reclaim safely on eject/disconnect. Handle missing/hot-removed/corrupt cards without auto-format or destructive repair.
- USB MSC only with physical switch ON. USB-when-OFF/auto-wake is a separate power architecture decision; do not silently change it.
- **Good Display pin5 remains unresolved:** GDEY0397T81P table says VDHR while typical application indicates VSH2. Available project evidence has no supplier resolution. **J3 current candidate EPD_VSH2 and disputed EPD copper unchanged.** Await written pinout/flex/mating confirmation before changing it.

## R41 engineering delivered

- Completed SD_CS_CARD and SD_MISO_CARD escapes, all four MCU-side SPI routes through R19–R22, R23 CS pull-up, C17 bypass branch and all J2 GND/contact/shell returns. Shared SPI display branches R33/R34 still lack routing; they are reported, not hidden.
- Routed USB CC1/CC2 Rd, both VBUS contact pairs, raw C2, U2 TPS2121 USB input and ESD U8 VBUS. Added GND stitches and dual expanded inner references. These planes include trace clearances and are **not a final uninterrupted USB reference stackup**.
- **VBUS monitor implemented:** U10 **TLV3012BIDBVR** on switched 3V3_SYS, output USB_VBUS_VALID → GPIO17/U1pad10. Exact B suffix is required for fail-safe input when MCU rail is OFF. R70 26.7k + R71 10k (0.1%,25ppm/K), R72 100k output pull-down, R73 3.3k raw VBUS bleeder, C38 100nF, C39 1nF C0G. C2 changed 10uF → 1uF/10V.
- `check_r41_vbus.py`: −40..85°C conservative threshold envelope 4.380..4.734V; **conditional** local unplug RC estimate 1.085ms if total raw-VBUS capacitance ≤1.5uF and no held external/backfed source. Bleeder ≤1.684mA at5.5V. Not bench proof: verify OFF/POR, actual capacitance, near-threshold comparator+firmware latency, dock reverse blocking, cable ringing with smaller C2 and **whole-device** USB suspend/charger policy. Never drive ESP GPIO with raw5V or substitute a non-fail-safe generic comparator/Schmitt buffer.
- **U8 geometry corrected:** new `ENKU:USBLC6_2SC6_ST_SOT23_6L`, ST figure19 pads 1.2x0.6mm,0.95mm pitch,2.30mm opposing pad centers; correct numbering1/2/3 left top→bottom and6/5/4 right top→bottom. AtPCB rotation180, GNDpin2 is world(55.35,108.8), VBUSpin5(53.05,108.8). Local symbol, schematic binding, PCB and pad assertions agree; Native U8/U10 pad audit exact matches.
- New via holes moved out of SMD lands. Source guard rejects new net-assigned land/hole intersections. An **inherited** J1 GND land-edge overlap atvia(65.1,94) remains a DFM review gate; this source check does not certify masks/paste/annuli or unassigned pads.

## Audit and release debt

- Active mechanical audit `R41_MECHANICAL_AUDIT.json`: 6 blockers,9 manual CAD gates. Four side buttons and SW1 provisional; display-over-hole overlap assumes centered registration and is not a proved collision. Need physical switch/button parts, actual display/FPC origin/fold, Hirose card travel, USB mating/case cutouts, battery swelling/NTC, dock mating, antenna and completeZ tolerance stack.
- Active supplier register `hardware/mainboard/procurement/COMPONENT_AUDIT_R41.csv`:132 current entries;112 purchasable parts unqualified (15 IDENTIFIED,92 UNSELECTED,5 PLACEHOLDER),20 board features. Exact prices/assembly availability **unquoted**. Added1IC+4R+2C, no bridge/hub. Engineering hours not metered; don't invent hours or turn CI runtime into human time.
- 241 non-unrouted DRC violations remain production blockers. Native detailed pad comparison has73 matches/59 differences, including legacy custom pads. Reconcile every difference and correct library identity/footprint production graphics without blindly moving routed copper. Pin1 assembly marking/3D/BOM/CPL review is not signed off.
- 210 unconnected items: remaining MCU3V3/peripheral, charger/dock controls and display network still need engineering. SD supply-drop/transients/clock-rate/return integrity and switching power layout are unqualified.
- USB D+/D− **unrouted**: use actual agreed PCBWay four-layer stackup for90Ω nominal pair, short ESD/series escapes, intact return, USB2.0 Full Speed (not480Mbps), cable/ESD/host testing. Do not claim a guessed stackup is factory-approved.
- No manufacturing Gerber/NC drill/BOM/CPL release, no fabrication order. Full ERC/DRC clean +mechanical/supplier/firmware tests remain required.

## CI and reproducible local source checks

`.github/workflows/native-base-mechanical.yml` runs the activePCB under NativeKiCad, strictERC, temporary root-name copy, pad audit, dual-zone refill/saved-layer audit, full parityDRC and priority/function gates. `hardware-checks.yml` includes current assembly/connectivity/VBUS/population plus explicit activePCB mechanical/procurement checks; R28–R40 fixtures continue as historical regressions. Old default root-PCB mechanical/provenance outputs describe historical boards, not R41.

From repository root:

```bash
python hardware/mainboard/kicad/check_schematics.py
python hardware/mainboard/kicad/check_r41_assembly.py
python hardware/mainboard/kicad/check_r41_sd_connectivity.py
python hardware/mainboard/kicad/check_r41_vbus.py
python hardware/mainboard/kicad/check_pcb_population.py
python hardware/mainboard/tools/mechanical_release_audit.py --pcb hardware/mainboard/kicad/enku-mainboard-r1.8-base-sd-card-completion.kicad_pcb
python hardware/mainboard/tools/check_component_manifest.py --pcb hardware/mainboard/kicad/enku-mainboard-r1.8-base-sd-card-completion.kicad_pcb --manifest hardware/mainboard/procurement/COMPONENT_AUDIT_R41.csv
```

`--release` on mechanical/procurement scripts must still fail. Do not weaken production gates to hide blockers. Source guards do not replace NativeKiCad.

## Next R42 pass

1. Read this handoff, R41 readiness, full raw reports, branch changes and latestCI. Start a separateR42 branch from current verified state; preserveR41 rollback.
2. Audit actualPCBWay stackup and the USB corridor before differential routing. Resolve ESD/series placement and same-layer escape without overriding disputed display pins.
3. Continue 3V3 MCU bypass/feed and safe charger/dock/local return paths; protect USB and SPI corridors and antenna keepout. Qualify thermal/current-drop/inrush, not merely connectivity.
4. Reconcile highest-risk manufacturer footprint discrepancies and mechanics; do not certify placeholders. Keep exact supplier questions explicit.
5. Run NativeERC0/parity0/priorityDRC0, saved inner-fill checks and functional continuity after each substantial batch; inspect all failures, fix, rerun. Report every remaining fullDRC/unconnected count, not only priority counts.
6. Preserve source, immutable real reports, actualcost/time when measurable, and honest PCBWay readiness. Complete a substantial engineering pass before returning a final report.

## GitHub transfer note

This Work session used public git clone/fetch for reads and the owner's GitHub connector for commit/ref writes; shell git push lacked credentials. One combined large transfer initially truncated `power.kicad_sch`; file was restored fully and NativeERC0 reverified. Transfer source content in bounded chunks, reject any “tokens truncated” marker, compare local bytes against fetched commits and use expected-head leases. Never print credentials or overwrite external branch updates.
