# ENKU Base R40 — verified USB-MSC microSD fanout / PCBWay readiness

**Planning readiness 30/100. PCBWay manufacturing release BLOCKED.**

Source: `hardware/mainboard/kicad/enku-mainboard-r1.7-base-sd-power-sclk-mosi.kicad_pcb` (125 KiCad footprints, 63 routed copper sections, 20 plated through vias, one inner In2.Cu local GND zone).

## Verified Native KiCad run, 2026-10-08

- [Native R40 run 37807935362](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807935362): **SUCCESS** including ERC strict 0 errors/0 warnings, PCB↔schematic parity 0, 0 critical copper shorts, clearance/edge, track- or via-dangling issues; refilled In2.Cu local GND zone.
- [Hardware schematic and physical guards 37807935436](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807935436): **SUCCESS**, native USB and microSD wiring source checked and physical SCLK/MOSI pilot clear.
- **236 non-unrouted DRC violations remain**: 124 `lib_footprint_mismatch`, 69 `silk_over_copper`, 27 `silk_overlap`, 16 `text_height`. **241 unconnected items**. `footprint_errors` 0.
- Previous R39 [Native run 37807447885](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807447885): 243 unconnected; R40 reduces to **241**, even though extra vias/tracks increase topology complexity. Electrical routing is still far from finished.

## Firmware and hardware scope

- Explicit USB-C MSC requirement: existing microSD shall appear as a host computer removable volume via ESP32-S3 native USB GPIO19 D-/GPIO20 D+, **without requiring Wi-Fi**. Firmware implementation has **not yet been delivered or tested**. Only hardware contract and first card copper have been done.
- R40 corrected R39's F.Cu power escape that otherwise blocked SPI pin fanout. SD VDD 3V3 on In1.Cu via; SD SCLK on B.Cu with two vias; SD MOSI on In1.Cu with two vias. **SD_CS and SD_MISO still unconnected**, as do ESP→card serial traces and USB D+/D−.
- The USB Type-C connector J5, protective U8 USBLC6, R62/R63 CC Rd 5.1k and R64/R65 0R USB series placeholders are in the PCB/schematic; proper controlled-impedance D+/D− routing and PCBWay stackup must be qualified.
- Mandatory VBUS-presence monitoring for battery/self-powered USB device is **not designed**, GPIO17 (U1 pad10) is reserved only. Avoid OFF-state backfeed and directly driving ESP32 GPIO from USB VBUS 5V. Espressif requires VBUS-valid monitoring and prompt disconnect; electronics still need design/bench signoff.
- Host MSC must own SD filesystem exclusively: before export close/flushing local FatFS, block Wi-Fi uploads/indexing, relinquish files, and on host eject/unplug safely remount and rebuild. USB storage only with SW1 ON under the present hardware architecture.
- Good Display GDEY0397T81P contact5 VDHR vs VSH2 and flex folding remains vendor-held, email already sent. No FPC changes.

## Blocking fabrication

241 unrouted connections, 236 DRC errors, 3D SD/USB solder and casing clearances, VBUS-valid stage, full USB FS pair stack-up and loss/ESD, source-approved SPI 4-pin SD MSC backend, correct CD pin behavior if required, LiPo charging/NTC and OFF state currents, PMOS thermal/inrush, DFM BOM/CPL/Gerbers. **No Gerber generation authorized.**