# R139 repository consolidation - physical R138 / NO FAB

User authorized integration into main and repository housekeeping on13October2026. The main update retains the complete R139 qualification/packet work descended from accepted main81b34a9 and all observed earlier branch heads. No branch or historical evidence is deleted.

## Scope and ancestry

45 remote heads were inspected.40 were already ancestors of R139 before consolidation. Five additional heads are retained as additional merge parents, with exact binary-capable diffs against their actual merge bases:

| Branch | Retained head | Meaning |
| --- | --- | --- |
| engineering/r134-native-evidence |e7c7b866112eea880394ffc889e084461a2586a9|Historical R134 CI/evidence state |
| engineering/r135-native-evidence |955474ac39ce3ee3f8a21529247e749ae57b9a4d|Historical R135 CI/evidence state |
| engineering/r136-native-evidence |94919167680a7858679c56435f91b8cd12a5efea|Historical R136 CI run identities |
| engineering/r50-dianwei-j3-evaluation |ee407d9f9d8e2372ee00d3a36338b9d964013c74|Read-only connector evaluation, not a approved J3 substitution |
| research/r24-c915811-4pin |507cb99cca38a5eb4938a1c04cd4ced95301efb0|Superseded switch experiment; current E-Switch hardware remains |

[Exact branch registry](qualification/R139/REPOSITORY_BRANCHES_R139.json), [historical diffs](history/retained-branches/README.md). Consolidation deliberately retains the accepted current hardware tree while preserving all historical ancestry and experimental changes for review. Evidence from older versions is not a new current test pass.

## Housekeeping

- Root README now distinguishes physical R138 from qualification R139, supplies current status/handoff/packet/battery/test links and keeps the original licensing/related-project sections.
- New stable documentation index, current mainboard overview and canonical KiCad directory guide identify current source and historical materials.
- Existing historical files are retained in place: native regression preservation pins1325 source hashes. In particular the original mainboard README is a frozen R136 record; current entry points explicitly identify its historical scope.
- Local KiCad session/backup files, Python caches, local runtimes/results and private supplier material are excluded from new Git additions. Verified source, licenses, BOMs and ZIP proof remain tracked.
- Current battery review records explicit Polybattery unavailability, no new Koosay response after the existing sent follow-up, Ropla's rejected5.2mm finished pack and inspection of its polarity photo without inventing a PH-2 pin map.

Physical PCB/libraries/schematic/rules/mask/paste/placements/BOM remain unchanged. Frozen PCB SHA256 `90d6e0ccd729ac6e916e7f24e173d52a316c3cd640128ea5d6df1f0fcafa8971`; engineering-review packet SHA256 `c113ffdac4c2613a2f8736acf692a01c063a4e41b7f521715bab50e7373a3b00`.

## Verification and release

Current-entry relative links, all1325 historical hashes, the complete hardware/workflow tree against R139 and the retained patch bytes are checked before publication. No guard is loosened and no native checkpoint regenerated for housekeeping. The actual existing main native workflow runs after the integration; its job conclusion/artifact must be inspected rather than assumed.

All physical product tests and manufacturing authorization remain HOLD. No mail, order, payment, purchase, factory upload or PCB production occurred. Read [CURRENT_STATUS](CURRENT_STATUS.md) for unresolved startup/NTC/pack/case/panel/firmware/FCT/process inputs.
