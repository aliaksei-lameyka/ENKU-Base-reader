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
repo=Path(__file__).resolve().parents[1];base=repo.parent;v=Path(sys.argv[1]).resolve();out=repo/'hardware/mainboard/r144/pcbway/03_drawings';out.mkdir(parents=True,exist_ok=True)
board_only='--board-review-only' in sys.argv[2:]
logo=repo/'docs/assets/enku-official-logo.png';native=fitz.open(out/'ENKU_R144_Layers_Assembly_NO_FAB.pdf' if board_only else base/'r144-work/native-pdfs/layers.pdf');sch=fitz.open(out/'ENKU_R144_Schematics_NO_FAB.pdf' if board_only else base/'r144-work/native-pdfs/schema-clean-new.pdf');g=json.loads((v/'geometry.json').read_text());er=json.loads((v/'independent_electrical_R144.json').read_text());lv=json.loads((v/'layer_visibility_audit_R144.json').read_text());gr=json.loads((v/'independent_Gerber_graph_R144.json').read_text());rq=json.loads((v/'requested_review_R144.json').read_text());sha=hashlib.sha256((repo/'hardware/mainboard/r144/kicad/enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
assert len(native)==10 and len(sch)==5
def bounds(page):
 rs=[d['rect']for d in page.get_drawings()];rs += [fitz.Rect(a[:4])for a in page.get_text('blocks') if not board_only or fitz.Rect(32,72,page.rect.width-32,page.rect.height-76).contains(fitz.Rect(a[:4]))];q=fitz.Rect(rs[0])
 for a in rs[1:]:q |= a
 return q+(-5,-5,5,5)
names=['F.Cu - top copper','In1.Cu - inner copper','In2.Cu - inner copper','B.Cu - bottom copper, unmirrored','F.Mask - openings','B.Mask - openings','F.Paste - top stencil','B.Paste - intentionally empty','F.Fab - assembly and pad numbers','B.Fab - service references']
def plots(src,target,labels,schematic=False):
 doc=fitz.open()
 for i,p in enumerate(src):
  width,height=(p.rect.width,p.rect.height)if schematic else A4; q=doc.new_page(width=width,height=height);q.insert_text((36,32),'ENKU Base R144 | NO FAB',fontsize=15,color=(.09,.17,.25));q.insert_text((36,53),labels[i],fontsize=10);
  if not schematic and i==7:
   scale=min((width-100)/59,(height-180)/101); ox=(width-59*scale)/2;oy=88
   xy=lambda t:fitz.Point(ox+(t[0]-18)*scale,oy+(t[1]-20)*scale)
   for poly in g['board_outline']:q.draw_polyline([xy(t)for t in poly+[poly[0]]],color=(0,0,0),width=.7)
   q.insert_text((36,height-66),'No bottom paste apertures. Actual closed outline shown for orientation.',fontsize=9)
  else:q.show_pdf_page(fitz.Rect(32,72,width-32,height-76),src,i,clip=bounds(p),keep_proportion=True);q.insert_text((36,height-48),'Source '+sha[:20]+'... | native KiCad 10.0.7 | '+str(i+1)+'/'+str(len(src)),fontsize=8);q.insert_text((36,height-33),'Unmirrored board coordinates. Engineering view; use paired Gerber/drill data for CAM.'if not schematic else'Five-sheet actual R144 hierarchy. Physical tests NOT RUN.',fontsize=8)
 doc.set_metadata({'title':'ENKU Base R144 '+target.stem,'subject':'Engineering NO FAB; actual source '+sha});doc.save(target,garbage=4,deflate=True);doc.close()
if not board_only:
 plots(native,out/'ENKU_R144_Layers_Assembly_NO_FAB.pdf',names)
 plots(sch,out/'ENKU_R144_Schematics_NO_FAB.pdf',['Root project','Power','MCU and IO','E-paper HV','Connectors'],True)
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

assert json.loads((v/'verification_R144.json').read_text())['complete_independent_manufacturing_checks']=='PASS'
st=json.loads((v/'startup_envelope_R144.json').read_text())
h('ENKU Reader Base R144')
p('15 октября 2026. Пакет для инженерного review первых 5-10 плат. <b>NO FAB. Физические испытания NOT RUN.</b>')
picture(0,base/'r144-work/board-top.png',250,390)
p('59 x 101 x 1.6 мм, четыре слоя меди. ESP32-S3-WROOM-1-N16R8, GDEY0397T81P / SSD1677, microSD SPI, BMI270. BQ24072T + TPS63802.')
p('R144 перерабатывает питание и reset. Полный локальный и серверный прогоны прошли. Источник 609f8ac00357b9b0c6b3c43c381469c498453a11; GitHub run38693384483. Выпуск в изготовление ещё не закрыт.')
p('SHA-256 фактической платы:<br/>'+sha)
page()
h('Питание и reset: изменения R144')
table(['Узел','Фактическая реализация'],[
 ['U11','TPS389001DSER, TI DSE0006A WSON6, без EP. 1 SENSE,2 GND,3 MR=3V3,4 VDD,5 CT,6 RESET_N=ESP_EN.'],
 ['Порог и задержка','R95=16.5k / R96=10k,0.1%10ppm. C40=100nF на CT; C41=1nF C0G на SENSE. R17 pullup и J7 EN сохранены.'],
 ['Регулятор','R14=27.4k + R98=402R, R15=5.11k,0.1%10ppm. Номинал3.220352V.'],
 ['Режим','R97 FIT -> PWM после soft-start. R99 DNP. Никогда не ставить оба. Initial soft-start PFM сохраняется; idle consumption не измерен.'],
 ['Геометрия','Новые passives и U11 разведены; C15 bypass перенесён.16 старых медных объектов удалены,183 новых добавлены. USB, антенна, контур, J2/J3 сохранены.'],
 ['Корпус U11','Фактические Gerber меди, маски и пасты совпали с TI drawing4220552/B. Асимметричные левые SMD и правые NSMD площадки не заменять типовым footprint.']],[140,370])
p('Два новых via с недостаточным отступом от SMD сдвинуты; минимальный обычный via/SMD gap >=0.10 мм. Все номинальные annular rings >=0.15 мм. Подпись pin1 U11 имеет silk0.15 мм.')
p('Legacy EPD правило с неподдерживаемым =~ молча отключало custom rules. В R144 оно заменено точными именами сетей. Sentinel подтверждает реальное исполнение; внесённая ошибка оператора выявляется. Исторические ревизии сохранены.')
page()
h('Выполненные проверки')
table(['Метод','Результат для текущей R144'],[
 ['KiCad10.0.7','DRC0 / ERC0 / opens0 / parity0; все severity и track errors; refilled zones. Source hashes при проверке не изменились.'],
 ['Независимая медь','Четыре полных Gerber image сравнены с native copper. Gerbonara + Shapely:84 сети,0 shorts/opens/missing lands. Реальные внесённые разрез и мост выявлены.'],
 ['Изготовление','11 Gerber; PTH/NPTH и четыре USB slots;456 pad +384 via =840 IPC356 records; mask/paste/silk, BOM и120 top placements.'],
 ['Компоненты','141 refs,473 native pads,64 active-IC lands; exact MPN/polarity/pin maps.19 bare PCB, R67/R99 DNP. U11 OEM и J3 actual paste проверены.'],
 ['Питание и интерфейсы','Независимый MNA/corners и реальные fault fixtures. GPIO35-37 NC; straps3/45/46 NC; GPIO0 BOOT10k/SW2/J7. SD SPI с pullups; BMI0x68/INT1GPIO18.'],
 ['Слои и земля','16 enabled layers с уникальными именами.93 hidden references и134 hidden values перечислены. Нет unnamed layers/netless routed copper.14 FAST centerlines покрыты GND хотя бы на одном inner layer.'],
 ['Серверная проверка','Run38693384483 SUCCESS на точном исходнике. Неизменяемая R138:27 scopes и20 negative cases. ZIP SHA/CRC проверены.']],[140,370])
p('Это статические и вычислительные проверки. Не выполнены SPICE с точными macromodels, IBIS/field solver, физические FCT, USB compliance, EMI/ESD/RF и полный текущий корпус. Геометрия return path не является EM-моделью.')
page()
h('Расчётные запасы и оставшийся риск')
rows=[]
for a in st['life_and_solder_scenarios']:
 label={'initial_only':'Начальные допуски + TCR','initial_plus_0p1percent_solder_shift':'Дополнительно +/-0.1% solder','initial_plus_0p1percent_solder_plus_0p5percent_life_shift':'Дополнительно +/-0.5% life'}[a['scenario']]
 rows.append([label,f"{a['regulator_PWM_V'][0]:.6f}..{a['regulator_PWM_V'][1]:.6f} V",f"{1000*(a['regulator_PWM_V'][0]-a['maximum_rising_V']):.3f} mV",f"{1000*(3.3-a['regulator_PWM_V'][1]):.3f} mV"])
table(['Сценарий резисторов','PWM питание','Запас release','До max панели'],rows,[165,145,100,100])
p('Первый и solder-сценарий проходят проектные резервы50 мВ release и25 мВ до3.3 В. Последний life-сценарий не проходит; min falling threshold может быть ниже ESP3.0 В. Это объявленный worst-case сценарий, а не вероятность отказа или квалификация фактической партии.')
p('C40: номинальная задержка около107 мс; условный диапазон59..181 мс. Эффективная ёмкость и утечки не гарантированы этим расчётом. Проверить реальные ramps, dips, EN timing, ripple/overshoot/load, OFF back-power и idle PWM current.')
p('BQ24072T сохраняет зарядку при hard OFF; default high-Z USB100. USB100 без батареи не гарантирует старт. Нужны квалифицированный protected pack или battery simulator. На плате нет PCM и fuel gauge: измеряется switched ADC voltage proxy.')
p('Ток sense-делителя при номинальных3.220352 В составляет121.523 мкА дополнительно к потреблению supervisor. Это расчёт DC, а не измеренный idle бюджет платы.')
page()
h('Первые 1-2 платы, затем остальные')
table(['Этап','Критерий и запись'],[
 ['До запуска изготовления','FPC/корпус, protected pack/NTC, stackup/drill/fill-cap/stencil, BOM/CPL import и lifetime/dynamic risk disposition; воспроизводимый FCT binary.'],
 ['Первые1-2 сборки','AOI/X-ray/ICT, pin1/polarity,120 fitted top parts. R67/R99 DNP, R97 FIT. Остальные собирать после диагностики первых.'],
 ['Питание/reset','ESP3.0..3.6V, панель VCI2.2..3.3V включая пики. Ramps0.1ms..10s,100 cold starts и100 rapid cycles на каждый serial.'],
 ['ROM и память','UART/USB recovery;16MiB Quad flash,8MiB Octal PSRAM patterns. Начальный flash80MHz; без изменения eFuse.'],
 ['SD / BMI / EPD','SD hashes/hot removal/USB-MSC ownership. BMI INTERNAL_STATUS[3:0]==1, config/self-test/IRQ. Panel full/partial refresh и HV waveform.'],
 ['Совместная нагрузка','Wi-Fi TX + SD write + EPD при min battery/cold/hot; extrema напряжений/токов, L2 peak/RMS, switch/VGS и температуры.'],
 ['OFF и заряд','USB/UART back-power; USB100/500/suspend authorization; PCM и NTC fault/temperature/thermal lag.'],
 ['Каждый serial','Source/BOM/firmware hash, приборы и условия, raw logs/waveforms, численные min/max. Отсутствие результата = NOT RUN.']],[140,370])
p('100 циклов - критерий bring-up, а не ресурсная сертификация. После первого отказа остановить продолжение сборки и выяснить причину. Этот план не является записью успешного испытания или заказом.')
page()
h('Оставшиеся согласования и пакет')
p('GoodDisplay/Felix подтвердил pin5 VDHR=VSH2, bend1-1.5 мм и glass gap>=2 мм. Применяем bend>=1.5 мм. Его подтверждение присланного DIANWEI не утверждает наш Hirose footprint.')
p('FPC панели0.25..0.35 мм против Hirose0.27..0.33 мм: номинал совпадает, полный допуск не покрыт. Нужны actual-lot acceptance толщины/ширины/finger/coverlay, folded pin1, GDEM/GDEY CAD identity и доступ к защёлке.')
p('Процесс:84 nominal0.2 мм bores на1.6 мм,384 vias и шесть resin-fill/copper-cap requests. Actual90-ohm USB stackup, допуски сверления/регистрации, void/flatness, короткие USB stakes и общий stencil/reflow требуют одобрения. TI U11 stencil example0.125 мм, Hirose recommendation0.10 мм; peak Hirose<=250C, >230C<=60s.')
p('EPD: L2=47uH, typical Isat1.1A @25C и30% L drop. D1-D3 MBR0530T1G30V/0.5A, Q1 IRLML6346. Hot peak/RMS, overshoot, R37 pulse heating и MLCC differential Ceff ещё не измерены.')
p('01_fabrication:11 Gerber, drill/maps, IPC356. 02_assembly:BOM/CPL CSV+XLSX, all-pad map/process requests. 03_drawings:этот обзор,10 layer/assembly и5 schematic pages. 04_editable_kicad:68 файлов. 05_verification:фактические отчёты и серверная сверка. 06_qualification:процедуры и открытые пункты.')
p('Первичные данные: TI TPS3890 /TPS63802 /BQ24072T; supplied GDEY0397T81P pp5/6/8/19; Hirose EDC-159714-50-08 /ELC4-159714-04; Espressif WROOM v1.8; Bosch BMI270 DS000-08. Ссылки/хеши/страницы указаны в отчётах. Supplier PDF/CAD не включены в публичный пакет.')
ledger=json.loads((repo/'docs/DEVELOPMENT_HOURS_READER.json').read_text())
p(f"Подтверждённый учёт разработки Reader: минимум{ledger['logged_lower_bound_hours']:.2f} ч. Неизмеренные прежние сеансы и паузы не добавлены.")
p('<b>R144 - проверенный инженерный пакет для review. Изготовление и гарантированный запуск не заявлены.</b>')
def decor(c,doc):
 c.saveState();c.setFont('DejaVu',8);c.setFillColor(colors.HexColor('#607589'));c.drawString(42,22,'ENKU Base R144 / NO FAB / physical tests NOT RUN');c.drawRightString(A4[0]-42,22,str(doc.page))
 if logo.exists():c.drawImage(str(logo),A4[0]-96,A4[1]-49,width=54,height=28,preserveAspectRatio=True,anchor='c',mask='auto')
 c.restoreState()
doc=SimpleDocTemplate(str(out/'ENKU_R144_Board_Review_NO_FAB.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=58,bottomMargin=42,title='ENKU Base R144 board review - NO FAB',author='ENKU',subject='Actual source '+sha);doc.build(story,onFirstPage=decor,onLaterPages=decor)
for f in out.glob('*.pdf'):
 z=fitz.open(f);print(f.name,len(z))
