# R50 actual copper inventory — 2026-10-10

Source: `hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb` on `engineering/r50-pcbway-closure`.
Read-only source inspection; **NOT a Native KiCad connectivity test**, not fabrication approval.
Net counts below count literal `(segment ... (net N))` records, **not connected endpoints**. Zero segments may be acceptable on intentionally shorted pads or zone-connected GND; review with native connectivity report.

## Measured board structure
- KiCad source: 168,678 characters; 132 `footprint` declarations; 515 `segment` declarations; 132 `via` declarations; 3 `zone` declarations (including zone-fill artifacts; do not infer three independent valid copper planes).
- Last verified R48 Native KiCad baseline: ERC 0, parity 0, priority DRC 0; **139 unconnected + 168 other DRC**. No R50 Native result claimed.
- Manufacturing score **44/100, NO-GO**. Do not increase from record counts.

## Measured segment inventory (critical selected nets)

| Net | Segment records |
| --- | ---: |
| USB_DP_CONN / USB_DM_CONN | 0 / 0 |
| USB_DP / USB_DM | 0 / 0 |
| USB_CC1 / USB_CC2 | 5 / 6 |
| VBUS_USB | 44 |
| USB_VBUS_VALID / USB_VBUS_DIV / USB_VBUS_REF | 18 / 21 / 1 |
| SD_CS_CARD / SD_MOSI_CARD / SD_SCLK_CARD / SD_MISO_CARD | 7 / 4 / 5 / 7 |
| SD_CS / SPI_MOSI / SPI_SCLK / SPI_MISO | 15 / 10 / 16 / 6 |
| BTN_L1 / BTN_L2 / BTN_R1 / BTN_R2 | 6 / 6 / 19 / 13 |
| I2C_SDA / I2C_SCL | 0 / 0 |
| EPD_CS / EPD_DC / EPD_RST | 0 / 0 / 0 |
| EPD_BUSY / EPD_SCLK_PANEL / EPD_MOSI_PANEL | 0 / 0 / 0 |
| EPD_VSH2 (held pin 5) | 0 |
| 3V3_SYS / VSYS / VBAT | 95 / 13 / 0 |

## Engineering route priority
1. **I2C + low-voltage EPD logic**: plan clear corridors, device orientation, local decoupling and return paths; do not route EPD HV pin 5 until supplier confirms VDHR/VSH2.
2. **USB data path**: establish actual PCBWay 4-layer stackup and impedance design **before** routing GPIO19/GPIO20 ↔ series resistors ↔ ESD ↔ USB-C. Check connector A/B pad polarity, CC1/CC2, ESD ground return and connector access.
3. **Remaining power / charger / battery routing**: inspect zone connections and OFF-state leakage; validate current rating and layer neck-downs. Physical slide switch MPN is provisional.
4. **Native KiCad**: rerun ERC, parity and **full** DRC; classify 139 baseline unrouted by net, eliminate all copper issues, then clean 130 footprint-library mismatches and 38 silk findings against supplier footprints.
5. **Manufacturing release**: GDEY vs GDEM CAD identity, J3 mating and contact side, FPC bend radius, supplier pin-5 written confirmation, HV parts ratings, 3D clearance, BOM/CPL orientation and inspected Gerber/drill outputs.

## Product boundary
Base 3.97-inch 480×800 panel; ESP32-S3, microSD, USB MSC requirement, four side buttons, BMI270, battery + slide power, repairable assembly. **No Hall, Qi or frontlight**. Pro remains separate.

**Hard block:** do not submit PCBWay manufacturing until Native KiCad reports zero unrouted and zero unwaived production DRC, and vendor electrical/mechanical holds are cleared.
