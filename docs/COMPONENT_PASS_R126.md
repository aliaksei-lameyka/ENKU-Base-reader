# R126 — exact components and corrected lands

R125 still carried generic MPNs and inconsistent physical rectangular-pad angles. R126 fixes **61 component instances**: 40 resistors, 17 capacitors, three diodes and SW2. The exact MPN/Manufacturer/Assembly fields agree between the native schematic netlist and PCB. This is an engineering component selection; procurement, assembly-process and electrical bench qualification remain open.

**Native KiCad 10.0.7: opens 0, ERC 0, schematic parity 0; DRC 65 = 45 library mismatch + 20 preserved hole clearances.** Short, copper clearance, courtyard overlap and outline violations: 0. No rules or exclusions were changed. [Server evidence](GITHUB_NATIVE_R126.md), [remaining work](REMAINING_TO_BUILD_R126.md).

## What changed physically

120 of the 124 declared pads change geometry/position; SW2's four lands keep their accepted geometry. All 417 pad UUIDs, logical pin numbers and net names survive. All 2610 original track/via identities, nets, layers, widths and drills survive. Ten footprints move locally; 57 original copper items have explicitly declared endpoint/position changes and 29 segments are added. All other copper, footprint placements, schematic net nodes, project rules, exclusions, outline, zones and RF keepouts are independently guarded against accepted R125.

C25 previously had horizontal pad centres but pad angle 90 degrees; R126 uses angle 0 with 0.95 × 1.40 mm rectangular lands. C26's pad angle changes 180 → 90 degrees to match its vertical package. Similar inconsistent axes on other generic passives are corrected. The guard now checks physical global pad axes against package rotation, not only the library nickname.

Dense body/land courtyards use a documented 0.10 mm nominal excess beyond maximum package body/nominal lands. Correcting axes and adding truthful courtyards exposed tight placements and routed copper. D1, C2/C6/C12 and R10/R12/R13/R15/R16/R36 move locally; explicit CHG_STAT1, EPD_RST, SD_CS, VBUS and SYS_EN/GND paths restore connectivity. Three same-net via-to-land clearances missed by native DRC were increased; the independent audit checks 90 new/relocated vias since R120 and preserves the 0.10 mm limit. **The dense courtyard allowance and assembly process are not factory-qualified.**

## Nominal land evidence

| Local footprint | Land, mm | Centre spacing, mm | Primary evidence / limit |
| --- | --- | --- | --- |
| R_RC0603_YAGEO_REFLOW | 0.90 × 0.80 | 1.70 | Yageo chip-resistor mounting v10, 2018-02-13, p4/table1: A2.6 B0.8 C0.9 D0.8; RC_L v14 package |
| C_CC0603_YAGEO_REFLOW_TRANSFER | 0.80 × 0.90 | 1.50 | Engineering transfer of Yageo AC HiCap X7R/X7S v4, 2025-08-05, p18/table14, 0603(1), to separately verified CC dimensions |
| C_CC0805_YAGEO_REFLOW_TRANSFER | 0.95 × 1.40 | 1.85 | Same engineering transfer, size 0805; current CC family documents do not establish CC-specific land approval |
| MBR0530T1G_ONSEMI_CASE425H | 0.91 × 1.22 | 3.27 | onsemi MBR0530T1/D rev9 Oct2024, CASE425 issueH, 2024-02-29, drawing98ASB42927B, p4 |
| TL3342F160QG_ESWITCH_P010632J | 1.70 × 1.00 | X6.30 / Y3.80 | E-Switch P010632 revJ/PCR24740, 2021-02-09; four-pad geometry unchanged |

URLs, downloaded byte counts and SHA256s are in [manufacturer_reference_manifest_R126.json](../hardware/mainboard/kicad/checks/manufacturer_reference_manifest_R126.json). The primary PDFs and their land drawings were read and visually inspected. Capacitor CC package body dimensions are checked separately against the exact MPN sheets. No CC-specific reflow qualification or minimum effective capacitance is inferred from a nominal land recommendation.

## Resistors

All selected RC0603 non-zero values: 1%, nominal 0.1 W at 70°C, 75 V working voltage; derating/voltage/pulse limits still apply. Jumpers RC0603JR-070RL have **rated 1 A, maximum 2 A**, not 2 A continuous rating; resistance <50 mΩ. Signal transient/pulse performance and precision circuits remain separate gates.

