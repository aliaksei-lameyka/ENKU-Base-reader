# ENKU Base Reader

ENKU Base is a compact, repairable 3.97-inch e-paper reader with physical controls, microSD and an ESP32-S3. It works locally without a required cloud service or subscription.

**Physical PCB: R138. Qualification/documentation: R139. Manufacturing: NO FAB.** R139 adds recovery review, the checked PCBWay engineering-review packet and test requirements. Physical product qualification is NOT RUN.

## Start here

| Need | Current entry |
| --- | --- |
| Status and remaining release gates | [Current status](docs/CURRENT_STATUS.md) |
| Editable PCB and five schematic sheets | [Canonical KiCad](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro) / [directory guide](hardware/mainboard/kicad/README.md) |
| Mainboard overview | [Current mainboard entry](hardware/mainboard/CURRENT_STATUS.md) |
| Continue engineering | [R139 handoff](docs/WORK_HANDOFF_R139.md) |
| PCBWay archive contents and hash | [Packet record](docs/qualification/R139/PCBWAY_PACKET_R138.json) / [process instructions](docs/PCBWAY_MANUFACTURING_NOTES_R138.md) |
| Product and factory tests | [Qualification](docs/PRODUCT_QUALIFICATION_R139.md) / [flashing contract](docs/FACTORY_FLASH_CONTRACT_R139.md) |
| Latest battery answers | [13 October battery status](docs/BATTERY_STATUS_R139.md) |
| Actual native verification | [R138 main/engineering evidence](docs/GITHUB_MAIN_R138.json) |
| Documentation/history | [Documentation index](docs/README.md) / [consolidation](docs/REPOSITORY_CONSOLIDATION_R139.md) |
| Development time | [Reader hours ledger](docs/DEVELOPMENT_HOURS_READER.json) |

## Hardware and verification

ESP32-S3-WROOM-1-N16R8, 3.97-inch 800x480 e-paper interface, GCT USB4215-03-A USB-C with ESD, microSD, BMI270, four E-Switch TL1016AAF160QG side buttons and a hard reader-load switch. Power: BQ24072T + TPS63802, direct JST PH-2 and a separate attached cell NTC. Four-layer PCB: 59x101x1.6mm. **Case thickness must not increase.** Frontlight, Hall/magnetic cover, wireless charging and dock belong to the separate Pro design.

Accepted actual GitHub artifacts establish KiCad10.0.7 **DRC 0 / ERC 0 / opens 0 / parity 0**, 27 R138 scopes and 20 effective rejection cases. Independent checks cover all four copper images, 11 Gerbers, 354 holes/slots, 753 IPC records, stencil, fitted BOM/CPL, component geometry and special-via requests. R139 adds source-only J7 UART/BOOT/EN recovery review and a fresh zero-result DRC/ERC run.

The engineering-review ZIP contains exact accepted manufacturing exports, 107 fitted placements, complete reference/pad maps, editable source, four PDFs (30 checked pages), process requirements and 20 physical-test groups. Its filename/hash are in the packet record. No validated factory firmware binary is supplied, and the archive grants no manufacturing permission.

## Remaining release work

Weak/absent-battery and blank-firmware startup in initial USB100 mode; reset ramps/cycles; effective capacitance and combined Wi-Fi/SD/EPD loads; real-pack CC/CV/timers and NTC faults/retention; final case/panel/FPC; two thin interchangeable protected 2000-2500mAh packs with China/Poland supply; actual stack/90-ohm USB, holes, six fill/cap sites, USB-stake and stencil approval; validated firmware/fixture/numeric FCT limits.

Polybattery now says LP405079 and LP355380 are unavailable. Koosay's complete 405381 pack/stock remain unconfirmed after the existing follow-up. Ropla's 5.2mm finished AKY0156 is excluded for thickness. Original BQ25185/~300mA RFQs are obsolete: the board uses BQ24072T, 445mA nominal, modeled maximum492.42mA and BAT max4.24V. See the dated battery review.

## Source and retained history

Open the canonical project above; its r0.1 filename is retained for sheet/library references. Older PCB variants, mechanical trials, readiness reports and proof are historical, not factory inputs. Regression verification pins 1325 accepted historical files. The old hardware/mainboard/README.md is a frozen R136 snapshot; use the current mainboard entry linked above.

Consolidation retains all observed branch heads and exact differences for five formerly separate evidence/research histories. Superseded connector/switch trials do not change current R138 copper. Historical branches, licenses and checkpoints are preserved. Local KiCad sessions, Python caches/runtime outputs and private supplier material are excluded from new Git additions.

A merge or native pass does not authorize manufacture, purchase, factory upload or supplier messaging. Approved EVT samples and physical qualification precede consumer release.

## Licensing

ENKU Base Reader uses **different licenses for different types of work**:

- **Original hardware design** — [CERN-OHL-W-2.0](LICENSE), including the KiCad PCB/schematic design and ENKU-authored hardware files.
- **Software and automation scripts** — [MIT](LICENSES/MIT.txt), including the Python validation tools and any future firmware expressly released in this repository.
- **Original project documentation** — [CC BY 4.0](LICENSES/CC-BY-4.0.txt), including README files and `docs/`.

Read the [license scope and third-party exceptions](LICENSE.md) before redistributing files or manufacturing modified boards. Third-party materials keep their own terms. The ENKU name and logos are not granted as trademarks by these licenses.

## Related project

[ENKU Originals](https://github.com/aliaksei-lameyka/ENKU-Originals) is a separate, early-stage experiment in AI-assisted, human-edited short fiction and reader-first EPUB delivery. It is currently private. **Its stories and editorial content are not licensed by this repository.**
