# ENKU R148 - FPC approach and low profile battery / RU + EN

Engineering candidate, NO FAB. Source commit `bec2966be64cd6fdce5b1060f05179370ff0da77`; PCB SHA256 `bb0aa41324b73ec13c087ab1c669c57c6bc6fd449621bf3aa34a53d3901b9476`.
[Source branch](https://github.com/aliaksei-lameyka/ENKU-Base-reader/tree/engineering/r148-mechanical-review) / [actual successful server verification](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38776369871).

## Русский

R148 освобождает перед J3 локальный коридор шириной14.0 и длиной10.7мм: KiCad X62.27..76.27,Y35.80..46.50. По нативным габаритным зонам других деталей пересечений нет; переходы в этой области закрыты маской спереди. Это проверка локального подхода, не подтверждение длины, направления контактов или полного перегиба настоящего шлейфа.

Принята заданная архитектура: **задняя сторона дисплея обращена к B.Cu платы; шлейф огибает плату и подключается на стороне компонентов**. Положение J3 пока сохранено: X69.27,Y34.00,угол0; вход со стороны +Y, вставка в сторону -Y. Pin1 справа в виде платы сверху, pin24 слева. При физическом перевороте панели её вид относительно платы меняется: нельзя совмещать две фронтальные проекции как одну сторону. До утверждения полной укладки может потребоваться перенос самого J3. Освобождённый коридор не закрывает этот вопрос.

Из подхода убраны C24,C29,C30,R38; связанная силовая группа e-paper перенесена и переразведена. L2,D1,Q1,C25,D3,C31 и токовый резистор R37 проверены вместе. Высоковольтные номиналы, MPN и карта24контактов J3 сохранены. Два старых соединения с общей землёй не скрыты допуском: независимый контроль выявил переход под новой площадкой R38, затем его размещение/подвод исправлены.

**Батарея:** высокий JST PH снят. J1 теперь две исходные площадки с прежней полярностью: pin1=VBAT+, центр(66.95,95.50); pin2=GND-,центр(66.95,93.50). Глобальный размер каждой медной площадки3.50x1.00мм, шаг2.00мм; пасты и покупного разъёма нет. J1 исключён из монтажной BOM/CPL. Есть обозначения полярности. Для пайки и проводов в STEP выделен отдельный предварительный резерв до1.2мм над платой, при целевом наружном диаметре изоляции до0.8мм; это допущение для проектирования, не измеренная высота готового жгута.

Разгрузка проводов - **прижим изоляции корпусом сверху платы**, в KiCad X70.8..76.0,Y92.2..96.8. Сквозная стяжка под дисплеем не предусмотрена. Геометрия и высота самого прижима, усилие, выбранный провод и качество пайки требуют проверки образца. Аккумулятор по-прежнему должен иметь PCM; отдельный датчик температуры10кОм/B3435, закреплённый на ячейке, подключается через J8. Электрическая схема зарядки и защиты не менялась. Замена аккумулятора при таком исполнении потребует отпаивания проводов.

Сравнены низкие разъёмы: JST ACHL1.2мм/2А приAWG28 (BM02B-ACHLKS-GAN-ETF +ACHLR-02V-S), JST ACH1.4мм/2А и Molex7817100021.55мм/1.5А. Они требуют собственного посадочного места и соответствующего жгута. В R148 выбран разрешённый вариант пайки проводов, без корпуса коннектора. Наличие у поставщиков не проверялось.

**Проверки:** DRC0,ERC0,обрывов0,расхождений схемы/платы0. Независимый Gerber-граф84цепей, контроль всех4медных слоёв,11файловGerber,сверка Excellon/IPC/BOM/CPL/маски/пасты, OEM-геометрия, питание/старт/NTC/USB/SD/IMU, антенная зона и возвратные пути быстрых сигналов прошли. Проверки с внесёнными обрывами, замыканиями, переполюсовкой батареи и препятствием в коридоре обнаруживают ошибки. Проверены именованные/включённые слои и скрытые поля; проводящих графических объектов без net-семантики нет. Все6запросов fill/cap сохранены без объявления заводского согласования.

141позиция,471площадка,389переходов.119монтируемых деталей сверху,20элементов голой платы, R67/R99=DNP. Изменения меди ограничены97удалёнными и235новыми объектами; остальная медь, USB, контур и крепёж сохранены строгим сравнением с R147. Исторические эталоны не переписаны.

**STEP:** точный контур59x101x1.60мм,4крепёжных отверстия2.20мм и25реальных отверстий корпуса платы. Номинальная полная толщина восстановлена из нативной геометрии диэлектрика1.51мм. Отверстия389переходов в упрощённом корпусном STEP опущены. Включены OEM-модели ESP32/Hirose/E-Switch, номинальные USB/SW1, дроссели и критические мелкие детали вокруг e-paper. Часть тел - явно названные габаритные модели. Пластикового J1 нет. Плата, размеры отверстий и конечный STEP проверены обратным импортом. Дисплей, реальный согнутый FPC, батарея и окончательный корпус в основной STEP не включены; это не полный монтажный макет.

Координаты STEP: X=KiCadX-18,Y=20-KiCadY; низ платыZ0,верхZ1.6. Отдельный OPTIONAL STEP содержит резервы доступа/кнопок/прижима, его не надо объединять с платой как материал.

PDF: первые4страницы - реальные слои меди; страницы5/6 - бумажные шаблоны платы и исходного плоского контура панели **1:1**. Печатать100%, без Fit/Shrink, проверить линейку50мм. Собрать печатные стороны наружу, спинки вместе, с прокладкой1.6мм для платы. Сверить сторону и контакт1 по исходному чертежу панели. Радиус>=1.5мм, отступ изгиба от стекла>=2мм; усилитель и бондинг не гнуть, заводские метки сгиба сохранять. Шаблон помогает найти механическую ошибку до изготовления, но не заменяет реальную панель/защёлку.

**Открыто:** полная зарегистрированная укладка ступенчатого шлейфа, запас длины, pin1 после сгибов, доступ и ход защёлки, отсутствие давления при закрытии, изоляция/опора между B.Cu и дисплеем, точное соответствие CAD GDEM выбранной GDEY панели, допуск толщины FPC0.30+/-0.05 против Hirose0.30+/-0.03, прижим жгута, батарея и окончательный стек корпуса. Физические/тепловые/электрические тесты образца НЕ ПРОВОДИЛИСЬ. Производственный выпуск, закупка и заказ в PCBWay не утверждены.

## English

R148 clears a **14.0x10.7mm local front approach** to J3 at KiCad X62.27..76.27,Y35.80..46.50. No other front component courtyard intersects that rectangle; vias in it are front tented. This is a local clearance result, not qualification of the actual stepped cable's reach, contact orientation, fold or enclosure closure.

The architecture is fixed as requested: the display back faces the PCB back/B.Cu; the flex wraps the board edge and plugs into the component side. J3 remains at(69.27,34.00),0deg,opening toward+Y and insertion toward-Y; pin1 is on the right in the PCB front view. Physically flipping the display changes its projected handedness relative to the board. The actual complete fold may still require moving J3. Two front-view drawings must not be treated as one assembled view.

Eleven parts in the e-paper group move; values, MPNs, panel pin mapping and electrical topology remain unchanged. The boost group is rerouted together, including its switch, input bypass, rectifiers and sense resistor. An independent via-to-SMD check caught a same-net via under relocated R38 and the placement/routing was repaired.

J1 becomes **two original bare battery wire lands**, no housing and no paste: pin1 VBAT+ at(66.95,95.50),pin2 GND- at(66.95,93.50); global copper3.50x1.00mm each,2.00mm pitch. It is excluded from fitted BOM/CPL. Polarity is marked. An optional<=1.2mm-above-board wire/fillet/clamp reserve assumes wire insulation OD<=0.8mm; it is a design allowance, not a selected or qualified harness. Clamp insulation to the case above the PCB in X70.8..76.0,Y92.2..96.8. Do not put rear lacing against the display. A protected PCM pack and separate cell-bonded10k/B3435 NTC on J8 remain required. Battery replacement requires desoldering in this version.

Low profile options compared: JST ACHL1.2mm/2A atAWG28 (BM02B-ACHLKS-GAN-ETF with ACHLR-02V-S), JST ACH1.4mm/2A and Molex7817100021.55mm/1.5A. Each needs its own lands and matching harness. R148 implements the user-authorized soldered-wire option; supplier availability was not checked.

Full local verification passed before the interruption. The actual [server run](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38776369871) for source `bec2966be64cd6fdce5b1060f05179370ff0da77` also passes. All70published source files were recovered byte-exact against their manifest; the server artifact SHA256 is `1240397f32171c8ce9b7c9ce9f737b8bf50b591f01626c6adace6da53bc59953`. Its native and independent checks include DRC/ERC/opens/parity0,84-net independent Gerber connectivity, effective injected opens/shorts, all4copper layers,11Gerbers, drill/IPC/BOM/CPL/mask/paste, OEM lands/pinout, power/startup/temperature, USB/SD/IMU, RF keepout and fast return geometry. Hidden fields/layers are inventoried; no netless conductive graphics are present. The6explicit unapproved fill/cap requests remain.

141references,471pads,389vias;119fitted top parts,20bare-PCB items and R67/R99 DNP. Strict R147 comparison permits exactly97removed and235new copper objects; other copper, USB, outline, mounts and topology are preserved. Historical checks/goldens remain unchanged.

The updated named-body STEP has the exact59x101x1.6mm contour,4mounting holes of2.2mm and25native component/board holes.389via holes are omitted for enclosure use. It retains aligned OEM major-component CAD and adds critical e-paper passive/package envelopes; no installed J1 housing remains. Source geometry, hole probes and STEP re-import pass. USB and SW1 are nominal drawing/envelope models; SW1 datum remains unqualified. The main STEP omits the display, actual folded flex, battery and finished enclosure. Datum: X=KiCadX-18,Y=20-KiCadY,bottomZ0,topZ1.6. Optional access zones are separate reserves, not material to fuse into the board.

PDF pages1-4 show actual copper; pages5-6 are1:1paper trial templates for the board and supplier flat panel outline. Print at100%with scaling disabled and verify the50mm ruler. Put paper backs together and use1.6mm board thickness. Preserve actual allowed folds/bond regions and stiffener; radius>=1.5mm and glass-to-bend>=2mm. Match contact1 to the original drawing. Paper is a geometry aid, not cable-thickness, retention or physical-fit qualification.

**HOLD / NO FAB:** registered whole stepped-flex fold, reach/pin1, latch sweep/tool access, pressure-free closure, rear insulating/support interface, GDEM/GDEY production identity, FPC thickness tolerance0.30+/-0.05 versus Hirose0.30+/-0.03, actual wire/clamp/pack and complete enclosure stack. No physical, thermal, firmware or startup tests have run on a prototype; no factory process acceptance or production order is implied.

## Placement changes / перемещения

| Ref | Previous X/Y mm | R148 X/Y mm | Angle |
| --- | --- | --- | --- |
| C24 | [68.9, 39.0] | [59.3, 39.0] | 90.0 deg |
| C29 | [64.0, 39.0] | [64.0, 24.0] | 90.0 deg |
| C30 | [66.0, 39.0] | [66.0, 24.0] | 90.0 deg |
| C31 | [56.5, 44.2] | [48.2, 40.0] | 90.0 deg |
| L2 | [61.5, 44.2] | [52.5, 44.2] | 0.0 deg |
| D1 | [66.8, 43.2] | [57.8, 43.2] | -90.0 deg |
| Q1 | [67.0, 48.0] | [58.0, 48.0] | 0.0 deg |
| R37 | [65.5, 51.8] | [55.0, 50.5] | -90.0 deg |
| C25 | [67.8, 52.0] | [58.8, 52.0] | -90.0 deg |
| D3 | [71.3, 52.9] | [62.3, 52.9] | 0.0 deg |
| R38 | [72.0, 41.5] | [59.7, 35.5] | 0.0 deg |

## Primary sources

- [JST ACHL](https://www.jst-mfg.com/product/index.php?lang=2&series=563)
- [JST ACH](https://www.jst-mfg.com/product/index.php?lang=2&series=9)
- [Molex781710002](https://www.molex.com/en-us/products/part-detail/781710002)
- [Hirose FH34SRJ-24S-0.5SH(50)](https://www.hirose.com/en/product/p/CL0580-1255-6-50)
- Private supplied GDEY0397T81P PDF p5 and GDEM0397T81P STEP; originals are not redistributed publicly. Supplier bend/pin5 confirmations dated10Oct2026 remain retained in project history.
