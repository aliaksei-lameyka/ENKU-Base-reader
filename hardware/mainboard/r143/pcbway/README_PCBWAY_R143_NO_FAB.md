# ENKU Base R143 - preliminary PCBWay engineering review

**NO FAB.** Review inputs only. Source revision R143; native10.0.7;59x101x1.6mm, four copper layers.

01_fabrication contains11 Gerber layers, separate PTH/NPTH decimal metric drills, four routed USB shell slots, IPC356 and drill maps/report. No copper-only substitute.
02_assembly contains114 fitted top placements, grouped fitted BOM, all134 classified references including19 bare entries and R67 DNP, all453 native pad rows and first-pad index. Native and mapped CPL use X=board X and Y=-board Y in mm, absolute0,0 origin and original top angle. Supplier import/rotation approval is pending. R67 has no paste; B.Paste is empty.
03_drawings contains board review, ten layer/assembly pages and five schematic sheets. PDF imagery is explanatory; fabrication uses the actual Gerber/drill set.
04_editable_kicad is byte-identical to current R143 source.05_verification contains actual native and independent reports.06_qualification specifies remaining physical and manufacturer evidence.

Five U3 vias plus one R28 via require resin fill and copper cap with approved finish/flatness/voiding. CSV requests are not process acceptance; Excellon does not encode fill/cap.373 total vias,367 ordinary vias, nominal annular ring at least0.15mm.84 nominal0.20mm bores on1.6mm give nominal8:1 aspect before process tolerances. Approved stackup/90-ohm USB, stencil and USB short stake assembly remain open.

EVT BUILD BLOCKED: joint logic/panel nominal supply3.24549V has only8.195mV upper and10.727mV reset release static margin in PWM; actual MODE permits PFM. See STARTUP_RISKS_R143.md. Felix's10Oct reply closes pin5 VDHR=VSH2 and specifies bendR1-1.5mm/glass clearance>=2mm. All24 J3 contacts and signal lands/paste pass. S1/S2 copper and paste are corrected to OEM0.40x0.80mm. Guaranteed FPC thickness/width and finger/coverlay acceptance, folded pin1, GDEM/GDEY CAD identity and common J3 stencil/reflow process remain open; see FPC_CONNECTOR_REVIEW_R143.md. Protected battery PCM/NTC, case fit, firmware, SD/EPD/USB-MSC and physical tests remain open. No factory upload/order/payment or production firmware release has been made.

Check PACKET_MANIFEST_R143.json for source hash and exact per-file SHA256. Use only this revision's paired files; historical reports are comparison controls, not current factory inputs.
