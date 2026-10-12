# R136 engineering handoff — NO FAB

Accepted R135 and the independent licensing commit were merged into `main` at **1a29692ae5498b5f3a668599129d475167113840**, with both parents retained. Main-license files are byte-identical to the original licensing commit; three conflicting overview documents use current Base engineering data. No hardware or R135 proof changed in that merge. R136 is retained on `engineering/r136-capacitance-release` from that exact merged main and its verified source/proof is consolidated into `main` after actual immutable CI/artifact verification.

## Current source and local checks

C9 changes to22uF10V Yageo CC0805MKX5R6BB226. Its four metadata fields are the only PCB/power-sheet changes. **All127 placements,438 physical pads,3707 copper items, full native net connections, zones/holes/mask/paste/USB/RF/outline/stack and thermal requests are identical to R135.** PCB SHA256`396a7ee137778778539848e9e1a3a7b95518ce329b63425822e191f1ef9c6849`.1140 R135 files plus main licenses are independently pinned; old checks and evidence remain.

Native KiCad10.0.7 local DRC0/ERC0/opens0/parity0,23 independent scopes plus checkpoint comparison and8 deliberate regression-rejection cases pass. Normal CI verifies the committed baseline and refuses to regenerate it. New current-source workflow covers main, the R136 engineering branch and relevant PRs. **Actual immutable-source GitHub run38259293325 and all9 job steps pass.** Actual44-member/641377byte artifact SHA/API digest/CRC, all24 audit reports, five plots and8 rejection cases were verified against local results.22 report JSONs match exactly;2 differ only by independently checked SVG title-date hashes. [Exact proof](GITHUB_NATIVE_R136.md). Source commitd55113c4900659c2f7f3c9e38c376034ec17904d; proof/docs commits preserve the source.

## Design progress

The inspected10uF DC-bias curve gives much less margin than the inherited70% scenario. Rounded-down60% produces4.131uF (3.28% margin); new22uF with40% retention produces5.3856uF (34.64% margin). This is a bounded project scenario, not a manufacturer guarantee. C7/C8 and local output scenarios plus all nine direct output capacitors are now checked. [Source-backed calculation and limits](CAPACITANCE_R136.md).

Old C9 max height0.95mm, new1.45mm. Other existing22uF components already have1.45mm maximum height. Local clearance at59.7,87.7mm still requires approval; external case thickness must not increase. New startup capacitance demands real Q2/charger/USB/brownout tests. All23 scopes preserve native rules and R135 source; they do not approve these physical behaviors.

Fresh supplier replies do not supply a qualified thin replacement: Ropla confirms AKY0156 maximum5.2mm finished height and no immediate thin stock substitute; its stock pack is rejected for this enclosure. Koosay still requires real compartment dimensions, Polybattery has no technical reply. Good Display's new frontlight answer is outside Base; PCBWay's reply is not process approval. [Exact technical status](SUPPLIER_STATUS_R136.md). No new messages, fabrication or purchases occurred.

## Remaining sequence

1. Register complete current case/component CAD, resolve PH2/pouch collision and check side-button pushers, C9 local height, USB opening, panel/FPC and service access at fixed thickness.
2. Qualify two finished thin2000–2500mAh protected two-wire packs with one maximum envelope,2A pulse/chemistry/polarity/transport evidence and CN/Poland supply. Do not substitute cell-code dimensions for the PCM pack.
3. Establish sufficiently bounded capacitance/sensor R/T/TS-leakage acceptance, detached-sensor/R82 fault treatment, exact Base panel/FPC, controlled USB stackup and factory U1/U3 stencil/fill/cap and USB short-stake process review.
4. Prepare a concrete reviewed EVT package and obtain user authorization before manufacturing or parts purchases. After approved boards arrive, run startup/loaded GPIO/charge/fault/thermal/USB/MSC and both-pack validation. Physical tests are NOT RUN. Production follows physical qualification.

Open `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Use `checks/run_native_current.py` with pinned runtime to verify this checkpoint, without `--freeze`. Historical R134/R135 workflows and checkpoints are retained for their historical branches, not selected as current main checks.
