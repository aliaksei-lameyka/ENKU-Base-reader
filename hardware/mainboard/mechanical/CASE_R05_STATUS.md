# ENKU Reader R05 — joint stack visualization

Date: 2026-10-08. Local generated deliverables: `enku_reader_case_r05.scad`, `enku_front_r05.stl`, `enku_rear_r05.stl` (conversation attachments, not committed CAD source).

- Two printable **watertight STL meshes** exported by OpenSCAD. This is a topology check only, not an assembly clearance or fit approval.
- The OpenSCAD model supports `part="front"`, `"rear"`, `"stack"`, `"section"`, `"assembly"`.
- Preview places display module 56.24 × 96.62, existing PCB 59 × 94, illustrative 40 × 60 × 3.8 LiPo and approximate ESP32 envelope in the same XY/Z frame. Red boss markers show current H1–H4 interference with display projection; red ESP32 volume indicates battery collision.
- **Do not print as a functional assembly yet:** upper lugs are registration placeholders, not load-rated serviceable hooks; PCB guide pads do not hold PCB; side-button openings do not yet have printed keys; battery pack and component heights are approximate; M2 insert and FPC geometry unverified.
- Preserve asymmetric front bezel and two rear-access lower M2 screws; no screw or boss may contact the glass or FPC.

Next: validate exact component height map and real LiPo dimensions, decide safe PCB retention, redesign PCB placements and H1–H4 as one coordinated change, then finalize hook mechanics and button caps.
