# ENKU Base R29: native diagnostic and real Hirose STEP audit

Sources: original J2 and J3 Hirose 2D PDFs and STEP archives supplied by project owner. Their original data is not redistributed.

**J3:** supplier FH34SRJ-24S-0.5SH STEP measures 14.0 x 3.8 x 1.0 mm in its native aligned coordinates. KiCad F.CrtYd is 14.5 x 4.3 mm, centered candidate at (69.37,34), giving just 0.38 mm edge-courtyard gap x76.62 to board x77. Must review body height, FPC insertion, closure/access and real stepped ribbon bend.

**J2:** supplier DM3AT-SF-PEJM5 STEP measures 13.85 x 16.15 x 1.68 mm, but vendor STEP coordinate origin is remote from connector body, so center-alignment cannot be treated as a valid pad datum. Compare Hirose 2D footprint datum when locating full body. The current J2 courtyard intentionally overhangs left board x18 by about 0.78mm. Case slot/ejection still needs 3D verification. Three series resistors R19-21 were inside old J2 courtyard and have been moved out in the R29 study.

**EPD VDDIO/VCI:** Good Display panel p6 explicitly requires pin15 VDDIO electrically connected to pin16 VCI. KiCad pads J3:15 = 3V3_SYS and J3:16 = EPD_VCI. The active schematic bridges those via R28 POPULATED zero-ohm resistor. Separate net names alone do not constitute a break. Added structural gate that refuses R28 missing/DNP/not 0R or swapped pad nets. Must still validate failure/open-jumper condition, vendor pin5 VDHR vs VSH2 discrepancy (p5/6 vs p19), and power sequencing.

**Native KiCad 8:** new workflow native-base-mechanical.yml runs schematic ERC, DRC and schematic parity on the EXACT R29 copy: it temporarily substitutes R29 PCB at old root project name inside CI container only, without modifying the repository legacy PCB. Logs are diagnostics, not green manufacturing status: 120 components unrouted; expect unconnected errors. Do not confuse workflow passing with native DRC passing. Report artifacts contain raw KiCad results. Structural courtyard audit in normal CI is separate.

Outstanding: authenticated full 3D fit of FPC to J3, direct J2 footprint pin/case registration, buttons and hard power footprints, all four rear-access M2 screws under glass, battery package, and complete routing.