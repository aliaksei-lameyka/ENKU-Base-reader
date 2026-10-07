# Hardware overview

## Base R0.1

Base R0.1 is a four-layer mainboard for the compact ENKU reader.

### Compute and storage

- ESP32-S3-WROOM-1-N16R8
- microSD
- USB-C USB 2.0 connection

### Display

The board carries a dedicated 24-pin e-paper interface and local high-voltage generation for the 3.97-inch panel class used by the first reader prototype.

### Power

The power architecture includes USB/dock source handling, Li-ion charging, a hard power control path and a 3.3 V system rail.

### Input and sensing

- two reading buttons on each side edge
- BMI270 IMU
- Hall sensor
- service/debug interface
- dock detect

The four reading buttons are intentionally symmetric so firmware can support left-handed and right-handed layouts.

### Base scope

Frontlight and wireless charging are not part of Base R0.1. Keeping those features out of the first-spin board reduces routing and validation complexity and lets the Base hardware reach bring-up sooner.

## Mechanical envelope

The current PCB outline is 54 × 94 mm in portrait orientation.

Mechanical release still requires final validation of the display flex path, USB-C opening, microSD insertion envelope, battery lead exit, dock contact face, hard-power actuator and side-button actuators against the enclosure master.
