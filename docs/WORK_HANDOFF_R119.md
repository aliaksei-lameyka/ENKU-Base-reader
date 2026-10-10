# ENKU Base R119 — recovered layout checkpoint

Canonical project: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`.
Canonical board: `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pcb`.
Use **KiCad 10.0.7**. The R50 workflows used KiCad 8, which is unsuitable for the current KiCad 10 file format.

This checkpoint preserves the reconstructed layout before the next large routing pass. It is **not fabrication-ready** and does not claim routing completion.

## Native evidence

Full-board DRC used `--all-track-errors --schematic-parity --refill-zones --save-board`.

| Result | R118 saved source | R119 recovered checkpoint |
| --- | ---: | ---: |
| Unconnected items | 15 | 67 |
| Library footprint mismatches | 111 | 111 |
| USB-C hole-clearance violations | 4 | 4 |
| RF keepout violations | 37 | 0 |
| Dangling tracks / vias | 0 / 0 | 25 / 28 |
| Schematic parity | 0 | 0 |
| ERC violations | 0 | 0 |

The additional opens are the explicit cost of moving buttons, battery ADC parts, USB series resistors/ESD and rebuilding J3 escapes. They must be closed before claiming progress in routing closure. The immutable R118 source is retained in `hardware/mainboard/revisions/R118/ENKU_R118_source_checkpoint.zip`.

Independent comparison preserves all 400 pad UUIDs, numbers, nets, sizes, drills and layers; all surviving copper net names; the complete schematic bytes; project rules and inherited DRC exclusions. Exact board hashes and native JSON reports are in `hardware/mainboard/kicad/checks/`.

## Reconstructed changes

- Keep the 59 × 101 mm envelope and open an edge notch beneath the ESP32 antenna; remove obsolete copper from the original RF conflicts.
- Move four reading switches to Y=73/85 mm and orient their actuators toward the outside edge. Move H1 to (29, 22.5) mm.
- Relocate U9/C37/R39 and the I²C pull-ups away from the switch contacts; restore local connections next. U9 is TMUX1101, with the existing D/S/SEL/VDD net assignment preserved.
- Correct the physical mirrored contact rows of bottom-side J7. Preserve logical UART/BOOT/EN pin numbering and the three guide holes. Restore its bottom-side keepout; the bundled source is explicitly patched to prohibit tracks inside the contact rectangle.
- Rebuild active J3 escapes with alternating Y=31.6/33.85 mm through vias. VCI/VDD trial escapes were rejected by native clearance checks and are absent from the accepted batch.
- Move C28 beside J3 pin5 and TP10 beside Q1. Good Display's later response identifies VDHR/VSH2 as the same pin5 signal; exact Hirose-versus-supplied-connector orientation still needs qualification.
- Place R64/R65 beside ESP32 USB pins and U8 near J5. Add the short MCU-to-resistor and flow-through ESD connections. The long USB pair and both connector orientations remain unrouted. `usb_pair.py` is an unaccepted proposer: it currently reports no continuous B.Cu corridor and has not added copper.

## Next electrical pass

1. Close moved-part power/ground and control nets, then finish all J3 connections.
2. Route USB as a coupled pair with explicit transition grounding and a continuous reference plane; qualify its width/spacing against the selected production stackup.
3. Remove obsolete dangling copper without increasing the number of opens. Audit plated-hole overlap with SMT pads and the Tag-Connect 0.508 mm foreign-signal spacing independently of the global DRC minimum.
4. Re-run full native DRC/ERC and compare every actual pad/copper net after zone refill. A CLI exit code of zero is not routing or fabrication signoff.
5. Resolve the four existing USB-C hole-clearance violations and qualify the real land patterns behind the 111 library mismatches.

The user is editing the enclosure. The display tail orientation, physical FPC fold and active-area window offset must be checked in that assembly; the old centered window/FPC pocket is not a qualified fit for the relocated electrical layout.

Base excludes Hall, Qi, frontlight and Pogo/Dock. USB access to microSD through ESP32 native MSC remains required; hardware continuity alone does not establish working firmware or bench qualification.
