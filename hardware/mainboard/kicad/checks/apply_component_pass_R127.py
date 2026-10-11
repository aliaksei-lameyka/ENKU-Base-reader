"""Apply R127 on the accepted R126 source; preserve every routed copper item.

Capacitor lands are an engineering transfer of Yageo's size-based AC reflow
recommendation to the verified CC packages, not CC-specific process approval.
"""
import gzip, hashlib, json, math, re, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p

r=Path(__file__).resolve().parents[1]; c=r/'checks'; prior=r.parents[2].with_name('ENKU_R126')/'hardware/mainboard/kicad'
def block(t,s):
 depth=0; quoted=False; escaped=False
 for i in range(s,len(t)):
  ch=t[i]
  if quoted:
   if escaped:escaped=False
   elif ch=='\\':escaped=True
   elif ch=='"':quoted=False
  elif ch=='"':quoted=True
  elif ch=='(':depth+=1
  elif ch==')':
   depth-=1
   if depth==0:return t[s:i+1],i+1
 raise ValueError('Unbalanced source')
def prop(t,key,value):
 t,n=re.subn(r'(\(property "'+re.escape(key)+r'" )"(?:\\.|[^"\\])*"',lambda m:m[1]+json.dumps(value),t,count=1)
 if not n:
  t=t[:-1]+'\n\t\t(property '+json.dumps(key)+' '+json.dumps(value)+' (at 0 0 0) (effects (font (size .8 .8)) (hide yes)))\n\t)'
 return t
def vec(x):return p.VECTOR2I(*(int(round(a*1e6)) for a in x))
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]

sources=['ENKU.kicad_sym','epd_hv.kicad_sch','power.kicad_sch','mcu_io.kicad_sch','connectors.kicad_sch']
for file in sources:(c/('source_R126_'+file+'.gz')).write_bytes(gzip.compress((prior/file).read_bytes(),mtime=0))
assert (c/'netlist_R126_baseline.xml').exists()
RURL='https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L'
old_patterns=json.loads((prior/'checks/applied_component_pass_R126.json').read_text())['patterns']
patterns={k:dict(v) for k,v in old_patterns.items() if k.startswith('C_CC')}
patterns['R_RT0603_YAGEO_REFLOW']=dict(old_patterns['R_RC0603_YAGEO_REFLOW'],source='Yageo Chip resistors mounting v10 p4 table1 0603 RT: A2.6 B.8 C.9 D.8 pitch1.7. RT exact sheets 0603 body1.6 x .8.',datasheet='https://www.yageogroup.com/content/datasheet/asset/file/PYU-RT_1-TO-0-01_ROHS_L')
patterns['R_CRCW0805_HP_VISHAY_REFLOW']=dict(size=[.95,1.45],pads=[('1',[-.975,0]),('2',[.975,0])],body=[2,1.25],yard=[1.55,.825],source='Vishay CRCW-HP e3 doc20043 rev17-Mar-2026 p9 reflow: G1.00 Y.95 X1.45 Z2.90; pitch1.95. Body2.0 x1.25. Dense courtyard is not factory-qualified.',datasheet='https://www.vishay.com/docs/20043/crcwhpe3.pdf')
for name,a in patterns.items():
 if name.startswith('C_CC'):
  assert (r/'ENKU.pretty'/(name+'.kicad_mod')).read_bytes()==(prior/'ENKU.pretty'/(name+'.kicad_mod')).read_bytes()
  continue
 bx,by=[v/2 for v in a['body']];cx,cy=a['yard'];w,h=a['size']
 module=f'''(footprint "{name}" (version 20240108) (generator "pcbnew") (layer "F.Cu")
 (descr "{a['source']}") (attr smd)
 (fp_text reference "REF**" (at 0 {-cy-.5}) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
 (fp_text value "{name}" (at 0 {cy+.5}) (layer "F.Fab") hide (effects (font (size .8 .8))))
 (property "MPN" "" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size .5 .5))))
 (property "Manufacturer" "" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size .5 .5))))
 (property "Voltage" "" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size .5 .5))))
 (property "Tuning MPN" "" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size .5 .5))))
 (property "Assembly" "" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size .5 .5))))
 (fp_rect (start {-bx} {-by}) (end {bx} {by}) (stroke (width .1) (type default)) (fill none) (layer "F.Fab"))
 (fp_rect (start {-cx} {-cy}) (end {cx} {cy}) (stroke (width .05) (type default)) (fill none) (layer "F.CrtYd"))
'''
 if name.startswith('MBR'):
  module+=' (fp_line (start -1 -.7) (end -1 .7) (stroke (width .18) (type default)) (layer "F.Fab"))\n'
 for n,(x,y) in a['pads']:module+=f' (pad "{n}" smd rect (at {x} {y}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask"))\n'
 module+=')\n';(r/'ENKU.pretty'/(name+'.kicad_mod')).write_text(module)
 # Canonicalize the footprint once, before using it for multiple parts.
 f=p.FootprintLoad(str(r/'ENKU.pretty'),name);assert f;f.SetFPID(p.LIB_ID('ENKU',name));p.FootprintSave(str(r/'ENKU.pretty'),f)

