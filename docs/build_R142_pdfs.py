"""Verified source plots and concise Russian board review, no fabricated test results."""
from pathlib import Path
import json,sys,hashlib
import fitz
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
repo=Path(__file__).resolve().parents[1];base=repo.parent;v=Path(sys.argv[1]).resolve();out=repo/'hardware/mainboard/r142/pcbway/03_drawings';out.mkdir(parents=True,exist_ok=True)
board_only='--board-review-only' in sys.argv[2:]
logo=repo/'docs/assets/enku-official-logo.png';native=fitz.open(out/'ENKU_R142_Layers_Assembly_NO_FAB.pdf' if board_only else base/'docs-build/native/layers.pdf');sch=fitz.open(out/'ENKU_R142_Schematics_NO_FAB.pdf' if board_only else base/'docs-build/native/schematics.pdf');g=json.loads((v/'geometry.json').read_text());er=json.loads((v/'independent_electrical_R142.json').read_text());lv=json.loads((v/'layer_visibility_audit_R142.json').read_text());gr=json.loads((v/'independent_Gerber_graph_R142.json').read_text());rq=json.loads((v/'requested_review_R142.json').read_text());sha=hashlib.sha256((repo/'hardware/mainboard/r142/kicad/enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
assert len(native)==10 and len(sch)==5
def bounds(page):
 rs=[d['rect']for d in page.get_drawings()];rs += [fitz.Rect(a[:4])for a in page.get_text('blocks') if not board_only or fitz.Rect(32,72,page.rect.width-32,page.rect.height-76).contains(fitz.Rect(a[:4]))];q=fitz.Rect(rs[0])
 for a in rs[1:]:q |= a
 return q+(-5,-5,5,5)
names=['F.Cu - top copper','In1.Cu - inner copper','In2.Cu - inner copper','B.Cu - bottom copper, unmirrored','F.Mask - openings','B.Mask - openings','F.Paste - top stencil','B.Paste - intentionally empty','F.Fab - assembly and pad numbers','B.Fab - service references']
def plots(src,target,labels,schematic=False):
 doc=fitz.open()
 for i,p in enumerate(src):
  width,height=(p.rect.width,p.rect.height)if schematic else A4; q=doc.new_page(width=width,height=height);q.insert_text((36,32),'ENKU Base R142 | NO FAB',fontsize=15,color=(.09,.17,.25));q.insert_text((36,53),labels[i],fontsize=10);
  if not schematic and i==7:
   scale=min((width-100)/59,(height-180)/101); ox=(width-59*scale)/2;oy=88
   xy=lambda t:fitz.Point(ox+(t[0]-18)*scale,oy+(t[1]-20)*scale)
   for poly in g['board_outline']:q.draw_polyline([xy(t)for t in poly+[poly[0]]],color=(0,0,0),width=.7)
   q.insert_text((36,height-66),'No bottom paste apertures. Actual closed outline shown for orientation.',fontsize=9)
  else:q.show_pdf_page(fitz.Rect(32,72,width-32,height-76),src,i,clip=bounds(p),keep_proportion=True);q.insert_text((36,height-48),'Source '+sha[:20]+'... | native KiCad 10.0.7 | '+str(i+1)+'/'+str(len(src)),fontsize=8);q.insert_text((36,height-33),'Unmirrored board coordinates. Engineering view; use paired Gerber/drill data for CAM.'if not schematic else'Five-sheet actual R142 hierarchy. Physical tests NOT RUN.',fontsize=8)
 doc.set_metadata({'title':'ENKU Base R142 '+target.stem,'subject':'Engineering NO FAB; actual source '+sha});doc.save(target,garbage=4,deflate=True);doc.close()
if not board_only:
 plots(native,out/'ENKU_R142_Layers_Assembly_NO_FAB.pdf',names)
 plots(sch,out/'ENKU_R142_Schematics_NO_FAB.pdf',['Root project','Power','MCU and IO','E-paper HV','Connectors'],True)
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('DejaVuBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='RU',fontName='DejaVu',fontSize=10.5,leading=15.5,spaceAfter=8,textColor=colors.HexColor('#182a3a')));styles.add(ParagraphStyle(name='RUHead',fontName='DejaVuBold',fontSize=18,leading=24,spaceAfter=15,textColor=colors.HexColor('#182a3a')));styles.add(ParagraphStyle(name='RUSub',fontName='DejaVuBold',fontSize=11,leading=16,spaceAfter=10));styles.add(ParagraphStyle(name='RUCell',fontName='DejaVu',fontSize=9.3,leading=14))
story=[]
def p(t):story.append(Paragraph(t,styles['RU']))
def h(t):story.append(Paragraph(t,styles['RUHead']))
def sub(t):story.append(Paragraph(t,styles['RUSub']))
def page():story.append(PageBreak())
def table(headers,rows,widths):
 data=[[Paragraph(str(t),styles['RUCell'])for t in row]for row in [headers,*rows]];t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7edf2')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#8295a8')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d7dfe5'))]));story.append(t);story.append(Spacer(1,10))
def picture(nativepage,path,width=260,height=420):
 if board_only:
  svg=fitz.open(stream=(v/'F_Cu.svg').read_bytes(),filetype='svg');drawing=fitz.open(stream=svg.convert_to_pdf(),filetype='pdf');pg=drawing[0];factor=72/25.4
  for poly in g['board_outline']:pg.draw_polyline([fitz.Point((t[0]-18)*factor,(t[1]-20)*factor) for t in poly+[poly[0]]],color=(.15,.18,.22),width=.3)
  pg.get_pixmap(matrix=fitz.Matrix(2,2)).save(path)
 else:native[nativepage].get_pixmap(matrix=fitz.Matrix(2,2),clip=bounds(native[nativepage])).save(path)
 im=Image(str(path));ratio=min(width/im.imageWidth,height/im.imageHeight);im.drawWidth=im.imageWidth*ratio;im.drawHeight=im.imageHeight*ratio;story.append(im);story.append(Spacer(1,10))
h('ENKU Reader Base R142');p('Инженерная проверка платы перед PCBWay. 14 октября 2026. <b>NO FAB</b>.');picture(0,base/'docs-build/board-top.png',260,440);p('59 × 101 × 1.6 мм. Четыре слоя меди. ESP32-S3-WROOM-1-N16R8, e-paper 3.97″, microSD SPI, BMI270.');p('SHA-256 текущей платы:<br/>'+sha);p('<b>Физические испытания не проведены.</b> Пакет содержит исходники и проверенный экспорт для инженерного review. Производственный выпуск требует закрытия перечисленных ограничений.');page()
h('Что исправлено в R142')
table(['Проблема','Исправление'],[
 ['Reset при медленном нарастании и быстрых циклах','TLV803EA30DBZR: GND/RESET/VDD = 1/2/3, open-drain EN; C15 = 100 нФ по питанию. Сохранены R17 и ручной reset через J7.'],
 ['Совместный предел ESP32, reset и панели','R14 27.4 кΩ / R15 4.99 кΩ, 0.1%, 10 ppm/K. Номинал 3.24549 В. Отброшен вариант 3.38 В, превышавший рабочий предел панели 3.3 В.'],
 ['Недостающие SD-подтяжки','R23 = 10 кΩ; R91-R94 = 10 кΩ на CMD/DAT0/DAT1/DAT2. Неиспользуемые DAT1/2 имеют отдельные bias-сети.'],
 ['Card Detect','J2.9/J2.10, R90 и GPIO39. GPIO35-37 остаются свободными от внешних подключений.'],
 ['NTC и отключение защиты TS','R82 100 кΩ сохранён; R89 3.3 МΩ задаёт пассивное смещение. Не объявляется защита от всех неисправностей.'],
 ['Медь в запретных областях Hirose','Пять front-only rule areas; исправлены пересечения VBUS/SD_CS_CARD, не обнаруживавшиеся прежним DRC.'],
 ['Скрытая старая документация','45 объектов удалены с архивом; trial-текст убран; USB mating guide сохранён на F.Fab.']],[145,365]);page()
h('Результаты проверок по файлам')
table(['Метод','Результат и граница'],[
 ['Native KiCad 10.0.7','DRC0 / ERC0 / обрывы0 / parity0. Зоны перезалиты. Правила и исходники R138/R141 сохранены.'],
 ['Схема, выводы и корпуса','134 reference /453 pad /114 установленных top-компонентов;19 bare и R67 DNP. 438 старых pad definitions сохранены.'],
 ['Независимая медь','Все четыре полных изображения Gerber сопоставлены с native copper; бюджет аппроксимации 0.0052 мм.'],
 ['Gerber connectivity','80 именованных сетей: обрывов и замыканий не найдено. Программные копии меди с реальным обрывом U11 и GND-RESET мостом отвергаются.'],
 ['Производственные файлы','11 Gerber; отдельные PTH/NPTH;439 conductive-pad +373 via записей IPC356; маска, паста, silk, BOM/CPL;114 fitted.'],
 ['Графы и опорная земля','30 фактических путей,14 FAST-сетей. Нет участка centerline без обеих внутренних GND-проекций. Есть gaps предпочтительного слоя: SI не квалифицирован.'],
 ['Расчёты и внесение ошибок','Nodal MNA, corners,50 000 Monte Carlo, RC-модели.18 ошибочных pin/value сценариев отвергнуты. Не SPICE и не измерения прототипа.']],[145,365]);p('Финальный source commit41b3f00a прошёл серверный run38576201886. Проверены API digest, ZIP CRC и все24 manufacturing-файла; совпадают после нормализации только явно заданных timestamp-полей. Полная запись: GITHUB_R142.json.');page()
h('ESP32, straps и USB')
table(['Пункт','Проверено'],[
 ['GPIO35-37','Модульные pads28/29/30: NC, внешней меди нет. GPIO26-32 остаются внутренними memory-сигналами модуля. Pad32 модуля - это GPIO39.'],
 ['GPIO0/3/45/46','GPIO3/45/46 не нагружены. GPIO0: R18 10 кΩ, кнопка SW2 на GND, J7 BOOT. EN доступен на J7.'],
 ['Ручной загрузчик','BOOT low при reset; удержание >=3 мс после EN rising. UART0/ROM USB. J7 pin1 - VREF, не вход питания. Автоматического DTR/RTS узла на плате нет.'],
 ['USB-C','R62/R63 5.1 кΩ на отдельных CC; USBLC6-2SC6 на D+/D-. Номинальная ёмкость VBUS 6.8 мкФ. Феррита нет; есть шунтирующая ёмкостная фильтрация.'],
 ['Требует испытаний','16 MiB flash/8 MiB octal PSRAM, фактический ROM boot, USB enumeration/suspend/inrush/ESD, измеренный stackup 90 Ω и кабели.']],[145,365]);p('Нельзя считать наличие VBUS/PGOOD разрешением на USB500. В режиме по умолчанию USB100 лимит включает ток всей системы. Запуск ESP32 без батареи от USB100 не гарантирован.');page()
h('Питание и температурные углы')
reset=er['reset'];table(['Величина','Расчёт'],[
 ['Номинальная 3V3_SYS',f"{reset['nominal_output_V']:.6f} В"],
 ['Статический PWM диапазон','3.199451..3.291805 В; initial0.1%, TCR10ppm/K, FB+-1%, IFB+-100 нА, dt до100 K.'],
 ['Макс. отпускание U11','3.188724 В; статический запас min10.727 мВ.'],
 ['Рабочий максимум панели','3.3 В; статический запас min8.195 мВ.'],
 ['Открытые пределы','PFM, startup/load/line transients и долговременный сдвиг R не квалифицированы. Узкий статический запас нельзя переносить на эти режимы.'],
 ['Power path / OFF','BQ24072T: USB-BAT-VSYS с DPPM. Q2 отключает reader после charger. OFF с USB оставляет charger включённым; high-Z default USB100/CE low.'],
 ['Батарея и SOC','PCM на mainboard отсутствует; нужен квалифицированный protected pack. Переключаемый делитель 2 МΩ/680 кΩ +ADC - оценка напряжения, не fuel gauge.']],[145,365]);p('NTC corners рассчитаны по таблице Semitec с допущением TS leakage +-100 нА. Гарантированный предел утечки неизвестен. R82-open бюджет около155.6 нА; detached sensor на горячей ячейке не определяется электрически. Зарядка/NTC остаются HOLD.');page()
h('E-paper и силовая часть')
table(['Узел','Проверка и ограничение'],[
 ['Конкретная панель','GDEY0397T81P /SSD1677. VCI2.2..3.3 В, ambient0..50°C. Ориентация в изделии portrait480×800.'],
 ['FPC24 pin','Феликс 10 октября подтвердил VDHR=VSH2. Все24 контакта J3 проверены; pin5 -> C28 4.7 мкФ/25 В на GND. Допуски FPC, folded pin1 и крепёжные лапки - HOLD.'],
 ['Силовая схема','Q1 IRLML6346TRPBF30 В; L2 47 мкГн20%; D1-D3 MBR0530T1G30 В/0.5 А; R37 2.2 Ω HP. Полярность и pin maps проверены.'],
 ['Индуктор','TYS5040470M-10: Irms typ1 А, Isat typ1.1 А при30% потере L и25+-5°C; DCRmax0.326 Ω. Это не гарантированный hot Isat.'],
 ['Керамика','Учитываются tolerance, temperature, ageing и типовые DC-bias сценарии. Для HV важна разность напряжений на выводах, включая overshoot. Гарантированная Ceff и реальные HV ещё не подтверждены.'],
 ['Разводка','Пути Q1-L2-D1-C25 и питание/возврат измерены по native-геометрии. Земля под силовой частью сохранена. Геометрия не даёт индуктивность петли, EMI или устойчивость управления.']],[145,365]);p('Нужны осциллограммы VGH/VGL/VSH/VCOM, VGS и switch node; peak/RMS L2, обратное напряжение диодов, leakage/temperature, repetitive pulse R37 и панельный refresh. Generic SSD1677 схема не закрывает несовпадение конкретного FPC.');page()
h('SD, BMI270 и слои')
table(['Пункт','Состояние'],[
 ['microSD','SPI совместно с EPD, отдельный CS. CMD/DAT0-3 внешне подтянуты10 кΩ, CLK без pullup. Card Detect GPIO39 active-low.'],
 ['Прошивка SD','Нужны debounce/hot remove, данные+hash, безопасная инициализация, эксклюзивное владение картой между filesystem и USB-MSC. Реальные peak currents не измерены.'],
 ['BMI270','VDD/VDDIO общая switched3V3; CSB high, SDO GND -> I2C0x68;4.7 кΩ pullups; INT1 -> GPIO18. Нужны config/internal-status/self-test/IRQ.'],
 ['I2C / ADC','Bring-up100 кГц;400 кГц только при измеренном rise <=300 нс. ADC: ожидание500 мс после rail valid, затем калибровка.'],
 ['Слои','16 enabled, уникальные имена; четыре медных слоя. Без unnamed layers, netless tracks/vias/fills и copper graphics без net semantics.'],
 ['Скрытые поля',f"Reference: {lv['hidden_reference_count']}; Value: {lv['hidden_value_count']}. Все перечислены в отчёте. Hide не исключает объект из DRC или экспорта."],
 ['RF','Одна исходная all-layer antenna exclusion; отдельная rear Tag-Connect exclusion. Медь/GND отсутствует в antenna region. Нужны корпус/батарея/FPC clearance и реальный RF range.']],[145,365]);page()
h('Что измерить до выпуска')
table(['Этап','Критерий закрытия'],[
 ['Поставщик / процесс','Гарантированные допуски FPC, folded pin1 и CAD identity; PCBWay J3 hold-down/stencil/stackup/drill84×0.2 мм/fill-cap6/USB stakes; protected pack и корпус.'],
 ['AOI / X-ray / ICT','Нет коротких замыканий/обрывов; правильный pin1/polarity;114 fitted, R67 DNP; согласованные пайка/void/flatness.'],
 ['Запуск и OFF','Supply ramps0.1 мс..10 с,100 cold starts и100 быстрых циклов; USB/UART back-power; reset и charger mode capture.'],
 ['Совмещённая нагрузка','Wi-Fi TX+SD write+EPD refresh: 3V3/VCI min/max, droop/overshoot, ток, температура и данные.'],
 ['Зарядка и NTC','Все4 режима, USB authorization/suspend, NTC0/25/45°C, open/short/faults и detachment/thermal lag.'],
 ['Функции и надёжность','ROM recovery, flash/PSRAM patterns, SD/MSC ownership, BMI self-test/IRQ, EPD modes/OTP, soak/cycles, RF/ESD/EMI и механика.']],[145,365]);p('Подробные процедуры: FCT_PLAN_R142.md. Для каждого теста фиксируются serial, source/BOM/firmware hash, реальные лимиты, приборы, температура и измеренные данные. Все физические тесты здесь имеют статус <b>NOT RUN</b>.');p('Статус платы: инженерный NO FAB. Производственный выпуск не объявлен.');page()
h('Дисплей и разъём: сверка документов')
table(['Пункт','Результат'],[
 ['Ответ Феликса 10 октября','VDHR и VSH2 - один сигнал. Подтвердил присланный DIANWEI, радиус1-1.5 мм и отступ>=2 мм. Для корпуса: R>=1.5 мм, отступ>=2 мм.'],
 ['Наш Hirose FH34SRJ','24 контакта, шаг0.5 мм, контакт сверху и снизу, высота1 мм. DIANWEI8.21A0.024200 имеет другой footprint и не является drop-in.'],
 ['Электрика и сигнальные lands','Все24 pin mappings совпали; NC1/4/6/7 и VPP19 открыты. Медь0.30×0.80 мм, паста0.25×0.65 мм соответствуют Hirose. Проверены26 реальных Gerber paste flashes и8 эффективных design-fault сценариев.'],
 ['Толщина и ширина FPC','Панель0.30±0.05 мм против Hirose0.30±0.03 мм. Ширина12.50±0.10 мм против рекомендованных12.50±0.05 мм. Номиналы совпадают, полный допуск не покрыт; нужна гарантия партии/acceptance. Это не доказательство отказа номинального шлейфа.'],
 ['Крепёжные лапки J3','Центры совпали. Медь0.80×0.80 и паста0.80×0.65 мм против OEM0.40×0.80 мм: пасты по площади больше на62.5%. Отдельная DFM/reflow квалификация.'],
 ['Окончательная сборка','Проверить толщину/coverlay/стоп, folded pin1-to-pin1, движение защёлки, strain relief и GDEM/GDEY CAD identity. Физическая примерка и работа панели не проведены.']],[145,365]);p('Полные источники, размеры и24-pin CSV: FPC_CONNECTOR_REVIEW_R142.md и FPC_connector_audit_R142.json. Сверка не меняет исходную плату и производственные файлы. Исторические результаты не переписаны.');page()
h('Пакет и воспроизводимость')
p('01_fabrication: 11 Gerber, PTH/NPTH, IPC356 и drill maps. 02_assembly: BOM/CPL CSV+XLSX, all-reference и all-pad данные, process CSV. 03_drawings: этот review,10 layer/assembly страниц и5 схемных листов. 04_editable_kicad: текущие исходники. 05_verification: native и независимые результаты. 06_qualification: процедуры и ограничения.');p('373 vias:367 обычных,6 resin-fill/copper-cap requests. Минимальное номинальное кольцо0.15 мм; обычные via не ближе0.10 мм к SMD lands.84 nominal0.20 мм bores на1.6 мм дают номинальный aspect8:1; технологические допуски не подтверждены.');p('BOM/CPL используют абсолютный origin0,0 и исходные KiCad top angles: X=boardX, Y=-boardY. Supplier import/rotation approval остаётся открытым. Не смешивать файлы различных ревизий.');p('Первичные источники и точные SHA приведены в PRE_REVIEW_CHECKS_R142.md. Основные документы: Espressif WROOM1/SD pullups/hardware checklist; TI BQ24072T/TPS63802/TLV803E; Bosch BMI270; Laird TYS5040; onsemi MBR0530; Yageo RT v17; NXP UM10204; оригинальные GoodDisplay и Hirose PDF.');p('Статические расчёты использовали независимые NumPy/Shapely/Gerbonara алгоритмы. IBIS, field solver, converter macromodel и реальные стендовые испытания не выполнялись. Методики и сценарные пределы подписаны в JSON-отчётах.');p('Публичные исторические исходники/guards/goldens R138 и предыдущая R141 не заменены. Поставщицкие PDF/CAD не включены в публичный пакет.');
ledger_path=repo/'docs/DEVELOPMENT_HOURS_READER.json'
if ledger_path.exists():
 ledger=json.loads(ledger_path.read_text());entry=ledger['entries'][-1];p(f"Учёт разработки: последний зарегистрированный проход {entry['hours']:.2f} ч; накопленный подтверждённый минимум {ledger['logged_lower_bound_hours']:.2f} ч. Это ограниченные наблюдаемыми интервалами часы задачи; старые не восстановленные сеансы и последующая публикация/сохранение не включены.")
def decor(c,doc):
 c.saveState();c.setFont('DejaVu',8);c.setFillColor(colors.HexColor('#607589'));c.drawString(42,22,'ENKU Base R142 / NO FAB / physical tests NOT RUN');c.drawRightString(A4[0]-42,22,str(doc.page));
 if logo.exists():c.drawImage(str(logo),A4[0]-96,A4[1]-49,width=54,height=28,preserveAspectRatio=True,anchor='c',mask='auto')
 c.restoreState()
doc=SimpleDocTemplate(str(out/'ENKU_R142_Board_Review_NO_FAB.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=58,bottomMargin=42,title='ENKU Base R142 board review - NO FAB',author='ENKU',subject='Actual source '+sha);doc.build(story,onFirstPage=decor,onLaterPages=decor)
for f in out.glob('*.pdf'):
 z=fitz.open(f);assert len(z)>0;print(f.name,len(z))