| References | Value | Exact Yageo MPN |
| --- | --- | --- |
| R19, R20, R21, R22, R28, R29, R64, R65, R67 | 0R | RC0603JR-070RL |
| R10, R13, R16, R35, R36, R40, R72 | 100k | RC0603FR-07100KL |
| R11, R12, R17, R18 | 10k | RC0603FR-0710KL |
| R8 | 18k | RC0603FR-0718KL |
| R38, R39, R66 | 1M | RC0603FR-071ML |
| R9 | 1k | RC0603FR-071KL |
| R30, R31, R32, R33, R34 | 22R | RC0603FR-0722RL |
| R26 | 2M | RC0603FR-072ML |
| R73 | 3.3k | RC0603FR-073K3L |
| R24, R25 | 4.7k | RC0603FR-074K7L |
| R23 | 47k | RC0603FR-0747KL |
| R62, R63 | 5.1k | RC0603FR-075K1L |
| R14 | 511k | RC0603FR-07511KL |
| R27 | 680k | RC0603FR-07680KL |
| R15 | 91k | RC0603FR-0791KL |

R12 and R67 remain DNP, including native PCB DNP attributes. R20/R21/R22/R64/R65 keep fitted 0R and the explicit tuning alternative RC0603FR-0722RL (22 Ω). R70/R71 precision values and R37 pulse-current sense value/package are unchanged and are not replaced with general 1% RC0603 parts.

## Capacitors

| References | Exact Yageo MPN | Nominal value | Rating / dielectric / tolerance |
| --- | --- | --- | --- |
| C6, C10, C37 | CC0603KRX7R9BB104 | 100nF | 50 V / X7R / 10% |
| C35 | CC0603KRX7R9BB472 | 4.7nF | 50 V / X7R / 10% |
| C4, C9, C13 | CC0805KKX5R6BB106 | 10uF | 10 V / X5R / 10% |
| C8 | CC0805KKX5R6BB475 | 4.7uF | 10 V / X5R / 10% |
| C7 | CC0805KKX5R8BB106 | 10uF | 25 V / X5R / 10% |
| C2 | CC0805KKX7R6BB105 | 1uF | 10 V / X7R / 10% |
| C5, C24, C25, C26, C31 | CC0805KKX7R8BB475 | 4.7uF | 25 V / X7R / 10% |
| C11, C12 | CC0805MKX5R6BB226 | 22uF | 10 V / X5R / 20% |

The generated CC0805MKX5R6BB226 sheet contains an invalid “insulation resistance 0 mOhms” entry. That entry was rejected; the X5R family specification controls insulation. No zero-resistance capacitor interpretation was carried into the design. Exact nominal values are not a claim that regulator/charger/EPD minimum capacitances are met after DC bias, tolerance, temperature and ageing. Those numeric checks remain open.

## Diodes and SW2

D1/D2/D3 are now **onsemi MBR0530T1G**, 30 V / 0.5 A nominal. Pin1 is the banded cathode: D1 EPD_VGH, D2 GND, D3 EPD_CP_NEG. Pin2: D1 EPD_SW, D2 EPD_CP_NEG, D3 EPD_VGL. The source net nodes and physical pad UUIDs are unchanged. Switching overshoot, reverse-voltage margin, heat, leakage during sleep and HV discharge require electrical verification.

SW2 is **E-Switch TL3342F160QG**, P010632 revJ, 12 V/50 mA, 160±50 gf nominal force. The horizontal top pair is logical1/BOOT (drawing reference3/4); bottom pair is logical2/GND (drawing reference1/2). Manufacturer reference terminal numbers are not substituted for logical schematic pad numbers.

## Independent checks and views

Native full DRC uses severity-all, all-track-errors, schematic parity and zone refill/save. Full schematic ERC and native XML netlist are exported. Additional guards cover exact MPNs and physical pad axes, common rows/cathode maps, DNP/tuning, Q1/Q2/U9 manufacturer pinouts and lands, U1 nine paste windows and 0.3 mm drills, J7 no-paste/backside contacts, J5 four logical S shield pads, actual filled USB GND references and all source/copper preservation.

The USB path checker now starts at actual connected track endpoints inside a resistor land and retains copper layers; vias alone link layers. The revised method was rerun on accepted R125: **USB routed copper and both revised measurements are identical between R125 and R126**. Revised track-only skew is A −2.702599 mm, B +1.214508 mm. The difference from the old centre-root numbers is a measurement-method change, not a routing improvement or impedance qualification. See [cross-check](../hardware/mainboard/kicad/checks/usb_contact_measurement_crosscheck_R126.json).

[Native top view](../hardware/mainboard/kicad/checks/native_top_R126.svg) and four cropped PNGs (native_epd_spi, native_logic_boot, native_power, native_usb) show actual KiCad F.Cu/F.Fab/F.CrtYd/Edge.Cuts. Red is copper, grey is fab geometry, magenta is courtyard. All 61 changed component centres are covered. These are source review views, not manufacturing outputs or complete assembly/3D approval.

**NO FAB.** Exact stock/lifecycle and complete BOM/CPL freeze remain open. Historical Q1/Q2/U9 and SW1 decisions are preserved.
