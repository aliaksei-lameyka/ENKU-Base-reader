# ENKU Reader R25D — Should we change the Good Display 3.97" screen?

**Decision: retain Good Display GDEY0397T81P as the preferred R0.2 candidate; do NOT freeze screen/J3 until mechanical FPC simulation.** Researched 2026-10-08 after reviewing exact owner-supplied GDEY0397T81P rev 1.0 drawings, and current manufacturer/reseller catalogs.

## Product fit, not just supplier logo

| Verified raw-panel candidate | Display pixels | Nominal panel outline, portrait (W×H) | Density | Main tradeoff |
|---|---|---|---|---|
| **Good Display GDEY0397T81P**, preferred | 480×800 | 56.24×96.62×0.92 mm | 235 PPI | Ideal within 59mm ENKU pocket width and compact typography; exact stepped/noncenter FPC needs J3 mechanical CAD |
| **Waveshare 3.7in B/W** (raw, SKU 18381) | 280×480 | 54.9×93.3×0.78 mm | 150 PPI | Just 1.34mm narrower than GDEY; about 65% fewer pixels; supplier itself warns FPC prone to failure under repeated bends |
| **Pervasive Displays 3.70in E2370KS0C1** | 240×416 | 53.0×92.99×0.85 mm | ~130 PPI | Independent panel maker and narrower glass, but ~74% fewer pixels than current, must redesign pinout, driving and FPC |
| **Waveshare 4.26in B/W** | 480×800 | 62.37×129.33×0.93 mm | ~180 PPI | Panel wider than 59mm board, also much taller; would abandon pocket-size geometry |

Data links:
- https://www.good-display.com/product/613.html — exact model 800×480, SSD1677 and module 56.24×96.62 (in portrait).
- Owner-provided file `GDEY0397T81P.pdf`, rev 1.0 Aug 2026, page 5 stepped FPC mechanical drawing, page 6 pinout and page 19 schematic. NOT checked into public repository.
- https://www.waveshare.com/product/displays/e-paper/3.7inch-e-paper.htm — raw Waveshare 3.7in 480×280; public price about US$18.29/pc at 100+ (not PCBWay sourcing quote).
- https://files.waveshare.com/upload/7/71/3.7inch_e-Paper_Specification.pdf — mechanical 3.7in drawing, its FPC shape and pin mapping must be reviewed before substitution.
- https://www.pervasivedisplays.com/products/3-70-e-ink-displays/ — independent 3.7in panel 416×240.
- https://www.waveshare.com/4.2inch-e-Paper.htm — vendor lineup, 4.26in BW 129.33×62.37.
- https://frameos.net/devices/good-display-3in97/ — third-party explicitly identifies Waveshare 3.97 and Good Display 3.97 as same panel for its driver; do not assume Waveshare branding changes mechanical FPC.
- https://buy-lcd.com/products/gdem0397t81p — Good Display direct-store 3.97, lists about US$14.88 retail at search date, includes `FPC customization` marketing; source SKU and quote not PCBWay validated.
- https://www.good-display.com/faq/1/ — vendor says nonstandard FPC moulding requires minimum 10k order; custom matrix display can be much higher MOQ, so neither is affordable at ENKU first-batch 50/100/300 scale.

**Do not treat a different dev-board manufacturer (Waveshare, Seeed) as proof of a different underlying EPD glass or ribbon.** Different board-level driver connector does not remove the raw module's ribbon.

## Correct engineering move now

1. Import the manufacturer **page 5 exact GDEY FPC**, mirror/reverse as appropriate for chosen top/bottom physical mounting, check exposed contact face and actual pin1 at tip.
2. Fix J3 placement *relative to free end of FPC*, not screen geometric center. The 3.97 FPC is side-offset; current J3 (58,28) not qualified.
3. Reconsider H2 (72,25) and M2 load path; conditional 3.97 tail-aligned J3 near x69.37, y28 overlaps its nominal Ø5.5 mm screw-head study envelope, according to R25D. H2 should move before ribbon is forced to bend.
4. Check PCB-side and display-side Z spacing and vendor minimum flex bend radius, connector actuation access, battery pocket, and pin polarity.
5. Retain Pervasive 3.7 and Waveshare 3.7 only as **contingencies** if the Good Display mechanical design cannot pass, not as automatic drop-ins.
6. Procurement: ask Good Display or distributor / PCBWay for exact 50/100/300 landed quotes, standard module stock and a sample with physically confirmed ribbon orientation before mass commitment. Avoid FPC-custom-tooling due to MOQ.

### Release policy

No screen change has been made. Do not move J3 or create PCBWay fab outputs solely based on this research. The production BOM and native KiCad DRC/schematic parity remain prerequisites.
