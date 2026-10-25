#!/usr/bin/env python3
"""R149-P5 ground-only stitching: USB2 and EPD signal routes untouched. NO FAB."""
import re,hashlib,uuid,shutil,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
src=root/'r149/p4/kicad/enku-mainboard-r0.1.kicad_pcb'
dst=root/'r149/p5/kicad'
P4='5a2e3e56ee40fd6efa83e439c53ed9010f2d98f2e013dd1b3876bb5c7ea8347c'
assert hashlib.sha256(src.read_bytes()).hexdigest()==P4,'P4 source changed'
s=src.read_text()
tracks=[
 ('GND','F.Cu',(62.925,99.0),(64.1,97.2),0.25),
 ('GND','F.Cu',(69.85,108.3),(69.65,108.5),0.25),
 ('GND','F.Cu',(69.65,108.5),(66.8,108.5),0.25),
 ('GND','F.Cu',(71.15,104.0),(68.8,104.0),0.45),
 ('GND','F.Cu',(68.8,104.0),(68.8,108.3),0.45),
 ('GND','F.Cu',(68.8,108.3),(69.85,108.3),0.45),
 ('USB_SHIELD','F.Cu',(60.68,114.9),(60.68,118.9),0.25),
 ('USB_SHIELD','F.Cu',(69.32,114.9),(69.32,118.9),0.25),
]
added=[]
for net,layer,a,b,w in tracks:
 uid=uuid.uuid5(uuid.NAMESPACE_URL,f'ENKU-R149-P5:{net}:{a}:{b}')
 added.append(f'''\t(segment
\t\t(start {a[0]:.4f} {a[1]:.4f})
\t\t(end {b[0]:.4f} {b[1]:.4f})
\t\t(width {w:.4f})
\t\t(layer "{layer}")
\t\t(net "{net}")
\t\t(uuid "{uid}")
\t)
''')
pos=s.rfind('\n)');assert pos>100000
s=s[:pos]+'\n'+''.join(added)+s[pos:]
s=s.replace('(rev "R149-P4 BUTTON DETOUR / NO FAB")','(rev "R149-P5 GND CONTACT BRIDGES / NO FAB")',1)
assert s.count('R149-P5 GND CONTACT BRIDGES / NO FAB')==1
assert len(re.findall(r'^\t\(footprint\s',s,re.M))==141
assert len(re.findall(r'^\t\(segment\s',s,re.M))==2969
assert len(re.findall(r'^\t\(via\s',s,re.M))==385
assert '(at 69.4600 94.2200)' in s and '(at 65.0000 117.3250)' in s
shutil.copytree(root/'r149/p4/kicad',dst,dirs_exist_ok=True)
(dst/src.name).write_text(s)
info={'revision':'R149-P5','parent_sha256':P4,'pcb_sha256':hashlib.sha256(s.encode()).hexdigest(),
 'added_ground_and_shield_segments':tracks,'status':'NO_FAB','signal_nets_modified':False,
 'battery_ground_current/thermal':'NOT YET QUALIFIED','manufacturing_ready':False}
(dst.parent/'manifest.json').write_text(json.dumps(info,indent=2)+'\n')
print(json.dumps({k:info[k]for k in ['revision','pcb_sha256','status']},indent=2))
