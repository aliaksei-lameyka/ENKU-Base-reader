# ENKU Base mainboard

Current working PCB **R144 / NO FAB**, branch `engineering/r144-power-margin`. [Project](r144/kicad/enku-mainboard-r0.1.kicad_pro), [review packet](r144/pcbway/), [source/checkpoint](r144/README.md), [current status](../../docs/CURRENT_STATUS.md).

TPS3890 reset + nominal3.220352V PWM supply. Full native/independent local and [server verification](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38693384483) passed. Initial/solder static reserves pass; lifetime/dynamic, FPC/pack/process/firmware and physical tests remain open. See [risks](../../docs/STARTUP_RISKS_R144.md), [FPC](../../docs/FPC_CONNECTOR_REVIEW_R144.md), [pilot FCT](../../docs/FCT_PLAN_R144.md). Physical tests NOT RUN. No case-thickness increase or Base dock/frontlight/Hall/Qi.

`kicad/` is immutable R138. R141/R142/R143 are historical controls. No historical guard/golden was changed. Hardware CERN-OHL-W-2.0, automation MIT.
