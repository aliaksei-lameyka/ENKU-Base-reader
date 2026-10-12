# ENKU Base — U1 Espressif module footprint comparative audit (R30)

**2026-10-08. Diagnostic only — NOT supplier fabrication approval.**

Official original CAD reference: [Espressif KiCad ESP32-S3-WROOM-1 footprint](https://github.com/espressif/kicad-libraries/blob/main/footprints/Espressif.pretty/ESP32-S3-WROOM-1.kicad_mod), compared against [our active Base R30 board](../../mainboard/kicad/enku-mainboard-r0.7-base-dfm-prep.kicad_pcb) U1 `RF_Module:ESP32-S3-WROOM-1`.

## 3mm-offset apparent discrepancy, resolved

ENKU U1 PCB local pad #1=(-8.75,-5.26), #14=(-8.75,11.25), #15=(-6.985,12.50), #27=(8.75,11.25), #40=(8.75,-5.26). The original Espressif counterpart uses (-8.75,-8.26), (-8.75,8.25), (-6.985,9.50), (8.75,8.25), (8.75,-8.26). Each is exactly 3.00mm different in Y with X unchanged.

**Important:** The entire module outline is equally shifted in local coordinates: ENKU F.Fab body rectangle is x[-9,+9], y[-12.75,+12.75] and vendor module body is located 3mm toward local negative Y. Thus relative pad-to-module positions are unchanged for the compared pads. An absolute-origin comparison alone would flag a FALSE assembly defect. **Do not subtract 3mm from only the U1 pads** — that would misalign the real module against its drawn F.Fab body.

This corrects an initial false alarm during comparative source audit. The board origin U1=(33,45,90deg) must still be checked for the actual RF antenna/case physical envelope; these CAD values do not sign off real 3D geometry or PCBWay reflow.

## Pad 41 and production verification

ENKU U1 currently has numbered edge contacts 1..40 once each, plus **13 pad number 41 objects**: 12 Ø0.6mm plated holes, drill 0.3mm under thermal GND and one 3.9×3.9mm SMD thermal pad. Thus the board contains 53 pad entries but **41 distinct pad numbers**, NOT 53 signal pins. Espressif's official file has 51 pad entries (1..40 plus 11 SMD copper regions numbered 41). Installed KiCad stock footprint differs again and its 62 pad descriptors do NOT imply 9 missing ESP32 signals.

Open: drilled 0.3mm holes inside exposed solderable GND land can wick solder during reflow. Decide whether to move ground vias outside EPAD or to tent/fill/plug and planarize per PCBWay capabilities, then review stencil aperture and the module's exposed pad recommendation. Do not rely on a fast footprint library mismatch comparison for this manufacturing decision.

## Adjacent higher-priority comparisons

- J5 USB-C: 22 pad count equal to KiCad stock but pin numbering/geometry differs; verify original GCT USB4105-GF-A-120 datasheet and physical receptacle orientation.
- D1-D3 SOD-123: library pad-1 locally at -1.65mm, our footprint pad-1 at +1.65mm. **Check cathode stripe, net mapping and diode supplier pin-1**; a footprint mirror can be legitimate only if the real physical marking and schematic agree.
- J1 battery footprint not found in installed project KiCad libraries; exact JST orderable variant/pin gender and LiPo NTC map unresolved.
- Generic stock resistors/capacitors with 25–50µm center spacing differences should be examined as a group against solder-paste/assembly tolerances, not automatically replaced in an unrouted board.

**Current unconnected signals: 252; relevant full release KiCad DRC must be clean before PCBWay order.**
