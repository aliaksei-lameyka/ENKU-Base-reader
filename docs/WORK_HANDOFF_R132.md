# ENKU R132 engineering handoff — NO FAB

Branch: `engineering/r132-battery-supply-charge`. Open `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Active selector: `checks/current_checkpoint.json` →R132. Canonical PCB SHA256: `540faac1779277466bdaca739325d1139cf8cead39f4d9b9df1eaa0529a648f3`. Do not open an older numbered experimental PCB as the current revision.

**Real local KiCad10.0.7:0opens,0ERC,0schematic parity; exactly20unchanged intrinsic hole findings;0library mismatch warnings.** All17 independent engineering guards plus native checkpoint comparison pass. Board:59×101×1.6mm,122footprints,442pads,3144copper items. Native CPL:102 fitted rows,19 bare PCB items,1DNP(R67),103explicit MPN fields including DNP. Server verification is recorded separately after the actual run; local success is not a claimed server result.

## What was completed

U3 now uses TI **BQ24072TRGTR** with a new project-local17-pad RGT land pattern and independent pin-map/stencil checks. R9=2k1% sets nominal445mA (394.6–492.4mA with stated IC/resistor corners). R8=3.48k1%; EN1=VBUS/EN2=GND selects USB500 mode. R83=69.8k1% gives nominal8.725h fast timer,6.718–10.771h corners. TD is low, CE has the existing100k pull-down. R12 is fitted for CHG; R67 remains DNP. C7/C8 are explicit22uF10V YageoCC0805MKX5R6BB226.

Keep direct J1 JSTPH2, pin1VBAT/pin2GND, and electrically independent J8 cell sensor. R80=31.6k/R81=19.6k bias the real Semitec103JT-050 NTC; R82=100k protects TS per TI. Nominal measured-table interpolation predicts4.587–39.740°C; the constant-beta corner exercise predicts2.606–7.531°C cold/36.947–42.114°C hot. Open/short and nominal0°C/45°C inhibit in the model. **Actual0–45°C protection, full R/T tolerances, input leakage and thermal attachment are not qualified.** No fake room-temperature resistor or automatic timer-restart workaround was introduced.

The bounded charger routing is complete. An independent native filled-plane test detected voids under the preserved USB pair even when native DRC reported0opens; only new power routing/vias were repaired. All actual USB projections and the accepted1mm core ground-reference strip now pass. The long USB pair, ESD polarity, signal contacts and previous reference geometry are preserved; actual90ohm stackup/power/bench compliance remains HOLD.

Power-sheet visual inspection also found obsolete BQ25185/three-wire/Dock-mux notes and overlap between J8/C7 and support labels. Current comments/title, the new IC pin labels, five support diagrams and separate J8 placement were corrected. Native ERC/parity and the exact net-node comparison were rerun; these are diagram changes, not moved PCB connectors. Finite before/after token signatures preserve22 intentionally adjusted old schematic children and the title block; every other old schematic element remains guarded.

## Preservation and recovery provenance

At the start of this turn the earlier scratch workspace was gone. Both remote R131 and the pre-existing R132 branch still held R131 hardware. The missing earlier R132 binary was **not recovered**. This source was reconstructed from accepted R131/R130 and the recorded design values, then routed and checked anew; no old zero-open result was reused as current proof.

Early reconstruction was separately published at commit65a51ad403a7b2e1b6ecbe8bd26d6933ab79a313, explicitly routing incomplete/NO FAB. Accepted historical reports, boards and commits remain intact. The current independent guard verifies627 unchanged project files,416 retained non-U3 pad UUIDs with only five declared component translations,2402 untouched original copper items,239 declared original local removals and742new bounded copper items. All other electrical nodes, old library/cache symbols, RF keepouts, outline, thickness, exclusions and rules are preserved. The20DRC findings match the old findings by type/severity/description/exact item UUIDs. No rule waiver was used to close new errors.

The old `apply_charge_R132.py` is the initial one-time reconstruction recipe from the recovery checkpoint, not a command to rerun on the finished source. `route_charge_R132.py` produces bounded heuristic proposals with actual USB reference protection; every proposal requires a new native DRC and independent guards. The committed canonical source is the final checked result.

## Battery and unchanged enclosure

[Thin-cell supply comparison](BATTERY_SUPPLY_R132.md) records all73 primary catalogue pages and319 qualifying thin rows. The Chinese stocked shortlist includes336080(3.3mm/2000mAh),385787(3.8mm/2500mAh),366076(3.6mm/2000mAh),385570(3.8mm/2050mAh). A Poland innEnergy306070 listing claims2000mAh/3mm/PCM, but its60mm width and1A current specification do not qualify the existing mechanical/2A-peak contract. Narrow335084/325381 show zero catalogue stock. There is **no approved interchangeable pack pair** and no verified China warehouse/EU delivery reservation.

The existing PH2 packaging collision and assumed boss/edge margins remain open. No current complete enclosure CAD is registered; the old10mm reference is not a current case approval. **No case thickness increase or arbitrary pouch relocation is accepted.** Direct PH2 avoids a three-contact adapter's extra harness/contact pair but its tall board header remains mechanically unqualified.

Existing Koosay, Polybattery and Akyga/Ropla supplier threads were checked; no new incoming response was found, no RFQ was duplicated, no email/order/manufacturing action was sent.

## Remaining work, in dependency order

1. Register full current enclosure/panel/FPC/component bodies and controlled maximum finished PCM-pack drawings; resolve PH2/pouch/RF/boss collision within the unchanged thickness. Confirm two procurable alternatives in China and Poland, polarity, PCM/current and swelling allowances.
2. Finish the real sensor/TS leakage/tolerance/attachment FMEA; confirm guaranteed effective C7/C8 capacitance, charger thermal spreading and complete2000–2500mAh charge before the minimum timer under the specified load/temperature. Current native/model results do not prove these behaviors.
3. Resolve20intrinsic hole findings against manufacturer drawings and the chosen fabrication process, actual controlled USB stackup, exact panel/FPC vendor ambiguities, stencil/reflow/EP via-grid process, complete assembly BOM/CPL and final manufacturing outputs. Existing U1 grid and accepted component-land fixes are retained.
4. Implement the changed PGOOD/CHG firmware contract and USB current/suspend policy, then reader/USB-MSC safe microSD ownership. Firmware is not present in this hardware tree.
5. After user approval for prototypes, execute [sequenced bring-up and fault matrix](BRINGUP_AND_FAULTS_R132.md), record actual instrument/firmware/pack evidence and fix any observed hardware issue before release. Do not claim that planned bench tests were performed.

Production/purchase release, battery thermal qualification and enclosure fit remain false. Do not infer PCBWay readiness from0opens or passing CI.
