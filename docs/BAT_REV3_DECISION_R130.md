# ENKU Base BAT-REV3 — R130 engineering decision

**Engineering branch:** `engineering/bat-rev3-external-ntc`. **NO FAB / no orders / no default merge.** Accepted predecessor is R129 HEAD `b7d05483db8b1b7794280c472e52a7824d88a662`, PCB SHA256 `bab3cda1faa40bb2535f2d3eefe6ef0a9f43593b82577843cfe54f6d98da013c`. Canonical project remains `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`; selector is R130. All ten BAT-REV3 package files were read; all nine manifest member hashes and sizes matched. Previously unpublished L2 work was recovered and tested again after the workspace reset.

## Connector decision

Choose **A for the engineering PCB: PH-2 plus separate retained cell sensor**. This is an implemented interface decision; complete battery/enclosure/charger acceptance remains open.

| Item | A: direct PCB PH-2 | B: original PH-3 and breakout |
| --- | --- | --- |
| PCB header | JST S2B-PH-SM4-TB(LF)(SN) | Existing S3B-PH-SM4-TB(LF)(SN) |
| Nominal header envelope | 7.9 mm wide, 9.6 mm total depth, 5.5 mm high | 9.9 mm wide; same nominal depth/height |
| Board power lands | Original VBAT and GND land coordinates and routing retained | All original lands/routing retained |
| Cell replacement | PHR-2 battery unplugs directly | Battery port on an additional harness/adapter |
| Sensor | J8 hand-solder terminals; remains with the reader | Separate sensor spliced into the third harness contact |
| Extra interconnections | No PH-3 breakout | PHR-3, three crimps, branch/splices and genuine PH-2 male port |
| PH-2 male port in B | Not required | PH is wire-to-board; a genuine header normally needs an adapter PCB. An unspecified inline male cable is not a frozen JST part |
| Service and assembly | Fewer battery interfaces; sensor termination and retention still require qualification | Additional continuity, polarity, insulation, pull and space checks; complete adapter dimensions not supplied |
| Release status | Interface built and native-checked; full assembly HOLD | Documented rollback option, not mixed into this canonical PCB or assembly BOM |

Both options retain the same TS temperature and charger timing problems described below. A is preferable because it removes the extra PH-3 breakout and reduces the board header width by 2 mm. B does not solve pack availability, temperature thresholds or the large-pouch cavity. Its additional header/PCB/harness has no demonstrated space advantage. R129 remains preserved for rollback.

J1 is now at `(69.8,94.5)` mm, 90°. Pin **1 = VBAT**, pad center `(66.95,95.5)`; pin **2 = GND**, `(66.95,93.5)`. Viewed from the mounting side, pin 1 is south of pin 2; the header opens toward **+boardX**. Both original power pads and their traces are unchanged. The north mounting bracket moved 2 mm; the south bracket is unchanged. The footprint comes from the official KiCad PH2 geometry, checked against JST's mounting-side drawing. Two silk segments were trimmed for the sensor terminal, and SW6/C12 reference labels moved to clear the new lands.

J8 is **bare PCB, not a purchased connector**. Pin1 TS/MR reuses the original J1 pin3 UUID, location and 3.5×1 mm global copper bar, removes paste, and becomes a manual solder terminal. Pin2 GND is a 1.5 mm land at `(64.8,89.3)` with one 0.25 mm trace and one 0.5/0.3 mm via into GND. Both are excluded from assembly CPL and purchased PCB BOM. Insulated extension tails/strain relief are required; the Semitec strip must not be assumed to be a general flexible cable.

## Battery supply evidence

All three existing Gmail SENT threads were read in the correct account. Each contained one outgoing RFQ, sent **2026-10-11 14:49 UTC**, no reply and no attachment. The incoming search was checked again during this pass and still found no response. No new request, reminder or order was sent. Private mail bodies/IDs are not published in the repository.

