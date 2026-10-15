# ENKU Base R144 - PCBWay engineering review

**NO FAB. Review/CAM inputs only.** Proposed pilot5-10 units. Board59x101x1.6mm, four copper layers. Exact source SHA256:676c157fb58c1d5b689b4a6841749d8be283982745ce40580c0a33308f7e2d2c. Verified source commit 609f8ac00357b9b0c6b3c43c381469c498453a11, GitHub Actions38693384483 SUCCESS.

01_fabrication:11 Gerber layers, separate PTH/NPTH metric decimal drills, four plated USB shell slots, IPC356, drill maps/report.02_assembly:120 fitted top placements, grouped fitted BOM, all141 classified references,19 bare PCB entries and two DNP R67/R99, all473 native pads and first-pad index.456 emitted pad +384 via IPC356 records. R97 FIT selects PWM; never fit both R97/R99. DNPs have no paste. B.Paste intentionally empty. Coordinates X=board X, Y=-board Y in mm, absolute0,0; native top angles. Supplier import/rotation approval is pending.

03_drawings:board review, ten layer/assembly pages and five schematic sheets. PDF imagery is explanatory; fabrication CAM uses the paired Gerber/drill data.04_editable_kicad:68 files byte-identical to current source.05_verification:actual native, independent and server comparison reports.06_qualification:remaining design/process/physical evidence and per-board FCT procedure.

R144 improves common-rail/reset static margins with TPS389001DSER, precise sense and feedback resistors and forced PWM after soft-start. Initial and declared extra +/-0.1% solder-shift reserves pass. Lifetime adverse-shift scenarios and actual dynamic startup/ripple/load/OFF behavior remain HOLD. See STARTUP_RISKS_R144.md. Forced PWM idle consumption is unmeasured. Mainboard uses BQ24072T, no dock, Hall, frontlight, Qi or battery PCM. Require actual qualified protected two-wire PH2 pack and separately cell-bonded NTC.

384 vias,378 ordinary; nominal ring>=0.15mm, ordinary via/SMD gap>=0.10mm.84 nominal0.20mm bores on1.6mm give nominal8:1 aspect before process tolerances. Five U3 plus one R28 via require resin fill/copper cap. CSV requests are not factory acceptance; Excellon does not encode fill/cap. Approve actual stackup/90-ohm USB, drill/registration/plating, finish/void/flatness, common stencil/reflow and short0.8mm USB stake assembly. TI U11 stencil example0.125mm and Hirose0.10mm guidance need one approved process.

J3 hold-down copper/paste0.40x0.80mm and all24 panel contacts pass OEM/source checks. Felix confirmed VDHR=VSH2, bend1-1.5mm and glass gap>=2mm. Design uses bend>=1.5mm. Guaranteed FPC thickness/width/finger/coverlay acceptance, actual folded pin1, GDEM/GDEY CAD identity and common process remain HOLD. Hirose peak<=250C, above230C<=60s, do not close an empty latch. His DIANWEI confirmation does not approve the different installed Hirose footprint.

Effective ceramic capacitance, EPD HV/overshoot/L2 hot saturation/pulse temperature, battery/NTC, firmware/FCT binary, complete case fit and physical per-board tests are not qualified. Bring up1-2 units first before the remainder. No physical tests, factory upload, order or payment have been performed by this publication. Source and calculations cannot guarantee every prototype starts.

Check PACKET_MANIFEST_R144.json for exact per-file SHA256. Do not mix revisions. Raw server evidence is unchanged; see REPORT_CLARIFICATIONS_R144.md for one informational divider-current correction. Supplier PDFs/CAD are private and omitted.
