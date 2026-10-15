# ENKU Base Reader

**Working PCB: R146. Branch: `engineering/r146-zigzag-review`. Engineering review / NO FAB.**

R146 simplifies routing in77 of78 user-marked R145 regions.730 old top-copper segments are replaced by138; total routed length is16.0074mm shorter. All141 footprints,473 pads,386 vias, values, MPNs, netlist, USB data, inner/bottom routing, antenna rules and the R145 BMI270 decoupler placement are preserved. Two local GND legs use the wider0.25mm width throughout.

Native KiCad10.0.7 DRC/ERC/opens/parity0 and complete independent four-layer, electrical, OEM and manufacturing checks pass. Actual source-pinned server evidence follows separately.

| Need | Current entry |
| --- | --- |
| Current handoff | [R146](docs/WORK_HANDOFF_R146.md) |
| All78 user marks | [Region dispositions](docs/MARKED_ZIGZAGS_REVIEW_R146.md) |
| Editable source | [R146 KiCad](hardware/mainboard/r146/kicad/enku-mainboard-r0.1.kicad_pro), [manifest](hardware/mainboard/r146/source_manifest_R146.json), [finite scope](hardware/mainboard/r146/scope_R146.json) |
| Current checks | [R146 strict derivatives](hardware/mainboard/r146/checks/), [local result](docs/qualification/R146/local_verification_R146.json) |
| Physical acceptance | [Risks](docs/STARTUP_RISKS_R144.md), [FPC](docs/FPC_CONNECTOR_REVIEW_R144.md), [FCT](docs/FCT_PLAN_R144.md) |
| Bounded hours | [Ledger](docs/DEVELOPMENT_HOURS_READER.json) |

Z49 retains the BMI270 INT1 escape because a direct trace would short U5.3. Z54 keeps R9 connected and uses a cleaner vertical leg. All prior revisions and their evidence remain historical. No prototype-startup guarantee or manufacturing release: physical tests, factory process/FPC/battery/NTC/dynamic rail/EPD/FCT qualifications remain open. Base has no dock, Hall, Qi or frontlight.

Original hardware CERN-OHL-W-2.0. Automation MIT. [Licensing](LICENSE.md).
