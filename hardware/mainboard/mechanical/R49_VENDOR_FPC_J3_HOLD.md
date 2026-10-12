# R49 — Good Display panel CAD, FPC bend and J3 connector hold

**Do not change active PCB in R49 without written vendor confirmation.** Last electrically Native-verified board: `hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb` (R48).

Supplier STEP/DWG received as `GDEM0397T81P-3D.STEP`, `GDEM0397T81P-CAD.dwg` (letter `M`) while selected Base panel data sheet is `GDEY0397T81P` (letter `Y`). **Must confirm CAD variant identity** before declaring our Fusion enclosure model vendor-accurate.

Supplier explicitly instructs not to put the fold immediately at glass edge and to allow FPC curvature. No bend radius numerical specification. Tail shape should be checked at native 1:1 using STEP and DWG against display outline **56.24×96.62mm**, 24-pin half-mm conductor contact side and manufacturer's original customer drawing. Base portrait chassis keeps USB-C/SD/switch cutouts and removable fasteners.

The provided DANWE 8.21A0 `8.21A0.024200` dual contact connector is a candidate, **not verified equivalence** to active `J3 FH34SRJ-24S-0.5SH`. Freeze neither J3 mechanics nor board edge notch until supplier confirms FPC stiffener + insertion side, pad pattern, max height. A double-contact receptacle may mate with top or bottom contacts mechanically but **pin1 orientation still changes with physical flipping**. Inspect pin1 triangles and actual FPC stiffener.

**Electrical blocker unchanged**: source 3.97" PDF pin5 table `VDHR` and typical p.19 `VSH2` conflict. Current KiCad pad5 carries `EPD_VSH2`; no changes in R49; ask for written confirmation. See [full supplier intake](../research/GOODDISPLAY_REPLY_2026-10-09.md).
