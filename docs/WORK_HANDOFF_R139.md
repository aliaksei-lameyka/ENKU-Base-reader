# ENKU Base Reader R139 - completed engineering-review packet / NO FAB

Physical hardware remains R138. Main is 81b34a97c765c0fdb5ded5e4c1d4ed22d06756cb; the engineering work is in engineering/r139-product-qualification. Do not relabel the physical PCB R139 or replace current source with historical r0.x/r2.x layouts.

## Completed in this pass

- Recovered the accepted main source and original main native artifact after the local work interruption; no R138 work was lost.
- Added and ran `hardware/mainboard/kicad/checks/audit_boot_recovery_R139.py`: schematic nodes and native physical connected partitions agree for J7/BOOT/EN/UART/USB/strap and reserved-memory pins. This is source evidence, not a flash/recovery bench result.
- Re-ran actual native KiCad 10.0.7 DRC/ERC: zero violations, opens and schematic parity. The frozen physical PCB SHA256 remains 90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971.
- Prepared a complete engineering-review ZIP: `ENKU_Reader_Base_R138_PCBWay_Engineering_Review_NO_FAB.zip`, 128 members, 2732875 bytes, SHA256 c113ffdac4c2613a2f8736acf692a01c063a4e41b7f521715bab50e7373a3b00. It is supplied as a standalone deliverable, not a production release.
- Retained the exact 24 manufacturing input files from actual main run38311804626: 11 Gerbers, two PTH/NPTH drill files, maps/report, IPC, native BOM/CPL and six process requests. Independent alias comparison preserves all native values, MPNs, origins and angles.
- Added the complete 127-reference/first-pad index, connector and MCU pad/net maps, pending off-board list, recovery/flash contract and 20-group qualification/log templates, all physical rows NOT RUN.
- Exported the five-sheet native schematic, front native numbered-pad view with complete index and 11 native layer views; authored the review/test plan. All four PDFs (30 total pages) were rendered and inspected. Embedded authored fonts prevent viewer substitution; no diagram geometry was invented.
- Verified 1325 pinned historical source hashes and all ZIP/file checksums/CRC, original manufacturing byte identity and BOM/CPL/process semantics. See `qualification/R139/PCBWAY_PACKET_R138.json` for exact evidence and PDF counts.

## Highest-priority engineering work next

1. Close startup with USB100 initial mode, blank flash, weak/absent battery and PCM-open; analyze reset ramp/cycle behavior. Source-supported 10k/1uF EN RC alone is not a guarantee. Decide a supported source policy and whether power-monitor hardware is necessary before release.
2. Close NTC electrical faults and mechanical retention, especially R82-open floating TS and a sensor detached from a hot pouch. Validate guaranteed tolerances/leakage or change the circuit based on justified limits; do not wave away the faults because sensor-open/short nominal models inhibit.
3. Establish real-pack CC/CV, timer, termination, recharge, thermal and combined-load behavior. TI dynamic timer slowing makes a simple wall-time comparison insufficient. Do not bypass charging safeguards.
4. Bind validated diagnostic/release firmware, approved flash offsets/hashes, fixture and numeric FCT limits to the final PCB/BOM. Firmware may exist elsewhere; none is validated and supplied for R138 in this packet. Native USB flashing is separate from OTG MSC and safe exclusive SD ownership.
5. Finalize exact panel/FPC, current complete case CAD and two qualified thin 2000-2500mAh PCM packs with CN/PL supply. No case thickening; confirmed 5.2mm AKY0156 is rejected. Supplier messages from the existing threads must not be duplicated; Koosay already received its provisional-envelope follow-up on12Oct18:59Z.
6. Obtain job-specific factory approval for stack/90-ohm USB, 91 nominal0.20mm bores on1.6mm, six actual fill/cap requests, U1 EP grid, USB short stakes and stencil. No approval is inferred from a published capability page.

Read `PRODUCT_QUALIFICATION_R139.md`, `PCBWAY_MANUFACTURING_NOTES_R138.md`, `FACTORY_FLASH_CONTRACT_R139.md`, original `GITHUB_MAIN_R138.json` and the R135/R136 power/NTC/capacitance sources. The original BAT and supplier audit evidence is already retained; no new outgoing mail was sent here.

## Rebuilding the review views

`docs/build_pcbway_review_R139.py` requires the pinned KiCad10.0.7 application, Python PyMuPDF/reportlab/pypdf and a fresh output packet directory. First create `tmp/pdfs/schematic-core.pdf`, `assembly-core.pdf` and `layers-core.pdf` with the current source using native CLI exports. Schematic: all sheets, black/white. Assembly: F.Fab,Edge.Cuts, mode-single, scale1, exclude refdes/value fields, sketch pads, cross out DNP, suppress property popups; no title border. Layers: F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.SilkS,B.SilkS,Edge.Cuts, mode-multipage, scale1, black/white, suppress popups, no title border. Run native DRC with parity and ERC into `pre_delivery_drc_R138.json` / `pre_delivery_erc_R138.json` in that build directory. Then run the builder with `--build-dir` and `--app`.

Builder output is initially visual-QA PENDING. Render/inspect final PDFs before setting PASS; after any edit rebuild manifest/checksums/ZIP and validate original-file identity. The authoritative manufacturing files always come from the retained accepted artifact. Do not freeze, reconstruct, loosen guards or change physical source to make a documentation build succeed.

Orders, purchases, production, factory uploads and supplier messaging were not performed. The package is ready for engineering review; all physical product qualification and consumer release remain HOLD. Maintain measured-hours records without counting the overnight interruption as work.
