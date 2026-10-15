# Current state

R147 on engineering/r147-mechanical-review, source commit0dccd442fb7ada7ad982a0ff375ac76560a5b862, PCB SHA256856e6d84905f978994316e2efcbb398184cf06dc4f95580c203ee244dd918bb2. Local and actual server run38763074552 PASS,24 manufacturing payloads and41 reports compared.18 marks reviewed,12 simplified. All mechanical source features preserved; R146 enclosure STEP is compatible. [Handoff](WORK_HANDOFF_R147.md). [CAD downloads](../hardware/mainboard/mechanical/r146_r147/DOWNLOADS.md).

Physical tests NOT RUN / NO FAB. SW1, FPC, battery/NTC and manufacturing/bench acceptance holds remain.

## FPC mechanical review,15Oct2026

Actual J3 opening direction checked from OEM solid: mouth at KiCadY35.8, insertion from +Y toward-Y. Straight12.5mm corridor intersects nominal C24/C29/C30 and an edge of L2. This is a counterexample to flat routing, not proof that all folded alternatives fail. Reach, true folded pose, no-pressure closure and latch access remain HOLD. Previous board STEP omitted those small MLCCs; use the four-cap add-on for case design. Saved R04 case has no display/flex/populated parts and its trial mounts differ from R147. [Detailed review](qualification/R147/FPC_mechanical/ENKU_R147_Display_FPC_Review_RU_EN.md). Source PCB unchanged, no new electrical CI claimed or required for this read-only study.
