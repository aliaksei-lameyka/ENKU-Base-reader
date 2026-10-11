# ENKU R133 engineering handoff — NO FAB

Branch: `engineering/r133-thermal-process`. Open `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`; the active checkpoint selector is R133. Canonical PCB SHA256: `d42f725afb5b597c1403a6a60e04c0d0e87d9821adb5f3cae479183f37bf1b25`.

**Actual local KiCad 10.0.7: 0 opens, ERC 0, schematic parity 0, exactly the same 20 hole-to-copper errors, no library mismatch.** All 19 independent engineering guards and the native checkpoint comparison pass. Board 59 × 101 × 1.6 mm; 122 footprints, 442 pads, 3477 copper items. Assembly remains 102 fitted CPL rows, 19 bare PCB items, R67 DNP and 103 explicit MPN fields including DNP. Local native exports/reports and all 20 check logs are retained in `checks/native_local_R133.zip`. Current server verification is pending publication; the R132 CI run is historical evidence only.

## Completed engineering changes

The previous U3 layout had no through-board thermal-via array beneath its exposed pad. R133 adds five 0.30 mm drill / 0.50 mm land GND vias: center X48.50/Y91.00 mm and four points at ±0.58 mm in both axes. The locations follow TI's RGT example; its 0.20 mm drill is adapted to the existing project drill constraint. KiCad contains explicit resin-fill and copper-cap requests, front exposed metal and bottom tenting. These are required fabrication construction requests, not evidence that a supplier has approved or manufactured the process. Copper/mask EP 1.68 mm and paste 1.55 mm, rounded corners 0.05 mm, remain exactly unchanged. The SVG contains the original EP mask plus five fully contained via-circle primitives; the measured physical union is still one unchanged opening.

CHG_STAT1/STAT2, CHG_ILIM_VSET and local VBAT copper were rerouted around the array. STAT2 no longer cuts the new spreading zone on B.Cu. Two front GND connections and one solid-connect B.Cu GND zone were added; native checks were rerun after pruning actual dangling ends. The new zone's actual minimum coplanar separation from the original USB copper is 1.00878 mm; the original USB pair and actual inner reference-plane guards still pass.

Actual refilled B.Cu has **22.812 mm² in the continuous region touching the EP**, not the sum of disconnected regions. The internal center-connected regions are 8.057/9.442 mm², with EP shadow GND coverage 97.995%/100%. The proposed 50 mm² continuous B.Cu objective is **not reached**. This is measured progress, not accepted heat spreading, a thetaJA specification or a qualified full charge cycle. Further layout/thermal work stays open.

The temperature analysis now uses the nominal Semitec table and explicitly labels the table-scaled R25/B corner exercise as a scenario, not a guaranteed R/T tolerance band. For those scenarios, only about 0.267/0.289 µA absolute TS input leakage can be tolerated at 0/45°C; a guaranteed TI TS leakage bound was not found. The analysis identifies **R81 open at 45°C** and **a detached sensor reading room temperature** as cases that can allow charging. Model checks pass because they retain these failures and HOLD status; the circuit is not described as fail-safe. See [temperature/timer analysis](TEMPERATURE_AND_CHARGE_R133.md).

Another pre-existing issue is now explicit: EN1=VBUS, EN2=GND and CE statically low select USB500. **The present hardware cannot select USB100 or suspend in firmware.** Resolve the hardware control/default behavior before implementing host current policy. No firmware source or actual USB power test is present in this tree.

## Source preservation

Parent: accepted R132 proof commit `dc56ab0c9a5b9a130fa5418b008c7f7af94c717f`. Strict preservation checks retain 874 parent repository files unchanged, every R132 footprint/pad/position/assembly field, electrical netlist, board outline/thickness, original zones/RF restrictions/rules/exclusions, 3115 R132 copper items and every surviving original R130 copper item. Exactly 29 declared local R132 copper pieces were removed and 362 bounded pieces were added, plus one new B.Cu zone. The same 20 DRC findings are compared by type/severity/description/item UUIDs. Schematic and libraries are unchanged. Old R132 evidence remains intact.

`apply_thermal_R133.py` is the one-time initial array proposal against the exact parent, not a script to rerun on this finished source. `route_charge_R133.py` generates heuristic route proposals, which always require actual native refill/DRC and independent geometry checks. Open the canonical checked PCB.

## Fixed thickness and battery availability

No case thickness, PCB thickness, connector placement, pouch location or mechanical body was changed. Direct horizontal JST PH-2 and separate J8 NTC remain the selected electrical architecture. The full current enclosure, PH2/pouch/boss/RF margins and finished protected-pack maximum dimensions are still unqualified.

[Retained battery supply register](BATTERY_SUPPLY_R132.md) includes thin stocked Chinese catalogue candidates 336080, 385787, 366076 and 385570, and the Polish 306070 listing. Those historical stock observations are not reservations or a guaranteed interchangeable CN/PL pair. The narrow 335084/325381 were listed at zero stock; the Polish candidate's width/current specification did not qualify the existing contract. No protected pack is selected for release and no thicker case is accepted. Existing Koosay, Polybattery and Akyga/Ropla RFQs were not duplicated; no outbound email, order or manufacturing action occurred.

## Remaining release gates

| Gate | Next concrete work | Status |
|---|---|---|
| Thin replaceable pack and enclosure | Controlled maximum finished PCM-pack drawings, two procurable CN/PL alternatives, 2A peak/polarity/connector contract, full current case/panel/FPC assembly at unchanged thickness | HOLD |
| USB current control | Select hardware-driven EN1/EN2/CE control and safe defaults; implement host/suspend policy and test inrush/backfeed/OFF behavior | Existing hardware cannot switch modes |
| Cell temperature | Guaranteed sensor R/T and TS leakage, single-fault response decision, sensor attachment and chamber tests | FMEA scenarios incomplete for guaranteed acceptance |
| Charger thermal/timer | Increase/justify continuous copper, validate filled/capped process, effective C7/C8, measured case temperature and complete 2000–2500mAh charge | 22.812 mm² versus proposed 50 mm²; untested |
| Intrinsic holes | Factory-specific registration/NPTH process acceptance or a real component replacement; no clipped lands or DRC waiver | Same 20 errors |
| Display/USB/process | Exact panel/FPC confirmation, actual 90-ohm stackup, U1/U3 stencil/reflow/voiding, final BOM/CPL/output review | HOLD |
| Bring-up and firmware | PGOOD/CHG contract, USB MSC exclusive SD ownership, sequenced power/fault/USB tests with recorded actual evidence | Planned, not performed |

[Fabrication review draft](DFM_REVIEW_R133.md) is complete for review and **was not sent**. [Existing bring-up matrix](BRINGUP_AND_FAULTS_R132.md) remains a plan. Prototype purchases/manufacturing require user approval. Passing native checks does not release this board to PCBWay.
