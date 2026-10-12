# ENKU Base mainboard

Accepted R135 in `main`; **NO FAB**. Open [the canonical project](kicad/enku-mainboard-r0.1.kicad_pro). Actual immutable-source KiCad10.0.7 [run38252194674](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38252194674): DRC0/ERC0/opens0/parity0,22 independent scopes and checkpoint comparison. Actual23-report artifact and five native exports match; API binary SHA/CRC verified.

New no-boss side switches remove16 old locator findings. R80/R81 bias addresses the R81-open hot fault in a bounded model; nominal healthy window4.90–35.01°C. Fixed59×101×1.6mm PCB, case thickness ceiling, thin2000–2500mAh PCM pack and separate attached NTC are preserved. New internal button pusher, full PH2/battery/enclosure fit, supply/process/thermal/firmware qualification remain HOLD.

[Current handoff](../../docs/WORK_HANDOFF_R135.md), [actual proof](../../docs/GITHUB_NATIVE_R135.md), [release gates](../../docs/DFM_REVIEW_R135.md). No production/orders/messages. All earlier source/evidence retained.

The original ENKU hardware design is licensed under **CERN-OHL-W-2.0**; see the repository [licensing guide](../../LICENSE.md). Automation scripts in `kicad/` are under MIT.
