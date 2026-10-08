# ENKU Reader R0.1 — four shared rear-access M2 fasteners (candidate)

**Status: mechanical feasibility candidate, NOT released to manufacturing.** PCB file remains at 59 × 94 mm with original H1–H4; this document and `enku_fastener_envelope.scad` define the proposed redesign, not an implemented KiCad layout.

## Fixed references (KiCad XY, mm)

- Existing PCB Edge.Cuts: x=18..77, y=20..114 (59 × 94).
- Good Display GDEY0397T81P portrait external outline: 56.24 × 96.62; centered at (47.5,67) gives x=19.38..75.62, y=18.69..115.31.
- Existing mounting holes H1 (30,23), H2 (71,23), H3 (23,111), H4 (71,111); M2 nominal drill 2.2 mm. Existing locations overlap display plan view.

## Proposed packaging envelope

- Extend PCB to x=18..77, y=12..122 (59 × 110), while keeping its center (47.5,67) and display position unchanged.
- Proposed mounting centers: H1 (30,15), H2 (71,15), H3 (30,119), H4 (71,119). The H3 x change is intentional to align paired bosses, but must be validated against microSD and USB-C keepouts.
- With 5.0 mm **illustrative** boss outside diameter, top boss spans y=12.5..17.5, display begins at y=18.69; bottom boss spans y=116.5..121.5, display ends at y=115.31. Plan-view clearance = 1.19 mm each end. Boss-to-PCB outer edge = 0.5 mm, **likely insufficient** for printed mechanical robustness: boss must be supported by the shell, not treated as a 0.5-mm PCB web. PCB drill edge distance is 1.9 mm (3.0 - 1.1), to be checked against fabrication requirements.
- This is only a 2D envelope: verify display FPC exit, cable bend, upper switch, microSD, USB-C, battery, shell ribs, screwdriver reach, antenna keepout and screw stack Z before approving.
- Rear screws pass through rear cover clearance holes, through H1–H4 in PCB (without transferring clamp load to fragile areas), and engage heat-set inserts in front shell bosses. Front shell is structural; display mounted separately with serviceable electronics tape. Prefer compression sleeves or rigid hard-stops so PCB does not carry enclosure screw preload.
- Side-actuated SW3–SW6 must register their native plungers at the PCB edge, with only the plunger flush or protruding; do not obstruct with bosses.

## Blocking checks before changing KiCad

1. Choose real M2 heat-set insert and printed material; size boss OD, insert depth and wall thickness from datasheet and printed coupons.
2. Place real display model including FPC/tail and tolerances. Verify that four bosses are entirely outside the display envelope and accessible from rear.
3. Repack U1/ESP32 antenna, SW1, J3 FPC, J2 microSD, J5 USB-C and J1 battery in new outline; validate side switch actuation.
4. Apply coordinated KiCad outline + mounting holes + component relocation + rerouting, refill zones, run ERC/DRC and inspect 3D model.
5. Validate enclosure outer dimensions and thickness against pocket-reader ergonomics; 110-mm PCB length is a candidate, not an approved product dimension.

## Approved direction 2026-10-08 — asymmetric bezels, two screws and upper hooks

**This supersedes the earlier four through-PCB enclosure-screw proposal.** The 59x110 mm four-screw CAD study remains an unapproved comparison, not the final board outline.

- Narrow top bezel; modestly deeper lower chin; narrow side bezels. Do not assume symmetrical end margins.
- Enclosure closure: two rear-access M2 screws in the lower structural region plus two robust serviceable hooks at the upper end. No glue joining the two shell halves.
- Four existing PCB holes H1–H4 are for independent board-to-chassis support, subject to relocation and display/FPC/port clearance; they are not automatically the two shell screw holes.
- Front shell is load-bearing; display is independently held by serviceable electronics adhesive strips. Rear cover removal must not require lifting the display.
- All screws, inserts, bosses, hooks and PCB supports must avoid the entire display outline including glass and flex tail. No point loading of display.
- Side-actuated switch plungers must remain flush with or slightly beyond PCB edge; upper hooks and lower screw bosses must not block them.
- Before KiCad hole changes: validate actual display/FPC geometry, upper-hook disassembly motion, lower insert dimensions, USB-C and microSD access, PCB retention and Z-stack in CAD. Final housing size not yet frozen.
