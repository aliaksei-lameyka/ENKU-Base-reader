# ENKU Base Reader

**Working PCB: R144. Branch: `engineering/r144-power-margin`. Engineering review / NO FAB.**

3.97-inch GDEY0397T81P /SSD1677, ESP32-S3-WROOM-1-N16R8, BMI270, shared SPI microSD.59x101x1.6mm, four copper layers. BQ24072T power path + TPS63802, protected two-wire PH2 pack with separate cell NTC. Base has no dock/frontlight/Hall/Qi. Case thickness is unchanged.

R144 jointly redesigns supply/reset: TPS389001DSER, precision sense/feedback and forced PWM after soft-start; nominal3.220352V. Initial and declared +/-0.1% extra solder-shift reserves pass. Lifetime adverse-shift and real dynamic startup/ripple/load/OFF qualification remain HOLD. The existing R143 Hirose J3 OEM correction is retained.141 refs,473 native pads,384 vias,120 fitted top parts; R67/R99 DNP, R97 FIT only.

Native KiCad10.0.7 DRC/ERC/opens/parity0, finite source delta, full four-layer copper, independent Gerber connectivity84 nets and actual injected open/short,11-layer Gerber/drill/IPC356/mask/paste/silk/BOM/CPL and OEM pin/land checks passed locally and in [source-pinned GitHub run38693384483](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38693384483). Verified source commit `609f8ac00357b9b0c6b3c43c381469c498453a11`; source PCB SHA256 `676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c`. Downloaded server artifact SHA/CRC and24 fresh manufacturing files agree after creation-timestamp-only normalization. Immutable R138 also passed27 scopes/20 effective rejection cases; historical goldens were not rewritten.

**Physical tests NOT RUN.** FPC actual-lot/pose, protected battery/NTC, stackup/drill/fill-cap/common stencil/reflow, lifetime/dynamic rails, effective capacitance/EPD power, reproducible FCT firmware and per-board acceptance remain open. Start the proposed5-10 unit pilot with1-2 assemblies once prerequisites are resolved. No guarantee of prototype startup or manufacturing release is claimed.

| Need | Current R144 entry |
| --- | --- |
| Editable source | [KiCad](hardware/mainboard/r144/kicad/enku-mainboard-r0.1.kicad_pro), [68-file manifest](hardware/mainboard/r144/source_manifest_R144.json), [finite delta](hardware/mainboard/r144/scope_R144.json) |
| Executed checks | [Pre-review](docs/PRE_REVIEW_CHECKS_R144.md), [server proof](docs/GITHUB_R144.json) |
| Remaining qualifications | [Startup risks](docs/STARTUP_RISKS_R144.md), [FPC](docs/FPC_CONNECTOR_REVIEW_R144.md) |
| Annotated routing review | [Procedure and open candidate queue](docs/VISUAL_REVIEW_WORKFLOW_R144.md); read-only, no copper changes |
| User green marks | [All18 dispositions](docs/MARKED_REGIONS_REVIEW_R144.md):7 locally acceptable,11 change-queue marks; BMI270 decoupling and SD MOSI priority; copper unchanged |
| Manufacturing inputs | [PCBWay review packet](hardware/mainboard/r144/pcbway/), [instructions](docs/PCBWAY_MANUFACTURING_NOTES_R144.md) |
| PDF board/layers/schematics | [Drawings](hardware/mainboard/r144/pcbway/03_drawings/) |
| BOM/CPL | [Assembly](hardware/mainboard/r144/pcbway/02_assembly/) |
| First5-10 procedures | [FCT plan](docs/FCT_PLAN_R144.md) |
| Bounded development hours | [Ledger](docs/DEVELOPMENT_HOURS_READER.json) |

The r0.1 basename preserves schematic hierarchy, not revision numbering. `hardware/mainboard/kicad/` is immutable R138; R141/R142/R143 retain historical source/evidence. Never mix their manufacturing files with R144. [Report clarification](docs/REPORT_CLARIFICATIONS_R144.md) preserves raw server evidence while correcting one informational nominal divider-current field.

Original hardware CERN-OHL-W-2.0. Automation MIT. [Licensing](LICENSE.md).

## English review and Gerber download

[English engineering review package](hardware/mainboard/r144/pcbway_en/README_PCBWAY_R144_EN_NO_FAB.md), [English board review PDF](hardware/mainboard/r144/pcbway_en/03_drawings/ENKU_R144_Board_Review_EN_NO_FAB.pdf) and [separate flat Gerber/drill ZIP](hardware/mainboard/r144/pcbway_en/ENKU_R144_GERBER.zip). The ZIP contains all11 actual Gerber layers and separate PTH/NPTH drills at its root. Manufacturing/source bytes match verified R144. NO FAB and all existing qualification holds remain in force.
