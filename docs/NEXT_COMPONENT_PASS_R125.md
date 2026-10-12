# Следующий компонентный проход

По восстановленным прошлым решениям SW2 назывался E-Switch TL3342 без утверждённого suffix, D1–D3 — MBR0530 без производителя. SW1 и боковые SW3–SW6 уже имеют отдельные выбранные детали; повторно их не выбираем.

SW2: текущая PCB геометрия уже совпадает с первичным TL3342F160QG, P010632 rev J/PCR24740 от2021-02-09: 8.0 overall vs4.6 inner по X дают 1.7-мм площадки; 4.8/2.8 по Y дают1.0; центры±3.15/±1.9. Общие пары — горизонтальные ряды. Логический pad1 BOOT соответствует reference terminals3/4; pad2 GND — terminals1/2. Реальной ошибки общих контактов не найдено. [Фактический read-only review и SHA256 PDF](../hardware/mainboard/kicad/checks/SW2_nominal_reference_review_R125.json). Он выполнен после source freeze и не выдаётся за часть server guard. В следующей source-ревизии зафиксировать точный MPN, документацию и локальную библиотеку с этой картой; life-cycle сверять по актуальному P010632, не переносить статус старых P010595/P010596.

D1–D3: изучить точный onsemi MBR0530T1G как инженерный кандидат, сопоставить SOD123 CASE425-04 и cathode band с физической pin1, проверить Vf/leakage/current/voltage применительно к SSD1677 HV. Первичный datasheet: https://www.onsemi.com/pdf/datasheet/mbr0530t1-d.pdf . Пока generic MBR0530 source не заменён точным MPN.

Для 47 pad/drill различий дать каждому конкретную причину и MPN: 17 capacitor footprints,26 resistor footprints,3 diodes и U1 (сверить актуальную таблицу triage перед изменениями). Проверить voltage/DC bias/ESR caps на EPD rail, реальные напряжения батареи/входа, resistor power/tolerance и DNP/tune options. Land-match и MPN qualification — отдельные выводы; массовое обновление generic библиотек не закрывает производственный вопрос.

U1: выбрать и документировать процесс EP/vias/mask/paste. Девять окон пасты .9 уже проверены; сплошная Cu3.9 и drill.3 — сохранённая адаптация. Для минимума drill.3 не использовать библиотечный drill.2 без согласованного реального процесса. Далее полноразмерная механика, полярности, BOM/CPL и единый freeze после внешних gate SW1/TL3340/USB/FPC/stackup.
