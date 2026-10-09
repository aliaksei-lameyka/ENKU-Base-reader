# ENKU Base R44 — Native-verified remote slide PMOS control

**Planning PCBWay Ready: 30/100. Do NOT fabricate.**

Active R44 branch `engineering/r44-hard-power-gate-route`. Source `hardware/mainboard/kicad/enku-mainboard-r2.1-base-sw1-gate-trial.kicad_pcb`.

**Actually verified on GitHub**:

- [R44 final Native KiCad run 37893508039](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893508039): **SUCCESS**, strict ERC **0 errors / 0 warnings**, schematic parity **0**, zero high-priority shorts/track-via dangling/hole clearance and zero DRC items involving SW1 PWR_GATE or GND after zone fill.
- [R44 structural and active component regression 37893508052](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893508052): **SUCCESS**; MCU power, SPI microSD, fail-safe VBUS, active SMD overlap and plated drill checks.
- **Non-unrouted DRC violations: 239** (full DRC **not clean**). **143 unconnected items** (R43 had 146); 132 footprints, **471 track segments / 124 plated vias**, 2 inner GND zones.
- Native priority DRC 0 ≠ full DRC 0 ≠ valid soldered physical power slide. R44 changes neither panel HV/FPC nor USB data-pair conductors.

**Native-defect correction:** first R44 attempt [37893338057](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37893338057) failed **3 guide-hole clearance errors** adjacent TagConnect J7 NPTH x32.46,87. Relocated B.Cu gate path around holes and confirmed successful Native re-run. A preflight grid router that ignores NPTH is *not* a valid KiCad release tool.

**R44 physical nets:** SW1.1 PWR_GATE -> high-side Q2.1/R40.2 via F.Cu/B.Cu with two through-vias, ~101.91mm B.Cu path; SW1.2 GND routed on F.Cu to 0.7mm plated via (47.5,36.5) connected to both native-refilled GND planes. Gate line is high impedance (100k pull-up), thus long-path EMI/EFT/ESD and ON/OFF switching timing must be measured. Source topology ≠ immunity or qualified mechanical MPN.

**Major remaining blockers:** four U1→SW3..SW6 button GPIO signal routes still absent; footprint and case actuator selection, PMOS SOA/inrush/off current, 143 unrouted, 239 non-unrouted DRC, USB D+/D− 90Ω differential stackup and actual USB Mass Storage firmware/desktop proof, complete supply/EPD HV routing, Good Display pin5 VDHR/VSH2 manufacturer written reply and FPC fold geometry, BOM/CPL/Gerber/NC drills and actual PCBWay DFM, power/EMC thermal and I/O tests.

**Release: NO-GO.**