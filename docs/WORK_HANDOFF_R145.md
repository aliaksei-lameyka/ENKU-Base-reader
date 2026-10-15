# R145 - marked layout corrections and next visual review

**Engineering review / NO FAB. Current branch: `engineering/r145-marked-layout`.**

R145 implements the11 correction-queue marks from the R144 green-mark review. The other7 marked local connections are retained. The original R144 source and its evidence remain unchanged. General unmarked zigzags await the user's next visual pass.

Only C18 and C19 move: C18 to(30,83)mm/-90deg, C19 to(27.5,83)mm/-90deg. All141 references,473 pads, values, MPNs, footprint libraries, netlist topology, rules, board outline, USB data, antenna keepouts and panel lands are preserved. Two ordinary0.6/0.3mm GND vias provide local capacitor returns;386 total vias. All six special fill/cap sites remain.

| Mark | R145 change |
| --- | --- |
| G02 | Redundant ESP_EN via approach and local SD_CD duplicate removed. |
| G04 | Coincident GND segments and unnecessary5mm open tail removed; existing real junctions retained. |
| G06/G07 | U9 VBAT right-side loop removed; necessary constrained VBAT feed retained.3V3 SEL/R39 rebuilt as one local tree. |
| G09 | BMI270 decouplers moved below their supply pins: actual track-model C18-VDD1.6715mm and C19-VDDIO1.2375mm, vs8.1188mm from the nearest old C19 to VDD and3.4571mm to VDDIO. Local GND returnsabout0.862/0.850mm. |
| G11 | Exact repeated short C4 pad tracks removed; physical capacitor/via connection retained. |
| G12 | CHG_ILIM_VSET folded-back tail removed. |
| G15 | C11/3V3 network rebuilt without the triangular meshes; existing0.5mm output-capacitor branch and all three power vias retained. |
| G16 | Small GND pocket/overlaps replaced by a clear local tree preserving capacitor returns. |
| G17 | Top-side microSD MOSI loop removed. One data path remains; original two-via B.Cu pullup detour retained because adjacent Top nets block a short legal same-layer path. J2.3/R20.2/R91.2 preserved. |
| G18 | Shared USB pad duplicate tracks and VBUS folded-back parallel spur removed; all connector pin aliases, CC nets and ESD ground preserved. |

204 old copper objects removed;45 added. Other retained copper objects are identical by UUID/geometry/net/layer/width. Existing reference positions are preserved except the two declared capacitor moves. All deliberate changes are finite in `scope_R145.json`; no historical golden is regenerated.

## Executed local checks

- Exact KiCad10.0.7 native DRC/ERC/opens/schematic parity:0/0/0/0 after refill/save.
- Full four-layer native-to-Gerbonara copper comparison;11 Gerber functions/units/precision, separate PTH/NPTH drills and slots, current-point IPC356, mask/paste/silk and native BOM/CPL validation.
- Independent Gerber connectivity:84 named nets, no shorts, opens or missing lands; deliberate physical bridge and moat/open detected.
- Netlist topology identical to R144. Only two footprints moved. Five effective preservation faults detected, plus inherited startup/electrical/OEM faults. No rules relaxed.
- All14 FAST-net centreline inventories covered by at least one actual inner GND projection. This is geometric support, not EM qualification.
- OEM part/land/pin checks, TPS3890 copper/mask/paste checks and10 effective panel/connector faults pass.120 fitted top parts,19 bare entries, R67/R99 DNP and R97 FIT unchanged.
- No same-net closed centreline face above the established0.005mm2 outside-pad threshold remains in the corrected marks. G08 retains the reviewed ground return. Detector limits still apply.

PCB SHA256: `bee45ea1b8e4532112e6ec91a181a1e1bd42d758ad981bf91a8a34e967dd924c`.

Actual source-pinned GitHub CI38710357144 passed on commit3e559f0aa8e093e82ec6d11003d6f72060fa3d9b. Downloaded artifact API SHA256 and ZIP CRC pass. All24 manufacturing files match after declared creation-timestamp normalization; native geometry is exact and all41 JSON reports match after explicit timestamp/plot-hash provenance and temperature solver roundoff (maximum 1.1102230246251565e-16). See `docs/GITHUB_R145.json` and `docs/qualification/R145/server_comparison_R145.json`. Helper scripts retain historical R144 names where their physical/electrical tests are inherited unchanged. R145 derivatives change only current revision/hash binding or the declared finite scope; the R144 originals are untouched.

## Next review and limits

Use the clean R145 Top Copper map made from the actual new Gerbers. Mark new concerns, including unmarked zigzags. Each area will again be traced through source, schematic, layers and fabrication data before changes.

Physical tests have not run. Existing FPC pose/tolerance, protected battery and bonded NTC, common factory process, MLCC effective capacitance, lifetime/dynamic rails, EPD power and reproducible FCT/per-board acceptance holds remain. R145 is a review candidate, not a manufacturing release.

Recorded current task interval: 0.813h; cumulative measured lower bound 27.509h. Later packaging/save/publication tail excluded.
