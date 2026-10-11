"""One-time controlled R129 -> R130 BAT-REV3 change; run with native pcbnew10.

Preserve all accepted source. Correct the Laird land interpretation and move
one tented EPD via out of its solder window; two-wire PH battery plus separate
bare-board sensor terminals. This is engineering source, never a fab release.
"""
import gzip, hashlib, json, re, sys, uuid
from pathlib import Path
import pcbnew as p

r=Path(sys.argv[1]).resolve(); before=Path(sys.argv[2]).resolve(); primary=Path(sys.argv[3]).resolve(); c=r/'checks'
filename='enku-mainboard-r0.1.kicad_pcb'
source_sha='bab3cda1faa40bb2535f2d3eefe6ef0a9f43593b82577843cfe54f6d98da013c'
assert hashlib.sha256((before/filename).read_bytes()).hexdigest()==source_sha
assert hashlib.sha256((r/filename).read_bytes()).hexdigest()==source_sha
b=p.LoadBoard(str(r/filename)); fps={f.GetReference():f for f in b.GetFootprints()}
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def state(a):return dict(uuid=a.m_Uuid.AsString(),ref=a.GetParentFootprint().GetReference(),number=a.GetNumber(),net=a.GetNetname(),pos=xy(a.GetPosition()),size=xy(a.GetSize()),drill=xy(a.GetDrillSize()),angle=a.GetOrientationDegrees(),shape=a.GetShape(),attribute=a.GetAttribute(),layers=list(a.GetLayerSet().Seq()),roundrect_radius_mm=p.ToMM(a.GetRoundRectCornerRadius()),mask=a.GetLocalSolderMaskMargin(),paste=a.GetLocalSolderPasteMargin(),paste_ratio=a.GetLocalSolderPasteMarginRatio())
old={a.m_Uuid.AsString():state(a) for f in fps.values() for a in f.Pads()}
fields={};lib_changes={}
def set_fields(ref,values):
 f=fps[ref];fields.setdefault(ref,{}).update(values)
 for key,value in values.items():
  if key=='Footprint':continue
  exists=f.HasField(key);f.SetField(key,value);a=f.GetField(key)
  if not exists:a.SetLayer(p.F_Fab);a.SetPosition(f.GetPosition());a.SetTextSize(vec(.8,.8));a.SetVisible(False)
def save_variant(ref,name,description):
 f=fps[ref];f.SetFPID(p.LIB_ID('ENKU',name));f.SetLibDescription(description)
 lib_changes[ref]='ENKU:'+name;fields.setdefault(ref,{})['Footprint']='ENKU:'+name
 clone=p.FOOTPRINT(f);clone.SetOrientationDegrees(0);clone.SetPosition(vec(0,0));clone.SetReference('REF**');clone.SetPath(p.KIID_PATH())
 for a in clone.Pads():a.SetNetCode(0)
 p.FootprintSave(str(r/'ENKU.pretty'),clone)

# Laird RevA p2: G=4.2 along each land, T=1.4 across, H=2.3 BETWEEN lands.
for a in fps['L2'].Pads():
 assert a.GetNumber() in ['1','2'] and xy(a.GetSize())==[1.4,2.3]
 a.SetSize(vec(1.4,4.2));a.SetPosition(vec(56.15 if a.GetNumber()=='1' else 59.85,43))
save_variant('L2','TYS5040_LAIRD_G42_T14_H23','Laird TYS5040 RevA p2 rotated90deg: G4.2 T1.4 H2.3; two1.4x4.2 lands at +/-1.85; assembly unqualified')
moves={
 '0bad18f5-f207-4458-93c2-434f62be69d3':([56.6,44.8],[57.4,44.8]),
 '7025ffc7-3c2c-4ce4-aaf9-d3305f55e2c7':([56.6,44.8],[57.4,44.8]),
 '28a4eb52-09ce-4819-b3e5-e6d46adb5e02':([56.6,44.8],[57.4,44.8])}
