# ENKU R132: thin battery and replacement supply

**No cell/pack is approved and the enclosure must not become thicker.** R131's narrow Koosay335084 is an engineering envelope, not a stocked protected-pack SKU. Keep two-wire, 1S4.20V charging, PCM, a separate attached cell NTC and the2000–2500mAh target. Do not silently substitute 3.8V/HV chemistry or a thicker Akyga pack.

A new primary-catalogue scan on2026-10-11 covers all73 Koosay pages:36,701 rows,319 with advertised2000–2500mAh and thickness≤4mm. **No positive-stock row also meets nominal width≤53mm/length≤85mm.** The retained source register includes page URLs, exact retrieval times, byte counts, SHA256 and every qualifying thin-cell row. A Chinese supplier catalogue quantity is not confirmation of a China warehouse, reserved stock, EU delivery or a finished protected pack.

Dimensions below are advertised T×W×L inmm. The Polish listing describes a finished battery; the Koosay dimensions are catalogue cells without a controlled maximum PCM envelope. Counts are observations, not commitments.

| Candidate/channel | Capacity | Advertised dimensions | Listed stock | Engineering position |
|---|---:|---|---:|---|
| Koosay336080 |2000mAh|3.3×60×80|4458|Best depth of listed supply among this short list;60mm width fails current reservation. |
| Koosay385787 |2500mAh|3.8×57×87|511|Highest capacity; wider and longer than the existing allocation; PCM maximum not known. |
| Koosay366076 |2000mAh|3.6×60×76|797|Shorter large-stock alternative; width remains incompatible. |
| Koosay385570 |2050mAh|3.8×55×70|38|Smallest useful stocked plan in this short list; still2mm wider than the earlier53mm request. Same code also has a2100mAh/54-stock entry; these are ambiguous distinct catalogue rows. |
| Liter Energy Battery306070, innEnergy, Poland |2000mAh|3.0×60×74|38|Thinnest reviewed local purchase listing, seller claims PCM;1A maximum charge/discharge does not qualify the existing2A peak-pack requirement. Width fails current reservation. |
| Koosay335084 |2000mAh|3.3×50×84|0|Retain narrow reference envelope; no stock guarantee. |
| Koosay325381 |2000mAh|3.2×53×81|0|Thin alternative with no positive stock and wider mechanical conflict. |
| PolybatteryLP355380 |2000mAh|3.5×53×80|Unconfirmed|Existing model-specific RFQ; no independent replacement assurance. |

Primary sources and model-specific page mappings: [machine-readable register](../hardware/mainboard/bom/battery_supply_R132.json), [Koosay catalogue](https://koosay.com/pages/lipo-battery-models-1), [Polish seller listing17700608421](https://allegro.pl/oferta/bateria-akumulator-li-po-li-poly-2000mah-306070-3-7v-17700608421), [PolybatteryLP355380](https://polybattery.com/2000mah-lipoly-battery-used-for-hand-held-power-scrubber). Ceneo repeats the Polish Allegro channel and is not an independent supply source. KoosayHV325982 advertises3.8V and is excluded from the4.20V design pending an exact controlled chemistry specification. AkygaAKY0156's approximately5.2mm maximum remains excluded by the unchanged-thickness requirement.

## Fixed-thickness and service decision

Actual board dimensions remain59×101×1.6mm, X18–77/Y20–121. The retained U1 antenna metal restriction ends at X26.25 for Y21–69. The R131 trial origin X26.75/Y28 gives only49.75×85.5mm with its assumed0.5mm edge/boss margins. Thus even the50mm-wide reference misses the right-edge margin by0.25mm. In the native-based continuous-translation study every feasible50×84mm pouch position overlaps the current PH2 reservation. This result remains applicable because U1, outline, bosses and J1 placement are preserved in R132.

The nominal PH2 top is Z7.114998 in the retained native model; an obsolete10mm-case reference assembly leaves only6.38mm to its rear inner plane. That reference is not current enclosure CAD. No taller enclosure, new battery origin or case approval has been asserted. Stocked55–60mm-wide options cannot be called drop-in replacements. Finished-pack tolerances, PCM, wire exit, sensor adhesive/strain relief and ageing expansion must be included in a registered full enclosure before accepting a battery.

**Electrical interface: retain direct JSTPH2 on the board and independent J8 NTC terminals.** Standard replaceable two-wire batteries do not carry the measured cell-temperature signal. A PH2-to-three-contact adapter retains a tall three-contact board header, adds a harness assembly, another contact pair and polarity/temperature wiring hazards; it does not resolve the existing height or pouch conflict. Direct PH2 is the supported electrical architecture; its placement/height are not a mechanical release. Battery harness must document J1pin1=VBAT and pin2=GND by continuity, not by wire colour or an assumed JST polarity. NTC is electrically isolated from the battery leads and physically attached to the pouch.

## Supply gate and supplier threads

The Koosay, Polybattery and Akyga/Ropla existing sent requests were already checked in R130/R131. A fresh incoming-mail search found no replies during this pass. No request was duplicated, no new email was sent and no component was ordered.

To accept two independently procurable alternatives, require controlled maximum finished-pack drawings under the fixed case ceiling, minimum/rated capacity,4.20V charge specification, PCM trip limits and load pulse capability, exact harness/polarity drawing, supplier SKU, verified China stock and Poland purchase channel, minimum order and transport documents. Confirm dimensions against complete current enclosure CAD. Catalogue evidence alone fails this gate. Prefer two protected-pack SKUs that fit one mechanical reservation; the common PH2 interface alone does not make their envelopes interchangeable.
