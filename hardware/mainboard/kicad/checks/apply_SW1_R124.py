"""Implement the approved MK-12C03-G015 on an isolated R123 copy.

A0 signal/locator geometry and X1 mechanical lands are kept explicitly separate
in evidence. Their revision conflict remains a manufacturing HOLD.
"""
import json,re,uuid,tempfile,hashlib
from pathlib import Path
import pcbnew as p

r=Path(__file__).resolve().parents[1]; c=r/'checks'
source=r.parent/'ENKU_R123'/'enku-mainboard-r0.1.kicad_pcb'
official='https://www.dg-switch.com/uploads/soft/200615/%E5%93%81%E8%B5%9EMK-12C03-GXXX.pdf'
exact='https://cdn.semikey.com/upload/pdfs/a6/85/a685b04beffe80627230619bb0c8ae8e.pdf'
name='GSWITCH_MK12C03_G015_DRAWING_REVIEW'
def block(text,start):
 depth=0;quoted=False;escaped=False
 for i in range(start,len(text)):
  ch=text[i]
  if quoted:
   if escaped:escaped=False
   elif ch=='\\':escaped=True
   elif ch=='"':quoted=False
  elif ch=='"':quoted=True
  elif ch=='(':depth+=1
  elif ch==')':
   depth-=1
   if depth==0:return text[start:i+1],i+1
 raise ValueError('Unbalanced source')
def iu(x):return int(round(x*1e6))
def vec(q):return p.VECTOR2I(*(iu(x) for x in q))
def uid():return str(uuid.uuid4())

# New SPDT symbol preserves the two wired endpoint positions. Pin 2 is COM.
symbol='''(symbol "MK12C03_G015"
 (pin_names (offset 0)) (in_bom yes) (on_board yes)
 (property "Reference" "SW" (at -6 9 0) (effects (font (size 0.95 0.95))))
 (property "Value" "MK-12C03-G015" (at 6 9 0) (effects (font (size 0.95 0.95))))
 (property "Footprint" "ENKU:GSWITCH_MK12C03_G015_DRAWING_REVIEW" (at 0 0 0) (effects (font (size 0.95 0.95)) (hide yes)))
 (property "Datasheet" "EXACT_URL" (at 0 0 0) (effects (font (size 0.95 0.95)) (hide yes)))
 (property "Description" "G-Switch MK-12C03-G015 SPDT; common 2; 1 GND ON; 3 unused OFF. Land revision HOLD." (at 0 0 0) (effects (font (size 0.95 0.95)) (hide yes)))
 (symbol "MK12C03_G015_0_1"
  (polyline (pts (xy -5.715 0) (xy -2.54 0) (xy 3.81 1.27)) (stroke (width 0.2) (type default)) (fill (type none)))
  (polyline (pts (xy 3.81 0) (xy 5.715 0)) (stroke (width 0.2) (type default)) (fill (type none)))
  (polyline (pts (xy 0.635 -5.08) (xy 0.635 -2.54) (xy 3.81 -2.54)) (stroke (width 0.2) (type default)) (fill (type none)))
  (pin passive line (at -8.255 0 0) (length 2.54) (name "COM_PWR" (effects (font (size 0.95 0.95)))) (number "2" (effects (font (size 0.95 0.95)))))
  (pin passive line (at 8.255 0 180) (length 2.54) (name "ON_GND" (effects (font (size 0.95 0.95)))) (number "1" (effects (font (size 0.95 0.95)))))
  (pin passive line (at 0.635 -7.62 90) (length 2.54) (name "OFF_UNUSED" (effects (font (size 0.95 0.95)))) (number "3" (effects (font (size 0.95 0.95)))))
 )
)'''.replace('EXACT_URL',exact)
lib=r/'ENKU.kicad_sym';text=(source.parent/'ENKU.kicad_sym').read_text();assert '(symbol "MK12C03_G015"' not in text
end=text.rfind(')');lib.write_text(text[:end]+symbol+'\n'+text[end:])
sch=r/'power.kicad_sch';text=(source.parent/'power.kicad_sch').read_text();start=text.index('(lib_symbols');cache,end=block(text,start)
text=text[:end-1]+'\n'+symbol.replace('(symbol "MK12C03_G015"','(symbol "ENKU:MK12C03_G015"',1)+'\n'+text[end-1:]
start=text.index('(symbol (lib_id "ENKU:SW_SPST") (at 205.105 127 0)');old,end=block(text,start);assert '(property "Reference" "SW1"' in old
new=old.replace('ENKU:SW_SPST','ENKU:MK12C03_G015').replace('"HARD POWER"','"MK-12C03-G015"').replace('ENKU:HARD_POWER_SWITCH_PLACEMENT','ENKU:'+name)
new=new.replace('(property "Datasheet" "~"','(property "Datasheet" "'+exact+'"')
new=re.sub(r'\(pin "([12])"',lambda m:'(pin "'+('2' if m[1]=='1' else '1')+'"',new)
new=new.replace('(instances ', '(pin "3" (uuid "'+uid()+'"))\n\t\t(instances ',1)
text=text[:start]+new+text[end:];end=text.rfind(')')
nc=uid();text=text[:end]+'\n(no_connect (at 205.74 134.62) (uuid "'+nc+'"))\n'+text[end:];sch.write_text(text)

