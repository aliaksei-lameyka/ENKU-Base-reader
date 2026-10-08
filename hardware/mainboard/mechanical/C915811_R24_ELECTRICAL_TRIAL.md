# R24 — four-contact G-Switch switch trial, PCB and schematic

**RESEARCH ONLY; NEVER SEND TO PCBWay.** Branch `research/r24-c915811-4pin`.

- Four new footprints based on `GT_TC035A_H0195_L3_C915811_EVAL`: SW3/SW4 on left at (20.8,63)/(20.8,75) with **90°** rotation; SW5/SW6 right at (74.2,63)/(74.2,75) with **270°**.
- Electrical banks from vendor: physical pins **1/2 = BTN_L1/L2/R1/R2**, **3/4 = GND**; schematic embedded `ENKU:SW_FOUR` now matches. SW2 is still distinct 2-pin BOOT.
- Removed four obsolete button-net escapes; added sixteen new local F.Cu segments (three signal segments and one GND pair tie per button), connected to prior traces.
- **No Edge.Cuts recessed pockets**, no full local ground isolation audit, unknown supplier pad Y-row position, copper clearances, shell travel, pick-and-place assembly and PCBWay milling. Manufacturer pocket drawing plus DRC improvements required.
- This trial must run native KiCad ERC, DRC, structural population and PCB-vs-schematic parity; compare counts with base R23. A red result means this design is not ready to merge.

## R24 correction — native KiCad axis sign
An actual F.SilkS edge check showed the earlier positive-angle transform was wrong: the SW3/SW4 REF labels at local (0,-2.4) projected toward left board edge when rotated 270°, which is inward-facing actuation, not outward. Corrected the placements to **90° left and 270° right** and fixed `check_gswitch_eval.py` to test the native KiCad coordinate rotation. The existing local copper route coordinates were authored for the intended world positions and now agree with the corrected physical pad rotation. DRC/clearances still require native validation.

## R24C — actual KiCad pad handedness (2026-10-08)

The earlier +90° left/+270° right correction was **incorrect**. Native KiCad logs showed for the physical C915811 pad3→pad4 pair at the left edge, +90° points towards +board X (inward), while for the right edge +270° points towards −board X (inward). Therefore the outward-facing physical actuator must use **SW3/SW4 = 270°** and **SW5/SW6 = 90°**. All four KiCad board footprints are now corrected to those orientations; label refs stay on F.Fab. The native `pcbnew` checker now validates pad world-XY and relative 3→4 X-direction before trusting manual routing.

A prior native DRC on PR #2 reported **677 violations and 8 real unconnected** for the wrong rotation. Those numbers must **not** be described as the corrected-board result until a new native run finishes. Manufacturer milling pockets remain unverified; PCBWay release blocked.
