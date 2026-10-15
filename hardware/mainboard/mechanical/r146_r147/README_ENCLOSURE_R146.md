# ENKU R146 - STEP reference for enclosure design

Модель для проектирования корпуса. Единицы - миллиметры. Основа - проверенный исходник R146; последующие локальные правки дорожек R147 сохраняют все положения компонентов, контур, отверстия и толщину платы.

## Что открывать

- `ENKU_R146_Enclosure_Reference.step` - плата и основные компоненты, отдельные именованные тела. Это основной файл для Fusion, SolidWorks, FreeCAD и другого CAD.
- `ENKU_R146_Bare_Board.step` - только плата с точным контуром, вырезом у антенны и всеми 25 реальными отверстиями/пазами посадочных мест. Мелкие переходные отверстия опущены.
- `ENKU_R146_Access_Zones_OPTIONAL.step` - отдельные рекомендательные объёмы для доступа к кнопкам/USB/microSD, движения карты/ползунка, шлейфа и проводов. Импортировать с сохранением координат. Это не установленные детали и не готовые вырезы корпуса.
- CSV - положения деталей, крепёжных отверстий и открытых сервисных контактов. JSON - источники, габариты, преобразования и результаты повторного импорта STEP.

## Размеры и координаты

Номинальная плата **59 x 101 x 1.6 мм**. Начало STEP соответствует KiCad X18/Y20: X направлен вправо, Y - к верхнему краю платы, Z - вверх. Нижняя поверхность Z0, верхняя Z1.6. Поэтому плата занимает X0..59 и Y-101..0. Нельзя зеркалить модель или переносить отдельные детали к собственным началам координат.

| Отверстие | X STEP, мм | Y STEP, мм | Диаметр, мм |
| --- | ---: | ---: | ---: |
| H1 | 11 | -2.5 | 2.2 |
| H2 | 39.5 | -5 | 2.2 |
| H3 | 5 | -96.5 | 2.2 |
| H4 | 54 | -96.5 | 2.2 |

Головки винтов, стойки, вставки и шайбы не смоделированы: их тип и диаметр нужно выбрать в корпусе и проверить по реальной плате и расположению компонентов.

## Важное для корпуса

- Боковые SW3/SW4 слева и SW5/SW6 справа: торцы толкателей находятся на 1.45 мм внутри края платы. Координаты осей вдоль платы Y-53 и Y-65. Номинальная высота кнопки над платой1.35 мм; ход по чертежу0.20 +0.2/-0.1 мм. Корпусной толкатель должен доходить внутрь, иметь ограничитель и не создавать постоянного нажатия.
- USB-C J5: плоскость сопряжения Y-101, центр X29/Z3.18. Номинальный наружный профиль8.94 x3.16 мм. Смоделирован по размерному чертежу GCT; внутренние контакты, штамповка и мелкие выступы упрощены. Размер окна и глубину стенки нужно проверить с выбранным кабелем.
- microSD J2: рот направлен к левому краю X0, плоскость рта X0.875. В дополнительных зонах есть номинальная карта в положениях фиксации, дожатия и выброса по чертежу Hirose. Проём должен обеспечивать доступ для извлечения.
- SW1: оранжевый **номинальный габарит с неподтверждённым положением корпуса относительно направляющих**. Нельзя финализировать прорезь ползунка по нему без образца/уточнённого чертежа. Широкая область толкателя обозначает суммарный номинальный резерв, не конкретную позицию фиксатора.
- SW2: внутренняя верхняя кнопка BOOT/RECOVERY, не пользовательская кнопка сброса. Доступ к ней необязателен, но полезен для обслуживания.
- J3: официальная модель Hirose с закрытой защёлкой. Реальная укладка ступенчатого шлейфа дисплея, плоскость дисплея и радиусы изгиба ещё требуют механической проверки.
- J1: жёлтый консервативный объём JST PH-2, включая область выводов; **это не детальная модель пластика и не подтверждённый максимальный допуск**. Предусмотрено место под ответный PHR-2 и провода, но конкретный жгут ещё не задан. Зарезервированная высота над платой5.5 мм.
- J7: только контактные площадки **на нижней стороне** и три направляющих отверстия. Установленного разъёма нет. В дополнительном STEP сервисный объём направлен вниз. J8 - верхние площадки для припайки проводов NTC.
- ESP32 и высокий L2 включены. L2 имеет номинальную высоту4.0 мм над платой; дополнительная зона учитывает размерный верхний предел4.2 мм. Остальные мелкие компоненты опущены по запросу: пустое место на изображении нельзя считать свободным для внутренних рёбер корпуса. Положения всех деталей доступны в исходнике KiCad и BOM.
- Аккумулятор, дисплей, крепления и корпусные толкатели не входят в модель платы. Необходимо добавить выбранные реальные детали перед проверкой замыкания корпуса. Не располагать металл, аккумулятор и проводящий пластик у антенны ESP32 без проверки RF.

