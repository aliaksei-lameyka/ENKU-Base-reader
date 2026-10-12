# ENKU Base R39 — USB MSC and microSD hardware audit

**PCBWay Ready: 30/100 provisional; FABRICATION BLOCKED.**

Architecture contract: **USB-C Mass Storage of existing microSD**, using ESP32-S3 GPIO19/20 native USB device and the microSD four-wire SPI card on MCU GPIO. Wi-Fi uploader remains. Firmware exclusive storage ownership required. Hardware source `enku-mainboard-r1.6-base-usb-msc-sd-power.kicad_pcb`: 125 footprints, 52 copper segments, 14 vias, existing In2.Cu local GND polygon. First SD power and decoupling return trace added. Vendor Good Display pin5 FPC hold unchanged.

**New mandatory blocker**: VBUS monitor for battery-powered self-powered USB device not yet designed; spare GPIO17 U1 pad10 reserved. Do NOT tie 5V directly to ESP32 or create off-state backfeed via resistor-divider. Confirm VBUS valid thresholds and unplug response on production circuit. USB data pair is electrically assigned to GPIO19/20 but not routed or 90-ohm verified. SD J2 data signals not yet routed. MSC firmware not implemented in this hardware-only repo. Current structural test guards pinout but does not provide USB operation.

R38 baseline [Native KiCad zone fill 37805934639](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37805934639): ERC0, parity0, 236 non-unrouted DRC, 245 unrouted. R39 Native verification pending. No PCBWay Gerbers.
