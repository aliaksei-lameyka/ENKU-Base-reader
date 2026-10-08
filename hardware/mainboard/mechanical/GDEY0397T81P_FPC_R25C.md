# ENKU Reader R25C — exact Good Display FPC placement and electrical sign-off

**Manufacturing gate: BLOCKED. Do not fabricate placement-first board or fix J3 on intuition.**

The current part is **Good Display GDEY0397T81P**, not previous-model GDEM0397T81P and not a generic SSD1677 flex connector.

## Exact primary manufacturer sources provided 2026-10-08

- [GDEY0397T81P panel specification PDF](https://v4.cecdn.yun300.cn/100001_1909185148/GDEY0397T81P.pdf)
- [SSD1677 controller IC PDF](https://v4.cecdn.yun300.cn/100001_1909185148/SSD1677.pdf)
- [Official Good Display current panel page](https://www.good-display.com/product/613.html)
- [Hirose FH34SRJ-24S-0.5SH(50) mechanical product page and 2D/STEP](https://www.hirose.com/product/p/CL0580-1255-6-50)

**Current retrieval status:** the Good Display CDN links returned HTTP 403/unreachable in automated checks on 2026-10-08. The exact new-panel PDF mechanical drawing was NOT visually inspected or downloaded. Prior GDEM panel photographs/drawings are **not substitute evidence** for the specific GDEY tail shape or solder-polarity convention.

## Confirmed from Good Display public panel specifications

| Parameter | Manufacturer listing |
|---|---|
| EPD | GDEY0397T81P, 3.97-inch monochrome |
| Panel resolution | 800 × 480 |
| Panel module outline | 96.62 × 56.24 × 0.92 mm |
| Active area | 86.40 × 51.84 mm |
| EPD driver | SSD1677 embedded on the DISPLAY (does not replace the 24-pin panel FPC definition) |
| Panel tail interface | 24 contacts at 0.5 mm pitch |

## Verified current PCB placement — **not approved**

- KiCad R25C board 59×101mm, x18…77, y20…121.
- Current **J3** `ENKU:FH34SRJ-24S-0.5SH`, **F.Cu x58 y28 angle 0°**. Centered panel rectangle projects x19.38…75.62, y22.19…118.81.
- Hirose official component: 24 contacts / 0.5mm pitch, top **and** bottom contact faces, 0.3mm nominal FPC thickness, horizontal insertion, ZIF back actuator, connector height 1.0mm.
- Board J3 footprint has 24 numbered signal pads; side-to-side 0.5mm center pitch. This **does not** prove the tail will reach, fold, or mate correctly.
- The 1st contact of a manufacturer's ribbon, folded or reversed, may not line up with KiCad physical pad #1. **Full diagram pin-1 check is mandatory**.
- A raw SSD1677 datasheet cannot resolve GDEY0397T81P *module* FPC pinout, pin1 direction, tail width and mechanical routing. Compare the exact panel PDF's 24-pin table to actual `J3` pad nets, then schematic.

## Actual drawing dimensions to register before J3 move

1. The front-side viewing and back-side bottom diagrams' orientation, **exact physical top/bottom**, module x/y datum and active-area offset.
2. FPC bond-to-glass exit position **x and y** in portrait coordinates, tail width, contact-end offset, steps in the unusual FPC geometry and allowed fold zones.
3. Stiffener thickness/length and whether exposed pads face front, back, or reverse when the tail reaches an underside vs topside connector.
4. Exact 24-contact ordering and optional NCs; inspect if actual panel FPC is 0.3mm (Hirose spec) including stiffener.
5. Mechanical collision check: FPC path vs H1-H4 rear M2 bosses, battery pouch, ESP32 antenna, J2 card tunnel, hard power SW1, case wall and USB-C. No forced bends, solder joints or glass-edge pressure.
6. Candidate final J3 origin and angle derived from free-tail end's accessible pose (show on manufacturing drawing); validate min bend radius from supplier and back-flip actuator accessibility in the shell.
7. Prohibit assembly or fabrication if any mating pin indices are reversed. Recheck via native KiCad pin-net parity once J3's approved location is chosen.

## Revision action

- **DO NOT move J3** from (58,28,0°) without the exact supplier drawing; currently a BLOCKER and explicitly annotated on `Dwgs.User`.
- `python hardware/mainboard/kicad/check_r25_fpc_registration.py` asserts the existing J3 has the expected 24 physical contacts and correct 0.5mm pitch, and always prints pending manufacturing gates.
- `--release` fails by design; it can only become green after engineering supplies actual GDEY drawing dimensions and signoff evidence, not by a guess.
- Keep e-paper tail geometry as a **first-class mechanical constraint** ahead of PCB routing or screw mount finalization.

**Recommendation to project owner:** if the web PDF viewer works locally, save and attach the **GDEY0397T81P.pdf** file (5.2MB) in chat. The actual mechanical drawing can then be rendered at high resolution and the real tail geometry established accurately.

## R25D — manufacturer's actual PDFs verified, 2026-10-08

Owner uploaded original `GDEY0397T81P.pdf` (26 pages, specification revision 1.0 dated 2026-08-13) and `SSD1677.pdf` (46-page controller Advance Information). The PDFs were directly viewed, superseding the earlier inaccessible-URL note above.

**Page 5, front and reverse mechanical views:** panel 56.24 x 96.62 x 0.92mm. Unusual stepped `FPC-7750` extends **33.66 +/- 0.30mm beyond a short edge**, has a drawn fold location, and ends in a **12.50 +/- 0.10mm-wide** 24-pin, 0.5mm-pitch terminal, displaced toward ONE lateral panel edge rather than centered. Front viewing diagram labels terminal 1 and 24 on opposite sides; reversing to back changes apparent left/right. Confirm the 3D folded contact-facing side, insertion Z and required bending radius before fixing the connector.

**Geometric test, if panel physically inverted 180 degrees so FPC exits TOP:** centered glass projects x19.38–75.62, y22.19–118.81. Terminal lateral center should project near **x=69.37mm** (19.38 + 56.24 - 12.50/2), whereas actual J3 is x58.0, y28.0. This ~11.37mm difference is a preliminary *projection*, not an already qualified mating position.

The J3 footprint courtyard is 14.5×4.3mm. Re-centering at x69.37 but preserving y28 gives x62.12–76.62, y25.75–30.05; this collides with the **H2 (72,25) M2 head/boss envelope Ø5.5mm**. A non-electrical J3-sized study rectangle is marked on KiCad Dwgs.User near **(69.37,34.0)**. Neither its Y coordinate nor the tail bend/contact side is approved. DO NOT relocate the electrical footprint or H2 until fit is simulated.

**Electrical module documentation inconsistency:** page 5 and page 6 name physical pin **5 VDHR**; same Good Display document page 19 reference application names it **VSH2** and decouples to GND. Current ENKU pad5 connects to `EPD_VSH2`. Do not rename blindly; check actual boost/HV topology and Good Display clarification. Pin 6 and 7 are NC in page6 but TSCL/TSDA (unconnected) in page19. VDDIO pin15 is required to be tied to VCI pin16 according to page6 and page19; ENKU currently has separate net names `3V3_SYS` and `EPD_VCI`, requiring a detailed power-up/backfeed audit.

**Decision:** HOLD current J3 placement and H2 mount, no new routing until verified folded FPC and pinout audit; SSD1677 controller chip manual does not substitute the exact module's FPC specification.
