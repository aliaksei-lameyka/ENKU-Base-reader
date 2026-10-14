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
repo=Path(__file__).resolve().parents[1];base=repo.parent;v=Path(sys.argv[1]).resolve();out=repo/'hardware/mainboard/r143/pcbway/03_drawings';out.mkdir(parents=True,exist_ok=True)
board_only='--board-review-only' in sys.argv[2:]
logo=repo/'docs/assets/enku-official-logo.png';native=fitz.open(out/'ENKU_R143_Layers_Assembly_NO_FAB.pdf' if board_only else base/'r143-work/native-pdfs/layers.pdf');sch=fitz.open(out/'ENKU_R143_Schematics_NO_FAB.pdf' if board_only else base/'r143-work/native-pdfs/schematics.pdf');g=json.loads((v/'geometry.json').read_text());er=json.loads((v/'independent_electrical_R143.json').read_text());lv=json.loads((v/'layer_visibility_audit_R143.json').read_text());gr=json.loads((v/'independent_Gerber_graph_R143.json').read_text());rq=json.loads((v/'requested_review_R143.json').read_text());sha=hashlib.sha256((repo/'hardware/mainboard/r143/kicad/enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
assert len(native)==10 and len(sch)==5
def bounds(page):
 rs=[d['rect']for d in page.get_drawings()];rs += [fitz.Rect(a[:4])for a in page.get_text('blocks') if not board_only or fitz.Rect(32,72,page.rect.width-32,page.rect.height-76).contains(fitz.Rect(a[:4]))];q=fitz.Rect(rs[0])
 for a in rs[1:]:q |= a
 return q+(-5,-5,5,5)
names=['F.Cu - top copper','In1.Cu - inner copper','In2.Cu - inner copper','B.Cu - bottom copper, unmirrored','F.Mask - openings','B.Mask - openings','F.Paste - top stencil','B.Paste - intentionally empty','F.Fab - assembly and pad numbers','B.Fab - service references']
def plots(src,target,labels,schematic=False):
 doc=fitz.open()
 for i,p in enumerate(src):
  width,height=(p.rect.width,p.rect.height)if schematic else A4; q=doc.new_page(width=width,height=height);q.insert_text((36,32),'ENKU Base R143 | NO FAB',fontsize=15,color=(.09,.17,.25));q.insert_text((36,53),labels[i],fontsize=10);
  if not schematic and i==7:
   scale=min((width-100)/59,(height-180)/101); ox=(width-59*scale)/2;oy=88
   xy=lambda t:fitz.Point(ox+(t[0]-18)*scale,oy+(t[1]-20)*scale)
   for poly in g['board_outline']:q.draw_polyline([xy(t)for t in poly+[poly[0]]],color=(0,0,0),width=.7)
   q.insert_text((36,height-66),'No bottom paste apertures. Actual closed outline shown for orientation.',fontsize=9)
  else:q.show_pdf_page(fitz.Rect(32,72,width-32,height-76),src,i,clip=bounds(p),keep_proportion=True);q.insert_text((36,height-48),'Source '+sha[:20]+'... | native KiCad 10.0.7 | '+str(i+1)+'/'+str(len(src)),fontsize=8);q.insert_text((36,height-33),'Unmirrored board coordinates. Engineering view; use paired Gerber/drill data for CAM.'if not schematic else'Five-sheet actual R143 hierarchy. Physical tests NOT RUN.',fontsize=8)
 doc.set_metadata({'title':'ENKU Base R143 '+target.stem,'subject':'Engineering NO FAB; actual source '+sha});doc.save(target,garbage=4,deflate=True);doc.close()
if not board_only:
 plots(native,out/'ENKU_R143_Layers_Assembly_NO_FAB.pdf',names)
 plots(sch,out/'ENKU_R143_Schematics_NO_FAB.pdf',['Root project','Power','MCU and IO','E-paper HV','Connectors'],True)
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
 if True:
  svg=fitz.open(stream=(v/'F_Cu.svg').read_bytes(),filetype='svg');drawing=fitz.open(stream=svg.convert_to_pdf(),filetype='pdf');pg=drawing[0];factor=72/25.4
  for poly in g['board_outline']:pg.draw_polyline([fitz.Point((t[0]-18)*factor,(t[1]-20)*factor) for t in poly+[poly[0]]],color=(.15,.18,.22),width=.3)
  pg.get_pixmap(matrix=fitz.Matrix(2,2)).save(path)
 else:native[nativepage].get_pixmap(matrix=fitz.Matrix(2,2),clip=bounds(native[nativepage])).save(path)
 im=Image(str(path));ratio=min(width/im.imageWidth,height/im.imageHeight);im.drawWidth=im.imageWidth*ratio;im.drawHeight=im.imageHeight*ratio;story.append(im);story.append(Spacer(1,10))
h('ENKU Reader Base R143')
p('Проверка перед первыми 5-10 образцами. 14 октября 2026. <b>NO FAB: выпуск не закрыт.</b>')
picture(0,base/'r143-work/board-top.png',250,400)
p('59 x 101 x 1.6 мм, четыре слоя меди. ESP32-S3-WROOM-1-N16R8, GDEY0397T81P / SSD1677, microSD SPI, BMI270. BQ24072T + TPS63802.')
p('R143 исправляет крепёжные площадки и пасту J3. Схема электрически совпадает с R142. Полный локальный native/независимый прогон прошёл; физические испытания не проведены.')
p('SHA-256 фактической платы:<br/>'+sha)
page()
h('J3: исправление по Hirose')
table(['Параметр','R142','Фактическая R143'],[
 ['Медь лапок S1/S2','0.80 x 0.80 мм','0.40 x 0.80 мм'],
 ['Отдельные окна пасты лапок','0.80 x 0.65 мм','0.40 x 0.80 мм'],
 ['Локальные центры лапок','+/-6.75, +1.25 мм','Сохранены'],
 ['24 сигнальные площадки','Медь0.30 x0.80 мм; паста0.25 x0.65 мм','Сохранены, совпадают с OEM'],
 ['Pin1 / pin24, F.Cu','75.02,32.75 /63.52,32.75 мм','Сохранены, без зеркалирования'],
 ['Контроль фактической пасты','Исторический экспорт','26 flashes Gerber, размеры и координаты проверены']],[160,170,180])
p('OEM E=13.1 и F=13.9 мм задают края лапок. Ширина=(F-E)/2=0.40 мм; центр=(E+F)/4=6.75 мм. Исправлены embedded footprint и исходная библиотека. Десять внесённых ошибок отвергнуты, в том числе возврат прежней увеличенной меди/пасты.')
p('Феликс 10 октября подтвердил VDHR=VSH2, радиус1-1.5 мм и отступ от стекла>=2 мм. В конструкции применяем R>=1.5 мм, отступ>=2 мм. Его подтверждение разъёма относится к присланному DIANWEI, а установленный Hirose имеет другой footprint.')
p('Остаётся сверить гарантированную толщину FPC: панель0.25..0.35 мм, Hirose0.27..0.33 мм; ширину/coverlay/стоп, folded pin1, защёлку и GDEM/GDEY CAD. Совпадение номинала не покрывает весь допуск. Физическая примерка NOT RUN.')
page()
h('Выполненные проверки')
table(['Метод','Результат'],[
 ['KiCad10.0.7','DRC0, ERC0, обрывы0, parity0. Все severity, track errors, refilled zones. Правила не ослаблены.'],
 ['Точный delta R142-R143','Изменены только четыре определения pad J3 и их полигоны. Все остальные pads/tracks/vias/позиции/outline/rule areas сохранены; topology идентична.'],
 ['Независимая медь Gerber','Все четыре полных изображения сопоставлены с native copper. Gerbonara + Shapely:80 функциональных сетей,0 обрывов/замыканий. Реальные виртуальные разрез и мост меди обнаружены.'],
 ['Экспорт изготовления','11 Gerber, PTH/NPTH, четыре USB slots,439 pad +373 via IPC356 records, mask/paste/silk, BOM и114 top placements проверены.'],
 ['Электрика и корпуса','134 refs,453 native pads;61 active-IC lands; exact MPN, polarities, shared nets,18 ошибочных pin/value случаев отвергнуты.'],
 ['Пути и земля','30 явных путей. На каждом участке centerline14 FAST-сетей есть GND хотя бы на одном внутреннем слое. В предпочтительном слое бывают gaps; SI/EMI не квалифицированы.'],
 ['Неизменяемая R138','Снимок commit2601e16:27 независимых scopes и20 эффективных отрицательных случаев прошли. Goldens не перезаписаны.']],[150,360])
p('GPIO35-37 не нагружены;26-32 внутренние memory-сигналы. GPIO3/45/46 свободны. GPIO0:10k, SW2 на землю и J7 BOOT; ручной EN на J7. На CC1/CC2 отдельные5.1k; USBLC6 на D+/D-. VBUS6.8 мкФ nominal, феррита нет.')
p('Серверный run38615866570 также прошёл на sourcec9dc9e6. У скачанного ZIP165 записей проверены API SHA/CRC;24 manufacturing-файла совпали после нормализации только creation timestamps.')
p('Слои имеют уникальные имена. Неименованных слоёв и netless copper нет. Hidden reference85, value127 перечислены в отчёте. SD CMD/DAT0-3 подтянуты10k; BMI270 I2C0x68, INT1=GPIO18.')
page()
h('Питание: блокер первого запуска')
table(['Величина','Текущее значение / ограничение'],[
 ['3V3_SYS nominal','3.245491 В, R14=27.4k /R15=4.99k,0.1%,10ppm/K'],
 ['Статический PWM диапазон','3.199451..3.291805 В при заданных corners; это условный расчёт для PWM'],
 ['U11 max rising','TLV803EA30DBZR:3.188724 В; min static release margin10.727 мВ'],
 ['Панель max operative','3.3 В; верхний статический запас8.195 мВ'],
 ['Фактический MODE','U4.2=GND, PFM разрешён. Гарантия +/-1% дана TI для PWM. Реальные PFM/overshoot/dips не квалифицированы.'],
 ['Вывод','DRC0 и статический расчёт не закрывают общую шину питания. MODE-only и divider-only изменения не объявлены решением.']],[150,360])
p('Независимый расчёт: с проектным резервом50 мВ снизу и25 мВ сверху даже идеальные резисторы при PWM+/-1% требуют nominal>=3.271438 В и одновременно<=3.242574 В. Интервалы не пересекаются. Резервы являются инженерными целями, не требованиями производителя.')
p('Нужен обоснованный совместный выбор rail/reset/panel: точный supervisor либо разделение питания с проверкой I/O/OFF, допусков, утечек, времени и idle budget. Нельзя механически заменить A30 на A29: slow-ramp release может оказаться ниже3.0 В для ESP32. TPS3808EG33 также не решает запас по гарантированным error/hysteresis.')
p('BQ24072T сохраняет зарядку при hard OFF; default high-Z USB100. Без батареи USB100 не гарантирует старт ESP32. Нужен квалифицированный protected pack или battery simulator для первого flash. Mainboard PCM и fuel gauge отсутствуют.')
page()
h('Первые 5-10 плат: порядок запуска')
table(['Этап','Критерий / запись'],[
 ['До передачи artwork','Закрыть питание, FPC/корпус, protected pack/NTC, stackup/drill/fill-cap/stencil и exact BOM/CPL import. Подготовить воспроизводимый FCT binary.'],
 ['Первые1-2 сборки','В пределах pilot сначала собрать1-2 платы. AOI/X-ray/ICT, полярность/pin1, R67 DNP. Остальные собирать после диагностики первых.'],
 ['Питание и reset','Rail у ESP3.0..3.6 В, VCI панели2.2..3.3 В, включая пики. Ramps0.1 мс..10 с;100 cold starts и100 rapid cycles на каждой плате.'],
 ['ROM и память','UART/USB recovery;16MiB Quad flash и8MiB Octal PSRAM patterns. Консервативный flash80MHz; без изменений eFuse.'],
 ['SD / USB / BMI','SD write/read hashes, remove/recovery, exclusive USB-MSC ownership. BMI config, INTERNAL_STATUS[3:0]==1, self-test и реальный IRQ.'],
 ['EPD и совмещённая нагрузка','Full/partial refresh; capture HV, switch/VGS, L2 peak/RMS, differential voltage capacitors. Wi-Fi TX+SD write+EPD, min battery и температуры.'],
 ['OFF / заряд / NTC','USB/UART back-power, input limit/authorization/suspend, PCM; sensor0/25/45C и fault cases, thermal lag/detachment.'],
 ['Каждый serial','Source/BOM/firmware hash, приборы, условия, raw logs/waveforms, численные min/max и disposition. Отсутствие результата остаётся NOT RUN.']],[150,360])
p('100 циклов - критерий bring-up, а не ресурсная квалификация. Первая неисправность останавливает продолжение сборки до выяснения причины. План не является записью успешного испытания или размещённым заказом.')
page()
h('Пакет, ограничения и источники')
p('01_fabrication:11 Gerber, drill PTH/NPTH/maps, IPC356. 02_assembly:BOM/CPL CSV+XLSX, all-pad map и process requests. 03_drawings:этот обзор,10 layer/assembly и5 schematic страниц. 04_editable_kicad:67 актуальных файлов. 05_verification:фактические native/independent evidence. 06_qualification:процедуры и открытые пункты.')
p('373 vias,84 nominal0.2 мм bores на1.6 мм PCB, шесть resin-fill/copper-cap requests. Actual stackup/90-ohm USB, aspect/drill tolerances, void/flatness, общий reflow и короткие0.8 мм USB stakes требуют согласования. J3: peak<=250C, выше230C<=60s; пустую защёлку не закрывать.')
p('На e-paper L2=47 мкГн, Isat typical1.1 А при30% потере L и25C; D1-D3 MBR0530T1G30 В/0.5 А; Q1 IRLML6346TRPBF30 В; R37 pulse-rated2.2 Ом. Hot peak/RMS, overshoot, pulse temperature и гарантированная MLCC Ceff не подтверждены.')
p('Первичные документы: supplied GDEY0397T81P pp5/6/8/19; Hirose EDC-159714-50-08 и ELC4-159714-04; TI TPS63802 SLVSEU9D, TLV803E SLVSES2J, BQ24072T SLUS937C; Espressif WROOM v1.8; Bosch BMI270 DS000-08. Точные ссылки, SHA и условия указаны в STARTUP_RISKS_R143.md и отчётах.')
p('Расчёты MNA/corners/Monte Carlo, граф меди и RC-модели выполнены. SPICE с точными macromodels, IBIS/field solver, физические FCT/EMI/ESD/RF и полный корпус не выполнены. Типовые кривые не выданы за гарантированные пределы. Поставщицкие PDF/CAD не распространяются в публичном пакете.')
ledger=json.loads((repo/'docs/DEVELOPMENT_HOURS_READER.json').read_text());entry=ledger['entries'][-1]
p(f"Учёт времени: последний зафиксированный проход{entry['hours']:.2f} ч; подтверждённый накопленный минимум{ledger['logged_lower_bound_hours']:.2f} ч. Неучтённые старые сеансы и хвост публикации/сохранения не добавлены без наблюдаемого интервала.")
p('<b>R143 - проверенный инженерный checkpoint. Готовность к изготовлению и гарантированный запуск не заявлены.</b>')
def decor(c,doc):
 c.saveState();c.setFont('DejaVu',8);c.setFillColor(colors.HexColor('#607589'));c.drawString(42,22,'ENKU Base R143 / NO FAB / physical tests NOT RUN');c.drawRightString(A4[0]-42,22,str(doc.page))
 if logo.exists():c.drawImage(str(logo),A4[0]-96,A4[1]-49,width=54,height=28,preserveAspectRatio=True,anchor='c',mask='auto')
 c.restoreState()
doc=SimpleDocTemplate(str(out/'ENKU_R143_Board_Review_NO_FAB.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=58,bottomMargin=42,title='ENKU Base R143 board review - NO FAB',author='ENKU',subject='Actual source '+sha);doc.build(story,onFirstPage=decor,onLaterPages=decor)
for f in out.glob('*.pdf'):
 z=fitz.open(f);print(f.name,len(z))
