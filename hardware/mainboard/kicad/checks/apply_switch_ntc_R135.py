"""SHA-pinned R134 -> R135 engineering change; native validation required."""
import hashlib,json,re,sys,uuid,tempfile
from pathlib import Path
import pcbnew as p
from cad_text_R134 import children,block,symbol,instance,prop,label

r=Path(sys.argv[1]).resolve();c=r/'checks';pcb=r/'enku-mainboard-r0.1.kicad_pcb'
assert hashlib.sha256(pcb.read_bytes()).hexdigest()=='07813982c1b4c4f191178a905edb90ecf9f583862de3b648eb4e9da416daa70a'
project=(r/'enku-mainboard-r0.1.kicad_pro').read_bytes()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'ENKU/R135/'+s))
def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def xy(v):return [round(p.ToMM(v.x),6),round(p.ToMM(v.y),6)]
lib='TL1016AAF160QG_ESWITCH_P520001'
fp=f'''(footprint "{lib}" (version 20260206) (generator "pcbnew") (layer "F.Cu")
(descr "E-Switch P520001 RevA28Apr2022; AA=no bosses/no ground terminal; actual four numbered SMD lands; case pusher/assembly acceptance pending")
(attr smd) (duplicate_pad_numbers_are_jumpers no)
(property "Reference" "REF**" (at -4.5 0 90) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
(property "Value" "TL1016AAF160QG" (at 0 4) (layer "F.Fab") (hide yes) (effects (font (size .8 .8))))
(fp_rect (start -1.75 -1.45) (end 1.75 1.45) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
(fp_rect (start -.85 1.45) (end .85 2.10) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
(fp_rect (start -2.75 -1.70) (end 2.75 2.35) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
'''
for n,x,y in [('1',-1.8,-.725),('2',1.8,-.725),('3',-1.8,.725),('4',1.8,.725)]:
 fp+=f'(pad "{n}" smd rect (at {x} {y}) (size 1.4 1.05) (layers "F.Cu" "F.Mask" "F.Paste"))\n'
fp+=')\n';(r/'ENKU.pretty'/f'{lib}.kicad_mod').write_text(fp)
symname='TL1016_AA_4PIN'
sym=f'''(symbol "{symname}" (pin_names (offset .7)) (exclude_from_sim no) (in_bom yes) (on_board yes)
(property "Reference" "SW" (at -6 7 0) (effects (font (size .88 .88))))
(property "Value" "TL1016AAF160QG" (at 6 7 0) (effects (font (size .88 .88))))
(property "Footprint" "ENKU:{lib}" (at 0 0 0) (effects (font (size .88 .88)) (hide yes)))
(property "Datasheet" "https://configured-product-images.s3.amazonaws.com/2D/specs/TL1016AAF160QG.pdf" (at 0 0 0) (effects (font (size .88 .88)) (hide yes)))
(property "Description" "SPST: 1/2 common A; 3/4 common B; all four pads explicitly routed" (at 0 0 0) (effects (font (size .88 .88)) (hide yes)))
(symbol "{symname}_0_1" (rectangle (start -6 4) (end 6 -4) (stroke (width .254) (type default)) (fill (type background)))
'''
for n,x,y,a,name in [('1',-8.255,0,0,'A'),('2',-8.255,-2.54,0,'A_DUP'),('3',8.255,0,180,'B'),('4',8.255,-2.54,180,'B_DUP')]:
 sym+=f'(pin passive line (at {x} {y} {a}) (length 2.54) (name "{name}" (effects (font (size .88 .88)))) (number "{n}" (effects (font (size .88 .88)))))\n'
