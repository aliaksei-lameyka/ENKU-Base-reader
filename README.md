# ENKU Base Reader

ENKU Base is a compact, repairable 3.97-inch e-paper reader with physical controls, microSD and an ESP32-S3. It works locally without subscriptions or a required cloud service.

**Current engineering revision: R135**, branch `engineering/r135-switch-ntc-review`. **Manufacturing status: NO FAB.** Open [the canonical KiCad project](hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro).

[Actual immutable-source KiCad10.0.7 run38252194674](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38252194674) passed: **DRC0, ERC0, opens0, schematic parity0**, all22 independent scopes plus checkpoint comparison. Actual23-report artifact, five native plots, reference/thermal fills, via requests, assembly/CPL/BOM and netlist match the retained local baseline; binary SHA256/API digest/CRC are verified. [Exact proof](docs/GITHUB_NATIVE_R135.md).

## Hardware

- ESP32-S3-WROOM-1-N16R8; 3.97-inch800×480 e-paper interface
- USB-C GCT USB4215-03-A, ESD, microSD and BMI270
- Four E-Switch TL1016AAF160QG side buttons, hard reader-load switch
- BQ24072T charger, TPS63802 regulator, direct JST PH-2 battery interface and separate attached cell NTC

Board remains59×101×1.6mm; case thickness must not increase. Base has its own PCB. Frontlight, Hall/magnetic-cover, wireless charging and Pogo/Dock belong to a separate Pro design.

## R135 changes and remaining work

Actual AA no-boss switches remove the old16 hole-clearance violations through a real component change. All four numbered contacts are externally routed. Native mask/paste and preserved USB/power/RF/outline geometry are checked. New button height/rectangular actuator require a reviewed internal case pusher; a mechanical drop-in is not claimed.

R80/R81 now40.2k/33.2k1%. The identified R81-open hot-fault inhibits in stated resistor/R/T/leakage scenarios. **Healthy nominal charge window is now4.90–35.01°C**, more conservative than R134. Sensor detachment, guaranteed R/T/TS leakage and bench qualification remain unresolved. [Switch/TS design decision](docs/SWITCH_NTC_R135.md).

Remaining gates are complete fixed-thickness enclosure/PH2/battery fit and two thin protected CN/PL replacements, effective capacitance and sensor/fault review, USB stackup and assembly process, plus firmware and physical qualification after approved EVT. [Concrete current fabrication gates](docs/DFM_REVIEW_R135.md). Zero DRC does not authorize manufacturing or purchases.

## Firmware and first boards

USB MSC must provide exclusive computer ownership of microSD and safe return to reader access; it is not implemented/tested in this hardware tree. [MSC specification](docs/usb-mass-storage.md). GPIO16/2/38 control EN1/EN2/CE; reset/OFF high-Z models USB100. FastOFF500mA and automatic BC1.2/PD are not implemented. [Current power contract](docs/USB_POWER_CONTROL_R135.md) and [first-board validation](docs/BRINGUP_R135.md).

## Source and evidence

`hardware/mainboard/kicad/` contains editable source/local libraries; `checks/` contains guards, native checkpoints and actual proof; `docs/` contains decisions/handoffs; `.github/workflows/` contains pinned source/evidence verification. Historical production/output directories are not a current release package.

1038 parent files and all earlier engineering evidence remain unchanged, including [accepted R134 proof](docs/GITHUB_NATIVE_R134.md). [Current handoff](docs/WORK_HANDOFF_R135.md). Battery remains2000–2500mAh, thin two-wire1S4.20V PCM pack with separate NTC; [supplier status](docs/BATTERY_STATUS_R134.md). No current finished pack/case is approved. No production, parts order or supplier message occurred in R135.
