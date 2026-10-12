"""One-time SHA-pinned R133 -> R134 proposal. Native DRC is mandatory.
Geometry is still NO FAB; no board rule, outline or thickness is relaxed.
"""
import gzip,hashlib,json,math,re,sys,tempfile
from pathlib import Path
import pcbnew as p
from cad_text_R134 import block,children,symbol,instance,pins,prop,q,uid,label,change_pin_label
r=Path(sys.argv[1]).resolve();c=r/'checks';pcb=r/'enku-mainboard-r0.1.kicad_pcb'
assert hashlib.sha256(pcb.read_bytes()).hexdigest()=='d42f725afb5b597c1403a6a60e04c0d0e87d9821adb5f3cae479183f37bf1b25'
texts={name:(r/name).read_text()for name in ['power.kicad_sch','mcu_io.kicad_sch','connectors.kicad_sch','ENKU.kicad_sym']}
def correct(sym):
    for n,name,kind in [('5','EN2','input'),('8','VSS','passive')]:
        old=pins(sym)[n][2];new=re.sub(r'^\(pin \w+ ',f'(pin {kind} ',old,count=1);new=re.sub(r'\(name "[^"]+"',f'(name {q(name)}',new,count=1);assert sym.count(old)==1;sym=sym.replace(old,new)
    return sym
lt=texts['ENKU.kicad_sym'];a,z,sym=symbol(lt,'BQ24072T_RGT');texts['ENKU.kicad_sym']=lt[:a]+correct(sym)+lt[z:]
t=texts['power.kicad_sch'];a,z,sym=symbol(t,'ENKU:BQ24072T_RGT',True);sym=correct(sym);t=t[:a]+sym+t[z:]
_,_,u3=instance(t,'U3');at=re.search(r'\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)\)',u3);cx,cy=float(at[1]),float(at[2]);assert float(at[3])==0
for n,net in [('5','CHG_EN2'),('6','CHG_EN1')]:
    x,y,_=pins(sym)[n];t=change_pin_label(t,[round(cx+x,6),round(cy-y,6)],net)
profile='R134 GPIO16/2 EN1/EN2;GPIO38 CE;reset/OFF high-Z USB100;authorizedUSB500;suspend11;bench HOLD'
a,z,v=instance(t,'U3');t=t[:a]+prop(v,'Charge Profile',profile)+t[z:]
a,z,v=instance(t,'R8');description='R134 ILIM fallback maximum493.5mA corner;GPIO-controlled input modes';t=t[:a]+prop(v,'Description',description)+t[z:]
parts={
 'R84':('2.2k 1%','RC0603FR-072K2L','CHG_EN1','GND',[53.8,79.]),
 'R85':('2.2k 1%','RC0603FR-072K2L','CHG_EN2','GND',[57.,79.]),
 'R86':('1k 1%','RC0603FR-071KL','CHG_EN1_CMD','CHG_EN1',[53.8,85.]),
 'R87':('1k 1%','RC0603FR-071KL','CHG_EN2_CMD','CHG_EN2',[57.,85.]),
 'R88':('1k 1%','RC0603FR-071KL','CHG_CE_CMD','CHG_CE_N',[53.8,77.])}
_,_,template=instance(t,'R9');added='';schids={}
for i,(ref,(value,mpn,n1,n2,pos))in enumerate(parts.items()):
    sid=uid(ref+'/symbol');schids[ref]=sid;oldid=re.search(r'\(uuid "([^"]+)"\)',template)[1];v=template.replace(oldid,sid);idx=[0]
    def rename(m):
        if m[1]==sid:return m[0]
        idx[0]+=1;return '(uuid '+q(uid(ref+'/child/'+str(idx[0])))+')'
    v=re.sub(r'\(uuid "([^"]+)"\)',rename,v);xx,yy=35.56+63.5*i,245.11
    v=re.sub(r'\(at [\d.-]+ [\d.-]+ [\d.-]+\)',f'(at {xx} {yy} 0)',v,count=1).replace('(reference "R9")',f'(reference {q(ref)})')
    for k,x in {'Reference':ref,'Value':value,'MPN':mpn,'Description':ref+' R134 USB current-control network','Assembly':'FIT'}.items():v=prop(v,k,x)
    for k in ['Reference','Value']:
        m=re.search(r'\(property '+q(k)+' ',v);b,end=block(v,m.start());b=re.sub(r'\(at [^)]*\)',f'(at {xx} {yy+(-5 if k=="Reference"else 5)} 0)',b,count=1);v=v[:m.start()]+b+v[end:]
    added+='\n'+v+'\n'+label(n1,xx-7.62,yy,0,ref+'/label1')+'\n'+label(n2,xx+7.62,yy,180,ref+'/label2')
