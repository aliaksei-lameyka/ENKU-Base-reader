# ENKU R147 handoff

Canonical branch: engineering/r147-mechanical-review. Source commit0dccd442fb7ada7ad982a0ff375ac76560a5b862, tree59c438b0fd151e319433eebc3b07f872cfe8670c, PCB SHA256856e6d84905f978994316e2efcbb398184cf06dc4f95580c203ee244dd918bb2. Local Git HEAD may remain R145; canonical R146/R147 were published via the correct account Git API. Do not restore an older local HEAD over the engineering branch.

All18 latest R146 marks are retained in qualification/R147/user_regions_R146.json;12 areas shortened,38 old segments replaced by13. All141 footprints,473 pads,386 vias, outline, holes and project rules are exactly preserved. N07 direct shortcut would leave0.0533mm to BAT_ADC, N08 shortcut0.168541mm to U5.6 GND; both below0.20mm rule. N01 is a three-way GND branch, N09 preserves a same-net contact, N11/N16 have no removable two-edge zigzag at the mark.

Full local native/independent pipeline and actual server run38763074552 passed; API artifact11985868301 SHA256917c12edd7dd87743f9efb20dd3362b61c9d53d2ee66e5f38a48894b4f206c60, ZIP CRC checked. All24 manufacturing files and41 JSON/native reports agree after declared metadata only. Historical goldens unchanged.

R146 mechanical STEP, CSVs, provenance, terminal/roundtrip/hole checks and separate access zones are linked from hardware/mainboard/mechanical/r146_r147/DOWNLOADS.md. Source mechanics are identical to R147. Nominal finished thickness is1.6mm; native KiCad dielectric1.51mm was analytically re-extruded from its exact face, preserving all25 source footprint holes. Main assembly has14 named components and256 solids. Side-button tips are1.45mm inboard. USB mouth(29,-101,3.18). J7 service contacts are B.Cu and access is below the board.

Vendor STEP: Hirose microSD/FPC, E-Switch side and BOOT buttons, Espressif module. USB reconstructed from GCT dimensions. SW1 body-to-peg datum is HOLD; JST is a conservative nominal envelope. Display FPC pose, selected battery/harness/NTC, real case tolerances and fasteners remain to qualify. Small passives and most ICs are omitted: empty-looking PCB regions are not free boss space.

Physical tests NOT RUN / NO FAB. No factory submission, message, purchase or production release. Current measured cumulative lower bound 28.612h; idle gaps excluded.