sym+='))'
t=(r/'ENKU.kicad_sym').read_text().rstrip();(r/'ENKU.kicad_sym').write_text(t[:-1]+'\n'+sym+'\n)\n')
t=(r/'mcu_io.kicad_sch').read_text();offset=t.index('(lib_symbols');cache,end=block(t,offset);cache=cache[:-1]+'\n'+sym.replace(f'(symbol "{symname}"',f'(symbol "ENKU:{symname}"',1)+'\n)';t=t[:offset]+cache+t[end:]
refs={'SW3':'BTN_L1','SW4':'BTN_L2','SW5':'BTN_R1','SW6':'BTN_R2'}
for ref,net in refs.items():
 a,z,v=instance(t,ref);cx,cy=map(float,re.search(r'\(at ([\d.-]+) ([\d.-]+) ',v).groups());v=v.replace('(lib_id "ENKU:TL3340_3PIN")',f'(lib_id "ENKU:{symname}")')
 for key,val in {'Value':'TL1016AAF160QG','Footprint':'ENKU:'+lib,'MPN':'TL1016AAF160QG','Datasheet':'https://configured-product-images.s3.amazonaws.com/2D/specs/TL1016AAF160QG.pdf','Description':net+' / actual AA no-boss variant; four numbered pads'}.items():v=prop(v,key,val)
 v=v[:-1]+''.join(f'\n(pin "{n}" (uuid "{uid(ref+"/pin"+n)}"))'for n in ['2','4'])+'\n)';t=t[:a]+v+t[z:]
 removed=0
 for a,z,v in reversed(list(children(t))):
  if v.startswith('(no_connect ') and f'(at {cx+.635:.3f} {cy+7.62:.2f})' in v:t=t[:a]+t[z:];removed+=1
 # Existing sheets encode coordinates with varying trailing zeroes.
 if not removed:
  for a,z,v in reversed(list(children(t))):
   if not v.startswith('(no_connect '):continue
   m=re.search(r'\(at ([\d.-]+) ([\d.-]+)\)',v)
   if m and abs(float(m[1])-cx-.635)<1e-6 and abs(float(m[2])-cy-7.62)<1e-6:t=t[:a]+t[z:];removed+=1
 assert removed==1,ref
 t=t.rstrip();t=t[:-1]+'\n'+label(net,cx-8.255,cy+2.54,0,'R135/'+ref+'/2')+'\n'+label('GND',cx+8.255,cy+2.54,180,'R135/'+ref+'/4')+'\n)\n'
(r/'mcu_io.kicad_sch').write_text(t)
values={'R80':('40.2k 1%','RC0603FR-0740K2L'),'R81':('33.2k 1%','RC0603FR-0733K2L')}
t=(r/'power.kicad_sch').read_text()
for ref,(value,mpn) in values.items():
 a,z,v=instance(t,ref)
 for key,val in {'Value':value,'MPN':mpn,'Description':'R135 TS bias; bounded R81-open hot-inhibit model; leakage/attachment bench HOLD'}.items():v=prop(v,key,val)
 t=t[:a]+v+t[z:]
t=t.replace('31.6k/19.6k bias, 100k series; nominal4.59-39.74C','40.2k/33.2k bias, 100k series; nominal4.90-35.01C; R81-open hot model inhibits').replace('R132: real retained cell NTC. Nominal guarded5-40C window','R135: real retained cell NTC. Conservative nominal4.90-35.01C window').replace('(rev "R134 NO FAB")','(rev "R135 NO FAB")');(r/'power.kicad_sch').write_text(t)
b=p.LoadBoard(str(pcb));fps={f.GetReference():f for f in b.GetFootprints()};nets={a.GetNetname():a.GetNet()for f in fps.values()for a in f.Pads()if a.GetNetCode()}
rem=['13189f34-10ff-4e15-8bb6-ae0c5552f190','3d5845e8-8648-434b-9847-60ed04d08065','f616e211-267e-4432-ab41-6a2dbbd62085','4d7ee7d4-b65a-454f-b40d-f6d593214673','6bd89e4c-7e3e-4ee2-86ff-09df599f6f0f','b0a9a07f-05fb-4649-938a-c902f6817e3f','cf3f1f35-40bc-41a1-b070-e1f1e8772c4a','72ea1407-a8ec-451f-bb6b-edc78b44c941','56af0489-437a-4049-8a73-447b40d2c632','4a367ee0-ff0f-4389-b61c-1a52fb94b624','fe1ed29c-9484-42e5-933a-d16e03986e0e','9c32f9ab-c0f3-49b5-a19a-193e59e8753c']
source=pcb.read_text();found=set()
def drop(m):
 u=re.search(r'\(uuid "([^\"]+)"\)',m[0])
 if u and u[1] in rem:found.add(u[1]);return ''
 return m[0]
source=re.sub(r'^\t\((?:segment|via)\n.*?^\t\)\n',drop,source,flags=re.M|re.S);assert found==set(rem)
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb')as tmp:
 tmp.write(source);tmp.flush();b=p.LoadBoard(tmp.name)
