# ENKU Base Reader

**Current PCB: R148 · Branch: `engineering/r148-mechanical-review` · Engineering review / NO FAB**

R148 clears a 14 × 10.7 mm local approach to display connector J3 by moving 11 e-paper components and rerouting the affected power and control circuits. The tall JST battery header is replaced by the original VBAT/GND copper lands for soldered wires, with no paste or fitted housing. A separate case clamp must secure the wire insulation. Electrical topology, the J3 pin map, USB, board outline and mounting datums are retained.

KiCad 10.0.7 reports zero DRC errors, ERC errors, opens and schematic/PCB mismatches. The OEM, power/startup, four-layer copper, manufacturing and independent 84-net Gerber checks pass, including injected-fault checks. The source-pinned [server run 38776369871](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38776369871) also passes. [Verification evidence](docs/GITHUB_R148.json).

**Full display-flex fit remains open.** The display back faces the PCB back, and the cable wraps the board edge. The cleared local approach does not qualify the actual stepped flex's reach, pin 1 after folding, latch access or pressure-free case closure. J3 retains its current position pending the complete registered fold and may still need relocation. The PDF includes 1:1 paper templates for this check. [Mechanical review in Russian and English](docs/MECHANICAL_REVIEW_R148_RU_EN.md).

The enclosure STEP contains the current placements and critical small e-paper parts. The PCB is 59 × 101 × 1.6 mm, with four 2.2 mm mounting holes. Major ports and buttons use the retained aligned OEM CAD. USB, SW1 and small package bodies have explicitly documented modelling limits. The main model excludes the display, folded cable, battery and finished enclosure. Optional access and clearance reserves are provided separately.

| Need | Current entry |
| --- | --- |
| Complete package, STEP, copper maps, Gerber and six-page PDF | [Downloads and checksums](hardware/mainboard/mechanical/r148/DOWNLOADS.md) |
| Editable PCB source | [KiCad project](hardware/mainboard/r148/kicad/enku-mainboard-r0.1.kicad_pro), [source manifest](hardware/mainboard/r148/source_manifest_R148.json), [strict change scope](hardware/mainboard/r148/scope_R148.json) |
| Manufacturing review exports | [PCBWay review files](hardware/mainboard/r148/pcbway/README_R148_NO_FAB.md) |
| Checks and evidence | [R148 checks](hardware/mainboard/r148/checks/), [reports](docs/qualification/R148/), [server proof](docs/GITHUB_R148.json) |
| Mechanical details and handoff | [RU/EN report](docs/MECHANICAL_REVIEW_R148_RU_EN.md), [handoff](docs/WORK_HANDOFF_R148.md) |
| Earlier user routing marks | [R147 dispositions](docs/MARKED_ROUTING_REVIEW_R147.md) |
| Physical acceptance | [Startup risks](docs/STARTUP_RISKS_R144.md), [panel/FPC review](docs/FPC_CONNECTOR_REVIEW_R144.md), [FCT plan](docs/FCT_PLAN_R144.md) |
| Development hours | [Bounded ledger](docs/DEVELOPMENT_HOURS_READER.json) |

The design has 141 references, 471 pads and 389 vias: 119 fitted top components, 20 bare-PCB items, and R67/R99 marked DNP. All six explicit fill/cap requests remain subject to factory approval. Earlier source and evidence are retained. This base has no dock, Hall sensor, Qi or frontlight.

Physical tests have not been run. Whole flex/pack/case fit, wire and clamp qualification, the SW1 datum, protected battery pack and bonded NTC, factory stackup/drill/fill-cap/stencil/USB impedance, effective MLCC capacitance, dynamic rails, e-paper operation and per-board FCT remain open. R148 is not released for production, and startup is not guaranteed by these file-based checks.

Source commit: `bec2966be64cd6fdce5b1060f05179370ff0da77`  
PCB SHA256: `bb0aa41324b73ec13c087ab1c669c57c6bc6fd449621bf3aa34a53d3901b9476`

Original hardware: CERN-OHL-W-2.0. Automation: MIT. Manufacturer CAD retains its copyright. [Licensing](LICENSE.md).
