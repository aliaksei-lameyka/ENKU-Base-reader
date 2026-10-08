# ENKU manufacturer-first component qualification policy (R24)

Apply the switch-process to **every physical component**: verified exact MPN, original manufacturer drawing, pin mapping, electrical/symbol footprint equivalence, mounting side/orientation, 3D package and physical access, local China/PCBWay sourcing, then KiCad ERC+DRC+first-article confirmation.

**Sourcing:** prioritize PCBWay-qualified Chinese suppliers and LCSC where plausible. PCBWay has its own sourcing team and can use requested distributors; an LCSC URL alone never establishes PCBWay stock. [PCBWay component sourcing](https://www.pcbway.com/pcb_prototype/Electronic_Components.html). [Required BOM+centroid+orientation](https://www.pcbway.com/smt_ordering_guide.html).

**Source of truth** `COMPONENT_AUDIT_R24.csv`: one row per physical PCB footprint. At generation 122 references, including holes/testpoints. `IDENTIFIED` means likely exact part but not approved; `UNSELECTED` covers still-generic passives; `PLACEHOLDER` cannot be ordered; `PCB_FEATURE` is not populated by pick-and-place. `QUALIFIED` demands all five QA flags YES and vendor MPN. Never auto-mark approval.

The normal checker (`python hardware/mainboard/tools/check_component_manifest.py`) fails when the actual KiCad footprint, solder side, XY center or rotation drifts without component review. The `--release` gate must remain red until PCBWay supplier confirmation, exact mechanical models and ECAD are correct. PCB feature mating components are additionally reviewed in mechanical release audit.

Immediate engineering blockers: C915811 four-terminal switch requires 2-pin schematic migration, PCB recessed milling approval; J2 card orientation, J5 7mm recess, M2 mounting projection, J1 battery mate/NTC polarity, SW1 hard-disconnect ratings. The project can pass normal structural CI without claiming production readiness.
