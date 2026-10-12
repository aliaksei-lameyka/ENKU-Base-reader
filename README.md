> R135 working branch `engineering/r135-switch-ntc-review`: actual native DRC0/ERC0/opens0/parity0 after real no-boss side-switch replacement and TS-bias correction. Independent audits/server proof pending; NO FAB. [Current handoff](docs/WORK_HANDOFF_R135.md). The R134 proof below remains historical.

# ENKU Base Reader

ENKU Base is a compact, repairable 3.97-inch e-paper reader with physical controls, microSD storage and an ESP32-S3. It is designed to work locally without subscriptions or a required cloud service.

**Current engineering revision: R134, branch `engineering/r134-usb-control-connector`. Manufacturing status: NO FAB.** Canonical source is [the KiCad project](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro). Native KiCad10.0.7 reports ERC0,unconnected0,schematic parity0 and16 active button-hole clearance errors. All 21 independent scopes passed the fresh immutable-source [GitHub run38240134929](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38240134929). Actual ZIP digest/CRC and all 22 report/export comparisons are verified and retained; use [the R134 handoff](docs/WORK_HANDOFF_R134.md) for its exact status. Passing engineering checks does not authorize fabrication.

The board remains59×101×1.6 mm and the case thickness target is unchanged. R134 replaces J5 with GCT USB4215-03-A, adds GPIO control of charger EN1/EN2/CE, closes control routing and preserves the long USB pair and its native refilled reference. The continuous charger GND-spreading geometry exceeds50 mm²; actual temperatures and assembly process remain unqualified.

## Hardware

- ESP32-S3-WROOM-1-N16R8 and3.97-inch800×480 e-paper interface
- USB-C with ESD and native ESP32 USB data path
- microSD storage, four side navigation buttons and BMI270 IMU
- hard reader-load power switch
- BQ24072T charger and TPS63802 system regulator
- direct two-wire JST PH-2 battery interface with a separate attached cell NTC

Base has its own board. Frontlight, Hall/magnetic-cover, wireless charging and Pogo/Dock features are outside this Base hardware scope; Pro is a separate design.

## Remaining release work

The16 SW3–SW6 locator-to-copper errors need a documented component/factory-process decision or a validated switch replacement. Other mandatory gates include fixed-thickness battery/PH2/enclosure fit, two interchangeable thin protected packs with CN/PL procurement, NTC single faults and attachment, effective capacitance, full charge/thermal tests, USB/current-mode firmware and bench behavior, impedance and exact panel/FPC/assembly acceptance. See [the concrete R134 fabrication gates](docs/DFM_REVIEW_R134.md).

The battery target remains2000–2500 mAh, thin two-wire1S4.20 V PCM pack. Neither a catalogue cell nor an email reply is an approved finished-pack SKU. [Current battery/supplier status](docs/BATTERY_STATUS_R134.md) supersedes earlier no-reply observations. No case-thickness increase, manufacturing order or component purchase was made.

## USB and firmware

The hardware supports USB access through ESP32-S3 GPIO19/20. USB Mass Storage firmware must grant the computer exclusive microSD ownership and restore reader access after safe disconnect; it is not implemented or bench-tested in this hardware tree. See [USB MSC specification](docs/usb-mass-storage.md).

Charger control now supports USB100,USB500,external ILIM and suspend. Reset/OFF high-impedance behavior is modeled USB100; fast OFF500 mA and automatic BC1.2/PD detection are not implemented. Boot/brownout, load voltage margins and source-authorized input-current policy require qualification. [R134 signal and power contract](docs/USB_POWER_CONTROL_R134.md).

## Source and evidence

| Location | Content |
|---|---|
| `hardware/mainboard/kicad/` | Editable canonical source and project-local libraries |
| `hardware/mainboard/kicad/checks/` | Native checkpoints, independent guards, exact source preservation and retained evidence |
| `docs/` | Current engineering decisions, handoffs and release gates |
| `.github/workflows/` | Pinned native source verification and isolated artifact-proof workflow |
| `hardware/mainboard/production/` | Historical/release output area; not a current fabrication release |

Earlier sources, handoffs and native proofs remain retained, including [accepted R133 evidence](docs/GITHUB_NATIVE_R133.md). Historical R40–R50 percentages and older schematic/PCB filenames are not current readiness evidence. Firmware/enclosure trees are not registered as complete current release sources in this repository.

## Manufacturing and license

Final Gerber/drill/BOM/CPL/assembly outputs require a frozen accepted source, all mandatory release gates and explicit user approval before manufacturing or purchasing. Current revision is an engineering candidate. License status must be checked for the eventual public release.
