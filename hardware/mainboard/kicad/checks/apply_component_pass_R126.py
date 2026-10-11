"""Apply R126 on the accepted R125 source; preserve every routed copper item.

Capacitor lands are an engineering transfer of Yageo's size-based AC reflow
recommendation to the verified CC packages, not CC-specific process approval.
"""
import gzip, hashlib, json, math, re, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p

r=Path(__file__).resolve().parents[1]; c=r/'checks'; prior=r.parent/'ENKU_R125'
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
for file in sources:(c/('source_R125_'+file+'.gz')).write_bytes(gzip.compress((prior/file).read_bytes(),mtime=0))
(c/'netlist_R125_baseline.xml').write_bytes((prior/'checks/netlist_R125.xml').read_bytes())
RURL='https://yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L'
patterns={
 'R_RC0603_YAGEO_REFLOW':dict(size=[.9,.8],pads=[('1',[-.85,0]),('2',[.85,0])],body=[1.6,.8],yard=[1.4,.55],source='Yageo Chip resistors mounting v10, page4/table1: A2.6 B.8 C.9 D.8; centre pitch1.7. RC_L v14 package.',datasheet=RURL),
 'C_CC0603_YAGEO_REFLOW_TRANSFER':dict(size=[.8,.9],pads=[('1',[-.75,0]),('2',[.75,0])],body=[1.6,.8],yard=[1.25,.55],source='Engineering transfer: Yageo AC HiCap X7R/X7S v4 page18 table14, 0603(1): A2.3 B.7 C.8 D.9. Verified CC package L1.6 +/- .1. CC-specific assembly qualification open.',datasheet='https://yageogroup.com/content/datasheet/asset/file/UPY-GPHC_X7R_6_3V-TO-250V'),
 'C_CC0805_YAGEO_REFLOW_TRANSFER':dict(size=[.95,1.4],pads=[('1',[-.925,0]),('2',[.925,0])],body=[2,1.25],yard=[1.5,.825],source='Engineering transfer: Yageo AC HiCap X7R/X7S v4 page18 table14: A2.8 B.9 C.95 D1.4. Verified CC package L2 +/- .2 W1.25 +/- .2. CC-specific assembly qualification open.',datasheet='https://yageogroup.com/content/datasheet/asset/file/UPY-GPHC_X5R_4V-TO-50V'),
 'MBR0530T1G_ONSEMI_CASE425H':dict(size=[.91,1.22],pads=[('1',[-1.635,0]),('2',[1.635,0])],body=[2.69,1.6],yard=[2.19,1.0],source='onsemi MBR0530T1/D rev9 Oct2024, CASE425 issueH 29Feb2024 drawing98ASB42927B: .91 x1.22 lands, centre pitch3.27. Pin1 cathode, pin2 anode.',datasheet='https://www.onsemi.com/pdf/datasheet/mbr0530t1-d.pdf'),
 'TL3342F160QG_ESWITCH_P010632J':dict(size=[1.7,1],pads=[('1',[-3.15,-1.9]),('1',[3.15,-1.9]),('2',[-3.15,1.9]),('2',[3.15,1.9])],body=[5.1,5.1],yard=[4.25,2.8],source='E-Switch TL3342F160QG P010632revJ PCR24740 2021-02-09: X8.0/4.6 Y4.8/2.8. Logical1 BOOT = reference3/4 top row, logical2 GND = reference1/2 bottom row. Drawing numbers reference-only; horizontal common pairs.',datasheet='https://configured-product-images.s3.amazonaws.com/2D/specs/TL3342F160QG.pdf')
}
for name,a in patterns.items():
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

