# R143 independent board review

**NO FAB.** Source PCB SHA256 `3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266`. Source commit `c9dc9e624c260154094d23a93028e547f52420e8`.

J3 S1/S2 copper and their two paste-only apertures now match the original Hirose drawing:0.40x0.80mm. Their four UUIDs are the only physical pad changes versus R142. Electrical topology, every other pad, all tracks/vias/placements/outlines/rule areas and project settings are preserved. Signal copper0.30x0.80mm and paste0.25x0.65mm remain unchanged.

Local native10.0.7 DRC0/ERC0/opens0/parity0; full Gerber/native copper, independent connectivity, IPC/drill/mask/paste/silk and BOM/CPL checks passed. R138 was rerun from immutable commit2601e16abb754564580adb28c202337e69d8b1ab:27 scopes and20 effective rejection cases passed. Current repository README has evolved, so the old R138 whole-repository hash guard is run in its actual historical snapshot. No old guard or golden was changed to accommodate current documentation.

J3 audit rejects10 effective design-fault cases. The exact R142-to-R143 native geometry and netlist delta is independently checked. Manufacturing release is separately blocked by [startup risks](STARTUP_RISKS_R143.md), especially the actual PFM/common-rail margin.

## User-requested additional checks

| Area | Actual-source result | Unclosed work |
| --- | --- | --- |
| ESP32 flash/PSRAM | N16R8 exact MPN. GPIO35/36/37, module pads28/29/30, are singleton NC nets with no tracks. GPIO26..32 are internal memory signals and not exposed by WROOM-1. **Module pad32 is GPIO39**, used for SD_CD. | Boot firmware must select16MiB flash /8MiB octal PSRAM and validate memory with real hardware. |
| Straps/recovery | GPIO3/45/46 unused. GPIO0 has10k pullup, SW2 to GND and J7 BOOT. EN accessible on J7 and supervised. | Hold BOOT low while resetting, maintain at least3ms after EN rises, then use UART0 or ROM USB. J7 VREF is a measurement reference, not power input. No automatic DTR/RTS programmer exists on board. |
| USB-C | Independent R62/R63 5.1k CC-to-GND; U8 USBLC6-2SC6 on both D lines. D+/D- tied correctly across both receptacle orientations. VBUS has6.8uF nominal shunt filtering; no series ferrite. | Ferrite presence is not a universal functional requirement. ESD, EMI, inrush, suspend, cable/source behavior and90-ohm stackup are unqualified. Add a filter only from measured need and verified stability/drop. |
| Power path | BQ24072T IN=USB, BAT=battery, OUT=VSYS. Internal DPPM reduces charge before system load and allows battery supplement; TI specifies input reverse blocking. **No dock exists in Base.** | No mainboard battery PCM. Qualified finished protected cell/pack, polarity, harness, current and protection cutoffs are mandatory. No fuel gauge: switched2M/680k ADC measures a voltage proxy, not accurate SOC. |
| Hard OFF + USB | SW1/Q2 disconnect reader load after charger. Charger remains supplied. In modeled MCU high-Z state, EN1/EN2 default00 USB100 and CE remains low. U4 EN tied to switched VIN; U11 monitors switched output. | Measure USB/UART/GPIO back-power, EN decay, leakage and mode states. OFF does not guarantee500mA charging. USB100 alone is not a guaranteed no-battery ESP startup source. |
| E-paper | Selected GDEY0397T81P with SSD1677; Q1 IRLML6346TRPBF30V, L2 47uH20%, D1-D3 MBR0530T1G30V/0.5A,2.2ohm pulse-rated R37. Felix confirmed pin5 VDHR=VSH2 on10Oct; all24 J3 contacts and signal copper/paste checked. | FPC thickness0.30+-0.05 versus Hirose0.30+-0.03mm; tongue/finger/coverlay acceptance, folded pin1 pose, GDEM/GDEY CAD identity and physical panel/HV tests remain HOLD. See FPC_CONNECTOR_REVIEW_R143.md. |
| Inductor | Exact Laird TYS5040470M-10: typical Irms1A, Isat1.1A, DCRmax0.326ohm; Isat defined at30% L reduction and25+-5C. | Actual hot peak/ripple and RMS current are not measured. Typical Isat is not a guaranteed minimum at temperature. Compare current probe waveform and transient voltages against panel reference and part limits. |
| microSD | **SPI**, shared clock/MOSI with EPD, separate CS; DATA1/2 unused by host but externally biased. Supply on switched3V3. | SD+Wi-Fi+EPD peak current, load steps, card insertion and USB-MSC/filesystem exclusive ownership need firmware/bench evidence. |
| BMI270 | VDD and VDDIO on same switched rail; CSB high selects I2C, SDO low sets0x68;4.7k pullups; INT1 to GPIO18. Unused auxiliary/INT2 pins NC. | Load correct Bosch configuration, confirm INTERNAL_STATUS and chip ID, self-test, orientation and real interrupt. Start100kHz;400kHz requires measured rise <=300ns. |
| Layout/RF | Explicit all-layer antenna exclusion and native/Gerber copper inspection; original USB core unchanged. All14 fast nets have a GND projection in at least one of the two inner planes at every track-centerline point. Either preferred plane can have gaps. Power routing paths and switch/interface projected distances recorded. | Single-plane projection is not EM simulation. Preferred-plane gaps, return-via spacing, switching loop inductance, coupling, USB impedance and RF with real case/battery/FPC need qualification. Ground remains under the power circuitry; only the RF exclusion is cleared. |

