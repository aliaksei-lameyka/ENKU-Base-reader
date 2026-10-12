# ENKU Base R36 — PCBWay readiness, verified 2026-10-08

**Milestone-based readiness: 30/100. DO NOT FABRICATE.**

Current source: `hardware/mainboard/kicad/enku-mainboard-r1.3-base-first-power-copper.kicad_pcb`. 125 footprints, 4 copper layers, **19 routed segment records and one 0.70/0.30mm plated through-via**, local AO3401A PMOS gate/VSYS/SYS_EN only.

## Native verification (actual results)

- [R36 KiCad 8 native verification run 37803618133](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37803618133) **SUCCESS** after split at explicit x58.7/y85.1 T-junction. Strict ERC **0 errors/0 warnings**, PCB↔schematic parity **0**, no copper shorts, mask bridges, critical hole/edge clearance or dangling ends.
- [Hardware structural + 125-footprint source run 37803618146](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37803618146) **SUCCESS**.
- Native KiCad: **236 non-unrouted DRC violations** — 124 `lib_footprint_mismatch`, 69 `silk_over_copper`, 27 `silk_overlap`, 16 `text_height`. **260 unrouted items**; `footprint_errors` 0. DRC as a whole still **FAILS** despite strict priority violations being absent.
- R35 baseline: 236 non-unrouted DRC, **267 unrouted**. First copper has reduced unconnected items by **7** but is not electrically complete.
- Initial R36 prototype had **one track_dangling** branch (KiCad issue on SYS_EN line at x59.0/y84.8). Corrected by splitting trunk at x58.7/y85.1; `track_dangling` is a hard-fail category in R36 CI. Keep failed verification in history.

## Non-negotiable PCBWay blockers

First copper does NOT yet link BQ25185 SYS output U3 to Q2 high-side source; SW1 long low-current gate wire, other 3V3 power outputs and the GND planes also remain unrouted. All display FPC signal and high-voltage EPD island routing pending.

Manufacturer Good Display was emailed. **J3 contact 5 is `VDHR` in official pin table but `VSH2` in application diagram**; keep existing EPD_VSH2 candidate net and 3D bend/connector orientation unresolved until written vendor answer. Base no Hall/Qi/frontlight; separate Pro PCB.

Pending vendor MPN and final 3D: physical slide switch and panel FPC, protected battery and custom 3-wire NTC cable/polarity, four side buttons, glass-safe mounting, USB-C mating, service/dock connector, AO3401A thermal at load/inrush and charger/USB/dock off-state backfeed. Still need full 4-layer copper/returns, fabrication DRC=0, supplier BOM/CPL, PCBWay Gerber/NC-drill (plated/NPTH) and assembly drawings.

Do not raise readiness percentage for an ERC-clean but **260-connection incomplete** prototype.
