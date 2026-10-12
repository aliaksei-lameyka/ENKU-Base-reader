# R133 temperature and charge qualification — HOLD

The normal circuit remains R80 31.6 kΩ, R81 19.6 kΩ and R82 100 kΩ with a real Semitec 103JT-050 sensor attached to the cell. The nominal TI voltage-TS thresholds and the Semitec nominal R/T table do not constitute a guaranteed temperature window.

The new calculation uses the manufacturer's actual R/T points. A table-scaled ±1% R25/B25–85 exercise is explicitly an engineering scenario, since a B25–85 tolerance does not bound the full pointwise R/T curve. Across the stated 4.35–5.25 V scenarios, that exercise leaves only approximately **267 nA at 0 °C and 289 nA at 45 °C** of absolute TS input-leakage allowance. The 100 kΩ series protection resistor makes leakage relevant. No guaranteed TI TS-leakage limit was found in the electrical table; do not mark the window qualified from this calculation.

Nominal sensor self-heating at 5.25 V is about 0.12 °C using Semitec's approximate 0.7 mW/°C dissipation factor. Its approximate 5-second time constant is measured in suspended air, not on a pouch under adhesive and insulation. These values do not establish the actual attachment response or maximum cell-to-sensor temperature difference.

| Fault | Calculation result | Required evidence |
|---|---|---|
| Sensor open or short | Nominal inhibit | Inject at J8 and verify actual battery current and recovery |
| R80 open/short; R81 short | Nominal inhibit | Controlled resistor substitution and current/temperature logging |
| R81 open | At 45 °C the nominal circuit can still allow charge | Assembly fault detection and protection/qualification decision; this is not claimed fail-safe |
| R82 open | TS is floating | Actual input behavior and no-charge evidence; no assumed default |
| R82 short | Series fault protection is lost | Protection and incorrect harness-voltage analysis |
| Sensor detached from a hot cell | A room-temperature sensor can allow charge | Attachment design, mechanical retention and thermal-lag tests |
| Wrong sensor harness voltage | Not bench-qualified | Assess VBAT/VBUS short into J8, series protection and input clamp limits |

Charge setting remains 445 mA nominal, 394.6–492.4 mA with the stated IC/resistor corners. Minimum modeled fast timer is 6.718 hours. Ideal constant-current time at the minimum programmed current is 5.069 hours for 2000 mAh and 6.336 hours for 2500 mAh. The latter leaves only **0.382 hours** before that timer in this simplified comparison. It excludes losses, CV taper, precharge, source/load/thermal limitations and the device's proportional timer behavior. A full 2500 mAh charge is not proved by the nominal 8.725-hour setting.

Use the existing bring-up sequence with a documented bench source, actual protected pack and instrument logs. Record programmed/actual input, battery and system currents; cell, sensor and PCB temperatures; PGOOD/CHG; timer/recharge states and hard-OFF behavior. Run full cycles for each qualified interchangeable pack under the specified loads and temperatures. No automatic CE restart to bypass a timer fault is accepted.

Sources: [Semitec JT](https://www.semitec-global.com/uploads/2022/01/P9-JT-Thermistor.pdf) and [TI SLUS937C](https://www.ti.com/lit/ds/symlink/bq24072t.pdf). Calculations and fault rows are retained in `checks/temperature_FMEA_R133.json`. All instrument and attachment tests remain unperformed.
