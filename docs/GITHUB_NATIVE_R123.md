# R123 actual native server verification — source match, NO FAB

Tested source commit: `478c9d79ab9cfc5da338de1634b2f62466f9f3ff` on `engineering/r120-routing-closure`.

[Completed GitHub Actions run 38089955370](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38089955370), job `114324173453`: **success**. Exact official KiCad **10.0.7**, runtime tar SHA-256 `3c6067b03e2e6eb7b3e17f63f6d57c2937a19c39d585edd0c0a8d0bebaec8969`. Source PCB SHA-256 before server refill: `89921e5219857e6602fc52ac1b8acf84821b747b06b999cf85b0794a80616644`.

| Actual server finding | Result |
| --- | ---: |
| Unconnected items | 0 |
| ERC findings | 0 |
| Schematic parity findings | 0 |
| Library footprint mismatches | 110 |
| Hole-clearance findings | 20 |
| Pads / footprint placements matching local source | 410 / 117 |

Every track/via UUID, net, endpoint, width, layer and drill matches. Pad numbers/nets, pose, dimensions, drills, copper polygons, shape and attributes match. Zone outlines and keepout restrictions match. DRC/ERC exclusion lists match the saved native checkpoint. All severities/all-track errors, native zone refill and parity were enabled.

The separate server USB guard uses the actual independently refilled GND export, not the local stored polygons: zero missing reference regions and zero missing core strip area. USB polarity/ESD mapping and all physical pad groups pass. Actual factory stackup/90-ohm impedance remain unqualified; full Type-C contact branches remain for review.

The Q1 manufacturer top-view guard retains the R122 pin-order correction and physical continuity of all three nets. The manufacturer/button guard passes the nominal drawing interpretation, four button keepouts, extra mechanical lands, corrected unused common labels and J2 pad orientation. It checks all 281 vias against the revised lands, with minimum annulus-to-land gap 0.150 mm and zero violations. Locator-hole interpretation and assembly tolerances remain **unqualified**.

Twenty hole findings remain active: four USB guide-hole findings and four per side button. The button contact/bracket gaps are 0.075/0.150 mm against the unchanged 0.250 mm rule. The source-comparison success grants no waiver or fabrication release.

Actual job JSON reports are committed under `hardware/mainboard/kicad/checks/server_*_R123.json`; proof metadata is in `server_evidence_R123.json`. GitHub artifact `11683054114` (`enku-native-kicad-478c9d79ab9cfc5da338de1634b2f62466f9f3ff`, 347168 bytes) has reported digest `sha256:53bcea09c4e5704e1c84a2447854bc3a935ccb62c2b467c0d62f0e2c1936b15b` and expires `2026-11-09T22:04:06Z`. The archive digest is GitHub's reported identity, not a locally recomputed download hash. Durable summaries remain in git after artifact expiration.

`fabrication_ready = false`. [Remaining release work](REMAINING_TO_BUILD_R123.md). Proof-only follow-up commits change reports/docs and the server-verified flag, not the tested board or schematic.
