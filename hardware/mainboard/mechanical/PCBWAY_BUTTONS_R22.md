# ENKU Reader R22 — PCBWay procurement shortlist: 4 miniature navigation switches

**Draft sourcing inquiry, NOT an approved production BOM.** The current PCB still contains virtual `READING_BUTTON_PLACEMENT` footprints for SW3–SW6; it does **not** fit the following part yet.

## Shortlist (Chinese/local channel first)

| Rank | Manufacturer MPN | LCSC ID | Size / height* | Actuation | Life | Source / why |
|---|---|---|---|---|---|---|
| 1 | **G-Switch GT-TC035A-H0195-L3** | **C915811** | 2.8×2.65×1.95 mm (manufacturer axis order) | right-angle, 1.6 N, travel 0.15±0.05 mm | 300k claimed | [LCSC](https://www.lcsc.com/product-detail/C915811.html), [G-Switch](https://www.dg-switch.com/qingchukaiguanchenbanshixilie/1539.html); Shenzhen/Dongguan procurement candidate |
| 2 | Panasonic EVPAVAA1A | C2845003 | 2.8×2.65×1.95 mm | right-angle, 1.6 N | 300k claimed | [LCSC](https://www.lcsc.com/product-detail/C2845003.html), second source / benchmark, NOT pinout drop-in |
| 3, cost fallback | SHOU HAN TS24CA | C393942 | 4.7×1.9×3.5 mm (listed axes) | right-angle, 1.6 N | 20k claimed | [LCSC](https://www.lcsc.com/product-detail/tactile%20switches_shou%20han_ts24ca_C393942.html), do not approve for heavy paging without accelerated wear testing |

*Footprint axes in distributor listings are inconsistent; recheck manufacturer's dimensioned 2D drawing, recommended land pattern and 3D height before CNC/SMT.

## Why G-Switch
- 2.8-mm-class micro side-actuated switch: suitable size for 59-mm pocket PCB.
- Recessed PCB mounting lowers effective Z envelope, but **requires a precise edge opening and pads**. Manufacturer lists recess 'height 0.98 mm' and actuation travel 0.15±0.05; neither figure is enough by itself to design Edge.Cuts.
- 300,000 manufacturer claimed actuations vs 20,000 on SHOU HAN TS24CA.
- Supplier information: China G-Switch/品赞, vendor pages at LCSC and official Dongguan manufacturer.

## Sourcing/cost caveats
- LCSC source prices at lookup were approximately **$0.26 each at 100+ quantity**, or **$1.04 for four switches per board**, excluding SMT, shipping, excess stock and taxes. Do NOT treat this as a PCBWay quote.
- PCBWay provides turnkey sourcing through local suppliers and through customer-selected vendors; only they can confirm stock, genuine sourcing route, order MOQ, substitutions and lead-time. [PCBWay sourcing policy](https://www.pcbway.com/pcb_prototype/Electronic_Components.html).
- Ask PCBWay to quote **200 assembled units** for 50 boards (4 switches per PCB), and a sensible percentage of SMT attrition/spares. Request separate quote for 100 / 300 / 500 readers later.
- **Substitution only with ENKU's advance approval.** Equal outside dimensions is NOT enough: pin count, land pattern, recessed cutout, travel, force and reliability must match.

## BOM quote line
| Designators | Qty/PCB | MPN | Manufacturer | Preferred local source | Status |
|---|---:|---|---|---|---|
| SW3 SW4 SW5 SW6 | 4 | GT-TC035A-H0195-L3 | G-Switch | LCSC C915811 or PCBWay-qualified local supplier | RFQ candidate — not footprint-approved |

## Manufacturing blockers
1. Secure a **manufacturer 2D recommended land pattern + PCB edge cutout and 3D model**.
2. Redesign KiCad pads and routed tracks for two left-facing and two right-facing switches; no mirrored circuit mistakes.
3. Keep actuators centered on the two existing y=63/75 control heights unless shell ergonomics demand adjustment.
4. Verify edge milling / slots: KiCad Edge.Cuts 59×101 rectangle must ultimately be modified **if** the manufacturer requires a recess.
5. Test physical force (~1.6 N), thumb travel, reliability and case keycap tolerances on a print.

## SW1 hard-power slide: separate from the four reading buttons
- **Candidate:** [G-Switch MK-12C03-G015, LCSC C2890358](https://www.lcsc.com/product-detail/C2890358.html): surface-mount right angle, **6.65×1.4mm** board-plane nominal, 4.25mm switch height, SPDT, rated 500mA/12V. Local/Chinese part, not a quote.
- **Not electrically approved**: SW1 is currently two solder pads; candidate SPDT requires circuit/footprint redesign. 500mA is not automatically sufficient for hard LiPo disconnection during Wi-Fi TX spikes or high-capacitance power-on inrush; evaluate peaks and switched load before approval.
- [SHOU HAN MSK12C02 C431540](https://www.lcsc.com/product-detail/C431540.html) is lower-profile (8×2.8×1.4mm) but **50mA** rated and therefore **REJECTED for direct battery hard power**. It can only serve as low-current logic enable with a separate guaranteed-disconnect power arrangement.
- Include SW1 in PCBWay sourcing RFQ as *separate candidate under engineering review*, not as an orderable populated item. Need both manufacturer STEP and actuator-to-shell opening verification.

## PCBWay feasibility: tiny recessed switch pockets
- PCBWay's [general capabilities](https://www.pcbway.com/capabilities.html?from=newtontecharticle) and [slot design note](https://www.pcbway.com/helpcenter/drill_hole_or_via_issues/Slots_standard_size___Limited_to_Quick_turn_PCB.html) list a **non-plated slot width >=0.8 mm** for standard quick-turn production. These values are **not** a guarantee that GT-TC035's open-sided, partial-depth/recessed edge pocket and contact pads can be fabricated at our layer count/thickness.
- Official PCBWay [milling overview](https://www.pcbway.com/pcb_prototype/PCB_Milling.html) lists minimum milling tool diameter **0.8 mm**. Do **not** draw 90° sharp pocket corners without compensating fillets/tool radii and copper-to-edge constraints.
- Send PCBWay the actual manufacturer's 2D land-pattern/edge-pocket drawing and requested 4-layer thickness before editing `Edge.Cuts`. Request **tool radius, copper-to-pocket clearance, solder-paste stencil constraints, panelization, assembly orientation and tolerance stack**, in writing.
- Until PCBWay confirms this, R22 `Dwgs.User` rectangles are size studies only; there is **no electrical manufacturing switch footprint**.

## R23 manufacturer PDF and evaluation footprint
- Exact 1-page manufacturer PDF confirmed: https://atta.szlcsc.com/upload/public/pdf/source/20201109/C915811_C704946C12D3A7315F3A918018B4FA40.pdf
- Evaluated 4-terminal land pattern is in `hardware/mainboard/kicad/ENKU.pretty/GT_TC035A_H0195_L3_C915811_EVAL.kicad_mod`.
- Pin 1/2 are one internal bank, pins 3/4 are the other. Original switch schematic was 2-pin: do not silently swap footprint without schematic migration.
- Source comparison: G-Switch general family specifies 20mA maximum, LCSC specific product listing specifies 50mA; retain conservative 20mA until verified by manufacturer.