## Источники и степень точности

Официальные STEP: Espressif ESP32-S3-WROOM-1, Hirose DM3AT-SF-PEJM5 и FH34SRJ-24S-0.5SH, E-Switch TL1016AAFxxxQG и TL3342FxxxQG. Геометрия вариантов силы нажатия одинакова; выбранные в BOM силы сохраняются. Преобразования выполнены по номинальным габаритам/выводам, не по центру произвольного bounding box: у microSD исходная система координат производителя удалена от детали.

USB, SW1, JST и индуктивности - явно названные номинальные реконструкции/резервы. Все производителя допускают допуски и посадку на припой; они не включены в один общий универсальный зазор. Для финальной механики назначить зазоры в зависимости от процесса корпуса и проверить образцы.

KiCad STEP-only экспортировал диэлектрическое тело толщиной1.51 мм. Точная плоская грань с исходными отверстиями аналитически выдавлена до полной номинальной толщины1.6 мм. Преобразование по Z не масштабирует XY, отверстия остаются цилиндрами. Проверены размеры, валидность тел, повторный импорт и точки внутри/снаружи четырёх крепёжных отверстий.

Исходник R146 SHA256: `89487b178c663ad0e0c2b5e574bd9727f27c19be9012936d6786e7813b9b76d1`.

## English handoff

Import the main assembly in millimetres and retain component placements. Board:59x101x1.6mm, origin at KiCad(18,20), CAD X=KiCadX-18, CAD Y=20-KiCadY, bottomZ0/topZ1.6. Mounting-hole positions are in the table above and CSV. All main bodies are separate and named. The optional access STEP uses the same origin and contains advisory reserves, not fitted parts or finished enclosure cutouts.

Hirose, E-Switch and Espressif parts use official manufacturer STEP. USB is a nominal GCT drawing reconstruction. SW1 has an unresolved body-to-locator datum: verify a sample before cutting its slot. JST PH-2 is a conservative nominal reserve rather than detailed supplier CAD. Side-button tips are1.45mm inboard; design inward-reaching pushers without preload. USB mating centre is(29,-101,3.18). microSD faces left. Tag-Connect contacts are on the bottom. J8 is hand-soldered top-side wire pads. No fitted dock connector exists in this Base revision.

Small passives, most ICs, battery, panel, screws, bosses and case pushers are omitted. Empty-looking regions may contain omitted electronics. Apply actual manufacturing/assembly/enclosure clearances and verify battery, harness, FPC bend, button travel, card ejection, USB cable and screw/boss volumes before finalising the enclosure. Nominal reference only; physical fit and prototype electrical tests have not been performed. Engineering review / NO FAB.

Primary sources:

- https://www.hirose.com/en/product/p/CL0609-0031-0-00
- https://www.hirose.com/en/product/p/CL0580-1255-6-50
- https://www.espressif.com/en/products/modules/esp32-s3
- https://www.e-switch.com/product/tl1016-series-subminiature-smt-right-angle-tactile-switch/?part-number=TL1016AAF160QG
- https://www.e-switch.com/product/tl3342-series-low-profile-smt-tactile-switch/?part-number=TL3342F160QG
- https://gct.co/files/drawings/usb4215.pdf
- https://www.jst-mfg.com/product/index.php?lang=2&series=199
- https://www.laird.com/sites/default/files/tys5040-series-datasheet.pdf
- https://cdn.semikey.com/upload/pdfs/a6/85/a685b04beffe80627230619bb0c8ae8e.pdf
