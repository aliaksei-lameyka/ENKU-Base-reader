# ENKU Base R31 PCBWay readiness (2026-10-08)

**30/100 = unchanged preliminary engineering maturity**, NOT ready to order.

R30 baseline evidence: 120 components, 0 schematic parity errors, 0 critical copper edge/shorting violations; 240 other Native KiCad DRC violations (119 footprint mismatches, 1 library issue, 68 silk_over_copper, 36 silk_overlap, 16 text_height) and **252 unrouted**. R30 native run [37790938942](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37790938942).

R31 changes: placement correction for D2/D3, D1/C24, C5/C6 overlapping SMT pads; new vendor-aware MBR0530 cathode F.SilkS marking; automated all-SMD-pad assembly overlap audit; GCT USB-C 16-contact pin/net-order guard.

**Next validation:** R31 Native ERC+DRC, schematic parity, full physical package/3D clearance (not only copper), re-assess all DRC classes; verify charger hard-off semantics and real switch/battery connector MPN before rooting all 252 signals. No Gerber generation.

Stage score remains as R29: requirements 9/10; schematic 11/20; mechanical 5/20; manufacturer-qualified footprint 3/15; placement+routing 2/25; manufacturing 0/10.
