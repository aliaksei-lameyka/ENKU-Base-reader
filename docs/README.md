# Current documentation

**Working PCB R142, NO FAB.** Start with [current status](CURRENT_STATUS.md), [current source](../hardware/mainboard/r142/README.md), [PCBWay instructions](PCBWAY_MANUFACTURING_NOTES_R142.md), [package record](evidence/R142/PCBWAY_PACKET_R142.json), [checks before submission](PRE_REVIEW_CHECKS_R142.md) and [Good Display / Hirose comparison](FPC_CONNECTOR_REVIEW_R142.md).

The entries below are retained R138/R139/R140/R141 references. Their recorded revisions do not override the current R142 board. Product qualification and factory-flash requirements remain applicable where identified in the current qualification plan.

# Retained documentation

Physical PCB R138 / qualification and consolidation R139 / NO FAB. Start with [CURRENT_STATUS](CURRENT_STATUS.md) and [WORK_HANDOFF_R139](WORK_HANDOFF_R139.md). Revision-named files describe their recorded revision and do not override these current entries.

The R140 engineering branch adds the [whole-board routing recheck](BOARD_ROUTING_REVIEW_R140.md), a fresh local native proof and specific layout findings; the physical source remains R138.

| Subject | Current document |
| --- | --- |
| Whole-board routes / new priority layout work | [R140 report](BOARD_ROUTING_REVIEW_R140.md) / [geometry and evidence](qualification/R140/verification_R140.json) |
| Qualification / release gates | [Product qualification](PRODUCT_QUALIFICATION_R139.md) |
| PCBWay process and manufacturing files | [Instructions](PCBWAY_MANUFACTURING_NOTES_R138.md) / [current upload files](qualification/R139/PCBWAY_UPLOAD_PACKAGE_R139.json) / [retained first packet](qualification/R139/PCBWAY_PACKET_R138.json) |
| Flashing, recovery and required firmware | [Factory contract](FACTORY_FLASH_CONTRACT_R139.md) / [source audit](qualification/R139/boot_recovery_source_audit_R139.json) |
| Actual native proof | [Consolidated main](GITHUB_MAIN_R139.json) / [retained R138 main/engineering](GITHUB_MAIN_R138.json) |
| Physical R138 changes and first boards | [Annular/copper review](ANNULAR_REVIEW_R138.md) / [bring-up](BRINGUP_R138.md) |
| Battery availability | [13 October review](BATTERY_STATUS_R139.md) |
| USB MSC | [Ownership specification](usb-mass-storage.md) |
| Time and integration | [Hours](DEVELOPMENT_HOURS_READER.json) / [consolidation](REPOSITORY_CONSOLIDATION_R139.md) |

[R135 power contract](USB_POWER_CONTROL_R135.md), [switch/NTC review](SWITCH_NTC_R135.md), [R136 capacitance](CAPACITANCE_R136.md) and [power checks](BRINGUP_R136.md) remain technical foundations where the current handoff retains them. Their dated stock statements are historical.

Older handoffs/readiness reports, `evidence/R*`, versioned PCB variants and the old mainboard README are preserved snapshots. Native source verification pins 1325 accepted historical files; moving/deleting them breaks reproducibility. [Retained branch differences](history/retained-branches/README.md) and their registry distinguish old evidence/research from current source. They are not manufacturing input folders.

