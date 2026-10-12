# R138 copper and annular-ring review — NO FAB

Current source PCB SHA256:90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971. Accepted parent main:f2016c82473b2c51997a6803f4bc74e02d184c0d. The editable board remains59×101×1.6mm; case thickness must not increase.

R137 had165 nominal0.10mm via rings, including five U3 thermal vias. A blanket0.50/0.30→0.60/0.30mm growth produced461 actual native clearance findings involving82 formerly0.50mm via UUIDs. That trial was rejected. R138 enlarges accessible copper lands and uses finite reviewed0.20mm bores where growth conflicts with existing copper, USB reference or service contacts.

| Diameter / drill, mm | Count | Nominal ring, mm |
| --- | ---: | ---: |
|0.70 /0.30|88|0.20|
|0.60 /0.30|150|0.15|
|0.50 /0.20|91|0.15|

All329 vias are checked individually. The project ring minimum strengthens0.10→0.15mm; the explicitly reviewed drill floor changes0.30→0.20mm. Existing clearance rules, exclusions, severities and physical electrical requirements are retained. The obsolete USB4105 locating-peg exception is removed because the actual USB4215 has no locating holes. This is a physical geometry change with an explicit smaller-drill tradeoff, not factory acceptance.

All323 ordinary vias remain at least0.10mm from every actual SMD land. Nineteen ordinary vias were relocated; deterministic local stubs retain junctions and avoid breaking existing connectivity. One redundant U5 GND via and its obsolete segment were removed; its other feed terminates at the existing central GND via. A proposed removal of the R28 supply via split3V3 and was rejected. The accepted via lies wholly inside R28 pin1 and requires actual resin filling and copper capping.

Five foreign vias beside USB retain their original0.50mm copper envelope with0.20mm bores. Enlarging them initially interrupted either a trace projection or the complete1mm core reference strip, despite native DRC0. The unchanged USB guard now finds zero missing reference area; all pair widths, gaps, branches, layer transitions and lengths remain unchanged. One ESP_EN via beside J7 likewise retains its old land to restore the separate0.508mm foreign-copper service-contact requirement.

The five U3 vias now have0.60/0.30mm geometry with corner offsets±0.53mm so all copper circles remain inside the unchanged1.68mm EP. The center remains48.5,91mm. U3's actual connected B GND spreading area is55.3333mm², exceeding the50mm² geometric objective; its minimum distance from B USB copper is1.00878mm. This does not establish thetaJA, cell temperature or charging thermal qualification. U3 mask/paste union and the two TPS paste windows are unchanged.

Six exact process requests are exported:five U3 plus one R28. Each requests resin fill/copper cap, front untented and back tented, with approval=false. The R28 request is a real additional manufacturing requirement; ordinary tenting is not an accepted substitute. CSVs carry UUID, actual board/Gerber coordinates and nominal land/drill sizes.

Local Native KiCad10.0.7 reports0 DRC/ERC/opens/parity and passes27 independent scopes plus the immutable checkpoint. A separate run without freeze reproduces28 reports, eight native plots and24 manufacturing files after only explicit creation timestamps are normalized. All127 placements,438 physical pads, MPNs/electrical fields, schematic nets, outline, stack thickness and zone parameters match R137. The finite source manifest verifies206 changed copper blocks, three removals and eight additions while1325 older repository files remain SHA-pinned.

Gerbonara1.6.3 independently checks11 Gerbers,354 holes/slots and753 IPC records,107 fitted parts, mask/paste, R67 DNP, all process requests and all four complete copper images. Full images include clear/dark regions and macros, actual filled-zone holes and all native pads/tracks/vias. The unchanged native chord budget is0.005mm; the independent rendering/quantization allowance is0.0002mm. All four layers have zero added or missing copper beyond that budget. The spatially indexed discrete Hausdorff calculation retains the vertex-to-segment metric and was checked against GEOS on containment, curves, holes and separate islands.

Twenty rejection fixtures first establish successful positive guards, then require actual assertions or intended dispatcher rejections. Missing files, import errors and generic runtime failures do not count. Cases include wrong C9, unreviewed rings/bores, ordinary via-in-land, omitted/added fill requests, wrong R28 coordinates, DNP paste and a changed copper image even after its temporary stream baseline is updated. The earlier R137 missing-file C9 fixture was corrected in f201; actual corrected-source run38290363302 and its digest/CRC-checked artifact are retained in[evidence/R137/fixed](evidence/R137/fixed). Older13-case claims remain historical; their original C9 case was invalid.

## Required before an approved EVT order

The PCBWay capability page publishes a0.15mm nominal ring minimum and nominal1.6mm maximum board thickness for0.20mm holes at aspect8. The91 small bores are exactly at that nominal boundary. A+10% board-thickness scenario would give aspect8.8. The particular job must accept actual finished thickness, drill, registration, barrel copper, fill/cap flatness, finish, stackup/90-ohm USB, short USB stake assembly and stencil process. The conditional18µm barrel DC resistance calculation is a sensitivity model, not guaranteed plating, ampacity or heat qualification.

Current complete case CAD and finished-pack T/W/L remain unavailable. Two interchangeable thin2000–2500mAh two-wire protected packs with China and Poland supply remain unqualified. The confirmed5.2mm AKY0156 is rejected for thickness; catalogue dimensions alone do not establish availability, finished PCM envelope or fit. Exact panel/FPC and current mechanical clearance also remain open. No orders, production, supplier messages or factory uploads were made or authorized.
