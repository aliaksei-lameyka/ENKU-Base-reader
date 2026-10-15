# ENKU R144 proposed manufacturing review — NO FAB

Engineering review only. Fabrication, procurement, assembly and stencil release are NOT authorized.
Source: proposed R144 PCB, KiCad10.0.7. Four copper layers,59×101×1.6mm.
All Gerber, drill, IPC and native CPL coordinates use absolute origin0,0:
X=KiCad boardX,Y=-KiCad boardY,mm; original top-side native CPL angles.
Board envelope X18..77,Y-121..-20mm. No supplier rotation/origin normalization is approved.
Gerber soldermask objects describe openings despite negative FilePolarity metadata.
Use the single native CPL and fitted review BOM together; all-classified BOM explicitly retains19 bare-PCB entries and R67/R99 DNP.
R67 and R99 default DNP has no paste apertures. Its copper/mask and optional rework lands remain.
All assembled120 parts are on front; back paste intentionally empty.
Separate PTH/NPTH Excellon files use decimal metric coordinates and routed USB slots.
Excellon alone does NOT convey fill/cap; the five U3 and one R28 UUIDs are explicitly listed in the two process request CSVs.
All386 vias have at least0.15mm nominal annular rings; all380 ordinary vias have at least0.10mm separation from SMD lands.
84 nominal0.20mm bores on1.6mm PCB give nominal aspect8, at the published process boundary.
Finished hole, thickness, registration and barrel copper tolerances require explicit job approval.
All six in-pad vias require actual resin fill and copper cap; no ordinary tent substitute.
Filled/capped under-EP, U1 grid/stencil, USB0.8mm stakes on1.6mm PCB, controlled90-ohm USB stackup,
thermal/fault/firmware qualification, thin replaceable battery and unchanged-thickness case fit remain open.
No current complete case CAD or qualified interchangeable CN/PL battery pair is registered.
Do not interpret Gerber availability, checksum verification or native DRC0 as factory acceptance.
