# R134 USB input-current and charger control

Engineering source contract; firmware and hardware qualification are pending. No production or purchasing permission is implied. Open the canonical `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro` project.

## Native signal mapping

| ESP32-S3 signal / WROOM-1 pad | Command net | Series part | Charger net / BQ24072T pin | Hardware pull-down |
|---|---|---|---|---|
| GPIO16 / pad9 | CHG_EN1_CMD | R86,1k1% | CHG_EN1 / pin6 EN1 | R84,2.2k1% |
| GPIO2 / pad38 | CHG_EN2_CMD | R87,1k1% | CHG_EN2 / pin5 EN2 | R85,2.2k1% |
| GPIO38 / pad31 | CHG_CE_CMD | R88,1k1% | CHG_CE_N / pin4 CE | R10,100k |

The library and sheet cache now identify **pin5 as EN2 and pin8 as VSS**, matching TI SLUS937C. The previous pin-name error was hidden while both nodes were grounded. Pin8 and exposed pad17 remain GND. GPIO19/20 USB, module PSRAM pins35–37, strap pins0/3/45/46 and the unused GPIO40/JTAG allocation are preserved. Exact native terminal sets are checked independently of labels.

## Modes and power states

Order is **EN2,EN1**. Values are TI input-current limits, including system load, not promised battery charge current.

| EN2 | EN1 | Mode | Input limit |
|---:|---:|---|---|
|0|0|USB100|90/95/100 mA minimum/typical/maximum|
|0|1|USB500|450/475/500 mA minimum/typical/maximum|
|1|0|External ILIM|R8=3.48k1%; modeled maximum493.45 mA|
|1|1|USB suspend|Qualify actual input draw against TI conditions and the applicable USB state|

CE high disables charging; it does not disconnect the charger's OUT/system power path. CE low enables charge subject to TS, timers, voltage and thermal conditions. SW1 disconnects the reader load; battery and charger remain connected.

With the MCU unpowered/high impedance, pull-downs model EN2/EN1=00 and CE=0. **OFF charging is therefore limited by USB100**, and fast OFF500 mA charging is not implemented. Boot ROM, brownout, GPIO hold/retention and partial power states must be measured; a nominal high-impedance model does not prove the actual startup sequence. No automatic BC1.2 detection or USB-PD negotiation is implemented.

Firmware must establish a safe current mode before requesting more input current, keep the mode within the connected source's authorized budget, and implement USB suspend/disconnect handling. Switching between two-bit modes needs a reviewed transition order and scope evidence; two independent GPIO writes are not simultaneous. A USB100-to-USB500 change uses EN1 only with EN2 low. Do not select ILIM or500 mA merely because VBUS/PGOOD is present. When unpowered, firmware cannot command suspend or recover a timer fault.

PGOOD is CHG_STAT1, CHG is CHG_STAT2; fitted10k pull-ups are supplied by3V3_SYS. Signals are not valid reader GPIO levels while OFF. CHG low alone does not prove charging and CHG high alone does not prove full SOC. Do not automatically toggle CE to bypass a charge-timer fault.

## Electrical margin and charge settings

R84/R85 use Yageo RC0603FR-072K2L; R86–R88 use RC0603FR-071KL on the project-specific nominal reflow lands. The independent control calculation models 1% tolerances,3.0–3.6 V supply, IC input-current corners and ESP VOH/VOL fractions. Its modeled minima/maxima are EN high1.633 V/low0.250 V/high-Z2.222mV and CE high2.366 V/low0.358 V/high-Z0.101 V.

**These figures are conditional.** Espressif's referenced DC table is at3.3 V/25 °C and describes high-impedance VOH/VOL measurement. Extending those fractions to this resistor load and full supply/temperature range is not a manufacturer guarantee. Scope the MCU-side and charger-side pins under boot/reset/brownout, all four modes and temperature/load corners before signoff; mode-pin GPIO load is modeled below 0.916 mA.

R9=2k1% gives nominal 445 mA fast charge with modeled394.55–492.42 mA setting corners. R83=69.8k gives nominal8.725 h timer, modeled minimum 6.718 h. Available battery current also depends on input budget, system load, DPPM and thermal regulation. Neither timer arithmetic nor mode selection proves a full2000–2500 mAh cycle. Existing TS parts/sensor are unchanged. CE control does not detect a physically detached sensor or cure the identified R81-open hot fault.

## Connector and verification

J5 is **GCT USB4215-03-A**, project footprint `ENKU:USB4215_03_A_GCT_REVA`, checked against GCT RevA26Apr2024 drawing SHA256 `1659ba00769b9b774a033fac72cb2f3bfc481a3272c53f34e87520f33635a9e1`. Nominal height3.16 mm; board remains1.6 mm and59×101 mm. The mating face stays at boardY121 mm. Four real plated shell slots replace the previous connector/locator geometry. Twelve physical SMD mask/paste openings serve sixteen numbered signal contacts; actual native plots are audited. Do not reuse the old USB4105 body model.

The preserved long USB pair, signal vias and reference requirements are checked against actual refilled native planes. EN1 command routing has additional clearance from USB signal-via reference copper. This closes the prior tiny reference-shadow gap; actual USB shadow/core missing area must be zero in the current guard report. A qualified90-ohm stackup, full case/plug fit, short0.8 mm shell-stake assembly on 1.6 mm board and USB power/functional bench evidence remain HOLD.

Primary references: [TI BQ24072T SLUS937C](https://www.ti.com/lit/ds/symlink/bq24072t.pdf), [Espressif WROOM-1 module datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), [ESP32-S3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf), [GCT USB4215](https://gct.co/connector/usb4215). Native electrical/control and connector reports remain the implementation evidence; these links do not imply physical qualification.
