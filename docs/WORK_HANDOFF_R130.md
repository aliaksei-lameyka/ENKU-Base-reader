# ENKU Base R130 / BAT-REV3 handoff

Continue from **`engineering/bat-rev3-external-ntc`**, canonical `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`, selector R130, KiCad 10.0.7. Accepted R129 parent `b7d05483db8b1b7794280c472e52a7824d88a662` is preserved. Do not restart from stale main or rerun an R128/R129 mutator on this source.

Implemented: direct JST PH-2 J1 and separate bare NTC terminals J8; corrected Laird L2 lands and relocated its via/two endpoints; all 99 purchased MPN fields explicit; 97 CPL rows, 19 bare items, 2 DNP. Full native local and actual server results: **ERC 0 / opens 0 / parity 0 / DRC 20 unchanged holes / library 0**; 428 pads, 118 footprints, 2641 copper items. Seventeen guards include exact R129 preservation and explicit unresolved battery safety gates. See [decision/source/validation report](BAT_REV3_DECISION_R130.md) and [replacement interface](BAT_REV3_SERVICE_R130.md).

All 427 old pad identities and 2639 copper items survive. Only four original pad changes and three L2 copper moves, one new sensor ground land and two new ground copper items. USB MSC/SD/EPD/four buttons/hard switch/RF/rules/exclusions are preserved. Three already-sent supplier RFQs were read; no replies/attachments found, no additional mail sent.

**Do not call the battery design qualified.** Direct 103JT 3435 K TS hot entry is about 60 °C, while Akyga specifies 0–45 °C charge. The 300 mA setting and Rev B 360 min timer need a real full-capacity charging solution. The accepted Git tree lacks a current complete enclosure/panel assembly. A dimensioned native-based trial shows RF/width/boss and PH-2 overlap constraints; actual allowable battery T/W/L is unknown. The trial 16.03/17.23 mm stack scenarios are not final case dimensions.

Next: hardware temperature window and charge-cycle architecture; actual enclosure/pack cavity; model-specific vendor PCM/drawing/certification/polarity; then existing hole/process/SW1/FPC/stackup/Ceff/stencil/EPD/USB/prototype gates. No purchase, manufacture or default merge without owner authorization. **fabrication_ready=false**.

Actual source `889a069afb8aed9515fbff6daba5f5e659ff9753`, tree `ba202b00c54b395b1678e876c8d8044c46e21dbc`; run 38153676192 / job 114512129168 passed all 12 steps. Eighteen actual reports and the 33-member artifact ZIP are retained; binary SHA256 matches its API digest. [GitHub proof](GITHUB_NATIVE_R130.md). Metadata follow-up does not change tested hardware/workflow/guards. Hours only count observed bounded work; historical total remains unknown.