components={x.attrib['ref']:x for x in ET.parse(c/'netlist_R126_baseline.xml').findall('./components/comp')}
recipes={}
cap_parts={ref:'CC0603KRX7R9BB104' for ref in ['C14','C17','C18','C19','C21','C38']}
cap_parts.update({ref:'CC0603KRX7R8BB105' for ref in ['C15','C22','C23']})
cap_parts.update({ref:'CC0805KKX7R8BB475' for ref in ['C27','C28','C29']})
cap_parts.update(C4='CC0805KKX7R8BB105',C16='CC0805KKX5R6BB106',C30='CC0805KKX7R8BB105',C39='CC0603JRNPO9BN102')
for ref,mpn in cap_parts.items():
 voltage=25 if '8BB' in mpn else 50 if mpn.startswith('CC0603') else 10
 recipes[ref]=dict(name='C_CC'+mpn[2:6]+'_YAGEO_REFLOW_TRANSFER',mpn=mpn,manufacturer='Yageo',datasheet='https://yageogroup.com/download/specsheet/'+mpn,value='1uF 25V' if ref=='C4' else components[ref].findtext('value'),assembly='FIT',rated_voltage_V=voltage,tolerance_percent=5 if 'JRNPO' in mpn else 10,dielectric='C0G' if 'NPO' in mpn else 'X5R' if 'X5R' in mpn else 'X7R',CC_specific_land_process_qualified=False,effective_capacitance_qualified=False)
for ref,mpn in [('R70','RT0603BRD0726K7L'),('R71','RT0603BRD0710KL')]:
 recipes[ref]=dict(name='R_RT0603_YAGEO_REFLOW',mpn=mpn,manufacturer='Yageo',datasheet='https://yageogroup.com/download/specsheet/'+mpn,value=components[ref].findtext('value'),assembly='FIT',tolerance_percent=.1,TCR_ppm_K=25,power_W=.1)
recipes['R37']=dict(name='R_CRCW0805_HP_VISHAY_REFLOW',mpn='CRCW08052R20FKEAHP',manufacturer='Vishay',datasheet=patterns['R_CRCW0805_HP_VISHAY_REFLOW']['datasheet'],value=components['R37'].findtext('value'),assembly='FIT',tolerance_percent=1,TCR_ppm_K=100,power_W=.5,actual_EPD_pulse_and_thermal_qualified=False)
assert len(recipes)==19 and len(cap_parts)==16

for file in ['epd_hv.kicad_sch','power.kicad_sch','mcu_io.kicad_sch','connectors.kicad_sch']:
 t=(prior/file).read_text()
 for ref,a in recipes.items():
  needle='(property "Reference" "'+ref+'"'
  if needle not in t:continue
  s=t.rfind('(symbol (lib_id',0,t.index(needle));x,e=block(t,s)
  a['description']=json.loads(re.search(r'\(property "Description" ("(?:\\.|[^"\\])*")',x)[1])
  fields={'Footprint':'ENKU:'+a['name'],'Datasheet':a['datasheet'],'Value':a['value'],'MPN':a['mpn'],'Manufacturer':a['manufacturer'],'Assembly':a['assembly']}
  if a.get('tune_MPN'):fields['Tuning MPN']=a['tune_MPN']
  if a.get('rated_voltage_V'):fields['Voltage']=str(a['rated_voltage_V'])+'V'
  if ref=='C4': fields['Description']='USB VBUS bypass; R127 reduces direct VBUS capacitor budget from15.8 to6.8uF. BQ25185 IN effective capacitance and actual inrush require qualification.'
  for k,v in fields.items():x=prop(x,k,v)
  a.update(sheet=file,source_fields=fields)
  t=t[:s]+x+t[e:]
 (r/file).write_text(t)
