# ENKU Base mainboard

Current engineering revision: R133, branch `engineering/r133-thermal-process`; **NO FAB**. Open `kicad/enku-mainboard-r0.1.kicad_pro`. [Current handoff](../../docs/WORK_HANDOFF_R133.md), [temperature and charge FMEA](../../docs/TEMPERATURE_AND_CHARGE_R133.md), [DFM draft](../../docs/DFM_REVIEW_R133.md), [thin batteries](../../docs/BATTERY_SUPPLY_R132.md).

Actual KiCad 10.0.7 verifies 0 opens / ERC 0 / parity 0 and 20 unchanged intrinsic hole errors. All 19 independent guards and checkpoint comparison pass. Five native fill/cap requests, local charger copper and one measured B.Cu GND zone are added. All schematic/footprint/placement/assembly fields and original rules remain preserved. Actual R133 server proof is pending publication.

Case thickness is unchanged. Approved CN/PL replaceable packs, full enclosure fit, actual temperature/thermal/full-cycle charge, fill/cap fabrication acceptance, USB current-mode hardware control, effective capacitors, display and process/bench gates remain open. The 22.812 mm² continuous thermal region does not meet the proposed 50 mm² objective. Dedicated Base scope; Pro remains separate. Production or component ordering requires user agreement.
