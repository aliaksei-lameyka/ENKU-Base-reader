# ENKU Base R130 / BAT-REV3 handoff

Continue from **`engineering/bat-rev3-external-ntc`**, canonical `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`, selectorR130, KiCad10.0.7. Accepted R129 parent `b7d05483db8b1b7794280c472e52a7824d88a662` is preserved. Do not restart from stale main or rerun an R128/R129 mutator on this source.

Implemented: direct JST PH2 J1 and separate bare NTC terminals J8; corrected Laird L2 lands and relocated its via/two endpoints; all99 purchased MPN fields explicit;97 CPL rows,19 bare items,2 DNP. Native full local **ERC0/opens0/parity0/DRC20 unchanged holes/library0**;428 pads,118 footprints,2641 copper items. Seventeen guards include exact R129 preservation and explicit unresolved battery safety gates. See [decision/source/validation report](BAT_REV3_DECISION_R130.md) and [replacement interface](BAT_REV3_SERVICE_R130.md).

All427 old pad identities and2639 copper items survive. Only four original pad changes and three L2 copper moves, one new sensor ground land and two new ground copper items. USB MSC/SD/EPD/four buttons/hard switch/RF/rules/exclusions are preserved. Three already-sent supplier RFQs were read; no replies/attachments found, no additional mail sent.

**Do not call the battery design qualified.** Direct103JT3435K TS hot entry is about60°C, while Akyga specifies0–45°C charge.300 mA and the RevB360 min timer need a real full-capacity charging solution. The accepted Git tree lacks a current complete enclosure/panel assembly. A dimensioned native-based trial shows RF/width/boss and PH2-overlap constraints; actual allowable battery T/W/L is unknown. The trial16.03/17.23 mm stack scenarios are not final case dimensions.

Next: hardware temperature window and charge-cycle architecture; actual enclosure/pack cavity; model-specific vendor PCM/drawing/certification/polarity; then existing hole/process/SW1/FPC/stackup/Ceff/stencil/EPD/USB/prototype gates. No purchase, manufacture or default merge without owner authorization. **fabrication_ready=false**.

GitHub source/run/artifact evidence is retained in `GITHUB_NATIVE_R130.md` after the actual run. Hours only count observed bounded work; historical total remains unknown.