# Contact/locator dimensions from the exact A0 drawing; mechanical solder
# lands from official family X1. Do not grant assembly signoff to this mixture.
module=f'''(footprint "{name}" (version 20240108) (generator "pcbnew") (layer "F.Cu")
 (descr "Approved MK-12C03-G015: A0 signals/locators, X1 bracket lands. Revision and body/peg datum HOLD; engineering review only.")
 (attr smd)
 (fp_text reference "REF**" (at 0 -4) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))
 (fp_text value "MK-12C03-G015" (at 0 4) (layer "F.Fab") hide (effects (font (size 0.8 0.8))))
 (fp_rect (start -3.3 -1.375) (end 3.3 1.375) (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))
 (fp_rect (start -1.4 1.375) (end 1.4 2.875) (stroke (width 0.1) (type default)) (fill none) (layer "F.Fab"))
 (fp_rect (start -3.9 -2.75) (end 3.9 3.125) (stroke (width 0.05) (type default)) (fill none) (layer "F.CrtYd"))
'''
for num,x in [('1',-2.25),('2',.75),('3',2.25)]:module+=f' (pad "{num}" smd rect (at {x} -1.75) (size .7 1.5) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
for x in [-1.5,1.5]:module+=f' (pad "" np_thru_hole circle (at {x} 0) (size .9 .9) (drill .9) (layers "*.Cu" "*.Mask"))\n'
for x in [-3.375,3.375]:
 for y in [-1.075,1.075]:module+=f' (pad "" smd rect (at {x} {y}) (size .55 .85) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
module+=')\n';path=r/'ENKU.pretty'/(name+'.kicad_mod');path.write_text(module)

src=source.read_text();start=src.index('(footprint "ENKU:HARD_POWER_SWITCH_PLACEMENT"');oldfp,end=block(src,start)
src=src[:start]+src[end:]
removed={'ea704456-d99f-4f60-8233-32eb7bbe4ba3','ff66cfe6-9160-4ce7-8c32-313a51f7a1cc','af9bcb89-9488-4d00-b9ec-c283ce4914fe'};found=set()
def drop(m):
 u=re.search(r'\(uuid "([^"]+)"\)',m[0])
 if u and u[1] in removed:found.add(u[1]);return ''
 return m[0]
src=re.sub(r'^\t\((?:segment|via)\n.*?^\t\)\n',drop,src,flags=re.M|re.S);assert found==removed
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb') as temp:
 temp.write(src);temp.flush();b=p.LoadBoard(temp.name)
f=p.FootprintLoad(str(path.parent),name);assert f is not None
f.SetUuid(p.KIID('3102cd65-de01-4060-8ede-2c3a51e223b0'));f.SetFPID(p.LIB_ID('ENKU',name));f.SetReference('SW1');f.SetValue('MK-12C03-G015')
f.SetPosition(vec([40.0,22.0]));f.SetOrientationDegrees(180);f.GetField('Datasheet').SetText(exact);f.GetField('Description').SetText('MK-12C03-G015')
f.Reference().SetPosition(vec([45.3,22]));f.Reference().SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));f.Reference().SetUuid(p.KIID('9cf8c9c2-31c9-4f3f-872c-89ecb530f51e'))
nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()}
unused='unconnected-(SW1-OFF_UNUSED-Pad3)';n=p.NETINFO_ITEM(b,unused);b.Add(n);nets[unused]=n
newpads=[];pad_changes=[]
for a in f.Pads():
 num=a.GetNumber()
 if num=='1':a.SetUuid(p.KIID('3cccc179-5bcf-40b5-9679-ec23facd66c2'));a.SetNet(nets['GND'])
 elif num=='2':a.SetUuid(p.KIID('2cf067bc-1a84-4388-80b9-eb9302c12ed2'));a.SetNet(nets['PWR_GATE'])
 elif num=='3':a.SetNet(nets[unused]);newpads.append(a.m_Uuid.AsString())
 else:newpads.append(a.m_Uuid.AsString())
 if num in ['1','2']:pad_changes.append({'uuid':a.m_Uuid.AsString(),'number':num,'net':a.GetNetname(),'pos':[p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)],'size':[.7,1.5]})
