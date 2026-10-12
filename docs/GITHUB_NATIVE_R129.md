# R129 native GitHub checkpoint — verified

Actual [run 38136336929](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38136336929) and job `114460858170` succeeded on2026-10-11. All12 reported job steps completed successfully. Evidence captured at `2026-10-11T11:43:07.732Z`.

- Checked source commit `3fe0934dff0059202fbc5455c16a5b778fff365b`; tree `8e5a4a9c701338b943eda7a4a28d417e6d98b6f7`.
- Repository `aliaksei-lameyka/ENKU-Base-reader`, branch `engineering/r120-routing-closure`.
- Canonical PCB SHA256 `bab3cda1faa40bb2535f2d3eefe6ef0a9f43593b82577843cfe54f6d98da013c`.
- Native KiCad **10.0.7**, pinned official runtime archive hash verified by CI.
- Native result **0 opens/ERC0/parity0; DRC20 only hole clearance; library0;427pads/117footprints**.

The source-bound workflow runs full-severity/all-track-errors DRC, zone refill/save, schematic parity/ERC/netlist, fifteen independent guards and exact native checkpoint comparison. All84 uploaded source blobs and the complete672-blob source tree were checked against local Git blob identities; all other accepted R128 blobs are preserved.

Sixteen report JSONs decoded from the actual job log are retained with SHA256 and log-line provenance in [server_evidence_R129.json](../hardware/mainboard/kicad/checks/server_evidence_R129.json).

| Retained report | Confirmed scope |
| --- | --- |
| `server_USB_audit_R129.json` | Both USB-C contact orientations, ESD polarity and actual filled In2.Cu GND reference |
| `server_physical_audit_R129.json` | 91 new/relocated vias, annulus-to-land and Tag-Connect foreign-copper clearance |
| `server_Q1_audit_R129.json` | Exact Gate1/Source2/Drain3 top-view order and native connectivity |
| `server_manufacturer_audit_R129.json` | Nominal microSD/button lands and twenty retained intrinsic hole findings |
| `server_SW1_audit_R129.json` | Approved MK-12C03-G015 common2/1GND/3NC, upper-edge pose and accepted source selection |
| `server_component_audit_R129.json` | Q1/Q2/U9 nominal lands and pin maps, J7 no paste and J5 USB_SHIELD |
| `server_component_pass_audit_R129.json` | 79 exact passive/SW2 MPN, land, metadata, net and DNP selections |
| `server_power_budget_audit_R129.json` | Native32 capacitor inputs and independent power arithmetic; unqualified process/bench assumptions remain false |
| `server_U1_EP_audit_R129.json` | Nine0.9mm GND lands,0.8mm mask/paste, twelve retained thermal drills, exact N16R8 and reserved pins |
| `server_U1_plot_audit_R129.json` | Actual nine0.8mm mask/paste apertures and absence of thermal drill openings in both mask layers |
| `server_holes_audit_R129.json` | Twenty active findings, eighteen physical gaps, unchanged hole dimensions and global0.25mm rule |
| `server_preservation_audit_R129.json` | All425 old pad identities/nets/positions/drills and2639 tracks/vias; exactly25 declared pad-property changes and two paste-only pads |
| `server_active_IC_audit_R129.json` | 52 numbered lands of U3/U4/U5/U8/U9/U10, native schematic/PCB pin maps, support networks and selected modes |
| `server_IC_stencil_audit_R129.json` | Actual native U3 mask/paste and U4 two separate paste windows; accepted R128 full-paste overlay defect independently confirmed |
| `server_assembly_audit_R129.json` | Actual native CPL97 rows, ten formerly omitted SMD parts, eighteen bare-PCB exclusions, two DNP exclusions, J7 pin1 and thirteen probe labels |
| `server_comparison_audit_R129.json` | Exact native geometry/attributes/zones/keepouts and full DRC/ERC/parity comparison |

Artifact API metadata: ID `11700484895`, `406001` bytes, digest `sha256:f345acc568e0580beb79386ffc235264db66d59764ac89ad557bbd2e4a6edcfe`, expires `2026-11-10T11:40:19Z`. These are actual API fields. The binary artifact was **not downloaded or independently hashed**. No local report is substituted for an actual server report. Server SVG timestamps can differ from local plot hashes while verified aperture geometry matches.

The proof follow-up changes only evidence/checkpoint/docs/hours metadata. Every canonical hardware, library, rule, workflow and script blob remains byte-identical to the tested source. The complete Git tree difference is checked against the explicit metadata allowlist before advancing the engineering ref.

**server_verified=true; fabrication_ready=false.** Twenty hole-clearance errors remain active. No hole dimensions, exclusions or severities were weakened. Unified stencil/U1 tenting, twelve explicit MPN fields, controlled SW1/FPC data, factory stackup, power/USB bench and enclosure/assembly gates remain open. [Remaining work](REMAINING_TO_BUILD_R129.md).
