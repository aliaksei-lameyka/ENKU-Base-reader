# ENKU Base R120 — engineering checkpoint, NO FAB

Canonical project: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Working branch: `engineering/r120-routing-closure`.

R120 recovers the routing pass from the exact server-verified R119. It accepts 59 routing proposals, reducing native missing connections from 67 to 6. All 400 original pad UUIDs, pin numbers, net names, drills and copper layers are preserved; all surviving copper retains its net name. The dedicated Base scope remains four side buttons, microSD and native USB MSC; Hall, frontlight, Qi and Pogo/Dock are outside Base.

Native KiCad 10.0.7: full DRC with `--severity-all --all-track-errors --schematic-parity --refill-zones --save-board`, ERC with `--severity-all`. ERC 0, parity 0. Project rules and schematics are byte-identical to R118. No new copper clearance or RF keepout violations were introduced. DRC findings remain:

| Type | Count |
| --- | ---: |
| hole_clearance | 4 |
| lib_footprint_mismatch | 111 |
| track_dangling | 18 |
| via_dangling | 8 |

The server comparison at commit `4d8abd587b8d5464e6282d4e13699d85c55c5f29` proved R119 geometry and native results matched the local source; this R120 checkpoint is locally verified. Passing source comparison does not imply fabrication readiness. Source PCB SHA-256: `4c80264d8aefade8c92d15ce819aa6842261ebc7db9f56756b36db308d9dd576`.

## Remaining missing connections

- Pad A6 [USB_DP_CONN] of J5 on F.Cu ↔ Pad B6 [USB_DP_CONN] of J5 on F.Cu
- Pad B6 [USB_DP_CONN] of J5 on F.Cu ↔ Track [USB_DP_CONN] on F.Cu, length 2.3000 mm
- Pad 1 [USB_DP_CONN] of U8 on F.Cu ↔ Pad 1 [USB_DP_CONN] of R64 on F.Cu
- Pad 1 [USB_DM_CONN] of R65 on F.Cu ↔ Pad 3 [USB_DM_CONN] of U8 on F.Cu
- Track [USB_DM_CONN] on F.Cu, length 2.3000 mm ↔ Pad B7 [USB_DM_CONN] of J5 on F.Cu
- Pad B7 [USB_DM_CONN] of J5 on F.Cu ↔ Pad A7 [USB_DM_CONN] of J5 on F.Cu

## Continue

1. Reserve a coupled USB corridor and route low-frequency/power crossings around it. The two series resistors are beside GPIO19/20, and USBLC6 has front-to-back D+/D− flow-through. Do not accept two independent long meandering data tracks. Actual 90-ohm geometry requires the PCBWay stackup and a reference-plane fill audit.
2. ESP_EN to the bottom Tag-Connect contact is closed by the accepted 8.666 mm service route; its source via stays outside the probe contact. The isolated EPD_VGH remnant and obsolete BOOT leaf stub are removed. Before pruning any further dangling copper, verify that every previously connected pad group remains connected; removing a flagged segment can expose another missing connection.
3. J3 land-pattern correction applied: True. The supplied Hirose EDC-159714-50-08 drawing, page 1, calls for 0.8×0.8 mm reinforcement copper, 0.25×0.65 mm signal stencil apertures and 0.8×0.65 mm reinforcement apertures. The isolated correction script shifts J3 0.1 mm left to retain edge clearance. It must pass a full native check and declared pad/copper identity audit before promotion.
4. Independently audit all new via annuli against SMD lands and the Tag-Connect 0.020-inch foreign-copper clearance. Preserve existing rules and exclusions; do not waive the four USB-C guide-hole findings or blindly replace library-mismatched footprints.
5. Keep the FPC/display orientation and enclosure fit as a separate open qualification item. The user is designing the enclosure; this pass does not settle the top connector versus bottom FPC pocket.

## Durable continuation

The previous local R120 pass was lost when the scratch environment refreshed. Recover from this committed source, not from an unsaved local pathname. Stop all local writing processes before GitHub connector mutations; these may synchronize the workspace. Freeze source and evidence outside the git checkout, then upload that immutable snapshot. Keep R119 and its CI evidence intact. Avoid repeated intermediate Actions runs.

`checks/current_checkpoint.json` selects the active revision for the exact-version native CI comparator. Decompress the committed geometry JSON before running local routing helpers. Only native-accepted plans may replace the canonical PCB. No fabrication package is released.
