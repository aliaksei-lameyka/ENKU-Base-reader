"""Reconstruct the R132 voltage-TS charger from the SHA-pinned R131 source.
Native pcbnew 10.0.7 only. Every removed copper item is logged; no rule waiver.
Run once: AppRun python3.11 apply_charge_R132.py KICAD_DIRECTORY.
Engineering reconstruction after scratch reset; not an identical old PCB hash.
"""
import gzip, hashlib, json, math, re, sys, uuid
from pathlib import Path
import pcbnew as p
r=Path(sys.argv[1]).resolve(); c=r/'checks'; pcb=r/'enku-mainboard-r0.1.kicad_pcb'
assert hashlib.sha256(pcb.read_bytes()).hexdigest()=='c5b1785535fd7d12c02ee8aaae5b8f96da9404f2bc55d919644b85209ebb4a96'
def uid(): return str(uuid.uuid4())
def q(s): return json.dumps(str(s))
def vec(x,y): return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def xy(a): return [p.ToMM(a.x),p.ToMM(a.y)]
def block(t,start):
    level=0; quoted=False; escape=False
    for i in range(start,len(t)):
        z=t[i]
        if quoted:
            if escape: escape=False
            elif z=='\\': escape=True
            elif z=='"': quoted=False
        elif z=='"': quoted=True
        elif z=='(': level+=1
        elif z==')':
            level-=1
            if level==0:return t[start:i+1],i+1
    raise ValueError('Incomplete s-expression')
def children(t):
    start=t.index('(')+1
    while start<len(t):
        z=t.find('(',start)
        if z<0: break
        v,end=block(t,z);yield z,end,v;start=end
def prop(t,k,v):
    pattern=r'\(property "'+re.escape(k)+r'" '
    m=re.search(pattern,t)
    if m:
        b,e=block(t,m.start())
        b=re.sub(r'^(\(property "[^"]+" )"(?:\\.|[^"\\])*"',lambda m:m[1]+q(v),b,count=1)
        return t[:m.start()]+b+t[e:]
    return t[:-1]+f'\n(property {q(k)} {q(v)} (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n)'
def instance(t,ref):
    for s,e,b in children(t):
        if b.startswith('(symbol (lib_id ') and f'(property "Reference" "{ref}"' in b:return s,e,b
    raise AssertionError(ref)
old_files={str(z.relative_to(r)):hashlib.sha256(z.read_bytes()).hexdigest() for z in r.rglob('*') if z.is_file() and '__pycache__' not in str(z)}
(c/'source_R130_power.kicad_sch.gz').write_bytes(gzip.compress((r/'power.kicad_sch').read_bytes(),mtime=0))
(c/'source_R130_ENKU.kicad_sym.gz').write_bytes(gzip.compress((r/'ENKU.kicad_sym').read_bytes(),mtime=0))
names=['TS','BAT','BAT','CE_N','VSS','EN1','PGOOD_N','EN2','CHG_N','OUT','OUT','ILIM','IN','TMR','TD','ISET','EP']
nets=['CHG_TS','VBAT','VBAT','CHG_CE_N','GND','VBUS_USB','CHG_STAT1','GND','CHG_STAT2','VSYS','VSYS','CHG_ILIM_VSET','VBUS_USB','CHG_TMR','GND','CHG_ISET','GND']
libname='BQ24072T_RGT0016C_TI'; symname='BQ24072T_RGT'
lands={}
for n in range(1,17):
    if n<=4: a,b,w,h=-1.4,-.75+(n-1)*.5,.6,.24
    elif n<=8: a,b,w,h=-.75+(n-5)*.5,1.4,.24,.6
    elif n<=12:a,b,w,h=1.4,.75-(n-9)*.5,.6,.24
    else:a,b,w,h=.75-(n-13)*.5,-1.4,.24,.6
    lands[str(n)]=dict(pos=[a,b],size=[w,h],net=nets[n-1])
