# Actual GitHub native R133 proof — NO FAB

**Actual KiCad 10.0.7 server results match the committed local R133.** [Successful run 38179847875](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38179847875) on branch `engineering/r133-thermal-process`, event `push`, source commit `6ea561a6000c87cdcc24b0c14e68cc268c80f624`, tree `75a62c3788bc62c9ccd945c1a6664bfdf1e518b4`. Hardware SHA256 `d42f725afb5b597c1403a6a60e04c0d0e87d9821adb5f3cae479183f37bf1b25`. Job 114589893651: all 12 actual job steps succeeded. A later evidence-only commit adds these retained results and does not change the canonical PCB; no second CI run is claimed for it.

| Actual result | Value |
|---|---:|
| KiCad version | 10.0.7 |
| Unconnected items / ERC / schematic parity | 0 / 0 / 0 |
| Active DRC errors | 20 unchanged intrinsic hole clearances |
| Library mismatch warnings | 0 |
| Footprints / pads / copper items | 122 / 442 / 3477 |
| Native fitted CPL / bare PCB / DNP | 102 / 19 / 1 |
| Independent engineering guards | 19 |
| Guard and checkpoint result reports | 20 |
| Actual successful job steps | 12 |

The actual source SHA, native version, exact pad/track/footprint/zone geometry, refilled USB reference and U3 thermal-plane polygons, five native fill/cap requests and assembly/orientation/CPL/review-BOM exports were compared. Electrical netlist sections match; export timestamp/path metadata is not electrical evidence. **18 JSON reports match exactly.** U1-plot and IC-stencil reports differ only in hashes of native plots with different title timestamps. All five F.Mask/F.Paste/B.Mask/F.Cu/B.Cu SVGs match by bytes after replacing only the one validated native export date in their titles. Each original local/server plot hash was checked against its corresponding untouched SVG. No geometry tolerance or DRC rule was relaxed.

Artifact 11716924652, `628643` bytes and 39 members: API digest and actual downloaded ZIP SHA256 `a413f7d10844f56f77a2be8582800a9a1f81da7ee63f5e6f5748d10bab54429d`. ZIP CRC was verified and every member safely extracted. The untouched binary is retained at [native_server_R133.zip](../hardware/mainboard/kicad/checks/native_server_R133.zip). The [machine-readable proof](../hardware/mainboard/kicad/checks/github_native_proof_R133.json), all 20 unchanged `server_*_R133.json` reports and actual API run/jobs/artifact JSON are retained. [Verification script](../hardware/mainboard/kicad/checks/verify_server_artifact_R133.py) checks the retained source commit and bytes; `native_local_R133.zip` contains actual local native results and logs.

This confirms requested geometry and source consistency, not fabricated construction or physical qualification. The continuous B.Cu thermal area remains 22.812 mm² versus the proposed 50 mm² objective. Filled/capped-process approval, actual temperature/thermal/full-cycle charging, USB current-control hardware, effective capacitors, unchanged-thickness enclosure, replaceable CN/PL protected packs, display/FPC/controlled stackup and the 20 hole errors remain open. **fabrication_ready=false.** See [current handoff](WORK_HANDOFF_R133.md) and [DFM draft](DFM_REVIEW_R133.md). No order, manufacturing action or outbound supplier message was made.

Proof capture UTC: 2026-10-11T22:23:00.385351+00:00.
