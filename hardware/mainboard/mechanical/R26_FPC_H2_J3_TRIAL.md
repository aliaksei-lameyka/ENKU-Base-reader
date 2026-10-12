# R26 ENKU Reader — Good Display actual FPC mechanical trial (NOT final)

This is a research branch **mechanical/r26-fpc-fit-trial**, not a replacement for manufacturing. Base `mechanical/r25-placement-first` kept unchanged.

Source: original `GDEY0397T81P.pdf` rev 1.0 (2026-08-13), specifically manufacturer p5 mechanical FRONT and REAR views and p6 24-pin table, submitted directly by the project owner.

The nominal panel in pocket ENKU remains 56.24×96.62×0.92mm, on PCB 59×101. Physical panel **rotated 180deg with flex exiting TOP**. LCD screen orientation can be compensated in firmware. Flat flex extends 33.66±0.30mm beyond glass short edge, with lateral 12.50±0.10mm 24-pin tongue anchored near right edge after rotation. Front drawing pin 1 is tongue left BEFORE rotation and back view shows a designated CONNECT SIDE. The exact stepped flex with marked folding line must be fit in 3D; this is NOT a simple rectangular cable that may be freely reshaped.

## What ACTUALLY changed in a separate KiCad placement copy
- `hardware/mainboard/kicad/enku-mainboard-r0.3-fpc-trial.kicad_pcb` cloned the copper-free R25 study; baseline R25 untouched.
- **J3 Hirose 24×0.5:** (58,28) → **(69.37,34)**, 0°. The x-coordinate registers the projected center of tongue, not proof that fold can reach y34.
- **H2 rear M2:** (72,25) → **(57.5,25)** to separate right-top tongue and J3 from screw-head Ø5.5 envelope. This is a structural *candidate*, not proven glass-safe. Check actual stepped root/FPC fold against screw head.
- **C28:** (61,34,90°) → **(55.2,34,90°)** to free room next to larger J3 courtyard. The right-edge J3 F.CrtYd now reaches x76.62, just 0.38mm from the outer PCB outline, requiring PCBWay DFM/assembly accessibility approval.
- In `Dwgs.User`, a **flat unfolded tongue envelope** x63.12..75.62, y-11.47..22.19 is drawn (NOT a routed FPC). It extends **31.47mm beyond PCB top y20** before the required fold. Manufacturer's step details and tip-to-plug Z profile are yet to be imported.
- All 122 footprints persist, no traces/zones/vias, all physical pad-net numbers unmodified. Existing study mounting holes H1,H3,H4 remain 2.2mm NPTH.

## Electrical source compatibility warnings from same manufacturer
- FPC **pin 5**: drawing/table name **VDHR** but reference circuit p19 **VSH2**. Our J3 net `EPD_VSH2` reflects vendor p19. Engineering must examine HV regulator and confirm pin5 function before building.
- FPC **pins 6 and 7**: p6 NC but p19 calls TSCL/TSDA and leaves them open: KEEP OPEN.
- FPC **pin15 VDDIO** is tied to **3V3_SYS**, **pin16 VCI** to `EPD_VCI`. Good Display says VDDIO must connect to VCI, p19 wiring physically ties pins15–16 at 3.3V. Treat distinction as **electrical HARD BLOCKER** until EPD_VCI power rail / supply isolation are verified, even if structural KiCad ERC passes.
- Connecting the same 24 logical nets to a physically rotated connector is NOT sufficient to confirm pin1 orientation after a back-fold.

## Release checks
- `check_r26_fpc_trial.py` verifies footprint presence, selected coordinates, source-matched lateral tongue position, 2D H2/J3/cap courtyard clearance and **zero routing** on R26 PCB, with a loud assembly BLOCKED message.
- `check_r25_fpc_registration.py --release` continues to fail on original R25 by design.
- NO Gerbers or BOM/CPL for R26 until manufacturer FPC fold and contact side is 3D fit-tested with real sample, screw load/rear shell proven and full ERC+DRC+sourcing & PCBWay DFM passed.

If 3D fails, prefer redesigning top-fastener system or reconsider glass/module physical orientation; do not force ribbon, drill through display, or invent extra flex extension.
