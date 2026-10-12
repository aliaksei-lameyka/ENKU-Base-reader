# ENKU Reader R0.1 — fit gate R03 (2026-10-08)

**Status: blocking conflicts identified; no PCB changes or manufacturing approval.**

Reference: provisional case 62 × 109 × 10 mm; module rectangle x=2.88..59.12, y=3.2..99.82; PCB rectangle x=1.5..60.5, y=7.5..101.5. These are preliminary coordinate registrations, not confirmed from STEP.

Existing KiCad mounting centers (PCB coordinates) H1=(30,23), H2=(71,23), H3=(23,111), H4=(71,111). Transform PCB XY to case XY by subtracting (18,20) and adding (1.5,7.5). With nominal 5 mm support boss diameters, **all four mounting boss projections intersect the display module footprint**. No drill may pass through or load the display. Relocate supports and/or redesign PCB mounting architecture before freezing enclosure.

The lower rear-cover screws are independent from PCB holes. Nominal centers (7.5,104.2) and (54.5,104.2) are outside module rectangle, but screw boss / FPC / USB-C / microSD / print clearances remain unvalidated.

The 40 × 60 mm candidate battery in case XY x=11..51, y=24.5..84.5 intersects an approximate ESP32 envelope x=7.5..25.5, y=20..45 by 297.25 mm². This XY collision is a **packaging warning**; actual Z interference requires a full component-height map. The 10 mm target remains unverified.

## Mechanical decision

- Asymmetric bezels, upper hooks, two lower rear screws retained.
- Four existing PCB mounting holes **must not be used unchanged**. They are not aligned to safe display-free zones in the current stack.
- Before modifying KiCad: confirm display FPC model, actual rear-facing components and LiPo pack envelope, and choose a PCB-retention strategy that does not enlarge the side bezels.
- Need assembly-accessible PCB fasteners or serviceable clips without stressing the e-paper glass; validate with cross sections.

Local calculated gate artifacts: `enku_mechanical_gate_r03.py`, `enku_mechanical_gate_r03.json`, `enku_mechanical_gate_r03.svg` generated in this work session.
