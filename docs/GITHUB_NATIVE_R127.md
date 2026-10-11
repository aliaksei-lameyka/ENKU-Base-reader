# R127 native GitHub checkpoint — verified

Actual [GitHub Actions run 38129966641](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38129966641) and job `114442073369` completed successfully on 2026-10-11. All 12 reported job steps succeeded. Evidence was captured at `2026-10-11T09:59:59.283Z`.

- Source commit: `e347e3bad3b76c74b764555880d2e9205fe04038`; tree: `5e3e70abb280f877b8d25d59ea30963e4371c956`.
- Branch: `engineering/r120-routing-closure` in `aliaksei-lameyka/ENKU-Base-reader`.
- Canonical PCB SHA256: `c2316fa909debdd69577cd565b04bab6e40db01acbfc9c2b6f1362ac4b14b1f2`.
- Native KiCad: **10.0.7**, exact runtime checked by CI.
- Native result: **0 opens, ERC 0, schematic parity 0; DRC 47 = 27 library mismatch + 20 hole clearance**; 417 pads, 117 footprints.

The full native DRC refilled and saved zones and checked schematic parity. Server geometry, all pad attributes, zone outlines and keepout restrictions match the committed local checkpoint. The 52 uploaded source blobs were individually verified against their local Git blob SHA1 and the complete committed Git tree.

Ten report JSONs were decoded from the actual job log and retained under `hardware/mainboard/kicad/checks/`. [Evidence and report hashes](../hardware/mainboard/kicad/checks/server_evidence_R127.json) record actual run/job identity, steps, provenance and log line ranges.

| Retained server report | Confirmed scope |
| --- | --- |
| `server_USB_audit_R127.json` | Both USB-C contact orientations, ESD polarity, copper-layer-aware paths and actual filled In2.Cu GND reference |
| `server_physical_audit_R127.json` | 91 new/relocated vias; at least 0.1 mm annulus-to-land and 0.5348469 mm Tag-Connect foreign-copper clearance |
| `server_Q1_audit_R127.json` | Manufacturer top-view Gate/Source/Drain order and physical connectivity |
| `server_manufacturer_audit_R127.json` | Nominal microSD/button geometry, via review and all 20 active intrinsic hole findings |
| `server_SW1_audit_R127.json` | Approved G-Switch selection, common pin 2, upper-edge pose and unused pin 3 |
| `server_component_audit_R127.json` | Q1/Q2/U9 lands and pin maps, U1 paste apertures, paste-free J7 and J5 shield pads |
| `server_component_pass_audit_R127.json` | 79 exact MPN selections: 43 resistors, 32 capacitors, 3 diodes and SW2; native metadata, pad axes, connectivity and DNP/tuning options |
| `server_power_budget_audit_R127.json` | Independent native 32-capacitor inputs, Ceff/VBUS/divider/discharge/R37/EPD arithmetic and explicit unqualified scenarios |
| `server_preservation_audit_R127.json` | All 417 pad and 2639 original copper identities/net names; 36 physical pad edits, 3 declared old copper adjustments, no added copper or moved footprints; native nets/rules/exclusions/old libraries preserved |
| `server_comparison_audit_R127.json` | Exact native geometry/checkpoint comparison and complete native DRC/ERC/parity counts |

Artifact API metadata: ID `11698648186`, `374409` bytes, digest `sha256:88f7a66e2065bde0cf23b567eceb9774e9b4e639513a9e82d4d62ae7940d487c`, expiry `2026-11-10T09:54:11Z`. These are actual GitHub API fields. The binary artifact was **not downloaded or independently hashed**. Retained report JSONs come from the actual job log, not local substitutes.

The proof follow-up changes report/checkpoint/documentation metadata only. Canonical PCB, schematics, project/rules, footprints and workflow remain byte-identical to the source commit checked by this run. The full Git tree difference is checked against the explicit metadata allowlist before the branch is advanced.

**server_verified=true; fabrication_ready=false.** U1 stencil/mask/via process, 20 button/USB hole findings, SW1 controlled drawing/mechanical datum, guaranteed DC-bias Ceff, real USB inrush/suspend/disconnect timing, R37 repetitive pulse/thermal behavior, exact EPD panel/FPC, factory stackup and enclosure/assembly gates remain open. A successful source check is not manufacturing or bench qualification. See [remaining work](REMAINING_TO_BUILD_R127.md).
