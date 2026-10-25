#!/usr/bin/env python3
"""ENKU R149-P4: SW4 via detour and J5 silk relocated. NO FAB."""
import re,hashlib,uuid,shutil,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
src=root/'r149/p3/kicad/enku-mainboard-r0.1.kicad_pcb'
dst=root/'r149/p4/kicad'
P3='8630b47b551d38147883cfcd1b68e6e4ede7613ea374c1353a826dc0a2cfad86'
assert hashlib.sha256(src.read_bytes()).hexdigest()==P3,'P3 source changed'
s=src.read_text()
start=s.find('\n\t(footprint "ENKU:USB4215_03_A_GCT_REVA"')
end=s.find('\n\t(footprint',start+3)
assert start>0 and end>start
j5=s[start:end]
old_ref='(property "Reference" "J5"\n\t\t\t(at 6.8 -0.825 0)'
new_ref='(property "Reference" "J5"\n\t\t\t(at -8 -0.825 0)'
assert j5.count(old_ref)==1
s=s[:start]+j5.replace(old_ref,new_ref,1)+s[end:]
pattern=r'\n\t\(segment\s+\(start 22\.2750 78\.2000\)\s+\(end 22\.2750 81\.8000\)\s+\(width 0\.2000\)\s+\(layer "F.Cu"\)\s+\(net "BTN_L2"\)\s+\(uuid "[^"]+"\)\s+\)'
assert len(re.findall(pattern,s))==1
s=re.sub(pattern,'',s,count=1)
paths=[((22.275,78.2),(21.9,79.0)),((21.9,79.0),(21.9,81.0)),((21.9,81.0),(22.275,81.8))]
new=[]
for a,b in paths:
 uid=uuid.uuid5(uuid.NAMESPACE_URL,f'ENKU-R149-P4:BTN_L2:{a}:{b}')
 new.append(f'''\t(segment
\t\t(start {a[0]:.4f} {a[1]:.4f})
\t\t(end {b[0]:.4f} {b[1]:.4f})
\t\t(width 0.2000)
\t\t(layer "F.Cu")
\t\t(net "BTN_L2")
\t\t(uuid "{uid}")
\t)
''')
pos=s.rfind('\n)')
assert pos>100000
s=s[:pos]+'\n'+''.join(new)+s[pos:]
s=s.replace('(rev "R149-P3 RF AND MOUNT PLACEMENT / NO FAB")','(rev "R149-P4 BUTTON DETOUR / NO FAB")',1)
assert len(re.findall(r'^\t\(footprint\s',s,re.M))==141
assert len(re.findall(r'^\t\(segment\s',s,re.M))==2961
assert len(re.findall(r'^\t\(via\s',s,re.M))==385
assert '(at 69.4600 94.2200)' in s and '(at 65.0000 117.3250)' in s
assert s.startswith('(kicad_pcb\n')
shutil.copytree(root/'r149/p3/kicad',dst,dirs_exist_ok=True)
(dst/src.name).write_text(s)
manifest={'revision':'R149-P4','state':'HOLD_NO_FAB','parent_sha':P3,
 'pcb_sha256':hashlib.sha256(s.encode()).hexdigest(),'changed_nets':['BTN_L2'],
 'J5_ref_move':{'original':[71.8,116.5],'new':[57.0,116.5]},
 'SW4_detour':paths,'fabrication_ready':False}
(dst.parent/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