t=re.sub(r'\(rev "R132 NO FAB"\)','(rev "R134 NO FAB")',t,count=1).rstrip();texts['power.kicad_sch']=t[:-1]+added+'\n)\n'
m=texts['mcu_io.kicad_sch'];_,_,sym=symbol(m,'ENKU:ESP32_S3',True);_,_,u1=instance(m,'U1');at=re.search(r'\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)\)',u1);cx,cy=float(at[1]),float(at[2]);assert float(at[3])==0
commands={'9':'CHG_EN1_CMD','38':'CHG_EN2_CMD','31':'CHG_CE_CMD'}
for n,net in commands.items():
    x,y,_=pins(sym)[n];pos=[round(cx+x,6),round(cy-y,6)];found=0
    for a,z,v in reversed(list(children(m))):
        if not v.startswith('(no_connect '):continue
        at=re.search(r'\(at ([\d.-]+) ([\d.-]+)\)',v)
        if at and math.dist(pos,[float(at[1]),float(at[2])])<1e-6:m=m[:a]+m[z:];found+=1
    assert found==1,(n,pos);m=m.rstrip();m=m[:-1]+'\n'+label(net,*pos,0 if x<0 else 180,'U1/'+n+'/command')+'\n)\n'
texts['mcu_io.kicad_sch']=m
lib='USB4215_03_A_GCT_REVA';front=3.675;row=-3.
fp=f'''(footprint "{lib}" (version 20260206) (generator "pcbnew") (layer "F.Cu")
(descr "GCT USB4215 RevA26Apr2024;16 logical contacts/12 physical lands;4plated slots;no locating pegs;0.8mm stakes/1.6mm PCB assembly HOLD")
(attr smd)
(property "Reference" "REF**" (at 6.8 -.825) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
(property "Value" "GCT USB4215-03-A" (at 0 5) (layer "F.Fab") (hide yes) (effects (font (size .8 .8))))
(fp_rect (start -4.47 -2.825) (end 4.47 3.675) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
(fp_rect (start -5.07 -3.825) (end 5.07 3.925) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
(fp_line (start -5 3.675) (end 5 3.675) (stroke (width .1) (type dash)) (layer "Dwgs.User"))
'''
for x in [-4.7,4.7]:fp+=f'(fp_line (start {x} -1.25) (end {x} .15) (stroke (width .12) (type default)) (layer "F.SilkS"))\n'
xs={'A1':-3.2,'A4':-2.4,'A5':-1.25,'A6':-.25,'A7':.25,'A8':1.25,'A9':2.4,'A12':3.2,'B1':3.2,'B4':2.4,'B5':1.75,'B6':.75,'B7':-.75,'B8':-1.75,'B9':-2.4,'B12':-3.2}
for number,x in xs.items():
    w=.6 if number in ['A1','A4','A9','A12','B1','B4','B9','B12']else .3
    fp+=f'(pad {q(number)} smd rect (at {x} -3) (size {w} 1.15) (layers "F.Cu" "F.Mask" "F.Paste"))\n'
for x in [-4.32,4.32]:
    for y,h,d in [(-2.425,1.8,1.4),(1.575,2.2,1.8)]:fp+=f'(pad "S" thru_hole oval (at {x} {y}) (size 1 {h}) (drill oval .6 {d}) (layers "*.Cu" "*.Mask"))\n'
