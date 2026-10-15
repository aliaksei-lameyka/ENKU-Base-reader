# R144 first 5-10 boards: release constraints

**Engineering checks PASS; manufacturing release NO FAB; physical tests NOT RUN.**

The R143 common-rail margin was addressed by a joint supply/reset redesign. TPS389001DSER with R95=16.5k/R96=10k senses the rail, C40=100nF delays reset and C41=1nF C0G filters sense. U11:1 SENSE,2 GND,3 MR to3V3,4 VDD,5 CT,6 RESET_N to ESP_EN. Existing R17 pullup and J7 wired-OR reset remain. R14=27.4k, R98=402R, R15=5.11k, all0.1%10ppm. Nominal3.220352V. R97 FIT selects forced PWM after soft-start; R99 DNP. Never fit both. Initial converter soft-start uses PFM. Idle efficiency/battery life must be measured.

These are independent linear static corners using TI guaranteed PWM feedback +/-1%, feedback/sense bias and threshold errors, hysteresis and the declared resistor error/TCR envelope. They are not a converter transient model. The50mV release and25mV panel-ceiling reserves are project targets, not manufacturer requirements.

| Resistor scenario | Regulator PWM V | Release reserve mV | Below panel3.3V mV | Falling threshold min>=3.0V |
| --- | --- | --- | --- | --- |
| initial_only | 3.174623..3.266354 | 61.843 | 33.646 | True |
| initial_plus_0p1percent_solder_shift | 3.169266..3.271879 | 52.601 | 28.121 | True |
| initial_plus_0p1percent_solder_plus_0p5percent_life_shift | 3.142643..3.299673 | 6.432 | 0.327 | False |

Initial and declared extra +/-0.1% solder-shift scenarios meet the targets. An additional independent adverse +/-0.5% life-shift scenario does not: minimum falling threshold can fall below3.0V and static reserves are insufficient. This scenario is not a field-failure probability or qualified actual-lot drift. Resolve lifetime requirements/part lot evidence and actual slow-ramp behavior before production release. Dynamic ripple/load/startup/fast-dip/OFF/USB back-power remain unmeasured. C40 nominal delay is about107ms, scenario59..181ms, conditional on effective capacitance/leakage. Measure it.

| Remaining item | Required evidence |
| --- | --- |
| Panel/FPC | Felix confirmed VDHR=VSH2 and supplied DIANWEI orientation, bend1-1.5mm and glass gap>=2mm. Apply bend>=1.5mm. The installed Hirose is a different footprint. Actual-lot FPC thickness/width/finger/coverlay acceptance, folded pin1 and GDEM/GDEY CAD identity remain open. |
| Battery/NTC | Qualified thin protected2000-2500mAh two-wire PH2 pack, correct polarity/PCM/pulse current, separately cell-bonded NTC and thermal/fault behavior. No mainboard PCM/fuel gauge. USB100 alone does not guarantee startup without battery. |
| Process | Actual90-ohm USB stack,84 nominal0.2mm bores on1.6mm, six resin-fill/copper-cap sites, short USB stakes, common U11/Hirose stencil/reflow and BOM/CPL import approval. |
| EPD power | Actual MLCC effective capacitance including differential voltage, Q1/diode overshoot, L2 hot peak/RMS/saturation, R37 repetitive pulse temperature and real-panel refresh. Typical curves/Isat are not minimum guarantees. |
| Firmware/FCT | Reproducible N16R8 first-boot binary and per-board raw logs/waveforms, UART/USB ROM recovery, memory patterns, SD hashes/MSC ownership, BMI config/self-test/IRQ and panel/combined-load/OFF/charging tests. |

Within the proposed5-10 unit pilot, bring up1-2 units first and diagnose failures before the remainder. All physical results remain NOT RUN. No order, supplier message or purchase is authorized by this document.

Primary references: https://www.ti.com/lit/ds/symlink/tps3890.pdf (DSE0006A drawing4220552/B, pp25-26); https://www.ti.com/lit/ds/symlink/tps63802.pdf; https://www.ti.com/lit/ds/symlink/bq24072t.pdf; supplied exact GDEY0397T81P pp5/6/8/19; Hirose EDC-159714-50-08 and ELC4-159714-04; Espressif WROOM v1.8; Bosch BMI270 DS000-08. Supplier files remain private; hashes/page references are in the reports.
