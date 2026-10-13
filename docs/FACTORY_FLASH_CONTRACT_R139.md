# ENKU factory programming and test contract - draft, NOT EXECUTABLE

Physical PCB R138 / audit R139. No diagnostic or release binary validated on this hardware is supplied. Do not manufacture, flash arbitrary firmware, burn eFuses or mark a unit PASS from this draft. A complete approved image set/offset map/fixture/limits must replace the pending records first.

## Target and service interface

U1: ESP32-S3-WROOM-1-N16R8, target 16MB Quad SPI flash and 8MB Octal PSRAM. Confirm actual chip revision, flash ID/size, PSRAM init and allocated-memory patterns on every accepted unit. Freeze ESP-IDF/esptool versions, sdkconfig, flash frequency/mode, partitions and image hashes with the released firmware; this contract does not invent offsets or assume another board's image is compatible.

J7 target-side contacts (PCB pad numbers, top/front view):

| Pin | Signal | Fixture use |
| --- | --- | --- |
| 1 | 3V3_SYS | Target VREF measurement; never automatically supply power here |
| 2 | GND | Common ground |
| 3 | UART_TX, GPIO43 | Fixture UART RX |
| 4 | UART_RX, GPIO44 | Fixture UART TX, 3.3V logic |
| 5 | BOOT, GPIO0 | Controlled pull-down, otherwise release |
| 6 | ESP_EN | Controlled pull-down, otherwise release |

The cable footprint family is not a standardized ENKU signal assignment. Continuity-check the actual adapter once against these numbered pads. Use VREF-aware buffers/pull-downs; disconnect fixture drive when the target is off to avoid back-powering. Power the board through an agreed VBUS/battery-simulator input. Do not connect 5V UART, force EN high against the target circuit or treat J7 pin 1 as a generic programmer supply.

## Recovery procedure for EVT validation

Connect ground and verify stable target supply. Pull BOOT low before reset. Pull ESP_EN low long enough to discharge the actual 1uF RC and to meet the manufacturer's minimum 50us reset timing at the pin; release EN after stable rails, keeping BOOT low through the minimum 3ms strap hold. Verify levels with a scope during fixture validation. Read ROM identity/log, then use the pinned esptool version to load the approved image set at its approved offsets and verify flash contents. Release BOOT and reset; require the expected diagnostic version and boot reason. This sequence is presently source-supported and physically NOT RUN.

Test native USB flashing through both plug orientations and UART fallback through J7. On controlled EVT samples, a recoverable invalid application or USB-pin misconfiguration must be recoverable through BOOT/EN/UART without soldering or component replacement. Do not burn irreversible security eFuses or erase calibration/device identity as part of an exploratory test. Read existing security settings and adapt the approved flashing procedure if they restrict access.

USB Serial/JTAG is fixed-function CDC/JTAG, not USB Mass Storage. Final reader firmware must use the supported OTG stack for MSC, own the SD card exclusively while the host writes, flush/unmount safely and remount for the reader after host release. Test interrupted transfers and USB sleep/reconnection behavior in the final firmware; a successful ROM flash does not prove MSC.

## Approved release inputs required

- Exact hardware/BOM/case/panel/pack revision and diagnostic/release firmware source commits.
- Reproducible build configuration, pinned tools, complete image files, offsets, sizes and SHA256; blank/invalid-image recovery instructions.
- Fixture drawing, ENKU J7 wiring, VREF/back-power behavior, calibrated supply/load/NTC/SD/panel stimulus and software versions.
- Numeric limits for rails/ripple, OFF/sleep/active/inrush current, charging/NTC, RF and test duration. Derived characterization targets must become approved limits before factory FCT.
- Per-unit log with board serial/MAC, manufacturing/component lots, firmware hash, fixture/calibration identity, results and raw evidence. Rejected units may not be relabelled by an unrecorded repair.
- After diagnostics, program approved user firmware, verify content and boot it; save a PASS/FAIL record. Ship only the accepted production design without required bodges.
