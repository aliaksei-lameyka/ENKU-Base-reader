"""Apply declared local 45-degree routes and retain all old item identities."""
import json,uuid
from pathlib import Path
import pcbnew as p
r=Path(__file__).resolve().parents[1];c=r/'checks';path=r/'enku-mainboard-r0.1.kicad_pcb';b=p.LoadBoard(str(path));rows=json.loads((c/'local_routes_R126.json').read_text());tracks={x.m_Uuid.AsString():x for x in b.GetTracks()}
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
def vec(x):return p.VECTOR2I(*(int(round(a*1e6)) for a in x))
for q in rows:
 t=tracks[q['uuid']];assert [xy(t.GetStart()),xy(t.GetEnd())]==q['before'] and t.GetNetname()==q['net']
 points=q['points'];t.SetStart(vec(points[0]));t.SetEnd(vec(points[1]))
 for i in range(1,len(points)-1):
  z=p.PCB_TRACK(b);z.SetUuid(p.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'ENKU-R126-'+q['uuid']+'-'+str(i)+'-'+json.dumps(points)))));z.SetStart(vec(points[i]));z.SetEnd(vec(points[i+1]));z.SetWidth(int(round(q['width']*1e6)));z.SetLayer(q['layer']);z.SetNetCode(t.GetNetCode());b.Add(z)
p.SaveBoard(str(path),b);print('Applied local paths:',len(rows),'additional segments:',sum(len(x['points'])-2 for x in rows))
