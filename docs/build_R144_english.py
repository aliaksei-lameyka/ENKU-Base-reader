"""Verified source plots and English board review, no fabricated test results."""
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
repo=Path(__file__).resolve().parents[1];base=repo.parent;v=Path(sys.argv[1]).resolve();out=repo/'hardware/mainboard/r144/pcbway_en/03_drawings';out.mkdir(parents=True,exist_ok=True)
board_only=True
logo=repo/'docs/assets/enku-official-logo.png';native=fitz.open(repo/'hardware/mainboard/r144/pcbway/03_drawings/ENKU_R144_Layers_Assembly_NO_FAB.pdf' if board_only else base/'r144-work/native-pdfs/layers.pdf');sch=fitz.open(repo/'hardware/mainboard/r144/pcbway/03_drawings/ENKU_R144_Schematics_NO_FAB.pdf' if board_only else base/'r144-work/native-pdfs/schema-clean-new.pdf');g=json.loads((v/'geometry.json').read_text());er=json.loads((v/'independent_electrical_R144.json').read_text());lv=json.loads((v/'layer_visibility_audit_R144.json').read_text());gr=json.loads((v/'independent_Gerber_graph_R144.json').read_text());rq=json.loads((v/'requested_review_R144.json').read_text());sha=hashlib.sha256((repo/'hardware/mainboard/r144/kicad/enku-mainboard-r0.1.kicad_pcb').read_bytes()).hexdigest()
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
 plots(native,repo/'hardware/mainboard/r144/pcbway/03_drawings/ENKU_R144_Layers_Assembly_NO_FAB.pdf',names)
 plots(sch,repo/'hardware/mainboard/r144/pcbway/03_drawings/ENKU_R144_Schematics_NO_FAB.pdf',['Root project','Power','MCU and IO','E-paper HV','Connectors'],True)
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
p('15 October 2026. Engineering review package for the first 5-10 boards. <b>NO FAB. Physical tests: NOT RUN.</b>')
picture(0,base/'r144-en-work/board-top.png',250,390)
p('59 x 101 x 1.6 mm, four copper layers. ESP32-S3-WROOM-1-N16R8, GDEY0397T81P / SSD1677, microSD SPI and BMI270. BQ24072T power path + TPS63802 supply.')
p('R144 redesigns the supply and reset circuit. Complete local and server checks passed. Verified source: 609f8ac00357b9b0c6b3c43c381469c498453a11. GitHub Actions run: 38693384483. Manufacturing release remains open.')
p('Actual PCB SHA-256:<br/>'+sha)
page()
h('Supply and reset: R144 changes')
table(['Circuit','Actual implementation'],[
 ['U11','TPS389001DSER, TI DSE0006A WSON-6, no exposed pad. 1 SENSE, 2 GND, 3 MR=3V3, 4 VDD, 5 CT, 6 RESET_N=ESP_EN.'],
 ['Threshold and delay','R95=16.5k / R96=10k, 0.1%, 10ppm/K. C40=100nF on CT; C41=1nF C0G on SENSE. Existing R17 pullup and J7 EN access retained.'],
 ['Regulator','R14=27.4k + R98=402R, R15=5.11k, 0.1%, 10ppm/K. Nominal output: 3.220352V.'],
 ['Operating mode','R97 FIT selects PWM after soft-start. R99 DNP. Never populate both. Initial converter soft-start still uses PFM; idle consumption is unmeasured.'],
 ['Layout','New passives and U11 routed; C15 bypass relocated. 16 old copper objects removed, 183 new objects added. USB, antenna exclusion, outline and J2/J3 retained.'],
 ['U11 footprint','Actual copper, mask and paste Gerbers match TI drawing 4220552/B. Preserve the asymmetric left SMD and right NSMD lands; do not substitute a generic footprint.']],[140,370])
