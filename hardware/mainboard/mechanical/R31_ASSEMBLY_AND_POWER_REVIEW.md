# ENKU Base R31 — assembly pad overlap and power-control review

**Status:** engineering, NOT fabrication-ready. Branch `engineering/r31-assembly-overlap-audit`. Base dedicated no Hall/Qi/frontlight. PCB `hardware/mainboard/kicad/enku-mainboard-r0.8-base-assembly-placement.kicad_pcb`.

## Real new defects found in R30

A pad-level scan (330 placed named-net SMD pads, all footprints regardless of CrtYd) identified three **same-net physical copper overlaps** not counted as KiCad shorts:

| Pair | Original net | Original geometrical overlap (mm² AABB) | Change in R31 |
|---|---|---:|---|
| D2 pad2 / D3 pad1 | EPD_CP_NEG | ~0.140 | D2 (56,49) → (56,50) |
| D1 pad1 / C24 pad1 | EPD_VGH | ~0.094 | C24 (48,42) → (47.3,42) |
| C6 pad2 / C5 pad2 | GND | ~0.040 | C6 (47.35,87.75) → (47.7,87.75) |

These are not cross-net shorts, but overlapping stencil apertures for independently placed components cause assembly defects. An explicit R31 source-geometry gate rejects **all** cross-component SMD pad rectangle overlaps, including same-net intersections, and refuses unreviewed coordinate regression.

## Diode D1–D3

Selected MBR0530 SOD-123 has **pin 1 = cathode**, pin 2 = anode, per manufacturer [onsemi MBR0530](https://www.onsemi.com/pdf/datasheet/mbr0530t1-d.pdf). Current pin pad nets: D1 K=EPD_VGH/A=EPD_SW; D2 K=GND/A=EPD_CP_NEG; D3 K=EPD_CP_NEG/A=EPD_VGL. These **match pin number polarity**, but complete EPD high-voltage pump circuit still needs vendor page-19 reference review.

Legacy drawings had silk box over each SOD-123 solder pad. R31 replaces it with F.Fab body box + **single F.SilkS cathode stripe** by pad 1 and a F.Fab cathode stripe. On real board the stripe faces the designated pad-1 direction. This is subject to final native silkscreen-to-copper and assembly orientation checks.

## USB-C GCT USB4105-GF-A-120

Manufacturer [USB4105 original product/drawing](https://gct.co/connector/usb4105) documents sixteen physical USB2 contacts ordered from component side:

A1/B12, A4/B9, B8, A5, B7, A6, A7, B6, A8, B5, B4/A9, B1/A12.

ENKU J5 current local X/order matches these contact positions; D+ A6/B6 connected to USB_DP_CONN, D- A7/B7 to USB_DM_CONN, CC1/CC2 kept independent, SBU1/SBU2 NC. R31 gate locks actual pad order and nets. **This is not the full original dimensioned 2D/stake-holes/vendor mounting clearance verification**, nor does it approve USB power/ESD behavior or case USB insertion window.

## Battery and hard-off — open serious architectural issue

Board SW1 is an **unqualified two-pad SPST placement** from VSYS to SYS_EN for the TPS63802 buck-boost converter. Charger BQ25185 remains linked directly to VBAT and VSYS, so 'hard power-off' is misleading as a claim of electrical battery isolation. TPS63802 requires EN low for shutdown; R13 provides 100k to GND, but battery charger/system paths are not physically disconnected. Need one explicit product decision before physical switch MPN and pad count can be frozen:

- System-rail shutdown with protected battery still connected to charger (lowest complexity, potentially supports charging while OFF), explicitly characterize battery-only quiescent and backfeed/leakage; OR
- True battery hard disconnect with an actual rated switch/load-disconnect topology, charger-off behavior, external USB/dock on/off state and battery safety reviewed.

Do not blindly replace the 2-pad SW1 with 3-pad G-Switch SPDT: off-state and contact mapping must be analyzed in full circuit.

## Other blockers carried forward

- J1 3-pad PH mating and JST original land pattern / battery wire order NTC; real battery supply/temperature and protection proof.
- Pin 5 Good Display VDHR vs VSH2 and folded FPC-7750 real 3D connector pose.
- ESP32 U1 pad-41 thermal via-in-pad/wicking + RF keepout; side keys C915811 pockets; mounting glass-safe rear screws.
- Copper fully unrouted (~252 initial connections), 4-layer return paths, full KiCad DRC and routed USB, power loops, EPD high-voltage spacing, actual PCBWay assembly BOM, fab panel Gerbers and NPTH.

The R31 test is source geometry only; **not** DRC fab approval. There is no reason to inflate the PCBWay readiness score yet.