lands['17']=dict(pos=[0,0],size=[1.68,1.68],net='GND')
fp=f'''(footprint "{libname}" (version 20260206) (generator "pcbnew") (layer "F.Cu")
(descr "TI SLUS937C RGT0016C 4222419/E 07/2025 p42-43: copper EP1.68sq, paste1.55sq RR0.05; nominal0.125mm stencil example; process HOLD")
(attr smd)
(property "Reference" "REF**" (at 0 -2.1) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .1))))
(property "Value" "BQ24072TRGTR" (at 0 2.1) (layer "F.Fab") (hide yes) (effects (font (size .8 .8))))
(fp_rect (start -1.55 -1.55) (end 1.55 1.55) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
(fp_rect (start -1.8 -1.8) (end 1.8 1.8) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
(fp_circle (center -1.75 -.75) (end -1.65 -.75) (stroke (width .1) (type default)) (fill none) (layer "F.SilkS"))
'''
for n,z in lands.items():
    a,b=z['pos'];w,h=z['size']; layers='"F.Cu" "F.Mask"' if n=='17' else '"F.Cu" "F.Mask" "F.Paste"'
    fp+=f'(pad "{n}" smd roundrect (at {a} {b}) (size {w} {h}) (layers {layers}) (roundrect_rratio {0.05/min(w,h)}))\n'
fp+='(pad "" smd roundrect (at 0 0) (size 1.55 1.55) (layers "F.Paste") (roundrect_rratio 0.032258064516129))\n)\n'
(r/'ENKU.pretty'/f'{libname}.kicad_mod').write_text(fp)
# Independent logical symbol with one labelled endpoint per physical pin.
pin_positions={}; pin_types=['input','power_out','passive','input','passive','input','open_collector','input','open_collector','power_out','passive','passive','power_in','passive','input','passive','passive']
sym=f'''(symbol "{symname}" (pin_names (offset .8)) (exclude_from_sim no) (in_bom yes) (on_board yes)
(property "Reference" "U" (at -15 22 0) (effects (font (size .95 .95))))
(property "Value" "BQ24072TRGTR" (at 15 22 0) (effects (font (size .95 .95))))
(property "Footprint" "ENKU:{libname}" (at 0 0 0) (effects (font (size .95 .95)) (hide yes)))
(property "Datasheet" "https://www.ti.com/lit/gpn/BQ24072T" (at 0 0 0) (effects (font (size .95 .95)) (hide yes)))
(symbol "{symname}_0_1" (rectangle (start -15.24 20.32) (end 15.24 -20.32) (stroke (width .254) (type default)) (fill (type background))))
(symbol "{symname}_1_1"
'''
for n in range(1,18):
    if n<=8:x,y,a=-17.78,17.78-(n-1)*5.08,0
    elif n<=16:x,y,a=17.78,17.78-(n-9)*5.08,180
    else:x,y,a=0,-22.86,90
    pin_positions[n]=[round(x,3),round(y,3)]
    sym+=f'(pin {pin_types[n-1]} line (at {x:.3f} {y:.3f} {a}) (length 2.54) (name "{names[n-1]}" (effects (font (size .95 .95)))) (number "{n}" (effects (font (size .95 .95)))))\n'
sym+='))'
lt=(r/'ENKU.kicad_sym').read_text().rstrip();(r/'ENKU.kicad_sym').write_text(lt[:-1]+'\n'+sym+'\n)\n')
t=(r/'power.kicad_sch').read_text(); start=t.index('(lib_symbols');cache,end=block(t,start)
cache=cache[:-1]+'\n'+sym.replace(f'(symbol "{symname}"',f'(symbol "ENKU:{symname}"',1)+'\n)'
t=t[:start]+cache+t[end:]
s,e,old=instance(t,'U3'); oldsid=re.search(r'\(uuid "([^"]+)"\)',old)[1]; cx,cy=132.08,62.23
# Old U3 endpoints use direct global labels; preserve every other schematic item.
oldends=[(115.57,57.15),(115.57,59.69),(115.57,62.23),(115.57,64.77),(115.57,67.31),
         (148.59,55.88),(148.59,58.42),(148.59,60.96),(148.59,63.50),(148.59,66.04),(148.59,68.58)]
