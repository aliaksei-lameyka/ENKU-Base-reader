# ENKU Base R32 PCBWay readiness

**30/100% — estimate unchanged, RELEASE BLOCKED.**

R31 latest valid baseline: 120 parts, 234 Native KiCad violations (except unrouted), 0 schematic parity faults, 255 unconnected nets, 0 cross-component SMD pad overlaps in independent structural check.

R32 replaces three-pad fake J1 with full 3-signal + 2-mechanical-pad **JST S3B-PH-SM4-TB** SMT land pattern, moves J1 to x69.8 y93.5 r90, updates schema and project local library. Run Native ERC/DRC and R32 pad envelope gate before updating metrics.

Unresolved: genuine battery/NTC polarity and protected cell, fit and assembly 3D, nonbattery-isolating SW1 control, folded Good Display FPC, HV rail, routing 255+ connections, footprint qualification/PCBWay BOM/CPL, Gerbers/NPTH/3D.

## Native first-run error / corrective design

Initial source R32 Native KiCad flagged two **critical shorts** between J1 pads (VBAT↔GND, GND↔BAT_TS), 2 solder-mask bridges, and 1 schematic value mismatch (J1 value). Cause: hand-created rotated JST J1 board had per-pad `(at ... 0°)` with footprint at 90°; KiCad board stores pad **absolute** orientation, unlike source-library local coordinates. Corrected all **three signal plus two mechanical pads to 90°** and restored J1 PCB Value to `1S LiPo + NTC` to equal schematic. Changed R32 audit to evaluate pad-rotation as stored and detect different-net overlapping copper inside a single footprint (not only between footprints). Native repeat REQUIRED before claiming fix; original failure is retained as evidence.

## Native R32 verification — 2026-10-08

- [KiCad 8 Native run 37795602991](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37795602991) on commit `8874ee4a`: structural R32 pad collision/diode/USB guard **PASS**; placement critical short and edge gate **PASS**; PCB/schematic parity **0**; Native job completed successfully as **diagnostics only**.
- **229 non-unrouted DRC violations**: 119 footprint-library mismatches, 67 silk-over-copper, 27 silkscreen overlaps, 16 text-height issues. No J1 library-absent error remains. **255 unconnected items**; no full routing or filled GND/copper planes.
- R31 prior snapshot was 234 non-unrouted DRC (119 footprint mismatches, 1 missing J1 footprint library, 65 silk-over-copper, 33 silk-overlap, 16 text-height); 255 unconnected. R32 is **5 fewer** overall, but individual classes may rise and still require cleanup.
- Initial R32 J1 attempt failed Native DRC with 2 inter-net copper shorts and schematic parity mismatch. Per-pad KiCad absolute orientations and J1 value were repaired; enhanced CI now refuses any such shorts/mask bridges/parity errors. Original failed run remains in Actions history (never erase failed test evidence).
- Manufacturer-equivalent KiCad source geometry is not certification of battery mating, cable order, mechanical snap/strain or electrical charge safety.

**PCBWay readiness remains 30/100**: milestone-based scoring unchanged due to no routing or full MPN qualification. Gerber/BOM/CPL release still **BLOCKED**.