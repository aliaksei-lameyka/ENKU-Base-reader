# R146 - user-marked zigzag and routing review

Engineering review / NO FAB. Branch: engineering/r146-zigzag-review.

The 78 recorded regions from the user's annotated R145 Top Copper image were traced through the immutable R145 geometry, current pad netlist and all four copper layers. R146 simplifies local copper in 77 regions. Z49 retains the BMI270 INT1 escape because the proposed direct segment intersects the physical U5.3 land, even though that pin is electrically unused.

730 old F.Cu segments are removed and 138 current F.Cu segments added: 3445 to 2853 routed segments in total, with 16.00742245mm less centreline copper length. All 386 via positions, sizes, drills and UUIDs are unchanged, including all six fill/cap sites. All 141 footprints, 473 pads, values, MPNs and netlist topology remain unchanged. The R145 C18/C19 placement and short decoupling are retained.

All B.Cu and both inner-layer tracks are byte/geometry-identical by UUID. USB D+/D- and their ESD-side data nets are unchanged. No track is narrowed. Two reviewed GND shortcuts use0.25mm throughout instead of mixed0.25/0.20mm and0.25/0.22mm legs; this only widens the short return portions.

The generic shortcut prefilter preserves endpoints, same-net local contacts, copper clearance and keepouts. It rejects any FAST signal shortcut with a gap in the actual inner-GND projection after the existing explicit own-via-antipad exclusion. Additional individually reviewed changes:
- Z17 EPD_CS: remove the unnecessary short approach to the via; endpoints retained.
- Z28 BTN_R2: replace the via-entry kink with a direct local segment.
- Z29 USB_VBUS_VALID: remove the50um folded corner; preserve the main controlled bend.
- Z44/Z48 GND: remove short redundant bends and use the wider existing0.25mm width throughout.
- Z54 CHG_ISET: keep the horizontal R9.1 branch and replace its diagonal leg by the vertical connection at X50.55mm. The resistor remains connected; a one-segment deletion that would isolate it was rejected.

Complete local KiCad10.0.7 native DRC/ERC/opens/parity0/0/0/0 passes. Independent complete four-layer Gerbonara copper equality,11 Gerbers, separate PTH/NPTH drills and routed slots, IPC356, native120-part CPL, fitted/classified BOM, DNP/paste/mask/silk,84-net conductor graph, effective physical open/short injections, OEM lands and10 connector faults pass. All14 FAST-net inventories satisfy the unchanged both-inner-GND projection acceptance. Geometric coverage is not EM qualification.

Current PCB SHA256:89487b178c663ad0e0c2b5e574bd9727f27c19be9012936d6786e7813b9b76d1.
Immutable R145 reference PCB SHA256:bee45ea1b8e4532112e6ec91a181a1e1bd42d758ad981bf91a8a34e967dd924c.

The current project settings are byte-identical to R145 and were restored after native board API saving introduced defaults. The unchanged exact-source guard detected that side effect; the complete final run uses the original rules. No guard threshold or fabrication rule was relaxed. Historical R144/R145 guards and golden evidence remain untouched. Raw inherited helper/report names may contain R144; their PCB hashes bind the actual R146 payload. R146 derivatives change revision/hash binding or add finite preservation checks.

Actual source-pinned server CI is pending at initial publication. See docs/GITHUB_R146.json once the actual run and downloaded artifact are verified. The next clean map must be rendered from the final R146 Gerber files, with the same coordinate axes as R145.

Physical tests are NOT RUN. FPC physical pose/fit, protected battery and bonded NTC, factory stackup/drill/fill-cap/stencil, MLCC effective capacitance, dynamic rails/EPD waveforms and reproducible FCT/per-board acceptance remain open. No factory submission, fabrication, procurement, supplier message or startup guarantee is implied.

The first observed R146 interval is2026-10-15T10:27:48Z..10:38:05Z. The interruption10:38:05Z..14:45:17Z is excluded. The resumed bounded interval is accounted separately in the ledger.

