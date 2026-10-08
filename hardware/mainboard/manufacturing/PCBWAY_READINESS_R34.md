# ENKU Base R34 — verified PCBWay readiness

**Estimated 30/100%. Not approved for manufacturing.**

**Active hardware:** `hardware/mainboard/kicad/enku-mainboard-r1.1-base-gated-battery-adc.kicad_pcb` (123 physical KiCad footprints including mechanical holes).

## Verified tests, 2026-10-08

- [R34 Native KiCad run 37799863680](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37799863680): **ERC 0 errors, 0 warnings**, PCB/schematic parity **0**, critical shorts / copper edge issues **0**, footprint_errors **0**. This is a diagnostic run; the PCB DRC did **not** pass.
- [R34 Hardware Schematic Check 37799863710](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37799863710): all structural checks passed, including current 123-footprint R34 population and new battery-ADC power domain.
- **Native PCB DRC 233 non-unrouted violations**: `lib_footprint_mismatch` 122, `silk_over_copper` 68, `silk_overlap` 27, `text_height` 16. **263 unconnected items**. Footprint pad comparison: 58 different, 65 matching to KiCad stock library; library pad difference is a review inventory, not necessarily a vendor mechanical defect.
- R33 baseline: 120 footprints; DRC 229 non-unrouted; 255 unrouted; ERC had 1 undriven power pin; R34 includes +3 components and now 0 ERC warnings/errors. Thus 4 more non-unrouted DRC observations and 8 more unconnected items are due to expanded architecture, not completed routing.

## Corrected product architecture

- SW1 now physically disconnects the **reader load**: BQ25185 SYS `VSYS` → SW1 → switched U4 TPS63802 VIN, EN, C9/C10 input capacitors (`SYS_EN`). Battery/charger remain connected and can charge OFF.
- U9 TMUX1101DBVR with C37 100nF and R39 1M gates direct VBAT voltage measurement divider: BAT_ADC_SW now feeds R26 only when 3V3_SYS powered. Original R26/R27 ADC divider voltage remains 2M/680k.
- EPD J3 24 pins and populated R28 VDDIO/VCI strap checked. Good Display GDEY0397T81P pin5 VDHR (pin table p6) vs VSH2 (diagram p19) **cannot be approved without supplier confirmation**.
- Two nonmanufacturable ERC-only symbols `#FLG01` (SYS_EN physical source after SW1) and `#FLG02` (battery ground reference) correctly document real sources. They have no footprint, no BOM/PnP; they do not substitute for any power path.

## Fabrication blockers

**Never upload R34 to PCBWay as production Gerber.** All **263 unrouted** connections and four-layer ground planes/power loops; 233 DRC non-unrouted violations; FPC-7750 actual 3D fold, latch contact side and Good Display pin5; full 3D mechanical clearances (body, battery, 4 buttons, enclosure screws, LiPo cable/microSD), actual switch orderable MPN and inrush rating; real battery cell protection, NTC wiring/polarity, charger/USB/dock off-state current/backfeed, U9 off-leakage, ADC pin startup transient; vendor qualified BOM, CPL rotations, Gerbers including NPTH and assembly DFM remain pending.

Readiness **30/100** unchanged: ERC and placement improvements reduce risk but do not constitute copper completion or fab signoff.