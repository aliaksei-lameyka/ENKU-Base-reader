# R149-P2 — Native KiCad Copper Repair Checkpoint (2026-10-25)

**Status: PARTIAL ROUTING / NO FAB / BLOCKED.** M03 user-confirmed panel/flex mechanical placements J3/J5/SW3–6 retained. Source: R148 `bb0aa41324b73ec13c087ab1c669c57c6bc6fd449621bf3aa34a53d3901b9476`, reproducible P0→P1→P2 generators in `hardware/mainboard/r149/checks/`.

## Engineering evidence — actual native KiCad 10.0.7
- P1 refilled source: [run 40200383790](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/40200383790).
- **R149-P1 refilled:** 78 DRC violations, 60 disconnected items, 4 shorts, 0 schematic parity issues.
- **R149-P2 refilled:** 53 DRC violations, 62 disconnected items, **0 shorts**, 0 schematic parity issues. [successful native diagnostics run 40201052053](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/40201052053).
- R149-P2 remaining DRC: 47 track dangling, 1 via dangling, 3 RF keepout items (SW3 vs U1), 1 H4/J5 courtyard overlap and 1 USB silk conflict. The KiCad process/workflow success means **diagnostic executed**, never fabrication approval.

## Byte-exact controlled change from P1
- SHA256 R149-P1: `a670b7cfb921fa7de7305672b708c1e12834ae097c8463479f267df2d339dfc9`.
- SHA256 R149-P2: `0d14749300afaf7968925c6836f9fb24b607e2307354cd70e41281138da17399` (pre-refill generated KiCad PCB).
- **Four** existing via objects removed at REG_MODE (56.3,90.25), REG_MODE (63.15,92.35), 3V3_SYS (62.3,95.9), GND (21.5,81.8).
- **Thirteen** legacy segments removed where new J3, moved U4 and SW4 conflict (incl. BAT_TS corridor, old SYS_EN route, REG_FB, REG_MODE, 3V3_SYS).
- **Five** new segments: SYS_EN safely bypassed above J3 (64.85,90.70→70.25,90.70), local BTN_L2/GND approaches to SW4.
- All 141 footprints and all approved M03 connector/side-button positions are unchanged. No network labels or schematic changed. 2963 old segments -> 2955; 389 old vias -> 385. Automatic zone refill must run before further DRC.
- **Caution:** existing unconnected copper is not an approved functional route. BAT_TS/REG_MODE/REG_FB/3V3_SYS and battery/USB/EPD routes require deterministic reconnection and full thermal/power analysis. Do not hide DRC errors with rule exceptions.

## Remaining blocking gates
1. **RF:** SW3 upper-left enters the actual U1 antenna keepout (3 DRC violations). Remedy must preserve Wi-Fi RF geometry; requires electrical/mechanical relocation approval. DO NOT waive RF keepout.
2. **USB/H4:** physical courtyard clash of USB-C J5 and H4 mounting hole. Needs printed screw head/stand-off clearance and revision of hole/case or a suitable mechanical alternative; no implicit exception.
3. **Dangling copper:** 47 tracks + 1 via, and **62 unconnected items**. Re-route J3 24-pin signals, USB DP/DM (paired geometry and length control), 3V3/REG, J1/J8 harness and side GPIOs. Re-run four-layer copper / manufacturing / OEM, BOM, CPL audits on same source.
4. Protected battery PCM + bonded 10k/B3435 NTC, FPC latch/contact1, case pressure, thermal/dynamic rails, actual firmware/EPD/USB/SD/FCT hardware tests must pass before supplier release.

**Manufacturing release remains strictly forbidden. No PCBWay files from P1/P2 may be fabricated.**