move_records=[]
for t in b.GetTracks():
 u=t.m_Uuid.AsString()
 if u not in moves:continue
 a,z=moves[u];assert t.GetNetname()=='EPD_VCI' and xy(t.GetStart())==a
 old_end=xy(t.GetEnd());layer=t.GetLayer()
 if isinstance(t,p.PCB_VIA):t.SetPosition(vec(*z))
 else:t.SetStart(vec(*z))
 move_records.append(dict(uuid=u,net='EPD_VCI',before=[a,old_end],after=[xy(t.GetStart()),xy(t.GetEnd())],layer=layer))
assert len(move_records)==3

# Load the actual official KiCad footprint, retaining R129 signal and bracket UUIDs.
name='JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal'
raw=(primary/'PH2_official.kicad_mod').read_text()
raw=re.sub(r'\n  \(model .*?\n  \)\n', '\n', raw, flags=re.S)
(r/'ENKU.pretty'/f'{name}.kicad_mod').write_text(raw)
oldj=fps['J1'];oldjp=list(oldj.Pads());ts=next(a for a in oldjp if a.GetNumber()=='3')
newj=p.FootprintLoad(str(r/'ENKU.pretty'),name);assert newj
newj.SetFPID(p.LIB_ID('ENKU',name));newj.SetReference('J1');newj.SetValue('1S LiPo PCM / PH-2');newj.SetAttributes(p.FP_SMD)
newj.SetUuidDirect(oldj.m_Uuid);newj.SetPath(oldj.GetPath());newj.SetPosition(vec(69.8,94.5));newj.SetOrientationDegrees(90)
for a in newj.Pads():
 if a.GetNumber() in ['1','2']:oldpad=next(z for z in oldjp if z.GetNumber()==a.GetNumber())
 else:oldpad=min((z for z in oldjp if z.GetNumber()=='MP'),key=lambda z:abs(xy(z.GetPosition())[1]-xy(a.GetPosition())[1]))
 a.SetUuidDirect(oldpad.m_Uuid);a.SetNet(oldpad.GetNet())
newj.Reference().SetVisible(oldj.Reference().IsVisible());newj.Reference().SetPosition(oldj.Reference().GetPosition());newj.Reference().SetTextSize(oldj.Reference().GetTextSize());newj.Reference().SetTextAngle(oldj.Reference().GetTextAngle());newj.Reference().SetLayer(oldj.Reference().GetLayer())
newj.Value().SetVisible(False)

# Clip the two official north-edge silk lines now intersecting the separate TS bar.
def intersects_box(a,z,lo,hi):
 d=[z[i]-a[i] for i in range(2)];l,h=0.,1.
 for i in range(2):
  if abs(d[i])<1e-9:
   if not lo[i]<=a[i]<=hi[i]:return False
  else:
   t1,t2=sorted([(lo[i]-a[i])/d[i],(hi[i]-a[i])/d[i]]);l=max(l,t1);h=min(h,t2)
 return l<=h

b.Remove(oldj);b.Add(newj);fps['J1']=newj
set_fields('J1',{'Description':'Protected standard TWO-wire LiPo; separate J8 cell-temperature sensor','Battery Interface':'PHR-2: cavity1 VBAT+, cavity2 GND; battery wire colors do not prove polarity','Mating Housing':'JST PHR-2','Crimp Contact':'JST SPH-002T-P0.5S; AWG30-24, insulation0.8-1.5mm; tooling/pull test pending'})
save_variant('J1',name,'BAT-REV3 JST PH2 nominal mounting-side drawing; opening +boardX; preserved R129 VBAT/GND copper; polarity/assembly unqualified')

