# Native KiCad comparison for R119

The R50 native workflow used `kicad/kicad:8.0`, while the current canonical source uses KiCad 10's `20260206` file format. Running the old workflow cannot validate R119 correctly.

The new workflow uses the same official **KiCad 10.0.7 Lite AppImage** as the local check. The downloaded archive is pinned by its SHA-256, not by a mutable Docker `10.0` tag. At setup time Docker Hub had no `kicad/kicad:10.0.7` tag; `10.0` referenced an image last updated before the 10.0.7 release.

It checks the committed PCB hash, refills zones, runs full-board DRC with every track error and schematic parity, runs ERC, exports the native netlist/geometry and compares every actual pad/copper object against the saved local checkpoint. The five inherited DRC exclusions are compared exactly and are not expanded.

The workflow separately reports **server/local comparison MATCH** and **fabrication NO FAB**. A matching diagnostic result does not remove or waive the 67 opens, 111 library mismatches, four USB-C hole-clearance violations or 53 dangling copper objects in this checkpoint.

Only the workflow-definition commit automatically starts the initial comparison on `engineering/r119-recovery-checkpoint`. Later PCB edits do not spend Actions minutes automatically. Additional complete checks can be started explicitly. The two obsolete R48/R50 structural/zone-fill workflows are retired on this working branch; they remain available in its parent history.

Primary runtime source: https://www.kicad.org/download/linux/

Official container documentation: https://www.kicad.org/download/docker/
