# R142: independent board review before PCBWay

Engineering review only. Physical tests: **NOT RUN**. Manufacturing: **NO FAB**.

Current PCB SHA256: `1ce355545d21d849e924f537488b5c9b9d59e9a8fa3cbbd129839823a7493ebf`.

## Actual corrections

| Finding | R142 change | Remaining qualification |
| --- | --- | --- |
| RC reset can release during slow supply ramps and retain charge across rapid cycling | U11 TLV803EA30DBZR, open-drain reset with existing R17 10k and J7 EN recovery. Pin1 GND,2 RESET,3 VDD. C15 becomes100nF supply bypass. | Supply ramps, rapid cycling, loaded dips, reset timing and partial-power states. |
| Retained feedback can fall below the supervisor's maximum release threshold; early R1423.38V candidate exceeds panel operative3.3V maximum | R14 27.4k / R15 4.99k,0.1%,10ppm/K exact Yageo RT codes. Nominal3.24549V. PWM initial/tolerance/TCR/FB-current scenario3.199451..3.291805V across -40..125C component temperatures. Maximum supervisor rising3.188724V gives10.727mV minimum static release margin; panel upper margin8.195mV. | **HOLD:** actual PFM, load/line behavior, startup overshoot and lifetime resistor drift. This narrow static margin is not dynamic or lifetime qualification. Panel ambient0..50C; module R8 ambient normally -40..65C. Silicon-temperature arithmetic does not extend product ratings. |
| SPI microSD has only a47k CS pullup | R23 changes to10k; R91-R94 add10k to CMD/DAT0/DAT1/DAT2. Unused DAT1/2 become bias-only nets, with no MCU allocation. No CLK pullup. | Actual cards, peak load, signal edge quality, initialization/hot removal and firmware ownership. |
| Card detection unused | J2.9 SD_CD, J2.10 GND, R90 10k, ESP GPIO39 / module pad32. | Configure GPIO39 as input and disable internal pulldown before interpreting active-low CD; debounce and test removal. |
| TS open-path behavior needs bias without removing fault protection | R82 100k retained; R89 3.3M to GND. Independent NTC MNA and corner/fault scenarios. | **HOLD:** guaranteed TS leakage and thermistor R/T envelope, mounting/thermal lag and fault tests. Detached sensor on a hot cell is not electrically detected. The network is not fail-safe for every fault. |
| Original VBUS and SD_CS_CARD copper enters Hirose hatched no-pattern areas despite DRC0 | Five front-only no-track/via/pad/fill rule areas from original DM3AT drawing; rerouted offending copper. | Drawing interpretation and actual card/socket/mechanical process fit. |
| Legacy drawings on disabled Dwgs.User and obsolete trial label |45 drawings archived/removed; trial note removed; USB mating guide retained on F.Fab. | Hidden reference/value fields remain intentionally inventoried; drawing visibility is not electrical qualification. |

## User-requested additional checks

| Area | Actual-source result | Unclosed work |
| --- | --- | --- |
| ESP32 flash/PSRAM | N16R8 exact MPN. GPIO35/36/37, module pads28/29/30, are singleton NC nets with no tracks. GPIO26..32 are internal memory signals and not exposed by WROOM-1. **Module pad32 is GPIO39**, used for SD_CD. | Boot firmware must select16MiB flash /8MiB octal PSRAM and validate memory with real hardware. |
| Straps/recovery | GPIO3/45/46 unused. GPIO0 has10k pullup, SW2 to GND and J7 BOOT. EN accessible on J7 and supervised. | Hold BOOT low while resetting, maintain at least3ms after EN rises, then use UART0 or ROM USB. J7 VREF is a measurement reference, not power input. No automatic DTR/RTS programmer exists on board. |
| USB-C | Independent R62/R63 5.1k CC-to-GND; U8 USBLC6-2SC6 on both D lines. D+/D- tied correctly across both receptacle orientations. VBUS has6.8uF nominal shunt filtering; no series ferrite. | Ferrite presence is not a universal functional requirement. ESD, EMI, inrush, suspend, cable/source behavior and90-ohm stackup are unqualified. Add a filter only from measured need and verified stability/drop. |
| Power path | BQ24072T IN=USB, BAT=battery, OUT=VSYS. Internal DPPM reduces charge before system load and allows battery supplement; TI specifies input reverse blocking. **No dock exists in Base.** | No mainboard battery PCM. Qualified finished protected cell/pack, polarity, harness, current and protection cutoffs are mandatory. No fuel gauge: switched2M/680k ADC measures a voltage proxy, not accurate SOC. |
| Hard OFF + USB | SW1/Q2 disconnect reader load after charger. Charger remains supplied. In modeled MCU high-Z state, EN1/EN2 default00 USB100 and CE remains low. U4 EN tied to switched VIN; U11 monitors switched output. | Measure USB/UART/GPIO back-power, EN decay, leakage and mode states. OFF does not guarantee500mA charging. USB100 alone is not a guaranteed no-battery ESP startup source. |
| E-paper | Selected GDEY0397T81P with SSD1677; Q1 IRLML6346TRPBF30V, L2 47uH20%, D1-D3 MBR0530T1G30V/0.5A,2.2ohm pulse-rated R37. Felix confirmed pin5 VDHR=VSH2 on10Oct; all24 J3 contacts and signal copper/paste checked. | FPC thickness0.30+-0.05 versus Hirose0.30+-0.03mm; tongue/finger/coverlay acceptance, folded pin1 pose, enlarged hold-down lands/paste, GDEM/GDEY CAD identity and physical panel/HV tests remain HOLD. See FPC_CONNECTOR_REVIEW_R142.md. |
| Inductor | Exact Laird TYS5040470M-10: typical Irms1A, Isat1.1A, DCRmax0.326ohm; Isat defined at30% L reduction and25+-5C. | Actual hot peak/ripple and RMS current are not measured. Typical Isat is not a guaranteed minimum at temperature. Compare current probe waveform and transient voltages against panel reference and part limits. |
| microSD | **SPI**, shared clock/MOSI with EPD, separate CS; DATA1/2 unused by host but externally biased. Supply on switched3V3. | SD+Wi-Fi+EPD peak current, load steps, card insertion and USB-MSC/filesystem exclusive ownership need firmware/bench evidence. |
| BMI270 | VDD and VDDIO on same switched rail; CSB high selects I2C, SDO low sets0x68;4.7k pullups; INT1 to GPIO18. Unused auxiliary/INT2 pins NC. | Load correct Bosch configuration, confirm INTERNAL_STATUS and chip ID, self-test, orientation and real interrupt. Start100kHz;400kHz requires measured rise <=300ns. |
| Layout/RF | Explicit all-layer antenna exclusion and native/Gerber copper inspection; original USB core unchanged. Both-inner GND centerline coverage retained for all14 fast nets. Power routing paths and switch/interface projected distances recorded. | Single-plane projection is not EM simulation. Preferred-plane gaps, return-via spacing, switching loop inductance, coupling, USB impedance and RF with real case/battery/FPC need qualification. Ground remains under the power circuitry; only the RF exclusion is cleared. |