# Sensor remains on the PCB during battery replacement. No paste, no purchased connector.
j8=p.FOOTPRINT(b);j8.SetReference('J8');j8.SetValue('External cell NTC / hand solder');j8.SetFPID(p.LIB_ID('ENKU','NTC_WIRE_TERMINALS_TS_BAR_GND_NO_PASTE'))
j8.SetUuidDirect(p.KIID('daaa0800-0000-4000-8000-000000000008'));j8.SetAttributes(p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES);j8.SetPosition(vec(66.95,91.5));j8.SetOrientationDegrees(0)
j8.Reference().SetPosition(vec(63.0,88.6));j8.Reference().SetLayer(p.F_SilkS);j8.Reference().SetTextSize(vec(.8,.8));j8.Reference().SetTextThickness(p.FromMM(.1));j8.Value().SetVisible(False)
layers=p.LSET();layers.AddLayer(p.F_Cu);layers.AddLayer(p.F_Mask)
for number,pos,net in [('1',[66.95,91.5],ts.GetNet()),('2',[64.8,89.3],next(a.GetNet() for a in newj.Pads() if a.GetNumber()=='2'))]:
 a=p.PAD(j8);a.SetNumber(number);a.SetAttribute(p.PAD_ATTRIB_CONN);a.SetShape(p.PAD_SHAPE_CIRCLE);a.SetSize(vec(1.5,1.5));a.SetDrillSize(vec(0,0));a.SetPosition(vec(*pos));a.SetLayerSet(layers);a.SetNet(net)
 
 if number=='1':a.SetShape(ts.GetShape());a.SetSize(ts.GetSize());a.SetOrientation(ts.GetOrientation());a.SetRoundRectRadiusRatio(ts.GetRoundRectRadiusRatio())
 a.SetUuidDirect(ts.m_Uuid if number=='1' else p.KIID('daaa0800-0000-4000-8000-000000000082'));j8.Add(a)
b.Add(j8);fps['J8']=j8
set_fields('J8',{'Assembly':'BARE_PCB','Sensor MPN Candidate':'Semitec 103JT-050','Sensor Status':'10k +/-1%, B25/85 3435K +/-1%; direct TS hot limit is NOT qualified for0-45C pack','Assembly Process':'Hand solder insulated sensor tails; sensor film stays <150C; minimum7mm bend distance, separate strain relief required','Thermal Attachment':'Retained flat against replaceable pouch, insulation/no pressure; mechanical retention and replacement test pending'})
save_variant('J8','NTC_WIRE_TERMINALS_TS_BAR_GND_NO_PASTE','Bare sensor terminals: pin1 original3.5x1mm global TS bar; pin2 dia1.5mm GND at(-2.15,-2.2); no solder paste/BOM/CPL; insulated fanout and manual termination unqualified')
route=p.PCB_TRACK(b);route.SetStart(vec(64.8,89.3));route.SetEnd(vec(66,88.9));route.SetWidth(p.FromMM(.25));route.SetLayer(p.F_Cu);route.SetNet(next(a.GetNet() for a in newj.Pads() if a.GetNumber()=='2'));route.SetUuidDirect(p.KIID('daaa0800-0000-4000-8000-000000000083'));b.Add(route)
via=p.PCB_VIA(b);via.SetPosition(vec(66,88.9));via.SetWidth(p.F_Cu,p.FromMM(.5));via.SetDrill(p.FromMM(.3));via.SetViaType(p.VIATYPE_THROUGH);via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(route.GetNet());via.SetUuidDirect(p.KIID('daaa0800-0000-4000-8000-000000000084'));b.Add(via)

parts={
 'J1':('JST','S2B-PH-SM4-TB(LF)(SN)','https://www.jst-mfg.com/product/pdf/eng/ePH.pdf'),
 'J2':('Hirose','DM3AT-SF-PEJM5','https://www.hirose.com/en/product/p/CL0609-0031-0-00'),
 'J5':('GCT','USB4105-GF-A-120','https://gct.co/connector/usb4105'),
 'L1':('Murata','DFE201612E-R47M=P2','https://pim.murata.com/asset/pim4/inductor/J%28E%29TE243A-0006_PDF_INDUCTOR'),
 'L2':('Laird Performance Materials','TYS5040470M-10','https://www.laird.com/sites/default/files/tys5040-series-datasheet.pdf'),
 'Q1':('Infineon','IRLML6346TRPBF','https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlml6346-datasheet-en.pdf'),
 'Q2':('Alpha & Omega Semiconductor','AO3401A','https://www.aosmd.com/sites/default/files/res/data_sheets/AO3401A.pdf'),
 'SW1':('G-Switch','MK-12C03-G015','https://cdn.semikey.com/upload/pdfs/a6/85/a685b04beffe80627230619bb0c8ae8e.pdf')}