for a,z,item in reversed(list(children(t))):
    if item.startswith('(global_label '):
        v=re.search(r'\(at ([\d.-]+) ([\d.-]+) ',item)
        if v and any(abs(float(v[1])-x)<1e-4 and abs(float(v[2])-y)<1e-4 for x,y in oldends):t=t[:a]+t[z:]
s,e,old=instance(t,'U3')
# Preserve original instance UUID/path; the physical IC is intentionally replaced.
inst=re.sub(r'\(lib_id "[^"]+"\)',f'(lib_id "ENKU:{symname}")',old,count=1)
inst=re.sub(r'\s*\(pin "[^"]+" \(uuid "[^"]+"\)\)', '',inst)
for k,v in {'Value':'BQ24072TRGTR','Footprint':'ENKU:'+libname,'Datasheet':'https://www.ti.com/lit/gpn/BQ24072T','Description':'4.2V voltage-based TS power-path charger, programmable timer','MPN':'BQ24072TRGTR','Charge Profile':'R132 445mA nominal; USB500 max500mA; voltage-TS guarded window; 8.725h nominal fast timer; all bench gates HOLD'}.items():inst=prop(inst,k,v)
inst=inst[:-1]+''.join(f'\n(pin "{n}" (uuid "{uid()}"))' for n in range(1,18))+')'
t=t[:s]+inst+t[e:]
labels=''
for n, (x,y) in pin_positions.items():
    gx,gy=round(cx+x,3),round(cy-y,3);angle=0 if x<=0 else 180
    labels+=f'\n(global_label "{nets[n-1]}" (shape input) (at {gx} {gy} {angle}) (effects (font (size .95 .95)) (justify {"left" if angle==0 else "right"} bottom)) (uuid "{uid()}"))'
parts={
 'R8':dict(Value='3.48k 1%',MPN='RC0603FR-073K48L',Description='ILIM parked; EN1 high EN2 low selects USB500'),
 'R9':dict(Value='2k 1%',MPN='RC0603FR-072KL',Description='445mA nominal BQ24072T fast charge'),
 'R12':dict(Value='10k',Assembly='FIT',Description='CHG_N pullup to switched3V3'),
 'C7':dict(Value='22uF 10V',MPN='CC0805MKX5R6BB226',Voltage='10V',Datasheet='https://yageogroup.com/download/specsheet/CC0805MKX5R6BB226',Description='22uF10V SYS decoupling; guaranteed Ceff pending'),
 'C8':dict(Value='22uF 10V',MPN='CC0805MKX5R6BB226',Voltage='10V',Datasheet='https://yageogroup.com/download/specsheet/CC0805MKX5R6BB226',Description='22uF10V BAT decoupling; guaranteed Ceff pending'),
 'J8':{'Sensor Status':'Real103JT-050; R132 voltage-TS model guards5-40C, absolute0-45C thermal qualification HOLD'}
}
for ref,values in parts.items():
    s,e,item=instance(t,ref)
    for k,v in values.items():item=prop(item,k,v)
    if ref=='R12':item=item.replace('(dnp yes)','(dnp no)')
    t=t[:s]+item+t[e:]
rspecs={'R80':('31.6k 1%','RC0603FR-0731K6L','VBUS_USB','BAT_TS',43.5,99),
 'R81':('19.6k 1%','RC0603FR-0719K6L','BAT_TS','GND',44,103.8),
 'R82':('100k 1%','RC0603FR-07100KL','BAT_TS','CHG_TS',43.5,102),
 'R83':('69.8k 1%','RC0603FR-0769K8L','CHG_TMR','GND',47,102)}
