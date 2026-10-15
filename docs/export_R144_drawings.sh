#!/usr/bin/env bash
set -euo pipefail
: "${ENKU_KICAD_APP:?Set the verified KiCad10.0.7 AppRun path}"
repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
plot_dir="${1:?Pass the native-PDF intermediate output directory}"
mkdir -p "$plot_dir"
test "$("$ENKU_KICAD_APP" kicad-cli version)" = 10.0.7
source_dir="$repo_dir/hardware/mainboard/r144/kicad"
"$ENKU_KICAD_APP" kicad-cli pcb export pdf --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Fab,B.Fab --common-layers Edge.Cuts --mode-multipage --sketch-pads-on-fab-layers --no-property-popups --output "$plot_dir/layers.pdf" "$source_dir/enku-mainboard-r0.1.kicad_pcb"
# The wrapper adds the current title, source hash and pagination. All electrical
# schematic objects remain; excluding the inherited drawing sheet avoids its
# title block overlapping the bottom DNP component and clips no circuit object.
"$ENKU_KICAD_APP" kicad-cli sch export pdf --exclude-drawing-sheet --no-background-color --output "$plot_dir/schema-clean-new.pdf" "$source_dir/enku-mainboard-r0.1.kicad_sch"