p('Two new vias were moved to correct inadequate separation from SMD lands. Ordinary via-to-SMD gap is at least 0.10mm; all nominal annular rings are at least 0.15mm. The U11 pin-1 silkscreen marker uses a 0.15mm stroke.')
p('An unsupported =~ operator in the legacy EPD rule silently disabled custom rules. R144 uses exact net names. A sentinel proves actual rule execution, and an injected operator fault is detected. Historical revisions remain unchanged.')
page()
h('Completed checks')
table(['Method','Result for the actual R144 source'],[
 ['KiCad 10.0.7','DRC 0 / ERC 0 / opens 0 / schematic parity 0. All severities and track errors included; zones refilled. Source hashes unchanged during acceptance.'],
 ['Independent copper','All four complete Gerber images compared with native copper. Gerbonara + Shapely: 84 named nets, no shorts, opens or missing lands. Injected physical copper cut and bridge detected.'],
 ['Manufacturing exports','11 Gerber layers; separate PTH/NPTH drills and four USB slots. 456 pad + 384 via = 840 IPC356 records. Mask, paste, silk, BOM and 120 top placements verified.'],
 ['Components','141 references, 473 native pads, 64 active-IC lands. Exact MPNs, polarity and pin maps checked. 19 bare-PCB entries; R67/R99 DNP. U11 OEM lands and actual J3 paste checked.'],
 ['Power and interfaces','Independent MNA/corner calculations and effective fault fixtures. GPIO35-37 NC; straps GPIO3/45/46 NC. GPIO0 BOOT has 10k/SW2/J7. SD SPI pullups; BMI address 0x68, INT1 GPIO18.'],
 ['Layers and returns','16 uniquely named enabled layers. 93 hidden reference fields and 134 hidden values inventoried. No unnamed layers or netless routed copper. All 14 FAST-net centerlines have GND projection on at least one inner layer.'],
 ['Server verification','Run 38693384483 SUCCESS on the exact source. Immutable R138: 27 scopes and 20 effective negative cases. Downloaded artifact SHA and ZIP CRC verified.']],[140,370])
p('These are static and computational checks. Exact-macromodel SPICE, IBIS/field-solver analysis, physical FCT, USB compliance, EMI/ESD/RF tests and the complete current enclosure have not been qualified. Geometric return-path coverage is not an electromagnetic simulation.')
page()
h('Calculated margins and remaining risk')
rows=[]
for a in st['life_and_solder_scenarios']:
 label={'initial_only':'Initial tolerance + TCR','initial_plus_0p1percent_solder_shift':'Additional +/-0.1% solder shift','initial_plus_0p1percent_solder_plus_0p5percent_life_shift':'Further +/-0.5% life shift'}[a['scenario']]
 rows.append([label,f"{a['regulator_PWM_V'][0]:.6f}..{a['regulator_PWM_V'][1]:.6f} V",f"{1000*(a['regulator_PWM_V'][0]-a['maximum_rising_V']):.3f} mV",f"{1000*(3.3-a['regulator_PWM_V'][1]):.3f} mV"])
table(['Resistor scenario','PWM supply','Reset release margin','Below panel maximum'],rows,[165,145,100,100])
p('The initial and solder-shift scenarios meet the project reserves of 50mV for reset release and 25mV below the panel 3.3V limit. The final life-shift scenario does not; its minimum falling threshold can be below the ESP module 3.0V minimum. This is a declared adverse-corner scenario, not a failure probability or actual-lot qualification.')
p('C40 nominal reset delay is about 107ms; the conditional scenario range is 59..181ms. This calculation does not guarantee effective capacitance or leakage. Measure actual ramps, dips, EN timing, ripple, overshoot, load steps, OFF-state back-power and PWM idle current.')
p('BQ24072T charging remains powered with the hard reader switch OFF. High-impedance MCU defaults select USB100. USB100 without a battery does not guarantee startup. Use a qualified protected pack or battery simulator. The board has no battery PCM or fuel gauge; its switched ADC measures a battery-voltage proxy.')
p('At the nominal 3.220352V, the sense divider draws 121.523uA in addition to supervisor consumption. This is a DC calculation, not a measured board idle-current budget.')
page()
h('First 1-2 boards, then the remainder')
table(['Stage','Acceptance and recorded evidence'],[
 ['Before manufacture','Resolve FPC/enclosure, protected pack/NTC, stackup/drill/fill-cap/stencil, BOM/CPL import, lifetime/dynamic risk disposition and a reproducible FCT binary.'],
 ['First 1-2 assemblies','AOI/X-ray/ICT, pin-1 and polarity, 120 fitted top parts. R67/R99 DNP; R97 FIT. Diagnose the first units before assembling the remainder.'],
 ['Supply and reset','ESP 3.0..3.6V and panel VCI 2.2..3.3V, including peaks. Ramps 0.1ms..10s, 100 cold starts and 100 rapid cycles on each serial number.'],
 ['ROM and memory','UART/USB recovery; 16MiB Quad flash and 8MiB Octal PSRAM patterns. Conservative initial flash clock: 80MHz. No eFuse changes.'],
 ['SD / BMI / EPD','SD hashes, removal and exclusive USB-MSC ownership. BMI INTERNAL_STATUS[3:0]==1, configuration, self-test and IRQ. Panel full/partial refresh and HV captures.'],
 ['Combined load','Wi-Fi TX + SD write + EPD at minimum battery and approved cold/hot conditions. Capture voltage/current extrema, L2 peak/RMS current, switch/VGS and temperatures.'],
 ['OFF and charging','USB/UART back-power, USB100/500/suspend authorization, PCM response and NTC temperature/fault/thermal-lag tests.'],
 ['Every serial number','Source/BOM/firmware hashes, instruments and conditions, raw logs/waveforms, numerical min/max and disposition. Missing results remain NOT RUN.']],[140,370])
