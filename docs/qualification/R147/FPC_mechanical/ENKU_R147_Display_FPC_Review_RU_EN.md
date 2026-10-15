# ENKU R147 - шлейф дисплея и разъём J3

**Вывод: длина в собранном виде, отсутствие давления и удобство подключения пока не подтверждены. Найден конкретный конфликт для прямой плоской укладки перед J3. Плата не изменена.**

Это механическая проверка R147 с PCB SHA256 `856e6d84905f978994316e2efcbb398184cf06dc4f95580c203ee244dd918bb2`. Успешные электрические проверки R147 сохраняются; они не удостоверяют механическую укладку шлейфа.

## Что установлено

1. **Вход J3 обращён в сторону увеличения KiCad Y, то есть вниз платы.** Чтобы вставить шлейф, его свободный конец нужно подвести снизу разъёма и двигать вверх. Это проверено по чертежу и проходному каналу официального STEP Hirose, а не по обозначению на шелкографии. Плоскость входа примерно KiCad Y35.8 мм, центр разъёма X69.27/Y34 мм.
2. Перед входом расположены **C24, C29 и C30**. Максимальные габариты их корпусов начинаются примерно в2.1 мм от входа. Корпуса пересекают в плане прямой коридор шириной12.5 мм. По актуальным спецификациям точных Yageo MPN их номинальная высота1.25 мм, размерный верхний предел1.45 мм, без добавления толщины припоя.
3. Плоский гибкий участок на уровне входа J3 проходит примерно на0.5 мм над верхом платы. Расчётный контрпример с толщиной0.1 мм пересекает номинальные тела всех трёх конденсаторов по0.25 мм³; на более длинном прямом участке пересекается и край L2. Это **не модель фактического согнутого шлейфа**. Результат доказывает, что оставлять такой прямой путь нельзя; он не доказывает невозможность всех других укладок.
4. В исходном упрощённом STEP эти мелкие конденсаторы были опущены по первоначальному запросу. Поэтому тот STEP подтверждает контур и размещение основных деталей, **но не отсутствие давления на шлейф**. Файл `ENKU_R147_J3_Critical_Caps_AddOn.step` добавляет C24/C29/C30/C28 в тех же координатах.
5. Отдельный риск - доступ к задней защёлке Hirose. Закрытая модель не воспроизводит пространство для её открытия и инструмента при уже установленном дисплее. Последовательность сборки должна позволять вставить шлейф, закрыть защёлку и установить плату без натяжения.

## Длина и изгиб

В оригинальном PDF GDEY0397T81P указана плоская проекция шлейфа **33.66 +/-0.30 мм**. Это не гарантированная доступная длина между точками собранного устройства: хвост ступенчатый, есть усилитель, зона склейки/бондинга и отмеченные места изгиба.

Феликс в письме10.10.2026 подтвердил радиус1-1.5 мм и рекомендовал отступ от стекла не менее2 мм. Для нашей проверки принят консервативный радиус не менее1.5 мм. В том письме нет утверждённой позы нашего разъёма относительно дисплея и нет подтверждения, что шлейф дотягивается именно до J3 на плате ENKU.

Для варианта, где шлейф огибает верхний торец дисплея и возвращается вдоль платы вниз, текущий вход J3 требует отдельно решить разворот свободного конца: простая однократная отгибка не даёт автоматически нужного направления входа. Положение панели, сторона контактов, pin1 и развернутая длина должны проверяться совместно. Нельзя делать вывод о запасе длины простым вычитанием расстояния между XY-точками из33.66 мм.

Поставщик прислал CAD с именем GDEM0397T81P, PDF выбранного изделия называется GDEY0397T81P. Номинальные размеры стекла56.24x96.62x0.92 мм и проекция хвоста совпадают, но тождество исполнения и лицевая/оборотная регистрация ещё не подтверждены как производственная спецификация.

## Почему старая модель корпуса не закрывает вопрос

Проверен сохранённый `ENKU_R142_Compact_R04_USB_SD_Fusion.zip`, Library ID `libfile_ac0b3aa21c6c819192501e41c960eeca`. В его сборке только рама, передняя/задняя панели и голая PCB. Дисплея, шлейфа и корпусов электронных компонентов нет. Это прямо указано в README и подтверждается составом STEP.

Пилотные крепления R04 также отличаются от текущей платы:

| Отверстие | R04, KiCad X/Y мм | R147, KiCad X/Y мм |
| --- | --- | --- |
| H1 |31 /22.5 |29 /22.5 |
| H2 |57.5 /22 |57.5 /25 |
| H3 |23 /119.5 |23 /116.5 |
| H4 |72 /119.5 |72 /116.5 |

По этой сборке нельзя подтверждать отсутствие столкновений с дисплеем. Её положения и оси не следует автоматически переносить на R147. Целевой корпус около10 мм остаётся целью, а не результатом проверки полного стека.

## Что нужно исправить до финализации

