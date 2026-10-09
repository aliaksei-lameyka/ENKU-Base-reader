# ENKU Base — измеримая готовность к PCBWay (R48, 2026-10-09)

Ранее отображалось фиксированное **30%**, даже когда продвигались до R47: это был консервативный статус производства, а не обновляемый процент выполнения. С R48 **отдельно считаем инженерную готовность (балльная модель 100)** и бинарный статус **PCBWay Production GO/NO-GO**. Вероятность выпуска и дата заказа этим процентом не оцениваются.

## Весовая модель

| Категория | Вес | Готовность | Баллы | Основание |
|---|---:|---:|---:|---|
| Электрическая архитектура, ERC, питание | 15 | 90% | 13.50 | ERC0, VBUS, Power/SPI hardware; физическая квалификация впереди |
| Размещение, корпус и посадочные места | 15 | 60% | 9.00 | 132 footprint; выключатель/кнопки/FPC/механика требуют проверки |
| Физическая разводка, возвраты GND | 35 | 45% | 15.75 | 139 unconnected; USB D+/D− пока не разведен |
| Полный DRC, производственная разметка и pad audit | 15 | 20% | 3.00 | 168 нарушений против 224 R47; 130 library mismatch и 59 отличий геометрии |
| USB MSC — железо и ПО | 10 | 25% | 2.50 | SPI microSD и VBUS есть; нет USB-пары, прошивки и ПК тестов |
| Файлы PCBWay и первый физический образец | 10 | 0% | 0.00 | нет готового комплекта BOM/CPL/Gerber/NC-drill или образца |
| **R48 общая инженерная готовность** | **100** | — | **43.75** | округлённо **44%** |

R47 ретроспективно **43.00%** по той же методике: единственное изменение R48 — доказанное уменьшение DRC/шелкографии **224→168**, поэтому DRC/DFM категория теперь 20% вместо 15% (= +0.75 балла). **44% — прогресс разработки, не разрешение печатать/собирать плату.**

## Фактическая доказательная база

- [R48 Native KiCad 37898825797](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825797), **success**: строгий ERC 0 ошибок / 0 предупреждений; schematic parity 0; критические DRC shorts/hole/edge/track-via dangling 0; 139 unrouted, 168 других DRC вместо 224.
- [R48 Active Hardware Checks 37898825577](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37898825577), **success**: 132 footprints, all four GPIO/switches native-connected, SPI microSD, VBUS and PMOS power switch source topology, zero added via-in-SMD pad defects, probe labels/cathode markings preserved.
- R48 перенос **43 прямоугольных очертаний корпусов** с печатных F/B.SilkS на инженерные F/B.Fab: `silk_over_copper` **67→27**, `silk_overlap` **27→11**. Вместе **−56** проблем шелкографии и **0 изменений меди**. `text_height` остаётся 0 после R45.
- **130 footprint-library mismatch** остаются. Отдельный [Native footprint pad audit](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/37896089937) R47 показывает **73 совпавших площадочных геометрии**, **59 отличающихся**: 55 pad centers, 1 pad count, 1 pad numbering (USB-C), 2 pad size/shape/type. **130 предупреждений библиотеки не означает 130 однозначно неправильных компонентов**, но 59 отличий pad требуют проверки по оригинальным даташитам. Особенно ESP32-S3, USB-C, SOT-23, диоды, microSD, кнопки.

## Независимый релиз-гейт

**PCBWay Production GO: НЕТ.** Обязательны одновременно: *0 unconnected, полный Native DRC0, ERC0, схема↔PCB0, manufacturer-verified всех footprints, габаритов кнопок и case/FPC, письменный Good Display pin5 VDHR/VSH2 и ориентация FPC, физическая USB2 D+/D− с 90Ω для подтверждённого стека PCBWay, прошивка USB MSC и host copy/eject/reconnect, питание LiPo/NTC/PMOS, 3D/механика и результаты первого включения, актуальные Gerber/NC drills/approved BOM+CPL и DFM PCBWay*.

Не повышать оценку только за появление дорожек или зелёный **priority-only** CI; возможно уменьшение оценки после обнаруженного производственного дефекта.
