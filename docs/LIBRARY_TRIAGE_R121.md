# R121 library mismatch triage — manufacturer qualification required

Read-only native comparison of all 111 warned footprints against the libraries referenced by this project. Each reference was placed, rotated and flipped into the actual board pose. Only enabled copper layers were compared. Symmetric pad rotations were normalized. The PCB was unchanged.

| Comparison class | Footprints |
| --- | ---: |
| pad_properties_equal_other_footprint_difference | 57 |
| pad_or_drill_difference | 52 |
| pin_number_or_attribute_difference | 2 |

Equality of pad properties does not certify custom primitives, footprint-level mask/paste overrides, graphics, exact MPN or vendor fit. The 111 native warnings remain active.

## Q1 — confirmed gate/source pad-location defect

Q1 is `IRLML6346TRPBF`, footprint `Package_TO_SOT_SMD:SOT-23`, front side, centre (67,48), angle 0. Embedded pin 1 / EPD_GDR is at (66,48.95), pin 2 / EPD_RESE at (66,47.05), pin 3 / EPD_SW at (68,48). The instantiated SOT-23 reference places pin 1 above pin 2 with the single drain pad on the right; the embedded Q1 has the opposite order.

Primary source: [Infineon IRLML6346TRPbF original datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlml6346-datasheet-en.pdf), pages 1 and 8. The package top view on page 8 places pin 1 and pin 2 in the standard SOT-23 order. Rotating that view so the single drain lead is on the right confirms the embedded Q1 Gate/Source location mirror. This is a geometry inference from the manufacturer view and native board coordinates, not a failure that native electrical connectivity detects.

Correct in R122 with a declared exchange of the physical locations of Q1 pads 1/2, preserving each pad UUID, number and net; reroute their connections and rerun full native and physical checks. Do not relabel nets merely to produce a lower DRC count.

## Other first review items

- J2 microSD has a 90-degree difference in nonsquare pad orientation relative to its project-local reference; recheck the Hirose manufacturer drawing before selecting which geometry is correct.
- SW1 uses an engineering placement footprint with different pad positions and sizes from its reference; exact switch MPN and mechanical fit remain unqualified.
- U1 exposed-pad drills are 0.30 mm versus 0.20 mm in the library. This may be an intentional engineering change and needs assembly/RF review.
- R64/R65 use 0.90 × 0.95 mm lands at ±0.80 mm rather than library 0.80 × 0.95 mm at ±0.825 mm. Preserve the USB reference check when deciding the qualified land pattern.
- J5 shell pad identifiers are `S` versus `SH`; J7 pad attributes differ. These need explicit symbol/assembly review and are not equivalent to the Q1 location defect.

The full per-pad differences and SHA-256 of each library reference are retained in `checks/library_mismatch_triage_R121.json`. No blind footprint replacements or rule waivers were applied.
