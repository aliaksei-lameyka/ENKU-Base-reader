# ENKU Base Reader

> **Current working source: R122, KiCad 10.0.7, NO FAB.**
> Open [the canonical project](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro).
> Full native local and server checkpoint: **0 opens, 115 other DRC, ERC 0, schematic parity 0**.
> R122 corrects Q1 Gate/Source pad locations using the Infineon top view and reroutes both connections. [R122 handoff](docs/WORK_HANDOFF_R122.md). USB filled-ground and via/Tag-Connect audits pass. [Actual R122 server evidence](docs/GITHUB_NATIVE_R122.md) confirms exact geometry, Q1 pin mapping and refilled USB reference planes; [R121 server evidence](docs/GITHUB_NATIVE_R121.md) is retained.
> Prior source and evidence remain in history. The R40–R50 engineering notes below are historical.

ENKU Base Reader is a compact open-source e-paper reader built around a custom ESP32-S3 mainboard.

The project is designed around a few practical ideas: local storage, physical controls, repairable construction, low idle power and hardware that can be inspected, modified and rebuilt without depending on a cloud service.

## Base R0.1

Base R0.1 is the first-spin engineering board.

Current hardware includes:

- 3.97-inch 800 × 480 e-paper display interface
- ESP32-S3-WROOM-1-N16R8
- USB-C
- microSD storage
- four side navigation buttons
- BMI270 IMU
- hard power switch
- battery charging and system power management

Hall, frontlight, wireless charging and Pogo/Dock are outside the dedicated Base scope; Pro will have its own PCB. Pro features remain on a separate board.

## Project status

**Base R0.1 is in active engineering validation and is not yet a production release.**

The schematic and PCB are source-controlled in KiCad and checked with lightweight structural tests plus native KiCad ERC/DRC at engineering gates.

## Historical R40–R50 engineering notes

Historical R48 source: [enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb](hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb), branch `engineering/r48-silkscreen-fab-clearance`. R41 completed microSD routing and VBUS monitoring; R42 advanced CPU power/reset/service and regulator feedback. R43 closed four side-button GND returns and local C26/C18/C19 ground loops. R44 physically routed hard slide SW1 PWR_GATE to Q2 and SW1 ground. R45 restored supplier-minimum legible 0.8mm service testpoint labels, RF warning and ENKU board identification. R46 verified the two left GPIO inputs via In1.Cu. R47 adds Native KiCad-validated B.Cu copper for both right GPIO inputs to SW5/SW6; all four physical reading GPIO nets are now source-connected (not yet manufacturer/3D-qualified); switch footprint mechanical MPN is not finalized. The experimental PCB holds 132 footprints, 515 segments, 132 vias and two editable inner GND zones (filled and tested in Native KiCad CI).

Native KiCad 8.0.9 R43 [verified run 37843277589](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37843277589): ERC 0 errors/0 warnings, parity 0, priority DRC 0, **239 other DRC violations and 146 unconnected items**. [R44 Native KiCad verified 37893508039](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893508039): strict ERC0, priority DRC0, 239 remaining non-unrouted DRC violations and 143 unconnected. Native return-ground gate on all 4 side buttons: 0 unconnected. PCBWay Ready remains **30%**. Battery/charger remain powered while OFF; electrical, thermal, mechanical, supplier and firmware qualification plus production outputs remain outstanding. Good Display's disputed pin5 remains unchanged.

For historical context, use [R41 handoff](docs/WORK_HANDOFF_R41.md) for historical decisions. See [manufacturing readiness and evidence](hardware/mainboard/manufacturing/PCBWAY_READINESS_R41.md) and [exact Native reports](hardware/mainboard/manufacturing/r41-native/).


## Repository

- `hardware/mainboard/kicad/` — editable KiCad source and project-local libraries
- `hardware/mainboard/production/` — release manufacturing files when a revision is frozen
- `docs/` — hardware, validation and manufacturing notes
- `.github/workflows/` — CI gates

Firmware and enclosure sources will be added to this repository as their public trees are cleaned and frozen.

## Hardware revisions

| Revision | Purpose | Status |
| --- | --- | --- |
| Base R0.1 | EVT / first-spin | In development |
| Base R0.2 | Bring-up corrections | Planned |
| Base R1.0 | Production candidate | Planned |

## Design principles

ENKU aims to be open, repairable, local-first and intentionally simple. The Base reader does not require a subscription or cloud service to read locally stored books.

## Manufacturing

Gerber, drill, BOM and pick-and-place packages will only be published when the corresponding board revision passes its fabrication release checklist. Editable source and generated production files are kept separate.

## License

A project license will be selected before the first public hardware release.

## USB-C direct microSD access

ENKU Base must expose its microSD card to a computer through USB-C using the ESP32-S3 native USB Mass Storage Device class (MSC); Wi-Fi uploader remains optional. USB is available when the reader power switch is ON. The PCB requires USB D−/D+ on ESP32-S3 GPIO19/20, SD SPI wiring, Type-C CC and ESD, **a fail-safe VBUS-present monitor**, and complete 4-layer controlled data-pair routing. R41 completes microSD SPI and ground continuity and implements a TLV3012B fail-safe VBUS monitor on GPIO17. R121 closes D+/D− through the ESD device and both USB-C contact orientations; the actual 90-ohm stackup is still unqualified; VBUS OFF/backfeed, disconnect timing, hotplug and suspend current still require bench qualification. USB MSC firmware and computer file transfer have not yet been implemented or tested. Firmware must grant the computer exclusive SD ownership and restore the reader filesystem only after safe disconnect. See [USB MSC hardware and firmware specification](docs/usb-mass-storage.md).

**PCBWay readiness is evidence-weighted, not a frozen 30%:** engineering stage R47 recalibrated at **43/100** with separate mandatory manufacturing **NO-GO** until full KiCad DRC, remaining copper, Good Display connector, footprint/vendor, USB MSC and assembly signoff. [Read the scoring model](hardware/mainboard/manufacturing/PCBWAY_SCORE_R48.md).

R48 final [Native 37898825797](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825797): 168 other DRC (130 library/38 silk), 139 electrically unrouted. [Hardware checks 37898825577](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825577) passed. **Weighted engineering 44%, PCBWay production NO-GO**; [scorecard](hardware/mainboard/manufacturing/PCBWAY_SCORE_R48.md).

## Good Display hardware response (2026-10-09)

Vendor has now supplied **GDEM0397T81P** 2D DWG / 3D STEP, 3.97-inch panel PDF, 24-pin dual-contact FPC candidate drawing and exact-panel Arduino driver demo; [technical handoff](hardware/mainboard/research/GOODDISPLAY_REPLY_2026-10-09.md). **Supplier email did not directly settle J3 pin5 VDHR vs VSH2 nor numeric FPC bend radius**; current R48 copper stays on manufacturer HOLD. The STEP CAD model prefix `GDEM` also differs from production panel `GDEY`, so don't assume exact FPC alignment. [PCBWay R49 readiness](hardware/mainboard/manufacturing/PCBWAY_READINESS_R49.md): weighted **44%**, manufacturing **NO-GO** until confirmed and final Native KiCad signoff. Reader Pro 4.26-inch frontlight+touch vendor suggestion is saved separately in private ENKU-lab; Pro is not this Base PCB.

