# R137 production-file engineering review — NO FAB

R137 fixes three actual output defects found on accepted main R136:72 visible silk strokes below0.15mm; four missing enabled mask/paste layers that let native CLI exit0 while exporting only7 of11 requested Gerbers; and two R67 default-DNP paste apertures despite R67 exclusion from CPL. Native source title now states R137 ENGINEERING/NO FAB.

The72 finite UUIDs retain position, text, visibility and size; all104 visible silk elements now have native effective stroke≥0.15mm and every printed text is≥0.8mm. R67 uses a dedicated ENKU:R_RC0603_YAGEO_REFLOW_DNP_NO_PASTE library in board and connectors sheet so its two copper/mask lands remain and library DRC still passes. The original fitted library and all other component MPNs remain untouched. The new library is an exact transfer with only name, paste layers and its default reference stroke changed.

All127 positions,438 physical pads,3707 copper items, nets, holes, stack, RF keepouts, USB and thermal requests remain physically identical to R136. Source reversal reproduces exact accepted PCB SHA396a7ee137778778539848e9e1a3a7b95518ce329b63425822e191f1ef9c6849; schematic reversal restores only R67's footprint field.1246 original main files, all previous evidence and licenses are SHA-pinned unchanged. Source PCB SHA99f2d9cff7a79cc9347f2430d422493e512e6c3b6d6cf82ffd408e0dd77db798.

Local native KiCad10.0.7:DRC0/ERC0/opens0/parity0,25 independent scopes plus checkpoint comparison. All23 previous scopes are retained, with finite R137 contracts for source preservation, R67 assembly/paste and J7 stroke; independent whole-file Gerber/Excellon/IPC/stencil and visible-silk audits add two scopes.13 rejection cases pass, including valid shifted copper despite updated checksum, missing requested layer, contradictory PTH metadata and reintroduced DNP paste. Immutable local dispatcher repeats the checks without baseline regeneration. GitHub verification is pending until actual source-commit artifact is captured; it must not be inferred from local success.

| Export | Actual verification |
|---|---|
|11 Gerbers|Four ordered Cu, two mask, two paste, two legend and outline; X2 FileFunction, metric4.6 precision, original coordinates and NO FAB title checked. Entire four Cu byte streams equal native accepted R136 after only creation dates and title revision normalization.|
|Drill|346 PTH features=342 round holes+4 USB slots;9 NPTH. All355 features match native geometry at Excellon0.001mm quantization, including slot axis/ends and tool diameter. Raw X2 plating headers are checked because Gerbonara does not infer plating from these comments.|
|Mask/paste|Independent exact-Gerber aperture unions agree with all-board native SVG. Comparison allows the unchanged native project0.005mm chord approximation plus0.0002mm render/coordinate budget; actual image bounds remain within0.0001mm. Back paste is empty; R67 and19 bare-PCB items have no paste.|
|IPC356|All754 actual records match330 vias and424 copper-layer/NPTH pad records, including25 exact NNAME aliases, pin identity, net and position within0.002mm IPC coordinate rounding.14 paste/mask-only primitives correctly produce no electrical test record.|
|BOM/CPL|107 fitted front parts;19 bare-PCB+1 DNP retained separately in classified BOM. Exact MPN/value/group count and native107-row CPL are checked. No supplier origin/rotation acceptance is claimed.|
|Filled/capped requests|Five U3 UUIDs, board/Gerber positions,0.50/0.30mm dimensions and requested fill/cap are explicitly supplied. Ordinary drill files alone do not convey this process.|

All exports are review-only, SHA-listed and retained in native_local_R137.zip. Native coordinates use absolute0,0:X=boardX,Y=-boardY,mm; board envelope X18..77,Y-121..-20. No alternate ambiguous CPL is supplied. Source board is59×101×1.6mm; no case-thickness increase is allowed. Actual Gerber previews are under hardware/mainboard/review/R137.

## Actual remaining PCBWay gates

The published standard annular-ring minimum is0.15mm. Actual native330-via inventory has165 nominal0.10mm rings:160 ordinary plus5 under U3 EP;74 are0.15mm and91 are0.20mm. Current native rules are unchanged and cannot certify a factory process outside its published standard. Repair/re-route these holes to a reviewed diameter/clearance, or obtain explicit suitable process acceptance. Do not silently mark this closed, replace fill/cap with tenting, or call the package PCBWay ready.

Also pending: factory90-ohm USB stackup; U1/U3 common stencil/reflow/fill-cap/flatness/voiding; USB4215 nominal0.8mm stakes on1.6mm board; exact panel/FPC; complete current case and PH2/pack/button/pusher/USB fit; guaranteed effective C7/C8/C9 and TS leakage/sensor fault limits; loaded GPIO/USB/startup/firmware/physical qualification. Native checks do not perform these tests. See retained R136 DFM and bring-up documents.

All10 BAT-REV3 archive members and all9 manifest SHA/size entries were read/checked, including its JSON BOM and work prompt. R129/BQ25185/300mA/3-pin J1 assumptions are explicitly superseded by current BQ24072T/445mA, direct PH2 and separate real NTC. The latest user forbids thicker-case fallback. Existing three supplier threads were re-read without new messages: Koosay still requests compartment limits; Polybattery still has no reply; confirmed5.2mm AKY0156 remains rejected. No thin interchangeable CN/PL pair or maximum finished-pack fit is qualified.

Primary references: [PCBWay capability table](https://www.pcbway.com/capabilities.html), [PCBWay assembly FAQ](https://www.pcbway.com/assembly-faq.html), [KiCad10 CLI documentation](https://docs.kicad.org/10.0/en/cli/cli.html), [independent Gerbonara parser](https://gerbolyze.gitlab.io/gerbonara/). Capabilities do not imply job-specific approval. No production, purchases, messages or factory uploads occurred.
