# R141 checks before PCBWay review

Current PCB SHA256: `b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe`. Working revision R141, NO FAB. The current package is a preliminary engineering packet. Review checks below have not been completed unless explicitly identified as passed. Physical tests require actual samples and cannot be closed by a source audit.

| Method | Next investigation | Evidence / closure condition | Current state |
| --- | --- | --- | --- |
| Native and export consistency | Exact-source DRC/ERC, connectivity/parity, four copper images, mask/paste/drill/IPC/BOM/CPL | Native0/0/0/0, actual-source20 guards, independent export pass and source hashes | PASS locally; published CI to be recorded separately |
| Regression fault injection | Historical control and effective rejection cases | All27 canonical R138 scopes and20 negative cases reject intended defects | PASS locally |
| Independent schematic walkthrough | U1..U11 pin functions, supply limits, startup defaults, pull-ups, straps, reset, BQ24072T/TPS63802 modes, HV panel sequencing | Pin-by-pin review tied to current schematic and primary manufacturer sources; findings resolved or explicit hold | TO DO |
| FMEA / fault trees | USB/battery absent/weak/reversed, NTC open/short/dislodged, shorted rails, switch/reset faults, connector/cable mistakes | Fault stimulus, propagation, protection response and measurable acceptance condition per case | TO DO; physical fault tests NOT RUN |
| SI / transmission-line review | USB pair vs actual stack, SPI clock/data/CS topology, stubs/branches, rise time, series termination, receiver timing | Stack-dependent estimates or model with stated inputs; measurable timing/impedance criteria | TO DO |
| Return-current review | Four-layer paths and transition returns; common MOSI0.741064mm/SCLK1.057355mm preferred-plane gaps; two ~2.7mm return-via locations | Quantified relevant transition paths and loop impact, preserving USB core and active ground planes | Geometry PASS; SI consequences TO DO |
| PI / DC paths | VBUS/VSYS/VBAT/3V3 drops, protection/cable/battery resistance, buck-boost demand, USB100 startup | Worst-case tolerances and combined ESP32/SD/EPD loads with explicit margins | TO DO; measurements NOT RUN |
| PI / transient and MLCC review | Effective capacitance vs bias/temp/tolerance, regulator stability, charge and load transients | Exact MPN data, load-step model and oscilloscope acceptance conditions | TO DO; measurements NOT RUN |
| Thermal analysis | Charger dropout power at worst supply/pack/load, regulator/MOSFET/diode/inductor heating, PCB heat spreading | Ambient and enclosure assumptions, uncertainty and component junction margins; real thermal tests | TO DO; physical tests NOT RUN |
| Footprint / polarity audit | Exact MPN land dimensions, pin1/cathode/source/drain, connector contact/FPC orientation, module EP | Independent manufacturer-drawing overlay and all127 references/438 pads disposition | Prior native checks PASS; independent manual pass TO DO |
| Process / stencil / DFM | Six filled/capped sites, U1 EP holes/window grid,0.2mm bores, USB slots/short stakes, solder masks and stencil | Written job-specific supplier acceptance and inspection criteria, no unapproved alternatives | HOLD |
| Mechanical / antenna | Exact current case CAD,59x101mm outline/cutout, holes, USB/buttons, module antenna, display/FPC bend, NTC retention, protected pack | Controlled CAD/physical fit with no increased case thickness; harness polarity and replaceability | HOLD; current complete CAD / qualified packs absent |
| Firmware / recovery / FCT | Blank-firmware startup, USB100 policy, charge/NTC modes, reset, UART/BOOT/EN fixture, USB-MSC/microSD ownership, PSRAM | Validated firmware image/offset/hash/flash contract and numeric fixture/FCT limits | HOLD; no production binaries |
| Real-board qualification | Startup/reset, USB current, CC/CV/timers, NTC faults, Wi-Fi/SD/EPD loads, temperature, USB-MSC, repeated cycles | Recorded waveforms/logs and pass/fail against predeclared limits, per R139 product plan | NOT RUN |

Record each new finding with method, affected refs/nets, source hash, primary evidence, severity, proposed action, verification and closure condition. If copper changes, create a new revision and re-export/reverify every manufacturing file. Preserve immutable historical guards and prove the new source separately.

Before the first PCBWay review upload: finish the source/geometry/manual methods, resolve package inconsistencies, state all remaining physical/process holds, verify final hashes and document exactly what response is requested. Supplier review can inform the eventual EVT process but does not close product qualification.

Layer audit also identifies unassigned J2 contacts9/10. Confirm their exact pin function against Hirose EDC-325165-00-00 and the intended card-detection/remount policy. They must not be silently described as mechanical lands or considered qualified.