assert all('sheet' in a for a in recipes.values())

source=prior/'enku-mainboard-r0.1.kicad_pcb';src=source.read_text();before=p.LoadBoard(str(source));oldfps={f.GetReference():f for f in before.GetFootprints() if f.GetReference() in recipes}
for m in reversed(list(re.finditer(r'\(footprint "',src))):
 x,e=block(src,m.start());z=re.search(r'\(property "Reference" "([^"\n]+)"',x)
 if z and z[1] in recipes:src=src[:m.start()]+src[e:]
with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb') as tmp:
 tmp.write(src);tmp.flush();b=p.LoadBoard(tmp.name)
nets={n.GetNetname():n for n in b.GetNetInfo().NetsByNetcode().values()};declared=[];poses={}
for ref,a in recipes.items():
 old=oldfps[ref];f=p.FootprintLoad(str(r/'ENKU.pretty'),a['name']);assert f
 f.SetFPID(p.LIB_ID('ENKU',a['name']));f.SetUuid(p.KIID(old.m_Uuid.AsString()));f.SetReference(ref);f.SetValue(a['value']);f.SetPath(old.GetPath());f.SetAttributes(old.GetAttributes()|p.FP_SMD);f.SetLocked(old.IsLocked());f.SetPosition(old.GetPosition());f.SetOrientation(old.GetOrientation())
 for key in ['Datasheet','MPN','Manufacturer','Assembly','Voltage','Tuning MPN']:
  if key in a['source_fields']:f.GetField(key).SetText(a['source_fields'][key])
 f.GetField('Description').SetText(a['source_fields'].get('Description',a['description']))
 for key in ['Reference','Value']:
  x=f.GetField(key);z=old.GetField(key);x.SetUuid(p.KIID(z.m_Uuid.AsString()));x.SetPosition(z.GetPosition());x.SetTextAngle(z.GetTextAngle());x.SetVisible(z.IsVisible());x.SetTextSize(z.GetTextSize());x.SetTextThickness(z.GetTextThickness())
 pool=list(old.Pads())
 for pad in f.Pads():
  same=[x for x in pool if x.GetNumber()==pad.GetNumber()];assert same
  z=min(same,key=lambda x:(x.GetPosition()-pad.GetPosition()).EuclideanNorm());pool.remove(z)
  pad.SetUuid(p.KIID(z.m_Uuid.AsString()));pad.SetNet(nets[z.GetNetname()]);pad.SetPinFunction(z.GetPinFunction());pad.SetPinType(z.GetPinType())
  declared.append(dict(uuid=pad.m_Uuid.AsString(),ref=ref,number=pad.GetNumber(),net=pad.GetNetname(),before_position=xy(z.GetPosition()),after_position=xy(pad.GetPosition()),before_size=xy(z.GetSize()),after_size=xy(pad.GetSize()),before_angle=z.GetOrientationDegrees(),after_angle=pad.GetOrientationDegrees(),before_shape=z.GetShape(),after_shape=pad.GetShape()))
 assert not pool
 poses[ref]=dict(before_attributes=old.GetAttributes(),after_attributes=f.GetAttributes(),dnp_preserved=bool(old.GetAttributes()&p.FP_DNP)==bool(f.GetAttributes()&p.FP_DNP))
 b.Add(f)
p.SaveBoard(str(r/'enku-mainboard-r0.1.kicad_pcb'),b)
unchanged=['ENKU.kicad_sym','enku-mainboard-r0.1.kicad_pro','enku-mainboard-r0.1.kicad_sch','fp-lib-table','sym-lib-table','enku-mainboard-r0.1.kicad_dru']
for file in (prior/'ENKU.pretty').glob('*.kicad_mod'):unchanged.append(str(file.relative_to(prior)))
unchanged.append('connectors.kicad_sch')
report=dict(revision='R127',source_R126_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),recipes=recipes,patterns=patterns,declared_pads=declared,footprint_attributes=poses,unchanged_files={x:hashlib.sha256((prior/x).read_bytes()).hexdigest() for x in unchanged},routed_copper_changes=[],schematic_net_changes=[],CC_specific_land_process_qualified=False,assembly_process_qualified=False,fabrication_ready=False)
(c/'applied_component_pass_R127.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(components=len(recipes),resistors=3,capacitors=len(cap_parts),declared_value_changes={'C4':['10uF 10V','1uF 25V']},declared_pads=len(declared)),indent=2))
