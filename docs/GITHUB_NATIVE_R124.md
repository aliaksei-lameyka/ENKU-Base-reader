# Actual GitHub-native R124 proof

**Completed and successful.** [Run 38092121645](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38092121645), job **114330515917**, tested source commit **`7878459718d8d8408eb6452ceac293cf76367637`** in `engineering/r120-routing-closure`. This is a real GitHub Actions run, separate from the local helper-format simulation.

Source PCB SHA256: **`5facf2ac0a91cbd79ec97e85fed2552e45cf46052aa66bb98a21bc5539639b5e`**. Official native runtime **KiCad 10.0.7**, tar SHA256 **`3c6067b03e2e6eb7b3e17f63f6d57c2937a19c39d585edd0c0a8d0bebaec8969`**. The source identity is captured before native refill/save.

All job steps completed successfully: pinned runtime validation, full DRC with all severities/track errors, native refill/save and schematic parity, full ERC/netlist, actual filled-plane export, USB/Q1/button/SD/SW1 guards, source geometry comparison and artifact retention.

| Actual server result | Value |
| --- | ---: |
| Physical pads / footprints | 417 / 117 |
| Unconnected items | 0 |
| ERC | 0 |
| Schematic parity | 0 |
| Library mismatch | 109 |
| Hole clearance | 20 |
| Active SW1 native findings | 0 |

Server and committed local pad identities, nets, dimensions, drills, copper polygons/attributes, tracks, footprint poses/library IDs and zone/keepout outlines and restrictions match. DRC/ERC exclusions match. The actual SW1 native netlist agrees with **2 COM/PWR_GATE, 1 GND, 3 unused**, physical pad groups are connected, all 282 vias were checked against its solder lands, and the RF keepout remains clear. Actual refilled USB ground has no missing trace-reference regions. Q1 manufacturer top-view pin mapping and manufacturer nominal button/microSD geometry guards pass.

Five report JSON objects were parsed from the **actual completed job logs** fetched through GitHub API and are retained in `hardware/mainboard/kicad/checks/`:

- `server_comparison_R124.json`
- `server_USB_audit_R124.json`
- `server_Q1_audit_R124.json`
- `server_manufacturer_footprint_audit_R124.json`
- `server_SW1_audit_R124.json`

`server_evidence_R124.json` retains source/run/job identities, successful step metadata, capture time and artifact metadata. Artifact **11684756743**, **352989 bytes**, GitHub API-reported digest **`sha256:968070cadf1a29fb5ae76aa80db45516530f79714d6513fedcbe8e7ae2bf964a`**, expiry **2026-11-09T22:38:36Z**. The binary archive was not downloaded or independently hashed; its digest is attributed to GitHub. Reports and provenance in this repository remain available independently of artifact retention.

**NO FAB**. This pass does not qualify the mixed A0/X1 SW1 land pattern, body-to-locator datum, switch retention or enclosure fit; the 20 button/USB hole findings stay active. MPN/land, display/FPC, stackup, assembly and freeze gates remain in [the work list](REMAINING_TO_BUILD_R124.md). No manufacturing release follows from successful regression comparison.

The subsequent evidence-only commit updates these reports/status/hours/documents and does not change the tested hardware or workflow.
