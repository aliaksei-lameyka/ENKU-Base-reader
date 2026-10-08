# ENKU Base — R35 PCBWay readiness

**Target estimate 30/100. Fabrication BLOCKED.**

R35 is a real electrical architecture revision: 125 physical footprints (R34 123), local AO3401A high-side 4A P-MOS Q2 and 100k pullup R40. Physical SW1 now operates only low-current `PWR_GATE→GND`, not 60mm power-to-top excursion. Protected LiPo/BQ25185 remain always connected and can charge in OFF. R34 gated BAT_ADC retained.

Native R35 verification is PENDING; R34 verified [run 37800130221](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37800130221) was ERC0, PCB/schematic parity0, 233 non-unrouted DRC, 263 unrouted. Do not reuse R34 measurements as R35 counts.

FPC Good Display pin5 VDHR/VSH2, 3D folded flex, exact switch MPN/placement, PMOS inrush/thermal/off currents, battery charge and NTC, exposed Dock, 4-layer routing, DRC, BOM/CPL and Gerber **remain open**. Supplier emailed; response awaited. No release until actual component and electrical signoff.
