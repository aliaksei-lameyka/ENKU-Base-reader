# ENKU Base R121 — USB routing closure, NO FAB

Canonical project: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Working branch: `engineering/r120-routing-closure`.

All six R120 missing connections are closed. Native KiCad 10.0.7, full severity, all track errors, actual zone refill and schematic parity: **0 opens, ERC 0, parity 0**. No dangling tracks or vias remain. The remaining 115 DRC findings are 111 library footprint mismatches and four inherited USB-C guide-hole clearance findings. These are retained, with unchanged rules and exclusions. Server verification of this exact checkpoint is pending.

PCB SHA-256: `8cdf268088804783025f1b2c30bced9006c847b6ac5e597bf6925b483b7d2efa`. All 402 R120 pad geometries, all 117 footprints and placements are identical; every surviving copper UUID retains its net. The original 400 electrical pad identities remain preserved. Schematics, project settings and rules are unchanged from the durable source. Base remains 59 × 101 mm, four side buttons, microSD and native USB MSC. Hall, frontlight, Qi and Pogo/Dock remain outside Base.

## Physical changes and evidence

The USB-C A6/B6 and A7/B7 duplicates have a local F.Cu breakout with no data vias. The long pair uses B.Cu with 0.20 mm track width and 0.20 mm gap, two signal vias per net, and nearby GND return vias at layer transitions. Six crossing low-frequency or power nets were rerouted around the pair; the accepted SD clock route is about 52.7 mm with its original series resistor retained. Local VBUS/ESD feed routing was rebuilt.

The cleanup removes 119 obsolete Cu elements in two guarded batches (80 + 39) and trims four live pass-through tails to actual junctions. Each removed element was checked against all previously connected pad groups; final native DRC confirms zero opens. A flagged dangling segment can still carry a needed pass-through connection, so blindly deleting every flag is unsafe.

The filled-plane audit found cuts below F.Cu USB caused by BTN_R1 and CC1, plus an isolated MCU ground island. The short BTN_R1 escape and CC1 were moved to In2 outside the B.Cu USB corridor, the MCU island received a GND stitch, and the DM fan-in shifted 0.02 mm clear of a foreign antipad edge. The full USB trace projection now stays over filled GND outside declared own signal-via antipads; the whole coupled core has a clear 1 mm reference strip. Native polygons are unfractured before testing real holes, rather than treating fill fracture seams as physical ground gaps.

The independent land/contact audit checks all 78 surviving vias added since R118 against SMD lands, including their own-net lands, and all foreign B-side Cu against Tag-Connect contacts. Both checks pass. The retained C28 correction provides 0.255 mm annulus-to-land clearance. The USB audit verifies MCU polarity, resistor nets, USBLC6 flow-through pin mapping and both connector contact orientations.

## USB limitations retained explicitly

Resistor-to-ESD centreline lengths: D− 53.351 mm; D+ 53.115 mm. Difference approximately 0.236 mm. This does not establish equal complete connector paths: the A-contact branch skew is -2.915 mm and B-contact skew 1.002 mm. The measurement excludes pad spreading, package/via delay and an electromagnetic stackup model. Width/gap are engineering geometry; factory 90-ohm impedance remains unqualified.

## Next release gates

1. Reconcile the 111 library mismatches against actual land patterns and manufacturer MPNs, keeping intentional/custom copper only with evidence. Never replace all footprints blindly or waive mismatches merely to reduce the count.
2. Resolve the four manufacturer USB-C guide-hole findings with the selected vendor footprint and board-fabricator rules.
3. Confirm the actual stackup and USB impedance, review both contact branches, then verify USB MSC, hotplug, OFF/backfeed and SD ownership on hardware.
4. Complete display/FPC pin and orientation qualification, button/connector mechanics, enclosure fit and assembly checks. The user designs the enclosure; top connector versus bottom panel FPC remains open.

The source is an engineering checkpoint, not a fabrication release. No Gerber/BOM/assembly release is issued.

## Reproduce and continue

`checks/current_checkpoint.json` selects the active revision for CI. The workflow installs the SHA-pinned official KiCad 10.0.7 image, runs full DRC/ERC/netlist, exports actual refilled ground polygons and runs `audit_usb.py` on the server geometry. It then compares every committed pad, footprint and track/via geometry plus native counts and exclusions. Passing the source comparison does not waive fabrication findings.

For local routing helpers, decompress `checks/geometry_checkpoint_R121.json.gz` into `checks/geometry_current.json`. The physical audit uses the committed R120 geometry and its preserved via audit as the baseline. The R121 source was recovered from the GitHub zero-open ZIP after a workspace reset; all last changes are now in the declared, native-accepted `accepted_r121_closure.json`. Prefer this canonical source over the older intermediate ZIP. Stop local writers before connector synchronization, and freeze uploads outside the checkout.