## Executed computational methods

Native KiCad10.0.7 all-severity ERC/DRC, every track error, schematic parity and refilled zones. No severity, exclusion, outline or project rule changes were used to pass R143. Historical ignored checks remain disclosed in native reports and are covered where applicable by independent source/land/manufacturer audits.

Current board:134 references /453 native pads /114 fitted top parts /19 bare PCB entries /R67 DNP /373 vias.85 reference fields and127 value fields are hidden;16 enabled layers are named uniquely. No unassigned tracks/vias/copper fills, copper graphics without net semantics or disabled documentation objects. Four copper layers exactly; the original rear Tag-Connect rule area is distinct from the antenna exclusion.

Independent methods use actual exported data, not regenerated old goldens:

- NumPy nodal analysis of feedback and TS; adversarial tolerance/temperature/current corners;50,000 seeded Monte Carlo scenarios; analytic slow-ramp RC models.18 deliberately wrong pin/value cases must be rejected. These are not SPICE or manufacturer macromodels.
- Pin-by-pin source/PCB/primary-land comparisons;434 original pads unchanged; four J3 hold-down copper/paste definitions corrected; explicit new source/net/component delta; USB UUID/name/physical geometry equality. Numeric KiCad net-code indices are permitted to reindex when adding new nets.
- Gerbonara1.6.3 parsing and full-polarity rendering of all four copper images. Added/missing copper outside0.0052mm curve budget must be below1e-6mm2; discrete Hausdorff below0.0052mm.
- Complete11-layer Gerber metadata/units/revision, PTH/NPTH drill and four USB slot axes,439 emitted pad records plus373 via IPC356 records, whole-board mask/paste/silkscreen, native BOM/CPL, R67 no-paste and six exact fill/cap requests.
- Independent Gerber conductor-island graph joined only by plated barrels, with actual pad labels independently IPC356 checked. No named-net opens/shorts accepted. In-memory copper bridge on U11 GND/RESET and copper cut on U11 supply must cause rejection. Original fabrication files are never mutated by these tests.
- Actual-layer centerline graphs and noded paths; three fixtures distinguish same-coordinate different layers, a real through-via and a same-layer crossing.30 explicit paths,14 fast-net reference metrics, via return distances and detours. No unresolved path accepted. Total-tree resistance, flight-time and capacitor-only droop scenarios are bounded models, not measured SI/PI.

The R143 workflow runs the same source-bound checks remotely. Its actual run result is recorded separately in GITHUB_R143.json after completion. No older run is labelled as current proof.

See [primary documents and release decision](STARTUP_RISKS_R143.md), [FPC drawing review](FPC_CONNECTOR_REVIEW_R143.md), [first5-10 board procedures](FCT_PLAN_R143.md) and [PCBWay process notes](PCBWAY_MANUFACTURING_NOTES_R143.md).
