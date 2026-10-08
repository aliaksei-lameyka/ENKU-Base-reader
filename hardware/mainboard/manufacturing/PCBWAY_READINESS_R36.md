# ENKU Base — R36 PCBWay readiness

**30/100 (planning estimate), not fabrication-ready.**

R36 first physical KiCad copper: 18 local segment records and one through-via for PMOS gate, VSYS and switched SYS_EN around Q2/R40/TPS63802 input. All four copper layers retained, 125 components. Actual source includes no EPD panel copper or FPC breakout, and no BQ25185 SYS-to-Q2 feed yet. Native KiCad ERC, parity, DRC and remaining unconnected counts **pending**. R35 prior Native verified [37802371422](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37802371422): ERC0, parity0, DRC non-unrouted236, unrouted267.

Sign-off remains blocked by power path completion, U4 0.18mm VIN breakout power-current adequacy, planes/return currents, FPC-7750 actual fold/pin5 clarification, real SW1 MPN, 4 button pinouts/PCB cutouts, MOSFET thermal/inrush, battery NTC/polarity, full copper, fabrication outputs and BOM.
