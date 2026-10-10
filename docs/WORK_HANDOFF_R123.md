# ENKU Base R123 — manufacturer geometry pass, NO FAB

Canonical source: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`, branch `engineering/r120-routing-closure`. Continue from R123; R122 is the server-verified predecessor. Base scope remains 59 × 101 mm, four side buttons; Pro has a separate PCB.

## Changes and evidence

The board's J2 microSD lands already matched the reviewed mounting-side layout. Fourteen rectangular pads in the project-local footprint had their orientation rotated relative to the board. R123 normalizes that library from the checked native instance without altering any J2 copper; its native mismatch disappears.

For SW3–SW6, the old trial omitted two bracket solder lands per switch and the circuit-trace keepout, and had incorrect nominal contact sizes/offsets and locator pitch. The reviewed E-Switch P021301 rev B / TL3340AF160QG interpretation is now present on all four instances and in the local footprint. It adds eight unnumbered solder lands and four F.Cu keepouts prohibiting tracks, vias and zone fills. The two locators per switch retain the existing 0.90 mm NPTH interpretation, with corrected 4.25 mm pitch. This interpretation and tolerance stack still require manufacturer/assembler qualification.

Terminal 2 is internally common with terminal 1. Its schematic library pin was incorrectly typed as internal No Connect. It is now a passive duplicate common terminal, with four explicit external No Connect markers; its unused PCB net labels follow the corrected name. The functional button/GND nets are unchanged. Contact/locator UUIDs and all 402 original pads remain; total is 410 pads and 117 footprints.

Affected local routes reconnect the shifted lands. C18 moves 0.40 mm to clear the revised SW3 locator. Ten obsolete BTN_R2 F.Cu segments are replaced with a short B.Cu escape and two vias. The existing BTN_L2 via moves 0.80 mm out of the expanded solder land, with its two adjacent track endpoints updated. The original nearby GND stitching via retains its original net and geometry. Full source-preservation evidence declares every exception and checks surviving copper nets, physical pad partitions, unrelated schematic sources and unchanged rules/exclusions.

Local native KiCad 10.0.7 with all severities, all-track errors, zone refill and schematic parity: **0 opens, ERC 0, parity 0; 130 active DRC findings = 110 library mismatches + 20 hole clearances**. Four USB guide-hole findings are inherited; sixteen are intrinsic to the revised button contact/bracket lands versus the interpreted locator holes. Button nominal gaps are 0.075 / 0.150 mm against the unchanged global 0.250 mm rule. No waiver has been added. Routing shorts, track-clearance, dangling and mask-bridge findings are zero.

Independent audits pass for 83 new/relocated vias and Tag-Connect clearance. All 281 board vias are additionally checked against the revised solder lands (minimum annulus-to-land gap 0.150 mm). The actual locally refilled USB ground remains continuous, with zero missing core reference area; Q1's R122 manufacturer pin-order correction remains verified. These are geometry checks, not controlled-impedance or assembly qualification.

Use `checks/current_checkpoint.json` to select active reports. Compressed native geometry contains pad shapes, attributes, physical polygons and zone/keepout flags. Source/source-file preservation evidence, exact PDF identities/hashes and library triage are committed alongside source. For local routing tools, decompress the active geometry to `checks/geometry_current.json` first. Native loading may rewrite project metadata; retain the committed project settings before source preservation comparison.

[Actual R123 server validation](GITHUB_NATIVE_R123.md) succeeded. The CI workflow independently refilled the board, ran full ERC/DRC, exported native geometry and actual ground, checked manufacturer/button geometry and Q1 pins, and compared source geometry and exclusions exactly. Local server-mode format validation is not counted as server verification. [Remaining work](REMAINING_TO_BUILD_R123.md) lists the manufacturing gates and the prototype bring-up separately.

No fabrication release, assembly package or ordering authorization is implied by a source-comparison pass.

Saved and tested source commit: `478c9d79ab9cfc5da338de1634b2f62466f9f3ff`; server run `38089955370`, job `114324173453`, success. Proof-only follow-up commits retain the tested PCB unchanged. Next priorities are button locator/hole qualification and exact SW1 MPN, then USB hole/stackup, FPC and assembly/mechanical gates.
