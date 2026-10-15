"""Native front courtyard geometry and J1 wire-interface manufacturing flags."""
import pcbnew as p,json,sys
from pathlib import Path
b=p.LoadBoard(sys.argv[1]);rows=[];j1=None
for f in b.GetFootprints():
 if f.GetReference()=='J1':
  j1=dict(attributes=f.GetAttributes(),pads=[dict(number=a.GetNumber(),layers=[p.LayerName(l)for l in a.GetLayerSet().Seq()],pos=[p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)],size=[p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)],net=a.GetNetname())for a in f.Pads()])
 if f.GetLayer()!=p.F_Cu:continue
 pts=[]
 for a in f.GraphicalItems():
  if a.GetLayer()!=p.F_CrtYd:continue
  bb=a.GetBoundingBox();pts.append([p.ToMM(bb.GetX()),p.ToMM(bb.GetY()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())])
 if pts:rows.append(dict(ref=f.GetReference(),bbox=[min(a[0]for a in pts),min(a[1]for a in pts),max(a[2]for a in pts),max(a[3]for a in pts)]))
Path(sys.argv[2]).write_text(json.dumps(dict(front_courtyards=rows,J1=j1),indent=2)+'\n')
