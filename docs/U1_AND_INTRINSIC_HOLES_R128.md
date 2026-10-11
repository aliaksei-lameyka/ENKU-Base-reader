# R128 — U1 and intrinsic locator holes

Accepted predecessor is R127 proof HEAD `3c988845ee68df616d5e6ba02212bc9996f2c550`, source `e347e3bad3b76c74b764555880d2e9205fe04038`, tree `8784437db3b03d44a99844eb2760a2971931b89b`. R127 PCB SHA256 is `c2316fa909debdd69577cd565b04bab6e40db01acbfc9c2b6f1362ac4b14b1f2`; R128 is `f53da6653e1f98241a4da7e337aa001a2b8614fa1b3e0685d893d299a18d5fa6`.

## U1 geometry and assembly request

Espressif ESP32-S3-WROOM-1/-1U datasheet v1.8, page45 Fig11-1 specifies a 3×3 array of nominal 0.9×0.9mm copper lands on 1.4mm pitch. R127 used one exposed 3.9×3.9mm copper square under nine 0.9mm paste windows. R128 reproduces the nine nominal copper squares in a new project footprint `ENKU:ESP32_S3_WROOM_1_N16R8_EP_GRID_03_TENT_REQUEST`. Their 3.7×3.7mm envelope and centres match the source drawing. Native GND connectivity is checked for every land.

| Item | R128 native result | Qualification |
| --- | --- | --- |
| Copper EP lands | 9 × 0.9×0.9mm, 1.4mm pitch, 7.29mm² | Nominal manufacturer grid reproduced |
| Top mask windows | 9 × 0.8×0.8mm, explicit −0.05mm margin, 0.6mm web | Project adaptation; registration/process pending |
| Paste windows | 9 × 0.8×0.8mm, explicit zero further margin | Project adaptation; stencil thickness/transfer pending |
| Paste fraction | 5.76/7.29 = 79.0123% | Area ratio only; does not prove paste volume/voiding |
| Thermal holes | Same12 Ø0.3mm PTH with Ø0.6mm Cu lands | All old drills/annuli/positions retained |
| Mask above thermal holes | No F.Mask or B.Mask opening in native plots | Both-side tent request, not a sealed/filled/plugged/capped process |
| Nominal mask/paste edge to drill | 0.15mm | Drill and mask tolerance stack still unqualified |

The copper lands connect through retained annuli and native GND copper. U1 perimeter40 pads, all 417 old pad UUIDs/numbers/nets/drills, all2639 track/via items, placements, outline, zones, RF restrictions, project/rules/exclusions and previous library files are preserved. Exactly22 old U1 pads change declared copper/mask/paste properties (one EP, nine paste-only, twelve thermal holes); eight EP SMD lands are added. Native schematic net node sets are unchanged. Board and MCU-sheet U1 metadata refer to the new exact project footprint.

The module's exact N16R8 rating also matters: v1.8 page3 lists the default ambient range −40..65°C. Operation up to85°C requires PSRAM ECC and reduces usable PSRAM by1/16. No firmware/ECC or whole-board85°C qualification is claimed. Page12 reserves GPIO35/36/37 for Octal PSRAM; module pads28/29/30 are native NC nets with no external copper and one XML node each.

## Active button and USB findings

The supplied original E-Switch TL3340AF160QG drawing P021301 revB dated2008-01-07 shows Ø0.9mm locator holes on4.25mm pitch. Native nominal copper-to-hole gaps are0.075mm at the signal lands and0.150mm at the bracket lands. All16 findings (four perSW3–SW6) are intrinsic to the source-recommended land/hole arrangement. GeneralX.X±0.4/X.XX±0.25mm dimensions do not qualify a factory's drill/copper process.

The supplied GCT USB4105 drawing revB4 dated2023-12-18, sheet1/2, shows two Ø0.65mm NPTH locators at localx±2.89/y−2.605. Its outer GND pad pairs share locations. Native rounded-land gap is0.1944027188mm; the drawing's rectangular land envelope gives0.1750999900mm. Four native findings represent two physical gaps because A1/B12 and A12/B1 are coincident. Recommended-layout±0.05mm does not settle the exact stake variant, PCB thickness or factory process. The current public PDF endpoint returned403; the supplied revision is explicitly identified, not claimed as a confirmed latest revision.

All20 active errors remain under the unchanged0.25mm hole-clearance rule: 18 distinct physical copper-to-hole interfaces. No hole shrinking, peg movement, NPTH-to-PTH reclassification, land clipping, rule weakening or new exclusions. Closure requires an accepted changed design or documented part-specific manufacturing rule/process supported by the controlled drawings and actual tolerances. No supplier communication or order was sent.

## Verification

Native KiCad10.0.7 full severity, all-track-errors, zone refill/save, schematic parity, ERC and XML netlist: **opens0/ERC0/parity0; DRC46=26library+20holes;425pads/117footprints**. U1's former pad/drill library mismatch disappears because board and the new native library footprint match. The other26 remain active:24 compared-pad-equal/other-graphics cases and2 J5 numbering/J7 attribute cases; these are not waived by equal copper geometry.

Twelve independent local guards pass: USB, physical geometry, Q1, manufacturer geometry, approved SW1, Q1/Q2/U9/J7/J5 assembly lands, exact79-part metadata/lands, numeric power, U1 EP/reserved pins, actual mask/paste plots, intrinsic holes, and full source preservation. A separate comparison checks native geometry/results against the committed R128 checkpoint. The same guards run on the actual GitHub source in CI; current server status is [GITHUB_NATIVE_R128.md](GITHUB_NATIVE_R128.md).

Actual native copper, top mask, paste, bottom mask and whole-board images were visually inspected. No GUI session is claimed; these are native KiCad CLI plots rendered faithfully from SVG. The plot guard uses native bbox origin(18,20), checks all nine actual apertures and checks for unintended openings above all twelve thermal holes.

**fabrication_ready=false.** Mask tent formation, drill tolerances, stencil/reflow, voiding, thermal/RF behavior, exact FPC, controlled stackup and enclosure remain unqualified. See [remaining work](REMAINING_TO_BUILD_R128.md).
