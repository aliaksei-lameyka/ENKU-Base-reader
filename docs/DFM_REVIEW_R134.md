# R134 fabrication gates — NO FAB

The routing and native verification gates are separate from manufacturing acceptance. Design, nominal electrical/mechanical and factory-process gates must be reviewed before a PCBWay EVT submission; measurements requiring an assembled board follow approved EVT and must pass before production release. Tests marked NOT RUN are not manufactured evidence. This is an engineering review document. No factory submission, order or purchase occurred. Fixed enclosure thickness,59×101×1.6 mm PCB,2000–2500 mAh two-wire PCM battery target and separate cell NTC are retained.

## Completed design changes

GCT USB4215-03-A replaces USB4105 with the manufacturer-specific no-peg footprint,3.16 mm nominal height, four plated shell slots and the preserved boardY121 mm mating face. Actual mask/paste, numbered contact nets and nominal slot geometry are audited. Four former J5 locator findings are eliminated through a real component/land change. No active board rule, severity or exclusion was relaxed.

GPIO16/2/38 now control BQ24072T EN1/EN2/CE with three 1k series and two 2.2k pull-down resistors. EN2pin5/VSSpin8 library/cache naming is corrected. OFF/high-Z models USB100; USB500 and suspend are hardware-selectable, with firmware/bench qualification pending. Bare TP8 moves to55.5/94.5 mm and its mirrored PG label to55.5/92.7 mm. All earlier mounted core placements remain preserved.

The native continuous B.Cu GND region touching U3 grows from 22.8123 to approximately 55.3333 mm², exceeding the 50 mm² geometry objective. Filled/capped five 0.50/0.30 mm under-EP through-via requests and all prior zones remain unchanged. This area alone does not prove temperatures, stencil/reflow quality or a full charge cycle.

## Design, EVT and production gates

| Gate | Current evidence and unresolved point | Closure required |
|---|---|---|
|Full native source and independent audits|ERC0/opens0/parity0; actual current source passed all 21 independent scopes and a fresh immutable-source GitHub run 38240134929. Actual digest/CRC and all 22 export/report comparisons are retained.|Retain actual source/run/job/artifact hashes, all 22 reports and unchanged-source comparisons. Passing engineering checks does not waive the rows below.|
|SW3–SW6 hole-to-copper|16 active KiCad hole_clearance errors remain under 0.25 mm rule. TL3340AF160QG recommended 0.90 mm NPTH locators have 0.075 mm signal and 0.150 mm bracket gaps.|Document guaranteed part/factory registration and an explicitly accepted component-specific manufacturing process, or select a replacement and revalidate actuator/lands/routing/case. Do not shrink holes, clip lands or suppress findings.|
|J5 assembly and plug fit|USB4215 has nominal 0.8 mm stakes on 1.6 mm PCB; replacement is not an approved old-model drop-in.|Approve exact slot/drill/finished plating, soldering or pin-in-paste process, retention, case opening, plug insertion and current supplier SKU.|
|U3/U1 stencil and thermal construction|Five U3 vias request fill/cap with exposed top metal and bottom mask; continuous GND goal now met.|Factory acceptance of fill/cap flatness/finish/voiding and actual output semantics; stencil/reflow/EP inspection and worst-case thermal evidence in fixed case. Mask tenting alone does not replace fill/cap.|
|Effective capacitance|C7/C8 nominal 22 uF; minimum 4.7 uF effective required; previous bias-budget condition retained.|Exact-part voltage/temperature/aging/tolerance curves and justified effective capacitance under actual operation.|
|Separate NTC and single faults|Nominal cold/hot/open/short modeling retained. Sensor detachment still electrically valid; R81-open at hot temperature remains an identified unsafe fault.|Review protection architecture, actual full R/T and leakage corners, attachment/thermal lag/self-heating, injected faults and charge inhibit. CE GPIO by itself does not resolve sensor detachment.|
|Current mode and USB|Hardware now selects USB100/500/suspend; high-Z/OFF is modeled USB100, no automatic BC1.2/PD or fast OFF500 mA.|Firmware policy, GPIO voltage margins under load, boot/ROM/brownout/hold states, mode-transition ordering, OFF/backfeed/inrush and host suspend/attach/disconnect measurements.|
|Full charge and system budget|Nominal445 mA/8.725 h; setting/timer corner models retained, current shares reader/DPPM/thermal load.|Full2000–2500 mAh charge cycles at approved limits/load/temperature before applicable minimum timer; no automatic CE restart to hide faults.|
|Battery/mechanical/CN+PL supply|No approved thin finished pack or two interchangeable stocked replacements; current PH2/pouch and enclosure conflicts remain.|Registered full current enclosure/component CAD, fixed-thickness fit and service proof, controlled PCM pack/polarity/pulse data, exact CN stock and Poland purchase channels. See BATTERY_STATUS_R134.md.|
|USB impedance and functionality|Long differential copper and actual refilled reference planes guarded; no claimed production 90-ohm stackup or working MSC firmware.|Accepted four-layer stackup/impedance tolerances and both USB orientations with firmware, exclusive SD ownership, safe hotplug and computer transfer tests.|
|Panel/FPC and final assembly outputs|Historical supplier material retained; exact pin5/panel-model/FPC mechanical evidence remains outstanding.|Resolve exact panel/FPC revision/orientation/bend/connector fit; review final BOM/CPL/mask/paste/drill/board/assembly artifacts from the approved source.|
|Manufacturing/purchase authorization|Not granted by development or CI.|After engineering/factory review, present the concrete release package and obtain user agreement before manufacturing or ordering.|

Source references for the button/process decision remain E-Switch P021301 revisionB and GCT USB4215 RevA26Apr2024; nominal recommended geometry is not a factory registration guarantee. Native rule violations remain visible. Historical R133 source and reports are preserved.

## First-board validation

Use [the R134 first-board measurement plan](BRINGUP_R134.md) and [the current signal contract](USB_POWER_CONTROL_R134.md). The older R132 hard-selected USB500 paragraph and 20-hole release count are historical and superseded here. Begin with unpowered inspection and current-limited emulators/fixtures before any unqualified battery. Record exact PCB SHA, assembled BOM/pack SKU, firmware commit, fixture, temperature, scope/current logs and verdict. All physical tests remain **NOT RUN**.
