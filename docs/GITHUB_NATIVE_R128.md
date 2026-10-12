# R128 native GitHub checkpoint — verified

Actual [run 38133416979](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38133416979) and job `114452255388` succeeded on2026-10-11. All12 reported job steps completed successfully. Evidence captured at `2026-10-11T10:54:06.903Z`.

- Checked source commit `562037ec0518072fae0e5f669f41fcf5b588e226`; tree `b51a8a91a41cc426a3a85e6ce68fb8be8bd8c263`.
- Repository `aliaksei-lameyka/ENKU-Base-reader`, branch `engineering/r120-routing-closure`.
- Canonical PCB SHA256 `f53da6653e1f98241a4da7e337aa001a2b8614fa1b3e0685d893d299a18d5fa6`.
- Native KiCad **10.0.7**, pinned official runtime archive hash verified by CI.
- Native result **0 opens/ERC0/parity0; DRC46=26library+20holes;425pads/117footprints**.

The actual source-bound workflow runs full-severity/all-track-errors DRC, zone refill/save, schematic parity/ERC/netlist, twelve independent guards and exact native checkpoint comparison. All53 uploaded source blobs and the complete586-blob Git source tree were verified against local Git blob identities; every other accepted R127 blob is preserved.

Thirteen report JSONs decoded from the actual job log are retained with SHA256 and log line provenance in [server_evidence_R128.json](../hardware/mainboard/kicad/checks/server_evidence_R128.json).

| Retained report | Confirmed scope |
| --- | --- |
| `server_USB_audit_R128.json` | Both USB-C contact orientations, ESD polarity and actual filled In2.Cu GND reference |
| `server_physical_audit_R128.json` | 91 new/relocated vias,0.1mm annulus-to-land,0.5348469mm Tag-Connect foreign-copper gap |
| `server_Q1_audit_R128.json` | Exact Gate1/Source2/Drain3 top-view order and native connectivity |
| `server_manufacturer_audit_R128.json` | Nominal microSD/buttons and20 retained intrinsic hole errors |
| `server_SW1_audit_R128.json` | Approved MK-12C03-G015 common2/1GND/3NC, upper edge and exact source selection |
| `server_component_audit_R128.json` | Q1/Q2/U9 nominal lands and pin maps, J7 no paste, J5 USB_SHIELD |
| `server_component_pass_audit_R128.json` | 79 exact R127 passive/SW2 MPN/land/metadata/net/DNP selections |
| `server_power_budget_audit_R128.json` | Native32 capacitor inputs and independent Ceff/VBUS/discharge/pulse/EPD arithmetic; unknown qualification remains false |
| `server_U1_EP_audit_R128.json` | Nine0.9mm GND lands,0.8mm mask/paste,12 retained thermal drills/tent requests, exact N16R8/reserved pins/ambient metadata |
| `server_U1_plot_audit_R128.json` | Actual native9×0.8mm F.Mask/F.Paste apertures; no thermal drill openings in either mask layer |
| `server_holes_audit_R128.json` | 20 active findings/18 physical gaps, source locator diameters/pitches and actual copper distances; no weakening |
| `server_preservation_audit_R128.json` | All417 old pad identities/net/drill and2639 old copper items;22 declared U1 edits+8 lands; all other native source/rules/libraries preserved |
| `server_comparison_audit_R128.json` | Exact native geometry/attributes/zones/keepouts and full DRC/ERC/parity comparison |

Artifact API metadata: ID `11699783727`, `423302` bytes, digest `sha256:566e0c69c18135707d8f9cf44392e6c7c58f1d379d4ab8211127a0d1bb7b3a4a`, expires `2026-11-10T10:51:39Z`. These are actual API fields. The binary artifact was **not downloaded or independently hashed**. No local report is substituted for an actual server report. The three server plot hashes refer to plots created in the actual job; SVG timestamps can differ from local plot hashes while verified aperture geometry matches.

The proof follow-up changes only evidence/checkpoint/docs/hours metadata. Every canonical hardware, library, rule, workflow and script blob remains byte-identical to the tested source. The complete Git tree difference is checked against the explicit metadata allowlist before the engineering ref is advanced.

**server_verified=true; fabrication_ready=false.** All20 intrinsic hole errors and26 library warnings remain active. U1 tent/mask/stencil/reflow qualification, controlled SW1/FPC, factory stackup, power/USB bench and enclosure/assembly gates remain open. [Remaining work](REMAINING_TO_BUILD_R128.md).
