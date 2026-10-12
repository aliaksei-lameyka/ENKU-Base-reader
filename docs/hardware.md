# Hardware overview

## Base R0.1

Base R0.1 is a four-layer mainboard for the compact ENKU reader.

### Compute and storage

- ESP32-S3-WROOM-1-N16R8
- microSD over SPI, with local book reading and USB Mass Storage (MSC) access planned
- USB-C USB 2.0 Full Speed on native ESP32-S3 GPIO19/20; VBUS sense mandatory before release
- No mandatory Wi-Fi/driver for USB file copy

### Display

The board carries a dedicated 24-pin e-paper interface and local high-voltage generation for the 3.97-inch panel class used by the first reader prototype. Exact panel identity, FPC orientation and bend path still require validation.

### Power

The current power architecture uses a BQ24072T USB charger/power path, TPS63802 3.3 V regulator, hard reader-load switch, direct two-pin JST PH battery connector and separate attached NTC. Current-limit and CE control are assigned to GPIO16/2/38; see [the R135 power contract](USB_POWER_CONTROL_R135.md).

### Input and sensing

- two reading buttons on each side edge
- BMI270 IMU
- service/debug interface

The four reading buttons are intentionally symmetric so firmware can support left-handed and right-handed layouts.

### Base scope

Frontlight, Hall/magnetic-cover sensing, wireless charging and Pogo/Dock are outside Base R0.1 and belong to a separate Pro design.

## Mechanical envelope

The current PCB is 59 × 101 × 1.6 mm in portrait orientation. Case thickness must not increase; a complete current enclosure CAD and compatible finished thin PCM pack are still required.

Mechanical release still requires final validation of the display flex path, USB-C opening, microSD insertion envelope, battery lead exit, hard-power actuator and side-button actuators against the enclosure master.

USB/SD R39 board requirements and MSC local/host ownership: see [USB Mass Storage specification](usb-mass-storage.md).
