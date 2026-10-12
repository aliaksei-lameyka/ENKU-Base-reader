# R122 actual server evidence — NO FAB

Source commit: `1698fbfa4ce06684c97c8e70e58b18c25e0a8d63`. [Run 38086819900](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38086819900), job `114314954263`, conclusion **success**. [Artifact 11682473691](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38086819900/artifacts/11682473691), digest `sha256:e32933579352f399fc07538700b8f1b792cc7ce4d3d2799aff19618fda30a54d`, expires 2026-11-09. The three JSON results are also retained in source control.

The SHA-pinned official KiCad 10.0.7 runtime performed full native DRC with zone refill, ERC, netlist and schematic parity. All 402 pad geometries, all 117 footprint placements and every track/via matched the committed checkpoint. Results: **0 opens, ERC 0, parity 0, 115 other DRC**: 111 library-footprint mismatches and four inherited USB-C guide-hole clearance findings. No dangling copper.

The independent USB audit ran on the server's own refilled GND polygons: no uncovered trace-reference regions and zero missing area in the 1 mm coupled-core reference strip. This checks continuity of the actual reference plane; factory stackup and 90-ohm impedance remain unqualified, and complete Type-C contact branch skew remains documented.

The separate Q1 guard checked corrected Gate/Source/Drain locations against the Infineon top view and native physical continuity of all three nets. The corrected pin locations are (66,47.05) for Gate, (66,48.95) for Source and (68,48) for Drain. These are absolute F.Cu pad centres in millimetres. Existing land dimensions and assembled circuit behaviour remain unqualified.

Source PCB SHA-256: `531d5a3dd0f6677f3a71e01f3030522c103bd0b1f6506c7df3fe8be487c5dcd0`. The retained `server_comparison_R122.json`, `server_USB_audit_R122.json` and `server_Q1_audit_R122.json` were extracted from the actual completed job logs, not local integration-test outputs. Run identity, runtime hash and artifact digest are retained in `server_evidence_R122.json`.

This completes exact server proof of R122 and its Q1 pin-order correction. Manufacturing remains blocked by the retained footprint/hole findings, stackup, display/connector and mechanical qualification, power/USB/SD firmware bring-up and bench checks. No fabrication release is issued.
