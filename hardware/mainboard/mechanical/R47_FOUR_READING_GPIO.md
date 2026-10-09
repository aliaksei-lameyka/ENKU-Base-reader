# R47 — hardware GPIO of all four side reading buttons

Active PCB `hardware/mainboard/kicad/enku-mainboard-r2.4-base-four-reading-gpios.kicad_pcb`. Verifiable delta from R46: **32 new F.Cu/B.Cu copper segments and 4 plated vias**, now 515 segments and 132 vias; 132 footprints and both inner GND reference zones unchanged.

Previously validated R46 left `BTN_L1`/`BTN_L2` from U1 pads4/5 to SW3/SW4 remain unchanged. New source PCB has **right signals**:
- U1 pad6 (34.09,53.75) F.Cu to PTH via (34,51.75), then B.Cu off the occupied MCU regulator/BOOT rail near x34,y44, route east above the regulator area to (68,60.75), and F.Cu SW5 pad1 (71.2,60.8).
- U1 pad7 (35.36,53.75) F.Cu to PTH via (35.25,51.75), B.Cu separated north-east path via x48.5,y42.5 and x65.75,y64 to PTH via (69.75,72.75), then F.Cu SW6 pad1 (71.2,72.8).

The B.Cu paths pass behind the **digital** portion of the ESP32 module: physical MCU antenna courtyard/return-plane and board enclosure still require manufacturer/3D qualification. All side switch footprints remain provisional placement-only; do not order assembled PCB before locking real MPN/actuator geometry. USB D+/D− intentionally unrouted pending real PCBWay 4-layer 90Ω stack. No Good Display panel pin5/FPC modification.

R46 final [Native 37895191252](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895191252) ERC0 / priority DRC0 /224 non-unrouted DRC / 141 unconnected. R47 Native verification pending.
