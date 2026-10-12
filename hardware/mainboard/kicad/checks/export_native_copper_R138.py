"""Export real refilled four-layer copper polygons with native hole recovery."""
import gzip,json,sys
from pathlib import Path
import pcbnew as p
b=p.LoadBoard(sys.argv[1]);layers={}
def xy(v):return[p.ToMM(v.x),p.ToMM(v.y)]
for layer in [p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]:
 rows=[]
 for z in b.Zones():
  if z.GetIsRuleArea()or not z.GetLayerSet().Contains(layer):continue
  s=p.SHAPE_POLY_SET(z.GetFilledPolysList(layer));s.Unfracture()
  for i in range(s.OutlineCount()):rows.append(dict(net=z.GetNetname(),zone_uuid=z.m_Uuid.AsString(),shell=[xy(s.COutline(i).CPoint(j))for j in range(s.COutline(i).PointCount())],holes=[[xy(s.CHole(i,k).CPoint(j))for j in range(s.CHole(i,k).PointCount())]for k in range(s.HoleCount(i))]))
 layers[str(layer)]=rows
graphics=list(b.GetDrawings())+[d for f in b.GetFootprints()for d in f.GraphicalItems()]
assert not any(p.IsCopperLayer(d.GetLayer())for d in graphics),'Copper graphics require an explicitly extended exporter'
j=dict(native_kicad=p.Version(),board_thickness_mm=p.ToMM(b.GetDesignSettings().GetBoardThickness()),copper_graphics_count=0,filled_zones=layers)
Path(sys.argv[2]).write_bytes(gzip.compress(json.dumps(j).encode(),mtime=0));print('Export native filled copper',[(k,len(v))for k,v in layers.items()])
