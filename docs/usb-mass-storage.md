# ENKU Base — USB-C microSD mass storage (R39 hardware contract)

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

**Critical discovery**: ENKU Base uses a battery, so even with USB unplugged the ESP32 remains powered. USB spec and Espressif require a **VBUS present / valid GPIO monitor** for a self-powered device (USB valid above ~4.75V, invalid below ~4.35V and prompt disconnection). Current R38/R39 does NOT yet route VBUS_USB to a dedicated sense GPIO; **GPIO17 U1 module pad10 is free and reserved**. A raw 5V GPIO wire is forbidden. A simple divider can backfeed unpowered 3V3_SYS in hard-OFF; ensure threshold accuracy, response <3ms and off-state leakage/no phantom power using a qualified comparator/level detector with a safe power domain. Do not install an arbitrary high-voltage divider or digital buffer without verifying the disconnect thresholds; this is a **PCBWay release blocker**.

USB MSC works with **physical switch ON** (3V3_SYS active). With switch OFF the ESP32 will not enumerate even though battery charging can continue over USB. If USB storage required with switch OFF, this changes power architecture and must be explicitly redesigned.

Physical USB design signoff required: Type-C receptacle orientation (A6/B6 data+, A7/B7 data−), both CC resistors, ESD near receptacle and VBUS power mux, D+/D− length matching and **90 ohm nominal differential impedance** using PCBWay actual 4-layer stack-up, no plane breaks/high-current routes under the pair, ESD pad + 0R/22R placement and 3D cable mating. USB-C is USB 2.0 **Full Speed** on ESP32-S3 OTG, not USB 3 or high-speed 480 Mbit/s. Data pair stays unrouted until stackup & corridor DFM review.

## KiCad first physical R39 step
Source `hardware/mainboard/kicad/enku-mainboard-r1.6-base-usb-msc-sd-power.kicad_pcb`: J2 card pad4 3V3_SYS connected to C16 bulk input and C16 GND to local In2.Cu GND return via. **Four additional F.Cu copper segments and one Ø0.7mm plated via**; totals 52 segments/14 vias/one inner ground zone/125 components. **No SPI card signals routed yet**; do not mistake valid netlist for a complete functional USB transfer. Preserve Good Display pending FPC pin5 vendor question; no touch to display copper.

Production criteria: full DRC0 (not just critical types0), no USB data pair shorts or CC swaps, driver descriptors VID/PID licensing, ESD and brownout while writing, at least Windows/macOS/Linux desktop mount/copy/eject/reconnect test and local/Wi-Fi/MSC mutual exclusion.
