#!/usr/bin/env python3
"""R149-P1 deterministic 5-component J3 clearance placement. NO FAB / NO ROUTING."""
import hashlib,re,shutil,json
from pathlib import Path
MAINBOARD=Path(__file__).resolve().parents[2]
source=MAINBOARD/'r149/kicad/enku-mainboard-r0.1.kicad_pcb'
dest=MAINBOARD/'r149/p1/kicad'
P0='764cbe8258df7e76f14936407ecabc2fa86e8a80bdc42c01774b26bb23dcc977'
P1='a670b7cfb921fa7de7305672b708c1e12834ae097c8463479f267df2d339dfc9'
changes={
'J1':('69.8 94.5 90','74.0000 105.0000 90'),
'J8':('66.95 91.5','72.0000 110.5000'),
'C12':('63.125 94.4','62.0000 99.0000'),
'L1':('61.2 91 -90','60.7000 91.2000 -90'),
'U4':('58 91','57.6500 91.0000')}
original=source.read_bytes()
assert hashlib.sha256(original).hexdigest()==P0,'R149-P0 checksum mismatch'
s=original.decode()
markers=[m.start() for m in re.finditer(r'^\t\(',s,re.M)]+[len(s)]
patches=[];found=set()
for i,j in zip(markers,markers[1:]):
 block=s[i:j]
 if not block.startswith('\t(footprint'):continue
 ref=re.search(r'\(property "Reference" "([^"]+)"',block)
 if not ref or ref[1] not in changes:continue
 old,new=changes[ref[1]]
 assert '(at '+old+')' in block[:ref.start()],ref[1]
 patches.append((i,j,block.replace('(at '+old+')','(at '+new+')',1)))
 found.add(ref[1])
assert found==set(changes)
for i,j,rep in reversed(patches):s=s[:i]+rep+s[j:]
s=s.replace('(rev "R149-P0 M03 PLACEMENT ONLY / NO FAB")',
            '(rev "R149-P1 M03 J3 CLEARANCE / NO FAB")',1)
out=s.encode()
assert hashlib.sha256(out).hexdigest()==P1,'R149-P1 checksum mismatch'
shutil.copytree(MAINBOARD/'r148/kicad',dest,dirs_exist_ok=True)
(dest/source.name).write_bytes(out)
for ref,xys in {'J3':'69.4600 94.2200','J5':'65.0000 117.3250',
 'SW3':'21.5500 68.0000 -90','SW4':'21.5500 80.0000 -90',
 'SW5':'73.4500 68.0000 90','SW6':'73.4500 80.0000 90'}.items():
 assert re.search(r'\(property "Reference" "'+ref+r'"',out.decode())
 assert '(at '+xys+')' in out.decode()
print('R149-P1 deterministic placement generated; STILL UNROUTED / NO FAB',P1)