| Candidate | Capacity | Published size T×W×L, mm | Status and connector |
| --- | ---: | --- | --- |
| Koosay405381 | 2500 mAh | 4.0×53×81 nominal cell | Catalogue row; zero listed stock when checked. Complete PCM-pack maximum, model-specific current data, certification and lead time pending |
| Polybattery LP405079 | 2000 mAh | 4.0×50×79 nominal cell | Catalogue row only. Detailed specifications on the same webpage describe **LP754460**, so they cannot qualify LP405079 |
| Polybattery LP355380 | 2000 mAh | 3.5×53×80 nominal cell | Alternate already included in the RFQ; supplier confirmation pending |
| Akyga AKY0156 / LP475085 | 2500 mAh | **5.2×51×87.5 assembled maximum**; free leads excluded | Ropla listing showed237 units, MOQ2 at review; availability/quotation not guaranteed. Manufacturer drawing Release1,2024-10-22. **SYP-02T-1,2.54 mm, incompatible with PH2.0** |
| LiPol China LP475085 | 2500 mAh minimum | 4.7±0.3 mm cell thickness | Separate supplier specification; not proof of Akyga pack equivalence. Its current/PCM/connector acceptance is separate |

Keep the 2000 mAh floor and 2500 mAh goal. No lower-capacity substitute is selected. Koosay and Polybattery remain primary thin-pack candidates. Akyga is a documented Poland fallback, requiring a separately qualified SYP-to-PH service adapter or a supplier-built PH2 variant; no lead cutting or polarity assumption is approved. At least one model-specific complete pack drawing and PCM/current/certification response is still required.

## Mechanical evidence

The accepted Git tree had no current registered enclosure STEP/assembly. Historical SCAD used a 59×94 mm board and a40×60×3.8 mm battery; it is not the current model. Native R130 is **59×101 mm, CAD board thickness1.6 mm**. That thickness is not a manufacturer-approved four-layer stackup.

The new native STEP contains the actual PCB and a conservative nominal PH2 envelope. Other component models are absent. The dimensional study uses live RF polygons, pad coordinates and mounting holes, and publishes every provisional wall/boss/gap assumption. See [dimensioned study](../hardware/mainboard/mechanical/BAT_REV3_dimensional_study_R130.png), [mechanical calculations](../hardware/mainboard/mechanical/BAT_REV3_mechanical_audit_R130.json), [conditional STEP](../hardware/mainboard/mechanical/BAT_REV3_conditional_stack_R130.step) and [intentional10mm collision trial](../hardware/mainboard/mechanical/BAT_REV3_10mm_collision_trial_R130.step).

With 0.5 mm plan margins, staying inside the PCB and clear of its RF metal zone leaves **49.75 mm width**. Trial x=26.75 mm keeps foil clear of the native reserved RF polygon, but50/51/53 mm bodies extend beyond this board-contained allowance by0.25/1.25/3.25 mm. These are not case clearance approvals. Assuming5 mm screw bosses plus0.5 mm clearance gives **85.5 mm length** between H2 and H4; Akyga87.5 mm intersects the assumed H4 boss clearance in that trial.

All three candidate pouch plans overlap J1 in XY. A low pouch placed in the shared component space intersects the conservative PH2 reserved envelope. A full-overlay separated stack with the documented display/wall/insulation/sensor/handling assumptions is about **16.03 mm for a nominal4 mm cell**, **17.23 mm for Akyga's5.2 mm pack**. These are scenarios, not measured minimum case thicknesses. A registered enclosure, exact panel/FPC, all body heights, ribs, screws, tolerances and swelling allowances can change the answer. **Actual allowable pack T/W/L is unknown**, so10 mm and complete collision-free fit are not accepted.

## Charger and sensor HOLD

Actual native source remains BQ25185DLHR, R8=18k1%, R9=1k1%, R10=100k:4.20 V, nominal500 mA input and300 mA fast charge. No current increase or timer restart workaround is introduced without qualification.

