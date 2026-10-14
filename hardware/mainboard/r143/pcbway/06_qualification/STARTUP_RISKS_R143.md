# R143: first 5-10 boards, release decision

**Design review completed for the recorded files. EVT manufacturing release: BLOCKED. Physical tests: NOT RUN.**

R143 corrects the Hirose J3 hold-down copper and stencil. Its electrical topology is identical to R142. Source-bound calculations expose a common-rail design margin that must be resolved before calling the design robust. A clean DRC does not establish a working product.

| Priority | Finding from exact source and primary documents | Required closure |
| --- | --- | --- |
| 1 | U4 TPS63802 MODE pin2 is GND, permitting PFM. TI's +/-1% feedback accuracy is specified in PWM. The shared ESP32/panel rail has conditional static PWM limits3.199451..3.291805V, versus panel operative max3.3V and U11 max rising3.188724V. Static margins are only8.195mV above and10.727mV below. | Redesign or demonstrate a defensible bounded joint supply/reset solution, then reverify source and manufacturing data. Qualify actual PFM/no-load/startup/line/load excursions. A MODE-only or feedback-only change is not accepted as closure. |
| 2 | Exact panel drawing permits FPC thickness0.25..0.35mm; exact Hirose spec permits0.27..0.33mm. Nominal fit does not cover the complete drawing tolerance. Folded pin1 and GDEM/GDEY CAD identity remain unverified. | Guaranteed actual-lot dimensions/connector acceptance and folded assembly drawing with pin1 datums, coverlay, latch and strain relief. No guessed tape/shaving/substitution. |
| 3 | BQ24072T power path and OFF behavior are wired, but mainboard has no battery PCM. TS corner calculations use a declared100nA leakage scenario rather than a guaranteed TI leakage envelope. | Qualify the actual protected two-wire pack, PH2 polarity, pulse current and separate bonded NTC R/T/leakage/thermal behavior. Default OFF charging is USB100, not guaranteed500mA. |
| 4 | Native manufacturing files are consistent.84 nominal0.2mm bores on1.6mm PCB, six in-pad fill/cap sites, short USB stakes and common stencil still need process acceptance. | Actual stackup/90-ohm USB, hole/registration/barrel tolerances, resin fill/copper cap, stencil/reflow and BOM/CPL import approval. Hirose peak<=250C and above230C<=60s must fit the common profile. |
| 5 | No built/reviewed first-boot test binary or actual board logs accompany this hardware. | Build an exact N16R8 FCT image, pin map and reproducible hashes before assembly. Test ROM recovery and each physical board; do not infer firmware correctness from PCB connectivity. |

## Independent margin feasibility calculation

For an explicitly declared project reserve of50mV below the supervisor release and25mV below the panel upper limit, even perfect feedback resistors and PWM+/-1% would require nominal voltage simultaneously:

- >=(3.188724+0.050)/0.99 =3.271438V;
- <=(3.300-0.025)/1.01 =3.242574V.

These intervals do not overlap. The reserves are engineering targets, not vendor specifications. This proves that changing only the feedback resistor ratio cannot satisfy those targets with the current supervisor. It is not a measured failure probability or a claim that every nominal board will fail.

TLV803EA29 is not blindly substituted: its lower release can allow an ESP32 supply below3.0V on a slow ramp. TPS3808EG33 also is not a simple improvement: the guaranteed fixed-threshold error is+/-1.5% and maximum hysteresis2.5%, not the typical headline accuracy. An adjustable precision supervisor or separate panel/logic supply architecture must include tolerance/leakage/timing, I/O levels and OFF/back-power behavior. TPS389001 was reviewed as an architecture candidate only; it is **not fitted** in R143.

## Primary documents reread

- TI [TPS63802 SLVSEU9D](https://www.ti.com/lit/ds/symlink/tps63802.pdf): pin/mode table, PWM accuracy, PFM operation and typical ripple/load/line behavior, effective-capacitance requirements and layout.
- TI [TLV803E SLVSES2J](https://www.ti.com/lit/ds/symlink/tlv803e.pdf): A30 actual threshold3.08V, +/-2%, hysteresis0.9..1.5%, delay130..270ms, exact standard DBZ pinout.
- Supplied GDEY0397T81P SHA256 `e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc`: pp5/6/8/19. Exact24-pin map, VCI2.2..3.3V, VDDIO tied to VCI, panel reference booster.
- [Espressif WROOM datasheet v1.8](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf): N16R8=16MB Quad flash and8MB Octal PSRAM; GPIO35..37 unavailable;3.0..3.6V; default flash max80MHz. Module pad32 is GPIO39.
- TI [BQ24072T SLUS937C](https://www.ti.com/lit/gpn/bq24072t): reverse blocking/DPPM, input-limit modes, battery regulation, NTC/timer, capacitors and thermal behavior.
- [Bosch BMI270 DS000-08](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf): exact pin/interface configuration and initialization sequence. Confirm INTERNAL_STATUS low nibble=1 after configuration, not merely one set bit.
- TI [TPS3808E SNVSCE0B](https://www.ti.com/lit/gpn/tps3808e), [TPS3890 SLVSD65A](https://www.ti.com/lit/ds/symlink/tps3890.pdf): alternative threshold/hysteresis and required footprint/timing differences. Neither is installed.

Exact-passive, active-IC, capacitance, EPD current/pulse and assembly guards retain their source manifests and explicit scenario/unknown labels. Typical MLCC DC-bias curves and typical hot inductor current are not converted into guaranteed bounds.
