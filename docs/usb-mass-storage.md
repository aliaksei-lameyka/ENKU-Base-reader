# ENKU Base — USB-C microSD mass storage (R127 active hardware contract)

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

## Active R127 hardware and open qualification

Canonical source: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Base uses BQ25185 charger/power path, TPS63802 regulator and the SW1/Q2 system gate. There is no TPS2121, Dock or Pogo on this dedicated Base.

U10 is **TLV3012BIDBVR**, sharing switched 3V3_SYS with ESP32, USB_VBUS_VALID to GPIO17/U1 pad10. Exact B suffix is mandatory for fail-safe inputs. R70 **RT0603BRD0726K7L** 26.7k and R71 **RT0603BRD0710KL** 10k have 0.1% tolerance and 25ppm/K TCR. R72 is the 100k output pull-down; R73 is the 3.3k raw VBUS bleeder; C38 is 100nF bypass; C39 **CC0603JRNPO9BN102** is 1nF C0G/50V. Raw VBUS never directly connects to GPIO17.

R127 checks native pin maps and every capacitor net node. Direct C2/C4/C5/C6 now total **6.8uF nominal** after C4 **10uF/10V to 1uF/25V X7R**; R126 was 15.8uF. The tolerance/temperature scenario plus a 0.25uF allowance totals 8.852uF. It does not guarantee voltage-dependent capacitance or whole-device inrush. BQ25185 requires more than 1uF effective IN/SYS/BAT capacitance after derating; qualification remains open.

The numeric threshold scenario over -40..85°C is **4.37697..4.73696V**, including an explicit 100nA board-leakage allowance. Conditional **passive** VBUS decay from 5.5V to the lower threshold is about **6.215ms**, assuming the stated capacitance and no retained external source/backfeed. C39 nominal tau is 7.275us. The historical R41/R46 **1.085ms with no more than 1.5uF** estimate is invalid for the current PCB. No disconnect latency guarantee follows: near-threshold comparator, firmware and POR timing require measurement. TI's 4us propagation value is at 100mV overdrive.

The USB pair is fully routed, native opens are zero, and actual refilled In2.Cu GND reference is checked. The B.Cu coupled core has 0.2mm width/gap and two vias per net. Layer-aware track-only USB-C contact skews are A -2.70260 / B +1.21451mm; these exclude pad spreading and package/via delay. Factory 90Ω stackup, branch behavior, ESD/long-cable hotplug and assembly orientation still need review.

USB MSC requires the physical switch ON. OFF allows charging, while ESP32 does not enumerate. Whole-device USB suspend/current/charger policy remains open. Fixed 500mA BQ25185 ILIM does not authorize 500mA before enumeration. Firmware descriptors must reflect actual power configuration, negotiated/advertised current and exclusive SD filesystem ownership. Hardware guards do not prove firmware or bench behavior.

See [R127 calculations and sources](COMPONENT_POWER_PASS_R127.md), [remaining gates](REMAINING_TO_BUILD_R127.md) and [actual native server proof](GITHUB_NATIVE_R127.md). Previous R41 source/check scripts are historical snapshots.

Production criteria: native DRC and assembly gates closed; VID/PID/descriptors reviewed; bench OFF/backfeed, thermal, hotplug, inrush and suspend checks; Windows/macOS/Linux mount/copy/eject/reconnect; SD removal/brownout and local/Wi-Fi/MSC mutual exclusion. No automatic formatting or destructive filesystem repair.
