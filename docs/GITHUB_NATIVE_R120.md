# R120 exact native server comparison — MATCH, NO FAB

The final corrected R120 source was saved to `engineering/r120-routing-closure` and checked by GitHub Actions using the exact official KiCad 10.0.7 runtime. The job completed successfully on 2026-10-10. A successful comparison proves source and check reproducibility; it does not waive the remaining fabrication findings.

## Immutable source and evidence

- Source commit: [22727d5e774f9c7755f558b93db4d91113482764](https://github.com/aliaksei-lameyka/ENKU-Base-reader/commit/22727d5e774f9c7755f558b93db4d91113482764).
- Source tree: `53c9daef003619d3631585e8c4cbdad3ca3f4427`.
- Source PCB SHA-256: `e081101868fbd34331c0a4f76a9aaf199b499a9b634e3579cebd7f83bf24818b`, recorded before server zone refill.
- Official runtime SHA-256: `3c6067b03e2e6eb7b3e17f63f6d57c2937a19c39d585edd0c0a8d0bebaec8969`.
- [Successful workflow run 38074970454](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38074970454), job `114279934920`.
- [Native report artifact 11677769393](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38074970454/artifacts/11677769393); ZIP SHA-256 `66999c6a02b7967d57e17de2dd712889bbec0532c110fd0ce6bfc256c2faf083`.
- [Machine-readable server comparison](../hardware/mainboard/kicad/checks/server_comparison_R120.json), copied from the completed job output.

The following documentation-only commit adds this evidence without changing the checked PCB, schematic, project rules or geometry checkpoint.

## Native results

DRC ran with `--severity-all --all-track-errors --schematic-parity --refill-zones --save-board`; ERC ran with `--severity-all`. The comparator checked the committed source hash, all pad identities and geometry, footprint positions/orientations, every track/via identity and geometry, native result counts and existing exclusions.

| Check | Local and server result |
| --- | ---: |
| Pad count | 402 |
| Footprint count | 117 |
| Missing connections | 6 |
| ERC findings | 0 |
| Schematic parity findings | 0 |
| Library footprint mismatches | 111 |
| USB-C guide-hole clearance findings | 4 |
| Dangling tracks | 18 |
| Dangling vias | 8 |
| Other DRC findings, total | 141 |

`server_matches_local_checkpoint` is `true`; `fabrication_ready` is `false`. All six opens are on `USB_DP_CONN` and `USB_DM_CONN`. R119 had 67 opens; R120 accepts 60 routing proposals and also removes verified obsolete copper. The original 400 pad UUIDs, pin numbers, net names, drills and copper layers are preserved; J3 has declared land position/size corrections and two additional paste-only pads.

## Independent local physical audit

The [physical geometry audit](../hardware/mainboard/kicad/checks/physical_geometry_audit_R120.json) applies to the same source PCB hash that the server checked. It was run independently of native DRC and is not an additional GitHub Actions step.

All 67 vias added since R118 were checked against SMD lands. Their minimum annulus-to-land gap is nominally 0.100 mm. Every B-side foreign track/via was checked against the Tag-Connect conductive contacts; minimum clearance is 0.534847 mm against the 0.508 mm requirement. Both violation lists are empty.

This audit caught a C28 GND via whose drill entered its own SMD land by 0.095 mm. The final source moves it 0.450 mm outward while preserving its UUID and net; its annulus-to-land gap is now 0.255 mm. The final native and server comparisons include this correction.

## Next engineering gate

Route the coupled USB pair and connector breakouts, then resolve the remaining DRC findings with pad-connectivity checks. Do not relax the four guide-hole findings or replace mismatched footprints blindly. Controlled impedance/reference planes, display/FPC orientation, vendor footprint qualification, enclosure fit and assembly/bring-up signoff remain open. No fabrication package is released.
