# ENKU Base Reader

**Working PCB: R141. Engineering branch: `engineering/r141-routing-power-fixes`. Manufacturing: NO FAB.**

ENKU Base is a compact 3.97-inch e-paper reader with physical controls, microSD and ESP32-S3. Four-layer 59x101x1.6mm board. Power is BQ24072T  + TPS63802 with direct PH-2 battery and separate cell NTC. Case thickness must not increase. Base excludes frontlight, Hall cover, dock andQi.

## Current engineering branch

| Need | Current entry |
| --- | --- |
| Editable R141 PCB and five schematic sheets | [R141 KiCad project](hardware/mainboard/r141/kicad/enku-mainboard-r0.1.kicad_pro) / [source guide](hardware/mainboard/r141/README.md) |
| Current status and release holds | [Current status](docs/CURRENT_STATUS.md) |
| R141 source, changes and verification | [Engineering handoff](docs/R141_ENGINEERING_HANDOFF_NO_FAB.md) / [progress](docs/WORK_PROGRESS_R141.md) |
| PCBWay preliminary review package | [Package directory](hardware/mainboard/r141/pcbway/) / [instructions](docs/PCBWAY_MANUFACTURING_NOTES_R141.md) / [archive record](docs/evidence/R141/final/PCBWAY_PACKET_R141.json) |
| Board PDF, layer/assembly views and schematics | [R141 drawings](hardware/mainboard/r141/pcbway/03_drawings/) |
| Checks before PCBWay review | [R141 methods and closure criteria](docs/PRE_REVIEW_CHECKS_R141.md) |
| Product and factory requirements | [Product qualification](docs/PRODUCT_QUALIFICATION_R139.md) / [factory-flash contract](docs/FACTORY_FLASH_CONTRACT_R139.md) |
| Battery constraints and availability | [Dated battery status](docs/BATTERY_STATUS_R139.md) |
| Development time | [Measured lower-bound hours ledger](docs/DEVELOPMENT_HOURS_READER.json) |

Exact working PCB SHA256: `b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe`. Source basename `r0.1` is retained for sheet/library references; it is not the board revision.

R141 local Native KiCad 10.0.7 evidence establishes **DRC0 / ERC0 / opens0 / parity0**, 20 inherited actual-source guards, invariant 438 pad definitions across 127 references, and independent comparison of all four complete copper images and 11 Gerbers plus drill/IPC/mask/paste/BOM/CPL. Historical R138 control passes 27 scopes and 20 effective negative cases. Read-only GitHub Actions verifies the archived R141 candidate outside the historical canonical checkout; [Actual server run38532688718](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38532688718) passed. [Downloaded proof](docs/GITHUB_R141.json) confirms API digest/CRC and all24 manufacturing files against the local exports after only timestamp normalization.

R141 shortens charger capacitor connections and the EPD switching routes, relocates R19 and revises control/SPI routing around ground references. 30 fast paths resolve; 14 fast nets have zero centreline length missing both inner ground planes. Common MOSI 0.741064mm / SCLK 1.057355mm preferred-plane gaps remain near MCU with far-inner ground present. These geometric results do not establish SI, impedance or physical qualification.

The PCBWay package contains exact current fabrication exports, 107 fitted top placements in 58 BOM groups, native/mapped CSV and Excel BOM/CPL, all-reference/pad maps, six filled/capped-via requests, editable source, three PDFs and verification/test requirements. Supplier rotation/origin import, actual stack/90-ohm USB,0.2mm bores, six fill/cap sites, USB short stakes and stencil process remain to be agreed. It is prepared for preliminary engineering review after further checks.

## Remaining release work

Independent schematic/FMEA, SI/PI/thermal/footprint/mechanical review precedes PCBWay submission. Real startup/reset, charging/NTC faults, combined Wi-Fi/SD/EPD loads, thermal, USB-MSC sharing the same microSD, PSRAM, firmware/fixture/FCT and consumer tests are **NOT RUN**. Current case CAD, exact panel/FPC fit andthin interchangeable protected 2000-2500mAh CN/PL packs remain open. No production firmware binary or factory test release is supplied.

## Retained history

`hardware/mainboard/kicad/` remains the immutable R138 comparison source. Open the linked R141 project for current engineering work. R139 qualification documents, R140 routing review, historical variants, acceptance guards/checkpoints and previously accepted server evidence are retained under their recorded revisions. They do not identify the current copper or constitute R141 factory input. Do not regenerate old goldens to accept a new layout.

A merge, package or computational pass does not release manufacture or purchasing. PCBWay review upload and eventual EVT/production are separate stages.

## Licensing

ENKU Base Reader uses **different licenses for different types of work**:

- **Original hardware design** — [CERN-OHL-W-2.0](LICENSE), including the KiCad PCB/schematic design and ENKU-authored hardware files.
- **Software and automation scripts** — [MIT](LICENSES/MIT.txt), including the Python validation tools and any future firmware expressly released in this repository.
- **Original project documentation** — [CC BY 4.0](LICENSES/CC-BY-4.0.txt), including README files and `docs/`.

Read the [license scope and third-party exceptions](LICENSE.md) before redistributing files or manufacturing modified boards. Third-party materials keep their own terms. The ENKU name and logos are not granted as trademarks by these licenses.

## Related project

[ENKU Originals](https://github.com/aliaksei-lameyka/ENKU-Originals) is a separate, early-stage experiment in AI-assisted, human-edited short fiction and reader-first EPUB delivery. It is currently private. **Its stories and editorial content are not licensed by this repository.**
