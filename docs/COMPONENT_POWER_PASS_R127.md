# ENKU Base — R127: все пассивы и численная проверка питания

R127 продолжает принятую R126 с PCB SHA256 `8deaaa605264ce3119da6aae8e7a8a837cb9e781caa45e3348738eeb13585393`.
Новый источник PCB SHA256 `c2316fa909debdd69577cd565b04bab6e40db01acbfc9c2b6f1362ac4b14b1f2`.
Native KiCad10.0.7: **opens0 / ERC0 / parity0 / DRC47 =27 library mismatch +20 hole clearance**. Все остальные типы native DRC —0; правила и исключения сохранены.

## Изменённые компоненты

Закреплены оставшиеся15 конденсаторов и3 специальных резистора. Дополнительно исправлен C4. Теперь независимая проверка сверяет **все32 конденсатора,43 резистора,3 диода иSW2 —79 точных MPN** в native XML netlist и фактических PCB fields. Номиналы R70/R71/R37, R12/R67 DNP и пять вариантов0R/22R сохранены.

| Ref | Точный MPN | Value | Локальная библиотека |
| --- | --- | --- | --- |
| C4 | CC0805KKX7R8BB105 | 1uF 25V | C_CC0805_YAGEO_REFLOW_TRANSFER |
| C14 | CC0603KRX7R9BB104 | 100nF | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C15 | CC0603KRX7R8BB105 | 1uF | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C16 | CC0805KKX5R6BB106 | 10uF 10V | C_CC0805_YAGEO_REFLOW_TRANSFER |
| C17 | CC0603KRX7R9BB104 | 100nF | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C18 | CC0603KRX7R9BB104 | 100nF | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C19 | CC0603KRX7R9BB104 | 100nF | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C21 | CC0603KRX7R9BB104 | 100nF | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C22 | CC0603KRX7R8BB105 | 1uF 25V | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C23 | CC0603KRX7R8BB105 | 1uF 25V | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C27 | CC0805KKX7R8BB475 | 4.7uF 25V | C_CC0805_YAGEO_REFLOW_TRANSFER |
| C28 | CC0805KKX7R8BB475 | 4.7uF 25V | C_CC0805_YAGEO_REFLOW_TRANSFER |
| C29 | CC0805KKX7R8BB475 | 4.7uF 25V | C_CC0805_YAGEO_REFLOW_TRANSFER |
| C30 | CC0805KKX7R8BB105 | 1uF 25V X7R | C_CC0805_YAGEO_REFLOW_TRANSFER |
| C38 | CC0603KRX7R9BB104 | 100nF 10V | C_CC0603_YAGEO_REFLOW_TRANSFER |
| C39 | CC0603JRNPO9BN102 | 1nF C0G 10V | C_CC0603_YAGEO_REFLOW_TRANSFER |
| R37 | CRCW08052R20FKEAHP | 2.2R 1% 0805 | R_CRCW0805_HP_VISHAY_REFLOW |
| R70 | RT0603BRD0726K7L | 26.7k 0.1% 25ppm | R_RT0603_YAGEO_REFLOW |
| R71 | RT0603BRD0710KL | 10k 0.1% 25ppm | R_RT0603_YAGEO_REFLOW |

C4 изменён с10uF10V X5R на1uF25V X7R **CC0805KKX7R8BB105**. Native netlist перечисляет C2/C4/C5/C6 напрямую между VBUS_USB иGND: ранее15.8uF, теперь6.8uF. Предыдущий избыток номинальной входной ёмкости убран; TI SLVA129 p1 объясняет10uF USB input limit. BQ25185 SLUSF65B p21 требует >1uF после derating и рекомендует25V для IN/SYS. C5 остаётся4.7uF25V. Это обоснованная корректировка прежнего MPN C4, а не замена ради унификации. **Реальные inrush, напряжение и питание при hotplug ещё не квалифицированы.**

## Физические изменения

