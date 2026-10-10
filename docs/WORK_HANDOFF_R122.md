# ENKU Base R122 — Q1 Gate/Source geometry correction, NO FAB

Canonical project: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`, branch `engineering/r120-routing-closure`.

R121 closed USB routing, removed 119 obsolete Cu items and passed [actual server KiCad and refilled-ground checks](GITHUB_NATIVE_R121.md). Its subsequent [library triage](LIBRARY_TRIAGE_R121.md) revealed that Q1 Gate and Source pads were mirrored relative to the IRLML6346 manufacturer top view. Native zero-open checks do not detect this physical pin error.

R122 corrects exactly the physical locations of Q1 pads 1/2, preserving their UUIDs, numbers, nets, dimensions and drills. Every other pad geometry and all 117 footprint placements are unchanged; schematics and project rules are byte-identical to R121. Drain pad 3 stays in place.

| Q1 pin | Net | R121 position, mm | R122 position, mm |
| --- | --- | --- | --- |
| 1 / Gate | EPD_GDR | (66, 48.95) | (66, 47.05) |
| 2 / Source | EPD_RESE | (66, 47.05) | (66, 48.95) |
| 3 / Drain | EPD_SW | (68, 48) | (68, 48) |

Primary reference: [Infineon IRLML6346TRPbF datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlml6346-datasheet-en.pdf), pages 1 and 8. Rotating the top view so the single drain lead is on the right confirms pin 1 above pin 2. Existing land dimensions still require assembly qualification.

The short gate branch now uses B.Cu with two 0.60/0.30 mm vias; the source branch stays on F.Cu. The original source testpoint via moves from (66.9,46.9) to (67.1,46.6) to clear the corrected gate land. TP10 itself stays in place on B.Cu. Five obsolete local branches are replaced without changing net names. The first proposal was rejected at a 0.1828 mm drain-to-source-track gap; the corrected bend passes the unchanged 0.20 mm rule. Full native acceptance is required for this batch.

Native KiCad 10.0.7: **0 opens, ERC 0, parity 0, 115 DRC** (111 library footprint mismatches and four inherited USB-C hole-clearance findings), no dangling tracks or vias. The unchanged warnings do not negate the Q1 correction; generic SOT-23 land sizes/shape still differ. [Actual R122 server verification](GITHUB_NATIVE_R122.md) passed: the committed PCB hash, all 402 pads, 117 footprint placements and every track/via match; the Q1 manufacturer-pin guard and actual server-refilled USB reference audit also pass.

PCB SHA-256: `531d5a3dd0f6677f3a71e01f3030522c103bd0b1f6506c7df3fe8be487c5dcd0`. Independent audit of all 81 new or relocated vias and Tag-Connect clearance passes. Actual refilled USB ground still passes with zero missing regions and a clear 1 mm coupled reference strip. A separate Q1 guard verifies manufacturer pin-location mapping and physical continuity of all three nets. These checks run alongside exact native source comparison in CI.

## Remaining release gates

1. Reconcile qualified manufacturer land patterns, beginning with microSD pad orientation, exact SW1 MPN, U1 exposed-pad drills and passive land variants. Review the retained triage; do not replace all 111 footprints blindly.
2. Resolve the four USB-C guide-hole findings and the actual board-factory 90-ohm stackup. Full Type-C contact branches remain for impedance/bench review.
3. Complete display/FPC pin and orientation qualification, enclosure/button fit, assembly controls, power/USB backfeed and USB MSC/SD ownership bring-up.

No fabrication release is issued. Q1 manufacturer pin ordering is corrected; full circuit behaviour and exact land dimensions remain unqualified.

Use `checks/current_checkpoint.json` to select active evidence; decompress its geometry file before local routing helpers. R121 remains the exact tested predecessor. Resume from canonical R122 rather than the older intermediate R121 ZIP.

Saved source commit: `1698fbfa4ce06684c97c8e70e58b18c25e0a8d63`; server run `38086819900`, job `114314954263`, success. Proof-only follow-up commits do not alter this tested PCB. The next pass starts with J2 microSD manufacturer pad orientation and mechanical/pin qualification, then exact SW1 MPN and the remaining footprint/guide-hole release gates.
