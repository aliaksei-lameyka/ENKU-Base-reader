# R134 thin battery and existing supplier requests

Checked existing supplier conversations on 2026-10-12. No new supplier message or order was sent. Private message bodies/identifiers are not copied into this public engineering repository.

Koosay has now replied: it indicates a model corresponding to405381,3.7 V/2500 mAh, and asks for the battery compartment's maximum thickness×width×length **including PCM** before verifying specifications and availability. The reply contains no exact finished-pack drawing, stock/lead-time confirmation, PCM/load limits, controlled charge specification or transport documents. It does not approve that model, confirm the thin335084, or establish an interchangeable replacement. Polybattery and Akyga/Ropla conversations still each contain only the existing outgoing enquiry and no incoming technical reply/attachment at this check.

## Fixed-thickness selection

Retain the narrower **335084 nominal3.3×50×84 mm /2000 mAh** as a provisional layout reference. **325381 nominal3.2×53×81 mm /2000 mAh** is0.1 mm thinner but3 mm wider; **LP355380 nominal3.5×53×80 mm /2000 mAh** is the existing second-supplier candidate. None has an accepted maximum finished PCM envelope or guaranteed stock.405381 is nominal4.0×53×81 mm and therefore does not replace the thinner target merely because a supplier answered.

[R131 mechanical study](BATTERY_THIN_SELECTION_R131.md) and [R132 CN/PL supply scan](BATTERY_SUPPLY_R132.md) remain historical evidence. Catalogue stock counts were observed2026-10-11 and were not revalidated by the new email. The wider stocked CN options and Polish3.0×60×74 mm listing are not proven drop-in replacements; the Polish listing's1A limit does not meet the retained2A pulse requirement. No currently accepted pair of finished protected-pack SKUs with China stock and Poland procurement exists.

Board59×101×1.6 mm, antenna reservation, J1 and fixed case target are preserved. The earlier interval study found every feasible50×84 mm nominal cell translation overlaps the current PH2 reservation under its declared boss/RF assumptions. The nominal PH2 top7.115 mm also exceeds the obsolete10 mm-case reference's6.38 mm inner plane; that reference is not registered current enclosure CAD. Replacing USB alone does not solve the battery/PH2 arrangement. Case thickness and the2000 mAh minimum must not be increased/reduced to hide this conflict.

Direct board JST PH-2 plus independent J8 NTC remains the supported electrical interface. Keeping an old three-contact J1 through an adapter adds height/contact/polarity/temperature harness issues and does not resolve the known collision. J1pin1=VBAT/pin2=GND must be verified by a polarity drawing and continuity, not wire color. The separate sensor stays attached to the pouch and isolated from the power leads.

## Next supplier evidence

Register the actual complete enclosure CAD and derive a usable maximum **finished-pack** envelope including PCM, tabs, connector/wire exit, NTC attachment, strain relief, tolerance and swelling allowance. Do not give Koosay an assumed53×85 mm compartment or equate nominal3.3 mm cell thickness with maximum pack thickness. Then continue the existing conversation with the actual target and request the already missing model-specific documents; there is no authorization to send a reply in this pass.

The original enquiries describe obsolete BQ25185/approximately300 mA charging. **Current board is BQ24072T at nominal 445 mA**, with USB100 default and USB500 selectable; any future technical supplier update must use the current limits and4.20 V termination. No correction email has been sent.

Require two procurable finished two-wire1S4.20 V PCM pack SKUs fitting one approved mechanical envelope, controlled minimum capacity and discharge/pulse/PCM data, exact polarity/harness, model-specific transport documents and repeatable CN/PL channels. Current battery, mechanical, supply and procurement gates remain HOLD.
