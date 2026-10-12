# ENKU Base mainboard

Current R136 engineering source starts from the history-preserving R135/main merge`1a29692`; **NO FAB**. Open [the canonical KiCad project](kicad/enku-mainboard-r0.1.kicad_pro). Local native KiCad10.0.7 DRC0/ERC0/opens0/parity0,23 scopes and8 rejection cases pass; actual immutable GitHub run38259293325 passed all9 job steps,24 report/5-plot artifact and8 rejection cases; SHA/API digest/CRC verified. [Actual proof](../../docs/GITHUB_NATIVE_R136.md).

C9 increases10uF→22uF with a finite MPN/value metadata change. All physical copper/pad/placement/net/mask/paste/outline/USB/RF geometry and prior evidence remain. C9 max height rises0.95→1.45mm; local case/pack clearance must be reviewed without increasing external case thickness. The thin2000–2500mAh PCM pack, separate attached NTC, PH2, switch pushers and factory/electrical/firmware qualification remain HOLD.

[Current handoff](../../docs/WORK_HANDOFF_R136.md), [capacitance decision](../../docs/CAPACITANCE_R136.md), [supplier status](../../docs/SUPPLIER_STATUS_R136.md), [retained R135 actual proof](../../docs/GITHUB_NATIVE_R135.md). No production/orders/messages.

The original ENKU hardware design is licensed under **CERN-OHL-W-2.0**; see the repository [licensing guide](../../LICENSE.md). Automation scripts in `kicad/` are under MIT.
