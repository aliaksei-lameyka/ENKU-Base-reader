# R136 input-capacitor review — NO FAB

C9, immediately on the TPS63802 SYS_EN input, changes from Yageo CC0805KKX5R6BB106 (10uF10V10%) to **CC0805MKX5R6BB226 (22uF10V20%)**. This existing project MPN is also used at C7/C8/C11/C12. Only C9's Value, MPN, Datasheet and Description change in the PCB and power sheet. All copper, pads, placement, mask/paste, net connections, USB/RF/outline/stack and thermal process requests remain identical to accepted R135. All earlier source and evidence remain.

The exact downloaded Yageo simulations were visually inspected, including the page2 DC curves, page1 package dimensions and page4 limitations. Their generated header is11Oct2026; the live web renderer also returned an12Oct rendering with a different graph arrangement. Downloaded byte hashes and the precise document used are retained in `checks/capacitor_sources_R136.json`; do not silently interchange generated sheets. These curves describe typical responses and **are not a manufacturer guarantee**.

The inherited R135 C9 scenario used70% DC retention at4.59V. The inspected10uF curve is nearer63%; the revised rounded-down60% project scenario gives only4.131uF after10% initial tolerance,15% temperature allowance and10% ageing reserve. This is only3.28% above TI's4uF minimum, before unbounded lot/AC/interaction effects. Replacing C9 provides useful margin within the same lands.

| Network | Bias scenario | DC retention scenario | Budget after tolerance, temperature, ageing and DC | Target minimum | Modeled margin |
|---|---:|---:|---:|---:|---:|
|Old C9 10uF|4.59V|0.60|4.131uF|4uF|3.28%|
|New C9 22uF|4.59V|0.40|5.3856uF|4uF|34.64%|
|C7 VSYS 22uF|4.59V|0.40|5.3856uF|4.7uF|14.59%|
|C8 BAT 22uF|4.24V|0.45|6.0588uF|4.7uF|28.91%|
|C11+C12 local output|3.40V|0.55|14.8104uF|7uF|111.58%|

The four22uF retention factors are rounded below the viewed typical curve. The15% temperature reduction and10% ageing reserve are project budget factors, not simultaneous guaranteed manufacturer corners. AC amplitude, temperature/bias/age interactions, manufacturing variation and actual ripple remain unqualified. A positive model result must not change a release or qualification flag to PASS.

SLUS937C p8 specifies BQ24072T BAT4.16/4.20/4.24V; p7 specifies tracking up to VBAT+270mV, giving4.51V before allocated margin. The4.59V SYS_EN/VSYS budget is retained. The3.40V steady output scenario covers the conditional1% PWM feedback and1% divider-ratio calculation (3.398V); PFM peaks, transient overshoot and actual regulation require measurement. SLVSEU9D p5 requires effective input≥4uF and output≥7uF for output>2.3V.

The direct output inventory includes **nine** board capacitors: C11,C12,C13,C14,C16,C17,C18,C19,C38, nominal64.5uF total. The local minimum calculation deliberately uses C11/C12 only. Downstream capacitor/network/panel dynamics are not a stability qualification. Direct VBUS inventory stays C2/C4/C5/C6, nominal6.8uF; no direct USB input capacitor is added. Increasing switched SYS_EN capacitance still changes startup demand through Q2/BQ24072T, so USB inrush and reset behavior are not declared unchanged.

**Mechanical consequence:** old C9 max height0.95mm; new C9 max height1.45mm. L/W and land geometry remain the same. The new height equals existing C7/C8/C11/C12, but it requires local clearance validation at59.7,87.7mm. No external case-thickness increase is allowed or approved. Do not call this a fully qualified mechanical drop-in.

Before design release, obtain a sufficiently bounded Ceff acceptance basis or approved measurement method for exact procurement lots and conditions. After approved EVT, measure biased capacitance with appropriate LCR/bias fixtures, effective small-signal/ripple conditions, then capture SYS_EN/3V3 at startup, brownout, battery2.5/3.0/3.6/4.24V, USB low/high voltage and authorised current modes, Wi-Fi load steps, microSD writes and full panel updates. Observe converter recovery, overshoot, Q2/charger input demand and both replacement packs. Physical tests are **NOT RUN**.
