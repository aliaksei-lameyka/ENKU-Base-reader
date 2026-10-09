# ENKU Base Reader R47 — manufacturer readiness audit

**PCBWay Ready: 30/100 (engineering planning estimate). FABRICATION AND ASSEMBLY: NO-GO.**

Branch `engineering/r47-right-button-signals`; source `hardware/mainboard/kicad/enku-mainboard-r2.4-base-four-reading-gpios.kicad_pcb`. **132 placed components, 515 KiCad track segment records, 132 plated through vias, two inner GND zones.**

## Verified successful CI runs

- [Native KiCad R47, run 37896089937](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37896089937): **SUCCESS**, ERC **0 errors / 0 warnings**, schematic parity **0**, priority DRC shorts/copper clearance/NPTH/edge/mask/dangling **0**, **all four reader GPIO nets native unrouted 0** after filling In1 and In2 GND zones, original PMOS SW1/SD/USB VBUS hard gates passed.
- [Active structure and physical pad/via checks R47, run 37896089990](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37896089990): **SUCCESS**, pad geometry and via-hole-on-SMD land checks pass, four MCU-to-side-switch signal source graphs pass.
- Remaining **139 unconnected items** (R46 141), **224 non-unrouted DRC violations**: **130 library footprint mismatches, 67 silkscreen clipped by exposed copper/mask and 27 silkscreen overlaps.** `text_height` is **0**. Full board DRC still **fails**.

## What physically changed

- GPIO BTN_L1/BTN_L2 x2 left buttons already verified R46 on F.Cu/In1.Cu; R47 routed BTN_R1/BTN_R2 U1 pads6/7 to SW5/SW6 signal pads on F.Cu/B.Cu, each with two plated vias. All SW3..SW6 grounds were previously stitched in R43.
- Initial [Native 37895850675](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37895850675) **failed 4 copper clearances** at right-button vias too close to ESP32 BOOT B.Cu. Corrected vias to (34,50.5) BTN_R1 and (36.5,51.5) BTN_R2, modified F.Cu pad escapes without moving BOOT, then passed final Native.
- The routing is electrically connected and Native KiCad DRC priority-clean but **NOT end-to-end firmware-functionality or RF/SI-validated**. The MCU module underside routing, antenna keepout and reference return paths still need vendor drawing review and DFM.

## Remaining production blockers

1. **139 other electrically unrouted connections** across the MCU/E-paper, button auxiliary paths, charging, dock and USB subsystems. Critical USB D+/D− differential data-pair copper **has not been routed**; select actual PCBWay stackup for 90Ω differential impedance, ESD placement and intact return plane. USB-C microSD Mass Storage firmware still unproven on Windows/macOS/Linux; Wi-Fi uploader remains optional.
2. **224 DRC violations remain**. Need manufacturer-accurate pad library review for 130 mismatches, not indiscriminate footprint overwrite (custom diode cathode polarity, stepped FPC, service/microSD layouts); finish 94 silkscreen crop/overlap fixes.
3. Side-reading buttons SW3..SW6 and hard slide SW1 **are placeholder placement-only footprints**; identify orderable MPN, pin contact order, actuator height, force, case travel and actual solder land before PCBWay assembly. Long Q2 gate/ESD/leakage and LiPo charging behavior still need electrical bench testing.
4. Good Display panel GDEY0397T81P FPC **pin5 VDHR versus VSH2 disagreement** — supplier already emailed, await written confirmation before committing J3/EPD HV or FPC case release.
5. Ground continuity/thermal/inrush, ESP32 RF antenna keepout (B.Cu signal underside), 3D USB/SD insertions, battery connector and NTC, full ERC/DRC0, BOM+PnP/CPL+Gerber+NC-drill manufacturing signoff and board power-up tests.

**Manufacturing files intentionally not generated.** Native priority pass != full fabrication DRC pass.