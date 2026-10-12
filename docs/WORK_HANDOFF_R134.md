# ENKU R134 working checkpoint — ROUTING IN PROGRESS, NO FAB

Branch `engineering/r134-usb-control-connector`. Parent is the retained R133 proof commit e75cdfb1dbf0a93eea7c7f7bcd14358690eec426. Open the canonical enku-mainboard-r0.1 project.

## Published source versus last local experiment

The canonical PCB published at 08fb52fcf02e0591e1ce58ecf97408248a35a637 is the earlier working checkpoint: actual KiCad10.0.7 ERC0, parity0,16 unchanged SW3–SW6 hole errors,1 isolated EN2 via and10 open connections. It is not a completed R134 native or independent-audit pass.

After that publication, local routing experiments reached **zero opens and zero schematic-parity discrepancies** in actual KiCad10.0.7 with all track errors, refill and save enabled. That local experimental board still had **37 track-width errors,16 original button-hole errors,2 dangling vias and1 dangling track**. The37 new short digital segments were0.15mm while the unchanged project minimum is0.20mm. Their width must be corrected and clearance revalidated. The obsolete VBUS stub and unnecessary VBUS/CHG_STAT2 vias must be pruned with connectivity checks.

The workspace disconnected before these corrections or publication of the latest PCB. It explicitly returned409 Conflict, environment_offline, “Environment is not connected.” **The locally routed PCB and its full reports are not included in this Git commit.** The zero-open observation must not be attributed to the currently published canonical PCB. No new R134 server CI proof exists. Recovery operations and exact known local edits are recorded in `hardware/mainboard/kicad/checks/routing_recovery_R134.json`; this is a recovery specification, not proof of a completed board.

## Implemented published engineering changes

GCT USB4105 is replaced by **USB4215-03-A**, using RevA26Apr2024 drawing,3.16mm profile and no locator pegs. The mating face at boardY121mm is retained. Four plated shell slots and16 logical contacts remain; two old NPTH pegs are removed by a real component replacement. Drawing dimensions and contact rows were checked, including the0.680mm copper-row shift toward the board edge. TME offered the part when checked; LCSC listing was out of stock. Factory acceptance of0.8mm shell stakes in a1.6mm PCB, full enclosure fit and USB impedance remain open. No PCB/case thickness increase.

BQ24072T symbol now correctly identifies **EN2=pin5 and VSS=pin8**. Both were formerly GND, so the old name swap did not alter its previous static behavior. GPIO16/modulepad9 drives EN1, GPIO2/modulepad38 drives EN2, GPIO38/modulepad31 drives CE through three1k resistors. Two2.2k mode pull-downs give USB100 in the high-Z reset/OFF model. USB500 and suspend become selectable. OFF charging is slower, limited by USB100.

The resistor logic-voltage calculations are conditional models: Espressif's published VOH/VOL table is specified at3.3V,25°C with a high-impedance measurement load. It does not itself guarantee loaded control voltages over the entire operating range. Boot ROM/pull states, brownout, GPIO holds, dead-battery startup, suspend, inrush and full-cycle charging require verification. No automatic BC1.2 or USB-PD detection has been added.

## Next concrete engineering operations

1. Recover the local directory if retained; otherwise reproduce from08fb52f using the existing native helpers and the recovery specification. Preserve the published source before experimenting.
2. Use at least0.20mm for every new digital segment. Correct the37 narrow segments and reroute clearance failures; never lower the existing minimum-width or clearance rule.
3. Remove the three obsolete dangling branches, checking native and independent pad connectivity after pruning.
4. Export ERC/netlist, actual assembly/CPL/mask/paste, via requests, USB reference planes and thermal planes. Complete and run the two new connector/control audits plus all retained independent scopes and exact preservation checks.
5. Publish the actual completed source/checkpoint, run GitHub native KiCad and verify that run's actual artifacts against the same source. Keep fabrication_ready=false until the outstanding mechanical, thermal, battery, NTC and manufacturing holds are resolved.

Preserve R133's five requested filled/capped U3 thermal vias,1.6mm stack,59×101mm outline, USB long-pair geometry, RF keepouts, original rules and all earlier evidence. Additional local changes deliberately open the charger routing corridors; they must have finite UUID-based before/after declarations. Earlier R133 thermal qualification and detached-NTC holds remain open. No production, purchases or supplier email have been sent.

Recorded 2026-10-12T07:19:21.354Z.