- Сначала зарегистрировать реальную панель, её активное окно, сторону просмотра и выход FPC относительно текущей платы и корпуса.
- Сравнить разворот J3 и/или его перенос ближе к естественному концу шлейфа. Критерий - короткий ненагруженный путь без прохода по конденсаторам/дросселю и с доступной защёлкой. Координаты нового положения этим отчётом не утверждаются.
- Зарезервировать коридор шлейфа в трёх измерениях. Включить усилитель и склейку; не назначать изгиб внутри них. Проверить длину по развёртке, радиус, запас и pin1 после сгибов.
- Проверить оба состояния защёлки и последовательность сборки. Шлейф должен лежать свободно и не выпрямляться усилием стенки/крышки корпуса.
- После выбора положения J3 и коррекции соседних компонентов выполнить необходимую переразводку и повторные электрические/производственные проверки. Затем подтвердить отсутствие натяжения и давления на физическом макете.

**Механический статус J3: HOLD.** Это фактическая незакрытая задача; не следует заменять её положительным результатом DRC или наличием STEP.

## Файлы и пределы модели

- `ENKU_R147_J3_FPC_Risk_Map.png` - фактическое расположение J3 и компонентов, направление входа и сечение прямого конфликтующего пути.
- `ENKU_R147_J3_Critical_Caps_AddOn.step` - четыре отдельных именованных тела по размерным верхним пределам Yageo. Импортировать без переноса начала координат поверх основной модели платы. Это прямоугольные габариты компонентов, а не точный CAD керамики; припой и зазор до шлейфа не добавлены.
- `J3_FPC_Analysis_R147.json` - расчёт, источники координат и объёмные контрпримеры. Полная укладка панели не моделировалась как подтверждённая.

Начало STEP совпадает с предыдущей моделью: X=KiCadX-18, Y=20-KiCadY, низ PCB Z0, верх Z1.6. Дополнение не содержит дисплея или выдуманного окончательного шлейфа.

## English handoff

**R147 FPC reach, no-pressure fit and latch accessibility are NOT qualified.** The Hirose J3 mouth faces +KiCadY; insert from below toward -Y. C24/C29/C30 occupy the straight12.5mm cable corridor starting about2.1mm beyond the mouth at their dimensional upper envelope. Exact Yageo MPN height is1.25+/-0.2mm. A flat0.1mm flex counterexample at0.5mm above the PCB intersects each nominal capacitor body; the longer corridor also clips L2. This is not the actual folded-flex pose and does not prove that every alternative is impossible.

The earlier simplified board STEP omitted these small capacitors. The supplemental STEP adds their upper dimension envelopes at the same origin. No PCB edit, latch-access clearance, solder allowance, folded panel model or physical fit approval is implied.

Good Display's33.66+/-0.30mm dimension is a flat projection. Felix confirmed radius1-1.5mm and at least2mm clearance from glass on10Oct; these are not an endorsement of ENKU's connector position. The saved R04 case contains a bare PCB only and has obsolete trial mounting-hole positions. Register the real panel, evaluate J3 orientation/position and a component-free cable corridor, preserve stiffener/bond zones, check developed length and pin1 after folding, then reroute/recheck as needed. Physical assembly must close without cable preload.

Primary source records:

- Good Display original panel PDF SHA256 `e28ea298457108bb3431b8c4de065834f62390b6caf2dc58e216d134fe559dbc`, p5.
- Vendor CAD STEP SHA256 `abcd05c962518c00da961538da74f4d8f15b67bd0b51fc20b4905636ba884036`.
- Felix email10Oct2026, Gmail message `1a1244f1a3c71a96`, thread `1a11c1721b3a3a9e`, read from aliaksei.lameyka account.
- https://www.hirose.com/en/product/p/CL0580-1255-6-50 - exact manufacturer STEP and EDC-159714-50 p1 connector section.
- https://yageogroup.com/download/specsheet/CC0805KKX7R8BB475 - C24/C28/C29, dimensions p1.
- https://yageogroup.com/download/specsheet/CC0805KKX7R8BB105 - C30, dimensions p1.
- Laird TYS5040 manufacturer RevA p2, already retained in the main CAD provenance.

Original supplier CAD/PDFs and email are kept private; no distribution permission inferred. Physical prototype tests NOT RUN.

Recorded active review interval: 0.236h. Project measured lower bound: 28.848h. Earlier idle periods excluded.

Current review files:

- [ENKU_R147_J3_FPC_Risk_Map.png](https://chatgpt.com/api/library/files/libfile_f0b306b9172c8191b65a4aab6650047a/download)
- [ENKU_R147_J3_Critical_Caps_AddOn.step](https://chatgpt.com/api/library/files/libfile_ec68a6c3cb1881918da52dff0ab54b3c/download)
- [ENKU_R147_Display_FPC_Review_RU_EN.md](https://chatgpt.com/api/library/files/libfile_e48cd53162248191890b158ab5752038/download)
