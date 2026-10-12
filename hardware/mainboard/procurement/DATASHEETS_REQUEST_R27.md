# ENKU Reader R27 — documents to send for original-supplier PCB verification

**Project owner: Please upload the PDFs to this conversation, keeping their original filenames.** Main firmware/schematic/net and draft component register are in `ENKU-Base-reader`; this is the open datasheet procurement checklist. Manufacturer/part number and CAD are source-of-truth, not catalogue thumbnails.

**Already received in chat:** exact `GDEY0397T81P.pdf` (panel mechanical FPC rev 1.0) and `SSD1677.pdf` (driver IC), no repeat required. Good Display's own original FPC **FPC-7750 2D DXF/DWG** plus fold/stiffener/contact-face spec is still needed from the manufacturer. Current contour is digitized from exact PDF page 5; only 33.66mm reach and 12.50mm tongue width are precisely drawing-anchored. It is NOT a folded 3D mating model.

## Priority 1: mechanical fit and edge access
| Ref | Actual or candidate component | Data source (vendor first, China/LCSC for procurement) | Ask for |
|---|---|---|---|
| J3 | Hirose FH34SRJ-24S-0.5SH(50) | https://www.hirose.com/product/p/CL0580-1255-6-50 | English 2D drawing PDF + full FH34 catalog/user guidelines + STEP zip; 0.3mm contact/stiffener, actuator, insertion direction |
| J2 | Hirose DM3AT-SF-PEJM5 | https://www.hirose.com/product/p/CL0609-0031-0-00 | English 2D PDF + assembly/mating guidelines + STEP; insert/eject stroke, edge keepout |
| J5 | GCT USB4105-GF-A-120 | https://gct.co/files/drawings/usb4105.pdf | Original mechanical drawing; PTH slots, NPTH, mouth overhang, height |
| SW3–SW6 | G-Switch GT-TC035A-H0195-L3 **C915811** candidate | https://www.lcsc.com/product-detail/C915811.html | Exact four-contact pinout, recommended land pattern and recessed milling clearance/STEP; physical samples |
| SW1 | G-Switch MK-12C03-G015 **C2890358** candidate | https://www.lcsc.com/product-detail/C2890358.html | SPDT 3-pin land pattern, slide travel/height/current, STEP; current/inrush of hard-off circuit is unresolved |
| J1 | JST PH 3-pin horizontal `S3B-PH-SM4-TB` only candidate | https://www.jst-mfg.com/product/pdf/eng/ePH.pdf | SMT drawing + matching plug/housing/pin genders, LiPo positive/negative/NTC wire map |
| Battery | **Not yet selected exact vendor.** LP505060 nominal envelope only | Supplier's exact model datasheet, factory packing list and dimensioned STEP | protected 1S capacity, pouch thickness/swelling + connector/wire exit, real protection IC, NTC type; do not substitute random similarly named LP505060 |

## Priority 2: schematic, power architecture, placement and RF
| Ref | Part | Manufacturer document |
|---|---|---|
| U1 | ESP32-S3-WROOM-1-N16R8 | https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf — antenna keepout, RF ground, pad/courtyard, boot/strapping |
| U2 | TPS2121RUXR | https://www.ti.com/lit/ds/symlink/tps2121.pdf — RUX 12-pin physical map, mux priority/current/thermal and board placement |
| U3 | BQ25185DLHR | https://www.ti.com/lit/ds/symlink/bq25185.pdf — charging, NTC/TS, protection, 10-pin DLH footprint |
| U4 | TPS63802DLAR | https://www.ti.com/lit/ds/symlink/tps63802.pdf — DLA 10-pin layout, decoupling and power loops |
| U5 | Bosch BMI270 | https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi270-ds000.pdf — axes, reflow / handling |
| U6 | DRV5032FBDBZR | https://www.ti.com/lit/ds/symlink/drv5032.pdf — exact FB sensitivity/polarity and magnet positioning |
| U8 | ST USBLC6-2SC6 | https://www.st.com/resource/en/datasheet/usblc6-2.pdf — connector-side ESD, correct SOT23-6 pads |
| Q1 | Infineon IRLML6346TRPBF | https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlml6346-datasheet-en.pdf — pinout MOSFET and SOT23 |
| L1 | Murata DFE201612E-R47M=P2 | https://www.murata.com/en-us/products/productdetail?partno=DFE201612E-R47M%23 — vendor mechanical/copper footprint 0.47uH |
| L2 | Laird TYS5040100M-10 | https://www.laird.com/products/inductive-components-inductors-for-power-and-signal-lines/wire-wound-smt-power-inductor/tys5040/tys5040100m-10 — height 4.0mm vs enclosure stack |
| SW2 | E-Switch TL3342 **family only** | https://www.e-switch.com/product/tl3342-series-low-profile-smt-tactile-switch/ — select EXACT ordering code before population |
| J7 | Tag-Connect TC2030-IDC-NL target footprint | https://www.tag-connect.com/wp-content/uploads/bsk-pdf-manager/2019/12/TC2030-IDC-NL-Datasheet-Rev-B.pdf — pad/hole stencil keepout; **no physical part soldered to J7 footprint** |

## Not orderable / sourcing unresolved

- **J6 dock pogo** is presently a 4-pad PCB footprint, not an approved contact-probe specification: select real probe/spring carrier, magnet positioning, compression stack, mating tolerance and supplier before component BOM.
- **SW1 and SW3–SW6** remain tentative, not source-qualified exact production footprints. C915811 recessed geometry may require special edge milling confirmed with PCBWay. Do not place order from LCSC stock alone.
- **Passive C1…C30, R1…R38, D1…D3** still need actual source MPN and tolerance/current/voltage before mass assembly, but can be batch-qualified after electromechanical pins and power scheme.
- **H1–H4 M2 NPTH** require the actual screw, washer/head, stand-off/nut or insert spec, and glass-safe load path. A 2.2mm PCB hole alone is not proof.
- Do not ship proprietary vendor full STEP assets to the public GitHub repo without permission; use them locally or upload here for validation.

## Engineering workflow

For every supplied component: audit **Manufacturer spec / geometry / pin-1 / footprint / pad-net match / assembly rotation / STEP/stack / PCBWay vendor quote and PnP**. Red flags get tracked as explicit release blockers; never silently assign `QUALIFIED`.
