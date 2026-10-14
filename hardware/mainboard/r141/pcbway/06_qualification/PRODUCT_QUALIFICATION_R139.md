# ENKU Base Reader - R139 qualification preparation / physical board R138

Status: ENGINEERING REVIEW ONLY - NO FAB. No production order, purchase, factory upload or supplier message is authorized by this document. R139 is an audit/documentation revision; the PCB remains the accepted R138, SHA256 `90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971`.

## Verified source evidence

Main `81b34a97c765c0fdb5ded5e4c1d4ed22d06756cb` retains the hardware and workflow of actually tested source `2601e16abb754564580adb28c202337e69d8b1ab`. Actual main run 38311804626 and its retained SHA/CRC-checked artifact establish KiCad 10.0.7 DRC/ERC/opens/parity zero, 27 independent scopes and 20 effective rejection cases. This is computational source evidence. It is not measured startup, RF, cell-temperature, programming, EMC or product qualification.

The new boot/recovery source audit checks both schematic nodes and native physical connected partitions. U1 is ESP32-S3-WROOM-1-N16R8. J7 offers target VREF, GND, UART TX, UART RX, BOOT and EN. GPIO46, GPIO45, GPIO3 and the exposed R8-reserved GPIO35/36/37 are externally unconnected. R17=10k/C15=1uF and R18=10k are present. GPIO19/20 connect to USB DM/DP through fitted zero-ohm R65/R64. This establishes a plausible programming/recovery route, not a successfully programmed unit.

## Design holds before an approved EVT order

1. **Startup and source policy.** Reset/hard-OFF high-impedance GPIO defaults set USB100. Input current supplies both reader and charger. An absent battery cannot supplement ESP32/EPD/SD peaks. Blank-flash, low-cell, PCM-open and no-battery startup require scope captures and a supported power-source policy. Do not assume 500mA before source authorization. The 10k/1uF reset network needs slow-ramp and rapid-cycle verification; the official Espressif guidance specifically calls for power-monitor review in those conditions. A design failure must be corrected in a new PCB revision before user release.
2. **Charging completion.** Current model: 445mA nominal, 394.55..492.42mA scenarios; maximum BAT regulation 4.24V. Fast timer nominal 8.725h, minimum 6.71825h. The ideal 2500mAh/minimum-current CC calculation leaves only about 0.382h against the minimum timer, excluding CV, precharge and losses. This is not a prediction of a timer fault: TI slows the timer during DPPM, VIN-DPM and thermal regulation. Full real-pack CC/CV, termination, recharge, fault and thermal cycles in the final enclosure must establish compatibility. Do not bypass safety timers or repeatedly restart charging as a workaround.
3. **NTC faults and attachment.** Separate Semitec 103JT-050 is a candidate, attached to the replaceable pouch, with hand-soldered tails at bare J8 pads. Nominal modeled window is about 4.90..35.01C. Guaranteed TS leakage/R-T corners and actual attachment lag remain unqualified. R82-open leaves a floating, unqualified TS input; R82-short loses series protection. A sensor detached from a hot pouch can still look like room temperature. Resolve the circuit/fault analysis and mechanical retention before consumer release; a passed sensor-open resistor test alone does not close detachment.
4. **Capacitance and loads.** R136 typical-curve scenarios provide margin; guaranteed effective capacitance across bias, AC voltage, ageing, temperature and lots is not available. Test converter stability, source inrush, R37 pulse stress, EPD rails and combined Wi-Fi/SD/EPD loads with real approved components. Proposed normal-operation rail target is 3.10..3.50V; U1's manufacturer operating range is 3.0..3.6V. The target is not measured or approved yet, and every other part's limits must also be met.
5. **Product definition.** Final panel/FPC, present complete case CAD and two interchangeable protected 2000-2500mAh two-wire packs with China/Poland sourcing are not qualified. Finished PCM/wires/tabs/connector dimensions must fit the unchanged case thickness, including clearance for tolerances and pouch swelling. The confirmed 5.2mm AKY0156 is rejected for thickness. A provisional supplier envelope does not approve a thicker case.
6. **Factory process.** Written job-specific acceptance is needed for 91 nominal 0.20mm via bores on 1.6mm PCB, six resin-filled/copper-capped sites, U1 EP grid, short USB stakes, stencil, stackup and 90-ohm USB. See manufacturing notes and exact process CSVs. Nominal geometry does not certify actual registration, plating or assembly quality.
7. **Firmware and fixture.** This hardware repository has no validated diagnostic/release binary and flash-offset manifest bound to R138. Firmware elsewhere is not invalidated by this statement. A production FCT cannot run until images, matching fixture, numeric acceptance budgets, test logs and recovery procedure are approved.

