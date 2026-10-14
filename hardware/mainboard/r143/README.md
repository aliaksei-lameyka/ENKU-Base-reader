# ENKU Base R143 - current engineering checkpoint

Open [KiCad project](kicad/enku-mainboard-r0.1.kicad_pro). Source manifest lists67 files; PCB SHA256`3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266`.

J3 S1/S2 copper and two separate paste rectangles are corrected to Hirose0.40x0.80mm at unchanged centers. Signal copper/paste, all24 mappings and every other physical board object are preserved from R142. Native10.0.7 and full independent audits passed locally and in [run38615866570](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38615866570) for commitc9dc9e624c260154094d23a93028e547f52420e8.

[PCBWay package](pcbway/) includes manufacturing,114 top placements, grouped/all-reference BOM, all453-pad map, source and actual verification. [PDFs](pcbway/03_drawings/) show board review,10 layer/assembly views and5 schematic sheets.

**NO FAB.** The [shared supply/reset/panel design margin](../../../docs/STARTUP_RISKS_R143.md) is not closed. Guaranteed FPC/fold/case, protected battery/NTC, factory process and first-boot firmware also require evidence. Every physical test remains NOT RUN. Proposed first quantity5-10 does not mean an order was placed.

R138/R141/R142 sources/guards remain immutable. All current scripts are in checks/; combine with unchanged canonical support scripts as shown in the R143 workflow.
