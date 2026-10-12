# ENKU Reader R0.1 — PCB-first mechanical policy (R11)

Decision: **the preliminary R08 Fusion housing is NOT a placement constraint for PCB components.** It is a reference for overall external envelope and enclosure closure principle only.

## Frozen
- Target enclosure approximately 62 x 109 x 10 mm, 3.97-inch GDEY0397T81P in portrait; maintain narrow side bezels.
- Four physical side navigation buttons, two left and two right, with ergonomic positioning and left/right remapping in firmware. Their exact production footprint and actuator orientation must be verified before final PCB placement.
- Serviceable enclosure: two upper mechanical engagements plus two lower M2 closure screws. The upper engagement geometry itself is not frozen.

## Free to move
- microSD socket and card slot location; hard power switch and access cutout; USB-C; LiPo connector; battery pocket; PCB mounting holes; internal ribs and bosses; other electronics as needed for electrical routing, signal integrity, manufacturability and serviceability.
- Do not constrain any component to a hole/cutout in the R08 model. Re-cut enclosure only after final PCB positions are validated.

## Execution order
1. Validate actual chosen parts/footprints for side switches, EPD FPC and battery power path. Preserve the frozen button ergonomics.
2. Route/fix electrical design in large coordinated passes. Run native KiCad ERC/DRC and inspect all error classes; no unsupported claims of clean DRC.
3. Verify PCB outline fits the nominal enclosure and the display/FPC service envelopes; place mount points only after component/routing feasibility is known.
4. Reconcile board with battery volume and enclosure stack height (including tolerances and battery swelling).
5. Rebuild production housing apertures and screw/hook geometry around the validated PCB. R08 STEP is an editable reference, not a manufacturing master.

## Explicit non-goals
- No PCB reroute solely to match the R08 microSD or switch cutouts.
- No claim that current PCB holes are final.
- No manufacturing Gerbers before electrical DRC and mechanical assembly verification.
