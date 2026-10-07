# Manufacturing notes

Base R0.1 is an engineering first-spin board. Manufacturing outputs are not considered authoritative until the fabrication release gate is closed.

## Board

- 4 layers
- 54 × 94 mm outline
- portrait primary orientation

The KiCad source under `hardware/mainboard/kicad/` is the editable source of truth.

## Assembly package

A release package will contain:

- Gerber files
- NC drill files
- BOM
- pick-and-place / CPL
- assembly notes
- board preview
- revision identifier

Generated outputs belong under `hardware/mainboard/production/<revision>/` and should not be edited by hand.

## First-spin priorities

For the first fabrication run, debug access and repairability take priority over cosmetic density. Important power rails and e-paper high-voltage rails retain measurement access where practical.

Component reference markings and polarity/orientation cues should remain readable after assembly wherever board space allows.
