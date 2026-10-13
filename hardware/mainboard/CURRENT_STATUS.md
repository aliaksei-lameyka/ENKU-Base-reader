# ENKU Base mainboard - current entry

Physical **R138**, qualification/documentation **R139**, **NO FAB**. Open [canonical KiCad](kicad/enku-mainboard-r0.1.kicad_pro); read [current status](../../docs/CURRENT_STATUS.md) and [R139 handoff](../../docs/WORK_HANDOFF_R139.md).

Actual accepted native KiCad10.0.7 main/engineering artifacts establish DRC/ERC/opens/parity zero, 27 scopes and 20 effective rejection cases. Source-only R139 recovery review and a fresh zero-result DRC/ERC run also pass. PCB SHA256: `90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971`.

The [engineering-review packet](../../docs/qualification/R139/PCBWAY_PACKET_R138.json) contains 107 fitted top placements, Gerber/drill/IPC, process CSVs, editable source, four PDFs/30 checked pages and test templates. It grants no manufacturing permission and supplies no validated factory firmware.

BQ24072T + TPS63802, direct PH-2 and independent attached cell NTC; ESP32-S3-WROOM-1-N16R8, USB4215-03-A, microSD, BMI270 and physical buttons. PCB59x101x1.6mm; no case thickening. Base excludes frontlight/Hall/dock/wireless charging.

[Battery review](../../docs/BATTERY_STATUS_R139.md): no qualified thin interchangeable CN/PL pair. Startup, loads/Ceff, full charging/NTC faults, final case/panel/FPC, factory process and validated firmware/fixture/FCT remain HOLD. Physical tests NOT RUN.

The directory's old `README.md` is the frozen R136 snapshot used by regression preservation; this is the current overview. [Licenses](../../LICENSE.md): original hardware CERN-OHL-W-2.0, scripts MIT.
