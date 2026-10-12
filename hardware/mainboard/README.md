# ENKU Base mainboard

Current R134 engineering branch: `engineering/r134-usb-control-connector`; **NO FAB**. Open [`enku-mainboard-r0.1.kicad_pro`](kicad/enku-mainboard-r0.1.kicad_pro). Board59×101×1.6 mm and case-thickness target are unchanged.

Actual immutable-source KiCad10.0.7 [run38240134929](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38240134929): ERC0,opens0,parity0,16 active SW3–SW6 hole-clearance errors;21 independent scopes plus checkpoint comparison passed. Actual artifact digest/CRC and 22 report/export comparisons are verified and retained; [current handoff](../../docs/WORK_HANDOFF_R134.md).

J5 is GCT USB4215-03-A; GPIO16/2/38 control BQ24072T EN1/EN2/CE. Reset/OFF high-Z model is USB100. Actual USB reference continuity and approximately55.33 mm² connected B-side charger GND-spreading geometry are verified. Neither native success nor copper area is manufacturing/thermal acceptance.

See [fabrication gates](../../docs/DFM_REVIEW_R134.md), [current power contract](../../docs/USB_POWER_CONTROL_R134.md) and [battery/supplier status](../../docs/BATTERY_STATUS_R134.md). Thin2000–2500 mAh two-wire PCM pack with independent NTC, fixed-case fit, CN/PL replacements, button/process decisions and firmware/bench qualification remain open. Previous engineering sources and evidence are preserved. No production/order activity.
