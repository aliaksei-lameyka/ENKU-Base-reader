# Actual GitHub native R132 proof — NO FAB

**KiCad10.0.7 server source matches the committed local PCB and geometry.** [Actual successful run38175546736](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38175546736) on branch`engineering/r132-battery-supply-charge`, event`push`, source commit`970c93eac57e411a45d5975d73ed080071d4769b`, tree`05e223518200bd546b66153ea9da767e2767d1a5`. Hardware SHA256`540faac1779277466bdaca739325d1139cf8cead39f4d9b9df1eaa0529a648f3`. Job114577056261: all12actual job steps succeeded, including exact runtime install, full native DRC/ERC/parity,17independent guards, checkpoint comparison and artifact upload. The later evidence-only commit does not change the canonical hardware; no second run is claimed for it.

| Real server result | Value |
|---|---:|
|Unconnected items|0|
|ERC violations|0|
|Schematic parity|0|
|Other native findings|20unchanged intrinsic hole clearances|
|Library mismatches|0|
|Footprints/pads|122/442|
|Native fitted CPL rows|102|
|Bare PCB/DNP items|19/1|
|Independent engineering guards|17|
|Actual JSON result reports|18|

The source commit, native10.0.7 version, exact pad/track UUIDs and geometry, footprint placement, RF/zone restrictions, source preservation and retained20hole findings were independently checked from the downloaded artifact. Actual native assembly-features/orientation/CPL/review-BOM files match local bytes. **16report JSON objects match exactly.** U1-plot and IC-stencil reports have different raw plot hashes because native SVG titles contain each machine's export time. All three raw SVGs were compared: removing only the one validated title date makes their bytes identical. Every physical/report field agrees; each original plot hash was validated against its corresponding untouched local/server SVG. No geometry tolerance or rule was relaxed to account for these metadata differences.

Artifact11715901613:`enku-native-kicad-970c93eac57e411a45d5975d73ed080071d4769b`,455203bytes. Its API digest and downloaded ZIP SHA256 both equal`27674619166d84889e167a7199bbd3ba7729144ddeabd4c922b099ac568db856`. ZIP CRC was verified and all33members inspected. The actual binary is retained at[checks/native_server_R132.zip](../hardware/mainboard/kicad/checks/native_server_R132.zip), not just a UI success badge. [Machine-readable proof](../hardware/mainboard/kicad/checks/github_native_proof_R132.json) and individual unchanged`server_*_R132.json`reports are committed. Actual API run/job results were read; a initially empty connector query was not treated as evidence of no run.

Passing native/independent checks does not qualify a protected battery,0–45°C charging, full-capacity timer/thermal behavior, effective capacitors, actual unchanged-thickness enclosure, controlled USB stackup or assembly process. **fabrication_ready=false.** The20existing intrinsic holes and remaining gates are listed in the[current handoff](WORK_HANDOFF_R132.md). No production, purchase or new supplier message was sent.

Proof capture UTC:2026-10-11T21:24:32.396374+00:00.
