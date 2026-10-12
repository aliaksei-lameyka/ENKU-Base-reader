# Good Display technical reply, 2026-10-09 — ENKU Base GDEY0397T81P

**Manufacturer:** Dalian Good Display; supplier reply from Felix Lee to ENKU Reader FPC/SSD1677 email sent 2026-10-08. Reply 2026-10-09. Source [mail thread](https://mail.google.com/mail/u/?authuser=aliaksei.lameyka%40gmail.com#all/1a11c1721b3a3a9e).

**STATUS:** Vendor docs and an Arduino 4-mode reference example received. **EPD FPC electrical/mechanical final production approval remains BLOCKED.** Do not interpret this reply as an explicit pin5 clarification, endorsed J3 footprint or bend radius.

## Local manufacturer source inventory

Received user ZIP `Archive(1).zip` on 2026-10-09, contains:

| File (supplier name) | Scope | SHA-256 (for comparing downloaded versions) |
|---|---|---|
| `GDEY0397T81P.pdf` | Base display datasheet, pin map, glass/FPC, application schematic | `e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc` |
| `sendgb-bvv5EelYNRi/GDEM0397T81P-CAD.dwg` | 2D mechanical CAD | `00399eb8d27e41bd3bcc57f62285bae3427f1ebbe5925039dab9395165b5b8aa` |
| `sendgb-bvv5EelYNRi/GDEM0397T81P-3D.STEP` | Fusion-ready STEP mechanical shape | `abcd05c962518c00da961538da74f4d8f15b67bd0b51fc20b4905636ba884036` |
| `24pin双接触 连接器.pdf` | 24-pin dual contact FPC connector 8.21A0 series drawing | `c2d1760728c3b14170a0500a0b63d12b7317848b2ed8e7026d266a98cd9a07ed` |
| `A32-GDEY0397T81P.rar` | Vendor Arduino example 2026-08-10 (normal/fast/partial/4-gray SSD1677), can be extracted using libarchive | `5381ddfcc3b1ba0e0620e841ddfed592628730fa39243d8d09931501a8a81c3c` |
| `sendgb-Bd2pur2bVox/GDEY0426T82.pdf` + `GDEQ0426T82-FT01C-20260831.pdf` | **4.26-inch Reader Pro only — DO NOT USE TO RESOLVE BASE PIN5** | Pro research in private `raznoglaz1y/ENKU-lab/research/reader-pro-gooddisplay-4p26-frontlight-touch-2026-10-09.md` |

Good Display links (expiry unknown): Base 2D/STEP https://www.sendgb.com/bvv5EelYNRi ; 24-pin dual-contact connector https://www.sendgb.com/67z59uTimqu ; exact panel PDF https://www.sendgb.com/1qIgCj9gXLu ; ESP32 sample firmware https://www.sendgb.com/QTknLKVzwYZ ; Pro bare panel/FL+CTP https://www.sendgb.com/Bd2pur2bVox .

**DO NOT** commit vendor source CAD, PDFs or copyrighted demo firmware to this public repo without distribution permission. This technical note cites filenames/hashes only. Keep original supplied ZIP privately for mechanical and firmware engineering.

## Confirmed Base GDEY0397T81P technical parameters

- Monochrome SSD1677 panel; portrait **480 × 800**, pixel pitch 0.108mm, active **51.84 × 86.40mm**, glass **56.24 × 96.62 × 0.92mm**; panel typical VCI **3.0 V**, operative VCI **2.2–3.3 V**; **VDDIO tied to VCI** in source datasheet; full/fast/partial typical ~3/1.5/0.3s.
- Glass + stepped FPC source drawing: approximate stepped projection **33.66 ±0.30mm**; **12.50 ±0.10mm** critical contact-strip dimension. Contact side and pin1 are illustrated on panel drawing; register these against front/rear 3D views and the actual connector before freezing 3D.
- Supplier: **if FPC bends around to the back, do not place the bend immediately adjacent to the glass; reserve a radius.** They supplied NO numeric minimum bend radius, adhesive keepout dimension or certified folding detail. Do NOT invent one. Prototype 3D should allow adjustable bend/strain-relief and proof with physical panel.
- **Vendor CAD mismatch to verify:** file basename **`GDEM0397T81P`**, while ordered selected model is **`GDEY0397T81P`**. The included STEP geometry MUST be overlay-checked against the PDF and vendor explicitly asked whether both represent **same current-production glass/FPC**. Do not treat CAD basename discrepancy as guaranteed interchangeable.
- Sender did **not** explicitly verify pin1 orientation or the proposed Hirose connector in the email.

## FPC connector alternative from vendor drawing

Supplied dual-contact family drawing `8.21A0-***200` identifies 0.5mm pitch, **H=1.2mm**, contacts on either FPC side; **24-pin row P/N `8.21A0.024200`**. This is a *drawing-derived candidate*, NOT a manufacturer-approved drop-in to our `J3 ENKU:FH34SRJ-24S-0.5SH`. Two footprints have different mechanical H/hold-down pads. No J3 replacement until we verify 24 pad centroids, footprint dimensions, latch, pin1 orientation, insertion direction, stiffener thickness, and sample mechanical fit. Dual-contact does not eliminate pin-number mirroring mistakes.

## BLOCKER: Base pin5 explicitly unresolved, despite new answer

The supplied **GDEY0397T81P pin assignment table** names FPC **pin5 `VDHR`** (“positive source driving voltage (Red)”). The **typical application schematic on p.19** shows the **same pin5 `VSH2`** decoupled by a 4.7uF/25V capacitor to GND. The **active PCB J3 pad5 already has net `EPD_VSH2`**; KiCad symbol also uses `EPD_VSH2`. The Good Display email merely says “refer to the schematic in the datasheet”; it **does not explicitly reconcile the two conflicting labels**, despite us asking.

**Engineering stop:** do not assume p.19 is proof that the actual `VDHR` panel FPC pin is safely the same circuit. Request pin-level written clarification with exact current production panel revision and corrected signed pinout. Hold any J3/EPD HV electrical release and production order until confirmation. The supplied 4.26" Pro datasheet using VSH2 does **not** resolve 3.97" Base ambiguity.

## Electrical design reference; compare, don't copy blindly

Good Display 3.97" reference schematic (typical application p.19) shows:
- VCI/VDDIO nominal 3.3V on the schematic (panel datasheet VCI typ 3.0V and max operating 3.3V); VDD bypass, 4-wire SPI, BS pin low, BUSY high while processing.
- Boost supply L **47µH, Io 500mA**, D1–D3 **MBR0530** minimum 30V/500mA, N-channel Q1 **Si1308EDL** min 30V VDS, VGS(th) max1.5V, RDS(on) max400mΩ, RESE sense R ~**2.2Ω**, gate R ~**1MΩ**, recommended caps **4.7uF/25V** and **1uF/25V**, X5R/X7R.
- Active ENKU PCB uses some different component picks (e.g. `Q1 IRLML6346TRPBF`, `L2 TYS5040_5x5` and alternate pad designs). Verify ratings/inductor saturation, diode polarity and actual nets versus Good Display's schematic and original MPN datasheets before reworking R48 layout. Do NOT silently swap these parts.

## Production/firmware remarks from Good Display

- Waveform/LUT for **each production run is tuned at factory and stored inside panel controller IC**, per Felix. Normal client code should use panel's init/refresh commands and not blindly ship universal hard-coded production LUT. Good Display will notify if init commands need adaptation.
- The supplied Arduino example `A32-GDEY0397T81P.rar` contains `Display_EPD_W21.cpp/.h`, `Display_EPD_W21_spi.cpp/.h`, `GDEY0397T81P_Arduino.ino` and sample images. The demonstration includes full, fast, partial and 4-grayscale modes. **4-grayscale is explicitly unavailable on older panel versions** per example comment; test panel capability before enabling feature flag.
- Example uses **SPI MODE0, MSB-first and 10MHz** configuration, sends SWRESET and BUSY waits. It advises **enter deep sleep after each update** and reinitialize for every full refresh. For partial mode, first establish baseline screen RAM, then periodically perform full refresh after about **5 partial changes** to mitigate ghosting (demo recommendation, not universal guarantee for all temperatures/batches).
- Do not assume Arduino example is production-safe/ESP-IDF-native or compatible with current ENKU OS loader/reflow; create a clean adapter and tests for BUSY pin active-high, command sequencing, panel orientation, mode selection and SD/Wi-Fi operation. Keep supplier code licensing/distribution private pending permission.

## Unanswered supplier questions to follow up

1. **Critical:** confirmed actual 3.97" FPC pin5 signal `VDHR` vs `VSH2` with exact current batch, corrected pinout and HV/reference source.
2. **Critical:** GDEM0397T81P STEP/DWG correspond exactly to GDEY0397T81P current batch? Provide revision label / FPC-7750 if not.
3. **Mechanical:** numeric FPC minimum bend radius, location and permitted flex window, PI/stiffener thickness, contact side, connector orientation and 24-pin mating P/N; compare `8.21A0.024200` and our Hirose FH34 J3.
4. **Commercial:** email supplied **EXW quotes**, did not answer sponsored sample request nor quantities logistics beyond 5–10 FedEx. Keep private quote in ENKU-lab rather than public repo.
5. **Firmware:** are partial/4-gray modes supported by this specific current batch, matching SSD1677 OTP? Read panel temperature options.

**Native KiCad R48 reference:** [37898825797](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825797) ERC0, priority DRC0 but full DRC **168**, electrically unrouted **139**. R49 is vendor documentation intake ONLY; active copper unchanged and **the manufacturing readiness score remains 44% / PCBWay NO-GO**.
