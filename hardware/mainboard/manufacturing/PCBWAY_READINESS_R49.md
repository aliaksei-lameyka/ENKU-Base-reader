# ENKU Base R49 — Supplier CAD Intake / PCBWay readiness

**Weighted engineering readiness: 44% (unchanged from R48). Manufacturing PCBWay GO: NO.**

R49 captures Good Display supplier answer and design/manufacturing holds. **No KiCad PCB or schematic copper changes were made:** active source `hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb`.

Last measured [R48 Native KiCad](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825797): **ERC0, PCB-to-schematic parity0, priority DRC0, 139 unconnected, 168 other DRC** including 130 footprint library mismatch and 38 silkscreen. Full DRC is not fabrication-passing. No fabricated/assembled sample.

2026-10-09 supplier package: 3.97" panel PDF + `GDEM0397T81P` STEP/DWG + dual-contact connector drawing + Arduino example; recommended **not bending flex immediately at glass edge**; no numeric bend radius; connector alternative 8.21A0.024200 **not explicitly endorsed as a J3 replacement**; supplier still did **not directly resolve pin5 `VDHR` versus `VSH2`**. This is a **critical go/no-go electrical hold** until corrected pin map or signed vendor clarification.

Next: ask written pin5 + variant CAD identity + explicit FPC/contact/connector fit; review vendor EPD power schematic against ENKU Q1/L2 ratings; reflect actual glass/step tail in Fusion only after identification, then route remaining 139 signals (incl. USB D+/D− with actual PCBWay 90-ohm stack-up) and eliminate all DRC. See `hardware/mainboard/research/GOODDISPLAY_REPLY_2026-10-09.md`.

Separate ENKU Reader Pro 4.26" frontlight + CTP is a **candidate**, its detailed specs are stored in *private* `raznoglaz1y/ENKU-lab/research/reader-pro-gooddisplay-4p26-frontlight-touch-2026-10-09.md`. No Pro panel, Qi or frontlight parts imported into Base PCB.
