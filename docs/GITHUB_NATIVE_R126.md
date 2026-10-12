# R126 actual GitHub native proof

[Actual successful run 38105337714](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38105337714) verifies source commit **3ddd3b5c69579727d66c2cf29d0fce3610dedee1** on engineering/r120-routing-closure. Every job step succeeded, including native DRC/refill/parity, full ERC/netlist, independent audits and comparison. All 60 uploaded source blobs were checked against the committed Git tree before proof capture.

Source PCB SHA256 **8deaaa605264ce3119da6aae8e7a8a837cb9e781caa45e3348738eeb13585393**. Runtime KiCad10.0.7 with the exact official archive SHA from the workflow. **417 pads /117 footprints; opens0/ERC0/parity0; DRC65 =45 library mismatch +20 hole clearances.** Server geometry, pad shape/attribute, zone outlines and RF keepout restrictions match the committed local checkpoint.

61 exact MPNs, physical pad axes, diode/common row maps and DNP/tuning options pass. All417 original pad UUIDs and2610 original copper identities/net/layer/width/drill survive;57 declared endpoint changes and29 declared added segments,10 declared footprint moves. All other copper/placements, net nodes, rules and exclusions are preserved. Physical audit:90 new/relocated vias sinceR120; no under-limit annulus-to-land or Tag-Connect findings. Full refilled USB reference and manufacturer/SW1/Q1/Q2/U9/U1/J7 assembly guards pass with qualification limits still explicit.

Nine **actual server reports** decoded from the job log are retained in Git, rather than relying solely on an expiring Actions artifact:

| Report | Retained actual JSON |
| --- | --- |
| USB | [server_USB_audit_R126.json](../hardware/mainboard/kicad/checks/server_USB_audit_R126.json) |
| physical | [server_physical_audit_R126.json](../hardware/mainboard/kicad/checks/server_physical_audit_R126.json) |
| Q1 | [server_Q1_audit_R126.json](../hardware/mainboard/kicad/checks/server_Q1_audit_R126.json) |
| manufacturer | [server_manufacturer_audit_R126.json](../hardware/mainboard/kicad/checks/server_manufacturer_audit_R126.json) |
| SW1 | [server_SW1_audit_R126.json](../hardware/mainboard/kicad/checks/server_SW1_audit_R126.json) |
| component | [server_component_audit_R126.json](../hardware/mainboard/kicad/checks/server_component_audit_R126.json) |
| component_pass | [server_component_pass_audit_R126.json](../hardware/mainboard/kicad/checks/server_component_pass_audit_R126.json) |
| preservation | [server_preservation_audit_R126.json](../hardware/mainboard/kicad/checks/server_preservation_audit_R126.json) |
| comparison | [server_comparison_audit_R126.json](../hardware/mainboard/kicad/checks/server_comparison_audit_R126.json) |

[Evidence manifest](../hardware/mainboard/kicad/checks/server_evidence_R126.json) retains actual run/job/step data, all report hashes and artifact API metadata. Job ID114369561681. Artifact ID11689069997, 376415bytes, digest `sha256:2a7ef75555a49b43e66ed575107ed7a30d88ff9cb0bd09c4d924e3ae77976bb9`, expires2026-11-10T02:30:58Z. This digest is reported by the GitHub artifact API; the binary archive was not separately downloaded and hashed. Proof captured2026-10-11T02:33:16.110Z.

The follow-up commit contains evidence/verification/documentation/hour metadata only; it preserves all hardware and workflow blobs of the tested source. [Changes](COMPONENT_PASS_R126.md), [remaining gates](REMAINING_TO_BUILD_R126.md). **fabrication_ready=false; no fabrication/default merge.**