The downloaded **TI SLUSF65B, revised August2026**, matches the accepted R129 source hash. It specifies a360 min fast-charge safety timer,90 min precharge timer, and CE/input reset after timeout. The optimistic Q/I reference is6.67 h for2000 mAh and8.33 h for2500 mAh, before CV taper/system load/thermal effects. Precharge has a separate timer;1800 mAh is nominal six-hour fast-stage input, not a universal pack-capacity ceiling. Full empty-to-termination charging must be demonstrated, or the current/charger/timer architecture changed. Repeated automatic CE resets are not an accepted solution.

Semitec **103JT-050** is the candidate:10kΩ±1%, B25/85=3435K±1%,≤0.5 mm thickness. Its manufacturer R/T table and the TI TS current/thresholds give a nominal hot entry near **60°C**, not Akyga's maximum **45°C**. The native/analytic guard explicitly detects this mismatch. Positive series/parallel compensation around this current-biased sensor cannot increase the R0/R45 ratio enough to preserve both nominal endpoints. Keeping this sensor requires an independently justified hardware temperature window; a different characterized sensor/charger architecture is another design option. Firmware-only protection cannot qualify unattended OFF-mode charging.

Open/short/displaced sensor, USB-present battery removal, wrong polarity, load peaks and cold/depleted PCM behavior require a safe prototype fixture. A detached sensor reading ambient10k cannot be distinguished electrically from a correctly attached cool cell. Use retained contact and a battery replacement inspection. A persistent TS-ground fault also invokes the documented10s factory-mode sequence on VIN removal; this is an explicit test item. Do not fit a fixed10k simulator as production protection.

JST PH is rated2 A under its specified contact/wire conditions. Battery2500 mAh capacity or2.5 A pack rating does not prove PH2/trace/PCM capability for reader load peaks. Harness polarity, correct AWG/contact/tooling, pull strength and repeated replacement remain unqualified.

## Additional recovered correction and validation

Laird TYS5040 RevA p2 was previously misinterpreted. L2 now uses two1.4×4.2 mm lands at local x±1.85, giving2.3 mm clear gap. A via previously under the enlarged solder land moved from `(56.6,44.8)` to `(57.4,44.8)` with its two existing track endpoints. Annulus clearance is0.30 mm. Actual native mask and paste each contain the two intended windows; the relocated tented via is outside them. The obsolete footprint remains preserved for historical revisions.

The twelve missing manufacturer/MPN fields are now explicit on board and schematic. There are99 purchased parts including2 DNP,97 native CPL rows,19 bare-PCB items. Local full KiCad10.0.7: **ERC0, opens0, parity0, DRC20 only unchanged hole-clearance records, library0**. Seventeen independent guards check native geometry, schematic nodes, actual plots, source preservation, assembly outputs and the known battery limitations. CI success validates engineering evidence, never fabrication readiness. Actual GitHub proof is recorded separately after the source run completes.

All427 original pad UUIDs and2639 original copper items survive. Four original pads change properties, one ground land is added, only three original L2 copper items move, and two sensor ground items are added. Other2636 copper geometries and all other footprint placements survive. Only J1:3→J8:1 and the added J8:2 GND node change the netlist. Global rules, exclusions, USB/SD/EPD/buttons/SW1, inner planes and RF keepouts are preserved.

## Next engineering gates

1. Resolve the real0–45°C hardware window and full-capacity charge cycle before battery-powered prototype acceptance.
2. Register the actual panel/FPC/enclosure and decide a feasible battery cavity/board arrangement using complete pack maximum drawings; retain the2000 mAh minimum.
3. Close supplier replies, PCM trip/current curves, PH2 polarity and replacement harness/retention process. Samples require owner approval before purchase.
4. Close the20 button/USB hole findings through controlled manufacturer/process evidence, plus SW1 datum, panel pin5/FPC,90Ω stackup, stencil/tents/Ceff/EPD pulses and USB/bench tests.

No manufacturing package is released and no components or PCB are ordered.
