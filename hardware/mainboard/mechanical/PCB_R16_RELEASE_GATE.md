# ENKU Reader — R16 board-outline and GND connection trial

**Status: engineering experiment / NOT for manufacturing** (2026-10-08).

## Changes
- PCB trial outline changed from 59 × 94 to **59 × 101 mm** by extending the lower Edge.Cuts boundary from y=114 to y=121 mm. Width remains 59 mm. No footprints or mechanical holes were silently moved.
- Added candidate R6 pad-2 (GND) escape: F.Cu from (73,82) to (74.5,82), with 0.6/0.3-mm GND via at (74.5,82). This routes **right** of R6, avoiding its MUX_OV1 pad on the left. Must be checked against KiCad refilled B.Cu zones and net-60 track near x=73.3.
- Corrected stale 54×94 placement baseline and adjusted outline migrator to recognize an already migrated board.

## Measured invariants
- Board: x=18…77, y=20…121 mm. Fastener and critical footprint coordinates deliberately unchanged.
- 4 side switches: 2 left + 2 right. They are **placement-only placeholders**, NOT approved side-actuated footprints.
- Display (portrait module nominal): 56.24 × 96.62 mm. PCB exceeds display length by just 4.38 mm total; no verified M2 boss land at both ends.
- Battery pocket, FPC insertion/bend, USB-C and microSD access, screw bosses, case wall thickness, finger-button travel all remain open.

## Manufacture-blocking gates
1. Native ERC and DRC rerun on refilled KiCad board; report shorts, copper clearance, hole clearance, routing closure and schematic parity. A structural checker passing alone does not mean PCB is ready.
2. Replace SW1 and SW3–SW6 placeholders with selected supplier footprints (and verifiable 3D orientation).
3. Reconcile actual GDEY0397T81P module and FPC tail with PCB, button bodies, battery and fastener axes in parametric CAD.
4. Rework routing and mechanical holes as a *coordinated pass*, not by moving circles outside glass in an unregistered 2D sketch.
5. Verify Gerber/drill/BOM/CPL and PCBWay DFM **only after** 1–4 pass.

## Pre-change native KiCad snapshot (commit 9022b570)
- Native DRC reported **664 violations** (including 127 clearance, 72 hole clearance, 57 tracks crossing, 40 shorting items), plus 4 unconnected reports (3 self-zone artifacts and 1 R6 GND pad-to-track gap).
- The figures are historical and must not be presented as post-change CI results. **The board is not production-ready.**
