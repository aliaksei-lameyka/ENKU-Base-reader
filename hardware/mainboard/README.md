# ENKU Base mainboard

Current working PCB: **R142, NO FAB**, branch `engineering/r142-startup-independent-review`. Open [R142 KiCad](r142/kicad/enku-mainboard-r0.1.kicad_pro). Native KiCad10.0.7 DRC0/ERC0/opens0/parity0 and independent manufacturing/conductor checks pass on the recorded source. See [current status](../../docs/CURRENT_STATUS.md), [source and packet](r142/README.md), [pre-review](../../docs/PRE_REVIEW_CHECKS_R142.md) and [Good Display / Hirose comparison](../../docs/FPC_CONNECTOR_REVIEW_R142.md). The original `kicad/` tree is the immutable R138 comparison baseline, not the working candidate.

R142 adds reset/card detection/all SD pullups, precision joint logic/panel supply feedback and Hirose microSD keepouts. The14Oct FPC document pass closes pin5 naming and records numerical bend limits, without changing PCB/production bytes. Guaranteed FPC tolerances/folded pose, enlarged J3 hold-down process, thin2000–2500mAh PCM pack, attached NTC, PH2, switch pushers and factory/electrical/firmware qualification remain HOLD. Case thickness must not increase.

Retained history: [R136 handoff](../../docs/WORK_HANDOFF_R136.md), [capacitance decision](../../docs/CAPACITANCE_R136.md), [dated supplier status](../../docs/SUPPLIER_STATUS_R136.md), [R136 actual proof](../../docs/GITHUB_NATIVE_R136.md), [R135 actual proof](../../docs/GITHUB_NATIVE_R135.md). No factory upload, order or production release has been made.

The original ENKU hardware design is licensed under **CERN-OHL-W-2.0**; see the repository [licensing guide](../../LICENSE.md). Automation scripts in `kicad/` are under MIT.

