# ENKU Base Reader — PCBWay Readiness R48

**Инженерная готовность: 44%** (43.75 / 100 по [новой взвешенной модели](PCBWAY_SCORE_R48.md)). **Готовность к заказу PCBWay: NO-GO.**

**Ветка:** `engineering/r48-silkscreen-fab-clearance`. **Актуальная KiCad PCB:** `hardware/mainboard/kicad/enku-mainboard-r2.5-base-silk-fab-outlines.kicad_pcb`. Электрическая сеть не менялась с R47: 132 посадочных места, **515 сегментов дорожек**, **132 vias**, **2 внутренних GND-полигона**.

## Проверено на реальном KiCad 8 CI

- [Native R48 — 37898825797](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825797): **SUCCESS**; ERC 0/0, PCB↔схема 0, приоритетные критические DRC 0, **139 unconnected**, **168 прочих DRC**.
- [Active Hardware R48 — 37898825577](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825577): **SUCCESS**; согласование 132 footprints, сверка pad/drill, microSD SPI, безопасного обнаружения VBUS, всех 4 боковых GPIO, аппаратного выключателя, контроль обозначений тестпоинтов.
- Печатная шелкография: **94→38** (silk_over_copper 67→27; silk_overlap 27→11), 43 пересекающих площадки контуров перенесены в Fab, все каталожные обозначения и 14 TP сохранены. **56 исправленных DRC без касания электрической платы**.
- Остаются **130 lib_footprint_mismatch + 27 silk_over_copper + 11 silk_overlap = 168**. Все предупреждения требуют явного разрешения; Native success означает, что *критический gate* пройден, но **FULL DRC НЕ ПРОЙДЕН**.
- Native-диагностика pad по библиотекам: **59 из 132** имеют pad-геометрию не как у установленного библиотечного образца. Это не доказательство 59 неисправных компонентов; производственные MPN чертежи обязательно сверить до сборки.

## Следующий этап

**R49:** оставшаяся видимая шелкография и исследование семейств отклонений посадочных мест, затем продолжить 139 неразведённых участков питания, EPD и USB. Не заменять автоматически footprints по стандартной библиотеке: корпус/полярность/форма контактов могут отличаться по заказанному MPN.

**Стоп-факторы:** спорный Good Display GDEY0397T81P контакт5 VDHR/VSH2, точная укладка ступенчатого FPC, размер боковых кнопок/slide и корпус, USB-C D+/D− и 90Ω stackup PCBWay, USB MSC прошивка с FAT lock и Windows/macOS/Linux, заряд LiPo/NTC/PMOS и EMI, полная механика, BOM/CPL/Gerbers/Drills/DFM.
