# R144 current checkpoint — ENGINEERING / NO FAB

The environment is recovered. Routed source and reproduction scripts are committed. Exact current native KiCad10.0.7 results: **DRC0 / ERC0 / opens0 / parity0**,141 references,473 pads,384 vias. Independent/OEM/manufacturing checks are in progress; physical tests **NOT RUN**.

R98 is now **402 ohm RT0603BRB07402RL**. The nominal PWM supply is3.220352V. The source-bound calculation including a declared extra+/-0.1% solder-shift scenario gives about52.6mV reset-release margin and28.1mV below panel3.3V. Long-term shifts and dynamic qualification remain HOLD. These are calculated conditional envelopes, not prototype results.

U11 is TPS389001DSER:1 SENSE,2 GND,3 MR=3V3,4 VDD=3V3,5 CT,6 RESET_N=ESP_EN. R95=16.5k/R96=10k precise sense divider; C40=100nF delay; C41=1nF C0G sense filter. C15 bypass is relocated. R14=27.4k,R98=402R,R15=5.11k. R97 FIT selects forced PWM after soft-start; R99 DNP provides a future power-save option. Never fit both mode links.

A legacy `=~` operator in the EPD custom rule silently disabled the entire KiCad rules file. R144 replaces it with a finite exact net-name expression and includes an execution sentinel plus an injected unsupported-operator test. Historical R143/R142/R141/R138 sources are not edited. The new U11 manufacturer land exception is confined to its own pad pairs; other clearances remain unchanged.

See [R144 source](../hardware/mainboard/r144/kicad/), [finite delta](../hardware/mainboard/r144/scope_R144.json), [native checkpoint](../hardware/mainboard/r144/checkpoint/), [initial rationale at the preserved earlier commit](https://github.com/aliaksei-lameyka/ENKU-Base-reader/blob/f7c2d512aecee89624672ab036518cfc568b36c4/docs/IN_PROGRESS_R144.md).

Remaining work: independent whole-board/source/export/OEM checks and fault fixtures; final source-pinned server CI; refreshed PCBWay review package, PDFs and README. The original FPC/connector actual-lot/pose, protected battery/NTC, stackup/process, effective capacitance and EPD pulse/HV qualification holds remain open. A reproducible first-boot/FCT image and physical per-board tests are still required before treating5–10 units as qualified.
