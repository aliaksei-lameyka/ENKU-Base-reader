# ENKU Base — R35 PCBWay readiness

**Target estimate 30/100. Fabrication BLOCKED.**

R35 is a real electrical architecture revision: 125 physical footprints (R34 123), local AO3401A high-side 4A P-MOS Q2 and 100k pullup R40. Physical SW1 now operates only low-current `PWR_GATE→GND`, not 60mm power-to-top excursion. Protected LiPo/BQ25185 remain always connected and can charge in OFF. R34 gated BAT_ADC retained.

Native R35 [verified KiCad run 37802371422](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37802371422): **ERC 0 errors/0 warnings**, **schematic parity 0**, **0 critical shorts/mask bridges/edge faults**, **236 DRC non-unrouted violations** (123 footprint-library differences plus remaining silk/text diagnostics), **267 unrouted**, **0 footprint_errors**. 125 footprints; 0 tracks/vias/zones. R34 verified [run 37800130221](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37800130221) was ERC0, PCB/schematic parity0, 233 non-unrouted DRC, 263 unrouted. R35 numbers supersede R34 for this branch.

FPC Good Display pin5 VDHR/VSH2, 3D folded flex, exact switch MPN/placement, PMOS inrush/thermal/off currents, battery charge and NTC, exposed Dock, 4-layer routing, DRC, BOM/CPL and Gerber **remain open**. Supplier emailed; response awaited. No release until actual component and electrical signoff.

R35 introduces a **low-current SW1 gate control**, not a fully battery-isolating switch; actual slider footprint and mechanical actuation remain EVT-only. Good Display was contacted, pending pin5 and flex details. **PCBWay status 30/100 unchanged.**
