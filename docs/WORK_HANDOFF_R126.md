# R126 handoff

Canonical source: hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro. Current selector R126. Native KiCad10.0.7 CLI (GUI was not available in this environment). PCB SHA256 **8deaaa605264ce3119da6aae8e7a8a837cb9e781caa45e3348738eeb13585393**. Parent: accepted R125 proof head91b90bad1f4afd86a3fb5bcc1fcdf9c87e497df8.

61 exact component instances; 120 physically changed pads, all417 original pad UUIDs and net names preserved. Ten footprint placements change; all2610 original routed copper identities/net/layer/width/drill survive,57 explicit endpoint changes,29 declared new segments. Native opens0 ERC0 parity0 DRC65:45 library +20 holes. Independent native-assembly/MPN, physical via/Tag-Connect, USB reference/topology and whole-source guards pass locally. No rule/exclusion changes.

[Changes and primary-source manifest](COMPONENT_PASS_R126.md), [remaining work](REMAINING_TO_BUILD_R126.md), [server status and retained evidence](GITHUB_NATIVE_R126.md). Source mutation scripts are historical acceptance recipes; apply_component_pass_R126.py requires an immutable restored sibling ENKU_R125. The committed final board itself is the canonical input; CI does not rerun mutation recipes.

Next: remaining15 capacitors + R70/R71/R37 exact parts and numeric effective-capacitance/pulse gates, U1 process adaptation; resolve SW1/TL3340/USB holes, exact FPC and factory stackup concurrently. Preserve approved MK-12C03-G015 common2/upper edge and Q1/Q2/U9 verified pinouts. Base59×101/four buttons; Pro separate. NO FAB/default merge.

Actual server run38105337714 succeeded for source3ddd3b5c69579727d66c2cf29d0fce3610dedee1. Nine reports are retained; [proof](GITHUB_NATIVE_R126.md). Hardware/workflow remain identical in the evidence follow-up.
