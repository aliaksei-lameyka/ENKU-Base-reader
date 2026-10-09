# R44 — case slide SW1 to Q2 gate and ground electrical copper

**Active PCB**: `hardware/mainboard/kicad/enku-mainboard-r2.1-base-sw1-gate-trial.kicad_pcb`. R43 remains an immutable native-verified rollback.

Actual high-side gate path added:
- Slide SW1 pad1 `PWR_GATE` (27.3,29) -> F.Cu via (26,31) -> **B.Cu switch return corridor** around congested USB/SD and ESP32 underside -> via (53,79.5) -> F.Cu existing gate net at (53,81.55), physically joins Q2 gate and R40 pull-up. Split the horizontal former pad-join at (53,81.55) to provide an explicit Tee; no implicit mid-line connectivity.
- Slide SW1 pad2 GND (33.7,29) -> F.Cu around top of MCU to via (47.5,36.5), tying to both inner GND polygons when Native KiCad refills. No direct 5V or regulator load current through switch; charger and LiPo remain live when OFF.
- 28 net-new KiCad copper segment records including split (442→470), three Ø0.7/0.3mm PTH vias (121→124), still 132 footprints and two inner GND zones.

**Electromagnetic and switching caution:** SW1 gate is very long and relatively high-impedance (R40 100k) and passes past MCU+microSD on B.Cu. This is **a provisional connectivity path**, not an approved EMI-immune final route. Bench verify ESD at switch, RC/dVdt and reliable OFF at battery/cable/dock ranges, gate pull-up effective with dropouts, PMOS VGS limits/inrush. If failure occurs, change topology/return path and keep rollback. SW1 physical land remains only `ENKU:HARD_POWER_SWITCH_PLACEMENT`, supplier MPN and actuator dimensions unqualified. **Do not fabricate board based on this pass alone.**

**Other uncompleted R44 nets**: U1 pads4–7 BTN_L1/L2/R1/R2; risky naive fanout from MCU intersects existing ESP_EN, BOOT, 3V3 and via channels (R43 preflight). Defer these until buttons/MCU fanout safely escape, do not cross RF antenna. J5 native USB D+/D− not routed pending real PCBWay stackup. No changes to GoodDisplay FPC and disputed pin5 VDHR/VSH2 while vendor response outstanding.
