# R130 battery and sensor service interface — qualification draft

Only a qualified protected1S4.20 V LiPo of2000–2500 mAh may be accepted after charge, case and PCM gates close. R130 is currently engineering HOLD.

| Reader interface | Required mating item | Controlled mapping |
| --- | --- | --- |
| J1 JST S2B-PH-SM4-TB(LF)(SN) | JST PHR-2 housing +2 SPH-002T-P0.5S contacts, correct wire/tooling | Cavity1 VBAT(+), cavity2 GND; numbered mating cavities, not wire colors |
| J8 bare hand-solder terminals | Separately retained Semitec103JT-050 candidate with insulated termination tails | Pin1 TS/MR, pin2 GND; no polarity intrinsic to thermistor |
| Akyga AKY0156 stock connector | JST SYP-02T-1,2.54 mm | Cannot plug into PH2.0; separately qualified conversion required |

Mounting-side PCB view has J1 pin1 below pin2 and opening to+X. Looking into a mating cable may mirror that view; identify numbered housing cavities and measure the assembled cable before connection. Keying does not establish supplier battery polarity.

The sensor belongs to the reader and remains retained against the pouch after cell replacement. Its lead strain relief must be independent of the pouch seal and hand-solder joints. Insulate exposed tails, prevent sharp edges/pinch points and compression, and obey Semitec solder/bend limits: avoid heating the film above150°C, do not bend within7 mm of the sensor, and do not assume repeated bending is allowed. The strip, attachment material, extension tails and retention fixture are not frozen assembly parts.

Prototype qualification must verify replacement restores flat thermal contact and no wire load on the pouch. Record actual sensor resistance at a known temperature, terminal continuity and pack polarity with the cell/USB disconnected. A detached sensor can read a valid ambient resistance. It is not detected by ERC or by the charger's nominal-temperature state.

Safe fixture test cases: cold/hot trip and hysteresis, sensor open/short/displaced, absent battery, USB-present battery unplug/replug, off/on/deep-sleep, deep-discharge recovery, charge termination/timer, pack PCM/current limits and wrong-harness risk. None are recorded as passed. Do not run unattended or uncontrolled cell abuse tests.
