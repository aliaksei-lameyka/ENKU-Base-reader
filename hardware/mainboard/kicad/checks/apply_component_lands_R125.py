"""Apply visually checked manufacturer lands on an isolated R124 copy.

Pin identities and all existing routed copper are preserved. Nominal land
agreement is separate from assembly/process and whole-board qualification.
"""
import gzip, hashlib, json, re, tempfile
from pathlib import Path
import pcbnew as p

r=Path(__file__).resolve().parents[1]; c=r/'checks'; prior=r.parent/'ENKU_R124'
def block(t,s):
 depth=0; quoted=False; escaped=False
 for i in range(s,len(t)):
  ch=t[i]
  if quoted:
   if escaped: escaped=False
   elif ch=='\\': escaped=True
   elif ch=='"': quoted=False
  elif ch=='"': quoted=True
  elif ch=='(': depth+=1
  elif ch==')':
   depth-=1
   if depth==0:return t[s:i+1],i+1
 raise ValueError('Unbalanced source')
def vec(x):return p.VECTOR2I(*(int(round(a*1e6)) for a in x))
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
recipes={
 'Q1':dict(name='IRLML6346_INFINEON_MICRO3',symbol='NMOS',sheet='epd_hv.kicad_sch',size=[.972,.802],x=.885,body=[1.3,2.92],courtyard=[1.65,1.8],pads={'1':[-.885,-.95],'2':[-.885,.95],'3':[.885,0]},datasheet='https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlml6346-datasheet-en.pdf',source='PD-97584A, 03/09/12, page 8. Outer span 2.742 minus pad length .972 gives centre span 1.770.'),
 'Q2':dict(name='AO3401A_AOS_SOT23',symbol='PMOS_LOAD',sheet='power.kicad_sch',size=[.8,.8],x=1.2,body=[1.6,2.9],courtyard=[1.85,1.8],pads={'1':[-1.2,-.95],'2':[-1.2,.95],'3':[1.2,0]},datasheet='https://www.aosmd.com/sites/default/files/res/data_sheets/AO3401A.pdf',source='AOS PO-00001 revision N, SOT23.pdf, recommended .8 square lands, row centre span 2.40.'),
 'U9':dict(name='TMUX1101_TI_DBV0005A',symbol='TMUX1101',sheet='mcu_io.kicad_sch',size=[1.1,.6],x=1.3,body=[1.6,2.9],courtyard=[2.1,1.8],pads={'1':[-1.3,-.95],'2':[-1.3,0],'3':[-1.3,.95],'4':[1.3,.95],'5':[1.3,-.95]},datasheet='https://www.ti.com/lit/ds/symlink/tmux1101.pdf',source='TI DBV0005A 4214839/K 08/2024, datasheet PDF page 33. Example .6 x 1.1 lands, row span 2.6, corner R .05.')
}
for file in ['ENKU.kicad_sym','epd_hv.kicad_sch','power.kicad_sch','mcu_io.kicad_sch']:
 (c/('source_R124_'+file+'.gz')).write_bytes(gzip.compress((prior/file).read_bytes(),mtime=0))
def prop(t,key,value):
 t,n=re.subn(r'(\(property "'+key+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(value),t,count=1);assert n==1;return t
for ref,a in recipes.items():
 name=a['name']; bx,by=[v/2 for v in a['body']];cx,cy=a['courtyard'];w,h=a['size']
 module=f'''(footprint "{name}" (version 20240108) (generator "pcbnew") (layer "F.Cu")
 (descr "{a['source']} Nominal land review R125; assembly qualification remains open.")
 (attr smd)
 (fp_text reference "REF**" (at 0 -2.5) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
 (fp_text value "{name}" (at 0 2.5) (layer "F.Fab") hide (effects (font (size .8 .8))))
 (fp_rect (start {-bx} {-by}) (end {bx} {by}) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
 (fp_rect (start {-cx} {-cy}) (end {cx} {cy}) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
 (fp_line (start {-bx} {-by+.35}) (end {-bx+.35} {-by}) (stroke (width .1) (type default)) (layer "F.Fab"))
'''
 for num,(x,y) in a['pads'].items():
  shape='roundrect' if ref=='U9' else 'rect';rr=' (roundrect_rratio 0.08333333333333333)' if ref=='U9' else ''
  module+=f' (pad "{num}" smd {shape} (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask"){rr})\n'
 module+=')\n';(r/'ENKU.pretty'/(name+'.kicad_mod')).write_text(module)
 # Change only instance metadata and the corresponding cached/library defaults.
 sheet=r/a['sheet'];t=sheet.read_text();idx=t.index('(property "Reference" "'+ref+'"');s=t.rfind('(symbol (lib_id',0,idx);old,e=block(t,s)
 new=prop(prop(old,'Footprint','ENKU:'+name),'Datasheet',a['datasheet']);t=t[:s]+new+t[e:]
 s=t.index('(symbol "ENKU:'+a['symbol']+'"');old,e=block(t,s);new=prop(prop(old,'Footprint','ENKU:'+name),'Datasheet',a['datasheet']);t=t[:s]+new+t[e:];sheet.write_text(t)
 lib=r/'ENKU.kicad_sym';t=lib.read_text();s=t.index('(symbol "'+a['symbol']+'"');old,e=block(t,s);new=prop(prop(old,'Footprint','ENKU:'+name),'Datasheet',a['datasheet']);lib.write_text(t[:s]+new+t[e:])

