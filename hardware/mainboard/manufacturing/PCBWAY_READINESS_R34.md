# ENKU Base PCBWay readiness R34

**Estimated 30/100, NOT released**. Current active R34 board `enku-mainboard-r1.1-base-gated-battery-adc.kicad_pcb`. Added U9 TMUX1101DBVR, C37 100nF input decoupler, R39 1M pull-down, BAT_ADC_SW gating R26 divider. Board population **123** (+3 vs R33). Real 3.3V-off ADC backfeed must still be measured; schematics and footprints vendor reviewed but not bench-approved.

Previous validated [R33 Native KiCad run 37796802448](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37796802448): 229 DRC non-unrouted, 255 unrouted, 0 PCB-schematic parity. **R34 counts unknown until its own Native run**. A pass of diagnostic tests never means production-ready.

Open blockers: remaining off-state charger/STAT/backfeeding paths; LiPo NTC cable and switch MPN, exact pin5 Good Display contradiction VDHR vs VSH2, 3D FPC, display power, footprints 119 source mismatch, full PCB copper routing and PCBWay manufacturing outputs. Do not generate Gerbers.
