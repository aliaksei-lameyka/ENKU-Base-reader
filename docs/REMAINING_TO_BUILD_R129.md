# ENKU Base — осталось после R129

Закрыты26 library warnings,52 IC pins/nominal lands и обвязка, фактическая паста BQ/TPS, метка J7, полный native CPL. **Обрывы0/ERC0/parity0; DRC20=hole_clearance**. [Подробности R129](ACTIVE_IC_AND_ASSEMBLY_R129.md).

| Блок | Что требуется для завершения |
| --- | --- |
|20 отверстий,18 физических зазоров |16 кнопочных gaps0.075/0.150mm и4 USB findings по2 gaps0.1944mm. Контролируемые допуски и принятый изготовителем part-specific процесс/правило либо обоснованная новая посадка. Общее правило0.25mm активно. |
|SW1, дисплей/FPC и корпус |Утверждённый MK-12C03-G015 остаётся: common2/PWR_GATE,1/GND,3/NC, верхняя грань. Требуются согласованные A0/X1 datums/slide states. Для панели разрешить GDEY/GDEM,pin5VDHR/VSH2,контактную сторону и bend radius. Проверить механический fit USB/SD/кнопок/FPC/батареи/RF/крепежа. |
|MPN/BOM/CPL freeze |Заполнить12 MPN fields для J1,J2,J5,L1,L2,Q1,Q2,SW1,SW3–SW6 по уже принятым точным вариантам и контролируемым ordering codes. Принять origin/углы/полярности/стороны97 строк native CPL. Сборочная таблица явно содержит18 bare-PCB и2 DNP, они не входят в монтаж. |
|Монтажный процесс |Принять U1 tents/mask registration/stencil/voiding; общий stencil для BQ/TPS, transfer/reflow; CC-specific lands и плотные courtyards. Рекомендованные manufacturer examples не означают process signoff. |
|Stackup, питание и прототип |Factory4-layer90Ω stackup; Ceff под реальным bias/температурой/ageing, заряд/NTC/тепло, OFF/backfeed, USB inrush/hotplug/suspend/disconnect timing, HV overshoot/утечка/тепло иR37 repetitive pulse. Численные модели и связность уже защищены; гарантии и bench ещё открыты. |
|Единый production export |После закрытия активных ограничений — финальная Gerber/drill/assembly ревизия и визуальное сравнение с frozen source; затем прототипное питание/заряд/HV/display/sleep/кнопки/SD/USB MSC с эксклюзивным владением SD. |

Следующий автономный проход: оставшиеся MPN fields и механический/assembly freeze по имеющимся контролируемым чертежам. Внешние вопросы требуют действительных ответов; существующие gaps не исчезают от изменения текста отчёта. Сообщения, заказы и release не выполнялись. **fabrication_ready=false**. Часы: DEVELOPMENT_HOURS_READER.json; историческая общая сумма неизвестна.
