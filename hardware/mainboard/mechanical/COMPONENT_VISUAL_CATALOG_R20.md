# ENKU Reader R20 — physical components and manufacturer references

Based on **actual** KiCad board: `enku-mainboard-r0.1.kicad_pcb`, engineering branch `validation/base-r01-import`, checked 2026-10-08. All coordinates are KiCad mm; positive Y points down on the PCB drawing. **Do not order PCBWay fabrication yet.**

## Critical parts present on PCB

| Ref(s) | Actual installed KiCad value / footprint | Supplier documentation / image | Status & what to verify |
|---|---|---|---|
| Display (off PCB) | Good Display **GDEY0397T81P** 3.97" 800×480 | [Good Display module + drawing](https://www.good-display.com/product/613.html) | Chosen display; actual FPC exit and Z stack NOT registered |
| U1 | ESP32-S3-WROOM-1-N16R8, F.Cu **(33,45,90°)** | [Espressif datasheet](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) | Exact variant planned; antenna direction / no-metal/keepout verify |
| J3 | Hirose **FH34SRJ-24S-0.5SH(50)**, (58,28,0°) | [Hirose 2D + STEP + product](https://www.hirose.com/product/p/CL0580-1255-6-50) | 24-pin 0.5 mm FPC; contact orientation and fold unknown |
| J2 | Hirose **DM3AT-SF-PEJM5**, (28.9,100.7,90°) | [Hirose 2D + STEP + product](https://www.hirose.com/en/product/p/CL0609-0031-0-00) | **BLOCKER**. Hirose drawing + actual footprint: card enters from +X (board interior), despite old erroneous 'LEFT EDGE' silkscreen user-note. Rotate/re-place, then reroute SD. |
| J5 | GCT **USB4105-GF-A-120**, (47,110.325,0°) | [GCT USB4105 specification](https://gct.co/files/specs/usb4105-spec.pdf), [photos TME PL](https://www.tme.eu/pl/details/usb4105-gf-a-120/zlacza-usb-i-ieee1394/gct/) | 7 mm recessed vs R16 bottom y121. RELOCATE or notch |
| J1 | `JST_PH_3_PLACEMENT` (66,93.5,90°) | [JST 3-pin side-entry S3B-PH-SM4-TB candidate](https://www.digikey.pl/pl/products/detail/jst-sales-america-inc/S3B-PH-SM4-TB/926656) | **PLACEHOLDER**, candidate not electrically or mechanically qualified, verify polarity / TS |
| SW1 | `HARD_POWER_SWITCH_PLACEMENT` (30.5,29,0°) | [C&K JS102011SAQN side-slide candidate](https://www.digikey.pl/en/products/detail/c-k/JS102011SAQN/1640095) | **PLACEHOLDER**, candidate SPDT 3-terminal differs from two-pad placeholder; power-path switching must be designed first |
| SW2 | `SW_SPST_TL3342` (35.5,87,0°) | [E-Switch TL3342 series](https://www.e-switch.com/product/tl3342-series-low-profile-smt-tactile-switch/) | Service/BOOT tactile; accessibility and case clearance |
| SW3 / SW4 | `READING_BUTTON_PLACEMENT` (25,63)/(25,75), 0° | [G-Switch GT-TC035A-H0195-L3 (LCSC C915811) miniature recessed side-button](https://www.lcsc.com/product-detail/C915811.html) | **PLACEHOLDERS**; C915811 candidate body envelope is shown on Dwgs.User, exact recessed cutout and land pattern NOT designed |
| SW5 / SW6 | `READING_BUTTON_PLACEMENT` (71.2,63)/(71.2,75), 0° | [G-Switch GT-TC035A-H0195-L3 (LCSC C915811) miniature recessed side-button](https://www.lcsc.com/product-detail/C915811.html) | **PLACEHOLDERS**; C915811 candidate envelope in Dwgs.User faces +X; final mirrored land pattern and cutout NOT designed |
| U2 | TI TPS2121RUX (43.5,91,0°) | [Texas Instruments TPS2121](https://www.ti.com/product/TPS2121/part-details/TPS2121RUXR) | Power mux; pin-1/pad orientation verify |
| U3 | TI BQ25185DLHR (48.5,91,180°) | [Texas Instruments BQ25185](https://www.ti.com/product/BQ25185) | LiPo charging + TS, regulation voltage must match actual pack |
| U4 | TI TPS63802DLAR (58,91,0°) | [Texas Instruments TPS63802](https://www.ti.com/product/TPS63802/part-details/TPS63802DLAR) | Buck-boost; pad dimensions and L1 proximity |
| U5 | Bosch BMI270 (28,80,0°) | [Bosch BMI270 + documentation](https://www.bosch-sensortec.com/en/products/motion-sensors/imus/bmi270) | Axes/pin-1 orientation and distance from magnet |
| U6 | TI DRV5032FBDBZR (72,45,0°) | [Texas Instruments DRV5032FBDBZR](https://www.ti.com/product/DRV5032/part-details/DRV5032FBDBZR) | Hall; magnet and case geometry not registered |
| U8 | ST USBLC6-2SC6 (54.2,108.8,180°) | [ST USBLC6-2](https://www.st.com/en/protections-and-emi-filters/usblc6-2.html) | USB ESD, very close USB port; pin orientation |
| Q1 | Infineon IRLML6346TRPBF (67,48,0°) | [Infineon IRLML6346](https://www.infineon.com/cms/en/product/power/mosfet/n-channel/irlml6346/) | SOT-23; pinout and power switching |
| L1 | Murata DFE201612E-R47M=P2 (61.2,91,270°) | [DigiKey PL Murata](https://www.digikey.pl/pl/products/detail/murata-electronics/DFE201612E-R47M-P2/9815903) | 0.47 µH; buck-boost |
| L2 | Laird TYS5040100M-10 (58,43,0°) | [Official Laird TYS5040 series datasheet](https://www.laird.com/sites/default/files/tys5040-series-datasheet.pdf) | 10 µH / nominal 5 × 5 mm; inductor height against 10 mm housing |
| J6 | 4 contact dock pad layout, B.Cu (47,99,0°) | [Actual PCB copper footprint](../kicad/enku-mainboard-r0.1.kicad_pcb) | **No qualified mating pogo pins**, stand alignment not proven |
| J7 | Tag-Connect TC2030-IDC-NL, B.Cu (35,87,0°) | [Tag-Connect footprint technical documentation](https://www.tag-connect.com/technical) | Programming pad pattern, not a fitted component |
| H1–H4 | 4 × 2.2-mm M2 mounting holes, (30,23),(71,23),(23,111),(71,111) | [Board source](../kicad/enku-mainboard-r0.1.kicad_pcb) | **PROVISIONAL**: lie under nominal centered display projection |
| R1–R38, R62–R69 | Generic 0603 / 0805 values in schematic/PCB | [KiCad PCB footprints](../kicad/enku-mainboard-r0.1.kicad_pcb) | Supplier-specific MPN not chosen for generic passives |
| C1–C36 | Generic 0603 / 0805 capacitors | [KiCad PCB footprints](../kicad/enku-mainboard-r0.1.kicad_pcb) | Voltage/dielectric/vendor MPN to be verified in BOM |
| D1–D3 | Generic SOD-123 diode footprints | [KiCad PCB footprints](../kicad/enku-mainboard-r0.1.kicad_pcb) | Final diode MPN/schematic polarity qualification remains |
| TP1–TP14 | Rear test pads, B.Cu | [KiCad PCB](../kicad/enku-mainboard-r0.1.kicad_pcb) | Copper land patterns, do NOT order as electronic components |

## Measured physical blockers (nominal centered display only)

- Board 59 × 101 mm, corners x18…77 y20…121.
- Good Display portrait module is 56.24 × 96.62 mm; centered module would cover approximately x19.38…75.62 and y22.19…118.81. **All four current M2 holes H1–H4 lie within that rectangular projection.** The module **must not be loaded** by screw heads, bosses or board.
- Side button centers: left x25 = 7.0 mm from edge x18; right x71.2 = 5.8 mm from edge x77. Original placeholder bodies are 3.8 mm wide; approximate body-to-edge gaps are left 5.1 mm, right 3.9 mm. These are NOT real side-mounted buttons and cannot prove actuator reach.
- The USB footprint nominal PCB edge datum is y=114.0, while the board now terminates at y=121.0; port is recessed 7.0 mm until we move it and reroute or machine a notch.
- **MicroSD insertion orientation error:** Hirose official 2D drawing has the electrical terminals opposite the card-entry edge. Actual footprint J2 has terminal-row pads at local Y=-7.725 and card entrance at local Y~+8.125. Board placement (28.9,100.7), 90° rotation, transforms the card-entry edge to x~37.025 mm and points the opening **toward positive global X (the board interior)**; left external edge is x=18.0. The previous text 'CARD EJECT → LEFT EDGE' was WRONG and is replaced by an explicit non-manufacturing note. Do not use a left-hand case opening at x18 for this layout; reroute/reorient first.
- J1 and SW1 are **not manufacturer-certified footprints**. J6 is pads, not a physical pogo connector. The exact battery pack, frontlight, all button model SKUs, rear shell and FPC exit are not qualified.

## Next corrective placement candidate

See [R21 coordinated connector/controls relocation plan](PCB_RELOCATION_PLAN_R21.md) — the candidate J2 rotation to 270° and J5 shift to the true bottom edge are NOT yet committed to the routed PCB. These require rerouting, not isolated coordinate patches.

## R22 shortlist: compact China-source tactile switches

The earlier C&K PTS645V family is **REJECTED** for ENKU Reader: too large for 59mm narrow side rails. Current candidate is **G-Switch GT-TC035A-H0195-L3**, LCSC **C915811**, 2.8 × 2.65 × 1.95mm according to the manufacturer's dimensions (LCSC lists 2.8 × 1.95 × 2.65mm in a different axis order); 1.6N actuation, 0.15±0.05mm travel, 300k cycles. Recessed-edge design requires a PCB edge pocket and qualified pads.

- [LCSC product C915811](https://www.lcsc.com/product-detail/C915811.html) — preferred Chinese distributor link for PCBWay BOM/RFQ. **LCSC stock does not prove PCBWay procurement**; require written PCBWay sourcing confirmation.
- [Official G-Switch family](https://www.dg-switch.com/qingchukaiguanchenbanshixilie/1539.html) — dimensions, recessed height 0.98mm, lifecycle, downloadable 3D/drawing inquiry. If drawing cannot be retrieved, do not fabricate exact footprint from thumbnail.
- [Panasonic EVPAVAA1A, LCSC C2845003](https://www.lcsc.com/product-detail/C2845003.html) — alternate family concept (not an automatic pin-compatible substitute).
- [SHOU HAN TS24CA, LCSC C393942](https://www.lcsc.com/product-detail/tactile%20switches_shou%20han_ts24ca_C393942.html) — very low-cost fallback, but much lower specified 20k cycles.
- **Do not use** E-Switch TL3780AF (vertical actuation) as a side button, irrespective of miniature package dimensions.

The four dashed button bodies on KiCad **Dwgs.User** are conceptual 2.65×2.8mm top-view projection near exterior edges; **not real footprint, solder mask, CNC pocket or verified actuator location**. They intentionally preserve SW3–SW6 electrical placeholders until official land patterns, 3D heights, left/right rotations, wall actuator, and PCBWay CNC capability are confirmed.

See [R22 PCBWay sourcing brief](PCBWAY_BUTTONS_R22.md).

## Production gate

Run `python hardware/mainboard/tools/mechanical_release_audit.py` to print physical blockers. Run with `--release` to fail closed when blockers/manual fit checks remain. This is deliberately separate from schematic and connectivity tests; a structural green check is never a claim of production readiness.

### Recommended reviewer order

1. Open manufacturer pictures + 2D drawings for J2/J3/J5 and look at the **slot/entry orientation**.
2. Inspect the four side-button candidates, then visually compare their body depth to the 59 mm board with only 62 mm proposed outer width.
3. Compare USB nominal port datum and cutout with housing, and LiPo connector mating side/cable routing.
4. Compare physical display + FPC projected space against screw bosses; choose new hole positions only after registered 3D.
5. Review U1 antenna, U5 axes, and high-profile L2 against back shell and battery pouch clearance.
