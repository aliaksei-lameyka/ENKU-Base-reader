# ENKU Base — USB-C microSD mass storage (R41 hardware contract)

**Requirement:** A user with a USB-C data cable and powered-on ENKU Reader can open the same removable microSD volume on Windows/macOS/Linux as a standard USB Mass Storage device. Wi-Fi remains a *separate* optional uploader, not a requirement for USB file copy. No driver, app account, subscription or backend.

## Architecture decision
Use the **existing ESP32-S3 USB-OTG peripheral with TinyUSB MSC and the existing microSD SPI interface**. No secondary USB SD-card bridge IC, no USB hub and no switch multiplexing SPI pins are needed. USB-C <-> ESP32-S3 USB D-/D+ on module pins 13/14 (GPIO19/GPIO20). MCU SPI storage pins18–21 <-> R19–R22 <-> microSD J2 contacts2/3/5/7. Existing R62/R63 5.1k Type-C Rd pull-downs, U8 USBLC6 ESD protector and R64/R65 0R (22R population tune pending) stay in circuit.

Official docs:
- https://docs.espressif.com/projects/esp-usb/en/latest/esp32s3/usb_device.html
- https://github.com/espressif/esp-idf/blob/master/examples/peripherals/usb/device/tusb_msc/README.md
- https://components.espressif.com/components/espressif/esp_tinyusb
- Note IDF examples often use SDMMC 1/4-bit; **our SPI-wired microSD card must use an SPI-compatible block backend** (SDSPI card object or customized MSC sector read/write). Build an actual ESP32-S3 MSC+SDSPI spike before claiming firmware parity. Never silently assume 4-bit SDMMC support on J2: there are only four storage signals!

## State machine required in firmware

```
LOCAL_READER (local FatFS owner; Wi-Fi uploads permitted under same lock)
  USB cable attached + 3V3 on + card present -> USB_REQUESTED
USB_REQUESTED:
  stop uploader and indexer; complete/abort pending writes; flush and close all files;
  save reading checkpoint outside SD if necessary; unmount local FatFS; hand raw sectors to MSC
USB_EXPORTED:
  PC sole filesystem owner; show "USB storage — safely eject before disconnecting";
  no EPUB load, catalog scan, cover cache writes or Wi-Fi storage write (deny reads too)
  USB disconnect / host START STOP UNIT/eject -> USB_RECLAIMING
USB_RECLAIMING:
  detach MSC LUN; wait for block I/O idle; remount/revalidate FAT; media-generation increment;
  reconcile library and bookmarks; re-enable uploader; local reader resumes
```

If card missing: return 'not ready' to USB LUN and keep running reader without crashing. If hot-removed while exported: abort/mark not-ready, never auto-format. If USB cable removed during write: remount read-only or prompt for filesystem repair, do NOT run automatic destructive fix. Test both read and write, card eject, fast reconnect, host suspend, corrupted FAT, card hot-swap. A host may cache writes so instruct safe eject.

## Hardware gating and unresolved compliance

**R41 VBUS monitor:** U10 **TLV3012BIDBVR**, powered by the same switched 3V3_SYS as ESP32, drives USB_VBUS_VALID on **GPIO17 / U1 pad10**. B-suffix fail-safe inputs are mandatory: do not substitute TLV3012 without B. R70 26.7k and R71 10k (both 0.1%, 25ppm/K) divide raw VBUS into IN+; internal 1.242V reference connects REF to IN−; R72 100k pulls output down; C38 100nF bypasses VDD; C39 1nF C0G filters sense. R73 3.3k discharges raw VBUS, and C2 changes from 10uF to 1uF/10V. Comparator output never intentionally exceeds the shared MCU supply.

`check_r41_vbus.py` conservatively combines reference range/drift, offset, hysteresis and resistor tolerances over −40..85°C: transition envelope **4.380..4.734V**. Conditional unplug RC estimate **1.085ms** assumes total raw-VBUS capacitance ≤1.5uF and no retained external/backfed source. This is a design calculation, **not a measured USB disconnect guarantee**; comparator delay close to threshold, actual capacitor tolerances, TPS2121 reverse behavior with the dock present and firmware detachment latency require oscilloscope tests. Raw 5V is never wired directly to GPIO17.

R73 consumes up to 1.684mA at 5.5V before other VBUS loads. Whole-device USB suspend current and charger-disable policy remain a release gate. Reducing C2 helps disconnect timing but increases hotplug-ringing sensitivity; measure connector/mux voltage with long cables and retain required downstream bypass/bulk. OFF leakage/backfeed and brownout/POR output state must be verified on assembled hardware.

Original design sources:
- TI TLV3012B / SBOS300C: https://www.ti.com/lit/gpn/TLV3012B
- TI TPS2121: https://www.ti.com/lit/ds/symlink/tps2121.pdf
- ST USBLC6-2 / DS4260: https://www.st.com/resource/en/datasheet/usblc6-2.pdf

Firmware must configure self-powered TinyUSB and its VBUS monitor on GPIO17, alongside the exclusive SPI block backend below. No firmware claim follows from the hardware checks.

USB MSC works with **physical switch ON** (3V3_SYS active). With switch OFF the ESP32 will not enumerate even though battery charging can continue over USB. If USB storage required with switch OFF, this changes power architecture and must be explicitly redesigned.

Physical USB design signoff required: Type-C receptacle orientation (A6/B6 data+, A7/B7 data−), both CC resistors, ESD near receptacle and VBUS power mux, D+/D− length matching and **90 ohm nominal differential impedance** using PCBWay actual 4-layer stack-up, no plane breaks/high-current routes under the pair, ESD pad + 0R/22R placement and 3D cable mating. USB-C is USB 2.0 **Full Speed** on ESP32-S3 OTG, not USB 3 or high-speed 480 Mbit/s. Data pair stays unrouted until stackup & corridor DFM review.

## Active R41 PCB

Source `hardware/mainboard/kicad/enku-mainboard-r1.8-base-sd-card-completion.kicad_pcb`: all four microSD SPI routes now connect MCU pads18–21 through R19–R22 to J2; R23 CS pull-up and C16/C17 supply branches and all J2 GND/shell returns are connected. CC1/CC2 pull-downs, both USB-C VBUS contact pairs, C2, U2 USB power-mux input, U8 VBUS and the comparator circuit have copper. Both inner layers carry GND zones with signal/power clearances and stitching; these are **not an approved uninterrupted reference plane or manufacturing stackup**.

U8's earlier embedded generic SOT23-6 geometry was incorrect. Its new project-local footprint `USBLC6_2SC6_ST_SOT23_6L` follows ST's top-view numbering and figure19 recommended lands: 0.95mm pitch, 2.30mm opposing pad-center separation, 1.20x0.60mm lands. Pin2 GND and pin5 VBUS are in opposite middle rows; active-board physical assertions protect this orientation. D+/D− remain unrouted pending stackup/corridor signoff. Keep J3 candidate pin5 EPD_VSH2 unchanged until Good Display answers.

See `hardware/mainboard/manufacturing/PCBWAY_READINESS_R41.md` for the final Native KiCad evidence and exact debt. SPI continuity does not demonstrate signal integrity, card power stability, card detection behavior or end-to-end USB MSC operation.

Production criteria: full DRC0 (not just critical types0), no USB data pair shorts or CC swaps, driver descriptors VID/PID licensing, ESD and brownout while writing, at least Windows/macOS/Linux desktop mount/copy/eject/reconnect test and local/Wi-Fi/MSC mutual exclusion.
