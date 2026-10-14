# R143 Good Display / Hirose J3 review

R143 actual PCB `3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266`. All24 signal mappings, signal copper/paste and four corrected hold-down objects pass the source/Gerber audit. Physical fit and production tolerances remain HOLD.

## Supplier confirmations recovered from the actual thread

Felix Lee answered on [2026-10-10](https://mail.google.com/mail/u/?authuser=aliaksei.lameyka%40gmail.com#all/1a1244f1a3c71a96): pin5 VDHR and VSH2 are the same signal, use the panel datasheet application circuit; supplied connector documentation and contact orientation are correct; bending radius is 1-1.5mm; recommended glass-to-bend clearance is at least2mm. For the enclosure use radius **at least1.5mm** and clearance **at least2mm**, retaining the original flex's bend marks and protected bond regions. These dimensions do not establish the folded tail's final pose by themselves.

The supplied connector drawing is **DIANWEI 8.21A0.024200**, a dual-contact0.5mm connector, height1.2mm. The installed BOM part is **Hirose FH34SRJ-24S-0.5SH(50)**, also dual-contact, height1.0mm. Felix's yes refers to the supplied DIANWEI documentation; it is not a statement about the ENKU Hirose footprint. DIANWEI is not a drop-in replacement. The 12/13 October answers concern the4.26-inch Pro frontlight and do not redefine the Base panel.

This review supersedes the unresolved pin5 and unspecified numerical bend limits in the9 October intake and the first R142 packet. Historical R49/R141 evidence remains unchanged.

## Primary source provenance

| Source | Pages / identifiers | SHA-256 |
| --- | --- | --- |
| Original supplied GDEY0397T81P.pdf |26 pages; p5 mechanics, p6 pin assignment, p19 application |`e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc` |
| Good Display 24pin dual-contact connector PDF |DIANWEI8.21A0-C, RevE,2017-06-12;24-pin row8.21A0.024200 |`c2d1760728c3b14170a0500a0b63d12b7317848b2ed8e7026d266a98cd9a07ed` |
| Hirose original2D PDF |EDC-159714-50-08; p1 land/stencil, p2 FPC, p4 row24 |See JSON source record |
| Hirose specification PDF |ELC4-159714-04; p1 thickness/electrical, p2 reflow/handling |See JSON source record |
| Supplier CAD DWG |GDEM0397T81P-CAD.dwg, different basename to selected GDEY panel |`00399eb8d27e41bd3bcc57f62285bae3427f1ebbe5925039dab9395165b5b8aa` |

Hirose [exact part](https://www.hirose.com/en/product/p/CL0580-1255-6-50), [drawing](https://www.hirose.com/en/product/p/CL0580-1255-6-50/documents?path=/api/v1/products/CL0580-1255-6-50/documents/drawing_2d/content?lang%3DEN), [specification](https://www.hirose.com/en/product/p/CL0580-1255-6-50/documents?path=/api/v1/products/CL0580-1255-6-50/documents/spec_sheet/content?lang%3DEN). Original supplier PDFs/CAD are private and are not redistributed here. The original ZIP contains exactly the same panel PDF as the earlier user-supplied copy, verified by hash.

## FPC mating dimensions

| Parameter | GDEY0397T81P / supplier | Hirose requirement or recommendation | Result |
| --- | --- | --- | --- |
| Contact count / nominal pitch |24 /0.5mm |24 /0.5mm |Nominal match |
| Contact1-to24 span |11.50±0.05mm |11.5mm nominal |Nominal match |
| Contact-side orientation |Exposed face drawn in panel p5; supplied DIANWEI confirmed |Top and bottom contacts |Face alone does not require replacement; final pin1 pose still matters |
| Contact-end thickness including stiffener |0.30±0.05mm =0.25..0.35mm |**0.30±0.03mm =0.27..0.33mm**, specification p1 |Nominal match; panel's entire tolerance envelope is not covered,20um at each extreme |
| Tongue width |12.50±0.10mm =12.40..12.60mm |Recommended12.50±0.05mm =12.45..12.55mm |Nominal match; recommended envelope is narrower, not a published guaranteed cavity limit |
| Finger width |0.35±0.03mm |Recommended0.30±0.03mm |Panel is wider than recommended; contact registration/clearance needs acceptance |
| Exposed/stiffened lengths |Panel p5 dimensions1.70±0.30 and3.00±0.30mm |Recommended exposed1.5±0.3 and stiffener2.5±0.3mm, with coverlay condition |Do not equate drawing datums without confirming stop/coverlay/contact engagement |
| Bend / glass clearance |Felix: radius1-1.5mm; clearance>=2mm |Connector requires strain relief for vertical force |UseR>=1.5mm and clearance>=2mm; preserve bend marks, no sharp crease |

The narrower Hirose thickness range is a **qualification gap, not proof that a nominal panel cannot mate**. DIANWEI's recommended thickness is0.30±0.02mm, so switching to the supplier's part does not automatically resolve the full panel tolerance range. Obtain a guaranteed lot-specific contact-end thickness/width, or written acceptance of the exact FPC by Hirose. Check insertion/retention on received samples without forcing the latch. Do not apply tape, shave the stiffener or otherwise rework the flex based on a guessed correction.

## R143 actual correction and independent checks

S1/S2 centers remain local(+/-6.75,+1.25)mm at J3 origin(69.27,34)mm, front, rotation0. Both copper lands and their separate paste-only apertures are now0.40x0.80mm. This follows width(F-E)/2=(13.9-13.1)/2=0.40mm and center(E+F)/4=6.75mm. Copper changed from0.80x0.80; paste from0.80x0.65. Signal copper0.30x0.80 and paste0.25x0.65mm are preserved.

The source audit checks every24 contact, the five individual open pins1/4/6/7/19, R28 VCI/VDDIO link and R29 four-wire selection. Actual Gerber has26 J3 paste flashes with exact sizes/coordinates.10 effective design-fault fixtures include the previous oversized copper and paste. A separate comparison verifies that every other PCB pad, track, via, placement, outline and rule area, and the complete electrical topology are identical to R142. The original footprint library is corrected as well as its embedded PCB instance.

Pin1 remains(75.02,32.75)mm and pin24(63.52,32.75)mm. Pin5 VDHR=VSH2 was confirmed by Felix on10Oct and is not an open naming issue. The remaining FPC dimensional envelope, folded pin1/coverlay/latch, GDEM/GDEY identity and shared stencil/reflow/physical panel operation still need evidence. Hirose peak<=250C, time above230C<=60s. Do not close the actuator empty.

Historical R142 report/source is retained unchanged. Current evidence is in pcbway/05_verification/FPC_connector_audit_R143.json and J3_pin_map_R143.csv.
