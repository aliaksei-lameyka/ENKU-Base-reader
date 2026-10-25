# R149-P1 — J3 corridor resolution (25 Oct 2026)

**NO FAB / NOT ROUTED / NOT VERIFIED ELECTRICALLY.** Branch: `engineering/r149-m03-integration-hold`.

## Scope and evidence
- Physical M03 mockup: user verified panel seating and flex reach. J3, J5, SW3–SW6 M03 positions remain unchanged.
- R149-P0: six M03 placements, still overlaid R148 copper (source SHA `764cbe8258df7e76f14936407ecabc2fa86e8a80bdc42c01774b26bb23dcc977`).
- R149-P1: relocate J1 (74,105; 90°), J8 (72,110.5), C12 (62,99), L1 (60.7,91.2;-90°), U4 (57.65,91) in native KiCad footprint data. Source-checked output SHA: `a670b7cfb921fa7de7305672b708c1e12834ae097c8463479f267df2d339dfc9`. Exact generator: `hardware/mainboard/r149/checks/rebuild_R149_P1.py`.
- Independent 2D nominal footprint-courtyard screen: 12 pre-existing P0 overlapping pairs reduced to six pairs; no new overlapping pairs introduced. This screen is **not** KiCad DRC. Remaining six overlaps are retained baseline testpoint/courtyard modelling artifacts and need native audit before manufacturing.
- J3 distances to closest courtyard: R97 0.17 mm, moved L1 0.31 mm, C11 0.61 mm. J1 to J8 0.65 mm. C12 nearest R99 0.735 mm.
- J5–H4 nominal courtyard separation **0.68 mm**; with typical M2 screw-head radii ~1.8–2 mm, head-to-USB body clearance is **unproven**, and PCB/case hole relocation may be needed. Do not assume M03 display-fit confirms screw or USB plug clearance.
- Battery solder pads and NTC positions are only candidate envelopes. Wire bend/solder relief/case clamp and pack assembly remain unqualified.
- 11 footprints across R149-P0/P1 were moved from R148, touching **44 pad-net names** including EPD, USB, battery, regulator, buttons and GND. 2963 old segments, 389 vias and eight old copper zones have **not been rerouted or accepted**. They are stale electrical data in P1.

## Next hard gates
1. Resolve J3 actuator / pin-1 and actual full assembled FPC against new J1/J8 leads and insulation.
2. Check H4 fastener head, standoff and USB shell and cable interference with casing. Do not move M03 USB datum without new physical fit approval.
3. Rip up and reroute moved signal and power groups; preserve return current paths and high-voltage display domain, USB-C ESD, 24 J3 contacts, battery-NTC reliability, side-button GND.
4. Run native KiCad ERC/DRC to **zero errors**, independent 84-net equivalent connectivity and stack/thermal/voltage checks; rebuild Gerber/BOM/CPL. No source manufactured before that.
5. Prototype bring-up, power load, USB MSC, SD, EPD and FCT; PCBWay sign-off.

R149-P1 is a **real editable KiCad placement snapshot**, not an approved routed PCB or manufacturing candidate.