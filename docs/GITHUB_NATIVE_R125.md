# Actual native KiCad R125 proof

[GitHub Actions run 38093887054](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38093887054) completed **success** for tested source [`83a16b2e627009d9d1e6e2516fb939ac64e05a27`](https://github.com/aliaksei-lameyka/ENKU-Base-reader/commit/83a16b2e627009d9d1e6e2516fb939ac64e05a27) on engineering/r120-routing-closure. Job 114335679411, all steps passed. Captured 2026-10-10T23:08:55.122824+00:00.

KiCad **10.0.7**, official runtime archive SHA256 3c6067b03e2e6eb7b3e17f63f6d57c2937a19c39d585edd0c0a8d0bebaec8969. PCB SHA256 **aa34851ae3f4174b0bb52eef2093bd61cd3d9428abfe1445d7fbb8c3850d7b36**. 417 pads, 117 footprints. Full --severity-all --all-track-errors --schematic-parity --refill-zones --save-board: **0 opens, ERC0, parity0; DRC126 = library106 + hole20**. No exclusions or global rules changed. Server effective pad polygons/attributes, all copper identities, footprint poses, zones and keepouts match the committed checkpoint.

Seven actual JSON reports were parsed from timestamped server logs and retained in checks/: server_USB_audit_R125.json, server_Q1_audit_R125.json, server_manufacturer_audit_R125.json, server_SW1_audit_R125.json, server_component_audit_R125.json, server_preservation_audit_R125.json, server_comparison_audit_R125.json. [Full provenance, job steps and reports](../hardware/mainboard/kicad/checks/server_evidence_R125.json).

New server checks verify manufacturer Q1/Q2/U9 pads and mappings, nine U1 paste apertures, no J7 contact paste, USB shell identity and complete R124-to-R125 preservation of all 417 pad UUIDs, all 2610 old copper items and all native net nodes. Existing USB filled-reference, side-button/microSD and SW1 guards also pass.

Artifact `enku-native-kicad-83a16b2e627009d9d1e6e2516fb939ac64e05a27`, ID **11685446658**, 358219 bytes; GitHub API reports digest **sha256:329b03c521efc280278540800a55c5aa897f7b7a5a09bd84027cada295497849**. Binary ZIP was not downloaded or locally hashed. Expires 2026-11-09T23:07:37Z; retained JSON proof survives artifact expiry. The following proof commit changes only evidence/docs/metadata; the hardware and workflow tested by the linked source commit are unchanged.

Nominal land match is separate from assembly/thermal/bench qualification. U1 solid EP and .3 drill remain a documented process adaptation, buttons/USB intrinsic hole findings remain active, and SW1 source revision/FPC/stackup/enclosure/remaining exact MPNs stay open. **fabrication_ready=false; NO FAB**.
