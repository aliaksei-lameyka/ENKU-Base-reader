# ENKU Base R41 — SD continuity, USB power and fail-safe VBUS

**PCBWay Ready: 30/100, unchanged. Manufacturing release BLOCKED.** Functional copper has advanced substantially, but the percentage is a planning estimate, not trace coverage or a fabrication approval.

## Active source and verified evidence

- Branch: `engineering/r41-sd-card-completion`, derived from R40 handoff tip `518343ce5365afe407434f52f3faf52757b787db`. R40 routing baseline remains untouched.
- Active PCB: `hardware/mainboard/kicad/enku-mainboard-r1.8-base-sd-card-completion.kicad_pcb`; root schematic remains `enku-mainboard-r0.1.kicad_sch` with its four Base sheets. The old root-named PCB and R28–R40 boards are historical fixtures, not the active source.
- Verified source commit: `cf04f72110456540a6bb1c9ef0a49f7621f87319`.
- [Native KiCad 8.0.9 run 37815837327](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37815837327), job `113444113178`: **SUCCESS**. ERC **0 errors/0 warnings**, schematic parity **0**, priority copper/mask/edge/hole/clearance/dangling DRC **0**. Both inner GND zones refilled, saved, reopened and checked: In1.Cu and In2.Cu, one filled polygon each.
- [Active hardware/source/mechanical/procurement checks 37816685057](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37816685057): **SUCCESS**, commit `621e9df64eae1afd63eae35c61bdd8bdacd9aea6`. Current 132-entry register and active mechanical blocker audit executed in CI; historical fixtures remain separate.
- **Full DRC is NOT clean:** 241 violations (130 library footprint mismatches, 68 silk over copper, 27 silk overlaps, 16 text height); **210 unconnected items**, footprint_errors 0. A green priority gate does not waive these errors.
- Native functional gates: **0 unconnected items involving microSD J2; 0 on USB_VBUS_* nets**. Shared SPI_MOSI/SPI_SCLK branches to display resistors R34/R33 remain unrouted; this does not break the completed MCU-to-SD paths.
- Exact original report bytes are committed in `r41-native/`: `r29-erc.rpt`, `r29-drc.json`, `r29-footprint-pad-audit.json`, `r41-ground-fill.json`. Filenames retain the existing CI naming convention; their provenance is **R41**, not R29. `verification.json` records commit/run IDs, counts, hashes and priority types.
- [CI artifact 11566888024](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37815837327/artifacts/11566888024) additionally contains the Native-refilled diagnostic PCB. Artifact expires 2027-01-06; committed reports remain in Git history.

| Metric | R40 | R41 |
|---|---:|---:|
| Footprints, including holes | 125 | 132 |
| Copper segment records | 63 | 270 |
| Plated vias | 20 | 66 |
| Inner GND zones | 1 local island | 2 expanded zones |
| ERC errors / warnings | 0 / 0 | 0 / 0 |
| Schematic parity / priority DRC | 0 / 0 | 0 / 0 |
| Non-unrouted DRC violations | 236 | 241 |
| Unconnected items | 241 | 210 |
| PCBWay Ready estimate | 30% | 30% |

Unconnected-item counts are KiCad diagnostics, not a percent-routed formula: adding parts, vias and ground connectivity changes the graph.

## Engineering delivered

1. Completed card-side CS/MISO escapes, MCU-to-R19–R22 SPI routes, CS pull-up R23, C17 branch and **all J2 GND/contact/shell returns**. Native continuity gate protects the complete card component, not just names in a netlist.
2. Routed CC1/CC2 pull-downs, both USB-C VBUS contact pairs, C2 raw input, U2 TPS2121 USB input and U8 VBUS. Added return vias and extended inner GND polygons around the lower board without changing the antenna keepout. USB D+/D− remain unrouted pending the actual 90-ohm PCBWay stackup/corridor review.
3. Added U10 **TLV3012BIDBVR** fail-safe VBUS comparator on switched 3V3_SYS, output to GPIO17/U1 pad10; R70 26.7k and R71 10k, both 0.1%/25ppm; R72 100k output pull-down; R73 3.3k bleeder; C38 100nF and C39 1nF C0G. C2 is now 1uF/10V. No non-B TLV3012 substitution is permitted.
4. Corrected U8 USBLC6-2SC6 embedded footprint from an incorrectly numbered generic SOT23-6 to ST figure19 SOT23-6L lands. Local library, cached schematic symbol, instance binding and PCB now agree. Native pad audit reports **exact pad matches for U8 and U10**.
5. Removed new via holes from SD/comparator/USB SMD lands; added a source guard against new hole/land intersections. `R41_VIA_IN_PAD_AUDIT.json` retains an inherited J1 GND land-edge intersection at (65.1,94), requiring production DFM; zero **new** hole intersections is not full mask/paste/annulus signoff.
6. Updated population and Base GPIO17 gates to the actual R41 design. Added explicit active-PCB mechanical/procurement checks; historical regression checks still run against their named historical boards. New `COMPONENT_AUDIT_R41.csv` covers every one of the 132 footprints with current values, positions and rotations.

