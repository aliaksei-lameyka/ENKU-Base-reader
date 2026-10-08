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

Hall, frontlight and wireless charging are outside the dedicated Base scope; Pro will have its own PCB. They can return in later revisions after the Base hardware has completed bring-up.

## Project status

**Base R0.1 is in active engineering validation and is not yet a production release.**

The schematic and PCB are source-controlled in KiCad and checked with lightweight structural tests plus native KiCad ERC/DRC at engineering gates.

R40 microSD power and first SPI fanout trial: hardware/mainboard/kicad/enku-mainboard-r1.7-base-sd-power-sclk-mosi.kicad_pcb (first gate, VSYS, SYS_EN copper tracks; not a fabrication release). Battery + charger stay powered while OFF; ADC leakage/backfeed still requires qualification. The R37 branch extends the first physical routing to 48 copper segments, thirteen plated vias and one editable In2.Cu GND polygon (R38 trial); Native KiCad CI refills this zone and verifies copper, but full DRC still fails on 236 non-unrouted violations and 245 incomplete connections. The majority of the board remains unrouted; full Native KiCad DRC, electrical/thermal, supplier and mechanical qualification and manufacturing outputs remain outstanding.

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

ENKU Base must expose its microSD card to a computer through USB-C using the ESP32-S3 native USB Mass Storage Device class (MSC); Wi-Fi uploader remains optional. USB is available when the reader power switch is ON. The PCB requires USB D−/D+ on ESP32-S3 GPIO19/20, SD SPI wiring, Type-C CC and ESD, **a fail-safe VBUS-present monitor**, and complete 4-layer controlled data-pair routing. The active R40 branch begins microSD SCLK/MOSI breakout with genuine via transitions, but USB and most SPI/card copper remain unrouted. Firmware must grant the computer exclusive SD ownership and restore the reader filesystem only after safe disconnect. See [USB MSC hardware and firmware specification](docs/usb-mass-storage.md).
