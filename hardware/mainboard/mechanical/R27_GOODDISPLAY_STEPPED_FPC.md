# ENKU R27 — Actual stepped FPC outline from Good Display GDEY0397T81P (engineering drawing trace)

**Important:** This is a drawing-based flat silhouette, not a proprietary vendor FPC DXF and **not a solution for connecting a folded flex to Hirose J3**.

Owner supplied manufacturer `GDEY0397T81P.pdf`, Good Display rev.1.0, **p5 mechanical drawing (front/rear)**. PDF explicitly dimensions panel 96.62×56.24mm landscape; 33.66±0.30mm maximum outward FPC extension; 12.50±0.10mm contact tongue width. Real FPC **steps in width and lateral position**, with a separate neck and fold alignment mark on rear view. Previous R26 rectangular 12.50×33.66mm model was only an oversimplified envelope; do not use for mechanical decisions.

## R27 work

- An independent placement-only KiCad study copy `enku-mainboard-r0.4-stepped-fpc-trial.kicad_pcb` retains 122 actual footprints from R26 and includes a 15-vertex **gr_poly** on `Dwgs.User` representing the full flat stepped FPC silhouette.
- The polygon was **digitized manually from the owner's manufacturer page-5 raster**, transformed from the page's landscape front view into the ENKU portrait convention with the flex exiting TOP, and anchored to the exact manufacturer nominal 33.66mm and 12.50mm dimensions. Midpoint vertices are approximated by raster reading (NOT manufacturer production tolerances).
- J3 (69.37,34), H2 (57.5,25), C28 (55.2,34) remain *R26 provisional* experimental placements. No copper and no current-modified connector pad/footprint. Original R25 and R26 boards kept for comparisons.
- The page-5 real FPC features include a fold line, an exposed contact side, a contact stiffener, patterned copper/adhesive patches, and its differing front/rear appearances. **Flat silhouette cannot determine in-world connector XY or angle after folding.**
- An external local CAD preview [ENKU_R27_Stepped_FPC_Trial.zip] was built with an editable STEP assembly and 2D comparison. It is NOT auto-synced to GitHub and must not be treated as a production 3D model.
- `check_r27_stepped_fpc_flat.py` checks the real stepped shape type, 15 vertices, panel datums, no copper and unchanged provisional connector positions.

## Next engineering gate

1. Ask Good Display for **GDEY0397T81P FPC-7750 original DXF/DWG (FRONT/REAR)** and a document showing recommended fold direction/position, minimum bending radius, permitted adhesive zone and FPC stiffener thickness, metal pad contact-side reference and physical pin-1 marker. A photo of the panel flex laid out flat, including a ruler, will also help, but is less authoritative than CAD.
2. Obtain Hirose `FH34SRJ-24S-0.5SH(50)` **original 2D PDF and 3D STEP**, plus FPC mating spec (0.3mm nominal stiffener); check actuator opening/assembly.
3. Verify J3 pad1 vs panel contact1 after actual top-exit fold. Check pin5 VDHR/VSH2 discrepancy and pin15 VDDIO vs pin16 VCI network, comparing Good Display pp6/19.
4. Resolve right/top M2 H2 structural boss vs connector access in actual shell and FPC 3D. Do not bend through glass, clamp adhesive or force contact tongue.
5. Only approve actual J3 and H2 final positions after mechanically modeled stress-free folded FPC, pad-net matching, and PCBWay assembly approval. Restore routing only then.

All PCBWay fabrication, manufacturer-contact claims and Native DRC readiness remain **BLOCKED**.