for ref in ['SW3','SW4','SW5','SW6']:parts[ref]=('E-Switch','TL3340AF160QG','https://configured-product-images.s3.amazonaws.com/2D/specs/TL3340AF160QG.pdf')
for ref,(maker,mpn,url) in parts.items():set_fields(ref,{'Manufacturer':maker,'MPN':mpn,'Datasheet':url,'Assembly':'FIT'})
set_fields('U3',{'Charge Profile':'HOLD BAT-REV3: 4.2V / 500mA IN / nominal300mA; RevB timer360min incompatible with assured full2500mAh recharge; direct3435K NTC hot threshold exceeds45C','Battery Qualification':'No battery/thermal/current/PCM approval; no manufacture'})

def block(t,s):
 d=0;q=e=False
 for i in range(s,len(t)):
  x=t[i]
  if q:
   if e:e=False
   elif x=='\\':e=True
   elif x=='"':q=False
  elif x=='"':q=True
  elif x=='(':d+=1
  elif x==')':
   d-=1
   if not d:return t[s:i+1],i+1
 raise ValueError('Unbalanced source')
def prop(t,k,v):
 t,n=re.subn(r'(\(property "'+re.escape(k)+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(v),t,count=1)
 if not n:t=t[:-1]+'\n\t\t(property '+json.dumps(k)+' '+json.dumps(v)+' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
 return t
symbol_changes={};sheet_edits={}
# Preserve the old BAT3 symbol for historical checkpoints; add a BAT2 variant.
lib=(r/'ENKU.kicad_sym').read_text();bat3,_=block(lib,lib.index('(symbol "BAT3"'))
bat2=bat3.replace('BAT3','BAT2').replace('1S LiPo + NTC','1S LiPo PCM / PH-2').replace('Connector_Generic:Conn_01x03','ENKU:'+name)
start=bat2.index('(pin passive line (at 9.525 -1.27');_,end=block(bat2,start);bat2=bat2[:start]+bat2[end:]
ntc='''(symbol "NTC_WIRE2"
 (pin_names (offset 0.5)) (exclude_from_sim no) (in_bom no) (on_board yes)
 (property "Reference" "J" (at 0 4 0) (effects (font (size .95 .95))))
 (property "Value" "External cell NTC / hand solder" (at 0 -4 0) (effects (font (size .95 .95))))
 (property "Footprint" "ENKU:NTC_WIRE_TERMINALS_TS_BAR_GND_NO_PASTE" (at 0 0 0) (effects (font (size .95 .95)) (hide yes)))
 (symbol "NTC_WIRE2_0_1"
  (rectangle (start -6.985 2) (end 6.985 -2) (stroke (width .254) (type default)) (fill (type background)))
  (pin passive line (at -9.525 0 0) (length 2.54) (name "TS/MR" (effects (font (size .95 .95)))) (number "1" (effects (font (size .95 .95)))))
  (pin passive line (at 9.525 0 180) (length 2.54) (name "GND" (effects (font (size .95 .95)))) (number "2" (effects (font (size .95 .95)))))
 ))'''
