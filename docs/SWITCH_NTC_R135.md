# R135 switch and TS design decision

Engineering candidate; NO FAB. Actual local KiCad10.0.7 DRC0/ERC0/opens0/parity0,22 independent scopes and checkpoint comparison pass. Source/assembly/factory/firmware/physical acceptance remain separate. Fixed59×101×1.6mm PCB, case-thickness ceiling and2000–2500mAh thin two-wire PCM pack with attached separate NTC are unchanged.

## Side buttons

Use E-Switch **TL1016AAF160QG**, the actual AA variant without bosses or a ground terminal. Manufacturer P520001 RevA release28Apr2022, drawing header12Apr2022, SHA2569f1097ea8591bbf730ee905ba186e0c6c0d48cfc573395d0ab7f9704a20e5a75. The configurator explicitly distinguishes A=no bosses and B=with bosses; do not procure TL1016BA/BB as substitutes. Actual terminal references1/2 are common A,3/4 common B. All four distinct pads are externally routed, with no virtual jumper or unused-contact exemption.

Nominal drawing land envelope5.00×2.50mm, inner gaps2.20×0.40mm, four1.40×1.05mm pads centeredX±1.80/Y±0.725mm. Independent native copper and actual F.Mask/F.Paste checks confirm four physical windows per switch,5.88mm² per switch/layer. No holes are invented or removed from the same component: the old TL3340 is replaced by a real no-boss component. The0.25mm board hole-clearance rule and all previous exclusions/severities remain unchanged.

TL6340 was reviewed but uses a different bracket/stake arrangement and actuator geometry; Würth436333033816 retains boss holes and does not eliminate the old class of manufacturing conflict. These are not automatic drop-ins. The TL1016 exact configuration is listed by the manufacturer and DigiKey/Mouser channels; distributor search snapshots are not reserved stock or a verified China warehouse. Current local seller endpoints denied retrieval, so no live stock/delivery guarantee is claimed and no purchase occurred.

Old TL3340 body height3.30mm; new nominal body height1.35mm. Button Y locations remain73/85mm. The new footprint moves X inward0.05mm per side; nominal tip planes stayX19.45/75.55mm using the old2.05mm peg-to-tip datum and new2.10mm center-to-tip geometry. Actuator changes from round to rectangular, vertical axis changes, and the new160gf force tolerance is+70/-40gf with0.20mm +0.2/-0.1 travel. The case's internal pusher, stroke stop, side load and assembly tolerances must be revalidated within the unchanged external thickness. This is not a mechanical drop-in approval.

Finite local routing removes20 old copper items: obsolete button-ground terminal branches and one3V3 straight segment. One old3V3 segment receives a declared0.1mm jog;27 new copper items provide explicit paired contacts, eight ordinary tented ground vias and restored C18/microSD ground links. Independent preservation checks cover1038 untouched R134 files and every other physical pad/core placement, the original outline/stack/RF/non-switch zones, long USB pair and charger thermal-via requests.

## NTC resistor-open fault

R80 changes31.6k→40.2k1%, Yageo RC0603FR-0740K2L; R81 changes19.6k→33.2k1%, RC0603FR-0733K2L. Pad geometry, placement,10k1% Semitec103JT-050,100k series R82, charger/current/timer and external J8 interface remain unchanged.

The old R81-open at45°C model yielded TS/VIN0.13446, inside a possible charging window. With the new bias it is below the most conservative0.12 hot threshold. In the stated table-scaled R25/B/resistor/source scenarios, the modeled absolute TS-leakage budget for this fault is350.9nA and the250nA scenario inhibits. This is an analytical correction of the identified resistor-open fault; actual guaranteed full sensor R/T envelope and TI TS leakage are still missing.0.5µA is not certified merely because0.25µA passes.

**Nominal healthy charge window becomes4.90–35.01°C**, more conservative at the hot end than the old4.59–39.74°C. Threshold/resistor/B corner ranges are retained in the actual charge report.25°C remains allowed; modeled0/45°C, sensor open/short and R80 open/short/R81 short inhibit. A sensor physically detached from a hot pouch still appears electrically valid. R82 open/fault isolation, sensor voltage miswiring/clamping, full R/T/leakage, attachment lag and bench tests remain HOLD. Do not claim every single fault is fail-safe or that PCM supplies temperature protection.

Nominal445mA fast-charge setting,8.725h timer, USB100 reset/OFF model and GPIO16/2/38 mode/CE controls are unchanged. Thermal/full-charge/loaded GPIO/USB/firmware qualification remains outstanding. Thin battery and CN/PL replacement supply are still governed by BATTERY_STATUS_R134.md; Koosay's request for a real maximum compartment envelope does not approve a thicker pack.

Primary sources: [TL1016 exact manufacturer configuration](https://www.e-switch.com/product/tl1016-series-subminiature-smt-right-angle-tactile-switch/?part-number=TL1016AAF160QG), [P520001 drawing](https://configured-product-images.s3.amazonaws.com/2D/specs/TL1016AAF160QG.pdf), [old P021301B](https://configured-product-images.s3.amazonaws.com/2D/specs/TL3340AF160QG.pdf), [TI SLUS937C](https://www.ti.com/lit/ds/symlink/bq24072t.pdf). Only constants/provenance are retained; proprietary manufacturer drawing files are not republished in the repository.
