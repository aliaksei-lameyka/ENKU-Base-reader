# R136 actual immutable-source proof — NO FAB

Accepted R135 plus the independent main licensing history were merged at1a29692ae5498b5f3a668599129d475167113840. R136 immutable CI source is **d55113c4900659c2f7f3c9e38c376034ec17904d**, tree **fbf598d38e6f75b04a8ff02da0c449225d3e4375**. Source PCB SHA256 **396a7ee137778778539848e9e1a3a7b95518ce329b63425822e191f1ef9c6849**. Later proof/document commits do not change this PCB, schematic, project or the verified23 guards.

[Actual run38259293325](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38259293325), actual job114845375862: **all9 steps succeeded**. Native KiCad10.0.7 DRC0/ERC0/opens0/schematic parity0;23 independent scopes plus checkpoint comparison. The separate8 deliberate rejection cases also match the local test results.

Actual artifact11751712447 (`enku-native-kicad-d55113c4900659c2f7f3c9e38c376034ec17904d`) was downloaded and verified: **641377bytes,44ZIP members**, SHA256/API digest **174eb821649a14de41333f1217a0b0e2cc685008eb559fa083cd1578e77666d2**, exact size and ZIP CRC pass. All24 audit reports match:22 JSON files are exact,2 contain only independently validated raw SVG title-export timestamp hash differences. All five actual native SVGs are byte-identical after removing exactly that one title timestamp; copper/mask/paste/path data remain exact.

Actual geometry, reference and thermal fills, via process, assembly/orientation, CPL/BOM, original project and netlist electrical sections match local files. Actual source preservation verifies1140 R135 files, main licenses and the finite four-property C9 change.127 footprints,438 pads and3707 copper items remain physically identical to R135. The cap scenarios validate arithmetic, exact MPNs and native nets; they are not manufacturer DC/AC guarantees or physical tests.

Full proof is in `checks/github_native_proof_R136.json`. Actual binary is retained as `checks/native_server_R136.zip`, alongside24 `server_R136_*.json` audit reports, the rejection report and actual GitHub API metadata. `verify_server_artifact_R136.py` pins the source commit/tree/PCB and independently compares the actual artifact; it does not regenerate a baseline or reuse another revision's run.

The current workflow uses `run_native_current.py` on main, the engineering branch and relevant PRs. It rejects a stale source hash, unreviewed selector/baseline and CI `--freeze`; it restores project preferences after native export even on export failure. Historical workflows/checkpoints remain for historical branches.

`fabrication_ready=false`, physical tests **NOT RUN**. Full case/pack/PH2/button/USB/panel fit, Ceff/sensor/fault evidence, USB stackup/assembly process and firmware/physical qualification remain separate gates. No manufacturing, orders or supplier messages occurred.