schids={}
# Add direct-label resistor networks in unused lower sheet area.
for index,(ref,(value,mpn,n1,n2,x,y)) in enumerate(rspecs.items()):
    xx,yy=35+index*50,198.12;sid=uid();schids[ref]=sid
    s,e,tmpl=instance(t,'R9')
    new=re.sub(r'\(at 142.24 105.41 0\)',f'(at {xx} {yy} 0)',tmpl,count=1)
    new=new.replace('(reference "R9")',f'(reference "{ref}")').replace('/70000000-0000-4000-8000-000000000139"',f'/{sid}"')
    new=re.sub(r'\(uuid "[^"]+"\)',lambda m:'(uuid "'+uid()+'")',new)
    new=re.sub(r'\(uuid "[^"]+"\)',f'(uuid "{sid}")',new,count=1)
    for k,v in {'Reference':ref,'Value':value,'MPN':mpn,'Description':value+' R132 charger network'}.items():new=prop(new,k,v)
    for key in ['Reference','Value']:
        m=re.search(r'\(property "'+key+'" ',new);b,e1=block(new,m.start())
        b=re.sub(r'\(at [^)]*\)',f'(at {xx} {yy+(-5 if key=="Reference" else 5)} 0)',b,count=1)
        new=new[:m.start()]+b+new[e1:]
    labels+='\n'+new
    # ENKU:R horizontal has endpoint +/-7.62.
    for endpoint,net,angle in [(xx-7.62,n1,0),(xx+7.62,n2,180)]:
        labels+=f'\n(global_label "{net}" (shape input) (at {endpoint:.3f} {yy} {angle}) (effects (font (size .95 .95)) (justify {"left" if angle==0 else "right"} bottom)) (uuid "{uid()}"))'
t=re.sub(r'\(text "BAT-REV3 HOLD:[^"]*"', '(text "R132: real retained cell NTC. Nominal guarded5-40C window,445mA/8.725h; full-cycle and thermal hardware qualification HOLD."',t,count=1)
t=t.rstrip();t=t[:-1]+labels+'\n)\n';(r/'power.kicad_sch').write_text(t)
b=p.LoadBoard(str(pcb));fps={f.GetReference():f for f in b.GetFootprints()}
netmap={a.GetNetname():a.GetNet() for f in fps.values() for a in f.Pads() if a.GetNetCode()}
for net in nets:
    if net not in netmap:
        z=p.NETINFO_ITEM(b,net);b.Add(z);netmap[net]=z
old=fps['U3'];new=p.FootprintLoad(str(r/'ENKU.pretty'),libname);assert new
new.SetFPID(p.LIB_ID('ENKU',libname));new.SetUuidDirect(old.m_Uuid);new.SetPath(old.GetPath())
new.SetReference('U3');new.SetValue('BQ24072TRGTR');new.SetPosition(old.GetPosition());new.SetOrientationDegrees(180)
new.Reference().SetPosition(vec(48,96.7));new.Reference().SetTextSize(vec(.8,.8));new.Reference().SetTextThickness(p.FromMM(.1))
for a in new.Pads():
    if a.GetNumber():a.SetNet(netmap[lands[a.GetNumber()]['net']])
for a in old.GetFields():
    if a.GetName() not in ['Reference','Value']:new.SetField(a.GetName(),a.GetText());new.GetField(a.GetName()).SetVisible(False)
b.Remove(old);b.Add(new);fps['U3']=new
def fields(f,values):
    for k,v in values.items():
        if k=='Footprint':continue
        f.SetField(k,v)
        if k not in ['Reference','Value']:
            a=f.GetField(k);a.SetVisible(False);a.SetLayer(p.F_Fab);a.SetPosition(f.GetPosition())