- RT0603: Yageo mounting v10 p4/Table1, lands0.9×0.8mm, centre pitch1.7mm. ТочныеRT sheets подтверждают1.6×0.8mm body,0.1%,25ppm/K,P70=0.1W. Это тонкоплёночныеRT, а не общие1%RC.
- R37: Vishay CRCW-HP e3 doc20043 rev17-Mar-2026 p9, reflow G1.00/Y0.95/X1.45/Z2.90: lands0.95×1.45mm, centre pitch1.95mm. КодF=1%,K=100ppm/K,EA=5000 tape,HP=pulse proof; P70=0.5W (p1–3).
- CC0603:0.8×0.9mm / pitch1.5mm; CC0805:0.95×1.4mm / pitch1.85mm. Сохраняется **инженерный перенос** размерной YageoAC рекомендации v4 p18/Table14 на проверенные размерыCC; это не CC-specific assembly approval. В том числе C0G C39 подтверждён точнымNPO sheet, но его монтажный процесс отдельно не квалифицирован.
- Все19 FP centres/angles сохранены.38 площадок объявлены,36 физически изменены; уC4 те же lands. Все417 padUUID/net identities сохранены. Корректных до прохода осей не переориентировали произвольно.
- УC27 расширенная GND land дала0.1772mm до EPD_VCI via при правиле0.20. Вершина via(50.1,32.45) перенесена в(50.2,32.4) вместе сдвумя attached segments. Это **три** явно объявленных изменения; новых Cu items нет. Все2639 старых tracks/vias UUID,net,layer,width,drill сохранены, вся остальная медь неизменна.
- Независимый audit91 новых/перенесённых vias сR120: annulus-to-land>=0.1mm. J7 чужая B.Cu/via медь>=0.5348469mm при требовании0.508. USB данные и фактический заполненный GND reference прошли прежние guards.

Четыре native Cu/F.Fab/F.CrtYd crop просмотрены, centres всех19 изменений покрыты. Это nominal geometry review, без полного3D/маркировки/монтажного signoff.27 library warnings:24 с равными сравниваемыми pad properties,1 U1 pad/drill,2 J5 numbering/J7 attribute.20 hole warnings оставлены активными.

## Численная проверка

[Машинный отчёт](../hardware/mainboard/kicad/checks/power_budget_audit_R127.json) вычисляется по **всем32 native capacitor net nodes иMPN**; тот же guard включён вCI. Следующие цифры — сценарий tolerance × temperature retention0.85 × ageing reserve0.90.10% ageing reserve — проектный резерв, **не опубликованная гарантия старения**. Гарантированные DC-retention/Ceff отсутствуют и записаныnull.

| Цепь / локальные caps | Требование Ceff | Ёмкость сценария доDC | Нужное weighted DC retention |
| --- | ---: | ---: | ---: |
| TPS63802 VIN / C9 | >=4uF |6.885uF |>=58.10% |
| TPS63802 VOUT / C11+C12, без удалённых C13/C16 |>=7uF приVO>2.3V |26.928uF |>=26.00% |
| BQ25185 SYS / C7 | >1uF |6.885uF |>14.52% |
| BQ25185 BAT / C8 | >1uF |3.23595uF |>30.90% |
| BQ25185 IN / C2+C4+C5+C6 | >1uF |4.6818uF |>21.36% |

TPS63802 SLVSEU9D p5/section8.3 задаёт4uF input и7uF effective output; **22uF — рекомендуемый номинал, а не Ceff minimum**. Точные Yageo sheets page2 визуально просмотрены: приближённые сценарииC9 retention0.70@4.59V →4.8195uF иC11+C12 retention0.60@3.3V →16.1568uF. Page4 прямо говорит, что это simulation, неspecification. Эти сценарии не закрывают гарантированный worst-case gate. X5R не квалифицирован выше85°C.

VBUS:6.8uF nominal →7.48uF tolerance-only upper →8.602uF temperature budget; с дополнительным0.25uF allowance сценарий8.852uF. Получается44.26uC@5V /48.686uC@5.5V. Voltage-dependent C и заряд downstream SYS/BAT/regulator/нагрузок не ограничены этим расчётом; **USB inrush/suspend остаются открытыми**. Доenumeration фиксированный500mA ILIM и заряд/потребление всего устройства требуют отдельного firmware/power policy review.

