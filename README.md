# ENKU Base Reader

ENKU Base is a compact, repairable3.97-inch e-paper reader with physical controls, microSD and an ESP32-S3. It works locally without a required cloud service or subscription.

**Current engineering revision: R136**, retained on `engineering/r136-capacitance-release` and consolidated into `main` after verification. The R135/main merge`1a29692` preserves the full engineering and independent licensing histories. **Manufacturing status: NO FAB.** Open [the canonical KiCad project](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro).

Local native KiCad10.0.7 passes **DRC0, ERC0, opens0, schematic parity0**,23 independent scopes plus checkpoint comparison and8 regression-rejection cases. [Actual R136 GitHub run38259293325](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38259293325) passed all9 job steps. Actual24-report/44-member binary artifact,5 native plots and all8 rejection cases match local results; SHA/API digest/CRC verified. [Exact proof](docs/GITHUB_NATIVE_R136.md). [Current handoff](docs/WORK_HANDOFF_R136.md). [Accepted R135 actual server proof](docs/GITHUB_NATIVE_R135.md) remains retained.

## Hardware and R136 progress

ESP32-S3-WROOM-1-N16R8,3.97-inch800×480 e-paper interface, USB-C GCT USB4215-03-A, ESD, microSD, BMI270, four E-Switch TL1016AAF160QG side buttons and hard reader-load switch. Power uses BQ24072T, TPS63802, direct JST PH-2 and a separate attached cell NTC. Base has its own59×101×1.6mm PCB. Case thickness must not increase. Frontlight, Hall/magnetic-cover, wireless charging and Pogo/Dock belong to a separate Pro design.

C9 now uses22uF10V Yageo CC0805MKX5R6BB226. The revised typical-curve scenario gives34.64% input-capacitance margin instead of3.28% for the previous10uF part. Four fields change in PCB/schematic; all positions, pads, copper, mask/paste, nets, USB/RF and thermal requests remain identical. New C9 max height1.45mm requires local clearance review. [Exact calculation and limitations](docs/CAPACITANCE_R136.md).

R135's four no-boss switches and R80/R81=40.2k/33.2k remain. Nominal healthy charge window is4.90–35.01°C. Guaranteed capacitance/sensor/leakage, detached-sensor and R82 fault behavior, complete case/PH2/battery/button/USB/panel fit and factory assembly/stackup remain unresolved. [Latest supplier status](docs/SUPPLIER_STATUS_R136.md): confirmed5.2mm finished AKY0156 is rejected; two thin2000–2500mAh protected CN/Poland replacements are still required.

## Firmware and first boards

GPIO16/2/38 control EN1/EN2/CE; reset/OFF high-Z models USB100. FastOFF500mA and automatic BC1.2/PD are not implemented. [Power contract](docs/USB_POWER_CONTROL_R135.md). USB MSC requires exclusive host/reader ownership of microSD and safe return; it is not implemented or tested in this hardware tree. [MSC specification](docs/usb-mass-storage.md). [R136 first-board checks](docs/BRINGUP_R136.md); physical qualification is NOT RUN.

## Source and verification

`hardware/mainboard/kicad/` contains editable source/local libraries, `checks/` contains exact checkpoints/guards/proof, and `docs/` contains decisions/handoffs. The current native workflow covers main, the engineering branch and relevant PRs, verifies immutable source and rejects baseline regeneration. Historical output directories are not a current manufacturing package. All earlier engineering commits/evidence and main licensing are preserved.

No production, purchases or supplier messages occurred in R136. A native pass does not authorize manufacture. Complete design/factory review and present the concrete EVT package for user agreement before ordering; successful physical qualification precedes production.

## Licensing

ENKU Base Reader uses **different licenses for different types of work**:

- **Original hardware design** — [CERN-OHL-W-2.0](LICENSE), including the KiCad PCB/schematic design and ENKU-authored hardware files.
- **Software and automation scripts** — [MIT](LICENSES/MIT.txt), including the Python validation tools and any future firmware expressly released in this repository.
- **Original project documentation** — [CC BY 4.0](LICENSES/CC-BY-4.0.txt), including README files and `docs/`.

Read the [license scope and third-party exceptions](LICENSE.md) before redistributing files or manufacturing modified boards. Third-party materials keep their own terms. The ENKU name and logos are not granted as trademarks by these licenses.

## Related project

[ENKU Originals](https://github.com/aliaksei-lameyka/ENKU-Originals) is a separate, early-stage experiment in AI-assisted, human-edited short fiction and reader-first EPUB delivery. It is currently private. **Its stories and editorial content are not licensed by this repository.**
