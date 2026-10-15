# Current ENKU Base state

R144 on `engineering/r144-power-margin`. PCB SHA256 `676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c`. Native DRC/ERC/opens/parity0 and complete independent audits passed locally and in [run38693384483](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38693384483), verified source 609f8ac00357b9b0c6b3c43c381469c498453a11. Server artifact and24 fresh exports match except declared creation timestamps.

TPS389001DSER, precision sense/feedback, nominal3.220352V and forced PWM after soft-start. Initial/solder-shift static targets pass.141 refs /473 pads /384 vias /120 fitted top /19 bare /R67+R99 DNP.16 uniquely named enabled layers,93 hidden refs/134 hidden values inventoried.

**NO FAB. Physical tests NOT RUN.** Lifetime drift/dynamic rails, real FPC/case, protected pack/NTC, common manufacturing process and reproducible FCT firmware/per-board evidence remain open. See [risks](STARTUP_RISKS_R144.md), [executed checks](PRE_REVIEW_CHECKS_R144.md), [FPC](FPC_CONNECTOR_REVIEW_R144.md), [pilot plan](FCT_PLAN_R144.md), [packet](../hardware/mainboard/r144/pcbway/). Historical R138/R141/R142/R143 unchanged.
