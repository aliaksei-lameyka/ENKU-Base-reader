# ENKU Base mainboard

Current working PCB: **R143, NO FAB**, branch `engineering/r143-j3-startup-review`. Open [R143 project](r143/kicad/enku-mainboard-r0.1.kicad_pro). Hirose J3 hold-down copper/paste corrected to0.40x0.80mm. Full local and [server verification](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38615866570) passed on sourcec9dc9e6. Electrical topology is identical to R142; four pad UUIDs alone change physical geometry.

[Startup design margin](../../docs/STARTUP_RISKS_R143.md) still blocks fabrication release. [Current packet](r143/pcbway/), [source](r143/README.md), [checks](../../docs/PRE_REVIEW_CHECKS_R143.md), [FPC](../../docs/FPC_CONNECTOR_REVIEW_R143.md), [pilot plan](../../docs/FCT_PLAN_R143.md). Physical tests NOT RUN. Case thickness is unchanged. Base has no dock/frontlight/Hall/Qi.

`kicad/` is the immutable R138 control; R141/R142 preserve history. R138 whole-repository guards are run in their exact historical snapshot so current README updates do not require rewriting goldens. No supplier message, factory upload/order or procurement is made by this publication.

Original hardware: CERN-OHL-W-2.0. Automation: MIT. See [licensing guide](../../LICENSE.md).
