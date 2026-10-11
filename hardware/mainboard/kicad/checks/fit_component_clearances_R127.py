"""Move only the declared EPD_VCI via vertex to clear the resized C27 land."""
import json
from pathlib import Path
import pcbnew as p
r=Path(__file__).resolve().parents[1];c=r/'checks';path=r/'enku-mainboard-r0.1.kicad_pcb';b=p.LoadBoard(str(path))
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def vec(a):return p.VECTOR2I(*(int(round(x*1e6)) for x in a))
a=json.loads((c/'applied_component_pass_R127.json').read_text());changes=[]
for t in b.GetTracks():
 before=[xy(t.GetStart()),xy(t.GetEnd())]
 if t.GetNetname()!='EPD_VCI' or [50.1,32.45] not in before:continue
 after=[[50.2,32.4] if x==[50.1,32.45] else x for x in before]
 if isinstance(t,p.PCB_VIA):t.SetPosition(vec(after[0]))
 else:t.SetStart(vec(after[0]));t.SetEnd(vec(after[1]))
 changes.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),before=before,after=after))
assert len(changes)==3
p.SaveBoard(str(path),b);a['routed_copper_changes']=changes
(c/'applied_component_pass_R127.json').write_text(json.dumps(a,indent=2)+'\n');print('Declared via + two attached segments:',len(changes))
