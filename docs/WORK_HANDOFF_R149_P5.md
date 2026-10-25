# R149-P5 — Native KiCad placement, copper progress and hold

Date: 2026-10-25. **NO FAB / NOT ELECTRICALLY COMPLETE / NOT A PRODUCTION RELEASE**.

## Provenance and sources
- R148 source is electrical reference; printed M03 from 2026-10-17 physically showed display position and FPC reach on 2026-10-25.
- Reproducible R149-P0 through R149-P5 generators: `hardware/mainboard/r149/checks/rebuild_R149_P*.py`.
- R149-P5 pre-refill KiCad PCB SHA256: `c1ef501f301b8bdc43838c43ce5846391732b50496c9ecd21ca7a188ea87afae`.
- R149-P5 native diagnostic PASS **means the DRC report completed**, not zero DRC violations: [GitHub Actions run 40202869674](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/40202869674).

## Verified DRC sequence (KiCad 10.0.7, -refill-zones, native)
| Candidate | DRC violations | Unconnected items | Shorts | Parity |
| --- | ---: | ---: | ---: | ---: |
| R149-P2 | 53 | 62 | 0 | 0 |
| R149-P3 | 47 | 48 | 0 | 0 |
| R149-P4 | 44 | 48 | 0 | 0 |
| **R149-P5** | **44** | **43** | **0** | **0** |

P5 **44 DRC errors = 43 track-dangling + 1 via-dangling**. No RF-keepout, footprint courtyard, clearance, hole clearance or silkscreen clipping violations remain in the native P5 report. This still does NOT mean the PCB is functionally routed: 43 independent KiCad unconnected items remain. **Never suppress/waive the outstanding errors to make a release appear clean**.

## Geometry contract
- **J3 at X69.46 Y94.22, USB J5 at X65 Y117.325 remain identical to physically tested M03.** 59 x 101 mm outline unchanged.
- RF keepout X5.25..26.25, Y21..69 preserved unchanged. SW3/SW5 upper side reading buttons shift from Y68 to **Y73** (symmetrical), SW4/SW6 at Y80; RF native keepout is clear. Upper-button spacing to lower-button is only **7 mm center-to-center**: this new ergonomic and case-aperture arrangement has **NOT been printed or user-approved**.
- H4 mounting hole X72→**73.5** (Y116.5 unchanged), +1.5 mm right. J5 retains its M03 location. Mechanical M2 screw head, insert, standoff and enclosure clearance remain **physical trial HOLD**; the previously printed M03 hole and two upper side buttons are now OUTDATED.
- Moved J5 reference/silkscreen to X57/Y116.5 to clear H4; connector stays unmoved.

## Electrical P5 delta
- P3 joined side switch pairs (all four switch groups). P4 detoured `BTN_L2` away from a grounded via near SW4. P5 adds eight F.Cu GND / USB_SHIELD short local segments connecting C12 GND, J8 GND, J1 GND on the battery side, and both pairs of USB-C shield stake contacts. This reduced unconnected KiCad items from 48 to 43.
- P5 resolved an inadequate VBAT-to-GND copper gap in the first P5 trial; corrected GND trace X69.0→X68.8 at the J1 region. Native DRC confirms required clearance. **Battery ground copper current carrying capability and harness strain relief are NOT qualified**.
- USB D+/D- and CC/VBUS networks, and the relocated 24-pin EPD/control/HV routes, are not complete or tuned/verified. Do not reuse R148 fabrication outputs or mixed vintage files.

## Next pass / safety gates
1. Preserve the 59x101 board/mechanical datums; confirm physically shifted side-button apertures/7mm ergonomic spacing and new H4 screw position before enclosure release.
2. Close 43 unconnected nets deliberately: J3 24-pin EPD interface and HV/return topology; USB 2.0 full receptacle pin groups with differential pair impedance/return and ESD; power REG_MODE/REG_FB/3V3/BAT_TS/VBAT, switch active signals and shield/ground topology.
3. Rerun KiCad ERC+DRC and schematic parity; zero DRC errors **and zero unconnected** required, followed by independent full four-layer graph connectivity, manufacturing Gerbers and drill, verified BOM/CPL/orientation and OEM geometry comparisons.
4. Battery protected PCM and bonded 10k/B3435 NTC, USB/FPC mechanical plug, actual sample bringup, thermal and voltage-transient/full-load testing, SD MSC and e-paper functionality, FCT before PCBWay authorization.

**Result:** R149-P5 is the correct, editable, *partial* KiCad hardware integration source. Manufacturing release is forbidden (NO FAB).
