# R36 first copper — controlled local power prototype

**Only power island, not full-board routing.** Source: `hardware/mainboard/kicad/enku-mainboard-r1.3-base-first-power-copper.kicad_pcb`.

A first, intentionally limited copper experiment connects the R35 local PMOS near converter without committing to Good Display FPC ribbon shape: 19 explicitly junctioned segment sections on F.Cu/B.Cu; one Ø0.70mm / Ø0.30mm drill via at x48.6,y83.7. Nets:
- `PWR_GATE` (96): R40.2 to Q2.Gate pin1 (2× 0.20mm segments), **mechanical SW1 remote line still unrouted**.
- `VSYS` (32): R40 pull-up to Q2.Source, F.Cu pilot to through-via and B.Cu up to rear TP5 VSYS, **physical charging controller SYS U3.1 is not yet linked**.
- `SYS_EN` (74): Q2.Drain to C9/C10 input, U4 VIN10 and EN1 breakout; widths 0.35mm for short loops and 0.18mm at tightly spaced U4 pads.

**Routing is incomplete and electrically nonfunctional as a standalone product.** No GND/3V3 stitching/planes, no EPD HV or FPC wires; no connected battery, no USB and no full power path. Native KiCad DRC is a strict stop for copper shorts, mask bridges, hole/edge faults or parity. Any failure means fix; do not claim routing is ready based on a source text check. 0.18mm is allowed by project rule but might be unsuitable as sole high-current VIN neck (must add copper area/parallel plane before final).

The Good Display clarification request is already sent by owner; retain J3 pin5 VDHR/VSH2 uncertainty and folded FPC no-go until response. Power switch physical MPN/actuator, true pack isolation decision and AO3401A heat/inrush qualification are still blocked.

This revision demonstrates the first local PCB copper and independent DRC loop. Roadmap remaining: charge path upstream Q2, return GND plane, 3V3_SYS bulk output, protected LiPo, microSD and SPI, four-layer HV & EPD, button pinouts, comprehensive BOM/CPL/Gerbers.
