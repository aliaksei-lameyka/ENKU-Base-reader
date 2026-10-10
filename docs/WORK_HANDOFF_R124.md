# ENKU Base — R124

R124 continues the actual server-verified R123 PCB, SHA256 `89921e5219857e6602fc52ac1b8acf84821b747b06b999cf85b0794a80616644`. The approved SW1 was recovered from the user's 2026-10-09 decision: **G-Switch MK-12C03-G015**, hardware ON/OFF at the upper PCB edge with an exterior horizontal slide. R123's remaining-work summary had omitted that approval; selecting another MPN is not required.

## Changed hardware

SW1 now uses a three-terminal SPDT symbol: **2 COM → PWR_GATE**, **1 → GND**, **3 explicitly unused**. The two existing schematic wire endpoints remain in place. The native netlist and physical copper agree; pad UUIDs retain their functional nets while their pin numbers are corrected.

The reviewed footprint `ENKU:GSWITCH_MK12C03_G015_DRAWING_REVIEW` contains three signal lands, two Ø0.90 locator holes and four unnumbered bracket solder lands. SW1 is at **(40,22) mm, 180°**, near the middle of the upper edge, clear of the U1 RF keepout and the H1/H2 mounting holes. The former upper-left trial was rejected by native keepout checks and is not the committed source. Body/locator datum and switch retention still need manufacturer confirmation; nominal actuator projection is not a qualified enclosure dimension.

The PWR_GATE escape uses F.Cu and B.Cu with a new signal via. The old SW1 signal via is removed because its old F.Cu branch no longer exists. GND has a local via into the ground planes. The ground connection from R29 to the existing (45,29) junction is retained. Three obsolete copper items are removed, thirteen new items are added. All surviving copper retains its original net and geometry.

## Evidence

Native **KiCad 10.0.7**, all severities and all track errors, zone refill/save and schematic parity:

| Check | Result |
| --- | ---: |
| Unconnected items | 0 |
| ERC | 0 |
| Schematic parity | 0 |
| Library mismatch | 109 |
| Hole clearance | 20 |
| Footprints / physical pads | 117 / 417 |
| Active SW1 native findings | 0 |

PCB SHA256: **`5facf2ac0a91cbd79ec97e85fed2552e45cf46052aa66bb98a21bc5539639b5e`**.

The preservation guard verifies all **410 original pad UUIDs**, seven declared new SW1 pads, unchanged unrelated footprint poses/library IDs, surviving copper, connected pad groups, board/zone outlines, RF keepouts, rules and exclusions. It compares every schematic net node and verifies that the power schematic and symbol library contain only the declared SW1 edits. All **282 board vias** were checked against SW1 lands; minimum annulus gap is **0.300 mm**. SW1 solder copper has **0.500 mm** minimum edge clearance. The broader via/Tag-Connect guard, manufacturer button/SD guard, Q1 pin guard and USB guard pass. Actual refilled USB ground has zero missing trace-reference regions.

Active evidence selector: `hardware/mainboard/kicad/checks/current_checkpoint.json`. Local CI-format simulation only tests helper/report compatibility and does not count as an actual server run. [Actual R124 server proof](GITHUB_NATIVE_R124.md) confirms the same 417 pads, 117 footprints, copper, zones, keepouts and native counts at source commit `7878459718d8d8408eb6452ceac293cf76367637`.

## Release status

**NO FAB**. SW1 drawing revision and mechanical datum remain unresolved; [the source conflict](SW1_DRAWING_REVIEW_R124.md) is explicit in the footprint, audit reports and active verification record. The 16 button and four USB hole findings are not waived. Other MPN/land checks, display/FPC, stackup, enclosure and manufacturing freeze remain in [the work list](REMAINING_TO_BUILD_R124.md).

No default-branch merge, production release, manufacturing order or supplier message is part of this checkpoint. Base remains 59 × 101 mm with four side buttons; Pro features remain on their separate PCB.
