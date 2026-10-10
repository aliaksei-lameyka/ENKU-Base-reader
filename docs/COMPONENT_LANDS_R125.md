# R125 — производительские площадки Q1/Q2/U9 и монтажный аудит

Исправлены 11 физических площадок; все 417 исходных pad UUID, 2610 дорожек/vias, размещение компонентов, электрические цепи, RF keepouts и правила сохранены. Native KiCad 10.0.7: 0 opens, ERC 0, parity 0; 126 DRC = 106 library mismatch + 20 hole clearance. Исключения не добавлены.

| Компонент | R124 | Принято в R125 | Первичный источник |
| --- | --- | --- | --- |
| Q1 IRLML6346TRPBF | 1.0 × 0.8, межрядные центры 2.0 мм | .972 × .802, межрядные центры 1.770 мм | Infineon PD-97584A, 03/09/12, с.8: внешний размер 2.742 минус длина площадки .972; pitch 1.9 |
| Q2 AOS AO3401A | 1.0 × .8, межрядные центры 2.0 мм | .8 × .8, межрядные центры 2.4 мм | AOS SOT23 PO-00001 rev N; body nominal 1.6 × 2.9 |
| U9 TMUX1101DBVR | 1.325 × .6, межрядные центры 2.275 мм | 1.1 × .6, межрядные центры 2.6 мм, R .05 | TI DBV0005A 4214839/K 08/2024, PDF с.33 |

Пин-карты сохранены: Q1 1 G/EPD_GDR, 2 S/EPD_RESE, 3 D/EPD_SW; Q2 1 G/PWR_GATE, 2 S/VSYS, 3 D/SYS_EN; U9 1 D/BAT_ADC_SW, 2 S/VBAT, 3 GND, 4 SEL/3V3_SYS, 5 VDD/VBAT. Сигналы U9 проверены отдельно по TI top view и table5-1. Новые проектные библиотеки и source/cache/instance metadata согласованы; generic references не использованы как доказательство производителя.

[Нативная геометрия до/после](../hardware/mainboard/kicad/checks/component_lands_native_R125.png). [Рецепт изменений](../hardware/mainboard/kicad/checks/applied_component_lands_R125.json). [Источники и SHA256 скачанных PDF](../hardware/mainboard/kicad/checks/manufacturer_reference_manifest_R125.json).

U1 ESP32-S3 имеет девять отдельных .9 × .9 окон F.Paste, суммарно 7.29 мм², с pitch 1.4. Паста не наносится непосредственно на EP41 и его 12 тепловых отверстий .3 мм; номинальный зазор края окна пасты до отверстия .1 мм. GPIO35/36/37 зарезервированы под PSRAM N16R8 и остаются NC. Однако Cu EP41 — сплошной квадрат 3.9 × 3.9, в то время как Espressif v1.8 с.45 показывает девять медных островков с общим габаритом3.7. Это существующая адаптация KiCad с .3 вместо библиотечного .2 drill, **не квалификация производителя или сборки**. Требуются решение по заполнению/закрытию отверстий, mask, регистрации, толщине трафарета и утеканию припоя; глобальный минимум drill .3 не снижался.

J7: шесть контактных площадок .7874 имеют только B.Cu/B.Mask, без B.Paste; исключён из BOM. Требование Tag-Connect Rev B соблюдено, хотя отличие SMD/CONNECT attribute остаётся активным library mismatch. Foreign copper ≥.5348469 при требовании .508 мм. J5: все четыре shell pads S подключены к USB_SHIELD; одинаковый S в custom schematic/PCB не является перепутанной цепью. Нумерация SH в generic library требует документирования, guide-hole clearance остаётся открытым.

Только номинальные размеры трёх land patterns сверены с чертежами. Assembly, circuit thermal/bench qualification и вся плата остаются **NO FAB**. Два новых guard проверяют source-preservation и фактические mask/paste layers также на сервере; native/library совпадение не заменяет внешний чертёж.
