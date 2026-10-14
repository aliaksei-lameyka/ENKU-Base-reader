# R142: Good Display panel and Hirose J3 document comparison

Reviewed 2026-10-14. PCB source unchanged: `1ce355545d21d849e924f537488b5c9b9d59e9a8fa3cbbd129839823a7493ebf`. Electrical and nominal signal-land review: **PASS**. Production FPC tolerance, folded assembly and DFM qualification: **HOLD**. Physical tests: **NOT RUN**; manufacturing: **NO FAB**.

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

## Actual R142 electrical map and lands

`audit_connector_R142.py` reads the actual saved PCB, verifies its source hash, compares J3 against the executed native geometry and netlist, and checks the26 actual J3 paste flashes in the paired Gerber. Results are [FPC_connector_audit_R142.json](evidence/R142/FPC_connector_audit_R142.json) and [all24 contacts](evidence/R142/J3_pin_map_R142.csv). Eight effective design-fault fixtures are rejected: reversed24 nets, pin5 grounded, NC6 loaded, mirrored pad1, pitch error, shifted hold-down, missing VCI bridge and wrong BS1 selection. These are source/model faults, not new physical or Gerber conductor fault-injection results.

- All24 numbered contacts match the panel assignment. Pin5 -> EPD_VSH2 -> C28 **4.7uF/25V to GND**, agreeing with p19 and Felix's clarification. NC1/4/6/7 and test-only VPP19 remain individual open nets, with no tracks. TSCL/TSDA aliases on6/7 do not load the exact panel's NC pins.
- VDDIO15 and VCI16 are linked through fitted **R28=0R**. **R29=0R** holds BS1 low for4-wire SPI. VDD18 is a core-regulator bypass node, not another external3V3 input.
- J3 origin **(69.27,34.00)mm**, rotation0, F.Cu. Pin1 **(75.02,32.75)mm**, pin24 **(63.52,32.75)mm**, in the unmirrored KiCad F.Cu view. Use these datums, not a mirrored rear screenshot, in the final assembly drawing. A dual-contact connector does not prevent pin1-to24 reversal after folding.
- Numbered copper lands **0.30x0.80mm**, pitch0.50mm; signal paste **0.25x0.65mm**, both agree with Hirose's nominal recommendation. Recommended stencil thickness is0.10mm, not yet an approved shared stencil/reflow process.
- Hold-down centroids **x=±6.75mm**, y offset2.50mm from the signal row, agree with the drawing. OEM E=13.1 and F=13.9 are the inner/outer edges: recommended hold-down width **(F-E)/2=0.40mm**, not0.80mm. Their centers are correctly **(E+F)/4=6.75mm**.
- Actual hold-down copper is **0.80x0.80mm** and paste **0.80x0.65mm**, versus recommended **0.40x0.80mm** for each. Paste rectangle area is0.52 vs0.32mm2, **62.5% more**. This expansion is not a signal-pin reversal or electrical short, but it is not an exact OEM land/stencil reproduction. Obtain assembly acceptance or revise the lands under a separately verified hardware revision. No source copper or historic reference was silently changed in this document pass.

## Remaining concrete closure items

1. Guaranteed production contact-end thickness/width and acceptance of the panel's finger/coverlay geometry for the actual Hirose part.
2. Folded pin1-to-pin1 assembly datum, insertion stop, latch travel, stiffener/coverlay, bend marks and strain relief in the current case. A flat FPC silhouette and matching pitch do not establish a stress-free3D fit.
3. Identity/overlay of the supplied **GDEM** CAD versus selected **GDEY** glass/FPC revision. No written equivalence was found in the retrieved Base replies.
4. PCBWay acceptance of expanded hold-down copper/paste, common stencil and component-specific reflow limits. Hirose spec: peak<=250C, time above230C<=60s. Do not close its actuator while empty; secure the flex if vertical force is expected.
5. Actual panel startup, refresh, HV and combined-load tests. The written pin5/bend answers do not substitute these tests.

Existing native source DRC/ERC and independent conductor results retain their tested-source status. They were not rerun for this documentation-only pass. The source file SHA and manufacturing exports remain identical to the successful server-tested R142 design.
