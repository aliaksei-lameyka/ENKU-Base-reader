# R141 working candidate — verified locally, NO FAB

The current working board is **R141** inside `docs/evidence/R141/final/R141_actual_candidate_NO_FAB.zip`, directory `editable/`. The unchanged older PCB under `hardware/mainboard/kicad/` is the retained R138 comparison reference for inherited guards; use the archive to resume R141.

Actual candidate PCB SHA256: `b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe`.
Native KiCad10.0.7: DRC0, ERC0, opens0, parity0.20 inherited actual-source guards, all438 pad definitions and127 references, exact USB copper, four complete independent copper images and all11 layers/drills/IPC/mask/paste/BOM/CPL passed. All14 fast nets have0mm missing both-inner-GND centreline; short common MCU exits retain the documented farther reference. Fresh reference controls:27 scopes and20 effective negative cases PASS.

The final package contains the editable project, libraries, current evidence,11 native review plots, retained reference and per-file SHA256 manifest. Current recovery session lower bound 0.744 hours; logged project lower bound 22.998 hours. Overnight/offline pauses excluded.

Archive SHA256: `5ad6eb182f4100e0fd9108fcc32fc77ef45479619c45179f8c2bfa3a4059ac79`; 43062767 bytes; 2356 files. Read `docs/R141_ENGINEERING_HANDOFF_NO_FAB.md` for paths and remaining qualifications.

Physical startup/charging/NTC/load/thermal/EPD/SD/USB-MSC/firmware/FCT, actual case/pack/panel fit, factory stackup/USB impedance and via process acceptance remain NOT RUN or unapproved. Fabrication and purchasing remain unauthorized. Public publication and the new server CI run are pending explicit approval; local checks are not presented as server proof.

## Published package and layer visibility update

Current editable R141 project is also retained at hardware/mainboard/r141/kicad/. PCB SHA256 remains unchanged. The complete recovery ZIP is stored as six ordered Git parts with per-part and combined hashes in recovery-archive-parts.json. A preliminary PCBWay packet, three visually checked PDFs, native/mapped CSV and Excel BOM/CPL and the next-methods checklist accompany the branch.

The layer audit found no unnamed layers or unassigned routed copper. Disabled User.Drawings retains45 historical documentation objects including obsolete charger/placement notes.79 references and120 values are hidden; all are preserved in the supplied maps. Historical drawing cleanup remains a pre-submission item.

Actual server run38532688718 passed for source18afbe4405a26e497eb6f0cd77975fb15f035027. Artifact11878791435 has154 CRC-checked members and API digest e5f27ed916ed9a24ee0556a75d34058a146d8ea67816e2658d72b135afebe9df. All24 native manufacturing files and the verification summary match the local result after explicit export timestamps only are normalized. The mapped U1 mounting type is SMT, while J5 is Hybrid. PCB/native fabrication files unchanged. See docs/GITHUB_R141.json.
