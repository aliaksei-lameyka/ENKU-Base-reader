# J7 TAG-CONNECT — original manufacturer footprint, not production-approved

Source: owner-supplied `TC2030-IDC-NL-Datasheet-Rev-B.pdf`, **page 1**, TC2030-IDC-NL-FP rev B, 12/05/2019.

The actual `ENKU Base` rear J7 is intended for a **Tag-Connect TC2030-IDC-NL** (no-legs) pogo programming cable. **It is a SERVICE PCB PATTERN, not a physical component to solder.** BOM must carry DNL / do not load.

## Vendor drawing (imperative)
- Six **nominal Ø0.787mm ±0.076mm conductive CONTACT PADS**; no solder paste and no solder stencil hole.
- Three **Ø0.991mm ±0.076mm NPTH** (nonplated alignment pin holes).
- Pads pitch 1.270mm; pair of rows y ±0.635mm. Vendor upper row = pins 2,4,6 and lower row = pins 1,3,5 in TOP-LAYER VIEW; rear mount needs mirror and explicit probe/pin1 verification.
- No tracks or vias in shaded central KEEP OUT; no other signal closer than **0.020in / 0.508mm** to any contact pad.
- Compressed pogo nails mechanical reach must be checked, optional retaining clip accesses alignment holes from the other side.

## Current R29 physical footprint NONCONFORMITY

Board `enku-mainboard-r0.6-base-placement.kicad_pcb`: J7 `Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical` located **rear B.Cu x35,y87**.

1. Board J7 has **six Ø0.5mm plated through-hole PADS**, but manufacturer says six SMD-like *unplated-surface contacts* with no paste; vendor explicitly allows thru-hole only at finished hole Ø0.008in/0.203mm or less when stencil cannot be avoided. The current 0.5mm plated signal holes do not satisfy this exception.
2. Board footprint has **zero NPTH alignment holes**; stock KiCad library footprint includes 6 contact + 3 NPTH features.
3. Rear J7 sits nearly directly under F.Cu SW2 BOOT x35.5,y87, which occupies x31.25..39.75,y84..90. Its three required guide holes project into the FRONT SW2 footprint and would affect switch solder pads/courtyard. This is an assembly/PCB drill incompatibility, not seen in single-side courtyard tests.
4. Existing J7 pad numbering also must be compared with manufacturer's *TOP* view after mounting on the *back* face. The currently arranged 1,2,3 in first row and 4,5,6 in second differs from vendor drawing's alternating numbering. Pinout is **not approved**.
5. PCBWay assembly must **NOT place any component** at J7, and the case must provide temporary programming connector access without opening/shorting battery.

**Decision:** DO NOT simply add guide holes at current x35,y87 or blindly flip pad names. First choose a backside access region clear from F.Cu button components and real battery. Rebuild vendor-exact 6 SMT no-paste + 3 NPTH with true B.Cu top/mirror pinout and physical pogo fixture, then run native KiCad DRC including hole/copper clearance, 3D shell review, and re-map schematic UART/BOOT/ESP_EN pins.

The structural inspection script `check_r29_tagconnect.py` documents current failures. `--release` FAILS by design until corrected. This is a concrete pre-PCBWay gate.
