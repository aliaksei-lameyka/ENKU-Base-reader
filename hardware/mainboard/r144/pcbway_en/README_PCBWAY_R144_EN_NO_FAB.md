# ENKU Base R144 - English engineering review package

**NO FAB. Physical tests: NOT RUN.** Proposed pilot:5-10 boards, with the first1-2 assemblies evaluated before the remainder.

Board:59 x101 x1.6mm, four copper layers. Verified source commit609f8ac00357b9b0c6b3c43c381469c498453a11. PCB SHA256:676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c. Source-pinned GitHub Actions run38693384483 passed. The English edition changes documentation only; all manufacturing, assembly, editable KiCad and verification inputs are byte-identical to the verified R144 package.

## Files to use

- `ENKU_R144_GERBER.zip`: separate flat archive for CAM review. All11 Gerber layers, separate PTH/NPTH drills, Gerber job, drill maps/report, IPC356 and the two fill/cap request CSVs are in its root. The archive is also supplied separately.
- `01_fabrication`: original paired Gerber/drill/IPC356 set in its reviewed folder structure.
- `02_assembly`:62 fitted BOM groups,120 top placements,141 classified references, complete473-pad map, first-pad index, CSV process requests and the English BOM/CPL workbook.19 bare-PCB entries, R67/R99 DNP, R97 FIT. Never populate R97 and R99 together.
- `03_drawings`:six-page English board review,10 layer/assembly pages and5 schematic pages. CAM uses the actual Gerber/drill files; PDFs support review.
- `04_editable_kicad`:68 byte-identical source files.
- `05_verification`:actual native/independent reports, source manifest and unchanged source-pinned server artifact.
- `06_qualification`:English manufacturing instructions, FPC review, executed checks, startup risks and per-board FCT plan.

Coordinates:millimetres, absolute0,0, X=KiCad board X and Y=-KiCad board Y. All fitted components are top side. Native top angles require supplier import/rotation approval. B.Paste is intentionally empty.

## Items still requiring closure

Initial and declared extra+/-0.1% solder-shift static reserves pass. Lifetime adverse-shift scenarios and measured startup/ripple/load/OFF behavior remain HOLD. Qualify the actual FPC contact-end dimensions/folded pin1, protected PH2 battery and cell-bonded NTC,90-ohm USB stackup,84 nominal0.20mm bores on1.6mm, six resin-fill/copper-cap sites, short USB stakes, common stencil/reflow, exact BOM/CPL import, effective capacitance/EPD power and reproducible FCT firmware. Physical tests have not been run.

All384 vias have nominal annular ring>=0.15mm;378 ordinary vias have SMD separation>=0.10mm. The five U3 and one R28 sites require resin fill/copper cap. Excellon does not encode this process: review the included request CSVs. No factory order or manufacturing release is made by this package.

Use PACKET_MANIFEST_R144_EN.json for exact file hashes. Do not mix revisions.
