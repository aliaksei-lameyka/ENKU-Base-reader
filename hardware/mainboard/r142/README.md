# R142 engineering source - NO FAB

Open `kicad/enku-mainboard-r0.1.kicad_pro` for the current PCB and five schematic sheets. Revision R142 is recorded in the title blocks; the retained r0.1 basename preserves the project hierarchy.

R142 adds a reset supervisor, external microSD detection and all CMD/DAT pullups; corrects the joint ESP32/panel supply budget; and reroutes copper away from Hirose mounting-face no-pattern regions. Original board outline, component pad definitions, USB differential geometry and project rules are preserved. Only C15 moves among original components; R14/R15 use precision RT resistors on the same physical lands. R23 becomes 10k.

The isolated workflow verifies current sources with immutable R138 and R141 references. `checks/` contains explicit R142 scopes. Runtime helpers and unchanged guards come from `hardware/mainboard/kicad/checks/`; do not regenerate historical goldens.

See [review findings](../../../docs/PRE_REVIEW_CHECKS_R142.md), [source manifest](source_manifest_R142.json) and [PCBWay review package](pcbway/). Physical tests, exact panel pin5/FPC confirmation, battery PCM qualification, case fit and manufacturer process acceptance remain open. No factory upload or order has been performed.
