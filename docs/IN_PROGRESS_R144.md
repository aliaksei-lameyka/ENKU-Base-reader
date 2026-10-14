# R144 power-margin work in progress — NOT FOR FABRICATION

R143 is the published, independently checked reference at commit `ad0d19cb8ce4538b32a3ae04df3486dfaf503ff1`. R143 remains blocked for EVT manufacturing; see [STARTUP_RISKS_R143.md](STARTUP_RISKS_R143.md).

**This document preserves the R144 design decision after loss of access to the KiCad working environment. The local R144 source and placement are not yet published or accepted. Do not use this branch as a manufacturing release.**

## Selected electrical change

The original common ESP32/panel supply cannot meet the declared 50 mV reset-release and 25 mV panel-ceiling engineering reserves with the old A30 supervisor. See the source-bound R143 calculation.

| Item | R144 selection and connection |
| --- | --- |
| U11 | TPS389001DSER, TI DSE0006A WSON6. Pin1 SENSE; 2 GND; 3 MR_N tied 3V3_SYS; 4 VDD=3V3_SYS; 5 CT; 6 open-drain RESET_N=ESP_EN. Retain R17 and J7 wired-OR reset. |
| R95 | RT0603BRB0716K5L, 16.5 kohm, 0.1%, 10 ppm/K, 3V3_SYS to RESET_SENSE. |
| R96 | RT0603BRB0710KL, 10 kohm, 0.1%, 10 ppm/K, RESET_SENSE to GND. |
| C40 | CC0603KRX7R9BB104, 100 nF 50 V X7R, RESET_CT to GND. Timing must use effective capacitance, not only nominal. |
| C41 | CC0603JRNPO9BN102, 1 nF 50 V C0G, RESET_SENSE to GND. Its roughly 6.2 us RC requires fast-dip qualification. |
| C15 | Existing 100 nF supply bypass relocated next to U11. |
| R14 | Existing 27.4 kohm 0.1% 10 ppm/K retained; pin1 becomes REG_FB_TOP. |
| R98 | RT0603BRB07301RL, 301 ohm 0.1% 10 ppm/K, 3V3_SYS to REG_FB_TOP. Combined top feedback resistance 27,701 ohm. |
| R15 | RT0603BRB075K11L, 5.11 kohm 0.1% 10 ppm/K. |
| R97 | RC0603JR-070RL, 0 ohm FIT, 3V3_SYS to REG_MODE. |
| R99 | RC0603JR-070RL, 0 ohm DNP with no paste, REG_MODE to GND. Never fit R97 and R99 together. |
| U4 | TPS63802 MODE pin2 becomes REG_MODE; AGND pin3 stays GND. Forced PWM is the default after soft-start. Initial soft-start behavior follows TI and must be measured. |

All added resistors are E96 values. The earlier hypothetical 27.1 kohm E192 choice was not used.

Conditional calculation with PWM feedback accuracy +/-1%, feedback/input leakage +/-100 nA, resistor initial +/-0.1%, 10 ppm/K and up to 100 K deviation from 25 C:

- Regulator nominal 3.210469667 V; initial static bounds 3.164888383..3.256322238 V.
- Supervisor falling bounds 3.007879204..3.087309556 V.
- Conservative maximum rising threshold 3.112779860 V, combining guaranteed threshold error and maximum hysteresis.
- Static release margin approximately 52.1 mV; margin below panel 3.3 V operative ceiling approximately 43.7 mV.

These are **calculated initial static envelopes**, not measurements or an unconditional lifetime/production guarantee. Solder/life drift, effective capacitance, ripple, fast load steps, slow ramps, converter soft-start, OFF/back-power and forced-PWM battery impact still require explicit assessment. The new sense divider draws approximately 120 uA at nominal supply.

## Exact U11 footprint requirement

Primary TI TPS3890 datasheet SLVSD65A; package drawing DSE0006A 4220552/B, January 2024:

