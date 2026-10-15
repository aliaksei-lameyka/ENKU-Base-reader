# ENKU Base Reader

**Working PCB: R145. Branch: `engineering/r145-marked-layout`. Engineering review / NO FAB.**

R145 corrects the11 queued user green marks: local BMI270 decoupling, microSD MOSI topology, repeated/overlapping copper and selected power/ground meshes. Only C18/C19 move.141 refs,473 pads,386 vias,120 fitted top parts; R67/R99 DNP, R97 FIT. All values, MPNs, netlist topology, libraries, rules,59x101x1.6mm board, USB data, antenna and panel interface remain preserved.

Native KiCad10.0.7 DRC/ERC/opens/parity0 and the complete local independent manufacturing/electrical/OEM checks pass for PCB SHA256 `bee45ea1b8e4532112e6ec91a181a1e1bd42d758ad981bf91a8a34e967dd924c`. Actual source-pinned server proof is recorded separately once retrieved; local verification is not labelled server verification.

| Need | Current entry |
| --- | --- |
| Changes and next visual review | [R145 handoff](docs/WORK_HANDOFF_R145.md) |
| Editable source | [KiCad](hardware/mainboard/r145/kicad/enku-mainboard-r0.1.kicad_pro), [68-file manifest](hardware/mainboard/r145/source_manifest_R145.json), [finite scope](hardware/mainboard/r145/scope_R145.json) |
| R144 user marks | [All18 reviewed dispositions](docs/MARKED_REGIONS_REVIEW_R144.md) |
| Current verification | [R145 checks](hardware/mainboard/r145/checks/), current source-pinned evidence after CI |
| Manufacturing review files | R145 packet is generated from the verified source; keep all revisions separate. |
| Physical qualifications | [Inherited risks](docs/STARTUP_RISKS_R144.md), [FPC](docs/FPC_CONNECTOR_REVIEW_R144.md), [pilot FCT](docs/FCT_PLAN_R144.md) |
| Bounded development hours | [Ledger](docs/DEVELOPMENT_HOURS_READER.json) |

3.97-inch GDEY0397T81P/SSD1677, ESP32-S3-WROOM-1-N16R8, BMI270 and shared-SPI microSD. BQ24072T power path and TPS63802/TPS389001 precision supply/reset. Base has no dock/frontlight/Hall/Qi. Case thickness is unchanged. Nominal3.220352V and all R144 startup selections are preserved.

**Physical tests NOT RUN.** Factory, FPC, protected battery/NTC, lifetime/dynamic rails, effective capacitance/EPD and FCT/per-board evidence remain open. No prototype-startup guarantee or manufacturing release is claimed. General unmarked zigzags await the next user-assisted visual pass.

R144 and older sources/evidence remain historical, including [R144 English review](hardware/mainboard/r144/pcbway_en/README_PCBWAY_R144_EN_NO_FAB.md). The r0.1 file basename preserves schematic hierarchy; it is not the working revision number. Never mix manufacturing exports from different revisions.

Original hardware CERN-OHL-W-2.0. Automation MIT. [Licensing](LICENSE.md).
