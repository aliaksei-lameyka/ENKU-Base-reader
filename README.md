# ENKU Base Reader

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
- rear dock interface

Hall, frontlight and wireless charging are outside the dedicated Base scope; Pro will have its own PCB. Pro features remain on a separate board.

## Project status

**Base R0.1 is in active engineering validation and is not yet a production release.**

The schematic and PCB are source-controlled in KiCad and checked with lightweight structural tests plus native KiCad ERC/DRC at engineering gates.

Active R43 engineering source: [enku-mainboard-r2.0-base-reading-ground-returns.kicad_pcb](hardware/mainboard/kicad/enku-mainboard-r2.0-base-reading-ground-returns.kicad_pcb), branch `engineering/r43-reading-button-ground-returns`. R41 completed microSD routing and VBUS monitoring; R42 advanced CPU power/reset/service and regulator feedback. R43 closes four side-button GND returns and local C26/C18/C19 ground loops. The experimental PCB holds 132 footprints, 442 segments, 121 vias and two editable inner GND zones (filled and tested in Native KiCad CI).

Last verified R42 KiCad 8.0.9: ERC 0 errors/0 warnings, parity 0, priority DRC 0, **239 other DRC violations and 152 unconnected items**. R43 requires a NEW Native pass; do not assume R42 numbers apply to new ground traces. PCBWay Ready remains **30%**. Battery/charger remain powered while OFF; electrical, thermal, mechanical, supplier and firmware qualification plus production outputs remain outstanding. Good Display's disputed pin5 remains unchanged.

Continue from R43 active board; use [R41 handoff](docs/WORK_HANDOFF_R41.md) for historical decisions. See [manufacturing readiness and evidence](hardware/mainboard/manufacturing/PCBWAY_READINESS_R41.md) and [exact Native reports](hardware/mainboard/manufacturing/r41-native/).


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

ENKU Base must expose its microSD card to a computer through USB-C using the ESP32-S3 native USB Mass Storage Device class (MSC); Wi-Fi uploader remains optional. USB is available when the reader power switch is ON. The PCB requires USB D−/D+ on ESP32-S3 GPIO19/20, SD SPI wiring, Type-C CC and ESD, **a fail-safe VBUS-present monitor**, and complete 4-layer controlled data-pair routing. R41 completes microSD SPI and ground continuity and implements a TLV3012B fail-safe VBUS monitor on GPIO17. USB D+/D− remain unrouted pending the actual 90-ohm stackup; VBUS OFF/backfeed, disconnect timing, hotplug and suspend current still require bench qualification. USB MSC firmware and computer file transfer have not yet been implemented or tested. Firmware must grant the computer exclusive SD ownership and restore the reader filesystem only after safe disconnect. See [USB MSC hardware and firmware specification](docs/usb-mass-storage.md).
