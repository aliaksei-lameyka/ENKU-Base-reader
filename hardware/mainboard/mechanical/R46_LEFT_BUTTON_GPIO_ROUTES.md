# ENKU Base R46 — physically routed left-hand reader GPIOs

**Source:** `hardware/mainboard/kicad/enku-mainboard-r2.3-base-left-button-signals.kicad_pcb` on `engineering/r46-left-button-signals`. R45 remains a Native-qualified reference.

### Electrical changes (not only documentation)

The four-button concept uses U1 ESP32-S3 module pins4–7 and case-edge SW3–SW6. The inner zones are GND. R45 connects all four button GND returns but **none of the four signal GPIOs**.

R46 makes two new end-to-end signal copper paths:
- `BTN_L1`: ESP32 U1 pad4 x31.55 y53.75 → F.Cu escape north to (31.5,51.75) via → 0.18mm In1.Cu under ESP32 *digital* module body (not antenna keepout), dogleg around pre-existing U1 GND via (27.74,55.5) → second via (27,60.75) → F.Cu to SW3 pad1 (25,60.8).
- `BTN_L2`: U1 pad5 (32.82,53.75) → (32.75,51.75) via → In1.Cu from (30,54.5) along x30 to (30,68), then southwest to (28,72.75) via → F.Cu SW4 pad1 (25,72.8).

2x2 additional Ø0.70/0.30mm plated via transitions; 12×0.18mm copper segments; active board 132 footprints, **483 track records**, **128 vias**, two inner GND zones. Preflight evaluated existing track/via clearances; real filled Native KiCad DRC must validate, and exact via-vs-pad/NPTH clearance is not inferred from preflight.

**Mechanical/RF warning:** U1 input escapes occupy PCB below the non-antenna portion of the ESP32 module. Manufacturer keepout and 3D must still be checked; no traces permitted below the antenna. Internal signal tracks displace In1.Cu GND copper. Confirm both GND plane continuity/return for EPD high-voltage, MCU and USB. SW3/SW4 are currently `ENKU:READING_BUTTON_PLACEMENT` placeholders, NOT approved switch MPNs and not final for production. BTN_R1/R2 remain unrouted; do not pretend 4-button I/O is finished.

R45 verified baseline [Native run 37893987801](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893987801): ERC0, priority-critical0, 224 non-unrouted DRC,143 unconnected. R46 native validation pending.


## Actual Native KiCad qualification

[R46 Native 37895191252](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895191252) and [structural 37895191246](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895191246) SUCCESS after correcting stale inherited test assertions that previously prohibited any button signals. New GPIO BTN_L1/BTN_L2 pad1 native unconnected 0. ERC0, PCB↔schematic parity0, priority DRC0, **141 remaining unconnected**, **224 non-unrouted DRC errors**. Real MCU module physical underside/thermal antenna zone qualification and placeholder side switch MPN still blockers.
