import json, sys, math, re, tempfile
from pathlib import Path
import pcbnew as p

def xy(v): return [p.ToMM(v.x),p.ToMM(v.y)]
def iu(v): return int(round(v * 1000000))
def polys(s):
    return [[xy(s.COutline(i).CPoint(j)) for j in range(s.COutline(i).PointCount())] for i in range(s.OutlineCount())]

def export(board, out):
    b=p.LoadBoard(str(board)); pads=[]; tracks=[]; zones=[]
    for f in b.GetFootprints():
        for a in f.Pads():
            layers=[l for l in a.GetLayerSet().Seq() if p.IsCopperLayer(l)]
            pads.append(dict(uuid=a.m_Uuid.AsString(),ref=f.GetReference(),number=a.GetNumber(),net=a.GetNetname(),code=a.GetNetCode(),pos=xy(a.GetPosition()),size=xy(a.GetSize()),drill=xy(a.GetDrillSize()),angle=a.GetOrientationDegrees(),layers=layers,polygons={str(l):polys(a.GetEffectivePolygon(l,p.ERROR_OUTSIDE)) for l in layers}))
    for t in b.GetTracks():
        via=isinstance(t,p.PCB_VIA)
        tracks.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),code=t.GetNetCode(),start=xy(t.GetStart()),end=xy(t.GetEnd()),width=p.ToMM(t.GetWidth(p.F_Cu) if via else t.GetWidth()),layer=t.GetLayer(),via=via,drill=p.ToMM(t.GetDrill()) if via else 0))
    for z in list(b.Zones())+[z for f in b.GetFootprints() for z in f.Zones()]:
        zones.append(dict(net=z.GetNetname(),layers=list(z.GetLayerSet().Seq()),rule=z.GetIsRuleArea(),no_tracks=z.GetDoNotAllowTracks(),no_vias=z.GetDoNotAllowVias(),polygons=polys(z.Outline())))
    bb=b.GetBoardEdgesBoundingBox()
    data=dict(version=p.Version(),pads=pads,tracks=tracks,zones=zones,bbox=[p.ToMM(bb.GetX())+.025,p.ToMM(bb.GetY())+.025,p.ToMM(bb.GetRight())-.025,p.ToMM(bb.GetBottom())-.025],footprints={f.GetReference():dict(uuid=f.m_Uuid.AsString(),pos=xy(f.GetPosition()),angle=f.GetOrientationDegrees(),lib=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())) for f in b.GetFootprints()})
    conn=b.GetConnectivity(); visited=set(); components=[]
    for a in list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads()]:
        uid=a.m_Uuid.AsString()
        if uid in visited or a.GetNetCode()==0:continue
        group={i.m_Uuid.AsString() for i in conn.GetConnectedItems(a)}|{uid}
        visited.update(group);components.append(sorted(group))
    data['components']=components
    outlines=p.SHAPE_POLY_SET(); b.GetBoardPolygonOutlines(outlines,False)
    data['board_outline']=polys(outlines)
    Path(out).write_text(json.dumps(data,indent=2))

def apply(board, plan, out):
    j=json.loads(Path(plan).read_text())
    remove=set(j.get('remove_tracks',[]))
    if remove:
        source=Path(board).read_text(); found=set()
        def drop(m):
            uid=re.search(r'\(uuid "([^"]+)"\)',m.group(0))
            if uid and uid[1] in remove:found.add(uid[1]);return ''
            return m.group(0)
        source=re.sub(r'^\t\((?:segment|via)\n.*?^\t\)\n',drop,source,flags=re.M|re.S)
        if found!=remove:raise ValueError('Removal UUIDs not found: '+str(remove-found))
        with tempfile.NamedTemporaryFile(mode='w',suffix='.kicad_pcb') as temp:
            temp.write(source);temp.flush();b=p.LoadBoard(temp.name)
    else:b=p.LoadBoard(str(board))
    codes={t.GetNetname():t.GetNetCode() for t in b.GetTracks()}
    codes.update({a.GetNetname():a.GetNetCode() for f in b.GetFootprints() for a in f.Pads()})
    via_positions={(t.GetNetname(),tuple(xy(t.GetPosition()))) for t in b.GetTracks() if isinstance(t,p.PCB_VIA)}
    for r in j['routes']:
        for seg in r.get('segments',[]):
            t=p.PCB_TRACK(b); t.SetStart(p.VECTOR2I(*(iu(c) for c in seg['a']))); t.SetEnd(p.VECTOR2I(*(iu(c) for c in seg['b']))); t.SetWidth(iu(r.get('width',.2))); t.SetLayer(seg['layer']); t.SetNetCode(codes[r['net']]); b.Add(t)
        for v in r.get('vias',[]):
            if (r['net'],tuple(v)) in via_positions: continue
            t=p.PCB_VIA(b); t.SetPosition(p.VECTOR2I(*(iu(c) for c in v))); t.SetWidth(p.F_Cu,iu(r.get('via_diameter',.6))); t.SetDrill(iu(.3)); t.SetViaType(p.VIATYPE_THROUGH); t.SetLayerPair(p.F_Cu,p.B_Cu); t.SetNetCode(codes[r['net']]); b.Add(t)
            via_positions.add((r['net'],tuple(v)))
    p.SaveBoard(str(out),b)

if __name__=='__main__':
    if sys.argv[1]=='export': export(*sys.argv[2:])
    elif sys.argv[1]=='apply': apply(*sys.argv[2:])