lib=lib.rstrip();assert lib.endswith(')');lib=lib[:-1]+'\n'+bat2+'\n'+ntc+'\n)\n';(r/'ENKU.kicad_sym').write_text(lib)
for sheet in r.glob('*.kicad_sch'):
 t=sheet.read_text();original=t;edits={}
 if sheet.name=='power.kicad_sch':
  pos=t.index('(lib_symbols');libblock,end=block(t,pos)
  libblock=libblock[:-1]+'\n'+bat2.replace('(symbol "BAT2"','(symbol "ENKU:BAT2"',1)+'\n'+ntc.replace('(symbol "NTC_WIRE2"','(symbol "ENKU:NTC_WIRE2"',1)+'\n)'
  t=t[:pos]+libblock+t[end:]
  i=t.index('(property "Reference" "J1"');s=t.rfind('(symbol (lib_id',0,i);sym,e=block(t,s)
  sym=sym.replace('ENKU:BAT3','ENKU:BAT2');sym=prop(sym,'Value','1S LiPo PCM / PH-2');sym=prop(sym,'Description','Protected standard TWO-wire LiPo; separate J8 cell-temperature sensor')
  sym=re.sub(r'\n\s*\(pin "3" \(uuid "[^"]+"\)\)', '',sym,count=1);t=t[:s]+sym+t[e:]
  i=t.index('(global_label "BAT_TS" (shape output) (at 144.78 127');sym,e=block(t,i);t=t[:i]+t[e:]
  # Dedicated sensor schematic uses explicit net labels, no false on-board NTC body.
  sid='daaa0800-0000-4000-8000-000000000008';inst=f'''(symbol (lib_id "ENKU:NTC_WIRE2") (at 135.255 148.59 0) (unit 1) (exclude_from_sim no) (in_bom no) (on_board yes) (dnp no) (uuid "{sid}")
   (property "Reference" "J8" (at 135.255 143.59 0) (effects (font (size .95 .95))))
   (property "Value" "External cell NTC / hand solder" (at 135.255 153.59 0) (effects (font (size .95 .95))))
   (property "Footprint" "ENKU:NTC_WIRE_TERMINALS_TS_BAR_GND_NO_PASTE" (at 135.255 148.59 0) (effects (font (size .95 .95)) (hide yes)))
   (pin "1" (uuid "daaa0800-0000-4000-8000-000000000091"))
   (pin "2" (uuid "daaa0800-0000-4000-8000-000000000092"))
   (instances (project "enku-mainboard-r0.1" (path "/10000000-0000-4000-8000-000000000001/{sid}" (reference "J8") (unit 1)))))'''
  for k,v in fields['J8'].items():inst=prop(inst,k,v)
  t=t.rstrip();t=t[:-1]+'\n'+inst+'''
   (global_label "BAT_TS" (shape output) (at 125.73 148.59 0) (effects (font (size .95 .95)) (justify left bottom)) (uuid "daaa0800-0000-4000-8000-000000000093"))
   (global_label "GND" (shape output) (at 144.78 148.59 180) (effects (font (size .95 .95)) (justify right bottom)) (uuid "daaa0800-0000-4000-8000-000000000094"))
   (text "BAT-REV3 HOLD: actual NTC retained on CELL. No fixed resistor. 3435K direct TS needs0-45C protection redesign. 300mA/6h timer not qualified for2-2.5Ah." (at 185 170 0) (effects (font (size 1 1)) (justify left)) (uuid "daaa0800-0000-4000-8000-000000000095"))
 )\n'''
 for ref,values in fields.items():
  marker='(property "Reference" "'+ref+'"'
  if marker not in t:continue
  i=t.index(marker);s=t.rfind('(symbol (lib_id',0,i);sym,e=block(t,s)
  for k,v in values.items():sym=prop(sym,k,v)
  t=t[:s]+sym+t[e:];edits[ref]=values
 if t!=original:
  (c/('source_R129_'+sheet.name+'.gz')).write_bytes(gzip.compress(original.encode(),mtime=0));sheet.write_text(t);sheet_edits[sheet.name]=edits
(c/'source_R129_ENKU.kicad_sym.gz').write_bytes(gzip.compress((before/'ENKU.kicad_sym').read_bytes(),mtime=0))
p.SaveBoard(str(r/filename),b)

