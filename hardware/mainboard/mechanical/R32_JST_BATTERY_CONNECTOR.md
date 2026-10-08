# R32 — ENKU Base battery connector: real SMT JST geometry

**Engineering placement, NOT ready for production.**
Manufacturer drawing: https://www.jst-mfg.com/product/pdf/eng/ePH.pdf (page 2; side-entry SMT PH, 2.0mm pitch).
Cross-check against KiCad land pattern: https://sources.debian.org/src/kicad-footprints/9.0.2-1/Connector_JST.pretty/JST_PH_S3B-PH-SM4-TB_1x03-1MP_P2.00mm_Horizontal.kicad_mod .

## Problem fixed in source

Previous J1 `Connector_Generic:JST_PH_3_PLACEMENT` had only **3 signal pads**, no mechanical solder anchors, no qualified mounted footprint library. Inserting/removing a battery harness would stress solder joints; the original was physically not equivalent to S3B-PH-SM4-TB.

R32 J1:
- Candidate exact MPN: **JST S3B-PH-SM4-TB(LF)(SN)**, 3-position right-angle SMT 2.0mm pitch, with matching **PHR-3** plug and proper PH crimp contacts (custom cable).
- Project local footprint `ENKU:JST_PH_S3B-PH-SM4-TB_1x03-1MP_P2.00mm_Horizontal`, placed on F.Cu (69.8,93.5,90°), not old (66,93.5,90°).
- From manufacturer-referenced KiCad land pattern: pin1/pin2/pin3 pad centers (-2,-2.85), (0,-2.85), (2,-2.85) and size 1.0×3.5mm; **two MP solder anchors at (±4.35,+2.9), size 1.5×3.4mm**; courtyard 11.2×10.2mm. Board nets 1=VBAT, 2=GND, 3=BAT_TS. Two unconnected mechanical anchor pads have exposed copper, paste and mask.
- Schematic J1 footprint pointer also moved to project local ENKU footprint. Board has 120 components, 5 physical J1 pads; actual native pad and schematic parity test required.
- R32 compares SMD copper-pad rectangle envelopes of the **entire active R32 board** including both MP anchors against all other F.Cu components and refuses same-net overlaps.

## Serious remaining red flags

1. **Battery polarity + NTC harness must be CUSTOM**. Do not connect a random three-wire JST PH battery. 1=VBAT, 2=GND, 3=BAT_TS is our electrically defined map, not a generic supplier pin order. Need actual cell brand/pack/protection PCB/NTC resistance and matching harness drawing before assembly.
2. Real JST side-entry cavity/mating travel and cable bend must clear 3D case, display backer, LiPo pouch, microSD eject path and body anchor solder fillets.
3. Hard power SW1 still only converts VSYS to SYS_EN: not a physically battery-isolating cut-off. Clarify required off-state semantics and select actual switch before layout.
4. Native KiCad DRC + physical STEP, EPD FPC fold, side-buttons, U1 ground via technology, USB connector, real PCBWay BOM remain open.

Manufacturer geometry is a candidate, not a real product test. Do not treat a green script or noncritical DRC as a fabrication release.
