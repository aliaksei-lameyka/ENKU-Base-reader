"""Export refilled GND copper and actual native zone connection requests."""
import gzip, json, sys
from pathlib import Path
import pcbnew as p

b = p.LoadBoard(sys.argv[1])
result = {}
def xy(v): return [p.ToMM(v.x), p.ToMM(v.y)]
for layer in [p.F_Cu, p.B_Cu, p.In1_Cu, p.In2_Cu]:
    rows = []
    for z in b.Zones():
        if z.GetIsRuleArea() or z.GetNetname() != 'GND' or not z.GetLayerSet().Contains(layer):
            continue
        filled = p.SHAPE_POLY_SET(z.GetFilledPolysList(layer))
        filled.Unfracture()
        for i in range(filled.OutlineCount()):
            rows.append(dict(zone=z.GetZoneName(), solid_connection_requested=z.GetPadConnection() == p.ZONE_CONNECTION_FULL,
                shell=[xy(filled.COutline(i).CPoint(j)) for j in range(filled.COutline(i).PointCount())],
                holes=[[xy(filled.CHole(i,k).CPoint(j)) for j in range(filled.CHole(i,k).PointCount())] for k in range(filled.HoleCount(i))]))
    result[str(layer)] = rows
Path(sys.argv[2]).write_bytes(gzip.compress(json.dumps(result).encode(), mtime=0))
print('Exported actual filled thermal GND copper, all four copper layers')