model_block='(model "${KIPRJMOD}/../mechanical/models/JST_PH2_CONSERVATIVE_NOMINAL_ENVELOPE.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'
def clip_north_silk(text):
 for m in list(re.finditer(r'\(fp_line',text))[::-1]:
  item,end=block(text,m.start())
  if '(layer "F.SilkS")' not in item:continue
  a=re.search(r'\(start ([^ ]+) ([^)]+)\)',item);z=re.search(r'\(end ([^ ]+) ([^)]+)\)',item)
  if intersects_box([float(a[1]),float(a[2])],[float(z[1]),float(z[2])],[2.3,-4.8],[3.7,-.9]):text=text[:m.start()]+text[end:]
 return text
pcb_text=(r/filename).read_text();start=pcb_text.index('(footprint "ENKU:'+name+'"');ftext,end=block(pcb_text,start);ftext=clip_north_silk(ftext);ftext=ftext[:-1]+'\n'+model_block+'\n)';pcb_text=pcb_text[:start]+ftext+pcb_text[end:];start=pcb_text.index('(footprint "ENKU:TL3340');
for m in re.finditer(r'\(footprint ',pcb_text):
 fblock,end=block(pcb_text,m.start())
 if '(property "Reference" "SW6"' in fblock:
  field_start=fblock.index('(property "Reference" "SW6"');field,fe=block(fblock,field_start);field=re.sub(r'\(at [^)]*\)', '(at -3.9 0 0)',field,count=1);fblock=fblock[:field_start]+field+fblock[fe:];pcb_text=pcb_text[:m.start()]+fblock+pcb_text[end:];break
else:raise AssertionError('SW6 reference absent')
for m in re.finditer(r'\(footprint ',pcb_text):
 fblock,end=block(pcb_text,m.start())
 if '(property "Reference" "C12"' in fblock:
  fs=fblock.index('(property "Reference" "C12"');field,fe=block(fblock,fs);field=re.sub(r'\(at [^)]*\)', '(at 0.4 -3.6 0)',field,count=1);fblock=fblock[:fs]+field+fblock[fe:];pcb_text=pcb_text[:m.start()]+fblock+pcb_text[end:];break
(r/filename).write_text(pcb_text)
lib_file=r/'ENKU.pretty'/f'{name}.kicad_mod';lib_text=clip_north_silk(lib_file.read_text().rstrip());lib_file.write_text(lib_text[:-1]+'\n'+model_block+'\n)\n')

new={a.m_Uuid.AsString():state(a) for f in fps.values() for a in f.Pads()}
unchanged=['enku-mainboard-r0.1.kicad_pro','enku-mainboard-r0.1.kicad_dru','fp-lib-table','sym-lib-table']
unchanged += [x.name for x in before.glob('*.kicad_sch') if x.name not in sheet_edits]
unchanged += [str(x.relative_to(before)) for d in ['ENKU.pretty','standard-footprints'] for x in (before/d).rglob('*.kicad_mod')]
plan=dict(revision='R130',battery_request='BAT-REV3',predecessor_R129_pcb_sha256=source_sha,changed_original_pads=[dict(uuid=u,before=x,after=new[u]) for u,x in old.items() if x!=new[u]],added_pads=[new[u] for u in new.keys()-old.keys()],moved_existing_copper=move_records,added_copper_UUIDs=[route.m_Uuid.AsString(),via.m_Uuid.AsString()],footprint_library_changes=lib_changes,native_board_fields=fields,schematic_edits=sheet_edits,unchanged_files={rel:hashlib.sha256((before/rel).read_bytes()).hexdigest() for rel in unchanged},native_J1_VBAT_GND_signal_lands_and_routes_preserved=True,battery_choice='A: PCB PH2 + separate sensor terminals',charge_temperature_and_full_capacity_qualification=False,fabrication_ready=False)
(c/'applied_parts_BAT_REV3_R130.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({k:len(plan[k]) for k in ['changed_original_pads','added_pads','moved_existing_copper','added_copper_UUIDs']},indent=2))
