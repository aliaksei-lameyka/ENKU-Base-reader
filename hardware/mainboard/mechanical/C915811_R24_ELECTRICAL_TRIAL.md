# R24 — four-contact G-Switch switch trial, PCB and schematic

**RESEARCH ONLY; NEVER SEND TO PCBWay.** Branch `research/r24-c915811-4pin`.

- Four new footprints based on `GT_TC035A_H0195_L3_C915811_EVAL`: SW3/SW4 on left at (20.8,63)/(20.8,75) with **270°** rotation; SW5/SW6 right at (74.2,63)/(74.2,75) with **90°**.
- Electrical banks from vendor: physical pins **1/2 = BTN_L1/L2/R1/R2**, **3/4 = GND**; schematic embedded `ENKU:SW_FOUR` now matches. SW2 is still distinct 2-pin BOOT.
- Removed four obsolete button-net escapes; added sixteen new local F.Cu segments (three signal segments and one GND pair tie per button), connected to prior traces.
- **No Edge.Cuts recessed pockets**, no full local ground isolation audit, unknown supplier pad Y-row position, copper clearances, shell travel, pick-and-place assembly and PCBWay milling. Manufacturer pocket drawing plus DRC improvements required.
- This trial must run native KiCad ERC, DRC, structural population and PCB-vs-schematic parity; compare counts with base R23. A red result means this design is not ready to merge.
