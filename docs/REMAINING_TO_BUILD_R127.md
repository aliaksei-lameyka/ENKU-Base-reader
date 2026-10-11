# ENKU Base — остаток после R127

R127 закрепила оставшиеся18 пассивов иисправила входную ёмкость USB C4. Теперь все32 caps/43 resistors имеют точныеMPN иnative geometry/metadata guards. **opens0/ERC0/parity0; DRC47=27library+20holes**. [Изменения ичисленная проверка](COMPONENT_POWER_PASS_R127.md).

## Следующий инженерный проход

1. Закрыть **U1 EP/stencil/via process**: сплошнойEP3.9²,12 thermal holesØ0.3 сlandØ0.6,9 paste apertures0.9² и0.1mm nominal gap. Manufacturer copper islands не воспроизведены; нужен конкретный монтажный процесс/mask/wicking.
2. Разобрать20 hole-clearance findings TL3340/USB4105 по контролируемым чертежам иконкретному процессу изготовителя. Правило0.25mm иисключения не ослаблять. SW1 MK-12C03-G015 — тот же утверждённый suffix, common2/upper edge; получить полныйA0/X1 drawing, не выбирать заново.
3. ДляCeff закрыть гарантированный минимум, ане типовую симуляцию: C9 DC-retention минимум58.10% всценарии; C11+C12 минимум26.00%.10% ageing reserve — предположение. EPD exactpanel requirements идифференциальныйC25 stress неизвестны. ДляR37 теперь точныйCRCW08052R20FKEAHP, но Ipeak/ti/duty/film-temperature иrepeat-pulse/voltage signoff открыты.
4. USB: directcap nominal6.8uF, условный passive decay6.215ms. Нужны whole-device inrush/hotplug/backfeed/suspend/charging policy, threshold-crossing/firmware timing иfactory90Ω stackup. Исторический1.085ms иописание unrouted pair/TPS2121/Dock удалены из текущего USB contract.

## До выпуска платы

| Открытая задача | Критерий закрытия |
| --- | --- |
| SW1 MK-12C03-G015, A0/X1 | Контролируемый полный чертёж точного suffix, datums, 3 контакта, 4 лапки, 2 locator holes и ход; подтверждены общий2/замыкание1–2 и посадка в корпусе. Утверждённый выключатель заново не выбирать. |
| TL3340 и USB4105 отверстия | Закрыты 16 замечаний кнопок (0.075/0.150 mm) и 4 USB (~0.1944 mm) при действующем правиле0.25 mm. Исправленная геометрия либо конкретное документированное правило изготовителя; без общего ослабления правил/исключений. |
| Остальные библиотечные предупреждения | 24 имеют равные сравниваемые pad properties, 1 — U1 pad/drill, 2 — J5 numbering/J7 attributes. Равные площадки не доказывают MPN, model, graphics или полный assembly fit; завершить разбор каждого предупреждения. J5 S→USB_SHIELD и J7 no-paste уже проверяются независимо. |
| MLCC/диоды/пассивы | CC-specific assembly lands и плотные0.10 mm courtyards согласованы с процессом; worst-case capacitance закрыта по exactMPN,ageing иDC/AC bias; HV overshoot/diode leakage/тепло, resistor pulse/derating приняты. Все32caps/43R имеют точныеMPN; численныйR127 сценарий не заменяет гарантий иизмерений. |
| Точная панель Base / 24-pin FPC | Однозначны GDEY/GDEM, pin5 VDHR/VSH2, стороны контактов, ориентация, координаты и численный радиус перегиба. Ответ от2026-10-09 этих вопросов полностью не закрыл. |
| Заводской stackup / USB90Ω | Реальный четырёхслойный stackup и width/gap/vias/USB-C branches согласованы. Непрерывность заполненной GND уже проходит; impedance/bench ещё открыты. |
| Корпус и монтаж | Проверены кнопки/SW1, SD/USB/FPC, батарея, RF keepout, screw heads, высоты и 3D, полярности/marking, mask/paste/courtyard. Новые локальные footprints не означают готовых контролируемых 3D моделей. |
| Freeze / manufacturing package | Все активные DRC и assembly ограничения закрыты; полный BOM с точными MPN/DNP и CPL со сторонами/углами сверены. Gerber/drill/stackup/assembly экспортированы из единственной принятой ревизии и визуально проверены. |

Вопросы по внешним чертежам уже подготовлены в [SUPPLIER_QUESTIONS_R124.md](SUPPLIER_QUESTIONS_R124.md); сообщения и заказы не отправлялись. Base59×101, четыре кнопки, без Hall/frontlight/Qi/Pogo/Dock; Pro — отдельная плата.

После прототипа: OFF/backfeed, charge/thermal, VBUS hotplug/suspend, HV/display power/sleep, кнопки/SD и USB MSC с эксклюзивным владением SD и безопасным возвратом reader filesystem. USB Base работает при включённом reader.

**fabrication_ready=false.** Историческая сумма часов неизвестна; подтверждённые интервалы — DEVELOPMENT_HOURS_READER.json.
