# ENKU Base R30 — J7/J6 service-contact DFM pass

**Status: NOT fabrication ready; PCBWay engineering estimate remains 30%.**

Branch: engineering/r30-service-dfm. Native PCB: hardware/mainboard/kicad/enku-mainboard-r0.7-base-dfm-prep.kicad_pcb. R29 historical source is preserved.

## KiCad PCB corrections

- J7 Tag-Connect TC2030-IDC-NL on **B.Cu**: replaced six Ø0.5mm plated-through signal holes with six Ø0.7874mm no-paste exposed SMT contacts plus **three Ø0.9906mm NPTH** registration holes. Alternating pad numbering matches manufacturer top-view drawing nominal coordinates. Excluded J7 from BOM/PnP.
- SW2 BOOT on front moved from (35.5, 87) to (35.5, 79). Nominal front button courtyard ends y82, rear J7 courtyard begins y85; drilled guide-hole clearance still needs Native KiCad DRC and physical fixture test.
- J6 four exposed backside dock pads at (47,99) changed from B.Cu+B.Paste+B.Mask to **B.Cu+B.Mask** only; no solder stencil or assembled part for passive mating contacts. J6 excluded from BOM/PnP.
- Base hardware boundary remains no Hall, no Qi, no frontlight. 120 footprints, *zero tracks and zones* on R30 study. Do not reuse legacy R0.1 copper.

## Verification still required

1. Physical Tag-Connect cable pin-1 on **back** viewed through actual programming jig; confirm mirror, orientation and service voltage before attaching to ESP32. This is source pad geometry, **not yet a proven physical pin mapping**.
2. Native KiCad 8 DRC across all four layers for J7 NPTH-to-front-copper and pad/silk/courtyard, + schematic parity. Save raw DRC diagnostics.
3. Real battery cavity, rear programmer access, SW2 BOOT actuation and serviceability. J7 cannot be blocked by LiPo or case ribs.
4. J6 PCB finish and mating spring: approved ENIG/other wear-resistant contact plating, spring force, orientation, board-to-dock z stack, no B.Paste, safe VBUS_DOCK, transient/short protection.
5. Real FPC-7750 3D fold and J3 contact face/pin1; J2 card ejection, J1/LiPo, SW1 and four side buttons, antenna, U1 53 vs library 62 pads; EPD HV sequencing and pin5 ambiguity.
6. Complete 252 unrouted connections, PCBWay sourcing BOM/placements, correct Excellon NPTH and fabrication drawings; no manufacturing request until all are approved.

CI structural check: hardware/mainboard/kicad/check_r30_service_pads.py. Its --release flag intentionally blocks production even when source geometry passes.