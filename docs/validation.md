# Validation

The repository uses two levels of checks.

## Lightweight checks

Structural checks run on hardware changes and catch issues that do not require KiCad itself:

- schematic hierarchy integrity
- required Base references and nets
- PCB population parity
- project-local footprint consistency
- placement and orientation invariants
- selected routing regression checks

These checks are intentionally fast.

## Native KiCad checks

Native KiCad ERC and DRC are the authority for electrical and PCB-rule validation.

They are used at meaningful engineering gates rather than as an interactive router. A passing structural check does not replace native ERC/DRC.

## Fabrication release gate

Before Base R0.1 can be released for fabrication, the board must have:

1. final Base routing closed;
2. no unexplained ERC errors;
3. no fabrication-blocking DRC violations;
4. final battery connector selected and polarity verified;
5. final hard-power switch selected and actuator geometry verified;
6. final side-button switch selected and enclosure interaction verified;
7. e-paper FPC pin 1, contact side and bend path verified against the selected panel;
8. USB-C and microSD mechanical access checked against enclosure geometry;
9. dock pogo face and pin order checked;
10. Gerber, drill, BOM and pick-and-place outputs visually reviewed.
