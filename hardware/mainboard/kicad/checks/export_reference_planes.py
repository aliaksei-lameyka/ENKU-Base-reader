"""Export native filled GND polygons and recover real holes from fractured fill."""
import json,sys,gzip
from pathlib import Path
import pcbnew as p
b=p.LoadBoard(sys.argv[1]);result={}
def xy(v):return [p.ToMM(v.x),p.ToMM(v.y)]
for layer in [p.In1_Cu,p.In2_Cu]:
 out=[]
 for z in b.Zones():
  if z.GetIsRuleArea() or z.GetNetname()!='GND' or not z.GetLayerSet().Contains(layer):continue
  s=p.SHAPE_POLY_SET(z.GetFilledPolysList(layer));s.Unfracture()
  for i in range(s.OutlineCount()):out.append({'shell':[xy(s.COutline(i).CPoint(j)) for j in range(s.COutline(i).PointCount())],'holes':[[xy(s.CHole(i,k).CPoint(j)) for j in range(s.CHole(i,k).PointCount())] for k in range(s.HoleCount(i))]})
 result[str(layer)]=out
Path(sys.argv[2]).write_bytes(gzip.compress(json.dumps(result).encode(),mtime=0))
print('Reference GND layers',[(k,len(v)) for k,v in result.items()])