fp+=')\n';(r/'ENKU.pretty'/f'{lib}.kicad_mod').write_text(fp)
z=texts['connectors.kicad_sch'];a,e,v=instance(z,'J5');j5fields={'Value':'GCT USB4215-03-A','Footprint':'ENKU:'+lib,'MPN':'USB4215-03-A','Datasheet':'https://gct.co/files/drawings/USB4215.pdf','Description':'R134 lower3.16mm USB2.0 data receptacle;no locating pegs;4plated shell slots;assembly HOLD'}
for k,x in j5fields.items():v=prop(v,k,x)
texts['connectors.kicad_sch']=z[:a]+v+z[e:]
# Remove exact native UUIDs in text before board load; no removed C++ object
# is reused through a stale Python wrapper.
g=json.loads(gzip.decompress((c/'geometry_checkpoint_R133.json.gz').read_bytes()));removed=[]
for t in g['tracks']:
    rem=t['uuid']in ['8e6d76c0-9059-5ee9-954d-04fa83084c4e','8f64d8ef-1ac3-5f74-90ea-daf79d558968']
    if not t['via']and t['layer']==0:
        if t['net']=='VBUS_USB'and [48.75,89.6]in [t['start'],t['end']]:rem=True
        if t['net']in ['USB_DM_CONN','USB_DP_CONN']and all(45<=x<=49.5 and 109.649<=y<=116 for x,y in [t['start'],t['end']]):rem=True
    if rem:removed.append({k:v for k,v in t.items()if k!='code'})
wanted={t['uuid']for t in removed};found=set()
def drop(match):
    n=re.search(r'\(uuid "([^"]+)"\)',match[0])
    if n and n[1]in wanted:found.add(n[1]);return ''
    return match[0]
source=re.sub(r'^\t\((?:segment|via)\n.*?^\t\)\n',drop,pcb.read_text(),flags=re.M|re.S);assert found==wanted
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb')as tmp:
    tmp.write(source);tmp.flush();b=p.LoadBoard(tmp.name)
fps={f.GetReference():f for f in b.GetFootprints()};netmap={a.GetNetname():a.GetNet()for f in fps.values()for a in f.Pads()if a.GetNetCode()}
for n in ['CHG_EN1','CHG_EN2',*commands.values()]:
    assert n not in netmap;net=p.NETINFO_ITEM(b,n);b.Add(net);netmap[n]=net
for f in [fps['U3'],fps['U1']]:
    for a in f.Pads():
        if f.GetReference()=='U3'and a.GetNumber()in ['5','6']:a.SetNet(netmap['CHG_EN2'if a.GetNumber()=='5'else'CHG_EN1'])
        if f.GetReference()=='U1'and a.GetNumber()in commands:a.SetNet(netmap[commands[a.GetNumber()]])
def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def fields(f,values):
    for k,v in values.items():
        if k=='Value':f.SetValue(v);continue
        f.SetField(k,v);a=f.GetField(k);a.SetVisible(False);a.SetPosition(f.GetPosition());a.SetLayer(p.F_Fab)
fields(fps['U3'],{'Charge Profile':profile});fields(fps['R8'],{'Description':description})
old=fps['J5'];new=p.FootprintLoad(str(r/'ENKU.pretty'),lib);assert new
new.SetFPID(p.LIB_ID('ENKU',lib));new.SetUuid(old.m_Uuid);new.SetPath(old.GetPath());new.SetReference('J5');new.SetPosition(old.GetPosition());new.SetOrientationDegrees(old.GetOrientationDegrees())
for fld in old.GetFields():
    if fld.GetName()not in ['Reference','Value']:fields(new,{fld.GetName():fld.GetText()})
fields(new,{k:v for k,v in j5fields.items()if k!='Footprint'})
new.Reference().SetPosition(old.Reference().GetPosition());new.Reference().SetTextSize(old.Reference().GetTextSize());new.Reference().SetTextThickness(old.Reference().GetTextThickness())
oldps={}
for a in old.Pads():
    if a.GetNumber():oldps.setdefault(a.GetNumber(),[]).append(dict(pos=xy(a.GetPosition()),uuid=a.m_Uuid.AsString(),net=a.GetNetname()))
