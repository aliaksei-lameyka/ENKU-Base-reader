# Concrete supplier questions — R123 (draft, not sent)

## E-Switch / TL3340AF160QG / P021301 rev B

1. Are the two Ø0.90 circles at 4.25 mm pitch in the recommended PCB layout drilled locator holes? Confirm the pin diameter/tolerance, hole finished diameter/tolerance, plating status and mounting-side/top-side interpretation.
2. Confirm the signal lands: outer width 0.75 mm, middle width 0.60 mm, height 1.80 mm; bracket lands 1.30 × 0.90 mm and the 2.00 × 1.20 mm circuit-trace keepout. Supply an unambiguous dimensioned layout/native CAD for the exact suffix.
3. With that interpretation, nominal copper-to-hole gaps calculate to 0.075 mm at the contact and 0.150 mm at the bracket land. Are these intended and qualified for assembly? Specify accepted finished-hole registration, mask/paste and soldering controls. Current global PCB rule is 0.250 mm, and findings are active.
4. Confirm that terminals 1 and 2 are internally common and press connects them to terminal 3; unused external terminal 2 is permissible. Confirm actuator datum/travel and part height for side-button enclosure fit.

## PCB fabricator / assembler

Review the four USB4105 guide-hole gaps and sixteen TL3340 locator gaps against the exact drawings, drill/Cu registration and stackup. Supply an actual four-layer 90-ohm USB stackup and proposed width/gap rather than a generic stackup. Confirm U1 exposed-pad via/drill, mask/paste, via-to-land rules, acceptable part rotations and source BOM MPNs before freeze.

## Good Display

For the exact Base panel, confirm 24-pin FPC pin 5 (VDHR versus VSH2), contact sides/orientation and connector drawing, fold path/minimum bend radius, and whether supplied GDEM STEP/DWG is geometrically identical to the ordered GDEY panel. The prior reply did not explicitly close these points. Pro/frontlight/touch is outside this Base checkpoint.
