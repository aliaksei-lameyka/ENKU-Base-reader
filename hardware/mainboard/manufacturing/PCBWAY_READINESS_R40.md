# ENKU Base — R40 PCBWay readiness

**30/100 (no increase), production release prohibited.** Active board: `enku-mainboard-r1.7-base-sd-power-sclk-mosi.kicad_pcb`.

R40 PCB includes 63 physical copper segments, 20 plated vias, 1 In2 GND zone, 125 components. R39 power breakout was **reworked to avoid blocking microSD SPI fanout**; SCLK and MOSI now have provisional F/B/In1 multi-layer routes to J2. CS and MISO still unrouted, and USB D+/D− remain unrouted pending 90Ω stackup and VBUS sense. Native R40 DRC results pending.

R39 actual Native [37807447885](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37807447885) baseline ERC 0 / parity 0 / 236 non-unrouted DRC / 243 unconnected. Entire board remains far from full DRC. Good Display p5 confirmation and FPC fold still pending written response.
