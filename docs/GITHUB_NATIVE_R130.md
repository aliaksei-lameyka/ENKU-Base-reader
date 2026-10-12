# R130 actual GitHub Native KiCad proof

Source commit **889a069afb8aed9515fbff6daba5f5e659ff9753**, complete tree **ba202b00c54b395b1678e876c8d8044c46e21dbc**, parent R129 `b7d05483db8b1b7794280c472e52a7824d88a662`. Branch `engineering/bat-rev3-external-ntc`. The complete tree matched the frozen local Git tree; all 88 changed/new blob SHA1s matched. Source tree contains 767 blobs.

Actual [GitHub Actions run 38153676192](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38153676192), job 114512129168, event push, KiCad 10.0.7, conclusion **success**. All 12 actual job steps succeeded. Eighteen JSON reports were extracted from actual decoded job output, matched to PCB SHA256 `c5b1785535fd7d12c02ee8aaae5b8f96da9404f2bc55d919644b85209ebb4a96`, and retained as `checks/server_*_R130.json`. Source/server geometry comparison passed, including pad polygons, drills, placement, zones and RF restrictions. This is not a locally simulated server run.

| Native result | Actual server |
| --- | ---: |
| ERC, including warnings | 0 |
| Opens | 0 |
| Schematic parity | 0 |
| DRC hole-clearance findings | 20 |
| Other DRC / library findings | 0 |
| Pads / footprints / copper items | 428 / 118 / 2641 |
| Independent engineering guards | 17 |
| CPL rows / explicit purchased MPN fields | 97 / 99 |

The 20 findings are the unchanged active button/USB holes, verified by item UUID and finding contents. No rule or exclusion was weakened. Battery guard success verifies native inputs and detects the temperature/timer limitations; **it does not qualify charging**.

Artifact ID **11707323952**, `enku-native-kicad-889a069afb8aed9515fbff6daba5f5e659ff9753`, **413220 bytes**, 33 ZIP members. The actual ZIP was downloaded, every member CRC checked, its source identity/native comparison read, and SHA256 compared with GitHub's API digest:

`5b8b3ef9e41b3176acdd4d893f981fac0b2709a1c37fe8e8a32652b95be1844d`

Retained binary: [native_server_R130.zip](../hardware/mainboard/kicad/checks/native_server_R130.zip). API metadata, actual step outcomes and report filenames: [server_evidence_R130.json](../hardware/mainboard/kicad/checks/server_evidence_R130.json). No temporary signed download URL is retained in source.

Proof captured `2026-10-11T16:10:05.876Z`. Current observed interval 1.161910 h; recorded project lower bound 6.750856 h. Historical total remains unknown; idle/unbounded earlier work is not fabricated into the ledger. Follow-up proof/docs/archive work is outside this bounded interval.

The proof follow-up changes only README/handoff/hours/verification metadata and adds actual server reports/artifact/evidence. Tested PCB, schematics, libraries, project rules, workflow, guards, local geometry and mechanical studies remain byte-identical to source 889a069.

**fabrication_ready=false**. [Battery and mechanical decision/gates](BAT_REV3_DECISION_R130.md). No manufacture, sample purchase or default merge.