- 1.5 x 1.5 mm body, six pins, no exposed pad.
- Pad centers: 1=(-0.55,-0.5), 2=(-0.6,0), 3=(-0.6,+0.5), 4=(+0.6,+0.5), 5=(+0.6,0), 6=(+0.6,-0.5) mm.
- Left SMD-defined lands: copper pin1 0.90 x 0.35 mm; pins2/3 0.80 x 0.35 mm; mask inset 0.05 mm. Separate paste pin1 0.80 x 0.25 mm; pins2/3 0.70 x 0.25 mm.
- Right NSMD lands: 0.70 x 0.25 mm; mask expansion 0.025 mm; nominal paste.
- Rounded-corner geometry and stencil/mask must be checked against the primary drawing, then against the actual Gerbers.
- Left copper gaps are 0.15 mm. A narrowly scoped U11 pad-pair rule was added locally, but the last DRC still reports the two 0.15 mm gaps against the project minimum 0.20 mm. Resolve the actual KiCad minimum-versus-rule behavior explicitly; retain independent >=0.20 mm foreign-copper checks everywhere outside the declared OEM land exception. Do not hide or waive the errors.

## Last actually observed local state

- New R144 source under `hardware/mainboard/r144/kicad/`, derived from R143 without modifying historical sources.
- 141 references and 473 native pads after placement. Expected assembly: 120 FIT top, 19 bare, R67 and R99 DNP. Confirm all counts from final exports.
- Initial schematic ERC: zero. After MODE/AGND correction, schematic/board parity: zero. ERC must be rerun on the final corrected source.
- Last placement DRC: **22 violations and 19 unconnected items**, not accepted. Includes R97/R98 placement conflicts, two U11 minimum-clearance errors, stale copper ends and one silk collision.
- The MODE/AGND label mistake was corrected: power-schematic label UUID ending 067=REG_MODE at pin2; UUID ending 068=GND at pin3.
- U11, R15 and C15 PCB descriptions were aligned to the schematic.
- The older R143 startup envelope still applies to R143 only. Do not rename its report and claim R144 passed.
- No physical startup, USB, EPD, battery, thermal, EMC, ESD or lifetime test has been run.

Last intended component positions in mm (not a routed final design):

| Ref | Center | Rotation |
| --- | --- | --- |
| U11 | 44.5,67.5 | 0 |
| R95 | 44.5,65.4 | 0 |
| R96 | 41.5,66.5 | 0 |
| C41 | 44.5,63.9 | 0 |
| C15 | 46.0,69.2 | 0 |
| C40 | 46.0,71.2 | 0 |
| R97 | 56.5,97.2 | 0 |
| R98 | 55.3,85.3 | 0 |
| R99 | 56.5,99.6 | 0 |

R97 and R98 still conflict with old copper/components and must move. Prefer geometry-based free placement rather than repeatedly guessing positions. Keep SENSE/CT short on F.Cu. Preserve USB geometry, antenna keepouts, Hirose J2 no-pattern areas, board outline and established mechanical constraints.

## Remaining acceptance work

1. Finish placement and routing; zero native DRC/ERC/unconnected/parity on the exact R144 source.
2. Add finite R143-to-R144 delta guards: only declared original component changes, seven additions and explicitly reviewed copper changes. Preserve immutable R138/R141/R142/R143 references.
3. Independently check manufacturer pin maps, new supervisor mask/paste/copper, complete copper connectivity, Gerber/netlist consistency, drill annuli and hole clearances, assembly data, rail/threshold/timing corners and FIT/DNP mode interlock. Prove checks reject actual injected faults.
4. Rerun ESP32 reserved pins and straps, ROM recovery, USB CC/ESD, power path/OFF, battery/NTC, exact panel map/booster, SD, BMI270, all named/hidden layers, RF keepouts and return paths. Retain explicit unknowns where primary sources provide only typical curves.
5. Build and review a reproducible N16R8 first-boot/FCT firmware before assembly. Physical per-board FCT must include supply ramps/dips, current-limited first power, battery/USB/OFF cases, ROM download and memory, SD, BMI270, e-paper HV/refresh and temperature.
6. Run source-pinned server CI; compare actual manufacturing outputs; regenerate README, PDFs, BOM/CPL and the PCBWay package. No fabrication release until the remaining assembly, FPC/connector, battery and qualification holds have defensible closure.

The environment failure is a tooling block, not evidence that the unresolved board checks pass.
