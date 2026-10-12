# ENKU Base R131 thin-battery handoff

Continue from **`engineering/r131-thin-battery`**, based on R130 proof commit `04a8344f1f71e6bdebb8cb8815ccbac8292fa6cc`. Canonical hardware remains **R130**, selector R130, `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. This pass changes battery selection/evidence only; source, libraries, routing, project, workflow and all previous guards remain unchanged. Do not restart from stale main or run an old revision mutator.

Hard constraint: **no increase of enclosure thickness**. Retain ≥2000 mAh, standard replaceable two-wire 1S/4.20 V protected LiPo with separate real cell NTC. Orders/manufacturing remain unauthorized.

Provisional primary is **Koosay 335084**, advertised 2000 mAh, nominal cell 3.3 × 50 × 84 mm. Thinner alternative 325381 is 3.2 × 53 × 81 mm. The primary trades 0.1 mm thickness for 3 mm less width: at X26.75/Y28 it remains within the actual board, unlike the alternative's 2.75 mm overhang. Its assumed right-edge gap is still short by 0.25 mm. Neither model is a qualified finished protected-pack SKU; both catalogue rows show zero stock cells. Minimum capacity, finished maximum dimensions and model-specific 4.20 V chemistry remain unconfirmed.

[Selection and bounded primary-source comparison](BATTERY_THIN_SELECTION_R131.md), [structured decision](../hardware/mainboard/bom/battery_selection_R131.json), [source register](../hardware/mainboard/bom/battery_sources_R131.json), [audit](../hardware/mainboard/mechanical/thin_battery_audit_R131.json).

Fresh checks re-verified actual R130 KiCad 10.0.7 CI artifact CRC/SHA256, exact native geometry and native STEP. A new analytical/CadQuery study identifies **250.272 mm³ nominal PH-2 reservation overlap** for the low 3.3 mm cell. A continuous interval proof shows translating that pouch alone cannot clear J1 within the declared board/RF/boss region. The historical fixed 10 mm reference has PH-2 0.734998 mm above its assumed rear inner plane. The accepted tree has no registered current complete enclosure CAD, so do not claim that 10 mm is verified current thickness or that this failed trial is an assembly release. No new native KiCad CI run was claimed for unchanged hardware.

Retained actual [native R130 proof](GITHUB_NATIVE_R130.md): source `889a069afb8aed9515fbff6daba5f5e659ff9753`, run 38153676192, all 12 server steps; ERC 0 / opens 0 / parity 0 / DRC 20 unchanged holes / library 0. Seventeen guards, 428 pads, 118 footprints, 2641 copper items. Earlier work remains preserved.

Next: solve battery/connector/tall-component topology within the fixed case constraint using actual enclosure/panel/FPC and finished-pack dimensions; then a concrete PCB placement/routing change and actual native KiCad checks. In parallel resolve 0–45 °C independent hardware charge inhibit and full-capacity charge architecture. Retain PCM/polarity/NTC fault/OFF-mode checks and the existing hole/process/stackup/stencil/EPD/USB/prototype gates.

All three existing supplier threads were checked; no replies/attachments or duplicate enquiries. No orders, manufacturing release or main merge. **fabrication_ready=false**. Hours count only the observed current task interval; historical total remains unknown.