components={x.attrib['ref']:x for x in ET.parse(prior/'checks/netlist_R125.xml').findall('./components/comp')}
recipes={}
for ref,x in components.items():
 value=x.findtext('value')
 if ref.startswith('R') and x.findtext('footprint')=='Resistor_SMD:R_0603_1608Metric' and ref not in ['R70','R71']:
  v=value.split()[0].upper();v='0R' if v=='0R' else v+'R' if re.fullmatch(r'\d+',v) else v
  if '.' in v:
   m=re.fullmatch(r'(\d+)\.(\d+)([RKM])',v);assert m;v=m[1]+m[3]+m[2]
  mpn='RC0603'+('JR-07' if v=='0R' else 'FR-07')+v+'L'
  recipes[ref]=dict(name='R_RC0603_YAGEO_REFLOW',mpn=mpn,manufacturer='Yageo',datasheet=RURL,tolerance='jumper' if v=='0R' else '1%',power_W=.1,value=value,assembly='DNP' if 'DNP' in value else 'FIT',tune_MPN='RC0603FR-0722RL' if 'tune' in value else '')
cap_parts={
 'C2':'CC0805KKX7R6BB105','C4':'CC0805KKX5R6BB106','C5':'CC0805KKX7R8BB475','C6':'CC0603KRX7R9BB104',
 'C7':'CC0805KKX5R8BB106','C8':'CC0805KKX5R6BB475','C9':'CC0805KKX5R6BB106','C10':'CC0603KRX7R9BB104',
 'C11':'CC0805MKX5R6BB226','C12':'CC0805MKX5R6BB226','C13':'CC0805KKX5R6BB106',
 'C24':'CC0805KKX7R8BB475','C25':'CC0805KKX7R8BB475','C26':'CC0805KKX7R8BB475','C31':'CC0805KKX7R8BB475',
 'C35':'CC0603KRX7R9BB472','C37':'CC0603KRX7R9BB104'
}
for ref,mpn in cap_parts.items():
 voltage=50 if mpn.startswith('CC0603') else 25 if '8BB' in mpn else 10
 recipes[ref]=dict(name='C_CC'+('0603' if mpn.startswith('CC0603') else '0805')+'_YAGEO_REFLOW_TRANSFER',mpn=mpn,manufacturer='Yageo',datasheet='https://yageogroup.com/download/specsheet/'+mpn,value=components[ref].findtext('value'),assembly='FIT',rated_voltage_V=voltage,tolerance_percent=20 if 'MKX' in mpn else 10,dielectric='X5R' if 'X5R' in mpn else 'X7R',CC_specific_land_process_qualified=False,effective_capacitance_qualified=False)
for ref in ['D1','D2','D3']:recipes[ref]=dict(name='MBR0530T1G_ONSEMI_CASE425H',mpn='MBR0530T1G',manufacturer='onsemi',datasheet=patterns['MBR0530T1G_ONSEMI_CASE425H']['datasheet'],value='MBR0530T1G',assembly='FIT',VRRM_V=30,IF_AV_A=.5,transient_reverse_voltage_and_thermal_qualified=False)
recipes['SW2']=dict(name='TL3342F160QG_ESWITCH_P010632J',mpn='TL3342F160QG',manufacturer='E-Switch',datasheet=patterns['TL3342F160QG_ESWITCH_P010632J']['datasheet'],value=components['SW2'].findtext('value'),assembly='FIT',rating_V=12,rating_A=.05,operating_force_gf=160)

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
 f.GetField('Description').SetText(a['description'])
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
report=dict(revision='R126',source_R125_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),recipes=recipes,patterns=patterns,declared_pads=declared,footprint_attributes=poses,unchanged_files={x:hashlib.sha256((prior/x).read_bytes()).hexdigest() for x in unchanged},routed_copper_changes=[],schematic_net_changes=[],CC_specific_land_process_qualified=False,assembly_process_qualified=False,fabrication_ready=False)
(c/'applied_component_pass_R126.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(components=len(recipes),resistors=sum(x.startswith('R') for x in recipes),capacitors=len(cap_parts),diodes=3,switches=1,declared_pads=len(declared)),indent=2))
