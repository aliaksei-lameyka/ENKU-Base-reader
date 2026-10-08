# ENKU Base R40 — microSD SPI fanout, USB MSC-compatible layout

**Real KiCad revision:** `hardware/mainboard/kicad/enku-mainboard-r1.7-base-sd-power-sclk-mosi.kicad_pcb`.

R39 verified [native KiCad run](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807447885): ERC0, parity0, DRC 236 non-unrouted, 243 unconnected. The initial 3V3_SYS F.Cu vertical trace at x36.3 from J2 pad4 to C16 pad1 ran beside the fine-pitch card and **obstructed the SPI fanout corridor**.

R40 corrects that before committing the full SPI layout:
- J2 pad4 `3V3_SYS` to via (36.0,100.175), routed via **In1.Cu** over to a second via (37.8,96.95) and C16 pad1 at (39,96.95). This frees F.Cu between J2 pins and the 3V3 capacitor, avoiding F.Cu fanout conflicts.
- J2 pad5 `SD_SCLK_CARD` to via (36,99.075), **B.Cu** along x37.5, via (40.5,107) to R21 pad2 (38.825,107).
- J2 pad3 `SD_MOSI_CARD` to via (36,101.275), **In1.Cu** over to via (40.5,104), then R20 pad2 (38.825,104) on F.Cu.
- Keep J2 pad2 `SD_CS_CARD` and pad7 `SD_MISO_CARD` unrouted until a non-crossing escape and metal-shell/mechanical clearance are checked. Card supply is still on switched 3V3_SYS, thus only powered with Reader ON.
- R39 C16 GND to via (40.8,95.05) and In2.Cu local ground fill retained.

**R40 has 125 footprints, 63 trace segments, 20 vias and one GND zone**, with KiCad-native fill/DRC required. No complete USB data pair yet: J5 A/B6/7, U8 ESD, R64/R65 0Ω tuning pads and ESP GPIO19/20 are still netlisted but un-routed. Reserve matched controlled-impedance corridor and future self-powered USB `VBUS_MONITOR` GPIO17 input. Do not put 5V directly to MCU. USB Mass Storage uses the **same SPI microSD card**, with exclusive storage ownership managed in firmware, not a separate SD controller.

**Good Display pending supplier reply for stepped FPC pin5 VDHR/VSH2**; no EPD trace changes in R40. Next: finish CS/MISO microSD escapes, repair possible DRC geometry issues and wire complete 3V3, MCU USB differential pair and VBUS sense after vendor stackup. Production must remain blocked until routing, ERC and full DRC=0, NTC/power-off, USB host MSC and mechanical tests.

Official TinyUSB stack info: https://docs.espressif.com/projects/esp-usb/en/latest/esp32s3/usb_device.html


## Native verification complete (2026-10-08)

[Run 37807935362](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807935362) successfully filled the editable In2.Cu GND polygon, ran KiCad strict ERC **0**, PCB↔schematic parity **0**, no native shorts/dangling tracks/vias or edge faults, and kept **236 other DRC violations and 241 unconnected items**. [Structural tests 37807935436](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807935436) also passed. This qualifies the *first two microSD signal escapes*, not completed USB MSC. USB D+/D− 90-ohm pair and 5V VBUS sense remain release blockers. Good Display clarification pending.
