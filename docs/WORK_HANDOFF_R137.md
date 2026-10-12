# ENKU R137 current engineering handoff — NO FAB

Repository:aliaksei-lameyka/ENKU-Base-reader. Branch:engineering/r137-fabrication-export-review, based on accepted main9859145; all main/engineering licensing ancestry retained. Canonical KiCad project:hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro. Source PCB SHA99f2d9cff7a79cc9347f2430d422493e512e6c3b6d6cf82ffd408e0dd77db798.

Read [actual export repair/review](FAB_EXPORT_REVIEW_R137.md), [complete BAT package audit](BAT_PACKAGE_REVIEW_R137.json), [fresh supplier thread status](SUPPLIER_THREAD_RECHECK_R137.json), [retained latest main R136 proof](GITHUB_MAIN_R136.json), and R136 power/DFM/bring-up documents. R136 accepted capacitor/power/switch/NTC geometry is preserved; R137 corrects silk/layer availability and explicit default-DNP stencil/library only.

Local immutable KiCad10.0.7 passes0 DRC/ERC/opens/parity,25 scopes+checkpoint and13 meaningful rejection cases. GitHub artifact comparison must be recorded against the exact published commit; local freeze is preparation only and prohibited in CI. Selected checkpoint R137/fabrication_ready=false. Previous allR135/R136 reports and binary proofs remain unchanged.

Next substantial engineering pass:repair/qualify165 vias with0.10mm nominal annular rings against PCBWay standard0.15mm, keeping1.6mm PCB, copper connectivity, RF/USB reference, clearance/wick constraints and exact U3 fill/cap process. Read native_export audit's full UUID/position list before changes. Increasing diameter may require local routing changes; a dimension-only global replacement must not be presumed safe. Retain strict native/physical/source guards and verify all new manufacturing output after edits.

Remaining external inputs:current complete case CAD and allowable finished-pack T/W/L;≥2 qualified interchangeable2000–2500mAh thin two-wire PCM packs with CN and PL supply; exact panel/FPC and factory stackup/stencil/PIP/fill-cap acceptance. Do not substitute old10mm SCAD for current approved case or increase case thickness. Current charge path is BQ24072T445mA nominal(max492.42mA),BAT max4.24V; original supplier RFQs still describe obsolete BQ25185/300mA and need correction only in a future user-authorized follow-up.

Physical/firmware qualification is NOT RUN; no fabrication,orders,outreach or factory uploads are authorized. A future concrete EVT package needs owner agreement before manufacture/purchases. Keep engineering branch/history/checkpoints; do not use historical output folders as current fabrication data.
