# R136 first-board validation additions — physical tests NOT RUN

Use the existing [R135 staged bring-up plan](BRINGUP_R135.md) and [R134 detailed twelve-stage sequence](BRINGUP_R134.md), with the following R136 additions. Manufacturing and purchases still require user approval; these are instructions for approved EVT boards, not reports of performed tests.

Before applying power, verify C9 is22uF10V CC0805MKX5R6BB226, installed on SYS_EN/GND at59.7,87.7mm. Confirm its1.45mm maximum-height clearance with the actual pack, NTC mounting, strain relief and case. Verify battery polarity independently of wire colours; keep the battery disconnected until supply-only rails and controls are checked.

Record PCB/schematic source commit and SHA, board serial, exact assembly lot, cap/sensor/pack part and lot IDs, instrument calibration, fixture and ambient/cell temperature. Retain raw scope/LCR traces and measurement conditions. Empty records and a native-check pass do not count as physical qualification.

Characterise C7/C8/C9/C11/C12 at the actual DC voltages, including4.24V BAT, up to4.59V allocated SYS_EN/VSYS and3.40V output scenario. Use an appropriate external DC-bias fixture and safe isolated part/fixture measurement; ordinary in-circuit LCR readings include parallel capacitance and cannot isolate a part. State frequency, AC amplitude, bias settling, temperature and age. Do not drive external bias into an unpowered MCU or charger measurement setup. Measure several actual procurement samples, with an agreed acceptance basis; preserve uncertainty and unqualified corners.

Capture SYS_EN,3V3,VBUS,VBAT and input/battery current during hard ON/OFF and restart, discharged/full/no battery, USB insertion/removal and agreed100/500mA source policies. Increased C9 is downstream of Q2 and the charger, so retain input-current/inrush/charge-path checks even though direct USB capacitance remains6.8uF nominal. Check supply-limited startup, Q2/charger stress, repeated brownouts and unintended current-mode transitions.

Exercise converter buck/boost transitions and repetitive Wi-Fi, microSD writes and full/partial panel updates. Check overshoot/undershoot, recovery, rail ripple, reset cause and thermal behavior with all nine direct output capacitors plus the actual ESP/panel loads. A positive small-signal capacitor scenario is not converter-loop or USB compliance validation.

Retain the R135 stricter4.90–35.01°C nominal charge-window checks, R81-open scenario, sensor-open/short/detachment, R82-open fault handling, loaded control GPIO, boot/ROM/reset/OFF/suspend and whole charging-cycle tests. Detached sensor and a floating TS node remain unqualified; do not relabel their behavior as fail-safe.
