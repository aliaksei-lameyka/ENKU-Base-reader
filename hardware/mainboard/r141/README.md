# R141 working mainboard

Open [kicad/enku-mainboard-r0.1.kicad_pro](kicad/enku-mainboard-r0.1.kicad_pro) with KiCad 10.0.7. The root and four child schematic sheets, project-local libraries and rules accompany the PCB. Working revision R141, NO FAB. Exact PCB SHA256: `b656abcf65c55cdb425a09468ef379187b561e764ad1257d2b2761e4f95451fe`.

[Current status](../../../docs/CURRENT_STATUS.md), [handoff](../../../docs/R141_ENGINEERING_HANDOFF_NO_FAB.md), [PCBWay packet](pcbway/README_PCBWAY_R141_NO_FAB.md), [pre-review methods](../../../docs/PRE_REVIEW_CHECKS_R141.md).

The historical canonical R138 folder and acceptance guards remain unchanged. R141 editable files are exact copies of the completely verified actual candidate. The legacy r0.1 basename preserves project and sheet references.

**Layer audit:** all four copper layers have names and are included in the verified exports. The disabled `User.Drawings` layer retains 45 historical objects, including obsolete placement and charger notes. They are excluded from fabrication and must not be read as current instructions. 79 references and 120 values are hidden in the native source. Complete reference and pad maps are supplied. Cleanup of the historical drawing layer is a next-pass item.
