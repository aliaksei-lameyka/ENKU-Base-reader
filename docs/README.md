# Current documentation

Physical PCB R138 / qualification and consolidation R139 / NO FAB. Start with [CURRENT_STATUS](CURRENT_STATUS.md) and [WORK_HANDOFF_R139](WORK_HANDOFF_R139.md). Revision-named files describe their recorded revision and do not override these current entries.

| Subject | Current document |
| --- | --- |
| Qualification / release gates | [Product qualification](PRODUCT_QUALIFICATION_R139.md) |
| PCBWay process and manufacturing files | [Instructions](PCBWAY_MANUFACTURING_NOTES_R138.md) / [packet record](qualification/R139/PCBWAY_PACKET_R138.json) |
| Flashing, recovery and required firmware | [Factory contract](FACTORY_FLASH_CONTRACT_R139.md) / [source audit](qualification/R139/boot_recovery_source_audit_R139.json) |
| Actual native proof | [R138 main/engineering](GITHUB_MAIN_R138.json) |
| Physical R138 changes and first boards | [Annular/copper review](ANNULAR_REVIEW_R138.md) / [bring-up](BRINGUP_R138.md) |
| Battery availability | [13 October review](BATTERY_STATUS_R139.md) |
| USB MSC | [Ownership specification](usb-mass-storage.md) |
| Time and integration | [Hours](DEVELOPMENT_HOURS_READER.json) / [consolidation](REPOSITORY_CONSOLIDATION_R139.md) |

[R135 power contract](USB_POWER_CONTROL_R135.md), [switch/NTC review](SWITCH_NTC_R135.md), [R136 capacitance](CAPACITANCE_R136.md) and [power checks](BRINGUP_R136.md) remain technical foundations where the current handoff retains them. Their dated stock statements are historical.

Older handoffs/readiness reports, `evidence/R*`, versioned PCB variants and the old mainboard README are preserved snapshots. Native source verification pins 1325 accepted historical files; moving/deleting them breaks reproducibility. [Retained branch differences](history/retained-branches/README.md) and their registry distinguish old evidence/research from current source. They are not manufacturing input folders.
