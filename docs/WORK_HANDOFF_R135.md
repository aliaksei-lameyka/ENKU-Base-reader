# R135 verified engineering handoff — NO FAB

Continue branch `engineering/r135-switch-ntc-review`, canonical `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`. Parent R134 d8677378bef58f3e76ef6b6839883fb09286cd18 and1038 earlier files/evidence are preserved. Board59×101×1.6mm, fixed case thickness,2000–2500mAh thin two-wire PCM battery and separate attached NTC remain requirements.

## Actual current evidence

**Native KiCad10.0.7 DRC0/ERC0/opens0/parity0;22 independent guards plus checkpoint comparison pass.** [Fresh immutable-source run38252194674](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38252194674), all8 actual job steps, source`bd3b66bcaf82c6ec734ab01ad0aff57a67a1f25f`. Actual42-member/639719byte artifact SHA/API digest/CRC and all23 report/export results match locally and in an isolated observer. [Full proof](GITHUB_NATIVE_R135.md). PCB SHA256`9c5101ce9b748e19be893f5cc75de55afe5ff6eb01c257cc48fc48c850bcf7df`. Current metadata/evidence commits do not change the verified copper/schematic.

## Changes

SW3–SW6 are actual E-Switch TL1016AAF160QG AA no-boss/no-ground-terminal variant. Four distinct pads:1/2 signal,3/4 GND, explicitly externally routed. Primary P520001A geometry and actual16 physical mask/paste windows verified. Real part replacement removes16 old hole findings without weakening the0.25mm rule, severity or exclusions. Y73/85mm locations and nominal tip planes19.45/75.55mm are preserved; X moves inward0.05mm per side. New lower/rectangular actuator needs an internal case-pusher review; no mechanical drop-in approval.

R80=40.2k1%,R81=33.2k1%, same Semitec sensor and100k R82. R81-open at45°C now inhibits in stated table-scaled resistor/leakage scenarios (350.9nA model budget). **Healthy nominal window4.90–35.01°C**. Detachment, R82/fault isolation, guaranteed RT/TS leakage and physical tests remain HOLD; not all faults are fail-safe. Charger/current/timer, GPIO modes, PH2 and thin-pack architecture stay unchanged. [Detailed decision](SWITCH_NTC_R135.md).

20 finite old-copper removals, one declared3V3 jog and27 added items restore button, C18 and microSD grounds. Every other old physical pad/core position, RF, outline/stack, non-switch zone, USB pair/reference and U3 thermal-via requests is preserved.107 fitted CPL positions and explicit MPNs checked. A stale inherited report counter was corrected to the actual88 checked parts/52 resistors.

## Next work

1. Register complete current enclosure/component CAD; verify new pusher/stroke/axis and resolve PH2/thin-pack collision within unchanged case thickness. Do not treat obsolete10mm reference or nominal cell dimensions as accepted pack space.
2. Obtain two controlled finished PCM pack SKUs fitting one envelope with CN stock and Poland procurement, minimum capacity/pulse/chemistry/polarity documents. Koosay's existing reply asks for a real maximum compartment envelope; it does not approve a thicker battery. No follow-up sent.
3. Complete RT/leakage/detachment/fault, effective capacitor, USB impedance and QFN fill/cap/stencil/short-stake assembly review. Prepare a concrete EVT package after design/factory gates; user approval remains required for fabrication or parts purchases.
4. Implement boot/current-mode/suspend/CE/MSC firmware and execute [first-board tests](BRINGUP_R135.md) after approved boards arrive; full charge/thermal/USB/fault qualification precedes production.

[Current gates](DFM_REVIEW_R135.md). No production, orders or outbound supplier messages. Earlier R135 checkpoint handoffs/partial routing snapshots are historical; use this source/proof. Development ledger updated through actual proof capture.
