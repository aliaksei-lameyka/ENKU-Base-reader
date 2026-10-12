# R134 actual native source and artifact proof

**Immutable source verified; NO FAB.** KiCad10.0.7 ran on [source commit `c33ef737`](https://github.com/aliaksei-lameyka/ENKU-Base-reader/commit/c33ef737064422e5a860bce3401c4fea8167daca). [Actual native run 38240134929](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38240134929) completed successfully; all 12 actual job steps succeeded. All 21 independent scopes plus checkpoint comparison passed.

The preceding [native repair run38236038134](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38236038134) generated the final EN1 command route with extra clearance from USB signal vias, then retained the source, native baseline and21 guard results. Its input differs from the generated PCB, so it was not used as immutable-source proof. A later source commit changed only workflow mode to VERIFY. The verification run did not repair routes, generate guards, regenerate manifests, freeze a checkpoint or publish a modified PCB.

| Identity or result | Value |
|---|---|
|Verified source commit|`c33ef737064422e5a860bce3401c4fea8167daca`|
|Verified source tree|`c7272c0f3dd58180dfed30edf198e9f5ff97422d`|
|Canonical PCB SHA256|`07813982c1b4c4f191178a905edb90ecf9f583862de3b648eb4e9da416daa70a`|
|Actual job ID|`114780403029`|
|Actual artifact ID|`11742127236`|
|Actual ZIP size/members|655772 bytes /41 members|
|Actual ZIP SHA256|`173ac5fe710a78427ee0e747d7b6d149eb6d64c46e91dd9fc3148d3151e992c7`|
|KiCad ERC /unconnected /schematic parity|0 /0 /0|
|Active DRC|16 hole_clearance, all unchanged SW3–SW6 findings|
|Report results|22 total;20 exact JSON matches and2 validated SVG-title timestamp hash differences|
|Fabrication release|False|

The artifact was actually downloaded, checked against the GitHub API binary digest and byte count, CRC-tested, safely extracted and independently compared locally. An isolated [artifact observer proof](../hardware/mainboard/kicad/checks/github_artifact_observer_R134.json) separately downloaded and verified the same bytes. Their source/run/tree/artifact identities match. Proof capture: `2026-10-12T11:08:28.243242+00:00`.

All five actual F.Mask/F.Paste/B.Mask/F.Cu/B.Cu SVG geometries match the retained generated native baseline after replacing **only one SVG title export timestamp**. The differing U1 plot/IC stencil report hashes are validated against each actual raw SVG, not ignored generically. Native geometry, recovered reference and thermal fills, individual via-process requests, assembly features, orientation, native CPL/review BOM and source project file match. Netlist components/libparts/nets match exactly; export date/tool path are outside those electrical sections.

The preservation guard independently checks930 unchanged R133 repository files, unchanged outline/stack/RF/zones/core placements,77 finite authorized old-copper removals, two exact EN2 escape reassignments, five new resistor placements and the single declared bare TP8 move. Old20-contact-pad UUIDs are retained across the real J5 footprint replacement, with two old locator pads removed. No severity, exclusion or clearance rule was weakened.

Actual USB refilled reference-shadow missing area is0; minimum coplanar USB-to-new B GND spacing is1.0088 mm. The continuous B-side U3 GND spreading region is55.3333 mm²; this is a geometry result, not an accepted temperature or process result. CPL includes 107 fitted parts, excludes 19 bare PCB items and R67 DNP, and has no missing fitted MPNs. Suppliers have not approved CPL origin/rotation for assembly.

Retained evidence: [full proof](../hardware/mainboard/kicad/checks/github_native_proof_R134.json), [checkpoint](../hardware/mainboard/kicad/checks/verification_checkpoint_R134.json), [actual native ZIP](../hardware/mainboard/kicad/checks/native_server_R134.zip), [generated baseline ZIP](../hardware/mainboard/kicad/checks/native_local_R134.zip), API run/jobs/artifact metadata and all 22 `server_R134_*.json` reports. [Reproduction script](../hardware/mainboard/kicad/checks/verify_server_artifact_R134.py) compares the safely extracted generated baseline and actual verification directory, with the retained API metadata. Later metadata/document commits preserve the identical canonical PCB SHA; the verified source identity stays explicit above.

Native success does not waive the16 button-hole errors or the battery/enclosure, NTC, thermal, USB, firmware, assembly and supply holds. [R134 fabrication review](DFM_REVIEW_R134.md). No manufacturing, purchase or outbound supplier message.
