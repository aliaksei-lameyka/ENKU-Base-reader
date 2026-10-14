# ENKU Base Reader current status

Updated 14 October 2026. **Working PCB R141 / branch `engineering/r141-routing-power-fixes` / NO FAB.** [Open current KiCad](../hardware/mainboard/r141/kicad/enku-mainboard-r0.1.kicad_pro). PCB SHA256: `b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe`.

| Area | Evidence | State |
| --- | --- | --- |
| Actual R141 source | Native KiCad 10.0.7 DRC/ERC/opens/parity zero, 20 actual-source guards, 438 pads / 127 references retained | PASS locally |
| Historical R138 control | 27 scopes and 20 effective rejection cases | PASS locally |
| Current exports | Four complete copper images, 11 Gerbers, 371 drill objects, 770 IPC records and 107 fitted top BOM/CPL units | PASS independent local parsing |
| Routing | Charger and EPD paths shortened, R19 body clearance, control/SPI reference work, 30 fast paths and 14 nets assessed | Geometry checked; SI/PI review required |
| Layer visibility | No unnamed layers, unassigned tracks/vias/copper zones or copper graphics without net semantics. 45 disabled legacy drawing objects; 79 references and 120 values hidden | Documented; legacy drawing cleanup pending |
| PCBWay package | Current R141 exports, source, three PDFs, CSV/Excel, six via requests and test requirements | Preliminary review; not submitted |
| Factory process | 346 vias, including 82 nominal 0.2mm bores; six fill/cap sites, U1 EP, USB stakes, stack and stencil | Job-specific acceptance HOLD |
| Product/mechanical | Current case, panel/FPC, thin protected CN/PL packs and separate NTC retention | Unqualified / HOLD |
| Firmware/FCT | Startup, USB-MSC/microSD ownership, PSRAM, recovery, image set, fixture and numeric criteria | NOT RUN / HOLD |
| Physical/consumer qualification | Power, charging, faults, loads, thermal and repeated cycles | NOT RUN |

[Handoff](R141_ENGINEERING_HANDOFF_NO_FAB.md), [package record](evidence/R141/final/PCBWAY_PACKET_R141.json), [PCBWay instructions](PCBWAY_MANUFACTURING_NOTES_R141.md), [next methods](PRE_REVIEW_CHECKS_R141.md). Actual server CI is recorded separately. A local PASS does not claim that a server run has completed.

R138 source, R139 qualification requirements, R140 routing findings and accepted historical server proof remain under their recorded revisions. No factory upload, order, purchase or supplier message has been made.
