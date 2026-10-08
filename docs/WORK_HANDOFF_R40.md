# ENKU Base Reader — Work handoff (R40, 2026-10-08)

This file hands the live KiCad / PCBWay work from a long ChatGPT chat to **ChatGPT Work on mobile**. It is a state snapshot, **not** PCB production approval. Work should read this file and the actual linked source and CI logs before committing any engineering changes. Do not blindly trust handoff figures after new changes.

## Exact repository and active engineering state

- Repo: `aliaksei-lameyka/ENKU-Base-reader` (connected GitHub; may require plugin permission in a new Work chat).
- **Latest verified branch:** `engineering/r40-sd-spi-fanout`; branch tip when this handoff was written: `5780100cb181fd5111471152adcf042e201232fc`.
- **Active four-layer KiCad PCB:** `hardware/mainboard/kicad/enku-mainboard-r1.7-base-sd-power-sclk-mosi.kicad_pcb`.
- Root schematic: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_sch`, hierarchical `power.kicad_sch`, `mcu_io.kicad_sch`, `connectors.kicad_sch`, `epd_hv.kicad_sch`, and local `ENKU.kicad_sym`.
- Production source is **not** the stale `enku-mainboard-r0.1.kicad_pcb` kept in the repo. The native CI copies the active revision to the root board filename in a temporary checked-out runner. Follow the `.github/workflows/native-base-mechanical.yml` for each branch, and do not edit stale board by accident.
- Actual R40 Native KiCad run: https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807935362 (**success**).
- R40 structural hardware workflow: https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807935436 (**success**).
- R40 native results: **ERC 0 errors / 0 warnings, PCB–schematic parity 0, native critical shorts/edge/mask/dangling tracks/dangling vias 0; 236 other non-unrouted DRC violations (124 library footprint mismatches, 69 silk-over-copper, 27 silk overlaps, 16 text-height); 241 electrically unrouted items**.
- PCB currently **125 footprint objects, 63 copper segment records, 20 plated vias, one local In2.Cu GND zone**. KiCad CI fills the GND zone via `refill_r38_zone.py` and runs DRC on the *refilled diagnostic copy*.
- **PCBWay readiness estimate: 30/100**. Gerbers are NOT ready. The native workflow returning green means stringent **priority** errors passed, not that full DRC passed.

## Immutable product and electrical scope

ENKU Base is a small **portrait 3.97-inch 800x480 e-paper reader** with a 59x101 mm four-layer prototype PCB, ESP32-S3-WROOM-1-N16R8, removable microSD, battery charging (1S LiPo with NTC), USB-C, four side-mounted reading buttons (two per side for left/right-hand remapping), BMI270 IMU, repairable hardware, dock service interface. **Base and Pro use different boards**. Base has **NO Hall sensor, wireless Qi charging, or frontlight**. Pro will be designed separately. No touch panel or cloud requirement.

- High-side power gate R35: AO3401A P-channel MOSFET `Q2` at (55.5,82.5) switches local `VSYS -> SYS_EN` close to TPS63802; case-edge slide `SW1` carries **gate control only** `PWR_GATE -> GND`, pulled up with R40 100k. Existing SW1 footprint is a provisional physical shape, NOT manufacturer-qualified. Battery and BQ25185 charging remain alive in switch OFF; this is not pack galvanic isolation.
- R34 gated battery ADC: TMUX1101 `U9` isolates `BAT_ADC` resistor divider from always-live VBAT when 3V3 is off; qualification of actual leakage/power-off injection still pending.
- R36–R38 built local PMOS/charger + 3V3 copper and **one real KiCad-filled In2.Cu GND island** with seven tested local return vias. Zone fill must be rerun and tested whenever other layers change.
- R39–R40 started microSD supply + SPI fanout: SD VDD is routed via In1.Cu to bulk capacitor; `SD_SCLK_CARD` has initial B.Cu breakout to R21, `SD_MOSI_CARD` has initial In1.Cu breakout to R20. `SD_CS_CARD` and `SD_MISO_CARD` still need routing, as do MCU-to-SD signal sections.
- **Non-negotiable: USB-C must expose the SAME microSD card to Windows/macOS/Linux as USB Mass Storage (MSC), not only by Wi-Fi.** Use ESP32-S3 native USB-OTG GPIO19=D− on U1 pad13 and GPIO20=D+ on U1 pad14, plus the existing four-wire SPI microSD. The USB-C reversible D+/- contacts, 5.1k CC pull-downs, USB ESD U8, and tuning R64/R65 are in schematics/PCB; **actual USB data pair copper is not routed**. Firmware shall implement an exclusive USB MSC block-device mode and release local FatFS/library/uploader access before host read/write, then remount/reconcile on safe host eject/disconnect. Wi-Fi uploader remains optional. No mandatory account/subscription/app.
- **USB VBUS-present sensing is not implemented!** This reader is battery-powered, so do not connect 5V directly to ESP32 or introduce OFF-state backfeed through a careless resistor divider. GPIO17 / U1 pad10 is free/reserved for safe VBUS detect, to be correctly engineered against Espressif USB requirements. The device currently only enumerates when user turns slide switch ON; auto-on for USB when switched off is a **separate architecture decision**. Do not silently change this.
- **USB D+/D− routing must satisfy controlled-impedance 90Ω differential target for actual PCBWay 4-layer stackup**, short ESD/series parts and intact adjacent return path. No guesswork or mixing with switching power; validate against real stackup/manufacturer.
- USB Mass Storage firmware, FAT ownership state machine, host suspend/reconnect, SD hot-removal, power removal mid-write, and Windows/macOS/Linux end-to-end testing are **not implemented or proven** by PCB connectivity checks. See `docs/usb-mass-storage.md`.
- **Good Display supplier has been emailed**, awaiting written confirmation on GDEY0397T81P panel **pin 5 VDHR in pin table versus VSH2 in typical application diagram** and exact flex shape/fold/connector mating. Keep J3 current `EPD_VSH2` *candidate* unchanged until answered; do not invent a pinout or pre-route unknown FPC/HV copper.
- The Pro-specific frontlight, Qi, Hall and alternate panel circuitry must NOT leak back into this Base design.

## Instructions for next autonomous engineering pass

Work in large, meaningful batches **without repeatedly asking the owner to type “continue.”** Actually edit the GitHub KiCad sources; a status report with no engineering change is not progress. Make a **new R41 branch** from the verified R40 tip, retain R40 as a rollback baseline, and batch all related source/test/doc/workflow changes in logical commits.

1. Fetch current branch, schematics, PCB, local libraries, test scripts, workflow and Native KiCad logs. Confirm there have not been external changes. If GitHub access is missing, request connector authorization rather than guessing.
2. Complete the remaining **microSD CS and MISO card-side escapes** and review already added SCLK/MOSI/VDD/vias for 0.2mm or greater clearances and signal return. Do not route through card insertion/courtyard/mechanical keepouts. Don't confuse pad coordinate rotation or exposed back-side testpoints with front copper pads.
3. Audit **USB-C schematic netlist all the way J5 ↔ U8 ↔ R64/R65 ↔ ESP32 pads 13/14**, CC/ESD/power-domain paths, 3V3_SYS card power, and connector footprint orientations. If PCBWay real stack-up is not verified, *document a protected USB corridor and constraints*, rather than asserting 90Ω guaranteed.
4. Research and, only when electrically justified with original datasheets, design safe **VBUS-present detection** on U1 pad10 with no 5V GPIO stress or powered-off backfeed; update schematic, PCB, local symbol/footprint and ERC gate together.
5. Route additional safe local connections in sensible order (3V3 to CPU and SD, USB/SD after corridor constraints, return vias/planes, dock/charging) while keeping the manufacturer-questioned EPD FPC unmodified.
6. In CI, **native KiCad ERC hard 0 errors/0 warnings, PCB–schematic parity 0, priority DRC 0** for shorts/mask/edge/clearance/dangling tracks/vias, native GND zone refill, true footprint and physical pin orientation tests, and report exact remaining unconnected and total non-unrouted violations. If CI fails: read complete job logs, find the root cause, fix, rerun until green; do not redefine a failure as success.
7. Update `hardware/mainboard/manufacturing/PCBWAY_READINESS_R41.md` with truthful verification links, concrete deltas, *% PCBWay-ready*, high-priority remaining blockers, parts cost impacts and actual engineering hours when properly measurable. Do not fabricate duration/hours or increase readiness for mere extra tracks/green ERC.

## Collaboration and output requirements

- Execute a **substantial batch** before stopping, not micro-status iterations. Keep progress visible but don't require trivial approvals for routine engineering. Stop for genuine manufacturing/safety/requirements decisions (vendor pinout, physical switch MPN, forced USB-when-OFF architecture, unknown battery connector).
- Keep ENKU Base/Pro split, user-first ergonomics, repairability, pocket-size and very-low budget in scope.
- Deliver branch URL, actual commit hash, changed paths, CI run URLs and their conclusions, ERC/DRC summaries, remaining unrouted, hard blockers and % PCBWay readiness. **Never claim fabrication-ready until full routing, ERC and DRC clean, production 3D/mechanics, Gerber/NC drill/BOM/CPL and supplier signoff.**
- This entire handoff describes **existing source**, not an instruction to invent a finished PCB when repository tools are missing.