for k,v in {'MPN':'BQ24072TRGTR','Datasheet':'https://www.ti.com/lit/gpn/BQ24072T','Description':'4.2V voltage-based TS power-path charger, programmable timer','Charge Profile':'R132 445mA nominal; USB500 max500mA; voltage-TS guarded window; 8.725h nominal fast timer; all bench gates HOLD'}.items():fields(new,{k:v})
for ref,values in parts.items():fields(fps[ref],values)
fps['R12'].SetAttributes(fps['R12'].GetAttributes() & ~p.FP_DNP)
moves={'C5':([47.2,87.25],0),'C6':([45,94.6],0),'C7':([51.6,93.9],90),'C8':([48.5,94.5],180),'R11':([51.5,98.8],90)}
for ref,(pos,theta) in moves.items():fps[ref].SetPosition(vec(*pos));fps[ref].SetOrientationDegrees(theta)
fps['C7'].Reference().SetPosition(vec(54.8,92.5))
for ref,(value,mpn,n1,n2,x,y) in rspecs.items():
    f=p.FootprintLoad(str(r/'ENKU.pretty'),'R_RC0603_YAGEO_REFLOW');assert f
    f.SetReference(ref);f.SetValue(value);f.SetFPID(p.LIB_ID('ENKU','R_RC0603_YAGEO_REFLOW'));f.SetPosition(vec(x,y));f.SetOrientationDegrees(0)
    path=p.KIID_PATH()
    for z in ['10000000-0000-4000-8000-000000000001',schids[ref]]:path.push_back(p.KIID(z))
    f.SetPath(path);f.SetAttributes(p.FP_SMD)
    f.Reference().SetPosition(vec(x,y-1.05));f.Reference().SetTextSize(vec(.8,.8));f.Reference().SetTextThickness(p.FromMM(.1))
    for a in f.Pads():a.SetNet(netmap[n1 if a.GetNumber()=='1' else n2])
    fields(f,dict(MPN=mpn,Manufacturer='Yageo',Assembly='FIT',Datasheet='https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L',Description=value+' R132 charger network'))
    b.Add(f);fps[ref]=f
# Rework bounded local copper only; retained external anchors are routed again.
removed=[]
charge_nets=set(nets)|{'BAT_TS','3V3_SYS'}
for item in list(b.GetTracks()):
    a,z=xy(item.GetStart()),xy(item.GetEnd())
    if item.GetNetname() not in charge_nets:continue
    if all(40<=pt[0]<=56 and 82<=pt[1]<=104.5 for pt in [a,z]):
        removed.append(dict(uuid=item.m_Uuid.AsString(),net=item.GetNetname(),start=a,end=z,width=p.ToMM(item.GetWidth(p.F_Cu) if isinstance(item,p.PCB_VIA) else item.GetWidth()),layer=item.GetLayer(),via=isinstance(item,p.PCB_VIA),drill=p.ToMM(item.GetDrill()) if isinstance(item,p.PCB_VIA) else 0))
        b.Remove(item)
p.SaveBoard(str(pcb),b)
allowed=['ENKU.kicad_sym','power.kicad_sch','enku-mainboard-r0.1.kicad_pcb','checks/current_checkpoint.json']
manifest=dict(revision='R132',parent_commit='13f8d51f2ad67e687a5e4380ecb35af66e3910b3',baseline_pcb_sha256='c5b1785535fd7d12c02ee8aaae5b8f96da9404f2bc55d919644b85209ebb4a96',
 unchanged_files={k:v for k,v in old_files.items() if k not in allowed},allowed_changed_original_files=allowed,allowed_original_geometry_refs=['U3']+list(moves),new_refs=list(rspecs),removed_original_copper=removed,primary_lands=lands,final_placements=moves,
 reconstructed_after_workspace_reset=True,old_R132_binary_not_recoverable=True,fabrication_ready=False)
(c/'preservation_manifest_R132.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('R132 reconstructed; removed local copper',len(removed),'new footprints',len(rspecs))

