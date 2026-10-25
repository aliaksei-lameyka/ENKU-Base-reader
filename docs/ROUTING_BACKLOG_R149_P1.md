# R149-P1 moved-footprint net routing backlog

State: **NO FAB — LEGACY R148 COPPER STALE — NO VERIFIED DRC**.

Active nets belonging to one or more of the 11 mechanically relocated footprints (R149 P0/P1) are 37 in total; seven additional pads have intentional `unconnected-*` net labels, bringing the total unique net labels to 44. This inventory comes from native pad/net strings in the R149-P1 KiCad PCB.

| Group | Electrically active net names | Existing legacy copper objects with those net names |
|---|---:|---:|
| EPD (FPC J3) | 17 | 644 |
| USB-C J5 | 6 | 191 |
| Battery / NTC | 2 | 203 |
| Buttons SW3–SW6 | 4 | 115 |
| Power/regulator (incl. GND/3V3) | 8 | 780 |
| **Total** | **37** | **1,933** |

**Interpretation:** These 1,933 copper objects are merely associated with affected net names and are *not* the number of tracks requiring replacement. GND and 3V3 are shared with other unmoved components; never blindly delete an entire shared power net. Source board contains 2,963 trace segments, 389 vias and eight zones.

Routing priority:
1. Identify and remove old stubs at moved pads while preserving common GND/3V3 copper where valid.
2. Lay out J3's active EPD signals, HV nets and returns with the new orientation and FPC clearances.
3. Reconstruct USB-C differential pair, CC, shield, ESD and VBUS power path without breaking 4-layer stackup impedance, and keep H4 screw clearance HOLD.
4. Reconnect J1 battery, J8 NTC, 3V3 regulator U4/L1/C12 and test no cross-net shorts; verify solder wire strain relief.
5. Reroute the four button contacts and verify hand-selectable GPIO assignments.
6. Refill polygons, ERC+DRC zero, independent 84-net equivalent graph, Gerbers, BOM/CPL, 3D step/test prints, OEM/factory acceptance; NO FAB until all close.

KiCad 10.0.7 native diagnostic is automated in `.github/workflows/r149-p1-clearance.yml`. Its diagnostic job succeeding only means the report was generated; it is **not** fabrication sign-off. Machine-readable report is uploaded as an Actions artifact if the job completes.
