# ENKU Base R134 handoff — verified source, NO FAB

Continue in `engineering/r134-usb-control-connector`; open `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Full R133 and earlier source/evidence are preserved. Fixed case-thickness target,59×101×1.6 mm board,2000–2500 mAh thin two-wire PCM pack and separate attached NTC remain requirements.

## Actual current verification

KiCad10.0.7: **ERC0,opens0,schematic parity0,exactly16 active SW3–SW6 hole-clearance errors**, no other DRC findings. **21 independent scopes plus checkpoint comparison pass.** Fresh immutable-source [run38240134929](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38240134929) succeeded on source `c33ef737064422e5a860bce3401c4fea8167daca`; all 12 actual steps. The actual artifact has 41 members/655772bytes, SHA256`173ac5fe710a78427ee0e747d7b6d149eb6d64c46e91dd9fc3148d3151e992c7`; downloaded API digest/CRC and native-export comparisons pass locally and in a separate observer.22 report results match, with only two explicitly checked SVG-title timestamp hash differences. [Full native proof](GITHUB_NATIVE_R134.md).

Canonical PCB SHA256: `07813982c1b4c4f191178a905edb90ecf9f583862de3b648eb4e9da416daa70a`. Later documentation/evidence/checkpoint flags do not change the PCB or schematic. Historical outage/routing-recovery snapshots are not the current source. The generated baseline and immutable verification are separate retained runs; do not claim the generated repair-run input was already this final PCB.

## Implemented

- J5 GCT USB4215-03-A, real no-peg primary-drawing footprint,3.16 mm nominal height, four plated shell slots and unchanged front/mating faceY121 mm. Actual 16 numbered contacts/12 physical paste+mask openings verified; old incompatible model removed. Four old J5 locator findings closed by actual component replacement.
- BQ24072T EN2pin5/VSSpin8 corrected in library and sheet cache. GPIO16/pad9→EN1,GPIO2/pad38→EN2,GPIO38/pad31→CE, via three 1k series/two 2.2k mode pull-downs. Reset/OFF high-Z modelUSB100; USB500/suspend selectable. OFF500 mA and automatic BC1.2/PD are not implemented; loaded GPIO and boot states remain conditional/unqualified. [Signal contract](USB_POWER_CONTROL_R134.md).
- Final legal-width control routing; exact 77 old-copper removals/two EN2 reassignments and 930 untouched parent files verified. Bare TP8 moved to55.5/94.5 mm, mirrored PG label55.5/92.7 mm. Other mounted-core positions, outline, RF keepouts, long USB pair, zone definitions and five filled/capped U3 via requests preserved.
- EN1 command route clears USB signal-via reference copper; actual refilled USB shadow/core missing area0. Continuous U3 B GND spreading grows22.8123→55.3333 mm², meeting the 50 mm² geometry goal without claiming thermal/assembly acceptance.
- Actual assembly features, mask/paste/copper plots, via process, recovered reference/thermal fills, native netlist and107-row CPL/review BOM checked and retained.

## Remaining work and sequence

1. Resolve16 button NPTH-to-copper errors by a real qualified manufacturing process or independently validated replacement; retain active0.25 mm rule and holes/lands until that decision. Check actuator geometry against actual current case.
2. Register the complete current enclosure/component CAD. Resolve PH2/battery collision and connector height while keeping case thickness, capacity minimum and serviceability. The obsolete10 mm reference is not accepted current CAD. Obtain controlled maximum finished-pack dimensions, PCM/current/polarity data and two interchangeable CN/PL procurement SKUs.
3. Review detached sensor/R81-open fault protection, full NTC/input/leakage corners and attachment, effective capacitors, short USB stake soldering, U1/U3 stencil/fill/cap and controlled USB stackup. Current copper area alone does not close these.
4. Implement and review boot/reset/current mode/suspend/CE/MSC firmware and create the exact bring-up fixture. Complete design and factory-process gates before presenting an EVT package; perform physical thermal/charge/USB/fault qualification after boards arrive and before a production release.
5. Freeze accepted source and inspect every generated manufacturing/assembly output. Obtain user agreement before manufacturing or ordering.

[Concrete fabrication gates](DFM_REVIEW_R134.md); [R134 first-board tests](BRINGUP_R134.md). PCBWay-ready manufacturing acceptance remains false; no percentage is invented from zero opens alone.

## Supplier update

Existing three sent requests were read again. Koosay now indicates a 405381 3.7 V/2500 mAh model and requests the maximum battery-compartment envelope including PCM; no exact finished-pack/availability documents supplied. This does not replace the thinner 335084 3.3×50×84 mm engineering target with a thicker cell. Polybattery and Akyga/Ropla still have no incoming technical reply at this check. Original requests describe obsolete BQ25185/300 mA and need current BQ24072T/445 mA parameters in any future authorized follow-up. [Current battery status](BATTERY_STATUS_R134.md). No duplicate query, outgoing message, production or order occurred.
