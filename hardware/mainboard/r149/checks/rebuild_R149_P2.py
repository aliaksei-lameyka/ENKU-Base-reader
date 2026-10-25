#!/usr/bin/env python3
"""R149-P2 source-bound isolate stale copper shorts; preserve M03; NO FAB."""
import re,uuid,hashlib,pathlib,shutil,json
root=pathlib.Path(__file__).resolve().parents[2]
src=root/'r149/p1/kicad/enku-mainboard-r0.1.kicad_pcb'
dst=root/'r149/p2/kicad'
original=src.read_bytes()
P1=hashlib.sha256(original).hexdigest()
assert P1=='a670b7cfb921fa7de7305672b708c1e12834ae097c8463479f267df2d339dfc9',P1
s=original.decode()
starts=[m.start() for m in re.finditer(r'^\t\(',s,re.M)]+[len(s)]
rejected_vias={
 ('REG_MODE',(56.3,90.25)),
 ('REG_MODE',(63.15,92.35)),
 ('3V3_SYS',(62.3,95.9)),
 ('GND',(21.5,81.8)),
}
rejected_traces={
 ('SYS_EN','F.Cu',(64.85,91),(64.85,92)),
 ('SYS_EN','F.Cu',(64.85,92),(65.2,92.35)),
 ('SYS_EN','F.Cu',(65.2,92.35),(68.7,92.35)),
 ('SYS_EN','F.Cu',(68.7,92.35),(70.25,90.8)),
 ('BAT_TS','F.Cu',(69.8,88.4),(66.95,91.5)),
 ('REG_MODE','F.Cu',(57.1,90.5),(56.55,90.4)),
 ('REG_MODE','F.Cu',(56.55,90.4),(56.3,90.25)),
 ('REG_MODE','In1.Cu',(56.8,90.75),(56.3,90.25)),
 ('REG_MODE','F.Cu',(63,92.2),(63.15,92.35)),
 ('REG_MODE','In1.Cu',(63.15,92.35),(61.25,92.35)),
 ('REG_FB','F.Cu',(56.5,91.5),(56.5,92.7)),
 ('3V3_SYS','F.Cu',(62.3,94.4),(62.3,95.9)),
 ('3V3_SYS','B.Cu',(62.3,95.9),(59,92.6)),
}
removed=[];kept=[]
for a,b in zip(starts,starts[1:]):
 t=s[a:b]
 if t.startswith('\t(via'):
  mm=re.search(r'\(at ([\d.-]+) ([\d.-]+)\)',t)
  nm=re.search(r'\(net "([^"]+)"\)',t)
  key=(nm[1],(float(mm[1]),float(mm[2]))) if mm and nm else None
  if key in rejected_vias:
   removed.append(('via',key));continue
 if t.startswith('\t(segment'):
  st=re.search(r'\(start ([\d.-]+) ([\d.-]+)\)',t)
  en=re.search(r'\(end ([\d.-]+) ([\d.-]+)\)',t)
  net=re.search(r'\(net "([^"]+)"\)',t)
  layer=re.search(r'\(layer "([^"]+)"\)',t)
  if st and en and net and layer:
   v=(net[1],layer[1],(float(st[1]),float(st[2])),(float(en[1]),float(en[2])))
   if v in rejected_traces or (v[0],v[1],v[3],v[2]) in rejected_traces:
    removed.append(('segment',v));continue
 kept.append(t)
assert len([x for x in removed if x[0]=='via'])==4,removed
assert len([x for x in removed if x[0]=='segment'])==len(rejected_traces),(len(removed),removed)
new_paths=[
 ('SYS_EN','F.Cu',(64.85,91.0),(64.85,90.70),0.2),
 ('SYS_EN','F.Cu',(64.85,90.70),(70.25,90.70),0.2),
 ('SYS_EN','F.Cu',(70.25,90.70),(70.25,90.8),0.2),
 ('BTN_L2','F.Cu',(22.275,81.8),(22.275,83.2),0.2),
 ('GND','F.Cu',(20.825,81.8),(20.825,83.2),0.2),
]
for net,ly,start,end,width in new_paths:
 uid=uuid.uuid5(uuid.NAMESPACE_DNS,'ENKU-R149-P2-'+net+str(start)+str(end))
 kept.insert(-1,f'\t(segment\n\t\t(start {start[0]:.4f} {start[1]:.4f})\n\t\t(end {end[0]:.4f} {end[1]:.4f})\n\t\t(width {width:.4f})\n\t\t(layer "{ly}")\n\t\t(net "{net}")\n\t\t(uuid "{uid}")\n\t)\n')
out=s[:starts[0]]+''.join(kept)
out=out.replace('(rev "R149-P1 M03 J3 CLEARANCE / NO FAB")','(rev "R149-P2 PARTIAL REROUTE / NO FAB")',1)
assert out.count('R149-P2 PARTIAL REROUTE')==1
assert len(re.findall(r'^\t\(footprint ',out,re.M))==141
assert len(re.findall(r'^\t\(segment\s',out,re.M))==2963-len(rejected_traces)+len(new_paths)
assert len(re.findall(r'^\t\(via\s',out,re.M))==389-4
shutil.copytree(root/'r149/p1/kicad',dst,dirs_exist_ok=True)
(dst/src.name).write_text(out)
manifest={'revision':'R149-P2','status':'NO_FAB','parent_p1_sha256':P1,'p2_sha256':hashlib.sha256(out.encode()).hexdigest(),'removed':removed,'added':new_paths,'unchanged_footprints':True,'zones':'STALE until native refill','electrical':'NOT QUALIFIED, DRC expected FAIL'}
(root/'r149/p2/manifest.json').write_text(json.dumps(manifest,indent=2,default=str)+'\n')
print(json.dumps({k:manifest[k]for k in ['revision','p2_sha256','status']},indent=2))
