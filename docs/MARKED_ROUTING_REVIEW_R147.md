# ENKU R147 -18 marked regions and mechanical compatibility

Twelve marked regions simplified:38 original top-copper segments replaced by13, unique length reduced0.818847mm. All141 footprints,473 pads,386 vias, outline, holes, source thickness and project rules preserved. The R146 mechanical STEP is compatible with R147.

Native KiCad10.0.7 DRC/ERC/opens/parity0. Complete local independent electrical, primary-source/OEM, power, four-layer Gerber equality, manufacturing and84-net Gerber graph checks PASS. Actual source-pinned server run38763074552 also PASS. API digest/ZIP CRC, all24 manufacturing files,41 JSON reports and native geometry match the local run with creation metadata only. Physical tests NOT RUN / NO FAB.

| Region | Nets | Result |
| --- | --- | --- |
| N01 | GND | Retained real three-way GND junction with0.20/0.25mm branches; no redundant degree-two bend. |
| N02 | EPD_MOSI_PANEL, EPD_RESE, EPD_VSH2 | SIMPLIFIED; full local native and independent checks PASS |
| N03 | EPD_RESE | SIMPLIFIED; full local native and independent checks PASS |
| N04 | I2C_SCL | SIMPLIFIED; full local native and independent checks PASS |
| N05 | GND, I2C_SDA, IMU_INT1 | SIMPLIFIED; full local native and independent checks PASS |
| N06 | GND, RESET_SENSE | SIMPLIFIED; full local native and independent checks PASS |
| N07 | 3V3_SYS, VBAT | Retained: direct3V3_SYS shortcut leaves only0.0533mm to BAT_ADC copper, below0.20mm rule. |
| N08 | 3V3_SYS, GND | Retained C19 supply entry: straight0.25mm shortcut leaves0.168541mm to U5.6 GND land, below0.20mm rule. |
| N09 | CHG_EN1, VSYS | Retained small VSYS jog: degree-two geometric simplification would lose a same-net contact/branch. Existing explicit connection preserved. |
| N10 | GND | SIMPLIFIED; full local native and independent checks PASS |
| N11 | CHG_ILIM_VSET, CHG_ISET | Single diagonal CHG_ILIM_VSET approach into a land; no two-edge zigzag at marked point. |
| N12 | SD_CS_CARD, SPI_SCLK | SIMPLIFIED; full local native and independent checks PASS |
| N13 | GND, REG_MODE, SYS_EN | SIMPLIFIED; full local native and independent checks PASS |
| N14 | CHG_ILIM_VSET, CHG_STAT2, GND, VSYS | SIMPLIFIED; full local native and independent checks PASS |
| N15 | GND, SD_CS_CARD | SIMPLIFIED; full local native and independent checks PASS |
| N16 | GND, VBAT | Single GND via approach and adjacent VBAT route; no eligible redundant two-edge corner at marked point. |
| N17 | 3V3_SYS, GND, SD_DAT1_BIAS, SD_MISO_CARD, SPI_SCLK | SIMPLIFIED; full local native and independent checks PASS |
| N18 | SD_MOSI_CARD, SPI_MOSI, SPI_SCLK | SIMPLIFIED; full local native and independent checks PASS |

Retained direct-route probes are geometric counterexamples; they do not assert every possible alternative reroute is impossible. No component moved to make routing cosmetically straight.
