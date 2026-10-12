# ENKU R132: first board checks and charger fault matrix

**Planned tests; no physical board or battery was tested in this pass.** This is an engineering bring-up sequence, not permission to manufacture or order. Do not connect an unqualified real pouch pack until its chemistry, polarity, PCM, charge-temperature range and mechanical installation are accepted.

## Firmware signal contract

U3 is nowBQ24072TRGTR. CHG_STAT1 is open-drain **PGOOD** and CHG_STAT2 is open-drain **CHG**, both pulled to3V3_SYS by fitted10k resistors R11/R12. They are not the former BQ25185 status pair. CE is held low by R10; TD is low and the safety timer is enabled. The hard switch still removes the reader load while the charger/battery remain connected.

PGOOD low means valid input under the TI conditions. CHG low alone does not prove charge current: TS/thermal charge suspension can keep CHG low. CHG high can also occur during recharge after the first completed cycle; it is not an unconditional SOC indication. TI specifies a2Hz CHG timer-fault pattern. No firmware source is present in this hardware tree; implementations must use input validity, cell voltage and fault history and must not automatically toggle CE to bypass timer faults. When the reader is OFF its status pull-ups are unpowered; do not report these GPIOs as valid.

USB500 mode is hard selected with EN1=VBUS and EN2=GND. This does not establish USB enumeration/suspend compliance. Until verified, use a regulated bench source with a documented current budget. Input current available for the battery falls under system load/DPPM; nominal445mA is a setting, not a guaranteed simultaneous load-plus-charge budget.

## Sequenced bench gates

| Gate | Equipment/action | Record and acceptance basis |
|---|---|---|
|1. Unpowered inspection|Microscope, DMM; inspect U3 pin1/bridges, EP soldering, U1 via-grid process, switch/USB/SD/FPC orientation; verify J1/J8 continuity and no shorts.|Compare exact netlist and native drawings. No battery attached; insulation, connector retention and polarity checked explicitly. |
|2. Battery-only reader|Current-limited 1S battery emulator with appropriate sink capability when later charging; USB absent; SW1OFF thenON.|OFF/backfeed leakage, VBAT/VSYS and3V3_SYS; regulator nominal3.3077V, accept against TI/feedback tolerances and load specification, not a made-up percentage. Verify switch interrupts SYS_EN load supply. Ramp qualified voltage range; record startup, droop and brownout. |
|3. USB-only/input transfer|Regulated documented5V source; suitable battery emulator/dummy load; scope input/SYS/3V3.|Input UVLO behavior, inrush, DPPM, battery supplement, cable drop and USB attach/detach. Check OFF connector backfeed, no unintended battery power at VBUS. Measure500mA-mode current including reader load against450/475/500mA IC bounds and datasheet test conditions. |
|4. MCU/reader peripherals|Controlled power, USB/UART/service programming, known microSD and exact panel; exercise4buttons/BMI270/e-paper.|Boot, flash, USB D+/D− polarity and both Type-C orientations, SD reads/writes, panel pin5/vendor hold resolution, full refresh current, radio burst droop and brownout recovery. Firmware functions are pending; native copper checks do not prove them. |
|5. Charge-setting check|Sink-capable battery emulator or accepted battery fixture, programmable load, ammeter and thermal measurement.|R9=2k1% implies394.6/445/492.4mA bounds including stated KISET/resistor tolerances. Record actual CV4.20V behavior, termination, recharge and system-current split. Apply the full datasheet voltage/current conditions and uncertainty budget. |
|6. Temperature/fault matrix|Precision resistance substitute at J8, then a real103JT-050 attached to a dummy pouch under controlled temperature; scope CHG_TS/VIN and charge current.|Open/short inhibit and controlled cold/hot transitions; see below. Model is not a guaranteed full sensor tolerance envelope. Do not heat or freeze a live unqualified battery to force faults. |
|7. Capacity/timer/thermal|Only an approved PCM pack after preceding gates; log a complete2000 and2500mAh cycle at specified temperatures and simultaneous reader loads.|Demonstrate completion before minimum6.718h timer or document a justified setting change. DPPM/thermal regulation slows the timer proportionally and TS pauses it; this is not proof that any load completes. Measure charger/junction/pouch/case temperatures under fixed enclosure conditions. |
|8. Functional stress|Qualified power and firmware: repeated USB disconnect, MSC file operations and safe ownership transfer, radio+refresh+SD peaks, low battery and OFF/ON.|No filesystem corruption, no unexpected reset, no lost disconnect event; capture scope traces and reproducible firmware version. Repeat with both approved replacement packs. |

Current-limited initial power is a reversible bench check. Measurements and firmware logs must be retained with PCB source SHA256, assembled BOM/pack MPN, fixture details, ambient, instrument calibration/uncertainty and verdict. Test outcomes are currently **not run**.

## NTC circuit and planned injected faults

External103JT-050 is10k1%/B25-85=3435K1%; R80=31.6k fromVBUS toBAT_TS, R81=19.6k toGND, R82=100k series toCHG_TS. NTC atJ8 is in parallel withR81. TI TS threshold ratios are cold0.245–0.255 and hot0.12–0.13 of input; use actual VIN. Nominal Semitec table interpolation predicts4.587°C/39.740°C. A constant-beta corner exercise gives2.606–7.531°C cold and36.947–42.114°C hot; these figures do not replace controlled full R/T tolerance or TS leakage, attachment lag and self-heating analysis.

| Injected condition | Model prediction | Required real evidence |
|---|---|---|
|J8 open|BAT_TS/VIN at leastapproximately0.378; above cold boundary; inhibit.|Charge current inhibited across VIN, source resistor and input leakage corners; status behavior logged. |
|J8 short|Ratio0; below hot boundary; inhibit.|Charge current inhibited; short is confined to isolated sensor circuit. |
|J8 at25°C equivalent10k|Nominal ratio inside charge window.|Actual allowed state and current at required source/system conditions. |
|Semitec nominal0°C/45°C equivalent|Both outside respective limits.|Inhibit at these points across controlled real sensor/input variations; no charging outside pack's approved0–45°C interval. |
|Sensor detaches from pouch|Electrical model still looks valid.|Mechanical attachment and thermal lag proof; this failure is not detected by resistance alone. |
|R80/R81/R82 open/short|Not fully qualified by the nominal sensor model.|FMEA and safely injected fixture tests; do not claim redundant protection or PCM temperature coverage. |
|Fast timer expiry|CHG2Hz fault per TI.|No automatic CE restart; record current/state/recovery under controlled timing/load. |

22uF nominal C7/C8 must each provide at least4.7uF effective. The current20%tol/15%temp/10%age budget leaves13.464uF before DC bias, so retained bias fraction must be≥0.349 for these minima. Exact DC-bias curves/part qualification remain missing. EP copper/mask1.68mm square and TI example paste1.55mm square give approximately85.1% paste area; actual stencil/reflow, EP voiding and heat spreading require assembler acceptance. No external QFN fanout via has been treated as a substitute for a verified thermal design.

## Release holds

Keep `fabrication_ready=false` until20 unchanged intrinsic hole findings have a justified process/design resolution, the exact battery and full fixed-thickness enclosure are accepted, effective capacitors and thermal/full-charge behavior are qualified, actual USB90-ohm stackup and power/suspend behavior are proved, exact panel/FPC ambiguities are resolved, and final BOM/CPL/mask/paste/drill/panel/assembly outputs are reviewed. Release only after user agreement; no manufacturing or purchase occurred in R132.
