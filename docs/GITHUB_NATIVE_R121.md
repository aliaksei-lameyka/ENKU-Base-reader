# R121 actual server evidence — NO FAB

Source commit: `60e67081482be1e4cbcbfea87c874a7a3933cf55`. [Run 38085655045](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38085655045), job `114311477749`, conclusion **success**. [Artifact 11681717419](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38085655045/artifacts/11681717419).

SHA-pinned official KiCad 10.0.7 performed full native DRC with actual refill, ERC and netlist. All 402 pads, 117 footprint placements and every track/via geometry matched the committed local checkpoint. Actual results: 0 opens, ERC 0, parity 0, 111 library mismatches and 4 inherited hole-clearance findings. No dangling copper. The independent USB audit also ran on the server's own refilled GND polygons: zero uncovered trace/reference regions and zero missing area in the 1 mm core reference strip.

Source PCB SHA-256: `8cdf268088804783025f1b2c30bced9006c847b6ac5e597bf6925b483b7d2efa`. The retained `server_comparison_R121.json` and `server_USB_audit_R121.json` were extracted from the actual job logs. They are not the local integration-test results.

This proves source consistency and the stated checks. It does not prove correct manufacturer pin geometry, component selection, stackup impedance or functioning assembled hardware. The read-only footprint triage subsequently identified the Q1 Gate/Source pad-location defect; manufacturing remains blocked.