## Qualification sequence

**Gate A - source and factory review:** close documented design inputs and obtain a proposed stackup/process/assembly/test response. This packet is usable for engineering feedback and costing, not manufacturing authorization.

**Gate B - approved engineering samples (EVT):** first inspect assembly and joints; then current-limited staged startup. Capture VBUS, VBAT, VSYS/SYS_EN, 3V3, EN, input/battery current and reset causes. Exercise blank/invalid firmware recovery by native USB and J7 UART; read device identity/eFuses without burning them, verify 16MB flash and 8MB Octal PSRAM with non-destructive/allocated test regions. Test both USB-C orientations, C-C/A-C hosts, source authorization, suspend and hot-plug. Check SD file checksums, interrupted writes and exclusive host/reader ownership in USB MSC. Verify exact EPD HV/refresh, buttons, BMI270, ADC, RF, OFF/sleep current, mechanics and battery replacement.

Charging fault tests start with a current-limited simulator/dummy pouch and a programmable NTC fixture. Never intentionally overheat an unqualified live pouch. Full charging and temperature tests use a qualified real pack within its limits. Proposed characterization includes load steps (50mA to 1A only where source/pack budgets permit), repeated power/USB cycles and a 24-72h combined workload. Counts, temperature range and limits must be frozen from measured EVT results before formal validation; these proposals are not completed tests or factory pass criteria.

**Gate C - design validation and golden unit:** validate final case/panel/packs, slow ramps/rapid cycles, charging and component faults, endurance, ESD/EMC pre-compliance and RF in the actual enclosure. Record raw evidence and root causes. Freeze the physical PCB, approved BOM/alternates, case and firmware together. A hardware change reopens affected checks; accepting a prototype with a bodge does not qualify the unmodified production design.

**Gate D - every manufactured unit:** inspect/polarity, safe power, flash identity and verified image, PSRAM, USB, SD, EPD, controls/IMU, charger/NTC stimulus and power-state transitions. Record serial/MAC, PCB revision, lots, firmware SHA256, fixture/software version, calibration, numeric results and raw-log paths. Install the approved user image after diagnostics and verify it. Return a unit-level PASS/FAIL record; empty records are NOT RUN. Factory FCT sampling must not replace requested 100% functional testing without explicit agreement.

## Factory and release boundaries

Bare-PCB electrical net testing and AOI check fabrication/assembly faults. They do not prove software flashing, SD ownership, load stability or charging safety. PCBWay's testing service asks for test steps, acceptance criteria, fixture requirements and environment. Functional-test scope/costs and sponsorship coverage need a concrete factory agreement.

There is no guarantee of zero physical failures before first hardware. The useful standard is closed design risks, traceable measured validation, repeatable unit testing and no accepted production-revision hardware rework. All physical test rows in the supplied template intentionally start as NOT RUN.

## Primary sources, read 2026-10-13

- Espressif schematic checklist: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html
- Espressif WROOM-1/1U datasheet v1.8: https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf
- esptool ROM boot selection: https://docs.espressif.com/projects/esptool/en/latest/esp32s3/advanced-topics/boot-mode-selection.html
- ESP-IDF USB Serial/JTAG limitations: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/usb-serial-jtag-console.html
- TI BQ24072T SLUS937C, especially dynamic timers section 9.3.9: https://www.ti.com/lit/ds/symlink/bq24072t.pdf
- TI TPS63802 SLVSEU9D: https://www.ti.com/lit/ds/symlink/tps63802.pdf
- PCBWay functional testing requirements: https://www.pcbway.com/pcb-assembly/pcb-assembly-testing.html
