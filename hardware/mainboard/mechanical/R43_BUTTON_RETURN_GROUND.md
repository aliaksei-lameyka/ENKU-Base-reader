# R43 — button return-current topology and upstream gate corridor audit

Branch `engineering/r43-reading-button-ground-returns`, active PCB `hardware/mainboard/kicad/enku-mainboard-r2.0-base-reading-ground-returns.kicad_pcb`. R42 source remains immutable rollback.

**Electrical additions:** F.Cu GND pad2 of four side buttons SW3/SW4 (left) and SW5/SW6 (right) now connects to off-pad plated vias inside the **existing** local inner GND zone envelopes (x28/68, y65.2/77.2). The mechanical button land positions at x25 and x71.2 are still preliminary. No via holes placed in solderable button lands. Existing neighboring local ground bypass branches C26 (panel-HV return), C18 and C19 (IMU/local 3V3) tied to button GND pads on F.Cu, without crossing opposite-net tracks in source preflight.

**Before native verification:** R42 ERC0, parity0, critical0, 239 full DRC non-unrouted violations and 152 unrouted. R43 increases counts to 442 tracks,121 vias (132 footprints,2 ground zones). Only Native KiCad refilled two zones and postfill DRC will prove the four vias are connected; zero other critical defects remains release condition.

**Critical new routing decision:** Module U1 pin4–7 four button signals have *no copper at R42*. Naively routing first B.Cu escape down x31.55..35.36,y55.5 would short/interfere with existing R42 power/BOOT/ground vias near x31.8,56 and x34.09,55.5. Naively taking RHS button signals across y59 on In1.Cu intersects live SPI_MOSI/SPI_MISO near x44.75–45.5. Do NOT assert complete button signal functionality. Plan a constraint-based escape around occupied module channels, preserve antenna and both inner reference planes, and only route once actual side button MPN/actuator design is locked. These side switches are **provisional** `ENKU:READING_BUTTON_PLACEMENT` geometry, not supplier-qualified 3D footprints.

**Power slide SW1 remains OFF-critical:** The current SW1.1 PWR_GATE (27.3,29) to Q2.1 (54.5,81.55) is **not yet wired on copper**. A tempting In1.Cu run along y81.5 would cross SPI_MOSI, SPI_MISO and a 3V3 rail; route must be detoured and matched to final physical switch. SW1.2 GND is unconnected and near ESP antenna mechanical exclusion; avoid blind stitching inside RF keepout.

USB-C MSC microSD and fail-safe VBUS R41 comparator routing remain regression-protected, but native USB D+/D− pair is unrouted pending actual 90Ω PCBWay stackup. GoodDisplay panel pin5 VDHR vs VSH2 and FPC mating remain vendor hold.


## R43 proven in native KiCad

Initial placement of SW3 ground via at (28,65.2) intersected the high-voltage supply capacitor C31 contact1 `EPD_VCI`. The first tests caught the production defect. Moving it to **(28,67)** avoided the SMD aperture while keeping it inside the In1/In2 copper envelope. [Native KiCad pass 37843277589](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37843277589) refilled zones, checked zero shorts/dangling tracks/vias, confirms **all four SW3–SW6 pad2 GND signals electrically connected, zero outstanding SW pad2 GND unrouted**, ERC0, parity0, and reports **146 general unconnected, 239 other DRC violations**. [Active structural checks 37843220711](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37843220711) verified no new via hole intersects an SMD pad. Not a production release.
