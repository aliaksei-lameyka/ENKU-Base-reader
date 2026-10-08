# ENKU Base R33 — PCBWay readiness

**30/100% estimated, RELEASE BLOCKED**. R32 latest verified [Native KiCad 37795602991](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37795602991): 229 non-unrouted DRC, 255 unconnected, 0 schematic parity, 0 copper shorts, 0 unqualified footprint library absences.

R33 introduces actual mechanical switched converter VIN/EN/Cin after SW1, rather than EN-only. This leaves charger BQ25185 and battery connected. Direct always-on VBAT→BAT_ADC resistor chain may backfeed unpowered MCU; block release until electrically isolated/validated. EPD pin5 VDHR vs VSH2 contradictory Good Display datasheet pages 6 vs 19, written supplier clarification mandatory. R33 new Native ERC/DRC counts are pending; new source-level tests protect all 24 J3 pins and power domain.

Remaining 255 unrouted, full DRC (incl silk/library), mechanical and real BOM/assembly, FPC fold, actual hard switch MPN and bench measurements; no Gerber release. 
