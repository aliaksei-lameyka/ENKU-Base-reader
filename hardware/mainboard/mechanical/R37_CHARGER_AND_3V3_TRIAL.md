# R37 — charger source & local 3V3 pilot copper

**Engineering-only, not a functional or orderable board.** R36 is retained as rollback. Source `hardware/mainboard/kicad/enku-mainboard-r1.4-base-charger-output-trial.kicad_pcb`.

Manufacturer Good Display correspondence on panel pin5 VDHR vs VSH2 and stepped folded FPC awaits written answer. No change in EPD island / J3 connector during this phase.

**New R37 actual KiCad copper (+19 F/B segments, +5 Ø0.7/0.3mm through-vias):**
- BQ25185 U3 pin1 VSYS pad at (49.6,91.8) escapes on F.Cu with 0.18mm width to the rear copper via (49.8,92.3), then ~0.45mm B.Cu to pre-existing PMOS VSYS trunk near (48.6,83.7). This creates a **source-to-MOSFET electrical path** without carrying current to the case switch. Real pad escape width and maximum BQ25185 VSYS current need simulation/thermals and complete 3D.
- Charger output bypass C7 VSYS at (51,94.5) to via (51,96.5), local rear copper tied to U3.1 VSYS.
- TPS63802 output U4 pin6 at (58.75,92) linked to C11 input (59.1,94.4) on F.Cu, and short F/B branches to C12 input (62.3,94.4) and rear TP6 (60,88.5), with extra branch to feedback top R14 input (55.3,89.1). Note ***test point TP6 is B.Cu***; proper vias were used at power components, not under the exposed TP6 metal.
- No GND plane yet: selected staging ensures DRC on copper before adding internal-layer returns. No copper near unknown Good Display FPC.

**These traces are provisional, not complete!** Remaining power: 3V3 upstream U1 and microSD, regulator GND loop/EP pad, return-plane vias, STAT and charger CE behavior, SW1 low-current gate lead, VBAT pack, USB/dock charging, thermal at 4A-rated PMOS and its inrush. Native DRC must reject shorts, mask bridges, copper edge, dangling track. Final fab DRC requires zero violations, all 3D/mating and supplier MPN approval.
