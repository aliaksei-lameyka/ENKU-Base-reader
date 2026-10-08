# ENKU Reader R0.1 — mechanical fit-check R02 (2026-10-08)

This is a calculated 2D envelope check of the current **62 × 109 × 10 mm** preliminary case. It is **not** validated full 3D CAD or a manufacturable assembly.

## Reference envelopes (case coordinates in mm)

| Item | x | y | width | height |
| --- | ---: | ---: | ---: | ---: |
| Display module | 2.88 | 3.20 | 56.24 | 96.62 |
| PCB, centered assumption | 1.50 | 7.50 | 59.00 | 94.00 |
| Battery 40 × 60, centered assumption | 11.00 | 24.50 | 40.00 | 60.00 |
| U1 ESP32, approximate envelope | 7.50 | 20.00 | 18.00 | 25.00 |

- Two lower M2 axes: (7.5,104.2) and (54.5,104.2), illustrative 5 mm boss diameter. **Neither boss intersects the nominal display or PCB rectangles** in this placement. This does NOT prove screw clearance from FPC, USB-C, microSD or wiring.
- Battery and approximate U1 envelopes **overlap by 297.25 mm² in XY**. They cannot occupy the same Z volume. Need height-map and component/packaging relocation before validating 10 mm thickness.
- PCB bottom is 1.68 mm beyond the display bottom. PCB and display are not vertically centered relative to each other; connector FPC reach must be checked.
- Bare nominal stack estimate 9.02 mm uses 1.25 front + 0.92 display + 0.5 support gap + 1 PCB + 0.3 separation + 3.8 battery + 1.25 rear; **only 0.98 mm nominal margin** for adhesive, pouch swelling, tolerances and non-overlapping high components. This is not yet acceptable production margin.
- Current four PCB holes still need their own structural support/retention design; two rear enclosure screws do not secure PCB.

## Next mechanical revision gates

1. Obtain exact chosen LiPo pack dimensions incl. PCM, wire exit and swelling allowance; actual U1 and all backside component heights.
2. Decide battery location without overlap with high components, or reroute/repack PCB. Check antenna keepout.
3. Import exact display module/FPC STEP or manufacturer drawing and all connector geometry into one common coordinate system.
4. Model actual top hook latch/relief and repeatable disassembly, rear screw insert and pilot holes, four PCB supports and side-button caps; verify print tolerance.
5. Produce assembled section and intersection checks before committing KiCad hole/placement changes or calling STL print-ready.
