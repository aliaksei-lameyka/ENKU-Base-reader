# ENKU Base R32 PCBWay readiness

**30/100% — estimate unchanged, RELEASE BLOCKED.**

R31 latest valid baseline: 120 parts, 234 Native KiCad violations (except unrouted), 0 schematic parity faults, 255 unconnected nets, 0 cross-component SMD pad overlaps in independent structural check.

R32 replaces three-pad fake J1 with full 3-signal + 2-mechanical-pad **JST S3B-PH-SM4-TB** SMT land pattern, moves J1 to x69.8 y93.5 r90, updates schema and project local library. Run Native ERC/DRC and R32 pad envelope gate before updating metrics.

Unresolved: genuine battery/NTC polarity and protected cell, fit and assembly 3D, nonbattery-isolating SW1 control, folded Good Display FPC, HV rail, routing 255+ connections, footprint qualification/PCBWay BOM/CPL, Gerbers/NPTH/3D.