## Executed computational methods

Native KiCad10.0.7 all-severity ERC/DRC, every track error, schematic parity and refilled zones. No severity, exclusion, outline or project rule changes were used to pass R142. Historical ignored checks remain disclosed in native reports and are covered where applicable by independent source/land/manufacturer audits.

Current board:134 references /453 native pads /114 fitted top parts /19 bare PCB entries /R67 DNP /373 vias.85 reference fields and127 value fields are hidden;16 enabled layers are named uniquely. No unassigned tracks/vias/copper fills, copper graphics without net semantics or disabled documentation objects. Four copper layers exactly; the original rear Tag-Connect rule area is distinct from the antenna exclusion.

Independent methods use actual exported data, not regenerated old goldens:

- NumPy nodal analysis of feedback and TS; adversarial tolerance/temperature/current corners;50,000 seeded Monte Carlo scenarios; analytic slow-ramp RC models.18 deliberately wrong pin/value cases must be rejected. These are not SPICE or manufacturer macromodels.
- Pin-by-pin source/PCB/primary-land comparisons;438 original pad definitions retained; explicit new source/net/component delta; USB UUID/name/physical geometry equality. Numeric KiCad net-code indices are permitted to reindex when adding new nets.
- Gerbonara1.6.3 parsing and full-polarity rendering of all four copper images. Added/missing copper outside0.0052mm curve budget must be below1e-6mm2; discrete Hausdorff below0.0052mm.
- Complete11-layer Gerber metadata/units/revision, PTH/NPTH drill and four USB slot axes,439 emitted pad records plus373 via IPC356 records, whole-board mask/paste/silkscreen, native BOM/CPL, R67 no-paste and six exact fill/cap requests.
- Independent Gerber conductor-island graph joined only by plated barrels, with actual pad labels independently IPC356 checked. No named-net opens/shorts accepted. In-memory copper bridge on U11 GND/RESET and copper cut on U11 supply must cause rejection. Original fabrication files are never mutated by these tests.
- Actual-layer centerline graphs and noded paths; three fixtures distinguish same-coordinate different layers, a real through-via and a same-layer crossing.30 explicit paths,14 fast-net reference metrics, via return distances and detours. No unresolved path accepted. Total-tree resistance, flight-time and capacitor-only droop scenarios are bounded models, not measured SI/PI.

The isolated GitHub workflow additionally runs immutable R13827 positive scopes and20 effective negative cases. Actual R142 source commit41b3f00a43748b81fdbdfcfd2fb15deee7c3f3e5 passed [run38576201886](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38576201886). `GITHUB_R142.json` records API digest, ZIP CRC and all24 manufacturing files matching after only declared timestamp normalization. Local or server pass does not run the physical procedures below.

## Primary references

Exact supplied panel PDF SHA256 `e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc`, pp5-8 and19; original microSD Hirose drawing SHA256 `43ac6f1af4a1fd92836f71e34614bbbc36903d2f403ff63c5aa4910da6a1e6ca`. FPC sources and the10Oct supplier confirmation are documented in [FPC_CONNECTOR_REVIEW_R142.md](FPC_CONNECTOR_REVIEW_R142.md). Supplied proprietary source PDFs/CAD are retained privately and not redistributed in this public repository.

[Espressif module](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), [SD pullups](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/sd_pullup_requirements.html), [schematic checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html), [PCB/RF guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html), [TI BQ24072T](https://www.ti.com/lit/gpn/bq24072t), [TPS63802](https://www.ti.com/lit/gpn/tps63802), [TLV803E](https://www.ti.com/lit/gpn/tlv803e), [Bosch BMI270](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf), [Laird TYS5040](https://www.laird.com/sites/default/files/tys5040-series-datasheet.pdf), [onsemi MBR0530](https://www.onsemi.com/pdf/datasheet/mbr0530t1-d.pdf), [Yageo RT v17](https://yageogroup.com/content/datasheet/asset/file/PYU-RT_1-TO-0-01_ROHS_L), [NXP I2C](https://www.nxp.com/docs/en/user-guide/UM10204.pdf).

See [physical procedures](FCT_PLAN_R142.md) and [manufacturer review instructions](PCBWAY_MANUFACTURING_NOTES_R142.md). None of the unclosed tests is represented as PASS.

