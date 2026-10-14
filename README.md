# ENKU Base Reader

**Working PCB: R142. Branch: `engineering/r142-startup-independent-review`. Manufacturing: NO FAB.**

3.97-inch GDEY0397T81P / SSD1677 reader, ESP32-S3-WROOM-1-N16R8, BMI270 and shared SPI microSD. Four copper layers, 59x101x1.6mm. BQ24072T power path and TPS63802 supply; PH2 two-wire protected battery plus separate cell NTC. Base has no dock, frontlight, Hall or Qi. Case thickness remains unchanged.

| Need | R142 entry |
| --- | --- |
| Current editable project | [KiCad project](hardware/mainboard/r142/kicad/enku-mainboard-r0.1.kicad_pro) / [source manifest](hardware/mainboard/r142/source_manifest_R142.json) |
| Findings and computational checks | [Pre-review report](docs/PRE_REVIEW_CHECKS_R142.md) |
| PCBWay files and assembly tables | [Review package](hardware/mainboard/r142/pcbway/) |
| Board, layers and schematic PDFs | [Drawings](hardware/mainboard/r142/pcbway/03_drawings/) |
| Physical tests and closure criteria | [Qualification procedure](docs/FCT_PLAN_R142.md) |
| Automated current-source verification | [Workflow](.github/workflows/r142-independent-review.yml) |
| Development time | [Measured lower-bound ledger](docs/DEVELOPMENT_HOURS_READER.json) |

Exact PCB SHA256: `1ce355545d21d849e924f537488b5c9b9d59e9a8fa3cbbd129839823a7493ebf`. The r0.1 basename preserves hierarchy and is not the board revision.

R142 corrects reset behavior with TLV803EA30DBZR, adds GPIO39 card detection and external10k CMD/DAT0..3 pullups, retains100k NTC protection and adds3.3M TS bias, enforces five front-side Hirose no-pattern regions, and removes obsolete hidden documentation. Precision27.4k/4.99k feedback gives3.24549V nominal; the discarded3.38V candidate exceeded the panel's operative3.3V limit. Static PWM corner arithmetic passes; PFM, overshoot, lifetime drift and actual load behavior require qualification.

Native10.0.7 current-source DRC/ERC/opens/parity are zero. Four complete Gerber images are compared with native copper; all11 manufacturing layers, drill, IPC356, paste, mask, BOM and114 top-side placements are independently audited. Real copper-image open/short injections exercise the independent connectivity checker. Read the report for exact coverage and limitations; physical tests remain NOT RUN. [Final source run38576201886](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38576201886) passed. [Downloaded proof](docs/GITHUB_R142.json) verifies API digest/CRC and all24 manufacturing files after only declared timestamp normalization.

Good Display's10Oct reply confirms pin5 VDHR=VSH2, bend radius1-1.5mm and glass clearance>=2mm. [J3 document comparison](docs/FPC_CONNECTOR_REVIEW_R142.md) checks all24 contacts and actual signal copper/paste. Remaining holds: guaranteed FPC thickness/width and finger/coverlay acceptance, folded pin1/case pose, GDEM/GDEY CAD identity and enlarged J3 hold-down land/paste process; PFM/load-step voltage limits; actual ceramic Ceff, HV transient/current/thermal behavior; protected thin battery/PCM and NTC faults; firmware, PSRAM, SD/EPD/USB-MSC ownership; factory90-ohm stackup,84 nominal0.2mm bores, six resin-filled/copper-capped sites, stencil and short USB stake process. No factory upload, procurement or production release has been performed.

`hardware/mainboard/kicad/` is the immutable R138 control, and `hardware/mainboard/r141/` retains the previous accepted engineering source. Historical reports describe their recorded revisions. Open R142 for current work; do not regenerate historical goldens to accept changed hardware.

## Licensing

ENKU Base Reader uses **different licenses for different types of work**:

- **Original hardware design** — [CERN-OHL-W-2.0](LICENSE), including the KiCad PCB/schematic design and ENKU-authored hardware files.
- **Software and automation scripts** — [MIT](LICENSES/MIT.txt), including the Python validation tools and any future firmware expressly released in this repository.
- **Original project documentation** — [CC BY 4.0](LICENSES/CC-BY-4.0.txt), including README files and `docs/`.

Read the [license scope and third-party exceptions](LICENSE.md) before redistributing files or manufacturing modified boards. Third-party materials keep their own terms. The ENKU name and logos are not granted as trademarks by these licenses.

## Related project

[ENKU Originals](https://github.com/aliaksei-lameyka/ENKU-Originals) is a separate, early-stage experiment in AI-assisted, human-edited short fiction and reader-first EPUB delivery. It is currently private. **Its stories and editorial content are not licensed by this repository.**