source=prior/'enku-mainboard-r0.1.kicad_pcb';src=source.read_text();before=p.LoadBoard(str(source));oldfps={f.GetReference():f for f in before.GetFootprints() if f.GetReference() in recipes}
for ref,f in oldfps.items():
 fpstart=src.index('(footprint "'+str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())+'"')
 # Q1 and Q2 share the old library: find the block by its actual reference.
 for m in re.finditer(r'\(footprint "',src):
  old,e=block(src,m.start())
  if re.search(r'\(property "Reference" "'+ref+'"',old):fpstart=m.start();break
 else:raise ValueError(ref)
 src=src[:fpstart]+src[e:]
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb') as tmp:
 tmp.write(src);tmp.flush();b=p.LoadBoard(tmp.name)
nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()};changed=[]
for ref,a in recipes.items():
 old=oldfps[ref];f=p.FootprintLoad(str(r/'ENKU.pretty'),a['name']);assert f
 f.SetFPID(p.LIB_ID('ENKU',a['name']));f.SetUuid(p.KIID(old.m_Uuid.AsString()));f.SetReference(ref);f.SetValue(old.GetValue());f.SetPath(old.GetPath());f.SetAttributes(old.GetAttributes());f.SetLocked(old.IsLocked())
 f.SetPosition(old.GetPosition());f.SetOrientation(old.GetOrientation());f.GetField('Datasheet').SetText(a['datasheet']);f.GetField('Description').SetText(old.GetValue())
 for key in ['Reference','Value']:
  x=f.GetField(key);z=old.GetField(key);x.SetUuid(p.KIID(z.m_Uuid.AsString()));x.SetPosition(z.GetPosition());x.SetTextAngle(z.GetTextAngle());x.SetVisible(z.IsVisible());x.SetTextSize(z.GetTextSize());x.SetTextThickness(z.GetTextThickness())
 op={x.GetNumber():x for x in old.Pads()}
 for pad in f.Pads():
  z=op[pad.GetNumber()];pad.SetUuid(p.KIID(z.m_Uuid.AsString()));pad.SetNet(nets[z.GetNetname()]);pad.SetPinFunction(z.GetPinFunction());pad.SetPinType(z.GetPinType())
  changed.append(dict(uuid=pad.m_Uuid.AsString(),ref=ref,number=pad.GetNumber(),net=pad.GetNetname(),before_position=xy(z.GetPosition()),after_position=xy(pad.GetPosition()),before_size=xy(z.GetSize()),after_size=xy(pad.GetSize()),shape=pad.GetShape()))
 b.Add(f)
 lf=p.FOOTPRINT(f);lf.SetPosition(vec([0,0]));lf.SetOrientationDegrees(0);lf.SetReference('REF**');lf.Reference().SetPosition(vec([0,-2.5]));p.FootprintSave(str(r/'ENKU.pretty'),lf)
p.SaveBoard(str(r/'enku-mainboard-r0.1.kicad_pcb'),b)
unchanged=['enku-mainboard-r0.1.kicad_pro','enku-mainboard-r0.1.kicad_sch','connectors.kicad_sch','fp-lib-table','sym-lib-table','enku-mainboard-r0.1.kicad_dru']
report=dict(revision='R125',source_R124_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),recipes=recipes,declared_pad_changes=changed,routed_copper_changes=[],unchanged_files={x:hashlib.sha256((prior/x).read_bytes()).hexdigest() for x in unchanged},schematic_net_changes=[],assembly_process_qualified=False,fabrication_ready=False)
(c/'applied_component_lands_R125.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'pad_changes':len(changed),'footprints':list(recipes),'source_R124_sha256':report['source_R124_sha256']},indent=2))