fps={f.GetReference():f for f in b.GetFootprints()};nets={a.GetNetname():a.GetNet()for f in fps.values()for a in f.Pads()if a.GetNetCode()}
def fields(f,vals):
 for k,v in vals.items():
  if k=='Value':f.SetValue(v)
  else:
   fld=next((a for a in f.GetFields()if a.GetName()==k),None)
   if fld is None:fld=p.PCB_FIELD(f,p.FIELD_T_USER,k);f.Add(fld)
   fld.SetText(v);fld.SetVisible(False);fld.SetLayer(p.F_Fab);fld.SetPosition(f.GetPosition())
for ref,(val,mpn) in values.items():fields(fps[ref],{'Value':val,'MPN':mpn,'Description':'R135 TS bias; bounded R81-open hot-inhibit model; leakage/attachment bench HOLD'})
count=0
def track(net,a,z):
 global count
 q=p.PCB_TRACK(b);q.SetStart(vec(*a));q.SetEnd(vec(*z));q.SetWidth(p.FromMM(.2));q.SetLayer(p.F_Cu);q.SetNet(nets[net]);q.SetUuid(p.KIID(uid('pair-track/'+str(count))));count+=1;b.Add(q)
def via(pos,name):
 q=p.PCB_VIA(b);q.SetPosition(vec(*pos));q.SetWidth(p.F_Cu,p.FromMM(.6));q.SetDrill(p.FromMM(.3));q.SetViaType(p.VIATYPE_THROUGH);q.SetLayerPair(p.F_Cu,p.B_Cu);q.SetNet(nets['GND']);q.SetUuid(p.KIID(uid(name)));q.SetFrontTentingMode(p.TENTING_MODE_TENTED);q.SetBackTentingMode(p.TENTING_MODE_TENTED);b.Add(q)
roots={'SW3':[23.9,74.2],'SW4':[23.9,86.2],'SW5':[71.2,71.8],'SW6':[71.2,83.8]}
for ref,net in refs.items():
 old=fps[ref];new=p.FootprintLoad(str(r/'ENKU.pretty'),lib);assert new;new.SetFPID(p.LIB_ID('ENKU',lib));new.SetUuid(old.m_Uuid);new.SetPath(old.GetPath());new.SetReference(ref);pos=xy(old.GetPosition());pos[0]+=.05 if ref in ['SW3','SW4'] else -.05;new.SetPosition(vec(*pos));new.SetOrientationDegrees(old.GetOrientationDegrees())
 for fld in old.GetFields():
  if fld.GetName()not in ['Reference','Value']:fields(new,{fld.GetName():fld.GetText()})
 fields(new,{'Value':'TL1016AAF160QG','MPN':'TL1016AAF160QG','Datasheet':'https://configured-product-images.s3.amazonaws.com/2D/specs/TL1016AAF160QG.pdf','Description':net+' / actual AA no-boss variant; four numbered pads'})
 new.Reference().SetPosition(old.Reference().GetPosition());new.Reference().SetTextSize(old.Reference().GetTextSize());new.Reference().SetTextThickness(old.Reference().GetTextThickness());new.Value().SetVisible(False)
 op={a.GetNumber():a.m_Uuid.AsString()for a in old.Pads()if a.GetNumber()};ps={a.GetNumber():a for a in new.Pads()}
 for n,a in ps.items():a.SetUuid(p.KIID(op.get(n,uid(ref+'/pad/'+n))));a.SetNet(nets[net if n in ['1','2']else'GND'])
 b.Remove(old);b.Add(new)
 for a,z in [('1','2'),('3','4')]:track(ps[a].GetNetname(),xy(ps[a].GetPosition()),xy(ps[z].GetPosition()))
 mid=[round((ps['3'].GetPosition().x+ps['4'].GetPosition().x)/2/1e6,6),round((ps['3'].GetPosition().y+ps['4'].GetPosition().y)/2/1e6,6)]
 via(mid,ref+'/front-common-ground');via(roots[ref],ref+'/preserved-ground-root')
p.SaveBoard(str(pcb),b);(r/'enku-mainboard-r0.1.kicad_pro').write_bytes(project)
(c/'applied_switch_ntc_R135.json').write_text(json.dumps(dict(parent_sha256='07813982c1b4c4f191178a905edb90ecf9f583862de3b648eb4e9da416daa70a',exact_removed_GND_terminal_spur_UUIDs=rem,part='TL1016AAF160QG',switches=list(refs),bias=values,outline_or_thickness_changed=False,fabrication_ready=False),indent=2)+'\n')
print('Applied four genuine no-boss switches, explicit four-pad routing and two TS-bias MPNs; native checks pending')
