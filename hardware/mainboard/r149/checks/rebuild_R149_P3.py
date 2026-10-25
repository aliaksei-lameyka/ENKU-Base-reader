#!/usr/bin/env python3
"""ENKU R149-P3: M03 controlled RF/fastener placement and 4 switch bridges. NO FAB."""
from pathlib import Path
import hashlib,re,uuid,shutil,json
root=Path(__file__).resolve().parents[2]
source=root/'r149/p2/kicad/enku-mainboard-r0.1.kicad_pcb'
dest=root/'r149/p3/kicad'
sha_p2='0d14749300afaf7968925c6836f9fb24b607e2307354cd70e41281138da17399'
data=source.read_bytes()
assert hashlib.sha256(data).hexdigest()==sha_p2,'Wrong P2 source; refuse patch.'
text=data.decode('utf-8')
moves={
    'SW3':('(at 21.5500 68.0000 -90)','(at 21.5500 73.0000 -90)'),
    'SW5':('(at 73.4500 68.0000 90)','(at 73.4500 73.0000 90)'),
    'H4':('(at 72 116.5)','(at 73.5 116.5)'),
}
starts=[m.start() for m in re.finditer(r'^\t\(',text,re.M)]+[len(text)]
patches=[];found=set()
for i,j in zip(starts,starts[1:]):
    blk=text[i:j]
    if not blk.startswith('\t(footprint'):continue
    mr=re.search(r'\(property "Reference" "([^"\n]+)"',blk)
    if not mr or mr[1] not in moves:continue
    ref=mr[1];old,new=moves[ref]
    assert old in blk[:mr.start()],(ref,old)
    patches.append((i,j,blk.replace(old,new,1)));found.add(ref)
assert found==set(moves),found
for i,j,sub in sorted(patches,reverse=True):text=text[:i]+sub+text[j:]
text=text.replace('(rev "R149-P2 PARTIAL REROUTE / NO FAB")',
                  '(rev "R149-P3 RF AND MOUNT PLACEMENT / NO FAB")',1)
assert text.count('R149-P3 RF AND MOUNT PLACEMENT / NO FAB')==1
tracks=[
 ('BTN_L2','F.Cu',(22.275,78.2),(22.275,81.8),0.2),
 ('GND','F.Cu',(20.825,78.2),(20.825,81.8),0.2),
 ('BTN_R2','F.Cu',(72.725,78.2),(72.725,83.2),0.2),
 ('GND','F.Cu',(74.175,78.2),(74.175,83.2),0.2),
]
added=[]
for net,layer,st,en,w in tracks:
    obj=f'''\t(segment
\t\t(start {st[0]:.4f} {st[1]:.4f})
\t\t(end {en[0]:.4f} {en[1]:.4f})
\t\t(width {w:.4f})
\t\t(layer "{layer}")
\t\t(net "{net}")
\t\t(uuid "{uuid.uuid5(uuid.NAMESPACE_URL,'ENKU-R149-P3:'+net+str(st)+str(en))}")
\t)
'''
    assert obj not in text;added.append(obj)
idx=text.rfind('\n)')
assert idx>100000
text=text[:idx]+'\n'+''.join(added)+text[idx:]
assert len(re.findall(r'^\t\(footprint\s',text,re.M))==141
assert len(re.findall(r'^\t\(segment\s',text,re.M))==2959
assert len(re.findall(r'^\t\(via\s',text,re.M))==385
assert '(at 69.4600 94.2200)' in text and '(at 65.0000 117.3250)' in text
shutil.copytree(root/'r149/p2/kicad',dest,dirs_exist_ok=True)
(dest/source.name).write_text(text)
info={'revision':'R149-P3','state':'NO_FAB','input_sha256':sha_p2,
      'output_sha256':hashlib.sha256(text.encode()).hexdigest(),
      'footprint_moves_kicad_mm':{'SW3':[21.55,73.0],'SW5':[73.45,73.0],'H4':[73.5,116.5]},
      'preserved':['J3','J5','U1','board outline','antenna keepout'],
      'added_trace_segments':tracks,'zones':'not qualified without KiCad 10.0.7 refill',
      'case_standoff_change_required_mm':{'H4_dx':1.5},
      'button_case_aperture_change_required_mm':{'SW3_dy':5.0,'SW5_dy':5.0},
      'manufacturing_ready':False}
(dest.parent/'manifest.json').write_text(json.dumps(info,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'sha':info['output_sha256'],'moves':info['footprint_moves_kicad_mm'],'added_segments':len(tracks),'strict_NO_FAB':True}))
