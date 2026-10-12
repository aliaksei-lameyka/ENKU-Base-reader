# ENKU Base R129 handoff

Canonical project `hardware/mainboard/kicad/enku-mainboard-r0.1.kicad_pro`; selector R129. Accepted R128 proof HEAD `6cd4868c0aaa7af0680c8ef72b56f35b824d4345`, tree `ffe7cf0682465543c2b74a0a44cf323996934733`, PCB SHA256 `f53da6653e1f98241a4da7e337aa001a2b8614fa1b3e0685d893d299a18d5fa6`. R129 PCB SHA256 `bab3cda1faa40bb2535f2d3eefe6ef0a9f43593b82577843cfe54f6d98da013c`. Exact KiCad10.0.7/runtime SHA pinned in workflow.

R129 corrects U4 full-paste overlay and uses two TI rounded stencil apertures; corrects U3 EP/paste corner/dimensions; moves J7 pin1 marker to actual pad1; canonicalizes symmetric pad angles and service contact type; restores10 omitted SMD parts to native CPL97 rows; excludes18 bare-PCB and2 DNP objects. All26 native library mismatches close through explicit classification and appropriate local definitions. See [engineering details](ACTIVE_IC_AND_ASSEMBLY_R129.md).

All425 old pad identities/nets/drills/positions and2639 tracks/vias are preserved. Exactly25 declared old pad-property changes plus2 paste-only pads; only U3 EP corner copper changes. Unrelated copper/placement/connectivity/source/rules/exclusions/zones/RF keepouts survive. Primary constants verify52 pins of six ICs, bypass/support networks and operating modes. U1/USB/buttons/SW1/Q1/Q2/U9/passive79/power models remain guarded.

Local native **opens0/ERC0/parity0/DRC20 only holes;427pads/117footprints**. Fifteen independent guards pass. Actual full native top/bottom, IC mask/paste and J7 plots were visually reviewed. Actual R129 run 38136336929, job 114460858170, source 3fe0934dff0059202fbc5455c16a5b778fff365b succeeded in all12 job steps. Sixteen actual job-log reports and artifact API metadata are retained. server_verified=true, fabrication_ready=false. The proof follow-up preserves all hardware/workflow/script bytes. [Evidence](GITHUB_NATIVE_R129.md).

Continue with12 missing MPN fields and mechanical/assembly freeze, controlled SW1/FPC/panel data,20 intrinsic hole findings, stencil/U1 tents/Ceff/pulse/USB bench/factory stackup. [Remaining work](REMAINING_TO_BUILD_R129.md). No arbitrary holes/rule changes. Mutator requires immutable R128 and must not be rerun on newer PCB.

Base59×101, four buttons, no Hall/frontlight/Qi/Pogo/Dock; Pro separate. Engineering branch only, no default merge, supplier messages/orders or fabrication release. **fabrication_ready=false**. Historical hours unknown; add only bounded active current interval through real CI proof capture, excluding idle after R128.