for n in oldps:oldps[n].sort(key=lambda a:a['pos'])
for n in xs.keys()|{'S'}:
    ns=sorted((a for a in new.Pads()if a.GetNumber()==n),key=lambda a:xy(a.GetPosition()));assert len(ns)==len(oldps[n])
    for a,op in zip(ns,oldps[n]):a.SetUuid(p.KIID(op['uuid']));a.SetNet(netmap[op['net']])
b.Remove(old);b.Add(new)
for ref,(value,mpn,n1,n2,pos)in parts.items():
    f=p.FootprintLoad(str(r/'ENKU.pretty'),'R_RC0603_YAGEO_REFLOW');assert f;f.SetFPID(p.LIB_ID('ENKU','R_RC0603_YAGEO_REFLOW'));f.SetReference(ref);f.SetValue(value);f.SetPosition(vec(*pos));f.SetOrientationDegrees(0);f.SetUuid(p.KIID(uid(ref+'/footprint')));f.SetAttributes(p.FP_SMD)
    path=p.KIID_PATH()
    for n in ['10000000-0000-4000-8000-000000000001',schids[ref]]:path.push_back(p.KIID(n))
    f.SetPath(path);f.Reference().SetLayer(p.F_Fab);f.Reference().SetPosition(vec(pos[0],pos[1]-1.1));f.Reference().SetTextSize(vec(.8,.8));f.Value().SetVisible(False)
    for a in f.Pads():a.SetNet(netmap[n1 if a.GetNumber()=='1'else n2])
    fields(f,dict(MPN=mpn,Manufacturer='Yageo',Assembly='FIT',Datasheet='https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L',Description=ref+' R134 USB current-control network'));b.Add(f)
count=0
def segment(net,a,z):
    global count
    assert a!=z;t=p.PCB_TRACK(b);t.SetStart(vec(*a));t.SetEnd(vec(*z));t.SetWidth(p.FromMM(.2));t.SetLayer(p.F_Cu);t.SetNet(netmap[net]);t.SetUuid(p.KIID(uid('initial-track/'+str(count))));count+=1;b.Add(t)
for n,ops in oldps.items():
    if n in ['A6','A7','B6','B7','A8','B8']:continue
    ns=sorted((a for a in new.Pads()if a.GetNumber()==n),key=lambda a:xy(a.GetPosition()))
    for op,a in zip(ops,ns):
        if op['pos']!=xy(a.GetPosition()):segment(a.GetNetname(),op['pos'],xy(a.GetPosition()))
for net,pts in {
 'USB_DM_CONN':[[46.05,109.65],[46.05,111.0],[46.25,111.2],[46.25,114.325],[46.25,115.45],[47.25,115.45],[47.25,114.325]],
 'USB_DP_CONN':[[47.95,109.65],[47.95,111.0],[47.75,111.2],[47.75,113.35],[46.75,113.35],[46.75,114.325]]}.items():
    for a,z in zip(pts,pts[1:]):segment(net,a,z)
segment('USB_DP_CONN',[47.75,113.35],[47.75,114.325])
# Serialize all proposed CAD to staging, then replace canonical sources only
# after every construction step has succeeded.
p.SaveBoard(str(pcb.with_suffix('.proposal.kicad_pcb')),b)
for name,text in texts.items():(r/name).write_text(text)
pcb.with_suffix('.proposal.kicad_pcb').replace(pcb)
man=json.loads((c/'preservation_manifest_R134.json').read_text());man.update(initial_declared_removed_copper=removed,new_control_resistors={ref:dict(value=v[0],mpn=v[1],nets=v[2:4],pos=v[4],symbol_uuid=schids[ref])for ref,v in parts.items()},commands=commands,connector_front_face_board_y_mm=121.,connector_drawing_sha256='1659ba00769b9b774a033fac72cb2f3bfc481a3272c53f34e87520f33635a9e1');(c/'preservation_manifest_R134.json').write_text(json.dumps(man,indent=2)+'\n')
print('R134 proposal applied:',len(removed),'exact copper removals;',count,'short contact traces;control routes pending. NO FAB.')
