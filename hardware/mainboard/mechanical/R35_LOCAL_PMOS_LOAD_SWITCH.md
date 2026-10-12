# ENKU Base R35 — local high-side PMOS, remote low-current slide

## Actual engineering source
- Active PCB: `hardware/mainboard/kicad/enku-mainboard-r1.2-base-local-load-switch.kicad_pcb` (125 footprints, four layers, currently no routed power copper).
- Power schematic: `hardware/mainboard/kicad/power.kicad_sch`.
- R34 board preserved for comparison.
- **Manufacturer review**: [Alpha & Omega AO3401A official](https://www.aosmd.com/products/mosfets/p-channel-mosfets-8v-60v/ao3401a), [original datasheet](https://www.aosmd.com/sites/default/files/res/data_sheets/AO3401A.pdf). Device in full production. SOT-23 pin1 Gate; pin2 Source; pin3 Drain; P-channel -30V, ±12V Vgs, Rds(on) ≤85mΩ at Vgs=-2.5V, nominal 4A at 25°C. Thermal margin on our actual 4-layer board still unverified.

## Critical topology change: stop routing device current through case-edge switch

R34 switched **VSYS → SW1 upper left at (30.5,29) → SYS_EN VIN near bottom at U4 (58,91)**. That doubles the long high-current path, is susceptible to excessive track losses/interference, and mechanically couples PCB power rating to an unsourced small slide switch.

R35 instead:
```
 BQ25185 SYS (VSYS) ------- Q2 AO3401A Source pin2
                             Q2 Drain pin3 ------- SYS_EN -> TPS63802 VIN/EN, C9/C10
             VSYS --- R40 100k --- PWR_GATE (Q2 Gate pin1)
                                               |
                                     SW1 case-edge slide -> GND
 SYS_EN -- R13 100k -> GND  (discharge/pull-down)
```
SW1 OFF=open: R40 pulls Q2 gate high towards VSYS, Vgs≈0, PMOS OFF. SW1 ON=closed: gate near GND, Vgs negative, PMOS ON. **SW1 carries only ~VSYS/100k ≈ 25–50µA**, not main regulator input current. The MOSFET is placed near charger and converter (Q2 x55.5,y82.5; R40 x50.5,y82.5), removing the power-loop excursion to case edge. LiPo and BQ25185 remain connected for charging when reader OFF; this is reader-load hard-off, **not physically disconnecting the battery pack**.

AO3401A pin ordering is manufacturer explicit. R35 first footprint draft mistakenly swapped local pad1 and pad2 relative to official SOT23 top view. **Corrected before validation**: pad1 upper-left (-1,-0.95) Gate; pad2 lower-left (-1,+0.95) Source; pad3 right (+1,0) Drain; F.SilkS pin1 dot matches gate.

Physical slider SW1 remains an EVAL 2-pad geometry and its exact mechanical MPN/3D case aperture is not frozen. [C&K JS102011JCQN](https://www.ckswitches.com/products/switches/product-details/Slide/JS/JS102011JCQN) is a **300mA 6V SMT SPDT candidate only**: it may be suitable for low-current gate control, but a real footprint, left/top actuation, switch bounce and assembly travel need fit testing. Its rating does not approve the chosen mechanical orientation.

Electrical signoff blockers: PMOS Vgs variation across LiPo VSYS, power-up/inrush C9/C10, temperature at real peak load, reverse current through MOS body diode, output cap discharge via R13, Q2 source/drain physical 3D layout, always-on BQ STAT/USB/dock inject-backfeed, TMUX off leakage. Prevent switching on false shutdown from GPIO and avoid low-battery thermal failure.

**Good Display GDEY0397T81P pin5 vendor contradiction VDHR vs VSH2 and 3D FPC insertion/fold remain frozen pending manufacturer's email response.** Do not change EPD J3 pinout or order flex until answered.

## Tests and manufacturing
R35 checker validates exact physical PMOS pin mapping, SW1 gate-to-GND, R40 pull-up, U4 VIN/EN switched node, battery ADC gate and 24pin Good Display connector. R35 all-footprint pad clearance checker screens 125 parts, including same-net pad overlap. Native KiCad ERC must be 0 and PCB–schematic parity=0; no critical copper/mask shorts acceptable. Positive CI does not mean fab release while PCB is un-routed.
