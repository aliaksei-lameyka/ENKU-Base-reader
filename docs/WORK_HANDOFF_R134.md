# ENKU R134 native routing checkpoint — NO FAB

Branch `engineering/r134-usb-control-connector`; canonical `enku-mainboard-r0.1` project. Parent R133 proof and every earlier engineering file remain retained.

The recovered and corrected source now has actual KiCad10.0.7 **ERC0,opens0,parity0,exactly16 unchanged SW3–SW6 hole-clearance errors**. Full DRC uses all track errors, schematic parity, zone refill and save. There are no width/dangling/silkscreen warnings. The earlier narrow-route experiment has been replaced with legal0.20mm digital copper; obsolete supply tails are removed.

This is a native routing checkpoint. **The complete R134 independent-guard suite and fresh server CI proof are still pending; neither is claimed by this commit.** `verification_checkpoint_R134.json` retains those false/zero fields. Geometry/DRC/ERC and exact applied routing/probe operations are included.

Implemented: GCT USB4215-03-A/no pegs/lower3.16mm profile, preserved mating face at boardY121mm; real EN2 pin5/VSS pin8 names; GPIO16/pad9 EN1,GPIO2/pad38 EN2,GPIO38/pad31 CE; three1k series and two2.2k mode pull-downs. Reset/OFF high-Z model USB100; USB500/suspend selectable. OFF fast500mA charging and automatic BC1.2/PD detection are not implemented. GPIO voltage arithmetic is conditional; the primary ESP table is3.3V/25C/high-impedance measurement, not a guarantee under our load or over all boot states.

TP8 was moved from[51,87] to[55.5,94.5]mm and connected by a short B trace to the existing PG via[54.25,93.75]. Its mirrored `PG` label is now[55.5,92.7]. This removes the obstructive old B probe branch and avoids extra vias in the dense charger node. Core mounted parts, case/PCB thickness,59×101mm outline, long USB pair, RF keepouts and the five U3 filled/capped requests are preserved.

Next: actual assembly/CPL/mask/paste and reference/thermal/process exports; independent connector/control and all retained audits; finite before/after preservation manifest; fresh GitHub native run and actual artifact verification. Keep NO FAB: button-hole manufacturing process,0.8mm USB shell stakes in1.6mm PCB, whole enclosure fit, effective capacitance/thermal acceptance, detached-NTC protection, battery supply/PCM/harness and firmware/bench qualification remain unresolved. No production, orders or outbound supplier messages.

The prior outage record `routing_recovery_R134.json` is historical; use this checked source and `applied_control_routing_R134.json` for current copper.
