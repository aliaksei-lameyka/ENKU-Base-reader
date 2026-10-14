# ENKU Base Reader

**Working PCB: R143. Branch: `engineering/r143-j3-startup-review`. NO FAB: EVT release remains blocked.**

3.97-inch GDEY0397T81P /SSD1677, ESP32-S3-WROOM-1-N16R8, BMI270 and shared SPI microSD.59x101x1.6mm, four copper layers. BQ24072T power path, TPS63802 supply, two-wire protected pack plus separate cell NTC. Base has no dock, frontlight, Hall or Qi; case thickness is unchanged.

R143 corrects J3 Hirose hold-down copper and separate paste apertures to OEM0.40x0.80mm. Four exact pad UUIDs change; electrical topology and every other pad/track/via/placement/outline/rule area are identical to R142. Both footprint library and PCB instance are corrected.

Native10.0.7 DRC0/ERC0/opens0/parity0 and complete independent Gerber/copper/IPC/drill/mask/paste/silk/BOM/CPL checks passed locally and in [actual source run38615866570](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38615866570). Exact source commit`c9dc9e624c260154094d23a93028e547f52420e8`. No goldens were regenerated; immutable R138 also passed27 scopes/20 rejection cases.

**The common logic/panel supply remains a design blocker.** Current MODE permits PFM while the cited+/-1% static accuracy is specified for PWM. Conditional static upper margin is only8.195mV and reset release margin10.727mV. A clean CAD/CAM result does not close this. Read the startup review before considering5-10 samples. Physical tests are NOT RUN.

| Need | Current R143 entry |
| --- | --- |
| Editable source | [KiCad](hardware/mainboard/r143/kicad/enku-mainboard-r0.1.kicad_pro), [manifest](hardware/mainboard/r143/source_manifest_R143.json) |
| Design blockers / primary data | [Startup review](docs/STARTUP_RISKS_R143.md) |
| Executed checks | [Pre-review](docs/PRE_REVIEW_CHECKS_R143.md), [server proof](docs/GITHUB_R143.json) |
| Good Display / Hirose | [FPC review](docs/FPC_CONNECTOR_REVIEW_R143.md) |
| Manufacturing and assembly inputs | [PCBWay review packet](hardware/mainboard/r143/pcbway/) |
| PDF board/layers/schematics | [Drawings](hardware/mainboard/r143/pcbway/03_drawings/) |
| First5-10 unit procedures | [FCT plan](docs/FCT_PLAN_R143.md) |
| Bounded development hours | [Ledger](docs/DEVELOPMENT_HOURS_READER.json) |

PCB SHA256:`3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266`. The r0.1 basename preserves hierarchy and is not the board revision. `hardware/mainboard/kicad/` is the immutable R138 control; R141/R142 retain their recorded source/evidence. Do not mix their manufacturing files with R143.

Felix's10Oct reply confirms pin5 VDHR=VSH2 and bend/clearance dimensions. Remaining pre-build work includes joint supply/reset margin, guaranteed FPC dimensions/folded pin1/CAD identity, protected pack/NTC, factory process/stackup/import acceptance and first-boot firmware. Generated files are design-review inputs; no PCBWay upload/order/purchase or successful physical prototype test is claimed.

## Licensing

ENKU Base Reader uses **different licenses for different types of work**:

- **Original hardware design** — [CERN-OHL-W-2.0](LICENSE), including the KiCad PCB/schematic design and ENKU-authored hardware files.
- **Software and automation scripts** — [MIT](LICENSES/MIT.txt), including the Python validation tools and any future firmware expressly released in this repository.
- **Original project documentation** — [CC BY 4.0](LICENSES/CC-BY-4.0.txt), including README files and `docs/`.

Read the [license scope and third-party exceptions](LICENSE.md) before redistributing files or manufacturing modified boards. Third-party materials keep their own terms. The ENKU name and logos are not granted as trademarks by these licenses.

## Related project

[ENKU Originals](https://github.com/aliaksei-lameyka/ENKU-Originals) is a separate, early-stage experiment in AI-assisted, human-edited short fiction and reader-first EPUB delivery. It is currently private. **Its stories and editorial content are not licensed by this repository.**

