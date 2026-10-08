# ENKU Reader enclosure R04 — 2026-10-08

Parametric SCAD and two STL parts were generated in the conversation working directory. R04 includes: asymmetric module margins (3.2 mm top, 9.18 mm bottom), 62x109 mm outline, two lower rear-access M2 screw positions, preliminary upper hook geometry, four side-key openings, PCB guide pads and USB-C bottom opening.

OpenSCAD CGAL export succeeded for both halves, but this is **not a validated manufacturable enclosure**. In particular, 1) PCB guide pads are not PCB fasteners; 2) no battery/ESP32 clearance solution; 3) hook engagement and removal untested; 4) connector/side-switch footprints and heights are provisional; 5) display FPC bend and rear-cover fit are unverified; 6) heat-set insert bores are placeholders. Existing KiCad H1-H4 still collide in projection with display and have not been moved.

Design next: component-accurate XY/Z height-map and PCB retention redesign, then print fit-check coupons and inspect assembly interference before manufacturing.
