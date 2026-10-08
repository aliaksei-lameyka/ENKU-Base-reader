# R23 — G-Switch C915811 manufacturer-land-pattern evaluation

**Status: EVALUATION ONLY. NOT AN APPROVED PCB footprint or assembly model.**

## Primary evidence

- [Original manufacturer drawing for GT-TC035X-HXXX-LX (LCSC C915811 PDF)](https://atta.szlcsc.com/upload/public/pdf/source/20201109/C915811_C704946C12D3A7315F3A918018B4FA40.pdf), rev X1 dated 2019-05-29.
- [LCSC supplier part C915811](https://www.lcsc.com/product-detail/C915811.html)
- [G-Switch manufacturer family](https://www.dg-switch.com/qingchukaiguanchenbanshixilie/1539.html)

## Copper lands: explicit source mapping

The PDF 'PWB land pattern for reference' gives (nominal, mm):
- Pad-row total width **3.2 ±0.05**.
- Central gap **0.92 ±0.05** between left/right metal lands.
- Upper pads length in direction of button push: **0.65 ±0.05**.
- Lower pads height **0.40 ±0.05**.
- Overall pattern height approx **1.50 ±0.05**.
- Derived symmetrical width of each pad **(3.2−0.92)/2 = 1.14 mm**, x-centers **±1.03 mm**.
- KiCad test footprint places upper row y=−0.425, lower row y=+0.550, a derived nominal 0.45-mm row gap. **This y offset is a drawing interpretation**, not a separate vendor dimension. Verify directly with vendor original CAD and real part before manufacture.

Manufacturer bottom view pin numbers:
- **1 and 2 electrically common**, left column.
- **3 and 4 electrically common**, right column.
- The switch closes between the two columns.

One large omission of the old R22 plan: the **existing ENKU schematic uses a 2-pin switch symbol**. Connecting a true 4-pin device requires reworking schematic symbol and board pad assignments. Do NOT renumber copper pads to 1,1,2,2: that would disagree with manufacturer physical pinout. Until that coordinated migration, **R23 does not replace SW3–SW6 on the main board**.

## Left/right hand mapping

In the library evaluation footprint, `PUSH +Y` points toward the exterior actuator face:
- Left side (SW3/SW4): **270°** footprint rotation, positive local Y points to negative global X.
- Right side (SW5/SW6): **90°** footprint rotation, positive local Y points to positive global X.
- Manufacturer pins 1/2 then occupy opposite physical button height compared with 3/4 on the opposite side. Either use a properly mirrored schematic symbol or explicitly assign pin banks per switch while preserving original BTN_L1/BTN_L2/BTN_R1/BTN_R2 ↔ GND nets.

## Pending PCBWay DFM

- Manufacturer says recessed height ~0.98mm; PDF shows recessed body/terminal, but no unambiguous Edge.Cuts specification in the one-page PDF.
- **Do NOT cut the 59×101 mm board edge** from this EVAL footprint. We still need the manufacturer's exact board-pocket construction and PCBWay minimum mill tool radius/NPTH copper clearance for our 4-layer stack.
- Sourcing details: 4 × G-Switch GT-TC035A-H0195-L3, **LCSC C915811**, board user-designated refs SW3–SW6.
- Manufacturer generic maximum contact current 20 mA, LCSC 50 mA; resolve conflicting claims on the exact variant. Input GPIO with pull-up should have far lower switching load.

## Work done

- Created `ENKU.pretty/GT_TC035A_H0195_L3_C915811_EVAL.kicad_mod`, preserving physical pad numbering.
- Added `check_gswitch_eval.py` to hardware CI to assert pad dimensions and mirrored actuation.
- Kept routed R22 main board unchanged until paired schematic/PCB migration can be checked as a single change.
