# R38 — pilot inner-layer GND return, NOT a poured fabrication plane

Branch `engineering/r38-local-ground-return`. Source `hardware/mainboard/kicad/enku-mainboard-r1.5-base-ground-return-island.kicad_pcb`. Retains R37 charger/Q2 and 3V3 pilot copper, introduces 10 GND F.Cu segments, seven Ø0.7mm/0.3mm PTH GND vias and an **In2.Cu only local GND zone polygon x40.5..67.0, y80.2..99.5mm**; GND zone currently defined but *not refilled to actual exported copper*.

GND return pilot connections:
- BQ25185: U3 exposed center pad11 at (48.5,91) to via (48.5,92.35), signal GND pad5 at (49.6,90.2) to via (50.6,90.9). No via in charger solder-paste underpad; center pad may require additional thermal routing and verified EP solder pattern.
- TPS63802: U4 GND pad3 to via (56,91), tied to U4 GND pad2 and large center pad8 by F.Cu 0.18mm traces. Needs source-approved ground pad EP inductive loop and wider copper current path before production.
- Regulator input C9 GND (60.7,87.7) to via (61.6,87.7), C10 GND (63.8,86.5) to via (65.1,86.5).
- Regulator output C11 GND (61.1,94.4) to via (61.1,93), C12 GND (64.3,94.4) to via (65.1,94).
- All vias are intentionally **off the copper pads**, unlike dangerous via-in-pad (unfilled via solder wick risk). 0.30mm PTH default and zone thermal gap .30mm.
- The In2.Cu GND polygon does **not extend to ESP32 antenna area**; this is a **local power return pilot**, not the whole board reference plane. Full stackup/plane merging/no islands and final RF keepouts need review.
- A global filled GND plane cannot be advertised from a source polygon alone. Verify KiCad zone refill and inspect fill islands/clearance when supported, plus check plating and thermal relief of all vias. Native DRC gate still rejects shorting and track_dangling; any new violation is a no-go.

Good Display panel pin5 VDHR vs VSH2 and FPC fold are still awaiting supplier email; no copper/keepout decisions on the EPD connector. Power switch SW1 is a low-current gate-only switch, unqualified mechanical MPN; battery stays on BQ25185 when reader OFF.


## Prevent false plane approval

The first R38 Native DRC reported **7 via_dangling** even though other critical types were zero. Their destination `In2.Cu` polygon was not filled copper. CI now must run KiCad Python `ZONE_FILLER` in a disposable copy, serialize real filled polygons and re-run Native DRC, hard-failing `via_dangling`. The source board retains unfilled zone as an editable KiCad polygon; Native diagnostic artifact is not PCBWay-ready Gerber.
