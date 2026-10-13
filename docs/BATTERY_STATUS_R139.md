# ENKU Base battery review -13October2026

Full existing battery threads and latest received messages were read from the project account. No outgoing mail, duplicate request, order or battery approval. Private quotes, original attachments, raw mail bodies and contact details are excluded from public source.

| Supplier/model | Dated evidence | Decision |
| --- | --- | --- |
| Polybattery/Lipoly Batteries LP405079 |13Oct04:02UTC:4x50x79mm model unavailable; no technical drawing/alternative offered | Exclude from presently procurable candidates |
| Polybattery LP355380 |Same reply:3.5x53x80mm model unavailable | Exclude from presently procurable candidates |
| Polybattery LP754460 |Same reply:7.5x44x60mm model unavailable | Unavailable and too thick |
| Koosay4053812500mAh |Last incoming12Oct03:37UTC discusses matching model. Our existing12Oct18:59UTC follow-up asks exact PCM/tolerance/PH2/stock/drawing details; no later incoming reply found | Candidate; finished envelope/stock/qualification unconfirmed; do not duplicate follow-up |
| Akyga/Ropla AKY0156/LP4750852500mAh |Existing12Oct12:02UTC reply states237 stock then, protected max5.2x51x87.5mm,150mm leads,SYP02T1/2.54mm; no comparable thin standard-stock option offered; no new reply | Rejected for thickness |

Ropla's polarity photo has now been inspected: marked protected LP475085, red/black leads, red connector. Mating-face/cavity numbering is not sufficient to assign an ENKU PH-2 map. It does not replace a numbered harness drawing or continuity verification. Original image remains private; no new polarity approval.

Five existing Ropla PDFs were reviewed in R136; no replacement attachments arrived. [Retained hashes/technical findings](../hardware/mainboard/bom/battery_supplier_review_R136.json). Finished-envelope, older transport-tested sample and current configuration still need exact mapping. No new certification or alternate-harness approval is inferred; quotations are excluded.

Requirements remain: finished two-wire1S PCM LiPo,2000-2500mAh,standard4.20V chemistry,about4mm and **no case thickening**; direct PH-2 J1pin1 VBAT/pin2 GND with a documented harness; independent attached NTC at bare J8 pads; two interchangeable controlled pack models with reliable China/Poland sourcing. Maximum dimensions include PCM/insulation/tabs/wire exit/connector/tolerances/swelling/retention and must fit current complete case CAD. Charge/discharge/pulse/temperature/document configuration need approval.

The12Oct4.0-4.5x<=53x<=85mm supplier target is provisional, not approved case space or permission to thicken. R132 catalogue quantities are historical; LP405079/LP355380 now have explicit negative supplier availability. Previously scanned55-60mm-wide alternatives still fail the old allocation and are not drop-in packs. No new positive-stock scan/reservation was performed in this mail review.

Original RFQs describe obsolete BQ25185/~300mA. Actual board: BQ24072T,445mA nominal, modeled max492.42mA/BAT max4.24V, external10k B3435 NTC. Any future authorized follow-up must use current values; none is sent here. Thin-pack pair and mechanical fit remain HOLD.

## Related display reply

The13Oct Good Display response concerns **Pro** GDEY0426T82-FL01C: independent warm/cool channels may operate together; e-paper/frontlight has no touch layer. New drawing/reference-circuit links were supplied but not qualified here. Free samples were declined. This does not add frontlight to Base or close Base's physical panel/FPC/connector/CAD checks.

Older10Oct Base correspondence already clarifies VDHR/VSH2 pin5 wording and gives bend/clearance guidance. The open task is matching actual controlled drawings and physical fit; do not repeat the same answered question.