## VBUS safety calculation and bench gates

`check_r41_vbus.py` gives a conservative −40..85°C threshold envelope **4.380–4.734V**, combining reference range/drift, input offset, hysteresis and resistor tolerance/drift. Conditional local unplug estimate **1.085ms** assumes total raw-VBUS capacitance ≤1.5uF and no retained external/backfed source. It is **not** measured timing or complete USB compliance. R73 consumes up to **1.684mA** at 5.5V, before other loads.

Measure OFF leakage/backfeed, POR behavior, simultaneous dock+USB removal, actual capacitance, comparator response near threshold plus firmware detachment latency, long-cable hotplug ringing at the reduced C2, charger-disable/suspend total current, card write brownouts and mux reverse blocking. Keep required downstream bulk/bypass. USB MSC still requires switch ON; charging remains alive with switch OFF, with no automatic USB wake redesign.

Primary references: [Espressif self-powered USB](https://docs.espressif.com/projects/esp-usb/en/latest/esp32s3/usb_device.html), [TI TLV3012B SBOS300C](https://www.ti.com/lit/gpn/TLV3012B), [TI TPS2121](https://www.ti.com/lit/ds/symlink/tps2121.pdf), [ST USBLC6-2 DS4260](https://www.st.com/resource/en/datasheet/usblc6-2.pdf).

## Production blockers and next pass

- 210 unconnected items, including remaining MCU supply/peripheral, display and charger/dock work; 241 other DRC violations. Reconcile footprint identity and manufacturer lands **before** blindly updating factory footprints on routed copper. Native detailed pad audit: 73 pads_match / 59 pads_differ; differences include prior deliberate custom patterns but every discrepancy still needs a documented disposition.
- Actual PCBWay four-layer stackup, continuous USB return corridor, USB differential pair and ESD/series routing. Inner zones contain signal/power clearances; they are not certified uninterrupted planes. SD signal integrity, via returns, clock rate and power-drop budget remain unqualified.
- Mechanical diagnostic: 6 blockers and 9 manual CAD gates (`R41_MECHANICAL_AUDIT.json`). SW3–SW6/SW1 are provisional; centered display-to-hole overlap is a **hypothesis**, not a proved collision. Need supplier 3D, card travel, connector mating, LiPo/NTC registration, enclosure tolerances and antenna clearance.
- Good Display GDEY0397T81P pin5 VDHR versus VSH2 and flex/mating decision remains unresolved in available project evidence. **J3 candidate EPD_VSH2 and display copper unchanged.**
- USB MSC firmware/backend and exclusive local-FatFS/host ownership not implemented or tested. Same microSD must mount over USB-C without Wi-Fi; Windows/macOS/Linux mount/copy/eject, suspend/reconnect and interrupted writes remain required.
- Procurement register: 112 purchasable parts not qualified; 15 IDENTIFIED, 92 UNSELECTED, 5 PLACEHOLDER, 20 PCB_FEATURE. No PCBWay sourcing approval follows from register integrity.
- Full ERC/DRC clean, mechanical signoff, Gerber/NC drill/BOM/CPL package and manufacturer review still required. **No manufacturing files or fabrication order released. Base has no Hall/Qi/frontlight; Pro stays a separate board.**

## Cost, time and iteration record

Delta: one comparator, four resistors and two capacitors added; C2 value changed and U8 footprint corrected. No USB SD bridge/hub added. Exact passive MPNs, comparator availability and PCBWay assembly prices are **unquoted**; no invented cost saving or total BOM price. Precision resistors and the bleeder's current cost are explicit procurement/power tradeoffs.

Engineering hours were not metered; do not convert CI runtime into human/billable hours. Final Native run started 2026-10-08 17:20:47 UTC; diagnostic reports timestamp 17:21:24–26 UTC.

Previous failed runs remain evidence, not release passes: [37812400417](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37812400417) (GND stitching collisions), [37813759798](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37813759798) (truncated transferred power schematic, restored), [37813952438](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37813952438) (CC2/dock and redundant vias), [37814977418](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37814977418) (SD via relocation clearance), [37815249984](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37815249984) (shell return crossed MISO). Every source fault was corrected before the final successful Native run; gates were not relaxed to accept these failures.
