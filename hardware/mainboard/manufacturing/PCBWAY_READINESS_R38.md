# ENKU Base R38 — verified PCBWay readiness (2026-10-08)

**30/100 preliminary milestone score — manufacturing RELEASE BLOCKED.**

Active source: `hardware/mainboard/kicad/enku-mainboard-r1.5-base-ground-return-island.kicad_pcb` (125 footprints, 48 routed segments, 13 PTH vias, one editable In2.Cu GND zone polygon).

## Actual KiCad results

- [R38 Native KiCad 8 real-zone-fill run 37805934639](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37805934639): **SUCCESS**: `pcbnew.ZONE_FILLER` filled **one GND copper polygon on In2.Cu**, saved/reopened the filled board and DRC checked that serialized result.
- ERC **0 errors / 0 warnings**; PCB↔schematic parity **0**; native priority errors **0** for shorting, mask bridges, copper/board edge and trace/via dangling. **0 dangling GND vias after native fill.**
- **236 non-unrouted DRC violations remain**: `lib_footprint_mismatch` **124**, `silk_over_copper` **69**, `silk_overlap` **27**, `text_height` **16**. **245 unrouted items**; `footprint_errors` **0**. This is diagnostic CI SUCCESS, **not** whole-board DRC PASS.
- [R38 hardware check](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37805601290) confirmed 125 footprint placement, pad clearances and GND source connectivity placeholders.
- R37 baseline Native had **254 unrouted** and 236 non-unrouted DRC. Native GND return pilot improved to **245 unrouted** (−9).

## Known issue and fix: false zone success

First R38 native run [37805601445](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37805601445) detected **7 `via_dangling`** because it evaluated an unfilled zone and the earlier script did not make `via_dangling` fatal. Revised CI fails if pcbnew filling fails, if saved copper polygons are absent, or if post-fill `via_dangling`/`track_dangling` persists. The fully filled *diagnostic* KiCad board is attached to run 37805934639, not silently promoted to the editable source or production outputs.

## Still blocks PCBWay

- 245 unrouted electrical connections, U4 ground/EP current return/thermal signoff, full four-layer plane geometry and KiCad zone-island/PCB-rework analysis.
- 236 known PCB DRC violations, especially 124 library mismatches and unreadable/crowded silkscreen; manufacturer-quality BOM, CPL, Gerber/NC drill and paste still absent.
- Slide SW1 exact orderable MPN/3D actuation, charger and LiPo NTC/polarity, charging when OFF and MOSFET inrush/thermal, ESP32 antenna keepout, case and edge button mechanical drawings.
- Good Display vendor response pending for GDEY0397T81P pin 5 `VDHR` (pin table) versus `VSH2` (application drawing), stepped FPC insertion/fold. No EPD copper routed yet.

**PCBWay-ready stays 30%.** Zero ERC and a valid local filled zone cannot compensate for incomplete routing and unqualified hardware.