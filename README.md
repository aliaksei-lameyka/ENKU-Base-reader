# ENKU Base Reader

**Working PCB: R147. Branch: `engineering/r147-mechanical-review`. Engineering review / NO FAB.**

R147 simplifies routing in12 of18 newly marked R146 regions:38 old top-copper segments replaced by13, length reduced0.818847mm. Six retained details have explicit geometric/topology reasons. All141 footprints,473 pads,386 vias, netlist, rules, holes, thickness, outline, USB data and inner/bottom routing are preserved.

Native KiCad10.0.7 DRC/ERC/opens/parity0. Complete local independent electrical, OEM, power, four-layer copper, manufacturing and84-net Gerber graph checks PASS. Actual source-pinned server [run38763074552](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38763074552) also passed; downloaded API digest/CRC, all24 manufacturing files,41 JSON reports and native geometry agree. [Proof](docs/GITHUB_R147.json).

**Display-FPC mechanical review remains open:** the actual J3 inlet faces down the board and a flat entry path intersects C24/C29/C30. [Measured review and corrective criteria](docs/qualification/R147/FPC_mechanical/ENKU_R147_Display_FPC_Review_RU_EN.md). A four-cap upper-envelope STEP add-on is available; the original simplified model omitted these small parts.

The enclosure STEP contains the exact R146 physical placement, unchanged in R147. Board59x101x1.6mm with four2.2mm mounting holes; official Hirose, E-Switch and Espressif CAD aligned to source lands. USB is a nominal drawing reconstruction; SW1 and JST are explicitly nominal reserves with unresolved mechanical qualifications. Optional access/travel zones are separate. Small passives, most ICs, panel, battery and fasteners are omitted.

| Need | Current entry |
| --- | --- |
| Enclosure STEP, package and preview | [Downloads](hardware/mainboard/mechanical/r146_r147/DOWNLOADS.md) |
| Enclosure datum / RU and EN notes | [Mechanical handoff](hardware/mainboard/mechanical/r146_r147/README_ENCLOSURE_R146.md) |
| All18 user marks | [R147 dispositions](docs/MARKED_ROUTING_REVIEW_R147.md) |
| Editable source | [R147 KiCad](hardware/mainboard/r147/kicad/enku-mainboard-r0.1.kicad_pro), [manifest](hardware/mainboard/r147/source_manifest_R147.json), [finite scope](hardware/mainboard/r147/scope_R147.json) |
| Manufacturing review | [Paired R147 files](hardware/mainboard/r147/pcbway/README_R147_NO_FAB.md) |
| Current checks | [R147 derivatives](hardware/mainboard/r147/checks/), [local+server proof](docs/qualification/R147/) |
| Current handoff | [R147](docs/WORK_HANDOFF_R147.md) |
| Physical acceptance | [Risks](docs/STARTUP_RISKS_R144.md), [FPC](docs/FPC_CONNECTOR_REVIEW_R144.md), [FCT](docs/FCT_PLAN_R144.md) |
| Bounded hours | [Ledger](docs/DEVELOPMENT_HOURS_READER.json) |

Physical tests NOT RUN. FPC pose/fit, SW1 mechanical datum, protected battery and bonded NTC, factory stackup/drill/fill-cap/stencil/USB impedance, MLCC effective capacitance, dynamic rails/EPD and reproducible FCT/per-board acceptance remain open. All prior revision evidence is retained. Base has no dock, Hall, Qi or frontlight. No prototype-startup guarantee or manufacturing release.

Original hardware CERN-OHL-W-2.0. Automation MIT. Manufacturer CAD retains its own copyright. [Licensing](LICENSE.md).
