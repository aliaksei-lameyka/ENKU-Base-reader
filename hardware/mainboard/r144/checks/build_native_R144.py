"""One-shot native R144 placement proposal; never runs during verification."""
from pathlib import Path
import hashlib,json,sys,xml.etree.ElementTree as E
import pcbnew as p
k=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();out.mkdir(parents=True,exist_ok=True)
pcb=k/'enku-mainboard-r0.1.kicad_pcb';pro=k/'enku-mainboard-r0.1.kicad_pro';project=pro.read_bytes()
assert hashlib.sha256(pcb.read_bytes()).hexdigest()=='3319ad4325e1856a923734be7a6f9eb6434ebbeaf3ca9d5f2b9e3615adb3b266'
spec=json.loads((k.parent/'new_parts_R144.json').read_text());b=p.LoadBoard(str(pcb));fp={f.GetReference():f for f in b.GetFootprints()};cs={c.get('ref'):c for c in E.parse(out/'netlist.xml').findall('./components/comp')}
for name in ['RESET_SENSE','RESET_CT','REG_MODE','REG_FB_TOP']:
 if not b.FindNet(name):b.Add(p.NETINFO_ITEM(b,name))
def position(f,pos,ang=0):f.SetOrientationDegrees(ang);f.SetPosition(p.VECTOR2I(*(p.FromMM(v)for v in pos)))
def fields(f,ref):
 c=cs[ref];vals={a.get('name'):a.text or ''for a in c.findall('./fields/field')};vals.update(Value=c.findtext('value'),Footprint=c.findtext('footprint'),Datasheet=c.findtext('datasheet')or'~',Description=c.findtext('description')or'')
 for name,val in vals.items():
  if name=='Reference':continue
  if name=='Value':f.SetValue(val)
  elif name=='Footprint':f.SetFPIDAsString(val)
  else:f.SetField(name,val)
  fld=f.GetField(name)
  if fld:fld.SetVisible(False)
 f.Reference().SetVisible(False);f.Value().SetVisible(False)
old=fp['U11'];u=p.FootprintLoad(str(k/'ENKU.pretty'),'TPS3890_TI_DSE0006A_SMD_LEFT');u.SetReference('U11');u.SetPath(old.GetPath());fields(u,'U11');position(u,[44.5,67.5])
for a in u.Pads():
 if a.GetNumber():a.SetNet(b.FindNet({'1':'RESET_SENSE','2':'GND','3':'3V3_SYS','4':'3V3_SYS','5':'RESET_CT','6':'ESP_EN'}[a.GetNumber()]))
b.Add(u)
for ref in ['R14','R15','C15']:fields(fp[ref],ref)
position(fp['C15'],[46,69.2]);fp['C37'].Reference().SetPosition(p.VECTOR2I(p.FromMM(40.8),p.FromMM(68.5)))
for ref,num,net in [('R14','1','REG_FB_TOP'),('U4','2','REG_MODE')]:
 next(a for a in fp[ref].Pads()if a.GetNumber()==num).SetNet(b.FindNet(net))
for ref,s in spec['new_parts'].items():
 f=p.Cast_to_FOOTPRINT(fp[s['template']].Duplicate(False));f.SetReference(ref);fields(f,ref);position(f,s['position_mm'],s['angle_deg']);f.SetDNP(ref=='R99')
 path=p.KIID_PATH();template=fp['R90']if s['sheet']=='mcu_io'else fp['R15']
 for id in template.GetPath().AsString().strip('/').split('/')[:-1]+[s['symbol_uuid']]:path.push_back(p.KIID(id))
 f.SetPath(path)
 for a in f.Pads():
  if a.GetNumber():a.SetNet(b.FindNet(s['nets'][a.GetNumber()]))
 b.Add(f)
remove={'0083ac47-c742-471c-a5de-7ecf908ab2c5','20595b77-d773-4399-b0db-cc860092c9ce','3a379b37-eee2-4199-9184-2b037ba728e4','49873983-cc14-4eb9-a292-d2e8cf9623f9','95cf7b7d-8dbf-49ef-b696-e4b281428b19','dae5d3c4-9c45-4213-aef0-d0aba34cec4e','e0e7401b-1e58-4617-a5d1-9f80bee8cfdd','edd1215d-81de-43d5-b85f-52930fe052e5','25898504-e081-4c54-8f0e-07a37841551b','d84c0087-b62c-4a4b-b1f3-a8c435334f32','8aac9b0d-0e78-4fec-bbc4-63ba18f76def'}
changed=[(next(a for a in fp['R14'].Pads()if a.GetNumber()=='1'),'3V3_SYS'),(next(a for a in fp['U4'].Pads()if a.GetNumber()=='2'),'GND')]
for t in b.GetTracks():
 if not isinstance(t,p.PCB_VIA)and any(t.GetNetname()==net and(a.HitTest(t.GetStart())or a.HitTest(t.GetEnd()))for a,net in changed):remove.add(t.m_Uuid.AsString())
b.GetTitleBlock().SetRevision('R144 - ENGINEERING / NO FAB')
for t in list(b.GetTracks()):
 if t.m_Uuid.AsString()in remove:b.Remove(t)
b.Remove(old)
try:p.SaveBoard(str(pcb),b)
finally:pro.write_bytes(project)
(out/'placement_changes.json').write_text(json.dumps(dict(removed_copper_UUIDs=sorted(remove),removed_U11_pad_UUIDs=[a.m_Uuid.AsString()for a in old.Pads()],source='R143',status='UNROUTED PROPOSAL'),indent=2)+'\n')
print('Placed R144 proposal; native DRC and routing required')