R70/R71: номинальный порог4.55814V; при−40..85°C, adversarial tolerance/TCR, reference/drift,±9mV offset,±8mV conservative hysteresis идобавочном100nA сценарии board leakage envelope **4.37697..4.73696V**. Leakage allowance — предположение, не TI hot-leakage guarantee. R70/R71 всего0.600/0.225mW@5.5V; R73≈9.167mW. На current Base нет TPS2121/Dock.

Условный пассивный спад VBUS5.5V→нижний порог: **6.215ms**, если ёмкость<=8.852uF, нет удерживающего внешнего/backfed источника и выполняются указанные параметры. C39 nominal tau7.275us. Старый1.085ms расчёт для<=1.5uF **не применим к текущей схеме**. Не добавляем4us comparator delay как гарантированный срок: эта цифра TI измерена при100mV overdrive, а не медленном прохождении порога; firmware latency неизвестна.

R37 CRCW0805HP: ambient derating0.5W@<=70°C,0.411765W@85°C,0.176471W@125°C. С initial1% иTCR envelope условные RMS limits0.474A@25°C /0.429A@85°C /0.280A@125°C. Это не предел peak pulse. Нужно измеритьIpeak,ti,duty,film/terminal temperature исверить **repetitive** pulse power/voltage поp5/6; одиночная pulse-кривая не даёт допуска на повторяющийся EPD boost. Не используем повышенный1.5W terminal-temperature rating без реального теплового подтверждения. Начальные1% не означают1% за весь срок службы.

ДляC22–C31 записаны конкретные native net pairs, номинал/рейтинг иpre-DC сценарий. Требуемые exact-panel Ceff иactual differential voltage/overshoot остаютсяnull. ОсобенноC25 подключён **EPD_SW–EPD_CP_NEG**, а не кGND; его напряжение надо считать как разность двух переключающихся узлов. Точный Base panel/FPC gate пока не закрыт.

## Проверенные первичные источники

[Manifest с URL/bytes/SHA256](../hardware/mainboard/kicad/checks/manufacturer_reference_manifest_R127.json) сохраняет provenance загрузок. Новые размерные страницы рендерены и просмотрены. Generated sheetsRT иCC получены10/11/2026 (C0603_1u25 generated10/10).

- [Yageo RTfamily](https://www.yageogroup.com/content/datasheet/asset/file/PYU-RT_1-TO-0-01_ROHS_L), [R70 exact](https://yageogroup.com/download/specsheet/RT0603BRD0726K7L), [R71 exact](https://yageogroup.com/download/specsheet/RT0603BRD0710KL).
- [Vishay CRCW-HP e3](https://www.vishay.com/docs/20043/crcwhpe3.pdf), rev17-Mar-2026, p1/2/3/5/6/9.
- [TPS63802](https://www.ti.com/lit/ds/symlink/tps63802.pdf), SLVSEU9D; [BQ25185](https://www.ti.com/lit/ds/symlink/bq25185.pdf), SLUSF65B August2026; [TLV3012B](https://www.ti.com/lit/ds/symlink/tlv3012b.pdf), SBOS300C B-version tables6.9/6.10.
- [USB input/inrush TI SLVA129](https://www.ti.com/lit/pdf/slva129), p1; [USB-IF electrical compliance v1.07](https://www.usb.org/sites/default/files/USB%202%200%20Electrical%20Compliance%20Specification(v1.07).pdf), p2.

**fabrication_ready=false.** Нет отправленных запросов поставщикам, заказов, production package или merge default branch. Фактический серверный [run 38129966641](https://github.com/aliaksei-lameyka/ENKU-Base-reader/actions/runs/38129966641) прошёл все 12 шагов; десять отчётов из его лога сохранены и совпадают с локальным checkpoint. server_verified=true; [полная provenance](GITHUB_NATIVE_R127.md).