b.Add(f);added=[]
def track(net,a,z,width=.2,layer=p.F_Cu):
 t=p.PCB_TRACK(b);t.SetNet(nets[net]);t.SetStart(vec(a));t.SetEnd(vec(z));t.SetLayer(layer);t.SetWidth(iu(width));b.Add(t);added.append(t.m_Uuid.AsString())
gate_front=[[39.25,23.75],[39.25,22.75],[40,22],[40,21]]
for a,z in zip(gate_front,gate_front[1:]):track('PWR_GATE',a,z)
gate_back=[[40,21],[33,21],[33,24.8],[28.4,29.4],[28.4,30.1]]
for a,z in zip(gate_back,gate_back[1:]):track('PWR_GATE',a,z,layer=p.B_Cu)
ground=[[42.25,23.75],[42.25,22.75],[42.5,22.5],[42.5,21]]
for a,z in zip(ground,ground[1:]):track('GND',a,z,.25)
# The old GND run also connected R29 to the existing 45,29 ground junction.
track('GND',[42,29],[45,29],.25)
for net,pos in [('PWR_GATE',[40,21]),('GND',[42.5,21])]:
 v=p.PCB_VIA(b);v.SetPosition(vec(pos));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetWidth(iu(.6));v.SetDrill(iu(.3));v.SetNet(nets[net]);b.Add(v);added.append(v.m_Uuid.AsString())
out=r/'enku-mainboard-r0.1.kicad_pcb';p.SaveBoard(str(out),b)
# Save the same reviewed instance to the local library so warnings cannot mask
# a real subsequent board/library divergence.
lf=p.FOOTPRINT(f);lf.SetPosition(vec([0,0]));lf.SetOrientationDegrees(0);lf.SetReference('REF**');lf.Reference().SetPosition(vec([0,-4]));p.FootprintSave(str(path.parent),lf)
report={'revision':'R124','source_R123_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'approved_MPN':'G-Switch MK-12C03-G015','approval_provenance':'User decision 2026-10-09T14:56:17Z recovered from prior context; upper edge, horizontal exterior slide.','SW1_before':{'pos':[30.5,29],'angle':0,'library':'ENKU:HARD_POWER_SWITCH_PLACEMENT'},'SW1_after':{'pos':[40,22],'angle':180,'library':'ENKU:'+name},'declared_original_pad_changes':pad_changes,'new_pad_uuids':newpads,'removed_track_uuids':sorted(removed),'added_copper_uuids':added,'external_unused_pin_marker':{'uuid':nc,'pos':[205.74,134.62]},'source_documents':{'A0_exact':{'url':exact,'sha256':'4254ee2080636765128efc54139ddafcc759de219cac106f31eaa8772fe226ac','drawing_date':'2022-11-01','scope':'3 signal lands .7 x 1.5, asymmetric contact pitch and two .9 locator holes. Four bracket lands omitted.'},'X1_family':{'url':official,'sha256':'2b86195ac34db4b0c37ca28da815c563905091292ff00f13f64073cefbed9214','drawing_date':'2019-05-29','scope':'Four .55 x .85 bracket solder lands derived from overall 7.3 / inner 6.2; centres +/-3.375 and +/-1.075. Signal land dimensions differ from A0.'}},'mixed_revision_land_pattern':True,'SW1_land_pattern_revision_resolved':False,'body_to_locator_Y_datum_qualified':False,'nominal_body_fab_envelope_assumes_locator_line_at_body_centre':True,'enclosure_and_assembly_qualified':False,'fabrication_ready':False}
(c/'applied_SW1_R124.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['source_documents','new_pad_uuids','added_copper_uuids']},indent=2))