p('100 cycles are a bring-up criterion, not lifetime certification. Stop further assembly after the first failure and establish its cause. This procedure is not a record of successful physical testing or a manufacturing order.')
page()
h('Open qualifications and package contents')
p('GoodDisplay/Felix confirmed pin 5 VDHR=VSH2, bend radius 1-1.5mm and glass-to-bend clearance at least 2mm. Use bend radius at least 1.5mm. His confirmation of the supplied DIANWEI connector does not approve the different installed Hirose footprint.')
p('Panel FPC thickness is 0.25..0.35mm versus Hirose 0.27..0.33mm. Nominal agreement does not cover the full tolerance. Obtain actual-lot thickness, width, finger/coverlay acceptance, folded pin-1 alignment, GDEM/GDEY CAD identity and latch-access evidence.')
p('Process: 84 nominal 0.20mm bores in a 1.6mm board, 384 vias and six resin-fill/copper-cap requests. Actual 90-ohm USB stackup, drilling/registration tolerances, void/flatness limits, short USB stakes and common stencil/reflow require approval. TI U11 stencil example: 0.125mm; Hirose recommendation: 0.10mm. Hirose peak at most 250C; time above 230C at most 60s.')
p('EPD: L2=47uH, typical Isat 1.1A at 25C and 30% inductance reduction. D1-D3 are MBR0530T1G, 30V/0.5A; Q1 is IRLML6346. Hot peak/RMS current, overshoot, R37 pulse heating and differential-voltage MLCC effective capacitance remain unmeasured.')
p('01_fabrication: 11 Gerbers, drills/maps and IPC356. 02_assembly: BOM/CPL CSV+XLSX, complete pad map and process requests. 03_drawings: this review, 10 layer/assembly pages and 5 schematic pages. 04_editable_kicad: 68 source files. 05_verification: actual reports and server comparison. 06_qualification: procedures and open items.')
p('Primary references: TI TPS3890 / TPS63802 / BQ24072T; supplied GDEY0397T81P pp5/6/8/19; Hirose EDC-159714-50-08 / ELC4-159714-04; Espressif WROOM v1.8; Bosch BMI270 DS000-08. Links, hashes and page references are in the reports. Supplier PDFs/CAD are omitted from the public package.')
ledger=json.loads((repo/'docs/DEVELOPMENT_HOURS_READER.json').read_text())
p(f"Confirmed recorded Reader development time: at least {ledger['logged_lower_bound_hours']:.2f} hours. Unmeasured earlier sessions and idle gaps are excluded.")
p('<b>R144 is a verified engineering review package. Manufacturing release and guaranteed prototype startup are not claimed.</b>')
def decor(c,doc):
 c.saveState();c.setFont('DejaVu',8);c.setFillColor(colors.HexColor('#607589'));c.drawString(42,22,'ENKU Base R144 / NO FAB / physical tests NOT RUN');c.drawRightString(A4[0]-42,22,str(doc.page))
 if logo.exists():c.drawImage(str(logo),A4[0]-96,A4[1]-49,width=54,height=28,preserveAspectRatio=True,anchor='c',mask='auto')
 c.restoreState()
doc=SimpleDocTemplate(str(out/'ENKU_R144_Board_Review_EN_NO_FAB.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=58,bottomMargin=42,title='ENKU Base R144 English board review - NO FAB',author='ENKU',subject='Actual source '+sha);doc.build(story,onFirstPage=decor,onLaterPages=decor)
for f in out.glob('*.pdf'):
 z=fitz.open(f);print(f.name,len(z))
